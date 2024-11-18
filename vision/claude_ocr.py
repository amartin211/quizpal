import anthropic
import requests
from io import BytesIO
import base64


def ocr_claude(image_url):
    # Initialize the Anthropic client
    client = anthropic.Anthropic()

    # Download the image
    response = requests.get(image_url)
    image_data = BytesIO(response.content)

    # Encode the image to base64
    base64_image = base64.b64encode(image_data.getvalue()).decode("utf-8")

    # Prepare the message with the image
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_image}},
                    {
                        "type": "text",
                        "text": "Can you extract all the text in this image? \
                        Make sure to include the text on the right and left side of the image even if it is cut off. \
                        Do not include any other information, just output the entire raw text.",
                    },
                ],
            }
        ],
    )

    # Extract and return the text from Claude's response
    return message.content[0].text


# Example usage
image_url = "https://bucketlambdafunc.s3.eu-north-1.amazonaws.com/00000000261981f9/image_20241114_155930.jpg"
extracted_text = ocr_claude(image_url)
