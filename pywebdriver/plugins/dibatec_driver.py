# -*- coding: utf-8 -*-

from pywebdriver import config, drivers
from threading import Thread


class DibatecDriver(Thread):
    
    def get_vendor_product(self):
        return "dibatec-icon"
    
    def get_status(self):
        messages = []
        messages.append("Dibatec")
        state = {
                "status": "disconnected",
            }
        return state

driver = DibatecDriver()
drivers["dibatec"] = driver 