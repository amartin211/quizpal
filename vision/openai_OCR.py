from openai import OpenAI
import openai
import json

client = OpenAI()
import re


# API_key = "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"


def parse_content(content):
    # Define the fields to extract and their regex patterns
    fields = {
        "text": r'"text":\s*"(.*?)"',
        "question and answer_choices": r'"question and answer_choices":\s*"(.*?)"',
        "is_text_complete": r'"is_text_complete":\s*(true|false|True|False)',
        "status": r'"status":\s*"(.*?)"',
    }

    # Initialize the result dictionary
    formatted_content = {}

    # Iterate over defined fields and apply the regex
    for key, pattern in fields.items():
        # Use re.IGNORECASE to handle case insensitivity
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            # Special handling for boolean fields
            if key == "is_text_complete":
                formatted_content[key] = match.group(1).lower() == "true"
            else:
                formatted_content[key] = match.group(1)

    return formatted_content


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


def process_ocr_content(ocr_content):
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "Format the results of OCR content into a structured dictionary. \
                    First identifies if the text is related to problem solving / question answering or multiples choices answers. \
                    If so, output 'success' as value for key 'status' and the extract the text and any detected question along with its answer choices. \
                    Your response should include the following keys and corresponding values: \
                    - 'text': The raw text extracted directly from the OCR.\
                    - 'question_and_answer_choices': Format any detected question along with its answer choices.\
                    - 'is_text_complete': Return True if the text is complete; otherwise, return False.\
                    - 'status': Output 'success' if the OCR successfully extracted text related to problem solving \
                    or question answering, such as mathematical or verbal problems. \
                    Output 'failed' if it did not.\
                Note: Do not provide answers to the questions or include any text that was not a direct result \
                of the OCR process.\
                Ensure this message includes the keyword json since we are using a json_object response format.",
            },
            {"role": "user", "content": ocr_content},
        ],
    )

    return json.loads(response.choices[0].message.content)


image_url = "https://bucketforprocessedimg.s3.eu-north-1.amazonaws.com/00000000261981f9/image_test.jpg"

image_url = "https://bucketforprocessedimg.s3.eu-north-1.amazonaws.com/00000000261981f9/image_20240217_134140.jpg"

# response = openai_ocr(image_url)
# print(response)

# formated_content = process_ocr_content(response)
# print(formated_content)
# print("text", response["text"])
# print("question and answer_choices", response["question and answer_choices"])
# print(response["is_text_complete"])
# print(response["status"])
