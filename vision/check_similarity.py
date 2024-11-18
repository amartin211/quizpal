from difflib import SequenceMatcher
from pathlib import Path


def clean_text(text):
    """Clean text by removing extra whitespace and normalizing"""
    return " ".join(text.split()).lower()


def get_sentences(text):
    """Split text into sentences and clean them"""
    # Simple sentence splitting - you might want to use nltk for better splitting
    sentences = text.replace("!", ".").replace("?", ".").split(".")
    return [clean_text(s) for s in sentences if clean_text(s)]


def calculate_similarity(text1, text2):
    """Calculate similarity ratio between two texts"""
    return SequenceMatcher(None, text1, text2).ratio()


def find_matching_saved_text(new_text, folder_path, similarity_threshold=0.8, matching_sentences_threshold=3):
    """
    Search through saved text files to find if new_text matches based on similar sentences.
    Returns the full text if found, None otherwise.
    """
    processed_texts_dir = Path(folder_path) / "processed_texts"
    if not processed_texts_dir.exists():
        return None

    # Get sentences from new text
    new_sentences = get_sentences(new_text)

    # Search through all saved text files
    for text_file in processed_texts_dir.glob("*.txt"):
        try:
            with open(text_file, "r", encoding="utf-8") as f:
                saved_text = f.read()
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
                    print(f"Match found in file: {text_file.name}")
                    print(f"Number of matching sentences: {matching_sentences}")
                    return saved_text

        except Exception as e:
            print(f"Error reading file {text_file}: {str(e)}")
            continue

    return None


if __name__ == "__main__":
    folder_path = "/home/aime/python-environments/exam_script_deploy/grouped_images"
    new_text = open("extracted_text.txt", "r").read()
    print(find_matching_saved_text(new_text, folder_path))
