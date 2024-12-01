
FROM public.ecr.aws/lambda/python:3.10

RUN yum -y update && yum install -y mesa-libGL

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . . 

# Image processing
COPY image_processing/image_preprocessing.py ${LAMBDA_TASK_ROOT}
COPY image_processing/ocr/claude_ocr_url.py ${LAMBDA_TASK_ROOT}
COPY image_processing/ocr/mathpix_ocr_url.py ${LAMBDA_TASK_ROOT}

# Text processing
COPY text_processing/check_matching_text_lambda.py ${LAMBDA_TASK_ROOT}

# Prompt template
COPY prompts_template/general_prompts.py ${LAMBDA_TASK_ROOT}

# Pipeline
COPY pipeline/all_exams_generate_full_response.py ${LAMBDA_TASK_ROOT}
COPY pipeline/long_text_processing_lambda.py ${LAMBDA_TASK_ROOT}

# Main
COPY main.py ${LAMBDA_TASK_ROOT}
COPY utils.py ${LAMBDA_TASK_ROOT}

# Models
COPY yolov8m.pt ${LAMBDA_TASK_ROOT}
COPY yolo_screen_detector.pt ${LAMBDA_TASK_ROOT}

CMD ["main.lambda_handler"]


