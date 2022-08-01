# syntax=docker/dockerfile:1

FROM python:3.10.5-slim-buster

WORKDIR /app


RUN mkdir data

VOLUME /app/data

COPY requirements.txt requirements.txt
RUN pip3 install --timeout=60 -r requirements.txt

COPY . .


ENTRYPOINT [ "python3", "bot.py"]
