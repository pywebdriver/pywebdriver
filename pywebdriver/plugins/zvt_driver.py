###############################################################################
#
#   Copyright (C) 2022 initOS (http://www.initos.com).
#   @author Florian Kantelberg <florian.kantelberg@initos.com>
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

import simplejson as json
from ecrterm.ecr import ECR
from ecrterm.packets.base_packets import Registration
from flask import jsonify, request
from pywebdriver import app, config, drivers

from .payment_base_driver import PaymentTerminalDriver

ZVTRegistrationDefaults = [
    ("ecr_prints_receipt", False),
    ("ecr_prints_admin_receipt", False),
    ("ecr_intermediate_status", True),
    ("ecr_controls_payment", True),
    ("ecr_controls_admin", False),
    ("ecr_use_print_lines", True),
]


class ZVTDriver(PaymentTerminalDriver):
    """ Telium Driver class for pywebdriver """

    def __init__(self):
        super().__init__()
        self.device = None

    def zvt_status(self):
        """Get the connection status of the device"""
        with self.lock:
            status = self.device and self.device.detect_pt()

        self._set_terminal_status("0", "connected" if status else "disconnected")
        return status

    def zvt_connect(self):
        """Connect to the device"""
        cfg = {}
        for field in ["device", "password", "baudrate"]:
            if config.has_option("zvt_driver", field):
                cfg[field] = config.get("zvt_driver", field)

        with self.lock:
            try:
                self.device = ECR(**cfg)

                config_byte = Registration.generate_config(
                    **{
                        field: config.getboolean("zvt_driver", field, fallback=fallback)
                        for field, fallback in ZVTRegistrationDefaults
                    }
                )
                self.device.register(config_byte)
            except Exception as e:
                app.logger.error("ZVT Error - %s", e)
                self.device = None

    def get_payment_info_from_price(self, price, payment_mode):
        return {
            "amount": price,
            "payment_mode": payment_mode,
            "currency_iso": "EUR",
        }

    def get_status(self, terminal_id="0", **kwargs):
        # Try to reconnect if not connected
        if not self.zvt_status():
            self.zvt_connect()
            self.zvt_status()
        return super().get_status("0", **kwargs)

    def _payment(self, amount, refund):
        if amount < 0:
            return False

        try:
            if refund:
                return self.device.refund(amount)
            return self.device.payment(amount)
        except Exception as e:
            app.logger.exception(e)
            self.device = None
            return False

    def transaction_start(self, data):
        payment_info = data["payment_info"]

        success = False
        status = reference = ""
        if self.zvt_status() and self._payment(
            int(100 * payment_info["amount"]), payment_info.get("refund")
        ):
            success = True
        else:
            status = "ZVT Driver - Device not connected"

        if success:
            last_transaction = self.device.last
            reference = getattr(last_transaction, "tid", "")
            status = "success"

        self.end_transaction(
            "0",
            data["transaction_id"],
            success=success,
            status=status,
            reference=reference,
        )

    def _end_of_day(self):
        try:
            return self.device.end_of_day()
        except Exception as e:
            app.logger.exception(e)
            self.device = None
            return False

    def end_of_day(self, data):
        status = message = ""
        if self.zvt_status() and self._end_of_day():
            lines = self.device.daylog
            message = "\n".join(lines)
            try:
                # assume device sends CP-437 strings (the default)
                message = bytes([ord(i) for i in message]).decode("cp437")
            except Exception:
                pass

            status = "success"
        else:
            status = "ZVT Driver - Device not connected"

        return {
            "status": status,
            "message": message,
        }


drivers["zvt"] = zvt_driver = ZVTDriver()


@app.route(
    "/hw_proxy/payment_terminal_transaction_start",
    methods=["POST", "GET", "PUT"],
)
def payment_terminal_transaction_start():
    payment_info = json.loads(request.json["params"]["payment_info"])
    transaction = zvt_driver.begin_transaction("0")
    zvt_driver.push_task(
        "transaction_start",
        data={
            "payment_info": payment_info,
            "transaction_id": transaction["transaction_id"],
        },
    )
    return jsonify(jsonrpc="2.0", result=transaction)


@app.route(
    "/hw_proxy/payment_terminal_end_of_day",
    methods=["POST", "GET", "PUT"],
)
def payment_terminal_end_of_day():
    return jsonify(jsonrpc="2.0", result=zvt_driver.end_of_day({}))
