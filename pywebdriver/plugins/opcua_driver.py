# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2016 Akretion (http://www.akretion.com).
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

from flask import app, request, make_response, jsonify
import simplejson as json
from pywebdriver import app, config, drivers

try:

    from opcua import Client, ua
    from opcua.ua.status_codes import code_to_name_doc

    def get_variant_type(datatype):

        if datatype == 'bool':
            variant = ua.VariantType.Boolean
        elif datatype == 'sbyte':
            variant = ua.VariantType.SByte
        elif datatype == 'byte':
            variant = ua.VariantType.Byte
        elif datatype == 'uint16':
            variant = ua.VariantType.UInt16
        elif datatype == 'unint32':
            variant = ua.VariantType.UInt32
        elif datatype == 'uint64':
            variant = ua.VariantType.UInt64
        elif datatype == 'int16':
            variant = ua.VariantType.Int16
        elif datatype == 'int32':
            variant = ua.VariantType.Int32
        elif datatype == 'int64':
            variant = ua.VariantType.Int64
        elif datatype == 'float':
            variant = ua.VariantType.Float
        elif datatype == 'double':
            variant = ua.VariantType.Double
        elif datatype == 'string':
            variant = ua.VariantType.String
        else:
            raise ValueError('"%s" datatype not implemented' % datatype)

        return variant

    def do_write(client, commands):
        commands_ok = []
        commands_ko = []
        for nodeid, datatype, value in commands:
            try:
                node = client.get_node(str(nodeid))
                variant_type = get_variant_type(datatype)
                node.set_value(value, variant_type)
                commands_ok.append(
                    {'nodeid': nodeid, 'value': node.get_value()})
            except Exception, err:
                error = code_to_name_doc.get(err.message, ('', 'N/A'))
                commands_ko.append({'nodeid': nodeid, 'error': error[1]})
        return commands_ok, commands_ko

    def opcua_init(request):

        client = Client(
            request.get('url', 'opc.tcp://localhost:4841'),
            timeout=request.get('timeout', 10)
        )
        client.set_security_string(request.get('security', ''))
        client.connect()

        return client

    def opcua_write(request):

        global_error = False
        commands_ok = False
        commands_ko = False
        try:
            client = opcua_init(request)
            commands_ok, commands_ko = do_write(
                client,
                request.get('commands', []),
            )
        except Exception, error:
            global_error = error.message
        finally:
            try:
                client.disconnect()
            except:
                pass

        return {
            'global_error': global_error,
            'commands_ok': commands_ok,
            'commands_ko': commands_ko,
        }

    @app.route('/hw_proxy/opcua_write', methods=['POST'])
    @cross_origin()
    def opcua_write_http():
        result = opcua_write(request.json)
        return jsonify(jsonrpc='2.0', result=result)

except ImportError:
    app.logger.info('opcua lib not found, function disabled')
