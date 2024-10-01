FROM public.ecr.aws/lambda/python:3.10

RUN yum -y update && yum install -y mesa-libGL

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py ${LAMBDA_TASK_ROOT}
COPY utils.py ${LAMBDA_TASK_ROOT}
COPY pipeline/ ${LAMBDA_TASK_ROOT}/pipeline/
COPY vision/ ${LAMBDA_TASK_ROOT}/vision/
COPY prompts_template/ ${LAMBDA_TASK_ROOT}/prompts_template/
COPY yolov8m.pt ${LAMBDA_TASK_ROOT}
COPY yolo_screen_detector.pt ${LAMBDA_TASK_ROOT}

CMD ["main.lambda_handler"]
