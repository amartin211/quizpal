import boto3
from difflib import SequenceMatcher
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_text(text):
    """Clean text by removing extra whitespace and normalizing."""
    return " ".join(text.split()).lower()


def get_sentences(text):
    """Split text into sentences and clean them."""
    sentences = text.replace("!", ".").replace("?", ".").split(".")
    return [clean_text(s) for s in sentences if clean_text(s)]


def calculate_similarity(text1, text2):
    """Calculate similarity ratio between two texts."""
    return SequenceMatcher(None, text1, text2).ratio()


def find_matching_saved_text_s3(new_text, bucket_name, similarity_threshold=0.8, matching_sentences_threshold=3):
    """
    Search through saved text files in S3 to find if new_text matches based on similar sentences.
    Returns the full text if found, None otherwise.
    """
    s3_client = boto3.client("s3")

    # List all objects in the bucket that match the pattern for processed texts
    paginator = s3_client.get_paginator("list_objects_v2")
    # Adjust the prefix if necessary; here we assume all processed texts are under the root
    page_iterator = paginator.paginate(Bucket=bucket_name)

    # Get sentences from the new text
    new_sentences = get_sentences(new_text)

    for page in page_iterator:
        if "Contents" in page:
            for obj in page["Contents"]:
                key = obj["Key"]
                if key.endswith("processed_text.txt"):
                    try:
                        logger.info(f"Processing {key}...")
                        # Get the object content
                        response = s3_client.get_object(Bucket=bucket_name, Key=key)
                        saved_text = response["Body"].read().decode("utf-8")
                        saved_sentences = get_sentences(saved_text)

                        # Count matching sentences
                        matching_sentences = 0
                        for new_sent in new_sentences:
                            for saved_sent in saved_sentences:
                                similarity = calculate_similarity(new_sent, saved_sent)
                                if similarity > similarity_threshold:
                                    matching_sentences += 1
                                    break  # Move to next new sentence once a match is found

                        # If enough sentences match, consider it the same text
                        if matching_sentences >= matching_sentences_threshold:
                            logger.info(f"Match found in file: {key}")
                            logger.info(f"Number of matching sentences: {matching_sentences}")
                            return saved_text

                    except Exception as e:
                        logger.error(f"Error processing {key}: {str(e)}")
                        continue

    return None
