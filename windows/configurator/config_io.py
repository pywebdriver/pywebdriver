"""Lectura y escritura de config.ini de PyWebDriver."""

import os
from configparser import ConfigParser

from .drivers_meta import DRIVERS, driver_by_key, recommended_keys


def default_config_path(app_dir):
    return os.path.join(app_dir, "config", "config.ini")


def load_config(path):
    parser = ConfigParser()
    if os.path.isfile(path):
        parser.read(path, encoding="utf-8")
    return parser


def parser_to_dict(parser):
    return {section: dict(parser.items(section)) for section in parser.sections()}


def _split_drivers(value):
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def config_to_state(parser, locale_default="es"):
    """Convierte un ConfigParser en el state que entiende el wizard."""
    enabled = _split_drivers(parser.get("application", "drivers", fallback=""))
    if not enabled:
        enabled = recommended_keys()

    state = {
        "locale": parser.get("localization", "locale", fallback="") or locale_default,
        "flask": {
            "host": parser.get("flask", "host", fallback="127.0.0.1"),
            "port": parser.getint("flask", "port", fallback=8069),
            "cors_origins": parser.get("flask", "cors_origins", fallback="*"),
            "debug": parser.getboolean("flask", "debug", fallback=False),
            "sslcert": parser.get("flask", "sslcert", fallback=""),
            "sslkey": parser.get("flask", "sslkey", fallback=""),
        },
        "application": {
            "print_status_start": parser.getboolean(
                "application", "print_status_start", fallback=False
            ),
            "drivers": enabled,
        },
        "drivers": {},
    }

    for driver in DRIVERS:
        if not driver["section"]:
            continue
        section = driver["section"]
        values = {}
        for field in driver["fields"]:
            key = field["key"]
            default = field.get("default", "")
            if parser.has_option(section, key):
                raw = parser.get(section, key)
            else:
                raw = str(default)
            values[key] = raw
        state["drivers"][driver["key"]] = values

    return state


def state_to_config(state, base_parser=None):
    """Combina el state del wizard con un ConfigParser existente y devuelve el resultado.

    Conserva secciones desconocidas (logging, odoo, etc.) intactas.
    """
    parser = ConfigParser()
    if base_parser is not None:
        for section in base_parser.sections():
            parser.add_section(section)
            for key, value in base_parser.items(section):
                parser.set(section, key, value)

    def ensure(section):
        if not parser.has_section(section):
            parser.add_section(section)

    ensure("localization")
    parser.set("localization", "locale", state.get("locale", "") or "")

    ensure("flask")
    flask = state.get("flask", {})
    parser.set("flask", "host", str(flask.get("host", "127.0.0.1")))
    parser.set("flask", "port", str(flask.get("port", 8069)))
    parser.set("flask", "cors_origins", str(flask.get("cors_origins", "*")))
    parser.set("flask", "debug", "true" if flask.get("debug") else "false")
    if flask.get("sslcert"):
        parser.set("flask", "sslcert", str(flask["sslcert"]))
    if flask.get("sslkey"):
        parser.set("flask", "sslkey", str(flask["sslkey"]))

    ensure("application")
    app_cfg = state.get("application", {})
    parser.set(
        "application",
        "print_status_start",
        "true" if app_cfg.get("print_status_start") else "false",
    )
    parser.set("application", "drivers", ",".join(app_cfg.get("drivers", [])))

    for driver_key, values in state.get("drivers", {}).items():
        meta = driver_by_key(driver_key)
        if not meta or not meta["section"]:
            continue
        section = meta["section"]
        ensure(section)
        for field in meta["fields"]:
            key = field["key"]
            if key in values and values[key] not in (None, ""):
                parser.set(section, key, str(values[key]))

    return parser


def write_config(parser, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        parser.write(fh)


def default_state(locale="es"):
    """Devuelve un state con valores por defecto (modo silencioso)."""
    parser = ConfigParser()
    parser.add_section("application")
    parser.set("application", "drivers", ",".join(recommended_keys()))
    return config_to_state(parser, locale_default=locale)
