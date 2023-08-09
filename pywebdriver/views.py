# Copyright (C) 2014-Today Akretion (http://www.akretion.com).
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import os
import platform
import subprocess
import sys

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata
else:  # Python < 3.8
    import importlib_metadata

from flask import render_template
from flask_babel import gettext as _

from pywebdriver import app, config, drivers


@app.route("/", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/status.html", methods=["GET"])
def status():
    drivers_info = {}

    for driver in drivers:
        tmp = drivers[driver].get_vendor_product()
        if tmp:
            image = "static/images/" + tmp + ".png"
        else:
            image = None
        drivers_info[driver] = {
            "state": drivers[driver].get_status(),
            "image": image,
        }
    return render_template("status.html", drivers_info=drivers_info)


@app.route("/usb_devices.html", methods=["GET"])
def usb_devices():
    str_devices = subprocess.getoutput("lsusb").split("\n")
    devices = []
    for device in str_devices:
        devices.append(
            {
                "bus": device.split(": ID ")[0].split(" ")[1],
                "device": device.split(": ID ")[0].split(" ")[3],
                "id": device.split(": ID ")[1][:9],
                "description": device.split(": ID ")[1][10:],
            }
        )
    return render_template("usb_devices.html", devices=devices)


@app.route("/system.html", methods=["GET"])
def system():
    pywebdriver_info = []
    pywebdriver_info.append(
        {
            "name": _("CORS allowed origins"),
            "value": config.get("flask", "cors_origins"),
        }
    )
    system_info = []
    system_info.append({"name": _("OS - System"), "value": platform.system()})
    system_info.append({"name": _("OS - Release"), "value": platform.release()})
    system_info.append({"name": _("OS - Version"), "value": platform.version()})
    system_info.append({"name": _("Machine"), "value": platform.machine()})
    system_info.append(
        {"name": _("Python Version"), "value": platform.python_version()}
    )
    distributions = importlib_metadata.distributions()
    installed_python_packages = []
    for distribution in distributions:
        installed_python_packages.append(distribution.metadata)
    installed_python_packages = sorted(
        installed_python_packages, key=lambda package: package["name"].upper()
    )
    return render_template(
        "system.html",
        pywebdriver_info=pywebdriver_info,
        system_info=system_info,
        installed_python_packages=installed_python_packages,
    )


@app.route("/static/images/<path:path>", methods=["POST", "GET", "PUT", "OPTIONS"])
def image_html(path=None):
    return app.send_static_file(os.path.join("images/", path))
