FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/app/requirements.txt
COPY ./balancer /usr/src/app/


RUN set -eux \
    && apt update && apt-get -y upgrade \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip

RUN useradd -m -u 1000 user
USER 1000
WORKDIR /usr/src/app

CMD python server.py
