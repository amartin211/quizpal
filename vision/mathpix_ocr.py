import os
import base64

import requests


def image_uri(filename):
    image_data = open(filename, "rb").read()
    return "data:image/jpg;base64," + base64.b64encode(image_data).decode()


def image_uri_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return "data:image/jpg;base64," + base64.b64encode(response.content).decode()


def ocr_mathpix(path_to_image):
    try:
        r = requests.post(
            "https://api.mathpix.com/v3/text",
            json={
                "src": image_uri_from_url(path_to_image),
                "math_inline_delimiters": ["$", "$"],
                "rm_spaces": True,
            },
            headers={
                "app_id": os.environ.get("APP_ID"),
                "app_key": os.environ.get("APP_KEY"),
                "Content-type": "application/json",
            },
        )
        return r.json()["text"]
    except Exception as e:
        raise ValueError("No text could be extracted from this image") from e
