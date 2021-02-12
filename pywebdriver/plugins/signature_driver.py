###############################################################################
#
#   Copyright (C) 2015 Akretion (http://www.akretion.com).
#   @author Sylvain Calador <sylvain.calador@akretion.com>
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

import os

from flask import jsonify

try:
    import pymtp
except ImportError:
    pass


from pywebdriver import app, config


@app.route("/hw_proxy/get_signature", methods=["GET"])
def get_signature_http():

    file_ = None
    data = None

    download_path = config.get("signature_driver", "download_path") or "/tmp"
    signature_file = config.get("signature_driver", "signature_file") or "signature.svg"

    try:
        mtp = pymtp.MTP()
        mtp.connect()
    except Exception as err:
        app.logger.error("Unable to connect device %s" % str(err))
        return jsonify(jsonrpc="2.0", result=data)

    for f in mtp.get_filelisting():
        if f.filename == signature_file:
            file_ = f
            break
    if file_:
        dest_file = os.path.join(download_path, signature_file)
        try:
            mtp.get_file_to_file(file_.item_id, dest_file)
            app.logger.debug("file downloaded to %s" % dest_file)
            with open(dest_file, "r") as f:
                data = f.read()
            app.logger.debug(data)
            mtp.delete_object(file_.item_id)
        except Exception as err:
            app.logger.error("error during file transfer %s" % str(err))
    else:
        app.logger.error("file not found on the device: %s" % signature_file)

    mtp.disconnect()
    return jsonify(jsonrpc="2.0", result=data)
