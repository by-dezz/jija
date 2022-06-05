FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY dist /dist
COPY integration_tests/installer.py /installer.py
RUN python installer.py /dist

COPY integration_tests/service /app
COPY integration_tests/entrypoint.sh /entrypoint.sh

WORKDIR app