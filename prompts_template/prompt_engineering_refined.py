from prompts_template.exercice_samples_prompts import (
    problem_solving_examples,
    data_sufficiency_examples,
    reading_comprehension_sample,
    critical_reasoning_example,
    sentence_correction_example,
    cleaning_text_examples,
    cleaning_response_example,
    combining_text_example,
    text_completness_examples,
)
from openai import OpenAI
import re

client = OpenAI()


#############################################################################################################################################################
#############################################################################################################################################################
""" STRUCTURING EXAM QUESTION """


def get_completion(prompt, model="gpt-4"):

    prompt_to_add = f""" 
    - Example 6:
        - Input:\n\
        {prompt} \n\
        - Output: """

    messages = [
        {
            "role": "system",
            "content": "You are an expert in GMAT exam formatting. Given a piece of text, your tasks are as follows:\n\n\
            1. **Passage Formatting**:\n\
                - Detect and remove any characters at the beginning or end of the passage that are inconsistent with the content.\n\
                - Place the characters '###' at the beginning and end of the passage.\n\n\
            2. **Question Formatting**:\n\
                - If there's a question at the end of the passage enclose it with ***.\
                - If a question is followed by two statements labeled (1) and (2), include them as part of the question.\n\
                - Always present five option choices labeled A) to E). Surround each option with '@@@'.\n\n\
            3. **Sentence Correction in Verbal Section**:\n\
                - Sometimes, there may not be any question, just a passage. The first option usually refers to a passage of the text. Treat it as a standard text and format accordingly.\n\n\
            4. **Irrelevant Items**:\n\
                - Remove any instances of 'Save for Later', 'PauseExam', 'Whiteboard', 'Next', 'Help', '[.] Expand' or 'Quantitative Reasoning' as they are not relevant.\n\n\
            5. **Consistency**:\n\
                - Keep in my mind that the resuling cleaned text and question should be consistent so that the information provided in the passage is sufficient to pick one of the answer choice provided .\n\n\
                - It is imperative that you do NOT change the phrasing and wording of the passage, the question nor the answer choices.\n\n\
            5. **Expected output**:\n\
                - Output is a tuple with the first element being the type of question which could be any of the following:\n\
                    - critical reasoning\n\
                    - problem solving\n\
                    - reading comprehension\n\
                    - data sufficiency\n\
                    - sentence correction\n\
                And the second element being the clean formated GMAT question as defined in items 1 to 4\n\
           ",
        },
        {"role": "user", "content": cleaning_text_examples + prompt_to_add},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0, seed=42)
    return response.choices[0].message.content


