import sys

import servicemanager
import win32serviceutil

from pywebdriver import app, config, flask_args


def run_flask():
    app.run(**flask_args)


def stop_flask():
    import requests

    protocol = "https" if config.has_option("flask", "sslkey") else "http"
    url = f"{protocol}://{config.get('flask', 'host')}:{config.get('flask', 'port')}/shutdown"
    return requests.get(url, verify=False)


class PywebdriverService(win32serviceutil.ServiceFramework):
    _svc_name_ = "Pywebdriver"
    _svc_display_name_ = "PyWebDriver"
    _svc_description_ = "Python Web Driver"

    def SvcStop(self):
        stop_flask()

    def SvcDoRun(self):
        run_flask()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PywebdriverService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PywebdriverService)
