import anthropic
import base64
from image_processing.image_preprocessing import preprocessing_raw_image_double_detect
from prompts_template.gmat_specifics.prompt_engineering_refined import merge_long_texts_into_one
import os
import logging
import boto3

s3 = boto3.client("s3")
logger = logging.getLogger(__name__)


def ocr_claude(image_path):
    # Initialize the Anthropic client
    client = anthropic.Anthropic()

    # Read the local image file
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Prepare the message with the image
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
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


def process_multiple_images(image_paths):
    all_extracted_text = ""
    valid_text_found = False

    # Iterate through all image paths
    for image_path in image_paths:
        try:
            logger.info(f"Processing {os.path.basename(image_path)}...")
            # Preprocess the image
            processed_image_path = preprocess_image(image_path)

            # Perform OCR on processed image
            extracted_text = ocr_claude(processed_image_path)

            if extracted_text and extracted_text.strip():
                valid_text_found = True
                # Append extracted text
                all_extracted_text += f"=== Text from {os.path.basename(image_path)} ===\n{extracted_text}\n\n"

            # Append extracted text
            # all_extracted_text += f"=== Text from {os.path.basename(image_path)} ===\n{extracted_text}\n\n"
        except Exception as e:
            logger.error(f"Error processing {os.path.basename(image_path)}: {str(e)}")

    # Merge the extracted texts
    single_text = merge_long_texts_into_one(all_extracted_text)

    for path in image_paths:
        os.remove(path)

    if not valid_text_found:
        return None

    # Return the combined text
    return single_text


def preprocess_image(image_path):
    # Create a temporary path for the processed image
    processed_image_path = image_path.replace(".jpg", "_processed.jpg")

    # Call your preprocessing function
    preprocessing_raw_image_double_detect(image_path, processed_image_path)

    return processed_image_path


def process_long_press_images(bucket, device_id, session_id):
    prefix = f"{device_id}/{session_id}/"
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

    image_keys = []
    for obj in response.get("Contents", []):
        key = obj["Key"]
        filename = key.split("/")[-1]
        if filename != "manifest.txt":
            image_keys.append(key)

    # Download all images to /tmp
    image_paths = []
    for key in image_keys:
        filename = key.split("/")[-1]
        tmp_file_path = os.path.join("/tmp", filename)
        s3.download_file(bucket, key, tmp_file_path)
        image_paths.append(tmp_file_path)

    # Process all images together
    result = process_multiple_images(image_paths)
    return result


def save_text_to_s3(text, bucket, device_id, session_id):
    # Define the S3 object key
    s3_key = f"{device_id}/{session_id}/processed_text.txt"

    try:
        # Upload the text to S3
        s3.put_object(Body=text.encode("utf-8"), Bucket=bucket, Key=s3_key, ContentType="text/plain")
        logger.info(f"Saved processed text to s3://{bucket}/{s3_key}")
    except Exception as e:
        logger.error(f"Failed to save processed text to S3: {str(e)}")


# if __name__ == "__main__":
#     bucket = "bucketlambdafunc"
#     device_id = "00000000261981f9"
#     session_id = "5dacf0c0-ed08-4c7b-afe0-a3da34e06046"
#     result = process_long_press_images(bucket, device_id, session_id)

#     print(result)
#     # save_text_to_s3(result, bucket, device_id, session_id)
