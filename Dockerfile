FROM python:3.8-slim

RUN mkdir -p /app
RUN mkdir -p /etc/pywebdriver

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libcups2-dev \
    libssl-dev \
    git \
    gunicorn \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

COPY /config/config.ini /etc/pywebdriver/config.ini

COPY pywebdriver ./pywebdriver

ENV UDEV=1

CMD SCRIPT_NAME=/iot gunicorn pywebdriver:app -b 0.0.0.0:8001
