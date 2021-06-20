FROM python:3.9.5-slim-buster

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY manage.py /app/
COPY project /app/project/
