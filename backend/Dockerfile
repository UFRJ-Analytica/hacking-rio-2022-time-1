FROM python:3.9.9-slim-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .