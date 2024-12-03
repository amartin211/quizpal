# docker commands:
# aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 583247773415.dkr.ecr.eu-north-1.amazonaws.com
# docker build -t general_question .
# docker tag general_question:latest 583247773415.dkr.ecr.eu-north-1.amazonaws.com/general_question:latest
# docker push 583247773415.dkr.ecr.eu-north-1.amazonaws.com/general_question:latest

from pipeline.all_exams_generate_full_response import get_response_from_raw_image
from pipeline.long_text_processing_lambda import process_multiple_images
from utils import get_connection_id, send_to_websocket

import os
import urllib.parse
import boto3
import json

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


print("Loading function")
s3 = boto3.client("s3")
sns_client = boto3.client("sns")
dynamodb = boto3.resource("dynamodb")
results_table = dynamodb.Table("intermediary_results")
connectionID_table = dynamodb.Table("WebSocketConnections")
secrets_manager = boto3.client("secretsmanager")

ARN_SNS = "arn:aws:sns:eu-north-1:583247773415:receive_sms_response"


def get_client_id_from_device(device_id, connection_table):
    """Get client ID associated with device ID from DynamoDB"""
    try:
        response = connection_table.get_item(Key={"device_id": device_id})
        return response["Item"]["client_id"]
    except Exception as e:
        logging.error(f"Error getting client ID: {str(e)}")
        raise


def get_openai_secret(client_id):
    """Get OpenAI credentials from Secrets Manager"""
    secret_name = f"openai_credentials_user_{client_id}"
    try:
        response = secrets_manager.get_secret_value(SecretId=secret_name)
        secrets = json.loads(response["SecretString"])
        return secrets["openai_api_key"]
    except Exception as e:
        logging.error(f"Error getting OpenAI secret: {str(e)}")
        raise


def save_text_to_s3(text, bucket, device_id, session_id):
    # Define the S3 object key
    s3_key = f"{device_id}/{session_id}/processed_text.txt"

    try:
        # Upload the text to S3
        s3.put_object(Body=text.encode("utf-8"), Bucket=bucket, Key=s3_key, ContentType="text/plain")
        logger.info(f"Saved processed text to s3://{bucket}/{s3_key}")
    except Exception as e:
        logger.error(f"Failed to save processed text to S3: {str(e)}")


def process_long_press_images(bucket, device_id, session_id):
    prefix = f"{device_id}/{session_id}/"
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

    image_keys = []
    for obj in response.get("Contents", []):
        key = obj["Key"]
        filename = key.split("/")[-1]
        if filename != "manifest.json":
            image_keys.append(key)

    # Download all images to /tmp
    image_paths = []
    for key in image_keys:
        filename = key.split("/")[-1]
        tmp_file_path = os.path.join("/tmp", filename)
        s3.download_file(bucket, key, tmp_file_path)
        image_paths.append(tmp_file_path)

    # Process all images together
    result = process_multiple_images(image_paths)
    return result


def is_long_press_session(bucket, device_id, session_id):
    """Check if this session has multiple images (indicating long press)"""
    prefix = f"{device_id}/{session_id}/"
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    if not response.get("Contents"):
        return False

    # Count the number of image files in the session
    image_count = sum(1 for obj in response["Contents"] if obj["Key"].endswith(".jpg"))

    # Return True if there are multiple images
    return image_count > 1


def lambda_handler(event, context):

    print("sucess")
    # Get bucket and object key from the event
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"])
    # key = event["Records"][0]["s3"]["object"]["key"]

    # Extract the device ID from the object key
    # Assuming the object key format is "DEVICE_ID/unique_filename.jpg"
    parts = key.split("/")
    device_id = parts[0]

    # Handle both short press (device_id/image.jpg) and long press (device_id/session_id/image.jpg) cases
    if len(parts) == 2:  # Short press: device_id/image.jpg
        session_id = None
        filename = parts[1]
        logging.info(f"Short press detected - Device ID: {device_id}, Filename: {filename}")
    else:  # Long press: device_id/session_id/image.jpg
        session_id = parts[1]
        filename = parts[2]
        logging.info(f"Long press detected - Device ID: {device_id}, Session ID: {session_id}, Filename: {filename}")

    # print("bucket : ", bucket)
    # print("key : ", key)
    # print("tmp_file_path : ", tmp_file_path)

    try:
        if session_id and is_long_press_session(bucket, device_id, session_id):
            if filename == "manifest.json":  # Only process when manifest arrives
                result = process_long_press_images(bucket, device_id, session_id)
                response_message = "X" if result is not None else "None"

                if result is not None:
                    save_text_to_s3(result, bucket, device_id, session_id)

                connection_id = get_connection_id(device_id, connectionID_table)
                response_data = {"message": response_message}
                send_to_websocket(connection_id, response_data)
                results = {"status": "success", "mode": "long_press", "result": result}
            else:
                # Skip processing individual images in long press mode
                logger.info(f"Skipping individual image processing in long press session: {filename}")
                return {"statusCode": 200, "body": json.dumps({"status": "skipped", "mode": "long_press_image"})}
        else:
            # For short press, process the single image
            tmp_file_path = os.path.join("/tmp", key)
            os.makedirs(os.path.dirname(tmp_file_path), exist_ok=True)
            s3.download_file(bucket, key, tmp_file_path)
            results = get_response_from_raw_image(tmp_file_path)
            connection_id = get_connection_id(device_id, connectionID_table)
            response_data = {"message": results["answer_choice"]}  # Replace with actual data
            send_to_websocket(connection_id, response_data)
            results_table.put_item(Item=results)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        # Save the error status and message to DynamoDB:
        results_table.put_item(Item=results)

    print(f"New file {key} has been uploaded to bucket {bucket}.")

    return {
        "statusCode": 200,
        "body": json.dumps(results),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # This is required for CORS if you're calling API from a different domain
        },
    }
