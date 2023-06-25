FROM public.ecr.aws/lambda/python:3.10
RUN yum update -y
RUN yum install -y git
RUN yum install -y zip
ADD secrets.txt .
RUN cat secrets.txt > .env
RUN git clone https://github.com/liufran1/RestaurantReviewSummaries.git
RUN mkdir python

RUN mv RestaurantReviewSummaries/lambda_function.py .

COPY lambda_function.py ${LAMBDA_TASK_ROOT}
CMD ["lambda_function.lambda_handler"]

