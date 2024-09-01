
FROM public.ecr.aws/lambda/python:3.10

RUN yum -y update && yum install -y mesa-libGL

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . . 
COPY vision/image_preprocessing.py ${LAMBDA_TASK_ROOT}
COPY vision/openai_OCR.py ${LAMBDA_TASK_ROOT}
COPY vision/mathpix_ocr.py ${LAMBDA_TASK_ROOT}
COPY vision/claude_ocr.py ${LAMBDA_TASK_ROOT}
COPY pipeline/refactored_generate_full_response.py ${LAMBDA_TASK_ROOT}
COPY main.py ${LAMBDA_TASK_ROOT}
COPY prompts_template/prompt_engineering_refined.py ${LAMBDA_TASK_ROOT}
COPY prompts_template/exercice_samples_prompts.py ${LAMBDA_TASK_ROOT}
COPY utils.py ${LAMBDA_TASK_ROOT}
COPY yolov8m.pt ${LAMBDA_TASK_ROOT}
COPY yolo_screen_detector.pt ${LAMBDA_TASK_ROOT}

CMD ["main.lambda_handler"]


