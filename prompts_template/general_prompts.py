from openai import OpenAI
from prompts_template.gmat_specifics.exercice_samples_prompts import cleaning_response_example

client = OpenAI()

# - get_ocr_status DONE
# - format_text_and_question_with_choices DONE
# - format_only_question (long text) DONE
# - define_question_type(verbal or quantitive) DONE
# - answer_verbal_question_with_reasoning DONE
# - answer_quant_question_with_reasoning DONE
# - structure_answer_choice DONE


def extract_text_and_question_with_choices(prompt, model="gpt-4o"):
    messages = [
        {
            "role": "system",
            "content": """
            You are an assistant specializing in text formatting. Your task is to reformat raw text output from OCR into a clean and well-structured multiple-choice question format.\
            These could include, but are not limited to, multiple answer choice question from the following exams:
                - TOEFL (Test of English as a Foreign Language)  
                - IELTS (International English Language Testing System)  
                - GRE (Graduate Record Examinations)  
                - GMAT (Graduate Management Admission Test)  
                - SAT (Scholastic Assessment Test)  
                - ACT (American College Testing)  
                - CFA (Chartered Financial Analyst)  
                - CPA (Certified Public Accountant)  
                - LSAT (Law School Admission Test)  
                - MCAT (Medical College Admission Test)  
                - USMLE (United States Medical Licensing Examination)  
                - NCLEX (National Council Licensure Examination)  
                - PMP (Project Management Professional)  
                - CISSP (Certified Information Systems Security Professional)  
                - PRAXIS (Teacher Certification Exam)  
                - CAT (Common Admission Test)  
                - JEE (Joint Entrance Examination)  
                - NEET (National Eligibility cum Entrance Test)  
                - CLAT (Common Law Admission Test)  

            The input text may include irrelevant or misplaced items caused by the OCR process. \
            Your goal is to:

            1. **Preserve the original wording** of the question, text, and answer choices without making any changes to the content, phrasing, or mathematical equations.
            2. **Remove any irrelevant items** or noise introduced by the OCR process (e.g., garbled text, extra numbers, or random symbols that do not belong to the question or answers).
            3. **Restructure the question** into a professional and readable format.

            ### Required Output Structure:

            1. **Text or Passage (if applicable):** Include any introductory context or passage if it exists, exactly as it appears in the input, but free of irrelevant items.
            2. **Question:** Write the question clearly, using the exact wording from the input.
            3. **Answer Choices:** Format the options using **letters (A, B, C, D, etc.)**, ensuring they are listed clearly and free of irrelevant noise.

            ### Rules:
            1. Do **not** change the content, phrasing, or equations of the original text.
            2. Remove any irrelevant elements caused by OCR (e.g., unrelated symbols, broken words, or misplaced fragments).
            3. Maintain the original intent and meaning of the question and answers.
            4. Ensure the output is professional, clean, and easy to read.

            Respond with the cleaned and structured question or passage as outlined above.
            """,
        },
        {"role": "user", "content": prompt.strip()},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0, seed=42)
    return response.choices[0].message.content


def extract_question_and_choices(prompt, model="gpt-4o"):
    messages = [
        {
            "role": "system",
            "content": """
            You are an assistant specializing in extracting and structuring content from OCR text. Your task is to process the raw OCR output and extract only the question and its corresponding answer choices, ignoring the text passage or other irrelevant content.

            ### Instructions:
            1. Identify and extract the **question** and the **answer choices** from the input.
            2. Format the output so it is clean and readable.
            3. Use **letters (A, B, C, D, etc.)** to label the answer choices.
            4. Ignore the introductory passage, unless part of the question.
            5. If irrelevant symbols, extra characters, or fragments caused by OCR noise are present, remove them.

            ### Required Output Structure:
            **Question:** Clearly extract the question, preserving its original wording.  
            **Answer Choices:** List the answer choices in a clean, labeled format:
            - A.
            - B.
            - C.
            - D.

            If no question or answer choices are found, return: "No question or answer choices identified."

            ### Rules:
            - Do **not** change the content or meaning of the question or answer choices.
            - Ensure that only the relevant question and choices are extracted.
            - Respond with only the formatted question and answer choices in the output.
            """,
        },
        {"role": "user", "content": prompt.strip()},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0, seed=42)
    return response.choices[0].message.content


