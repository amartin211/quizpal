import anthropic
import requests
from io import BytesIO
import base64
from pathlib import Path
from image_preprocessing import preprocessing_raw_image_double_detect
from prompts_template.prompt_engineering_refined import merge_long_texts_into_one
from vision.claude_ocr import ocr_claude


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


def process_folder(folder_path, output_file):
    # Create Path object for better path handling
    folder = Path(folder_path)

    # Create a temporary directory for processed images
    temp_dir = Path(folder_path) / "temp_processed"
    temp_dir.mkdir(exist_ok=True)

    # Supported image extensions
    image_extensions = (".jpg", ".jpeg", ".png")

    all_extracted_text = ""

    # Iterate through all files in the folder
    for image_file in folder.iterdir():
        if image_file.suffix.lower() in image_extensions:
            try:
                print(f"Processing {image_file.name}...")
                # Preprocess the image
                processed_image_path = temp_dir / f"processed_{image_file.name}"
                preprocessing_raw_image_double_detect(str(image_file), str(processed_image_path))

                # Perform OCR on processed image
                extracted_text = ocr_claude(str(processed_image_path))

                # Write the extracted text with a separator
                all_extracted_text += f"=== Text from {image_file.name} ===\n{extracted_text}\n\n"
            except Exception as e:
                print(f"Error processing {image_file.name}: {str(e)}")

    # shutil.rmtree(temp_dir)
    single_text = merge_long_texts_into_one(all_extracted_text)
    saved_path = save_processed_text(single_text, folder_path)
    print(f"Processed text saved to: {saved_path}")
    return single_text


def save_processed_text(text, folder_path, filename="processed_text.txt"):
    # Create output directory if it doesn't exist
    output_dir = Path(folder_path) / "processed_texts"
    output_dir.mkdir(exist_ok=True)

    # Save the text file
    output_path = output_dir / filename
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    return output_path


# Update the example usage section
if __name__ == "__main__":
    folder_path = "/home/aime/python-environments/exam_script_deploy/grouped_images"
    output_file = "extracted_text.txt"
    single_text = process_folder(folder_path, output_file)
    print(single_text)

    # text_content = open("extracted_text.txt", "r").read()
    # single_text = merge_long_texts_into_one(text_content)
    # print(single_text)


# Example usage
# image_path = "/home/aime/python-environments/exam_script_deploy/processed_image.jpg"
# extracted_text = ocr_claude(image_path)
# print(extracted_text)

# Example usage
# if __name__ == "__main__":
#     folder_path = "/home/aime/python-environments/exam_script_deploy/grouped_images "
#     output_file = "extracted_text.txt"
#     process_folder(folder_path, output_file)
