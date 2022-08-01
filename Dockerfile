# syntax=docker/dockerfile:1

FROM python:3.10.5-slim-buster

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip3 install --timeout=60 -r requirements.txt

COPY . .


RUN mkdir /app/data


ENTRYPOINT [ "python3", "bot.py"]
