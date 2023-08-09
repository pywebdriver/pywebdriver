# Copyright (C) 2014-Today Akretion (http://www.akretion.com).
# Copyright (C) 2015-Today: GRAP (http://www.grap.coop)
# Copyright (C) 2004-Today: Odoo S.A (<http://odoo.com>).
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import time
import traceback
from queue import Queue
from threading import Lock, Thread

from flask import jsonify

from pywebdriver import app


def check(installed, plugin):
    def wrap(func):
        def wrapped_func(*args, **kwargs):
            if installed:
                return func(*args, **kwargs)
            else:
                app.logger.warning(
                    "The plugin %s can not be loaded as one of its dependency "
                    "is missing. You can install them using pip or debian\n"
                    "The pip package are : %s \n"
                    "The debian package are : %s \n"
                    "More information here : "
                    "https://github.com/akretion/pywebdriver\n"
                    "Return False to the API Call"
                    % (plugin["name"], plugin["require_pip"], plugin["require_debian"])
                )
                return jsonify(jsonrpc="2.0", result=False)

        return wrapped_func

    return wrap


class AbstractDriver(object):
    """Abstract Driver Class"""

    def __init__(self, *args, **kwargs):
        self.status = {"status": "disconnected", "messages": []}


class ThreadDriver(Thread, AbstractDriver):
    def __init__(self, *args, **kwargs):
        Thread.__init__(self)
        AbstractDriver.__init__(self, *args, **kwargs)
        self.queue = Queue()
        self.lock = Lock()
        self.vendor_product = None

    def get_vendor_product(self):
        return self.vendor_product

    def lockedstart(self):
        with self.lock:
            if not self.is_alive():
                self.daemon = True
                self.start()

    def set_status(self, status, message=None):
        if status == self.status["status"]:
            if message is not None and (
                len(self.status["messages"]) == 0
                or message != self.status["messages"][-1]
            ):
                self.status["messages"].append(message)
        else:
            self.status["status"] = status
            if message:
                self.status["messages"] = [message]
            else:
                self.status["messages"] = []

    def process_task(self, task, timestamp, data):
        return getattr(self, task)(data)

    def push_task(self, task, data=None):
        if not hasattr(self, task):
            raise AttributeError("The method %s do not exist for the Driver" % task)
        self.lockedstart()
        self.queue.put((time.time(), task, data))

    def run(self):
        while True:
            try:
                timestamp, task, data = self.queue.get(True)
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
