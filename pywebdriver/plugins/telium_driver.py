# Copyright (C) 2014-Today Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import pypostelium
import simplejson as json
from flask import jsonify, render_template, request

from pywebdriver import app, config, drivers

from .base_driver import ThreadDriver


class TeliumDriver(ThreadDriver, pypostelium.Driver):
    """Telium Driver class for pywebdriver"""

    def __init__(self, *args, **kwargs):
        ThreadDriver.__init__(self)
        pypostelium.Driver.__init__(self, *args, **kwargs)
        # TODO : FIXME : Remove once 'status-posdisplay' branch is merged
        self.vendor_product = None

    def get_payment_info_from_price(self, price, payment_mode):
        return {
            "amount": price,
            "payment_mode": payment_mode,
            "currency_iso": "EUR",
        }


driver_config = {}
if config.get("telium_driver", "device_name"):
    driver_config["telium_terminal_device_name"] = config.get(
        "telium_driver", "device_name"
    )
if config.getint("telium_driver", "device_rate"):
    driver_config["telium_terminal_device_rate"] = config.getint(
        "telium_driver", "device_rate"
    )

telium_driver = TeliumDriver(driver_config)
drivers["telium"] = telium_driver


@app.route(
    "/hw_proxy/payment_terminal_transaction_start", methods=["POST", "GET", "PUT"]
)
def payment_terminal_transaction_start():
    app.logger.debug("Telium: Call payment_terminal_transaction_start")
    payment_info = request.json["params"]["payment_info"]
    app.logger.debug("Telium: payment_info=%s", payment_info)
    result = telium_driver.transaction_start(payment_info)
    app.logger.debug("Telium: result of transation_start=%s", result)
    return jsonify(jsonrpc="2.0", result=result)


@app.route("/telium_status.html", methods=["POST"])
def telium_status():
    values = request.form.to_dict()
    info = telium_driver.get_payment_info_from_price(
        float(values.get("price") or 0.00), request.values["payment_mode"]
    )
    app.logger.debug("Telium status info=%s", info)
    telium_driver.push_task("transaction_start", json.dumps(info, sort_keys=True))
    return render_template("telium_status.html")
