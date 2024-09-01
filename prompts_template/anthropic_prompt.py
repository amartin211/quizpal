api_key = "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"


from prompts_template.exercice_samples_prompts import (
    text_completness_examples,
)
import anthropic


def check_text_completness(prompt):
    prompt_to_add = f""" 
    - Input 8:\n\
        {prompt} \n\
    - Output 8: """

    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=api_key,
    )
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=100,
        system="""Analyze the given passage, which is a result of an OCR process, to determine if it's complete. Follow these steps strictly:

            1. Identify the main body of text, ignoring any questions, answer choices, or metadata that may follow or precede.

            2. For the main body of text, evaluate the following:
            a) Does it start with a complete sentence?
            b) Does it end with a complete sentence?

            3. Output ONLY 'false' (without quotes) if ANY of the following are true:
            - The text ends mid-sentence
            - The text starts mid-sentence
            - The last paragraph is clearly incomplete
            - There are obvious abrupt cuts in the content

            4. Output ONLY 'true' (without quotes) if ALL of the following conditions are met:
            - The text starts and ends with complete sentences
            - The last paragraph appears to be a complete thought
            - There are no abrupt cuts or incomplete ideas in the text

            5. Disregard any questions, answer choices, or metadata that may follow the main text when making your determination.

            6. Pay special attention to the end of the text. If it seems like there should be more content following what's given, output 'false'.

            Provide no explanation, just output the boolean result as a string ('true' or 'false').""",
        messages=[
            {"role": "user", "content": prompt_to_add},
        ],
    )

    return message.content[0].text


def extract_main_text(ocr_result):
    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Please extract only the main passage from the following OCR result. 
    Exclude any metadata, question prompts, or answer choices. 
    Return only the extracted main text, without any additional commentary or introductory phrases:

    {ocr_result}
    """

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620", max_tokens=1000, messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


prompt = """
Practice Exam 1
Verbal Reasoning
|
Whiteboard

The United States government has a long-standing policy of using federal funds to keep small business viable. The Small Business Act of 1953 authorized the Small Business Administration (SBA) to enter into contracts with government agencies having procurement powers and to arrange for fulfillment of these contracts by awarding subcontracts to small businesses. In the mid-1960's, during the war on poverty years, Congress hoped to encourage minority entrepreneurs by directing such funding to minority businesses. At first this funding was directed toward minority entrepreneurs with very low incomes. A 1967 amendment to the Economic Opportunity Act directed the SBA to pay special attention to minority-owned businesses located in urban or rural areas characterized by high proportions of unemployed or low-income individuals. Since then, the answer given to the fundamental question of who the recipients should be—the most economically disadvantaged or those with the best prospects for business success—has changed, and the social goals of the programs have shifted, resulting in policy changes.

The first shift occurred during the early 1970’s. While the goal of assisting the economically disadvantaged entrepreneurs remained, a new goal emerged: to remedy the effects of past discrimination. In fact, in 1970 the SBA explicitly stated that their main goal was to increase the number of minority-owned businesses. At the time, minorities constituted seventeen percent of the nation's population, but only four percent of the nation's self-employed. This ownership gap was held to be the result of past discrimination. Increasing the number of minority-owned firms was seen as a way to remedy this problem.  In that context, providing funding to minority entrepreneurs in middle- and high-income brackets seemed justified.

In the late 1970’s, the goals of minority-business funding programs shifted again. At the Minority Business Development Agency, for example, the goal of increasing numbers of minority-owned firms was supplanted by the goal of creating and

Time Remaining: 00:0
5 of 36
Flag for Review

The passage mentions which of the following as a basic consideration in administering minority-business funding programs?

