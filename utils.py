import os
import spacy
import boto3
import json
from boto3.dynamodb.conditions import Key

s3 = boto3.client("s3")


def get_root_path():
    """Gets the root path of the current working directory."""
    return os.path.dirname(os.path.abspath(__file__))


def check_folder_empty(folder_path):
    files = os.listdir(folder_path)
    return not files


def create_folder(folder_name):
    """Creates an empty folder."""
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def empty_folder(folder_path):
    """Emptys a folder."""
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            empty_folder(file_path)


nlp = spacy.load("en_core_web_md")


def similarityscore(text1, text2):
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    similarity = doc1.similarity(doc2)
    return similarity


def is_text_missing(text):
    if text[-1] == ".":
        return False
    else:
        return True


def create_tuple_from_string(string):
    title_end = string.find(",")
    question_type = string[1:title_end].strip()
    clean_question = string[title_end + 1 :].strip()
    return question_type, clean_question


def upload_to_s3(image, BUCKET_NAME, image_path):
    s3.upload_file(image, BUCKET_NAME, image_path)


def read_image_as_binary_file(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    return image_data


def put_image_to_s3(image_path, device_id, filename):
    bucket_processed_img = "bucketforprocessedimg"
    processed_image_path = f"{device_id}/{filename}"
    image_data = read_image_as_binary_file(image_path)
    s3.put_object(Bucket=bucket_processed_img, Key=processed_image_path, Body=image_data)


def get_connection_id(device_id, connectionID_table):
    # Use query to find the item with the matching device_id
    response = connectionID_table.query(KeyConditionExpression=Key("client_id").eq(device_id))
    items = response.get("Items", [])

    if items:
        # Assuming each device_id maps to a unique connection_id
        return items[0]["connectionId"]
    else:
        raise Exception("No connection ID found in DynamoDB for device_id: {}".format(device_id))


def send_to_websocket(connection_id, data):
    endpoint_url = "https://ypvy1ycxbh.execute-api.eu-north-1.amazonaws.com/production/"
    client = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint_url)

    client.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data).encode("utf-8"))
