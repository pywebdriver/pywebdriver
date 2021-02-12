import json

from flask import jsonify, request

from pywebdriver import app, drivers

from .payment_base_driver import PaymentTerminalDriver


class PaymentMockDriver(PaymentTerminalDriver):
    def __init__(self):
        super(PaymentMockDriver, self).__init__()
        self._set_terminal_status(terminal_id="0", status="connected")

    def transaction_start(self, data):
        payment_info = data["payment_info"]
        transaction_id = data["transaction_id"]
        terminal_id = payment_info.get("terminal_id", "0")
        app.logger.info(
            "payment mock driver transaction start for terminal %s: %s",
            terminal_id,
            payment_info,
        )
        status = input("status: enter 'ok' for sucess, or any other status: ")
        if status == "ok":
            self.end_transaction(
                terminal_id,
                transaction_id,
                success=True,
            )
        else:
            self.end_transaction(
                terminal_id,
                transaction_id,
                success=False,
                status=status,
                reference="",
            )


@app.route("/hw_proxy/payment_terminal_transaction_start", methods=["POST"])
def payment_terminal_transaction_start():
    # TODO why json in json?
    payment_info = json.loads(request.json["params"]["payment_info"])
    terminal_id = payment_info.get("terminal_id", "0")
    transaction = payment_mock_driver.begin_transaction(terminal_id)
    payment_mock_driver.push_task(
        "transaction_start",
        data=dict(
            payment_info=payment_info, transaction_id=transaction["transaction_id"]
        ),
    )
    return jsonify(jsonrpc="2.0", result=transaction)


payment_mock_driver = PaymentMockDriver()
drivers["payment_mock_driver"] = payment_mock_driver
