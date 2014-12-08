# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2014 Akretion (http://www.akretion.com).
#   @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#   @author Sébastien BEAU <sebastien.beau@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import commands
import platform
import pip
import os

from flask import render_template
from flask_cors import cross_origin
from flask.ext.babel import gettext as _

from pywebdriver import app, drivers


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
        'name': _('OS - Distribution'),
        'value': platform.linux_distribution()})
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