A       Coining up with funding for the programs
B       Encouraging government agencies to assist middle- and high-income minority entrepreneurs
C       Recognizing the profit potential of small service businesses in urban communities
D       Determining who should be the recipients of the funding
E       Determining which entrepreneurs are likely to succeed
"""
# print(check_text_completness(prompt))

import re


def extract_main_passage(text):
    # Remove any leading metadata (e.g., "Practice Exam 1")
    text = re.sub(r"^.*?\n", "", text, 1)

    # Split the text into lines
    lines = text.split("\n")

    main_passage = []
    for line in lines:
        # Stop if we encounter a line that looks like the start of a question
        if re.match(r"^[0-9]+[\).]|^[A-Z][\).]", line.strip()):
            break
        # Stop if we encounter lines that look like answer choices
        if re.match(r"^[A-E](\s+|\.|\))", line.strip()):
            break
        main_passage.append(line)

    return " ".join(main_passage).strip()


def is_text_complete(text, min_length=200):
    # Clean the text
    text = re.sub(r"\s+", " ", text).strip()

    # Check text length
    if len(text) < min_length:
        return True  # Short texts are considered complete

    # Check first character capitalization
    if not text[0].isupper():
        return False  # First character should be capitalized

    # Check ending punctuation
    if not re.search(r"[.!?]$", text[-1]):
        return False  # Should end with proper punctuation

    return True


# Test function
def check_text_completeness(full_ocr_text, min_length=100):
    main_passage = extract_main_text(full_ocr_text)
    # print(main_passage)
    return is_text_complete(main_passage, min_length)


# Test cases
ocr_result1 = """Practice Exam 1
Verbal Reasoning
|
Whiteboard
The United States government has a long-standing policy of using federal funds to keep small business viable. The Small Business Act of 1953 authorized the Small Business Administration (SBA) to enter into contracts with government agencies having procurement powers and to arrange for fulfillment of these contracts by awarding subcontracts to small businesses. In the mid-1960's, during the war on poverty years, Congress hoped to encourage minority entrepreneurs by directing such funding to minority businesses. At first this funding was directed toward minority entrepreneurs with very low incomes. A 1967 amendment to the Economic Opportunity Act directed the SBA to pay special attention to minority-owned businesses located in urban or rural areas characterized by high proportions of unemployed or low-income individuals. Since then, the answer given to the fundamental question of who the recipients should be—the most economically disadvantaged or those with the best prospects for business success—has changed, and the social goals of the programs have shifted, resulting in policy changes.

The passage mentions which of the following as a basic consideration in administering minority-business funding programs?
A       Coming up with funding for the programs
B       Encouraging government agencies to assist middle- and high-income minority entrepreneurs
C       Recognizing the profit potential of small service businesses in urban communities
D       Determining who should be the recipients of the funding
E       Determining which entrepreneurs are likely to succeed"""

ocr_result2 = """Practice Exam 1
Verbal Reasoning
|
Whiteboard
The United States government has a long-standing policy of using federal funds to keep small business viable. The Small Business Act of 1953 authorized the Small Business Administration (SBA) to enter into contracts with government agencies having procurement powers and to arrange for fulfillment of these contracts by awarding subcontracts to small businesses. In the mid-1960's, during the war on poverty years, Congress hoped to encourage minority entrepreneurs by directing such funding to minority businesses. At first this funding was directed toward minority entrepreneurs with very low incomes. A 1967 amendment to the Economic Opportunity Act directed the SBA to pay special attention to minority-owned businesses located in urban or rural areas characterized by high proportions of unemployed or low-income individuals. Since then, the answer given to the fundamental question of who the recipients should be—the most economically disadvantaged or those with the best prospects for business success—has changed, and the social goals of the programs have shifted, resulting in policy changes.
The first shift occurred during the early 1970's. While the goal of assisting the economically disadvantaged entrepreneurs remained, a new goal emerged: to remedy the effects of past discrimination. In fact, in 1970 the SBA explicitly stated that their main goal was to increase the number of minority-owned businesses. At the time, minorities constituted seventeen percent of the nation's population, but only four percent of the nation's self-employed. This ownership gap was held to be the result of past discrimination. Increasing the number of minority-owned firms was seen as a way to remedy this problem.  In that context, providing funding to minority entrepreneurs in middle- and high-income brackets seemed justified.
In the late 1970's, the goals of minority-business funding programs shifted again. At the Minority Business Development Agency, for example, the goal of increasing numbers of minority-owned firms was supplanted by the goal of creating and"""

# print(check_text_completeness(ocr_result1))  # Should print True
# print(check_text_completeness(prompt))  # Should print False
