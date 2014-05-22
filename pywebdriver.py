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
from os.path import isfile, join
from ConfigParser import ConfigParser

# Librairies Imports
from flask import (
    Flask, render_template, request, jsonify, make_response, session)
from flask.ext.babel import Babel
from flask.ext.babel import gettext as _

# Project Import
from lib.cors_decorator import crossdomain
from lib.escpos.driver import EscposDriver


# Application
app = Flask(__name__)


# ############################################################################
# HTML Pages Route Section
# ############################################################################


@app.route("/")
@app.route('/index.html', methods=['GET'])
@crossdomain(origin='*')
def index_http():
    return render_template('index.html')


@app.route('/print_status.html', methods=['GET'])
@crossdomain(origin='*')
def print_status_http():
    drivers['escpos'].push_task('printstatus')
    return render_template('print_status.html')


@app.route('/status.html', methods=['GET'])
@crossdomain(origin='*')
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
@crossdomain(origin='*')
def devices_http():
    devices = commands.getoutput("lsusb").split('\n')
    return render_template('devices.html', devices=devices)


@app.route('/system.html', methods=['GET'])
@crossdomain(origin='*')
def system_http():
    system_info = []
    system_info.append({
        'name': _('OS - System'), 'value': platform.system()})
    system_info.append({
        'name': _('OS - Release'), 'value': platform.release()})
    system_info.append({
        'name': _('OS - Version'), 'value': platform.version()})
    system_info.append({
        'name': _('OS - Machine'), 'value': platform.machine()})

    return render_template('system.html', system_info=system_info)


@app.route(
    '/static/images/<path:path>',
    methods=['POST', 'GET', 'PUT', 'OPTIONS'])
def image_html(path=None):
    return app.send_static_file(join('images/', path))


# ############################################################################
# Route Section Emulating Odoo hw_proxy behaviour
# ############################################################################


@app.route('/hw_proxy/hello', methods=['GET'])
@crossdomain(origin='*')
def hello():
    return make_response('ping')


@app.route('/hw_proxy/handshake', methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@crossdomain(origin='*', headers='accept, content-type')
def handshake():
    return jsonify(jsonrpc='2.0', result=True)


@app.route('/hw_proxy/status_json', methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@crossdomain(origin='*', headers='accept, content-type')
def status_json():
    statuses = {}
    for driver in drivers:
        statuses[driver] = drivers[driver].get_status()
    return jsonify(jsonrpc='2.0', result=statuses)


@app.route(
    '/hw_proxy/print_receipt',
    methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@crossdomain(origin='*', headers='accept, content-type')
def print_receipt():
    receipt = request.json['params']['receipt']
    drivers['escpos'].push_task('receipt', receipt)


@app.route(
    '/hw_proxy/print_xml_receipt',
    methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@crossdomain(origin='*', headers='accept, content-type')
def print_xml_receipt():
    receipt = request.json['params']['receipt']
    drivers['escpos'].push_task('xml_receipt', receipt)


# ############################################################################
# Init Section
# ############################################################################

# Config Section
LOCAL_CONFIG_PATH = 'config/config.ini'
PACKAGE_CONFIG_PATH = '/etc/pywebdriver/config.ini'

config_file = LOCAL_CONFIG_PATH
if not isfile(config_file):
    config_file = PACKAGE_CONFIG_PATH
assert isfile(config_file), (
    'Could not find config file (looking at %s and %s )' % (
        LOCAL_CONFIG_PATH, PACKAGE_CONFIG_PATH))
config = ConfigParser()
config.read(config_file)

# Localization
app.config['BABEL_DEFAULT_LOCALE'] = config.get('localization', 'locale')
babel = Babel(app)

# Drivers
drivers = {}
drivers['escpos'] = EscposDriver(
    localization=config.get('localization', 'locale'),
    port=config.get('flask', 'port'))
if config.getboolean('application', 'print_status_start'):
    drivers['escpos'].push_task('printstatus')
else:
    drivers['escpos'].push_task('status')

# Run application
if __name__ == '__main__':
    app.run(
        port=config.getint('flask', 'port'),
        debug=config.getboolean('flask', 'debug'))
