from openai import OpenAI
import base64

# Initialize OpenAI client
client = OpenAI()


def encode_image(image_path):
    """Convert local image to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def openai_ocr(image_input):
    """
    Perform OCR on an image using OpenAI's Vision API.
    Accepts both URLs and local file paths.
    """
    try:
        # Prepare the image content based on input type
        if image_input.startswith(("http://", "https://", "s3://")):
            image_url = image_input
        else:
            # Treat as local file path
            base64_image = encode_image(image_input)
            image_url = f"data:image/jpeg;base64,{base64_image}"

        response = client.chat.completions.create(
            model="gpt-4o",
            seed=42,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Can you extract all the text in this image? Do not include any other information, just output the entire raw text.",
                        },
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            max_tokens=1000,
        )

        # Extract and return the OCR result
        if response.choices:
            return response.choices[0].message.content
        return None

    except Exception as e:
        print(f"Error performing OCR: {str(e)}")
        return None


if __name__ == "__main__":
    # Example usage with a local image
    local_image_path = "/home/aime/python-environments/exam_script_deploy/processed_image.jpg"
    result = openai_ocr(local_image_path)

    if result:
        print("OCR Result:")
        print(result)
    else:
        print("OCR failed or returned None.")
