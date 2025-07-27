FROM python:3.11-slim

WORKDIR /app

COPY ../requirements.txt .

RUN pip install -r requirements.txt

COPY submitter/ . 
COPY shared_services/ shared_services/

CMD ["python", "app.py"]



