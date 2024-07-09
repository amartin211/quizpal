# docker commands:
# aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 583247773415.dkr.ecr.eu-north-1.amazonaws.com
# docker build -t my-lambda-image .
# docker tag my-lambda-image:latest 583247773415.dkr.ecr.eu-north-1.amazonaws.com/myapp_image_repo:latest
# docker push 583247773415.dkr.ecr.eu-north-1.amazonaws.com/myapp_image_repo:latest

import sys
from pipeline.refactored_generate_full_response import get_response_from_raw_image
from utils import get_connection_id, send_to_websocket

import os
import urllib.parse
import boto3
import json
from botocore.exceptions import ClientError
from datetime import datetime

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


print("Loading function")
s3 = boto3.client("s3")
sns_client = boto3.client("sns")
dynamodb = boto3.resource("dynamodb")
results_table = dynamodb.Table("intermediary_results")
connectionID_table = dynamodb.Table("WebSocketConnections")

ARN_SNS = "arn:aws:sns:eu-north-1:583247773415:receive_sms_response"


def lambda_handler(event, context):

    print("sucess")
    # Get bucket and object key from the event
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"])
    # key = event["Records"][0]["s3"]["object"]["key"]

    # Extract the device ID from the object key
    # Assuming the object key format is "DEVICE_ID/unique_filename.jpg"
    device_id = key.split("/")[0]
    print("device_id : ", device_id)

    # filename = key.split("/")[-1]
    # tmp_file_path = os.path.join("/tmp", filename)

    tmp_file_path = os.path.join("/tmp", key)

    print("bucket : ", bucket)
    print("key : ", key)
    print("tmp_file_path : ", tmp_file_path)

    os.makedirs(os.path.dirname(tmp_file_path), exist_ok=True)

    s3.download_file(bucket, key, tmp_file_path)

    try:
        results = get_response_from_raw_image(tmp_file_path)
        # sns_client.publish(TopicArn=ARN_SNS, Message=str(results['answer_choice']))
        connection_id = get_connection_id(device_id, connectionID_table)
        response_data = {"message": results["answer_choice"]}  # Replace with actual data
        send_to_websocket(connection_id, response_data)

        # Store results in DynamoDB

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
