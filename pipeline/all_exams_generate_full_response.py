import os
from pathlib import Path
from datetime import datetime
import logging
import boto3
from botocore.exceptions import ClientError

from image_processing.image_preprocessing import preprocessing_raw_image_double_detect
from image_processing.ocr.claude_ocr_url import ocr_claude
from image_processing.ocr.mathpix_ocr_url import ocr_mathpix
from image_processing.ocr.openai_ocr_url import openai_ocr
from utils import put_image_to_s3


from text_processing.check_matching_text_lambda import find_matching_saved_text_s3
from prompts_template.general_prompts import (
    extract_text_and_question_with_choices,
    extract_question_and_choices,
    answer_verbal_question,
    answer_quantitative_question,
    structure_response,
    get_ocr_status_and_question_type,
)


logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client("s3")

BUCKET_LAMBDA = os.environ["BUCKET_LAMBDA"]
BUCKET_PROCESSED_IMG = os.environ["BUCKET_PROCESSED_IMG"]
BASE_DIR = "/tmp/"
PROCESSED_FOLDER = "processed_folder"


def initialize_directories():
    os.makedirs(BASE_DIR, exist_ok=True)
    path_to_processed = os.path.join(BASE_DIR, PROCESSED_FOLDER)
    os.makedirs(path_to_processed, exist_ok=True)
    return path_to_processed


def process_image(file_path):
    path_to_processed = initialize_directories()
    file_name = Path(file_path).name
    file_path_processed = os.path.join(path_to_processed, file_name)
    processed_img = preprocessing_raw_image_double_detect(file_path, file_path_processed)
    return file_path_processed


def upload_image_to_s3(file_path_processed, device_id, file_name):
    put_image_to_s3(file_path_processed, device_id, file_name)
    processed_image_url = f"https://{BUCKET_PROCESSED_IMG}.s3.eu-north-1.amazonaws.com/{device_id}/{file_name}"
    return processed_image_url


def process_complete_question(verbal_or_quant, raw_ocr_result, device_id):

    if verbal_or_quant == "verbal" or verbal_or_quant == "other":
        saved_full_passage = find_matching_saved_text_s3(
            raw_ocr_result, bucket_name="bucketlambdafunc", device_id=device_id
        )
        if saved_full_passage is not None:
            print("saved text found")
            # check similarity between raw_ocr_result and saved full passage
            question_only = extract_question_and_choices(raw_ocr_result)  # API CALL 3
            clean_question = f"{saved_full_passage}\n{question_only}"
            final_response = answer_verbal_question(clean_question)  # API CALL 4
            print("Using saved full passage")

        else:
            print("No matching text find")
            clean_question = extract_text_and_question_with_choices(raw_ocr_result)  # API CALL 3
            final_response = answer_verbal_question(clean_question)  # API CALL 4
    else:
        clean_question = extract_text_and_question_with_choices(raw_ocr_result)  # API CALL 3
        final_response = answer_quantitative_question(clean_question)  # API CALL 4

    answer_choice = structure_response(final_response)  # API CALL 5
    return clean_question, final_response, answer_choice


def get_response_from_raw_image(file_path):
    current_timestamp = datetime.utcnow().isoformat()
    s3_key = file_path.split("/tmp/")[-1]  # Remove the /tmp/ prefix
    device_id = s3_key.split("/")[0]  # Get the first part of the S3 key

    print(f"S3 key: {s3_key}")
    print(f"Device ID: {device_id}")
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

    raw_ocr_result = ocr_claude(processed_image_url)  # API CALL 1
    print(raw_ocr_result)
    if raw_ocr_result is None:
        results["status"] = "error"
        results["error_message"] = "There is an issue with the API call"
        logger.error("An error occurred with the API while processing the image")
        return results

    # ocr_status = get_ocr_status(raw_ocr_result)  # API CALL 2
    status_response = get_ocr_status_and_question_type(raw_ocr_result)  # API CALL 2

    ocr_status = status_response.ocr_status
    verbal_or_quant = status_response.verbal_or_quant

    print(status_response)
    if ocr_status == False:
        results["status"] = "error"
        results["error_message"] = (
            "Unable to retrieve texts from the image or the text is not related to a problem-solving question"
        )
        logger.error("An error occurred while processing the image")
        return results

    # verbal_or_quant = verbal_or_quantitive(raw_ocr_result)  # API CALL 3

    if verbal_or_quant == "quantitative":
        raw_ocr_result = ocr_mathpix(processed_image_url)

    try:
        ocr_text, response_text, answer_choice = process_complete_question(verbal_or_quant, raw_ocr_result, device_id)

    except Exception as e:
        results["status"] = "error"
        results["error_message"] = str(e)
        logger.error(f"Error during Claude OCR: {str(e)}")
        return results

    results["status"] = "success"
    results["error_message"] = "No errors"
    results["ocr_text"] = ocr_text
    results["response_text"] = response_text
    results["answer_choice"] = answer_choice
    return results
