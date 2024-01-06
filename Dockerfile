
FROM public.ecr.aws/lambda/python:3.10

RUN yum -y update && yum install -y mesa-libGL

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . . 
COPY generate_full_response_webapp.py ${LAMBDA_TASK_ROOT}
COPY main.py ${LAMBDA_TASK_ROOT}
COPY mathpix.py ${LAMBDA_TASK_ROOT}
COPY prompt_engineering_refined.py ${LAMBDA_TASK_ROOT}
COPY exam_instructions_template.py ${LAMBDA_TASK_ROOT}
COPY utils.py ${LAMBDA_TASK_ROOT}
COPY yolov8m.pt ${LAMBDA_TASK_ROOT}

CMD ["main.lambda_handler"]




#FROM public.ecr.aws/lambda/python:3.10
#
#RUN yum -y update && yum install -y mesa-libGL
#
## Install dependencies
#COPY requirements.txt .
#RUN pip install -r requirements.txt
#
## Copy the rest of the code
#COPY . . 
#COPY generate_response.py ${LAMBDA_TASK_ROOT}
#COPY main.py ${LAMBDA_TASK_ROOT}
#COPY mathpix.py ${LAMBDA_TASK_ROOT}
#COPY prompt_engineering_refined.py ${LAMBDA_TASK_ROOT}
#COPY exam_instructions_template.py ${LAMBDA_TASK_ROOT}
#COPY utils.py ${LAMBDA_TASK_ROOT}
#
#CMD ["main.lambda_handler"]

