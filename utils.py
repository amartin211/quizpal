import os
import re
import json

import spacy
import boto3
from boto3.dynamodb.conditions import Key

s3 = boto3.client("s3")
nlp = spacy.load("en_core_web_md")


def get_root_path():
    return os.path.dirname(os.path.abspath(__file__))


def check_folder_empty(folder_path):
    return not os.listdir(folder_path)


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def empty_folder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            empty_folder(file_path)


def similarityscore(text1, text2):
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    return doc1.similarity(doc2)


def check_if_text_complete(text, min_length=1500):
    text = text.replace("###", "")
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) < min_length:
        return True

    if not text[0].isupper():
        return False

    if not re.search(r"[.!?]$", text[-1]):
        return False

    return True


def create_tuple_from_string(string):
    title_end = string.find(",")
    question_type = string[1:title_end].strip()
    clean_question = string[title_end + 1 :].strip()
    return question_type, clean_question


def upload_to_s3(image, bucket_name, image_path):
    s3.upload_file(image, bucket_name, image_path)


def read_image_as_binary_file(image_path):
    with open(image_path, "rb") as image_file:
        return image_file.read()


def put_image_to_s3(image_path, device_id, filename):
    bucket_processed_img = os.environ.get("BUCKET_PROCESSED_IMG", "bucketforprocessedimg")
    processed_image_path = f"{device_id}/{filename}"
    image_data = read_image_as_binary_file(image_path)
    s3.put_object(Bucket=bucket_processed_img, Key=processed_image_path, Body=image_data)


def get_connection_id(device_id, connection_table):
    response = connection_table.query(KeyConditionExpression=Key("client_id").eq(device_id))
    items = response.get("Items", [])
    if items:
        return items[0]["connectionId"]
    raise Exception(f"No connection ID found for device_id: {device_id}")


def send_to_websocket(connection_id, data):
    endpoint_url = os.environ.get("WEBSOCKET_ENDPOINT")
    client = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint_url)
    client.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data).encode("utf-8"))
