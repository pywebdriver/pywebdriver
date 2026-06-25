# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


# Core Imports
import gettext
import logging.config
import os
import sys
from configparser import ConfigParser
from locale import getdefaultlocale

# Librairies Imports
from flask import Flask
from flask_babel import Babel
from flask_cors import CORS

# Config Section

# When frozen by PyInstaller, sys.executable is the .exe in the install root.
# The user-editable config lives in <install root>\config\config.ini — check
# that first so it takes priority over the bundled template in _internal\.
_exe_dir = os.path.dirname(os.path.realpath(sys.executable))
CONFIG_PATHS = (
    os.path.join(_exe_dir, "config", "config.ini"),
    "config.ini",
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "config", "config.ini"
    ),
    "/etc/pywebdriver/config.ini",
)

for config_file in CONFIG_PATHS:
    if os.path.isfile(config_file):
        break
else:
    logging.basicConfig()
    logging.error(
        "Could not find config.ini. Expected in one of: %s"
        " -- To fix: copy config\\config.ini.tmpl config\\config.ini"
        " and set your printer details.",
        ", ".join(CONFIG_PATHS),
    )
    sys.exit(1)

config = ConfigParser()
config.read(config_file)

if (
    config.has_section("loggers")
    and config.has_section("handlers")
    and config.has_section("formatters")
):
    logging.config.fileConfig(config)
else:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

logging.info("Using config file: %s", os.path.realpath(config_file))

drivers = {}

# Project Import
# Application
app = Flask(__name__)
try:
    cors_origins = config.get("flask", "cors_origins")
except Exception:
    logging.error(
        "config.ini is missing the [flask] section."
        " Add '[flask] / cors_origins = *' -- see config\\config.ini.tmpl for a full example."
    )
    sys.exit(1)
cors = CORS(app, resources={r"/*": {"origins": cors_origins}})

from . import plugins  # noqa: E402
from . import views  # noqa: E402

# Localization
localization = config.get("localization", "locale")
locale = localization if localization else getdefaultlocale()[0]
app.config["BABEL_DEFAULT_LOCALE"] = locale or "en_US"

babel = Babel(app)

path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "translations")
mo_path = os.path.join(path, localization or "", "LC_MESSAGES", "messages.mo")
if localization and os.path.exists(mo_path):
    language = gettext.translation("messages", path, [localization])
else:
    # No .mo for this locale (e.g. 'en' uses the built-in source strings)
    language = gettext.NullTranslations()
language.install()
_ = language.gettext

logging.info(
    "Listening on %s:%s",
    config.get("flask", "host", fallback="0.0.0.0"),
    config.getint("flask", "port", fallback=3000),
)
logging.info("Active drivers: %s", ", ".join(sorted(drivers)) or "none")

# To run with flask
if config.getboolean("application", "print_status_start"):
    if "escpos" in drivers:
        drivers["escpos"].push_task("printstatus")
flask_args = dict(
    host=config.get("flask", "host", fallback="0.0.0.0"),
    port=config.getint("flask", "port", fallback=3000),
    debug=config.getboolean("flask", "debug", fallback=False),
    use_reloader=config.getboolean("flask", "use_reloader", fallback=False),
    processes=0,
    threaded=True,
)
if config.has_option("flask", "sslcert"):
    sslcert = config.get("flask", "sslcert")
    if sslcert:
        if not config.has_option("flask", "sslkey"):
            print("If you want SSL, you must also provide the sslkey")
            sys.exit(-1)
        sslkey = config.get("flask", "sslkey")
        if not os.path.exists(sslcert):
            print("SSL cert not found at", sslcert)
            sys.exit(-1)
        if not os.path.exists(sslkey):
            print("SSL key not found at", sslkey)
            sys.exit(-1)
        flask_args["ssl_context"] = (sslcert, sslkey)
