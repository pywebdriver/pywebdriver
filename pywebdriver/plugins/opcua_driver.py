# Copyright (C) 2016-Today Akretion (http://www.akretion.com).
# @author Sylvain Calador <sylvain.calador@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import simplejson as json
from flask import jsonify, make_response, request

from pywebdriver import app, config, drivers

try:

    from opcua import Client, ua
    from opcua.ua.status_codes import code_to_name_doc

    def get_variant_type(datatype):

        if datatype == "bool":
            variant = ua.VariantType.Boolean
        elif datatype == "sbyte":
            variant = ua.VariantType.SByte
        elif datatype == "byte":
            variant = ua.VariantType.Byte
        elif datatype == "uint16":
            variant = ua.VariantType.UInt16
        elif datatype == "unint32":
            variant = ua.VariantType.UInt32
        elif datatype == "uint64":
            variant = ua.VariantType.UInt64
        elif datatype == "int16":
            variant = ua.VariantType.Int16
        elif datatype == "int32":
            variant = ua.VariantType.Int32
        elif datatype == "int64":
            variant = ua.VariantType.Int64
        elif datatype == "float":
            variant = ua.VariantType.Float
        elif datatype == "double":
            variant = ua.VariantType.Double
        elif datatype == "string":
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
                commands_ok.append({"nodeid": nodeid, "value": node.get_value()})
            except Exception as err:
                error = code_to_name_doc.get(err.message, ("", "N/A"))
                commands_ko.append({"nodeid": nodeid, "error": error[1]})
        return commands_ok, commands_ko

    def opcua_init(request):

        client = Client(
            request.get("url", "opc.tcp://localhost:4841"),
            timeout=request.get("timeout", 10),
        )
        client.set_security_string(request.get("security", ""))
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
                request.get("commands", []),
            )
        except Exception as error:
            global_error = error.message
        finally:
            try:
                client.disconnect()
            except:
                pass

        return {
            "global_error": global_error,
            "commands_ok": commands_ok,
            "commands_ko": commands_ko,
        }

    @app.route("/hw_proxy/opcua_write", methods=["POST"])
    def opcua_write_http():
        result = opcua_write(request.json)
        return jsonify(jsonrpc="2.0", result=result)


except ImportError:
    app.logger.info("opcua lib not found, function disabled")
