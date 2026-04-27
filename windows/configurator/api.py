"""API expuesta a JavaScript a traves de pywebview.

Cada metodo publico de Api se invoca como `window.pywebview.api.<metodo>()` desde JS.
Las respuestas siguen siempre la forma {ok: bool, data?: ..., error?: str}.
"""

import os
import sys
import traceback

from . import config_io, hardware, service, ssl_setup
from .drivers_meta import DRIVERS, windows_drivers


def _ok(data=None):
    return {"ok": True, "data": data}


def _err(message):
    return {"ok": False, "error": str(message)}


def _safe(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            traceback.print_exc()
            return _err(exc)

    wrapper.__name__ = fn.__name__
    return wrapper


class Api:
    def __init__(self, app_dir, on_finish=None):
        self.app_dir = app_dir
        self.on_finish = on_finish
        self.config_path = config_io.default_config_path(app_dir)

    @_safe
    def get_bootstrap(self):
        parser = config_io.load_config(self.config_path)
        state = config_io.config_to_state(parser)
        cert, key = ssl_setup.existing(self.app_dir)
        return _ok(
            {
                "drivers_meta": windows_drivers(),
                "state": state,
                "service_status": service.status(self.app_dir),
                "ssl": {"cert": cert, "key": key},
                "app_dir": self.app_dir,
                "platform": sys.platform,
            }
        )

    @_safe
    def detect_hardware(self):
        return _ok(hardware.detect_all())

    @_safe
    def generate_ssl(self):
        cert, key = ssl_setup.generate(self.app_dir)
        return _ok({"cert": cert, "key": key})

    @_safe
    def save_config(self, state):
        base_parser = config_io.load_config(self.config_path)
        parser = config_io.state_to_config(state, base_parser=base_parser)
        config_io.write_config(parser, self.config_path)
        return _ok({"path": self.config_path})

    @_safe
    def install_service(self, autostart=True):
        service.install(self.app_dir, autostart=autostart)
        return _ok({"status": service.status(self.app_dir)})

    @_safe
    def start_service(self):
        service.start(self.app_dir)
        return _ok({"status": service.status(self.app_dir)})

    @_safe
    def stop_service(self):
        service.stop(self.app_dir)
        return _ok({"status": service.status(self.app_dir)})

    @_safe
    def restart_service(self):
        service.restart(self.app_dir)
        return _ok({"status": service.status(self.app_dir)})

    @_safe
    def remove_service(self):
        service.remove(self.app_dir)
        return _ok({"status": service.status(self.app_dir)})

    @_safe
    def service_status(self):
        return _ok({"status": service.status(self.app_dir)})

    @_safe
    def apply_all(self, state, options):
        """Operacion atomica para el ultimo paso del wizard.

        options = {generate_ssl, install_service, autostart}
        """
        result = {"steps": []}
        options = options or {}

        if options.get("generate_ssl"):
            cert, key = ssl_setup.generate(self.app_dir)
            state.setdefault("flask", {})["sslcert"] = cert
            state["flask"]["sslkey"] = key
            result["steps"].append({"name": "ssl", "ok": True})

        base_parser = config_io.load_config(self.config_path)
        parser = config_io.state_to_config(state, base_parser=base_parser)
        config_io.write_config(parser, self.config_path)
        result["steps"].append({"name": "config", "ok": True, "path": self.config_path})

        if options.get("install_service"):
            try:
                service.install(self.app_dir, autostart=options.get("autostart", True))
                result["steps"].append(
                    {"name": "service", "ok": True, "status": service.status(self.app_dir)}
                )
            except Exception as exc:
                result["steps"].append({"name": "service", "ok": False, "error": str(exc)})

        result["finished"] = True
        if self.on_finish:
            self.on_finish()
        return _ok(result)

    @_safe
    def quit(self):
        if self.on_finish:
            self.on_finish()
        return _ok()

    @_safe
    def open_logs_folder(self):
        if sys.platform == "win32":
            os.startfile(self.app_dir)
            return _ok()
        return _err("Only available on Windows")
