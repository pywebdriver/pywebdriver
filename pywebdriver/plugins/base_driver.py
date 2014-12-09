# -*- coding: utf-8 -*-
###############################################################################
#
#   Module for OpenERP
#   Copyright (C) 2014 Akretion (http://www.akretion.com).
#   @author Sébastien BEAU <sebastien.beau@akretion.com>
#   @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#   Copyright (C) 2004-TODAY Odoo S.A (<http://odoo.com>).
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

from threading import Thread, Lock
from Queue import Queue, Empty
import traceback
import time
import logging
_logger = logging.getLogger(__name__)


class AbstractDriver(object):
    """ Abstract Driver Class"""

    def __init__(self, *args, **kwargs):
        self.status = {'status':'connecting', 'messages':[]}
        super(AbstractDriver, self).__init__(*args, **kwargs)


class ThreadDriver(Thread, AbstractDriver):

    def __init__(self, *args, **kwargs):
        Thread.__init__(self)
        AbstractDriver.__init__(self, *args, **kwargs)
        self.queue = Queue()
        self.lock  = Lock()

    def get_vendor_product(self):
        return self.vendor_product

    def lockedstart(self):
        with self.lock:
            if not self.isAlive():
                self.daemon = True
                self.start()

    def get_status(self):
        self.push_task('status')
        return self.status

    def set_status(self, status, message = None):
        if status == self.status['status']:
            if message != None and (
                    len(self.status['messages']) == 0 \
                    or message != self.status['messages'][-1]):
                self.status['messages'].append(message)
        else:
            self.status['status'] = status
            if message:
                self.status['messages'] = [message]
            else:
                self.status['messages'] = []

    def process_task(self, task, timestamp, data):
        return getattr(self, task)(data)

    def push_task(self, task, data = None):
        if not hasattr(self, task):
            raise AttributeError(
                'The method %s do not exist for the Driver' % task)
        self.lockedstart()
        self.queue.put((time.time(), task, data))

    def run(self):
        while True:
            try:
                timestamp, task, data = self.queue.get(True)
                self.process_task(task, timestamp, data)
            except Exception as e:
                self.set_status('error', str(e))
                errmsg = str(e) + '\n' + '-'*60+'\n' + traceback.format_exc()\
                         + '-'*60 + '\n'
                #TODO FIXME
                #_logger.error(errmsg)
                print errmsg


class UsbDriver(object):

    def __init__(self, port):
        self.vendor_product = None

    def get_vendor_product(self):
        return self.vendor_product
