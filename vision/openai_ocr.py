import logging

from openai import OpenAI

logger = logging.getLogger(__name__)
client = OpenAI()


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
                            "text": "Please do an OCR on the attached image and output the raw text extracted. "
                            "NOTE: just output the raw text extracted from the image. "
                            "If the image is blurry or the text is not clear, please output None. "
                            "Do not include any additional information.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url},
                        },
                    ],
                }
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI OCR error: {e}")
        return None
