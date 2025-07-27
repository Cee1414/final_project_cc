FROM python:3.11-slim

WORKDIR /app

COPY ../requirements.txt .
RUN pip install -r requirements.txt

COPY init/init_dynamo.py .
COPY shared_services ./shared_services

CMD ["python", "init_dynamo.py"]


