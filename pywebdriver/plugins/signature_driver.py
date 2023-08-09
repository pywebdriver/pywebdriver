# Copyright (C) 2015-Today Akretion (http://www.akretion.com).
# @author Sylvain Calador <sylvain.calador@akretion.com>
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

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
