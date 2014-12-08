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

# Project Import
from libraries.escpos_driver import EscposDriver

from libraries.cups_driver import CupsDriver
from libraries.display_driver import DisplayDriver

# Application
app = Flask(__name__)


# ############################################################################
# HTML Pages Route Section
# ############################################################################
@app.route("/")
@app.route('/index.html', methods=['GET'])
@cross_origin()
def index_http():
    return render_template('index.html')


@app.route('/print_status.html', methods=['GET'])
@cross_origin()
def print_status_http():
    drivers['escpos'].push_task('printstatus')
    return render_template('print_status.html')


@app.route('/status.html', methods=['GET'])
@cross_origin()
def status_http():
    statuses = {}
    for driver in drivers:
        tmp = drivers[driver].get_vendor_product()
        if tmp:
            image = 'static/images/' + tmp + '.png'
        else:
            image = None
        statuses[driver] = {
            'state': drivers[driver].get_status(),
            'image': image,
        }
    return render_template('status.html', statuses=statuses)


@app.route('/devices.html', methods=['GET'])
@cross_origin()
def devices_http():
    devices = commands.getoutput("lsusb").split('\n')
    return render_template('devices.html', devices=devices)


@app.route('/system.html', methods=['GET'])
@cross_origin()
def system_http():
    system_info = []
    system_info.append({
        'name': _('OS - System'), 'value': platform.system()})
    system_info.append({
        'name': _('OS - Distribution'), 'value': platform.linux_distribution()})
    system_info.append({
        'name': _('OS - Release'), 'value': platform.release()})
    system_info.append({
        'name': _('OS - Version'), 'value': platform.version()})
    system_info.append({
        'name': _('Machine'), 'value': platform.machine()})
    system_info.append({
        'name': _('Python Version'), 'value': platform.python_version()})
    installed_python_packages = pip.get_installed_distributions()
    installed_python_packages = sorted(
        installed_python_packages, key=lambda package: package.key)
    return render_template(
        'system.html',
        system_info=system_info,
        installed_python_packages=installed_python_packages)


@app.route(
    '/static/images/<path:path>',
    methods=['POST', 'GET', 'PUT', 'OPTIONS'])
def image_html(path=None):
    return app.send_static_file(os.path.join('images/', path))


# ############################################################################
# [Odoo 7.0] Proxy behaviour
# ############################################################################
@app.route('/pos/print_receipt', methods=['GET'])
@cross_origin()
def print_receipt_http():
    """ For Odoo 7.0"""
    params = dict(request.args)
    receipt = simplejson.loads(params['r'][0])['params']['receipt']
    # Add required information if not provided
    if not receipt.get('precision', False):
        receipt['precision'] = {
            'price': config.getint('odoo', 'precision_price'),
            'money': config.getint('odoo', 'precision_money'),
            'quantity': config.getint('odoo', 'precision_quantity')}
    else:
        if not receipt['precision'].get('price', False):
            receipt['precision']['price'] = config.getint(
                'odoo', 'precision_price')
        if not receipt['precision'].get('money', False):
            receipt['precision']['money'] = config.getint(
                'odoo', 'precision_money')
        if not receipt['precision'].get('quantity', False):
            receipt['precision']['quantity'] = config.getint(
                'odoo', 'precision_quantity')
    drivers['escpos'].push_task('receipt', receipt)
    return make_response('')


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
# Display Route
# ############################################################################

display_driver = DisplayDriver('bixolon', app.config)

@app.route(
    '/hw_proxy/send_text_customer_display',
    methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def send_text_customer_display():
    #logger.debug('LCD: Call send_text_customer_display')
    text_to_display = request.json['params']['text_to_display']
    lines = simplejson.loads(text_to_display)
    display_driver.push_task('send_text', lines)
    return jsonify(jsonrpc='2.0', result=True)


# ############################################################################
# Init Section
# ############################################################################
# Config Section
LOCAL_CONFIG_PATH = '%s/config/config.ini' % os.path.dirname(
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
drivers = {}
drivers['escpos'] = EscposDriver(
    port=config.get('flask', 'port'))
if config.getboolean('application', 'print_status_start'):
    drivers['escpos'].push_task('printstatus')
else:
    drivers['escpos'].push_task('status')

# Connect to local cups
drivers['cups'] = CupsDriver()

def main():
    host = config.get('flask', 'host')
    port = config.getint('flask', 'port')
    debug = config.getboolean('flask', 'debug') 
    app.run(host=host, port=port, debug=debug)

# Run application
if __name__ == '__main__':
    main()
