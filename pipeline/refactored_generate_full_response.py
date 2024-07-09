import os
from datetime import datetime
from pathlib import Path
import logging
import numpy as np
import os
from pathlib import Path


from vision.image_preprocessing_V2 import (
    preprocessing_raw_image_double_detect,
)

from vision.openai_OCR import openai_ocr, process_ocr_content

from utils import (
    check_folder_empty,
    create_folder,
    empty_folder,
    similarityscore,
    create_tuple_from_string,
    put_image_to_s3,
)

from prompts_template.prompt_engineering_refined import (
    get_completion,
    merge_two_texts_into_one,
    text_cleaner,
    question_cleaner,
    get_ocr_status,
    verbal_or_quantitive,
    check_text_completness,
    extract_incomplete_text,
    extract_question,
    structure_response,
    answer_ps_question,
    answer_ds_question,
    answer_rc_question,
    answer_cr_question,
    answer_sc_question,
)

import boto3
from botocore.exceptions import ClientError
from datetime import datetime


logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client("s3")

logger = logging.getLogger(__name__)


def setup_directories(base_dir="/tmp/"):
    folders = {
        "processed": "processed_folder",
        "full_text": "previous_full_passage",
        "missing_text": "missing_passage_folder",
    }
    paths = {k: os.path.join(base_dir, v) for k, v in folders.items()}
    for path in paths.values():
        os.makedirs(path, exist_ok=True)
    return paths


def save_text(text, file_path):
    with open(file_path, "w") as f:
        f.write(text)


def read_text(file_path):
    with open(file_path, "r") as f:
        return f.read()


def save_as_missing_text(text, path):
    clean_text = text_cleaner(text)
    save_text(clean_text, os.path.join(path, "missing_passage.txt"))
    return {
        "status": "success",
        "error_message": "No errors",
        "ocr_text": clean_text,
        "response_text": "waiting for the next image to complete the text",
        "answer_choice": "waiting for the next image to complete the text",
    }


def process_complete_text(raw_ocr_result):
    output = get_completion(raw_ocr_result)
    question_type, clean_question = create_tuple_from_string(output)

    question_handlers = {
        "critical reasoning": answer_cr_question,
        "problem solving": answer_ps_question,
        "data sufficiency": answer_ds_question,
        "sentence correction": answer_sc_question,
        "reading comprehension": answer_rc_question,
    }

    final_response = question_handlers.get(question_type, answer_rc_question)(clean_question)
    answer_choice = structure_response(final_response)

    return {
        "status": "success",
        "error_message": "No errors",
        "ocr_text": clean_question,
        "response_text": final_response,
        "answer_choice": answer_choice,
    }


def process_incomplete_text(incomplete_text, question, paths):
    if os.listdir(paths["missing_text"]):
        initial_text = read_text(os.path.join(paths["missing_text"], "missing_passage.txt"))
        if similarityscore(initial_text, incomplete_text) > 0.99:
            return complete_and_process_text(initial_text, incomplete_text, question, paths)

    if os.listdir(paths["full_text"]):
        text_full = read_text(os.path.join(paths["full_text"], "prior_full_passage.txt"))
        if similarityscore(text_full, incomplete_text) > 0.99:
            return process_with_existing_full_text(text_full, question)
        else:
            return handle_new_incomplete_text(incomplete_text, paths)

    return handle_new_incomplete_text(incomplete_text, paths)


def complete_and_process_text(initial_text, incomplete_text, question, paths):
    complete_text = f"{initial_text}+///+{incomplete_text}"
    clean_text = merge_two_texts_into_one(complete_text)
    save_text(clean_text, os.path.join(paths["full_text"], "prior_full_passage.txt"))
    empty_folder(paths["missing_text"])
    return process_with_existing_full_text(clean_text, question)


def process_with_existing_full_text(text_full, question):
    formated_question = question_cleaner(question)
    full_question = f"{text_full}\n{formated_question}"
    final_response = answer_rc_question(full_question)
    answer_choice = structure_response(final_response)
    return {
        "status": "success",
        "error_message": "No errors",
        "ocr_text": full_question,
        "response_text": final_response,
        "answer_choice": answer_choice,
    }


def handle_new_incomplete_text(incomplete_text, paths):
    empty_folder(paths["full_text"])
    return save_as_missing_text(incomplete_text, paths["missing_text"])


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

    paths = setup_directories()
    bucket_lambda = os.environ["BUCKET_LAMBDA"]
    bucket_processed_img = os.environ["BUCKET_PROCESSED_IMG"]

    results["original_image"] = f"https://{bucket_lambda}.s3.eu-north-1.amazonaws.com/{device_id}/{file_name}"
    file_path_processed = os.path.join(paths["processed"], file_name)

    try:
        processed_img = preprocessing_raw_image_double_detect(file_path, file_path_processed)
        put_image_to_s3(file_path_processed, device_id, file_name)
        results["processed_image"] = (
            f"https://{bucket_processed_img}.s3.eu-north-1.amazonaws.com/{device_id}/{file_name}"
        )
        results["status"] = "success"
        results["error_message"] = "No errors"
    except ValueError as e:
        results["status"] = "error"
        results["error_message"] = str(e)
        logger.error(str(e))
        return results

    raw_ocr_result = openai_ocr(results["processed_image"])
    if raw_ocr_result is None or get_ocr_status(raw_ocr_result) == "false":
        results["status"] = "error"
        results["error_message"] = "OCR failed or retrieved text is not related to a problem-solving question"
        logger.error("An error occurred while processing the image")
        return results

    is_text_complete = (
        "true" if verbal_or_quantitive(raw_ocr_result) != "verbal" else check_text_completness(raw_ocr_result)
    )

    if is_text_complete == "true":
        results.update(process_complete_text(raw_ocr_result))
    else:
        incomplete_text = extract_incomplete_text(raw_ocr_result)
        question = extract_question(raw_ocr_result)
        results.update(process_incomplete_text(incomplete_text, question, paths))

    return results


# Usage
file_path = "/home/aime/python-environments/exam_script_deploy/raw_images (copy)/20240112192559.jpg"
print(get_response_from_raw_image(file_path))
