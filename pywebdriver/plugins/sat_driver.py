import simplejson as json
from flask import jsonify, render_template, request

from pywebdriver import app, config, drivers

from .base_driver import ThreadDriver
from erpbrasil.driver.sat import driver


class SatDriver(ThreadDriver, driver.Sat):

    def __init__(self, *args, **kwargs):
        ThreadDriver.__init__(self)
        driver.Sat.__init__(self, *args, **kwargs)


driver_config = {}

if config.get("sat_driver", "sat_path"):
    driver_config["sat_path"] = config.get(
        "sat_driver", "sat_path"
    )

if config.getint("sat_driver", "codigo_ativacao"):
    driver_config["codigo_ativacao"] = config.getint(
        "sat_driver", "codigo_ativacao"
    )

if config.get("sat_driver", "impressora"):
    driver_config["impressora"] = config.get(
        "sat_driver", "impressora"
    )

if config.get("sat_driver", "printer_params"):
    driver_config["printer_params"] = config.get(
        "sat_driver", "printer_params"
    )

if config.get("sat_driver", "fiscal_printer_type"):
    driver_config["fiscal_printer_type"] = config.get(
        "sat_driver", "fiscal_printer_type"
    )

if config.get("sat_driver", "assinatura"):
    driver_config["assinatura"] = config.get(
        "sat_driver", "assinatura"
    )

sat_driver = SatDriver(**driver_config)
drivers["sat"] = sat_driver


@app.route('/hw_proxy/enviar_cfe_sat/', methods=["POST", "GET", "PUT"])
def enviar_cfe_sat():
    return drivers['sat'].action_call_sat('send', request.json["params"]['json'])


@app.route('/hw_proxy/cancelar_cfe/', methods=["POST", "GET", "PUT"])
def cancelar_cfe():
    return drivers['sat'].action_call_sat('cancel', request.json["params"]['json'])


@app.route('/hw_proxy/reprint_cfe/', methods=["POST", "GET", "PUT"])
def reprint_cfe():
    return drivers['sat'].action_call_sat('reprint', request.json["params"]['json'])


@app.route('/hw_proxy/sessao_sat/', methods=["POST", "GET", "PUT"])
def sessao_sat():
    return drivers['sat'].action_call_sat('sessao')
