from openai import OpenAI

client = OpenAI()
from prompts_template.exam_instructions_template import (
    verbal_questions_direction,
    quantitative_questions_direction,
    data_sufficiency_strategy,
    output_structure,
)


def answer_question_v2(prompt, model="gpt-4"):
    messages = [
        {
            "role": "system",
            "content": f"You are a world leading expert at GMAT exam.\
                There are 2 sections in the GMAT exam, one is quantitative reasoning section and the other is the verbal reasoning section.\
                If this is a verbal question you will follow this directions: {verbal_questions_direction}.\
                If this is a quantitative question you will follow this directions: {quantitative_questions_direction}.\
                If this is a quantitative question AND a data sufficiency question you will follow this strategy to answer the question : {data_sufficiency_strategy}.\
                You will only output the letter A, B, C, D or E corresponding to the correct answer.",
        },
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=0)
    return response.choices[0].message.content


def answer_question_v3(prompt, model="gpt-4"):
    messages = [
        {
            "role": "system",
            "content": "GMAT Exam Expertise\n"
            "\n"
            "You are an expert in the GMAT exam which consists of two main sections:\n"
            "1. Quantitative Reasoning\n"
            "2. Verbal Reasoning\n"
            "\n"
            "If 'section type' is 'verbal':\n"
            "\n"
            "Verbal section has three types of questions:\n"
            "1. Reading Comprehension:\n"
            "   - Based on a passage's content.\n"
            "   - Directions: After reading, choose the best answer for each question. \n"
            "   - Indicators: Text is marked by '###', questions by '***', and options by '@@@'.\n"
            "   - Sample provided in the original prompt.\n"
            "\n"
            "2. Critical Reasoning:\n"
            "   - Select the best answer from given choices.\n"
            "   - Indicators: Text is marked by '###', questions by '***', and options by '@@@'.\n"
            "   - Sample provided in the original prompt.\n"
            "\n"
            "3. Sentence Correction:\n"
            "   - A sentence is given with a part that may need correction.\n"
            "   - Directions: Choose the best way to phrase some part of the passage. The first option provided (option A) is the same as in the text passage. You have to decide if this the correct option or not.\n"
            "   - Indicators: Sentences are marked by '***' and options by '@@@'.\n"
            "   - Sample provided in the original prompt.\n"
            "\n"
            "If 'section type' is 'quantitative':\n"
            "\n"
            "Quantitative section has two types of questions:\n"
            "1. Problem Solving:\n"
            "   - Use logic and analytical reasoning to solve.\n"
            "   - Directions: Solve and choose the best answer.\n"
            "   - Indicators: Questions are marked by '***' and options by '@@@'.\n"
            "   - Sample provided in the original prompt.\n"
            "\n"
            "2. Data Sufficiency:\n"
            "   - Analyze a problem, recognize relevant data, and determine if there's enough data to solve.\n"
            "   - Directions: A problem is given with two statements. Decide if the data in the statements is sufficient.\n"
            "   - Indicators: Questions are marked by '***' and options by '@@@'.\n"
            "   - Strategy for answering data sufficiency questions provided in the original prompt.\n"
            "   - Sample provided in the original prompt.\n"
            "\n"
            "Output Requirement:\n"
            "Only output the letter corresponding to the correct answer: A, B, C, D, or E.",
        },
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=0)
    return response.choices[0].message.content


def get_completion(prompt, model="gpt-4"):
    messages = [
        {
            "role": "system",
            "content": "You are a standardized exam expert.\
                 Given a text, your task is to detect whether some characters at the beginning or at the end of a text or option choices\
                 needs to be removed because there are inconsistent with the whole text. For the text only, once you have removed them \
                 you will put the following character: ### at the beginning and at the end of the passage.\
                 Given a question, your task is to detect whether some characters at the beginning or at the end of a question and the proposed choice answers\
                 needs to be removed because there are inconsistent with the whole questions and options choices.\
                 For questions, you put the following character: *** at the begining and at the end of the question.\
                 In some cases, for sentence correction the verbal section, there won't be any questions  but just a simple text. Usually, the first option provided will refers to a passage of the text.\
                 Sometimes questions will be presented in a form a question first and two statements labelled (1) and (2).\
                 Additionally, you will label the 5 options choices with A, B, C, D and E. Regardless of the question there will always be 5 options choices.\
                 Each option choices should be surrounded by ^^^.\
                 If you see any items such as 'Save for Later' or 'PauseExam' or 'Quantitative Reasoning' just removed these as they are irrelevant to the text \
                 nor to the questions",
        },
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=0)
    return response.choices[0].message.content


def get_structured_questions(prompt, model="gpt-4"):
    messages = [
        {
            "role": "system",
            "content": f"You are a standardized exam expert.\
                Given a series of questions and their associated option choices, your task will be to separate and restructure these questions into the appropriate format.\
                First, you will identify and indicate the question number.Then you will restructure the question in a way that is consistent with the format set forth in the following : {verbal_questions_direction}\
                Then, you will removed piece of text mentionning : 'Problem Solving Practice Questions'.\
                You will structure the output exaclty as per this exemple : {output_structure},respecting the indentation and always putting response : 'X'\
                If you see only part of option choices from a previous question you will display them as well as option choices.",
        },
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=0)
    return response.choices[0].message.content


prompt_verbal = "question type :  verbal\
***By the mid-seventeenth century, Amsterdam had built a new town hall so large that only St. Peter’s in Rome, the Escorial in Spain, \
# and the Palazza Ducale in Venice could rival it for scale or magnificence.***\
A) @@@could rival it for@@@\
B) @@@were the rivals of it in their@@@\
C) @@@were its rival as to@@@\
D) @@@could be its rivals in their@@@\
E) @@@were rivaling its@@@"


prompt_quant = "question type :  quantitative\
***The formula $F=\frac{9}{5} C+32$ gives the relationship between the temperature in degrees Fahrenheit, $F$, and the temperature given in degrees Celsius, $C$. \
If the temperature is 85 degrees Fahrenheit, what is the temperature, to the nearest degree, in degrees Celsius?***\
A) @@@$18^{\circ} \mathrm{C}$@@@\
B) @@@$23^{\circ} \mathrm{C}$@@@\
C) @@@$29^{\circ} \mathrm{C}$@@@\
D) @@@$47^{\circ} \mathrm{C}$@@@\
E) @@@$51^{\circ} \mathrm{C}$@@@"
