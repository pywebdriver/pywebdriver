# Copyright (C) 2019 Druidoo (https://www.druidoo.io)
# Copyright (C) 2014 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import socket
import time
import traceback
from queue import Empty

from flask import jsonify, request

from pywebdriver import app, drivers

from .base_driver import ThreadDriver

BUFFER_SIZE = 1024
KEEPALIVE_TIME_LIMIT = 120
KEEPALIVE_INTERVAL = 30
SOCKET_TIMEOUT = 30
INITIALIZE_TIMEOUT = 240

ALLOWED_COMMANDS = [
    "initialize",
    "start_add_change",
    "start_acceptance",
    "get_amount_accepted",
    "stop_acceptance",
    "dispense",
    "get_inventory",
    "get_total_amount",
    "display_transaction_start",
    "display_close_till",
    "display_complete_emptying",
    "display_empty_stacker",
    "display_backoffice",
]


class CashlogyDriver(ThreadDriver):
    """Cashlogy Automatic Cashdrawer Driver

    Communicates with a Cashlogy device via TCP socket through the
    CashlogyConnector middleware.
    """

    def __init__(self):
        super().__init__()
        self.device_name = "Automatic Cashdrawer"
        self.socket = None
        self.status = {"status": "disconnected", "messages": ["Stand by.."]}
        self._device_config = {}
        self._keepalive_tick = time.time()

    def get_status(self, **kwargs):
        # Called frequently by the POS via /hw_proxy/status_json.
        # Update the keepalive tick so the connection stays alive while a session is active.
        self._keepalive_tick = time.time()
        return self.status

    def _check_keep_alive(self):
        # Disconnect if the POS has not polled status in KEEPALIVE_TIME_LIMIT seconds.
        now = time.time()
        if (
            self.status.get("status") == "connected"
            and (now - self._keepalive_tick) >= KEEPALIVE_TIME_LIMIT
        ):
            app.logger.debug("Cashlogy: disconnected because of inactivity")
            self.disconnect()

    def run(self):
        while True:
            try:
                self._check_keep_alive()
                try:
                    timestamp, task, data = self.queue.get(timeout=KEEPALIVE_INTERVAL)
                except Empty:
                    continue
                self.process_task(task, timestamp, data)
            except Exception as e:
                self.set_status("error", str(e))
                errmsg = (
                    str(e)
                    + "\n"
                    + "-" * 60
                    + "\n"
                    + traceback.format_exc()
                    + "-" * 60
                    + "\n"
                )
                app.logger.error(errmsg)

    def connect(self, config):
        """Connect to CashlogyConnector and initialize the device.

        Returns True on success.
        """
        if not config:
            config = {}
        host = config.get("host")
        port = int(config.get("port", 0))
        if not host or not port:
            self.set_status(
                "error",
                "Configuration error (host: %s, port: %s)" % (host, port),
            )
            return False
        try:
            self.set_status("connecting")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(SOCKET_TIMEOUT)
            self.socket.connect((host, port))
            self.set_status("connecting", "Initializing..")
            self.initialize()
            self.set_status("connected")
            self._device_config = config
            return True
        except Exception as e:
            self.set_status("error", repr(e))
            return False

    def initialize(self):
        """Initialize the machine. Takes around 1 minute on first run.

        Returns the firmware version string.
        """
        self.socket.settimeout(INITIALIZE_TIMEOUT)
        try:
            res = self.send(["I"])
        finally:
            self.socket.settimeout(SOCKET_TIMEOUT)
        return res[1]

    def disconnect(self):
        """Send disconnect command and close the connection."""
        if self.status.get("status") == "connected":
            self.send(["E"])
        self.set_status(
            "disconnected", "No request to connect from POS. Standing by.."
        )

    def keepalive(self, device_config=None, force=False):
        """Connect or reconnect to CashlogyConnector if needed.

        If force=True, reconnects even if in error state.
        Returns get_status().
        """
        status = self.status.get("status")
        if (device_config and status == "disconnected") or (
            force and status not in ["connected", "connecting"]
        ):
            self.push_task("connect", device_config)
        return self.get_status()

    def _send(self, msg, blocking=False):
        """Raw socket send and receive."""
        with self.lock:
            try:
                if blocking:
                    self.socket.settimeout(None)
                self.socket.send(msg.encode() if isinstance(msg, str) else msg)
                res = self.socket.recv(BUFFER_SIZE)
            except Exception as e:
                self.set_status("error", repr(e))
                raise
            finally:
                if blocking:
                    self.socket.settimeout(SOCKET_TIMEOUT)
        return res.decode()

    def send(self, msg, raw=False, blocking=False):
        """Send a message to CashlogyConnector and return the parsed response.

        Args:
            msg:      Either a raw string '#I#0#1#' or a list ['I', 0, 1]
            raw:      If True, return the raw response string unparsed
            blocking: If True, disable socket timeout (for long operations)

        Returns a list split on '#' delimiter, e.g. ['I', '2.01']
        """
        if not isinstance(msg, str):
            iter(msg)  # raises TypeError if not iterable
            for i, v in enumerate(msg):
                if isinstance(v, str):
                    continue
                elif isinstance(v, bool):
                    msg[i] = str(int(v))
                elif isinstance(v, int):
                    msg[i] = str(v)
                elif isinstance(v, float):
                    msg[i] = str(int(v * 100))
                else:
                    app.logger.debug("Cashlogy: unrecognized param type: %s", v)
                    msg[i] = str(v)
            msg = "#%s#" % "#".join(msg)
        res_raw = self._send(msg, blocking=blocking)
        res = res_raw.strip("#").split("#")
        if res and res[0].startswith("ER:"):
            raise Exception("Cashlogy error: %s (sent: %s)" % (res_raw, msg))
        elif res and res[0].startswith("WR:"):
            app.logger.warning("Cashlogy warning: %s (sent: %s)", res_raw, msg)
        if raw:
            return res_raw
        return res

    def value_float(self, value):
        """Convert Cashlogy integer-cents string to float euros."""
        if isinstance(value, str):
            return float(value) / 100
        elif isinstance(value, int):
            return float(value)
        elif isinstance(value, float):
            return value
        else:
            raise TypeError("Unrecognized type for value_float: %s" % type(value))

    def display_backoffice(self):
        """Display the backoffice screen on the cashier display."""
        return self.send("#G#1#1#1#1#1#1#1#1#1#1#1#1#1#", blocking=True)

    def get_inventory(self):
        """Get the content of the cashdrawer by denomination.

        Returns dict with 'recycler', 'stacker', 'total' where each value
        is a dict of {denomination_float: count}.
        """
        res = self.send(["Y"])
        recycler = {
            self.value_float(i[0]): int(i[1])
            for i in [p.split(":") for p in res[1].replace(";", ",").split(",")]
        }
        stacker = {
            self.value_float(i[0]): int(i[1])
            for i in [p.split(":") for p in res[2].replace(";", ",").split(",")]
        }
        totals = {
            v: recycler.get(v, 0) + stacker.get(v, 0)
            for v in set(list(recycler.keys()) + list(stacker.keys()))
        }
        return {"recycler": recycler, "stacker": stacker, "total": totals}

    def get_total_amount(self):
        """Get the total cash amount in the cashdrawer.

        Returns dict with 'recycler', 'stacker', 'total' amounts in euros.
        """
        res = self.send(["T"])
        recycler = self.value_float(res[1])
        stacker = self.value_float(res[2])
        return {"recycler": recycler, "stacker": stacker, "total": recycler + stacker}

    def dispense(self, amount, options=None):
        """Dispense the given amount from the cashdrawer.

        Returns the actual amount dispensed.
        """
        if not options:
            options = {}
        amount = float(amount)
        res = self.send(["P", amount, False, options.get("only_coins", False)])
        return self.value_float(res[1])

    def start_add_change(self):
        """Set the machine to accept money for adding change."""
        return self.send(["A", 2])

    def start_acceptance(self):
        """Set the machine to accept cash for a sale operation."""
        return self.send(["B", 0])

    def get_amount_accepted(self):
        """Return the amount accepted by the machine so far."""
        res = self.send(["Q"])
        return self.value_float(res[1])

    def stop_acceptance(self):
        """Stop the cash acceptance operation.

        Returns the total amount loaded.
        """
        res = self.send(["J"])
        return self.value_float(res[1])

    def display_transaction_start(self, amount, options):
        """Run a complete cash transaction (customer pays, machine gives change).

        Returns dict with 'amount_in', 'amount_out', 'amount' (net received).
        """
        amount = float(amount)
        operation_number = options.get("operation_number", "00000")
        msg = ["C", operation_number, 1, amount, 15, 15, 1, 1, 1, 0, 0]
        res = self.send(msg, blocking=True)
        amount_in = self.value_float(res[1])
        amount_out = self.value_float(res[2])
        return {
            "amount_in": amount_in,
            "amount_out": amount_out,
            "amount": amount_in - amount_out,
        }

    def display_close_till(self):
        """Display the backoffice till closure wizard.

        Returns dict with 'total_before', 'added', 'total', 'dispensed'.
        """
        res = self.send(["F", True], blocking=True)
        result = {
            "total_before": self.value_float(res[1]),
            "added": self.value_float(res[2]),
            "total": self.value_float(res[3]),
        }
        result["dispensed"] = (
            result["total_before"] + result["added"] - result["total"]
        )
        return result

    def display_complete_emptying(self):
        """Display the backoffice complete emptying wizard.

        Returns the total amount removed from the machine.
        """
        res = self.send(["V", True, ""], blocking=True)
        return self.value_float(res[1])

    def display_empty_stacker(self):
        """Display the backoffice empty stacker wizard.

        Returns the amount removed from the stacker.
        """
        res = self.send(["S", True], blocking=True)
        return self.value_float(res[1])


cashlogy_cashdrawer_driver = CashlogyDriver()
drivers["cashlogy_cashdrawer_driver"] = cashlogy_cashdrawer_driver

@app.route("/hw_proxy/cashlogy/connect", methods=["POST"])
def cashlogy_connect():
    """Receive connection config and connect/reconnect if needed."""
    params = request.json or {}
    device_config = params.get("config", {})
    result = cashlogy_cashdrawer_driver.keepalive(device_config, force=True)
    return jsonify(jsonrpc="2.0", result=result)

    
@app.route("/hw_proxy/cashlogy/<string:cmd>", methods=["POST"])
def cashlogy_command(cmd):
    """Dispatch a command to the cashdrawer driver."""
    if cmd not in ALLOWED_COMMANDS:
        return jsonify(jsonrpc="2.0", result={"error": "Invalid command: %s" % cmd}), 400
    params = request.json or {}
    result = getattr(cashlogy_cashdrawer_driver, cmd)(**params)
    return jsonify(jsonrpc="2.0", result=result)
