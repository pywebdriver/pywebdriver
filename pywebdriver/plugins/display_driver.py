###############################################################################
#
#   Copyright (C) 2014-2016 Akretion (http://www.akretion.com).
#   @author Sébastien BEAU <sebastien.beau@akretion.com>
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
        ([u"PyWebDriver", u"By"], 2),
        ([u"Sylvain CALADOR", u"@ Akretion"], 1.5),
        ([u"Sébastien BEAU", u"@ Akretion"], 1.5),
        ([u"Sylvain LE GAL", u"@ GRAP"], 1.5),
        ([u"Status:", u"OK"], 5),
    ]
    installed = True

    class DisplayDriver(ThreadDriver, pyposdisplay.Driver):
        """ Display Driver class for pywebdriver """

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
