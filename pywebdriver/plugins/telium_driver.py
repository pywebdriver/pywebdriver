# Copyright (C) 2014-Today Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import pypostelium
import simplejson as json
from flask import jsonify, render_template, request
from serial import Serial

from pywebdriver import app, config, drivers

from .payment_base_driver import PaymentTerminalDriver

# Telium E+ delay flag asking the terminal to answer at the end of the
# transaction (A011 asks for an immediate answer)
DELAY_WAIT_FOR_TRANSACTION = "A010"
TRANSACTION_SUCCESS = "0"
# Telium spec: wait up to 3 seconds for each control byte and the LRC
CONTROL_TIMEOUT = 3


class TeliumDriver(PaymentTerminalDriver, pypostelium.Driver):
    """Telium Driver class for pywebdriver"""

    def __init__(self, driver_config):
        PaymentTerminalDriver.__init__(self)
        pypostelium.Driver.__init__(self, driver_config)
        self.transaction_timeout = int(
            driver_config.get("telium_terminal_transaction_timeout", 120)
        )
        # TODO : FIXME : Remove once 'status-posdisplay' branch is merged
        self.vendor_product = None

    def get_payment_info_from_price(self, price, payment_mode):
        return {
            "amount": price,
            "payment_mode": payment_mode,
            "currency_iso": "EUR",
        }

    def get_status(self, terminal_id="0", **kwargs):
        port_status = pypostelium.Driver.get_status(self)
        self._set_terminal_status(terminal_id, port_status["status"])
        terminal = dict(PaymentTerminalDriver.get_status(self, terminal_id))
        terminal["messages"] = port_status["messages"]
        return terminal

    def transaction_start(self, data):
        payment_info = data["payment_info"]
        terminal_id = payment_info.get("terminal_id", "0")
        try:
            success, status = self._telium_transaction(payment_info)
        except Exception as e:
            success, status = False, str(e)
        if not success:
            app.logger.error("Telium: %s", status)
        self.end_transaction(
            terminal_id, data["transaction_id"], success=success, status=status
        )

    def _telium_transaction(self, payment_info):
        msg = self.prepare_data_to_send(payment_info)
        if not msg:
            return False, "Unsupported payment information"
        msg["delay"] = DELAY_WAIT_FOR_TRANSACTION
        self.serial = Serial(
            self.device_name, self.device_rate, timeout=CONTROL_TIMEOUT
        )
        try:
            if not self.initialize_msg():
                return False, "No answer from the payment terminal"
            self.send_message(msg)
            if not self.get_one_byte_answer("ACK"):
                return False, "Payment request refused by the payment terminal"
            self.send_one_byte_signal("EOT")
            self.serial.timeout = self.transaction_timeout
            if not self.get_one_byte_answer("ENQ"):
                return False, "No transaction result from the payment terminal"
            self.serial.timeout = CONTROL_TIMEOUT
            self.send_one_byte_signal("ACK")
            answer = self.get_answer_from_terminal(msg)
            self.send_one_byte_signal("ACK")
            self.get_one_byte_answer("EOT")
        finally:
            self.serial.close()
        result = answer["transaction_result"]
        if result != TRANSACTION_SUCCESS:
            return (
                False,
                "Transaction refused by the payment terminal (code %s)" % result,
            )
        return True, None


driver_config = {}
if config.get("telium_driver", "device_name"):
    driver_config["telium_terminal_device_name"] = config.get(
        "telium_driver", "device_name"
    )
if config.getint("telium_driver", "device_rate"):
    driver_config["telium_terminal_device_rate"] = config.getint(
        "telium_driver", "device_rate"
    )
driver_config["telium_terminal_transaction_timeout"] = config.getint(
    "telium_driver", "transaction_timeout", fallback=120
)

telium_driver = TeliumDriver(driver_config)
drivers["telium"] = telium_driver


def _start_transaction(payment_info):
    terminal_id = payment_info.get("terminal_id", "0")
    transaction = telium_driver.begin_transaction(terminal_id)
    telium_driver.push_task(
        "transaction_start",
        data=dict(
            payment_info=payment_info, transaction_id=transaction["transaction_id"]
        ),
    )
    return transaction


@app.route(
    "/hw_proxy/payment_terminal_transaction_start", methods=["POST", "GET", "PUT"]
)
def payment_terminal_transaction_start():
    app.logger.debug("Telium: Call payment_terminal_transaction_start")
    payment_info = json.loads(request.json["params"]["payment_info"])
    app.logger.debug("Telium: payment_info=%s", payment_info)
    return jsonify(jsonrpc="2.0", result=_start_transaction(payment_info))


@app.route("/telium_status.html", methods=["POST"])
def telium_status():
    values = request.form.to_dict()
    info = telium_driver.get_payment_info_from_price(
        float(values.get("price") or 0.00), request.values["payment_mode"]
    )
    app.logger.debug("Telium status info=%s", info)
    _start_transaction(info)
    return render_template("telium_status.html")
