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
                            If the image is blurry or the text is not clear, please output None \
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


if __name__ == "__main__":
    # Test the openai_ocr function with an S3 image
    s3_image_url = "s3://bucketforprocessedimg/00000000b5a3d56b/image_20240730_151125.jpg"
    
    # Convert S3 URL to a publicly accessible HTTP URL
    # Note: This assumes you have the necessary permissions and the bucket is configured for public access
    http_image_url = f"https://bucketforprocessedimg.s3.eu-north-1.amazonaws.com/00000000b5a3d56b/image_20240730_150806.jpg"
    
    result = openai_ocr(http_image_url)
    
    if result:
        print("OCR Result:")
        print(result)
    else:
        print("OCR failed or returned None.")
