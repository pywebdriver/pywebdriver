# -*- coding: utf-8 -*-
###############################################################################
#
#   Cups driver for pywebdriver
#   Copyright (C) 2014 Akretion (http://www.akretion.com).
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

import cups
import tempfile

class CupsDriver(cups.Connection):

    def printData(self, printer, data, title='Pywebdriver', options=None):
        with tempfile.NamedTemporaryFile() as f:
            f.write(data.decode('base64'))
            f.flush()
            res = self.printFile(printer, f.name, title, options)
        return res

    def printFile(self, printer, filename, title='Pywebdriver', options=None):
        if options is None:
            options = {}
        string_options = {}
        for key, value in options.items():
            string_options[str(key)] = str(value)
        return super(CupsDriver, self).printFile(
            printer, filename, title, string_options)

    def printFiles(self, printer, filenames, title='Pywebdriver', options=None):
        if options is None:
            options = {}
        string_options = {}
        for key, value in options.items():
            string_options[str(key)] = str(value)
        return super(CupsDriver, self).printFiles(
            printer, filenames, title, string_options)

    def get_vendor_product(self):
        return 'cups-icon'

    def get_status(self):
        messages = []
        mapstate = {
            3: 'Idle',
            4: 'Printing',
            5: 'Stopped',
            }
        for printer, value in self.getPrinters().items():
            messages.append("%s : %s"
                %(printer, mapstate[value['printer-state']]
                ))
        state = {
            'status': 'connected',
            'messages': messages,
        }
        return state

