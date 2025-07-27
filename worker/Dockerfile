FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ../requirements.txt .
RUN pip install -r requirements.txt

COPY worker/worker.py .
COPY shared_services ./shared_services

CMD ["python", "worker.py"]


