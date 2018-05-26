# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2015 Akretion (http://www.akretion.com).
#   @author Sylvain Calador <sylvain.calador@akretion.com>
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

import logging
import os
import sys

import serial
from flask import request, make_response, jsonify
import simplejson as json

from pywebdriver import app, config, drivers


def serial_options(options):

    values = {}
    values['port'] = options.get('port',
        config.get('serial_driver', 'port') or '/dev/ttyS0'
    )

    values['baudrate'] = options.get('baudrate',
        config.getint('serial_driver', 'baudrate')
    )
    values['bytesize'] = options.get('bytesize',
        config.getint('serial_driver', 'bytesize')
    )
    values['parity'] = options.get('parity',
        config.get('serial_driver', 'parity')
    )
    values['stopbits'] = options.get('stopbits',
        config.getint('serial_driver', 'stopbits')
    )
    values['rtscts'] = options.get('rtscts',
        config.getboolean('serial_driver', 'rtscts')
    )
    values['xonxoff'] = options.get('xonxoff',
        config.getboolean('serial_driver', 'xonxoff')
    )
    values['timeout'] = options.get('timeout',
        config.getint('serial_driver', 'timeout')
    )
    values['eol_cr'] = options.get('eol_cr',
        config.getboolean('serial_driver', 'eol_cr')
    )
    values['eol_lf'] = options.get('eol_lf',
        config.getboolean('serial_driver', 'eol_lf')
    )
    data = options.get('data','')

    if values['eol_cr']:
        data += serial.CR
    if values['eol_lf']:
        data += serial.LF

    return values, data


def serial_open(options):

    port = options['port']
    if sys.platform.startswith('linux') or \
        sys.platform.startswith('cygwin') or \
        sys.platform.startswith('darwin'):
            if not port.startswith('/dev/tty'):
                raise serial.SerialException('%s: invalid serial port' % port)

    app.logger.debug('serial: open %r', options)
    return serial.Serial(
        port=options['port'],
        baudrate=options['baudrate'],
        bytesize=options['bytesize'],
        parity=options['parity'],
        stopbits=options['stopbits'],
        rtscts=options['rtscts'],
        xonxoff=options['xonxoff'],
        timeout=options['timeout'],
    )


def serial_close(ser):
    if ser:
        ser.close()


def serial_do_operation(operation, params):
    options, data = serial_options(params)
    result = {}
    ser = None
    try:
        ser = serial_open(options)
        if ser:
            if operation == 'read':
                data = ser.readline()
                app.logger.debug('serial: read done (data: "%s")' %
                    data.strip()
                )
                result['data'] = data
            else:
                ser.write(data)
                app.logger.debug('serial: write done (data: "%s")' %
                    data.strip()
                )
            result['status'] = 'ok'

    except serial.SerialException, message:
        result['status'] = 'error'
        result['message'] = str(message)

    serial_close(ser)

    return result


@app.route('/hw_proxy/serial_read', methods=['POST'])
def serial_read_http():
    result = serial_do_operation('read', request.json)
    return jsonify(jsonrpc='2.0', result=result)


@app.route('/hw_proxy/serial_write', methods=['POST'])
def serial_write_http():
    result = serial_do_operation('write', request.json)
    return jsonify(jsonrpc='2.0', result=result)
