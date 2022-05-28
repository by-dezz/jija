FROM python:3.8-slim-buster

COPY dist /dist
COPY integration_tests/installer.py /installer.py
RUN python installer.py /dist

COPY integration_tests/service /app
COPY integration_tests/entrypoint.sh /entrypoint.sh

WORKDIR app