import numpy as np
import os
from pathlib import Path
import time

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
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client("s3")


def get_response_from_raw_image(file_path):

    current_timestamp = datetime.utcnow().isoformat()
    device_id = file_path.split("/")[-2]
    print(device_id)
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

    bucket_lambda = os.environ["BUCKET_LAMBDA"]
    bucket_processed_img = os.environ["BUCKET_PROCESSED_IMG"]

    ## GENERATE URL
    original_image_url = f"https://{bucket_lambda}.s3.eu-north-1.amazonaws.com/{device_id}/{file_name}"
    results["original_image"] = original_image_url

    base_dir = "/tmp/"  # Change this to the desired persistent directory path
    os.makedirs(base_dir, exist_ok=True)

    processed_folder = "processed_folder"
    full_text_folder = "previous_full_passage"
    missing_text_folder = "missing_passage_folder"

    path_to_processed = os.path.join(base_dir, processed_folder)
    path_to_previous_text = os.path.join(base_dir, full_text_folder)
    path_to_missing_text = os.path.join(base_dir, missing_text_folder)

    os.makedirs(path_to_processed, exist_ok=True)
    os.makedirs(path_to_previous_text, exist_ok=True)
    os.makedirs(path_to_missing_text, exist_ok=True)

    file_path_processed = os.path.join(path_to_processed, file_name)

    try:
        processed_img = preprocessing_raw_image_double_detect(file_path, file_path_processed)

        ## SAVE TO S3 AND GENERATE URL
        put_image_to_s3(file_path_processed, device_id, file_name)
        # time.sleep(2)
        processed_image_url = f"https://{bucket_processed_img}.s3.eu-north-1.amazonaws.com/{device_id}/{file_name}"

        results["status"] = "success"
        results["error_message"] = "No errors"
        results["processed_image"] = processed_image_url

    except ValueError as e:
        results["status"] = "error"
        results["error_message"] = str(e)
        logger.error(str(e))
        return results

    raw_ocr_result = openai_ocr(processed_image_url)  # API CALL 1
    print(raw_ocr_result)

    if raw_ocr_result is None:
        results["status"] = "error"
        results["error_message"] = "There is an issue with the API call"
        logger.error("An error occured with the API while processing the image")
        return results

    ocr_statut = get_ocr_status(raw_ocr_result)  # API CALL 2

    if ocr_statut == "false":
        results["status"] = "error"
        results["error_message"] = (
            "We were not able to retrieve texts from the image or the text extracted \
                was not related to a problem solving question"
        )
        logger.error("An error occured while processing the image")
        return results

    verbal_or_quant = verbal_or_quantitive(raw_ocr_result)  # API CALL 3

    if verbal_or_quant == "verbal":
        is_text_complete = check_text_completness(raw_ocr_result)  # API CALL 4
        print(is_text_complete)
    else:
        is_text_complete = "true"

    if is_text_complete == "true":
        print("TEXT IS COMPLETE")

        output = get_completion(raw_ocr_result)  # API CALL 5
        print(output)
        question_type, clean_question = create_tuple_from_string(output)

        # API CALL 6
        if question_type == "critical reasoning":
            final_response = answer_cr_question(clean_question)
        elif question_type == "problem solving":
            final_response = answer_ps_question(clean_question)
        elif question_type == "data sufficiency":
            final_response = answer_ds_question(clean_question)
        elif question_type == "sentence correction":
            final_response = answer_sc_question(clean_question)
        elif question_type == "reading comprehension":
            final_response = answer_rc_question(clean_question)

        # API CALL 7
        answer_choice = structure_response(final_response)

        results["status"] = "success"
        results["error_message"] = "No errors"
        results["ocr_text"] = clean_question
        results["response_text"] = final_response
        results["answer_choice"] = answer_choice

        return results

    else:
        # TEXT IS NOT COMPLETE
        incomplete_text = extract_incomplete_text(raw_ocr_result)  # API CALL 4
        question = extract_question(raw_ocr_result)  # API CALL 5

        # CHECK IF A MISSING TEXT HAS ALREADY BEEN RETRIEVED
        if os.listdir(path_to_missing_text):
            initial_text = open(f"{path_to_missing_text}/missing_passage.txt", "r").read()
            score = similarityscore(initial_text, incomplete_text)
            print(score)

            if score > 0.99:

                print("a missing text already exist, we'll complete this text and save it")
                complete_text = f"{initial_text}+///+{incomplete_text}"
                clean_text = merge_two_texts_into_one(complete_text)  # API CALL 6

                with open(f"{path_to_previous_text}/prior_full_passage.txt", "w") as f:
                    f.write(clean_text)

                # EMPTY THE MISSING TEXT FOLDER SINCE WE HAVE THE COMPLETE TEXT SAVED IN path_to_previous_text
                empty_folder(path_to_missing_text)

                formated_question = question_cleaner(question)  # API CALL 7
                full_question = f"{clean_text}\n{formated_question}"

                print(full_question)
                final_response = answer_rc_question(full_question)  # API CALL 8
                answer_choice = structure_response(final_response)  # API CALL 9

                results["status"] = "success"
                results["error_message"] = "No errors"
                results["ocr_text"] = full_question
                results["response_text"] = final_response
                results["answer_choice"] = answer_choice
                return results

        # CHECK IF A FULL TEXT HAS ALREADY BEEN RETRIEVED
        if os.listdir(path_to_previous_text):
            text_full = open(f"{path_to_previous_text}/prior_full_passage.txt", "r").read()
            score = similarityscore(text_full, incomplete_text)
            print(score)

            if score > 0.99:
                print("a full text already exist, we'll use this text")
                # TEXT ALREADY COMPLETE : WE CAN GENERATE THE ANSWER
                formated_question = question_cleaner(question)  # API CALL 6
                full_question = f"{text_full}\n{formated_question}"

                print(full_question)
                final_response = answer_rc_question(full_question)  # API CALL 7
                answer_choice = structure_response(final_response)  # API CALL 8

                results["status"] = "success"
                results["error_message"] = "No errors"
                results["ocr_text"] = full_question
                results["response_text"] = final_response
                results["answer_choice"] = answer_choice

                print(final_response)
                return results

            else:
                # THE PARTIAL TEXT PROVIDED IS NOT RELATED TO THE LAST PRIOR FULL TEXT (MEANING IT IS A NEW TEXT)
                print("some text are missing, we are saving this part")
                clean_text = text_cleaner(incomplete_text)  # API CALL 6
                with open(os.path.join(path_to_missing_text, "missing_passage.txt"), "w") as f:
                    f.write(clean_text)

                empty_folder(path_to_previous_text)  # EMPTY THE FULL TEXT FOLDER
                response = "waiting for the next image to complete the text"

                results["status"] = "success"
                results["error_message"] = "No errors"
                results["ocr_text"] = clean_text
                results["response_text"] = response
                results["answer_choice"] = response
                return results

        else:
            # THE TEXT IS NEW, THERE IS NOT PARTIAL TEXT NOR EXISTING FULL TEXT
            print("some text are missing, we are saving this part")
            clean_text = text_cleaner(incomplete_text)  # API CALL 6
            with open(os.path.join(path_to_missing_text, "missing_passage.txt"), "w") as f:
                f.write(clean_text)
            response = "waiting for the next image to complete the text"

            results["status"] = "success"
            results["error_message"] = "No errors"
            results["ocr_text"] = clean_text
            results["response_text"] = response
            results["answer_choice"] = response
            return results


file_path = "/home/aime/python-environments/exam_script_deploy/raw_images (copy)/20240112192559.jpg"
print(get_response_from_raw_image(file_path))
