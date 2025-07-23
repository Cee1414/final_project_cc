FROM python:3.11-slim

WORKDIR /app

COPY init_dynamo.py .

RUN pip install boto3

CMD ["python", "init_dynamo.py"]


