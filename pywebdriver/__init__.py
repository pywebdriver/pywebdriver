#!/usr/bin/env python
# -*- encoding: utf-8 -*-
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
    'config.ini',
    os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'config', 'config.ini'),
    '/etc/pywebdriver/config.ini',
)

for config_file in CONFIG_PATHS:
    if os.path.isfile(config_file):
        break
else:
    assert "Could not find config file (looking at %s)." % (CONFIG_PATHS,)

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
cors_origins = config.get('flask', 'cors_origins')
cors = CORS(app, resources={r"/*": {"origins": cors_origins, "headers":['Content-Type']}})

from . import views
from . import plugins

# Localization
app.config['BABEL_DEFAULT_LOCALE'] = config.get('localization', 'locale')
babel = Babel(app)

path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'translations')
localization = config.get('localization', 'locale')
language = gettext.translation(
    'messages',
    path,
    [localization])
language.install()