def merge_two_texts_into_one(prompt, model="gpt-3.5-turbo"):

    prompt_to_add = f""" 
    - Input 2:\n\
        {prompt} \n\
    - Output 2: """

    messages = [
        {
            "role": "system",
            "content": "You are a world leading expert at GMAT exam.\
                Given a piece of text that contain two passages separated by /// your task is to combined the two texts by removing the duplicated texts and output a clean text surounded by ###",
        },
        {"role": "user", "content": combining_text_example + prompt_to_add},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content


def structure_response(prompt, model="gpt-3.5-turbo"):

    prompt_to_add = f""" 
    - Input 5: {prompt} 
    - Output 5: """

    messages = [
        {
            "role": "system",
            "content": "Given a reasoning about a certain solution to a problem, your task is to indicate which specific letter the solution is referring to. \
            You ONLY output the letter attached to the correct answer choice, that is, A, B, C, D or E.",
        },
        {"role": "user", "content": cleaning_response_example + prompt_to_add},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content


def text_cleaner(prompt, model="gpt-3.5-turbo"):
    messages = [
        {
            "role": "system",
            "content": "You are a renowned expert in GMAT exam formatting.\n\
            When presented with a text passage, your primary responsibility is to cleanse it.\n\
            This involves detecting and eliminating any unrelated characters or elements, especially at the beginning or end of the passage.\n\
            The output should be the purified text, free from these extraneous details. You will not change any text within the passage itself.",
        },
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content


def question_cleaner(prompt, model="gpt-3.5-turbo"):
    messages = [
        {
            "role": "system",
            "content": "You're a recognized GMAT exam expert.\n"
            "When presented with a text, your duties include:\n\n"
            "1. Text Cleansing:\n"
            "   - Eliminate any unrelated elements, particularly at the start or end of the passage.\n\n"
            "2. Question Formatting:\n"
            "   - Frame the main content as a GMAT Verbal reading comprehension question but do not alter the question by changing the wordings.\n"
            "   - The main question should be enclosed with '***'.\n"
            "   - Present the five option choices, labeled as A) to E). Each option should be wrapped with '@@@'.\n\n"
            "Example:\n\n"
            "Input:\n"
            "Flag for Review\n"
            "The passage mentions which of the following as a basic consideration in administering minority-business funding programs?\n"
            "Option 1\n"
            "Option 2\n"
            "... and so on\n\n"
            "Output:\n"
            "***The passage mentions which of the following as a basic consideration in administering minority-business funding programs?***\n"
            "A) @@@Option 1@@@\n"
            "B) @@@Option 2@@@\n"
            "... and so on",
        },
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content


def get_ocr_status(prompt, model="gpt-3.5-turbo"):
    messages = [
        {
            "role": "system",
            "content": "Given the raw result of an OCR, your task is to defined whether the extracted text is consistent with a question answering / multiple choices answers / exam question or a text passage.\
                        If this is the case you output 'true' if not 'false. You only output 'true' or 'false', nothing more.",
        },
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content


# Consider the passage complete if it forms a coherent whole with no such issues, even if short. \
def check_text_completness(prompt, model="gpt-3.5-turbo"):

    prompt_to_add = f""" 
    - Input 8:\n\
        {prompt.strip()} \n\
    - Output 8: """

    messages = [
        {
            "role": "system",
            "content": " Analyze the given passage, which is a result of an OCR process, to determine if it's complete. Follow these steps:\
            1. Identify the main body of text, ignoring any questions or answer choices that may follow.\
            2. For the main body of text, evaluate the following:\
                a) Does it start with a complete sentence?\
                b) Does it end with a complete sentence?\
                c) Are there any sentences that end abruptly or mid-thought?\
            3. Output ONLY 'false' if any of the following are true:\
                - The text ends mid-sentence\
                - The last paragraph is clearly incomplete\
                - There are obvious abrupt cuts in the content\
            4. Output 'true' ONLY if none of the conditions in step 3 are met.\
            5. Disregard any questions or answer choices that may follow the main text when making your determination.\
            Provide no explanation, just output the boolean result as a string.",
        },
        {"role": "user", "content": text_completness_examples + prompt_to_add},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0, seed=42)
    return response.choices[0].message.content


def verbal_or_quantitive(prompt, model="gpt-3.5-turbo"):
    messages = [
        {
            "role": "system",
            "content": "Given the raw result of an OCR, your task is to defined whether the extracted text is related to a \
            verbal or a quantitive question. It is a verbal question with a lot of text you output 'verbal' \
            if it is a quantitive question you output 'quantitive'.",
        },
        {"role": "user", "content": prompt.strip()},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0, seed=42)
    return response.choices[0].message.content


def extract_incomplete_text(prompt, model="gpt-3.5-turbo"):
    messages = [
        {
            "role": "system",
            "content": "Given the raw result of an OCR which contains text related to a question answering/multiple choice answers problem, \
                your task is to separate the text/passage from the question and answer choices and output this text.\
                The text passage should have a missing part and you only output this raw text/passage without the \
                related question and answer choices.",
        },
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0, seed=42)
    return response.choices[0].message.content


def extract_question(prompt, model="gpt-3.5-turbo"):
    messages = [
        {
            "role": "system",
            "content": "Given the raw result of an OCR which contains text related to a question answering/multiple choice answers problem, \
                your task is to separate the question and related answer choices from the text/passage.\
                You only output question and answer choices without the related text/passage.",
        },
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0, seed=42)
    return response.choices[0].message.content


#############################################################################################################################################################
#############################################################################################################################################################
""" ANSWERING EXAM QUESTION """


def answer_ps_question(prompt, model="gpt-4"):

    prompt_to_add = f""" 
    - Problem 10: {prompt} 
    - Explanation for Problem 10: """
    messages = [
        {
            "role": "system",
            "content": "You are a world leading expert at GMAT exam.\
            When given a problem you break it down step by step.\
            You verify that your reasonning is correct and that you have find the right answer.",
        },
        {"role": "user", "content": problem_solving_examples + prompt_to_add},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content


def answer_ds_question(prompt, model="gpt-4"):

    prompt_to_add = f""" 
    - Problem 6: {prompt} 
    - Explanation for Problem 6: """
    messages = [
        {
            "role": "system",
            "content": "You are a world leading expert at GMAT exam.\
            When given a problem you break it down step by step.\
            You verify that your reasonning is correct and that you have find the right answer.",
        },
        {"role": "user", "content": data_sufficiency_examples + prompt_to_add},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content


def answer_rc_question(prompt, model="gpt-4"):

    prompt_to_add = f""" 
    - Problem 4: {prompt} 
    - Explanation for Problem 4: """
    messages = [
        {
            "role": "system",
            "content": "You are a world leading expert at GMAT exam.\
            When given a problem you break it down step by step.\
            You verify that your reasonning is correct and that you have find the right answer.",
        },
        {"role": "user", "content": reading_comprehension_sample + prompt_to_add},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content


def answer_cr_question(prompt, model="gpt-4"):

    prompt_to_add = f""" 
    - Problem 4: {prompt} 
    - Explanation for Problem 4: """
    messages = [
        {
            "role": "system",
            "content": "You are a world leading expert at GMAT exam.\
            When given a problem you break it down step by step.\
            You verify that your reasonning is correct and that you have find the right answer.",
        },
        {"role": "user", "content": critical_reasoning_example + prompt_to_add},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content


def answer_sc_question(prompt, model="gpt-4"):

    prompt_to_add = f""" 
    - Problem 4: {prompt} 
    - Explanation for Problem 4: """
    messages = [
        {
            "role": "system",
            "content": "You are a world leading expert at GMAT exam.\
            When given a problem you break it down step by step.\
            You verify that your reasonning is correct and that you have find the right answer.",
        },
        {"role": "user", "content": sentence_correction_example + prompt_to_add},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content
