FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY dist /dist
COPY ./dev/installer.py /installer.py
RUN python installer.py /dist

COPY ./dev/service /app
COPY ./dev/entrypoint.sh /entrypoint.sh

WORKDIR app