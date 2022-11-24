FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY dist /dist
COPY ./dev/installer.py /installer.py
RUN python installer.py /dist

#COPY ./jija_orm /jija_orm
RUN #python installer.py /jija_orm
RUN pip install jija_orm

COPY ./dev/service /app
COPY ./dev/entrypoint.sh /entrypoint.sh

WORKDIR app