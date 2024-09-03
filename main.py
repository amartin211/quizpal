import os
import json
import logging
import urllib.parse

import boto3
from botocore.exceptions import ClientError

from pipeline.generate_full_response import get_response_from_raw_image
from utils import get_connection_id, send_to_websocket

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
results_table = dynamodb.Table(os.environ.get("RESULTS_TABLE", "intermediary_results"))
connections_table = dynamodb.Table(os.environ.get("CONNECTIONS_TABLE", "WebSocketConnections"))


def lambda_handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"])
    device_id = key.split("/")[0]

    tmp_file_path = os.path.join("/tmp", key)
    os.makedirs(os.path.dirname(tmp_file_path), exist_ok=True)
    s3.download_file(bucket, key, tmp_file_path)

    try:
        results = get_response_from_raw_image(tmp_file_path)
        connection_id = get_connection_id(device_id, connections_table)
        send_to_websocket(connection_id, {"message": results["answer_choice"]})
        results_table.put_item(Item=results)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        error_result = {
            "PK": "IMAGE_PROCESSING",
            "SK": key,
            "status": "error",
            "error_message": str(e),
            "device_id": device_id,
        }
        results_table.put_item(Item=error_result)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }

    logger.info(f"Processed {key} from bucket {bucket}")

    return {
        "statusCode": 200,
        "body": json.dumps(results),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }
