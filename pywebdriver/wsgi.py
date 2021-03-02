#!/usr/bin/env python

from pywebdriver import config as conf

# gunicorn configuration
for option, value in conf.items("gunicorn"):
    vars()[option] = value
