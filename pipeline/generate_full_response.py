import os
import logging
from pathlib import Path
from datetime import datetime

import boto3

from vision.image_preprocessing import preprocessing_raw_image_double_detect
from vision.claude_ocr import ocr_claude
from utils import (
    empty_folder,
    similarityscore,
    create_tuple_from_string,
    put_image_to_s3,
    check_if_text_complete,
)
from prompts_template.prompt_engineering import (
    get_completion,
    merge_two_texts_into_one,
    text_cleaner,
    question_cleaner,
    get_ocr_status,
    verbal_or_quantitive,
    extract_main_text,
    extract_question,
    structure_response,
    answer_ds_question_with_claude,
    answer_ps_question_with_claude,
    answer_rc_question,
    answer_cr_question,
    answer_sc_question,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client("s3")

BUCKET_LAMBDA = os.environ.get("BUCKET_LAMBDA", "")
BUCKET_PROCESSED_IMG = os.environ.get("BUCKET_PROCESSED_IMG", "")
BASE_DIR = "/tmp/"
PROCESSED_FOLDER = "processed_folder"
FULL_TEXT_FOLDER = "previous_full_passage"
MISSING_TEXT_FOLDER = "missing_passage_folder"


def initialize_directories():
    path_to_processed = os.path.join(BASE_DIR, PROCESSED_FOLDER)
    path_to_previous_text = os.path.join(BASE_DIR, FULL_TEXT_FOLDER)
    path_to_missing_text = os.path.join(BASE_DIR, MISSING_TEXT_FOLDER)
    for path in [path_to_processed, path_to_previous_text, path_to_missing_text]:
        os.makedirs(path, exist_ok=True)
    return path_to_processed, path_to_previous_text, path_to_missing_text


def process_image(file_path):
    path_to_processed, _, _ = initialize_directories()
    file_name = Path(file_path).name
    file_path_processed = os.path.join(path_to_processed, file_name)
    preprocessing_raw_image_double_detect(file_path, file_path_processed)
    return file_path_processed


def upload_image_to_s3(file_path_processed, device_id, file_name):
    put_image_to_s3(file_path_processed, device_id, file_name)
    return f"https://{BUCKET_PROCESSED_IMG}.s3.eu-north-1.amazonaws.com/{device_id}/{file_name}"


def process_complete_question(raw_ocr_result):
    output = get_completion(raw_ocr_result)
    question_type, clean_question = create_tuple_from_string(output)

    answer_handlers = {
        "critical reasoning": answer_cr_question,
        "problem solving": answer_ps_question_with_claude,
        "data sufficiency": answer_ds_question_with_claude,
        "sentence correction": answer_sc_question,
        "reading comprehension": answer_rc_question,
    }

    handler = answer_handlers.get(question_type)
    if handler is None:
        raise ValueError(f"Unknown question type: {question_type}")

    final_response = handler(clean_question)
    answer_choice = structure_response(final_response)
    return clean_question, final_response, answer_choice


def process_incomplete_text(main_text_extracted, question, path_to_previous_text, path_to_missing_text):
    # Clean up incomplete prior texts
    if os.listdir(path_to_previous_text):
        text_full = open(f"{path_to_previous_text}/prior_full_passage.txt", "r").read()
        if not check_if_text_complete(text_full):
            empty_folder(path_to_previous_text)

    # Check if a missing passage fragment already exists
    if os.listdir(path_to_missing_text):
        initial_text = open(f"{path_to_missing_text}/missing_passage.txt", "r").read()
        if similarityscore(initial_text, main_text_extracted) > 0.99:
            return merge_and_process_text(
                initial_text, main_text_extracted, question, path_to_previous_text, path_to_missing_text
            )

    # Check if a complete passage already exists
    if os.listdir(path_to_previous_text):
        text_full = open(f"{path_to_previous_text}/prior_full_passage.txt", "r").read()
        if similarityscore(text_full, main_text_extracted) > 0.99:
            return process_existing_full_text(text_full, question)

    return save_partial_text(main_text_extracted, path_to_missing_text, path_to_previous_text)


def merge_and_process_text(initial_text, main_text_extracted, question, path_to_previous_text, path_to_missing_text):
    complete_text = f"{initial_text}+///+{main_text_extracted}"
    clean_text = merge_two_texts_into_one(complete_text)

    with open(f"{path_to_previous_text}/prior_full_passage.txt", "w") as f:
        f.write(clean_text)
    empty_folder(path_to_missing_text)

    formatted_question = question_cleaner(question)
    full_question = f"{clean_text}\n{formatted_question}"
    final_response = answer_rc_question(full_question)
    answer_choice = structure_response(final_response)
    return full_question, final_response, answer_choice


def process_existing_full_text(text_full, question):
    formatted_question = question_cleaner(question)
    full_question = f"{text_full}\n{formatted_question}"
    final_response = answer_rc_question(full_question)
    answer_choice = structure_response(final_response)
    return full_question, final_response, answer_choice


def save_partial_text(main_text_extracted, path_to_missing_text, path_to_previous_text):
    clean_text = text_cleaner(main_text_extracted)
    with open(os.path.join(path_to_missing_text, "missing_passage.txt"), "w") as f:
        f.write(clean_text)
    empty_folder(path_to_previous_text)
    response = "waiting for the next image to complete the text"
    return clean_text, response, response


def get_response_from_raw_image(file_path):
    current_timestamp = datetime.utcnow().isoformat()
    device_id = file_path.split("/")[-2]
    file_name = Path(file_path).name

    results = {
        "PK": "IMAGE_PROCESSING",
        "SK": current_timestamp,
        "image_key": file_name,
        "status": "processing",
        "error_message": "",
        "original_image": None,
        "processed_image": None,
        "ocr_text": None,
        "response_text": None,
        "answer_choice": None,
        "device_id": device_id,
    }

    original_image_url = f"https://{BUCKET_LAMBDA}.s3.eu-north-1.amazonaws.com/{device_id}/{file_name}"
    results["original_image"] = original_image_url

    path_to_processed, path_to_previous_text, path_to_missing_text = initialize_directories()

    try:
        file_path_processed = process_image(file_path)
        processed_image_url = upload_image_to_s3(file_path_processed, device_id, file_name)
        results["status"] = "success"
        results["error_message"] = "No errors"
        results["processed_image"] = processed_image_url
    except ValueError as e:
        results["status"] = "error"
        results["error_message"] = str(e)
        logger.error(str(e))
        return results

    raw_ocr_result = ocr_claude(processed_image_url)

    if raw_ocr_result is None:
        results["status"] = "error"
        results["error_message"] = "OCR API call failed"
        logger.error("OCR API call failed while processing the image")
        return results

    ocr_status = get_ocr_status(raw_ocr_result)
    if ocr_status == "false":
        results["status"] = "error"
        results["error_message"] = "Unable to extract exam question text from the image"
        logger.error("OCR did not detect valid exam content")
        return results

    verbal_or_quant = verbal_or_quantitive(raw_ocr_result)

    if verbal_or_quant == "verbal":
        main_text_extracted = extract_main_text(raw_ocr_result)
        is_text_complete = check_if_text_complete(main_text_extracted)

        if is_text_complete:
            ocr_text, response_text, answer_choice = process_complete_question(raw_ocr_result)
        else:
            question = extract_question(raw_ocr_result)
            ocr_text, response_text, answer_choice = process_incomplete_text(
                main_text_extracted, question, path_to_previous_text, path_to_missing_text
            )
    else:
        try:
            claude_ocr_result = ocr_claude(processed_image_url)
            ocr_text, response_text, answer_choice = process_complete_question(claude_ocr_result)
        except Exception as e:
            results["status"] = "error"
            results["error_message"] = str(e)
            logger.error(f"Error during quantitative processing: {e}")
            return results

    results["status"] = "success"
    results["error_message"] = "No errors"
    results["ocr_text"] = ocr_text
    results["response_text"] = response_text
    results["answer_choice"] = answer_choice
    return results
