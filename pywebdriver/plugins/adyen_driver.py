import json
import uuid
from datetime import datetime

import requests
from flask import jsonify, request

from pywebdriver import app, config, drivers

from .payment_base_driver import PaymentTerminalDriver

CONFIG_SECTION = "adyen_driver"


class AdyenDriver(PaymentTerminalDriver):
    def __init__(self):
        super(AdyenDriver, self).__init__()
        self.endpoint = config.get(CONFIG_SECTION, "endpoint", fallback=False)
        self.api_key = config.get(CONFIG_SECTION, "api_key", fallback=False)

    def _prepare_request_data(self, payment_info, terminal_id):
        return {
            "SaleToPOIRequest": {
                "MessageHeader": {
                    "ProtocolVersion": "3.0",
                    "MessageClass": "Service",
                    "MessageCategory": "Payment",
                    "MessageType": "Request",
                    "SaleID": terminal_id,
                    "ServiceID": str(uuid.uuid4().hex)[:10],
                    "POIID": terminal_id,
                },
                "PaymentRequest": {
                    "SaleData": {
                        "SaleTransactionID": {
                            "TransactionID": payment_info["order_id"],
                            "TimeStamp": datetime.utcnow()
                            .replace(microsecond=0)
                            .isoformat(),
                        }
                    },
                    "PaymentTransaction": {
                        "AmountsReq": {
                            "Currency": payment_info["currency_iso"],
                            "RequestedAmount": payment_info["amount"],
                        }
                    },
                },
            }
        }

    def transaction_start(self, data):
        payment_info = data["payment_info"]
        transaction_id = data["transaction_id"]
        terminal_id = payment_info.get("terminal_id", "0")
        app.logger.info(
            "adyen driver transaction start for terminal %s: %s",
            terminal_id,
            payment_info,
        )
        request_headers = {
            "x-API-key": self.api_key,
            "Content-Type": "application/json",
        }
        request_data = self._prepare_request_data(payment_info, terminal_id)
        success = False
        status = ""
        psp_reference = ""
        try:
            response = requests.post(
                self.endpoint, data=json.dumps(request_data), headers=request_headers
            )
            response.raise_for_status()
            json_response = response.json()
            if "SaleToPOIResponse" in json_response:
                status = json_response["SaleToPOIResponse"]["PaymentResponse"][
                    "Response"
                ]["Result"]
                POITransactionID = json_response["SaleToPOIResponse"][
                    "PaymentResponse"
                ]["POIData"]["POITransactionID"]["TransactionID"]
                if status == "Success":
                    tender_reference, psp_reference = POITransactionID.split(".")
                    success = True
            else:
                status = "Adyen driver - Event Error"
                app.logger.error(
                    "%s : %s",
                    status,
                    json_response["SaleToPOIRequest"]["EventNotification"],
                )
        except requests.exceptions.HTTPError as errh:
            status = "Adyen driver - HTTP Error"
            app.logger.error("%s : %s", status, errh)
        except requests.exceptions.ConnectionError as errc:
            status = "Adyen driver - Error Connecting"
            app.logger.error("%s : %s", status, errc)
        except requests.exceptions.Timeout as errt:
            status = "Adyen driver - Timeout Error"
            app.logger.error("%s : %s", status, errt)
        except requests.exceptions.RequestException as err:
            status = "Adyen driver - Request Error"
            app.logger.error("%s : %s", status, err)
        self.end_transaction(
            terminal_id,
            transaction_id,
            success=success,
            status=status,
            reference=psp_reference,
        )


@app.route("/hw_proxy/payment_terminal_transaction_start", methods=["POST"])
def payment_terminal_transaction_start():
    # TODO why json in json?
    payment_info = json.loads(request.json["params"]["payment_info"])
    terminal_id = payment_info.get("terminal_id", "0")
    transaction = adyen_driver.begin_transaction(terminal_id)
    adyen_driver.push_task(
        "transaction_start",
        data=dict(
            payment_info=payment_info, transaction_id=transaction["transaction_id"]
        ),
    )
    return jsonify(jsonrpc="2.0", result=transaction)


adyen_driver = AdyenDriver()
drivers["adyen_driver"] = adyen_driver
