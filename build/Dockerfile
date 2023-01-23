FROM python:3.9-slim-buster

COPY jija /build/jija
COPY setup.py /build/setup.py

WORKDIR /build
RUN python setup.py sdist

FROM python:3.9-slim-buster

COPY --from=0 /build/dist /dist
RUN pip install /dist/$(ls /dist)

COPY tests /tests
WORKDIR /tests
RUN python main.py

FROM python:3.9-slim-buster

ARG PYPI_USERNAME
ARG PYPI_PASSWORD

COPY --from=0 /build/dist /dist
RUN pip install twine

RUN twine upload /dist/* -u ${PYPI_USERNAME} -p ${PYPI_PASSWORD}