def verbal_or_quantitive(prompt, model="gpt-4o"):
    messages = [
        {
            "role": "system",
            "content": "Given the raw result of an OCR, your task is to defined whether the extracted text is related to a \
            verbal or a quantitative multiple choice question. It is a verbal question with a lot of text you output 'verbal' \
            if it is a quantitive question you output 'quantitative', otherwise you output 'other'.",
        },
        {"role": "user", "content": prompt.strip()},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0, seed=42)
    return response.choices[0].message.content


def get_ocr_status(prompt, model="gpt-4o"):
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


def answer_verbal_question(formatted_question, model="gpt-4o"):
    messages = [
        {
            "role": "system",
            "content": """
            You are an expert assistant specializing in answering verbal multiple-choice questions. Your task is to carefully analyze the question and answer choices provided, reasoning step-by-step to determine the correct answer.

            ### Instructions:
            1. **Understand the Question:**
            - Read and comprehend the question, ensuring you grasp its key focus (e.g., main idea, tone, meaning, inference, etc.).

            2. **Try answering the question without looking at answer choices**
            - First take a step by step approach and reason through the question to see if you can find the answer without looking at the answer choices.
            
            3. **Evaluate the Answer Choices:**
            - Analyze each choice individually, ruling out incorrect options based on the reasoning process.
            - Provide a clear explanation for why each incorrect option is wrong and why the correct option is the best answer.

            4. **Reason Step-by-Step:**
            - Clearly outline your reasoning steps in your response.
            - Justify your final answer with evidence or logical inference from the question content.

            4. **Respond with the Correct Answer:**
            - Format your response to include the reasoning steps and the final answer choice in a clear format.

            ### Required Output:
            1. **Reasoning Steps:** Provide detailed reasoning explaining the process of elimination and selection of the correct choice.
            2. **Final Answer:** Clearly state the letter corresponding to the correct answer choice.

            If the question is unclear or cannot be answered, respond with: "The question cannot be answered based on the provided information."
            """,
        },
        {"role": "user", "content": formatted_question.strip()},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0, seed=42)
    return response.choices[0].message.content


def answer_quantitative_question(formatted_question, model="gpt-4o"):
    messages = [
        {
            "role": "system",
            "content": """
            You are an expert assistant specializing in answering math and quantitative multiple-choice questions. Your task is to carefully analyze the question and solve it step-by-step, explaining your reasoning clearly to determine the correct answer.

            ### Instructions:
            1. **Understand the Problem:**
            - Read the question carefully and identify the key components or equations needed to solve it.

            2. **Solve the Problem:**
            - Show all necessary calculations or logical steps to arrive at the answer.
            - Use proper mathematical reasoning and notation where applicable.

            3. **Evaluate the Answer Choices:**
            - Compare your solution to the given choices.
            - Clearly explain why the correct choice matches your solution and why the others are incorrect.

            4. **Respond with the Correct Answer:**
            - Format your response to include the reasoning steps and calculations, followed by the correct answer choice.

            If the question is unclear or missing critical information, respond with: "The question cannot be answered based on the provided information."

            ---

            ### Required Output:
            1. **Reasoning Steps:** Provide detailed calculations and explanations leading to the correct answer.
            2. **Final Answer:** Clearly state the letter corresponding to the correct answer choice.
            """,
        },
        {"role": "user", "content": formatted_question.strip()},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0, seed=42)
    return response.choices[0].message.content


def structure_response(prompt, model="gpt-4o"):

    prompt_to_add = f""" 
    - Input 5: {prompt} 
    - Output 5: """

    messages = [
        {
            "role": "system",
            "content": "Given a reasoning about a certain solution to a problem, your task is to indicate which specific letter the solution is referring to. \
            You ONLY output the letter attached to the correct answer choice, that is, A, B, C, D, E, ect... depending on the number of answer choices.",
        },
        {"role": "user", "content": cleaning_response_example + prompt_to_add},
    ]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content
