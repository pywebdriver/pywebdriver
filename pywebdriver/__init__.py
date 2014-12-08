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
import platform
import commands
import os
import gettext
import pip

from ConfigParser import ConfigParser

# Librairies Imports
import simplejson
from flask import (
    Flask, render_template, request, jsonify, make_response)
from flask.ext.babel import Babel
from flask.ext.babel import gettext as _
from flask_cors import cross_origin

# Config Section
LOCAL_CONFIG_PATH = '%s/../config/config.ini' % os.path.dirname(
    os.path.realpath(__file__))
PACKAGE_CONFIG_PATH = '/etc/pywebdriver/config.ini'

config_file = LOCAL_CONFIG_PATH
if not os.path.isfile(config_file):
    config_file = PACKAGE_CONFIG_PATH
assert os.path.isfile(config_file), (
    'Could not find config file (looking at %s and %s )' % (
        LOCAL_CONFIG_PATH, PACKAGE_CONFIG_PATH))
config = ConfigParser()
config.read(config_file)

drivers = {}

# Project Import
# Application
app = Flask(__name__)

from plugins.escpos_driver import EscposDriver

from plugins.cups_driver import CupsDriver

import views
import plugins

# ############################################################################
# [Odoo 8.0] Route Section Emulating Odoo hw_proxy behaviour
# ############################################################################
@app.route('/hw_proxy/hello', methods=['GET'])
@cross_origin()
def hello_http():
    return make_response('ping')


@app.route('/hw_proxy/handshake', methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def handshake_json():
    return jsonify(jsonrpc='2.0', result=True)


@app.route('/hw_proxy/status_json', methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def status_json():
    statuses = {}
    for driver in drivers:
        statuses[driver] = drivers[driver].get_status()
    return jsonify(jsonrpc='2.0', result=statuses)


@app.route(
    '/hw_proxy/print_xml_receipt',
    methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def print_xml_receipt_json():
    """ For Odoo 8.0+"""
    receipt = request.json['params']['receipt']
    encoding = config.get('odoo', 'force_receipt_encoding')
    if encoding != '':
        drivers['escpos'].push_task('xml_receipt', receipt.encode(encoding))
    else:
        drivers['escpos'].push_task('xml_receipt', receipt)
    return jsonify(jsonrpc='2.0', result=True)


@app.route('/hw_proxy/log', methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def log_json():
    arguments = request.json['params']['arguments']
    print (' '.join(str(v) for v in arguments))
    return jsonify(jsonrpc='2.0', result=True)


# ############################################################################
# Cups Route
# ############################################################################
@app.route('/cups/<method>', methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def cupsapi(method):
    args = []
    kwargs = {}
    if request.json:
        args = request.json.get('args', [])
        kwargs = request.json.get('kwargs', {})
    if request.args:
        kwargs = request.args.to_dict()
    result = getattr(drivers['cups'], method)(*args, **kwargs)
    return jsonify(jsonrpc='2.0', result=result)



# ############################################################################
# Init Section
# ############################################################################

# Localization
app.config['BABEL_DEFAULT_LOCALE'] = config.get('localization', 'locale')
babel = Babel(app)

path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translations')
localization = config.get('localization', 'locale')
print localization
language = gettext.translation(
    'messages',
    path,
    [localization])
language.install(unicode=True)


# Drivers
drivers['escpos'] = EscposDriver(
    port=config.get('flask', 'port'))
if config.getboolean('application', 'print_status_start'):
    drivers['escpos'].push_task('printstatus')
else:
    drivers['escpos'].push_task('status')

# Connect to local cups
drivers['cups'] = CupsDriver()
