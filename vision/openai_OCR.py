from openai import OpenAI

client = OpenAI()


# API_key = "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"


def openai_ocr(image_url):

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            seed=42,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please do an OCR on the attached image and \
                            output the raw text extracted. NOTE: just output the raw text extracted from the image. \
                            Do not include any additional information.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                    ],
                }
            ],
            max_tokens=500,
        )

        content = response.choices[0].message.content.strip()  # Get the message object
        return content

    except client.error.InvalidRequestError as e:
        if e.code == "invalid_image":
            print(f"Error: Invalid image provided. Details: {e}")
            return None
        else:
            print(f"Invalid request error: {e}")
            return None
    except client.error.OpenAIError as e:
        print(f"An error occurred: {e}")
        return None
