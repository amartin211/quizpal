import os
import boto3
import logging

logger = logging.getLogger(__name__)


def process_multiple_images(image_paths):
    all_extracted_text = ""

    # Iterate through all image paths
    for image_path in image_paths:
        try:
            logger.info(f"Processing {os.path.basename(image_path)}...")
            # Preprocess the image
            processed_image_path = preprocess_image(image_path)

            # Perform OCR on processed image
            extracted_text = ocr_claude(processed_image_path)

            # Append extracted text
            all_extracted_text += f"=== Text from {os.path.basename(image_path)} ===\n{extracted_text}\n\n"
        except Exception as e:
            logger.error(f"Error processing {os.path.basename(image_path)}: {str(e)}")

    # Merge the extracted texts
    single_text = merge_long_texts_into_one(all_extracted_text)

    for path in image_paths:
        os.remove(path)

    # Return the combined text
    return single_text
