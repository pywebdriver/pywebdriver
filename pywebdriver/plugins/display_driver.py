# Copyright (C) 2014-Today Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import time

import simplejson
from flask import jsonify, render_template, request

from pywebdriver import app, config, drivers

from .base_driver import ThreadDriver, check

meta = {
    "name": "POS Display",
    "description": """This plugin add the support of customer display for your
        pywebdriver""",
    "require_pip": ["pyposdisplay"],
    "require_debian": ["python-pyposdisplay"],
}

try:
    import pyposdisplay
except ImportError:
    installed = False
    print("DISPLAY: pyposdisplay python library not installed")
else:
    AUTHOR = [
        (["PyWebDriver", "By"], 2),
        (["Sylvain CALADOR", "@ Akretion"], 1.5),
        (["Sébastien BEAU", "@ Akretion"], 1.5),
        (["Sylvain LE GAL", "@ GRAP"], 1.5),
        (["Status:", "OK"], 5),
    ]
    installed = True

    class DisplayDriver(ThreadDriver, pyposdisplay.Driver):
        """Display Driver class for pywebdriver"""

        def __init__(self, *args, **kwargs):
            ThreadDriver.__init__(self)
            pyposdisplay.Driver.__init__(self, *args, **kwargs)
            # TODO FIXME (Actually hardcoded, but no possibility to know
            # the model easily
            self.vendor_product = "1504_11"

        def get_status(self, **params):
            status = {"status": "disconnected"}
            try:
                status = super().get_status()
                # When I use Odoo POS v8, it regularly displays
                # "PyWebDriver / PosBox Status" on the LCD !!!
                # So I comment the line below -- Alexis de Lattre
                # display_driver.push_task(
                #    'send_text', [_(u'PyWebDriver'), _(u'PosBox Status')])
                # TODO Improve Me
                # For the time being, it's not possible to know if the display
                # is 'disconnected' in 'error' state
                # Maybe could be possible, improving pyposdisplay library.
            except Exception:
                app.logger.debug("Could not retrieve serial display status")
            return status

        def display_status(self, display):
            for lines, duration in AUTHOR:
                self.send_text(lines)
                time.sleep(duration)

    driver_config = {}
    if config.get("display_driver", "device_name"):
        driver_config["customer_display_device_name"] = config.get(
            "display_driver", "device_name"
        )
    if config.getint("display_driver", "device_rate"):
        driver_config["customer_display_device_rate"] = config.getint(
            "display_driver", "device_rate"
        )
    if config.getfloat("display_driver", "device_timeout"):
        driver_config["customer_display_device_timeout"] = config.getfloat(
            "display_driver", "device_timeout"
        )
    driver_name = "bixolon"
    if config.has_option("display_driver", "driver_name"):
        driver_name = config.get("display_driver", "driver_name")

    display_driver = DisplayDriver(driver_config, use_driver_name=driver_name)
    drivers["display"] = display_driver


@app.route("/display_status.html", methods=["GET"])
def display_status_http():
    display_driver.push_task("display_status")
    return render_template("display_status.html")


@app.route("/hw_proxy/send_text_customer_display", methods=["POST", "GET", "PUT"])
@check(installed, meta)
def send_text_customer_display():
    app.logger.debug("LCD: Call send_text")
    text_to_display = request.json["params"]["text_to_display"]
    lines = simplejson.loads(text_to_display)
    app.logger.debug("LCD: lines=%s", lines)
    display_driver.push_task("send_text", lines)
    return jsonify(jsonrpc="2.0", result=True)
