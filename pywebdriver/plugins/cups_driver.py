# -*- coding: utf-8 -*-
###############################################################################
#
#   Cups driver for pywebdriver
#   Copyright (C) 2014 Akretion (http://www.akretion.com).
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

import cups
import tempfile

from flask import request, jsonify, make_response

from pywebdriver import app, drivers
from .base_driver import AbstractDriver
import logging
_logger = logging.getLogger(__name__)


class ExtendedCups(cups.Connection):

    def printData(self, printer, data, title='Pywebdriver', options=None):
        with tempfile.NamedTemporaryFile() as f:
            f.write(data.decode('base64'))
            f.flush()
            res = self.printFile(printer, f.name, title, options)
        return res

    def printFile(self, printer, filename, title='Pywebdriver', options=None):
        if options is None:
            options = {}
        string_options = {}
        for key, value in options.items():
            string_options[str(key)] = str(value)
        return super(ExtendedCups, self).printFile(
            printer, filename, title, string_options)

    def printFiles(self, printer, filenames,
                   title='Pywebdriver', options=None):
        if options is None:
            options = {}
        string_options = {}
        for key, value in options.items():
            string_options[str(key)] = str(value)
        return super(ExtendedCups, self).printFiles(
            printer, filenames, title, string_options)


class CupsDriver(AbstractDriver):

    def getConnection(self):
        try:
            return ExtendedCups()
        except:
            return False

    def get_vendor_product(self):
        return 'cups-icon'

    def get_status(self, **params):
        messages = []
        mapstate = {
            3: 'Idle',
            4: 'Printing',
            5: 'Stopped',
            }
        conn = self.getConnection()
        if not conn:
            return {
                'status': 'disconnected',
                'messages': ['Cups Sever is not running'],
                }
        for printer, value in self.getConnection().getPrinters().items():
            messages.append(
                "%s : %s" % (printer, mapstate[value['printer-state']]))
        state = {
            'status': 'connected',
            'messages': messages,
        }
        return state

@app.route('/cups/printData', methods=['POST', 'GET', 'PUT'])
def cupsapi():
    args = []
    kwargs = {}
    if request.json:
        args = request.json.get('args', [])
        kwargs = request.json.get('kwargs', {})
    if request.args:
        kwargs = request.args.to_dict()
    conn = drivers['cups'].getConnection()
    try:
        result = conn.printData(*args, **kwargs)
    # TODO we should implement all cups error
    except cups.IPPError as e:
        err = str(e)
        return make_response(
            jsonify({
                'cups_error': 'IPPError',
                'cups_error_status': err,
                'cups_error_description': err,
                }), 400)

    return jsonify(jsonrpc='2.0', result=result)

drivers['cups'] = CupsDriver()
