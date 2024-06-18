import base64
from io import BytesIO

import anthropic
import requests


def ocr_claude(image_url):
    client = anthropic.Anthropic()

    response = requests.get(image_url)
    image_data = BytesIO(response.content)
    base64_image = base64.b64encode(image_data.getvalue()).decode("utf-8")

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64_image,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Extract and print the text in this image. Do not include any other text than the text in the image.",
                    },
                ],
            }
        ],
    )

    return message.content[0].text
