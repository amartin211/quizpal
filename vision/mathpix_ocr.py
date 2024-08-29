import os
import base64
import requests
import json


os.environ["APP_ID"] = "alex_ac596d_e43aae"
os.environ["APP_KEY"] = "83c0f4255d169354ea28ba691cffda63067b8901a0f0eb6fb9c518f219491f52"


def image_uri(filename):
    image_data = open(filename, "rb").read()
    return "data:image/jpg;base64," + base64.b64encode(image_data).decode()


def ocr_mathpix(path_to_image):
    try:
        env = os.environ
        print(env.get("APP_ID"))

        r = requests.post(
            "https://api.mathpix.com/v3/text",
            json={
                "src": image_uri(path_to_image),
                "math_inline_delimiters": ["$", "$"],
                "rm_spaces": True,
            },
            headers={
                "app_id": env.get("APP_ID"),
                "app_key": env.get("APP_KEY"),
                "Content-type": "application/json",
            },
        )
        json_output = r.json()
        return json_output["text"]
    except Exception as e:
        raise ValueError("No text could have been extracted from this image") from e


print(
    ocr_mathpix("/home/aime/python-environments/exam_script_deploy/image_20240730_151353 (1).jpg")
)
