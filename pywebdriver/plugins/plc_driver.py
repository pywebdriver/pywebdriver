# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2016 Oliverstore (http://www.akretion.com).
#   @author Marcin Wojtysiak <m.wojtysiak@oliverstore.com>
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

from flask import app, request, make_response, jsonify
import simplejson as json
from pywebdriver import app, config, drivers

try:

    from pylogix import PLC

    def do_write(client, commands):
        commands_ok = []
        commands_ko = []
        for tag_name, datatype, value in commands:
            try:
                # TODO: For this moment we only use INT datatype
                # this is for improve in future
                client.Write(tag_name, int(value))
            except Exception, err:
                error = code_to_name_doc.get(err.message, ('', 'N/A'))
                commands_ko.append({'nodeid': nodeid, 'error': error[1]})
        return commands_ok, commands_ko

    def plc_init(request):
        client = PLC()
        client.Micro800 = config.get('plc', 'micro800') or False
        client.IPAddress = request.get('url', '')

        return client

    def plc_write(request):

        global_error = False
        commands_ok = False
        commands_ko = False
        try:
            client = plc_init(request)
            commands_ok, commands_ko = do_write(
                client,
                request.get('commands', []),
            )
        except Exception, error:
            global_error = error.message

        return {
            'global_error': global_error,
            'commands_ok': commands_ok,
            'commands_ko': commands_ko,
        }

    @app.route('/hw_proxy/plc_write', methods=['POST'])
    def opcua_write_http():
        result = plc_write(request.json)
        return jsonify(jsonrpc='2.0', result=result)

except ImportError:
    app.logger.info('pylogix lib not found, function disabled')
