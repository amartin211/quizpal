import os
import spacy
import boto3
import json
from boto3.dynamodb.conditions import Key
import re

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


def check_if_text_complete(text, min_length=1500):

    text = text.replace("###", "")
    # Clean the text
    text = re.sub(r"\s+", " ", text).strip()

    # Check text length
    if len(text) < min_length:
        return True  # Short texts are considered complete

    # Check first character capitalization
    if not text[0].isupper():
        return False  # First character should be capitalized

    # Check ending punctuation
    if not re.search(r"[.!?]$", text[-1]):
        return False  # Should end with proper punctuation

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


ocr_text = """
funding to minority businesses. At first this funding was directed toward minority entrepreneurs with very low incomes. A 1967 amendment to the Economic Opportunity Act directed the SBA to pay special attention to minority-owned businesses located in urban or rural areas characterized by high proportions of unemployed or low-income individuals. Since then, the answer given to the fundamental question of who the recipients should be—the most economically disadvantaged or those with the best prospects for business success—has changed, and the social goals of the programs have shifted, resulting in policy changes.

The first shift occurred during the early 1970’s. While the goal of assisting the economically disadvantaged entrepreneur remained, a new goal emerged: to remedy the effects of past discrimination. In fact, in 1970 the SBA explicitly stated that their main goal was to increase the number of minority-owned businesses. At the time, minorities constituted seventeen percent of the nation’s population, but only four percent of the nation’s self-employed. This ownership gap was held to be the result of past discrimination. Increasing the number of minority-owned firms was seen as a way to remedy this problem. In that context, providing funding to minority entrepreneurs in middle- and high-income brackets seemed justified.

In the late 1970’s, the goals of minority-business funding programs shifted again. At the Minority Business Development Agency, for example, the goal of increasing the numbers of minority-owned firms was supplanted by the goal of creating and assisting more minority-owned substantive firms with future growth potential. Assisting manufacturers or wholesalers became far more important than assisting small service businesses. Minority-business funding programs were now justified as instruments for economic development, particularly for creating jobs in minority communities of high unemployment.

"""

# print(check_if_text_complete(ocr_text, min_length=200))
