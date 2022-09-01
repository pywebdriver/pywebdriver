import flask
import simplejson as json
from erpbrasil.driver.sat import driver
from flask import jsonify, render_template, request

from pywebdriver import app, config, drivers

from .base_driver import ThreadDriver


class SatDriver(ThreadDriver, driver.Sat):

    def __init__(self, *args, **kwargs):
        ThreadDriver.__init__(self)
        driver.Sat.__init__(self, *args, **kwargs)


#if config.get("sat_driver", "sat_path"):
#    driver_config["sat_path"] = config.get(
#        "sat_driver", "sat_path"
#    )

#if config.get("sat_driver", "codigo_ativacao"):
#    driver_config["codigo_ativacao"] = config.get(
#        "sat_driver", "codigo_ativacao"
#    )

#if config.get("sat_driver", "impressora"):
#    driver_config["impressora"] = config.get(
#        "sat_driver", "impressora"
#    )

#if config.get("sat_driver", "printer_params"):
#    driver_config["printer_params"] = config.get(
#        "sat_driver", "printer_params"
#    )

#if config.get("sat_driver", "fiscal_printer_type"):
#    driver_config["fiscal_printer_type"] = config.get(
#        "sat_driver", "fiscal_printer_type"
#    )

#if config.get("sat_driver", "assinatura"):
#    driver_config["assinatura"] = config.get(
#        "sat_driver", "assinatura"
#    )

#if config.get("sat_driver"):
#    sat_driver = SatDriver(**driver_config)
#    drivers["hw_fiscal"] = sat_driver
#else:

@app.route('/hw_proxy/init', methods=["POST", "GET", "PUT"])
def int_sat():
    res = request.json["params"]["json"]
    sat_driver = SatDriver(**res)
    drivers["hw_fiscal"] = sat_driver
    return jsonify(success=True)
    # TODO: Verificar a questão do retorno do init.
    # {"jsonrpc": "2.0", "id": 581330955, "result": true}

@app.route('/hw_proxy/enviar_cfe_sat/', methods=["POST", "GET", "PUT"])
def enviar_cfe_sat():
    res = drivers['hw_fiscal'].action_call_sat('send', request.json["params"]['json'])
    return jsonify(jsonrpc= "2.0", result=res)


@app.route('/hw_proxy/cancelar_cfe/', methods=["POST", "GET", "PUT"])
def cancelar_cfe():
    res = drivers['hw_fiscal'].action_call_sat('cancel', request.json["params"]['json'])
    return jsonify(jsonrpc= "2.0", result=res)


@app.route('/hw_proxy/reprint_cfe/', methods=["POST", "GET", "PUT"])
def reprint_cfe():
    res = drivers['hw_fiscal'].action_call_sat('reprint', request.json["params"]['json'])
    return jsonify(jsonrpc="2.0", result=res)

@app.route('/hw_proxy/sessao_sat', methods=["POST"])
def sessao_sat():
    res = drivers['hw_fiscal'].action_call_sat('sessao')
    return jsonify(jsonrpc="2.0", result=res)
