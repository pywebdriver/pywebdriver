FROM python:3.12-slim

# gcc and libcups2-dev build pycups and netifaces, git fetches the
# requirements installed from git repositories, libusb is needed at runtime by
# the escpos driver when the printer is connected by USB.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    libcups2-dev \
    libusb-1.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Default configuration, override it by mounting your own file on
# /etc/pywebdriver/config.ini
COPY config/config.ini.tmpl /etc/pywebdriver/config.ini

COPY pywebdriver ./pywebdriver

# pywebdriver takes its default locale from the environment when the
# [localization] locale option is empty, and Babel rejects the "C" locale
# of the base image. LC_ALL wins over the LC_CTYPE that Python sets itself.
ENV LC_ALL=en_US.UTF-8

EXPOSE 8069

# Set the SCRIPT_NAME environment variable (e.g. SCRIPT_NAME=/iot) to serve
# pywebdriver under a path prefix behind a reverse proxy.
CMD ["gunicorn", "--bind", "0.0.0.0:8069", "pywebdriver:app"]
