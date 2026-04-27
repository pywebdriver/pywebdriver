"""Entry point del configurador grafico de PyWebDriver.

Modo interactivo (default):
    pywebdriver-configurator.exe

Modo silencioso (escribe config con defaults sin abrir GUI, util para /SILENT):
    pywebdriver-configurator.exe --silent
    pywebdriver-configurator.exe --silent --install-service --generate-ssl
"""

import argparse
import os
import sys

from . import config_io, service, ssl_setup
from .api import Api


def app_dir():
    """Directorio donde esta instalado PyWebDriver.

    En produccion (PyInstaller COLLECT) es la carpeta que contiene el .exe.
    En desarrollo se puede sobreescribir con env var PYWEBDRIVER_HOME.
    """
    override = os.environ.get("PYWEBDRIVER_HOME")
    if override:
        return override
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def web_dir():
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        return os.path.join(base, "configurator_web")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


def run_silent(args, app_path):
    config_path = config_io.default_config_path(app_path)
    base_parser = config_io.load_config(config_path)
    state = config_io.config_to_state(base_parser, locale_default=args.locale)

    if args.generate_ssl:
        try:
            cert, key = ssl_setup.generate(app_path)
            state["flask"]["sslcert"] = cert
            state["flask"]["sslkey"] = key
        except Exception as exc:
            print("SSL generation failed:", exc, file=sys.stderr)

    parser = config_io.state_to_config(state, base_parser=base_parser)
    config_io.write_config(parser, config_path)
    print("Wrote config to:", config_path)

    if args.install_service:
        try:
            service.install(app_path, autostart=not args.no_autostart)
            print("Service installed and started.")
        except Exception as exc:
            print("Service install failed:", exc, file=sys.stderr)
            return 1
    return 0


def run_uninstall(args, app_path):
    """Ejecutado por InnoSetup [UninstallRun]. Reemplaza al uninstall.bat."""
    try:
        service.remove(app_path)
        print("Service removed.")
    except Exception as exc:
        print("Service remove failed:", exc, file=sys.stderr)
    if args.remove_ssl:
        try:
            ssl_setup.uninstall_root_ca(app_path)
            print("mkcert root CA removed from trust store.")
        except Exception as exc:
            print("mkcert -uninstall failed:", exc, file=sys.stderr)
    return 0


def run_gui(app_path):
    try:
        import webview
    except ImportError:
        print(
            "pywebview no esta instalado. Ejecutar: pip install pywebview",
            file=sys.stderr,
        )
        return 2

    index_path = os.path.join(web_dir(), "index.html")
    if not os.path.exists(index_path):
        print(f"No se encontro la UI del configurador en {index_path}", file=sys.stderr)
        return 3

    finished = {"flag": False}

    def on_finish():
        finished["flag"] = True
        for window in webview.windows:
            window.destroy()

    api = Api(app_path, on_finish=on_finish)

    webview.create_window(
        title="PyWebDriver",
        url=index_path,
        js_api=api,
        width=900,
        height=640,
        min_size=(780, 540),
    )
    webview.start()
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="PyWebDriver configurator")
    parser.add_argument("--silent", action="store_true",
                        help="Run without GUI (write defaults and optionally install service)")
    parser.add_argument("--locale", default="es", help="Locale for silent mode (es/en)")
    parser.add_argument("--install-service", action="store_true",
                        help="Install Windows service in silent mode")
    parser.add_argument("--no-autostart", action="store_true",
                        help="Do not autostart service when installing")
    parser.add_argument("--generate-ssl", action="store_true",
                        help="Generate SSL certificates with mkcert in silent mode")
    parser.add_argument("--uninstall", action="store_true",
                        help="Remove the Windows service (used by InnoSetup uninstaller)")
    parser.add_argument("--remove-ssl", action="store_true",
                        help="With --uninstall: also remove mkcert root CA from trust store")
    args = parser.parse_args(argv)

    app_path = app_dir()

    if args.uninstall:
        return run_uninstall(args, app_path)
    if args.silent:
        return run_silent(args, app_path)
    return run_gui(app_path)


if __name__ == "__main__":
    sys.exit(main())
