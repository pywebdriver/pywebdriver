#!/usr/bin/env python
##############################################################################
#
#    PyWebDriver Software
#    Copyright (C) 2014-TODAY Akretion <http://www.akretion.com>.
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


# Core Imports
import gettext
import logging.config
import os

from configparser import ConfigParser

# Librairies Imports
from flask import Flask
from flask_babel import Babel
from flask_cors import CORS

# Config Section
CONFIG_PATHS = (
    "config.ini",
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "config", "config.ini"
    ),
    "/etc/pywebdriver/config.ini",
)

for config_file in CONFIG_PATHS:
    if os.path.isfile(config_file):
        break
else:
    assert "Could not find config file (looking at {}).".format(CONFIG_PATHS)

config = ConfigParser()
config.read(config_file)

if (
    config.has_section("loggers")
    and config.has_section("handlers")
    and config.has_section("formatters")
):
    logging.config.fileConfig(config)

drivers = {}

# Project Import
# Application
app = Flask(__name__)
cors_origins = config.get("flask", "cors_origins")
cors = CORS(
    app, resources={r"/*": {"origins": cors_origins, "headers": ["Content-Type"]}}
)

from . import views  # noqa: E402
from . import plugins  # noqa: E402

# Localization
app.config["BABEL_DEFAULT_LOCALE"] = config.get("localization", "locale")
babel = Babel(app)

path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "translations")
localization = config.get("localization", "locale")
language = gettext.translation("messages", path, [localization])
language.install()

# To run with flask
if config.getboolean("application", "print_status_start"):
    if "escpos" in drivers:
        drivers["escpos"].push_task("printstatus")
flask_args = dict(
    host=config.get("flask", "host", fallback="0.0.0.0"),
    port=config.getint("flask", "port", fallback=3000),
    debug=config.getboolean("flask", "debug", fallback=False),
    use_reloader=config.getboolean("flask", "use_reloader", fallback=False),
    processes=0,
    threaded=True,
)
if config.has_option("flask", "sslcert"):
    sslcert = config.get("flask", "sslcert")
    if sslcert:
        import sys

        if not config.has_option("flask", "sslkey"):
            print("If you want SSL, you must also provide the sslkey")
            sys.exit(-1)
        sslkey = config.get("flask", "sslkey")
        if not os.path.exists(sslcert):
            print("SSL cert not found at", sslcert)
            sys.exit(-1)
        if not os.path.exists(sslkey):
            print("SSL key not found at", sslkey)
            sys.exit(-1)
        flask_args["ssl_context"] = (sslcert, sslkey)
