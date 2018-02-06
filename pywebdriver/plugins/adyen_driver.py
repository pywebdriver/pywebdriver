# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2018 ACSONE SA/NV (https://www.acsone.eu/).
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
from ctypes import CFUNCTYPE, POINTER, c_void_p
from collections import OrderedDict
from ConfigParser import NoOptionError
import logging

import simplejson as json
from promise import Promise
from flask_cors import cross_origin
from flask import request, jsonify, render_template

from pywebdriver import app, config, drivers

from .base_driver import ThreadDriver
from .adyen_c_link import ADYPEDResultUnfinishedTender,\
                          ADYCreateTenderStatusCreated,\
                          ADYboolTrue,\
                          ADYEnvironmentTest,\
                          ADYLibraryResultOk,\
                          ADYPSPResultCodeOk,\
                          ADYPSPResultCodeRegistered,\
                          ADYPSPResultCodeAlreadyRegistered,\
                          ADYPEDResultOk,\
                          ADYTransactionTypeGoodsServices,\
                          ADYTenderOptionReceiptHandler,\
                          String,\
                          UNCHECKED,\
                          get_ped_result_code_text,\
                          get_ped_state_string,\
                          get_create_tender_status_text,\
                          get_adyen_library_result_text,\
                          init_library_allocate,\
                          init_library,\
                          register_app_allocate,\
                          register_app,\
                          register_dev_allocate,\
                          register_device,\
                          create_tender_allocate,\
                          create_tender,\
                          add_tender_option,\
                          cancel_transaction,\
                          tx_store_query_allocate,\
                          tx_store_query,\
                          tx_store_query_response,\
                          ped_device_info,\
                          register_app_response,\
                          register_device_response,\
                          create_tender_response,\
                          get_PSP_code_text,\
                          get_tender_state_text,\
                          response_header,\
                          receipts_strct,\
                          final_strct

logger = logging.getLogger(__name__)
library_logger = logging.getLogger('ADYENLIB')
logger.setLevel(logging.DEBUG)
library_logger.setLevel(logging.DEBUG)

app_log = CFUNCTYPE(c_void_p, String, String)
initialization_CB = CFUNCTYPE(c_void_p, c_void_p, c_void_p)
library_exception_CB = CFUNCTYPE(
    c_void_p, POINTER(final_strct), POINTER(ped_device_info), c_void_p)
register_pos_CB = CFUNCTYPE(c_void_p, POINTER(register_app_response), c_void_p)
register_ped_CB = CFUNCTYPE(
    c_void_p, POINTER(register_device_response), c_void_p)
ped_state_change_CB = CFUNCTYPE(
    c_void_p, c_void_p, POINTER(ped_device_info), c_void_p)
tender_additional_data_CB = CFUNCTYPE(
    c_void_p, POINTER(response_header), POINTER(ped_device_info), c_void_p)
tender_print_receipt_CB = CFUNCTYPE(
    c_void_p, POINTER(receipts_strct), POINTER(ped_device_info), c_void_p)
tender_check_signature_CB = CFUNCTYPE(
    c_void_p, POINTER(response_header), POINTER(ped_device_info), c_void_p)
ped_state_change_CB = CFUNCTYPE(
    c_void_p, c_void_p, POINTER(ped_device_info), c_void_p)
tender_finished_CB = CFUNCTYPE(
    c_void_p, POINTER(final_strct), POINTER(ped_device_info), c_void_p)
create_tender_CB = CFUNCTYPE(
    c_void_p, POINTER(create_tender_response), c_void_p)
tx_store_query_CB = CFUNCTYPE(
    UNCHECKED(None), POINTER(tx_store_query_response), POINTER(None))

def adyenresult_to_dict(res):
    return {
        'library_result_code': (res.library_result_code,
                                str(get_adyen_library_result_text(
                                    res.library_result_code))),
        'psp_result_code': (res.psp_result_code,
                            str(get_PSP_code_text(res.psp_result_code))),
        'ped_result_code': (res.ped_result_code,
                            str(get_ped_result_code_text(
                                res.ped_result_code))),
        'error_message': str(res.error_message),
    }

def finalstruct_to_dict(strct):
    return {
        'info': {
            'terminal_id': str(strct.info.terminal_id),
            'tender_reference': str(strct.info.tender_reference),
            'additional_data_obj': str(strct.info.terminal_id),
            'state': (strct.info.state, str(get_tender_state_text(strct.info.state))),
            'parsed_result': adyenresult_to_dict(strct.info.parsed_result),
        },
        'auth_code': str(strct.auth_code),
        'refusal_reason': str(strct.refusal_reason),
        'result_code': str(strct.result_code),
    }



class ValidationError(Exception):
    pass

@app_log
def app_logger(header, data):
    library_logger.info(header + data)

@library_exception_CB
def except_CB(ptr, pedstate, echo_struct):  # pylint: disable=unused-argument,invalid-name
    logger.error("Exception CB: %s, %s", ptr, pedstate)

@tender_additional_data_CB
def tender_additional_data(status_tender, ped_state, echo_struct):  # pylint: disable=unused-argument
    pass

@tender_print_receipt_CB
def tender_print_receipt(status_tender, ped_state, echo_struct):  # pylint: disable=unused-argument
    logger.info("Receipt was printed")

@tender_check_signature_CB
def tender_check_signature(status_tender, ped_state, echo_struct):  # pylint: disable=unused-argument
    logger.info("Sig was checked")

@ped_state_change_CB
def ped_state_change(pos_dev, pedstate, echo_struct):  # pylint: disable=unused-argument
    ped_state_code = pedstate.contents.device_state
    ped_state_text = get_ped_state_string(ped_state_code)
    logger.info("The device state changed: %s - %s",
                ped_state_code, ped_state_text)


class LimitedDict(OrderedDict):
    """ A dictionary that only keeps the last few added keys
        This serves as a FIFO cache """
    def __init__(self, size=20):
        super(LimitedDict, self).__init__()
        self._max_size = size

    def __setitem__(self, key, value):
        if len(self) == self._max_size:
            self.popitem(last=False)
        super(LimitedDict, self).__setitem__(key, value)


class AdyenDriver(ThreadDriver):

    def __init__(self, cfg, *a, **kw):
        super(AdyenDriver, self).__init__(*a, **kw)
        self.cfg = cfg
        self.terminal_id = None
        self.transactions_count = 0
        self.orders_mapping = LimitedDict()
        self.transactions_cache = LimitedDict()
        # only for preveting the GC from release them too soon
        self._callbacks = {}

    def get_status(self):
        status = {
            'status': 'connected' if self.terminal_id else 'disconnected',
            'transactions_count': self.transactions_count,
            'latest_transactions': self.transactions_cache,
        }
        logger.info("Status - self: %s, terminal_id: %s",
                    self, self.terminal_id)
        return status

    def get_payment_info_from_price(self, price, payment_mode):
        logger.info("Payment mode: %s", payment_mode)
        if isinstance(price, float):
            price = int(round(price * 100))
        return {
            'amount': price,
            'payment_mode': payment_mode,
            'currency_iso': 'EUR',
        }

    def run(self):
        self.init()
        super(AdyenDriver, self).run()

    def init(self):
        logger.info("Starting")
        p_mylib = init_library_allocate()
        mylib = p_mylib.contents
        mylib.library_log = app_logger
        mylib.libraryRetainsVariables = ADYboolTrue
        mylib.logArea = 0x7fff
        mylib.environment = ADYEnvironmentTest
        mylib.pos_name = String(self.cfg['pos_name'])
        mylib.app_name = String(self.cfg['app_name'])
        mylib.app_id = String(self.cfg['app_id'])
        mylib.throw_exception = except_CB
        init_promise = Promise()
        init_promise.then(self.register_myself)
        @initialization_CB
        def init_cb(result, echo_struct):
            init_promise.do_resolve(True)
        self._callbacks['init_cb'] = init_cb
        res = init_library(p_mylib, init_cb, None)
        if res != ADYLibraryResultOk:
            logger.error("The Adyen library couldn't be initiated")
            logger.error("Error code: %s", res)
            raise Exception("ERR in init: %s" % res)

    def register_myself(self, _):  # pylint: disable=unused-argument
        logger.info("Registering myself")
        mypos = register_app_allocate()
        mypos.contents.merchant_account = String(self.cfg['merchant_account'])
        mypos.contents.user_id = String(self.cfg['username'])
        mypos.contents.password = String(self.cfg['password'])
        mypos.contents.app_id = String(self.cfg['app_id'])
        pos_promise = Promise()
        pos_promise.then(self.register_terminal, lambda: "ERROR")

        @register_pos_CB
        def register_pos(result, echo_struct):  # pylint: disable=unused-argument
            try:
                self._validate_adyen_result(result.contents.parsed_result)
            except ValidationError as error:
                logger.error("Problem registering the POS application:")
                logger.error(error.message)
                return
            pos_promise.do_resolve(True)

        self._callbacks['register_pos_CB'] = register_pos
        res = register_app(mypos, register_pos, None)
        if res != ADYLibraryResultOk:
            logger.error("Couldn't register myself")
            logger.error("Error code: %s", res)
            raise Exception("ERR in Registering: %s" % res)

    def fetch_psp_reference(self, transaction_ref):
        p_query = tx_store_query_allocate()
        query = p_query.contents
        query.ped = None
        query.merchant_account = String(self.cfg['merchant_account'])
        query.terminal_id = String(self.terminal_id)
        query.tender_reference = String(transaction_ref)
        query.max_transaction = 1

        @tx_store_query_CB
        def tx_store_CB(p_response, p_unknown):  # pylint: disable=unused-argument
            response = p_response.contents
            try:
                self._validate_adyen_result(response.parsed_result)
            except ValidationError as error:
                logger.error("Problem fetching the PSP reference:")
                logger.error(error.message)
                return
            psp_reference = str(response.report.contents.psp_reference)
            amount = int(response.report.contents.amount_value)
            order_id = self.orders_mapping.get(transaction_ref)
            if not order_id:
                logger.error("Order for transaction %s not found!",
                             transaction_ref)
                return
            self.transactions_cache.setdefault(order_id, []).append({
                'reference': psp_reference,
                'amount_cents': amount
            })
        self._callbacks['tx_store_CB'] = tx_store_CB

        tx_store_query(p_query, tx_store_CB, None)

    def register_terminal(self, _):  # pylint: disable=unused-argument
        logger.info("Registering PED")

        @tender_finished_CB
        def tender_finished(p_final, pedstate, echo_struct):  # pylint: disable=unused-argument
            final_result = finalstruct_to_dict(p_final.contents)
            logger.info("The transaction finished")
            logger.info("Result: %s", final_result)
            transaction_ref = final_result['info']['tender_reference']
            self.fetch_psp_reference(transaction_ref)
        self._callbacks['tender_finished_CB'] = tender_finished

        p_myped = register_dev_allocate()
        myped = p_myped.contents
        myped.address = String(self.cfg['device_ip'])
        myped.posregister_configured_name = String("SIMULATE-PosRegister")
        myped.number_of_payment_device_options = 0
        myped.callbacks.device_state_update_CB = ped_state_change
        myped.callbacks.status_tender_final = tender_finished

        @register_ped_CB
        def register_ped(p_result, echo_struct):  # pylint: disable=unused-argument
            result = p_result.contents
            ped_result_code = result.parsed_result.ped_result_code
            result_text = get_ped_result_code_text(ped_result_code)
            logger.info("PED Register result: %s - %s",
                        ped_result_code, result_text)
            self.terminal_id = str(result.terminal_id)
            logger.info("Terminal: %s", self.terminal_id)
            logger.info("Self: %s", self)
        self._callbacks['register_ped_CB'] = register_ped

        res = register_device(p_myped, register_ped, None)
        if res != ADYLibraryResultOk:
            logger.error("Couldn't register terminal")
            logger.error("Error code: %s", res)
            raise Exception("ERR in Registering PED: %s" % res)

    def transaction_start(self, info):
        self.transactions_count += 1
        info = json.loads(info)
        order_id = info['order_id']
        if not self.terminal_id:
            logger.warn("Terminal not registered yet, can't start transaction")
            return
        logger.info("Starting transaction")
        amount = int(round(info['amount'] * 100))
        p_tender_req = create_tender_allocate()
        tender_req = p_tender_req.contents
        tender_req.merchant_account = String(self.cfg['merchant_account'])
        tender_req.terminal_id = String(self.terminal_id)
        tender_req.reference = String(order_id)
        tender_req.transaction_type = ADYTransactionTypeGoodsServices
        add_tender_option(
            tender_req.tender_options_obj, ADYTenderOptionReceiptHandler)
        tender_req.amount_currency = String(b"EUR")
        tender_req.amount_value = amount

        @create_tender_CB
        def create_tender_cb(p_response, echo_struct):
            logger.info("Transaction was created")
            response = p_response.contents
            ped_result_code = response.parsed_result.ped_result_code
            if ped_result_code == ADYPEDResultUnfinishedTender:
                # unfinished transaction
                cancel_transaction(
                    response.terminal_id, response.tender_reference)
            elif response.create_tender_status != ADYCreateTenderStatusCreated:
                logger.error(
                    "Error creating transaction: %s - %s",
                    response.create_tender_status,
                    get_create_tender_status_text(
                        response.create_tender_status))
            else:
                logger.info(
                    "Transaction created! Ref: %s", response.tender_reference)
                self.orders_mapping[str(response.tender_reference)] = order_id
        self._callbacks['create_tender_cb'] = create_tender_cb
        create_tender(p_tender_req, create_tender_cb, None)

    def _validate_adyen_result(self, result):
        all_ok = (result.library_result_code == ADYLibraryResultOk and
                  result.psp_result_code in (
                      ADYPSPResultCodeOk,
                      ADYPSPResultCodeRegistered,
                      ADYPSPResultCodeAlreadyRegistered) and
                  result.ped_result_code == ADYPEDResultOk)
        if not all_ok:
            raise ValidationError("library_result_code: %s"
                                  "psp_result_code: %s"
                                  "ped_result_code: %s"
                                  "Error message: %s" % (
                                      result.library_result_code,
                                      result.psp_result_code,
                                      result.ped_result_code,
                                      result.error_message))


def load_driver_config():
    driver_config = {}
    for key in ('pos_name', 'app_name', 'app_id', 'username', 'password',
                'merchant_account', 'device_ip'):
        try:
            driver_config[key] = config.get('adyen_driver', key)
        except NoOptionError:
            raise Exception("Missing configuration for adyen driver: %s" % key)
    return driver_config

adyen_driver = AdyenDriver(load_driver_config())
drivers['adyen'] = adyen_driver
adyen_driver.start()


@app.route(
    '/hw_proxy/payment_terminal_transaction_start',
    methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def payment_terminal_transaction_start():
    app.logger.debug('Adyen: Call payment_terminal_transaction_start')
    payment_info = request.json['params']['payment_info']
    app.logger.debug('Adyen: payment_info=%s', payment_info)
    adyen_driver.push_task('transaction_start', payment_info)
    return jsonify(jsonrpc='2.0', result=True)


@app.route('/adyen_status.html', methods=['POST'])
@cross_origin()
def adyen_status():
    info = adyen_driver.get_payment_info_from_price(
        float(request.values['price']),
        request.values['payment_mode'])
    app.logger.debug('Telium status info=%s', info)
    adyen_driver.push_task('transaction_start', json.dumps(
        info, sort_keys=True))
    return render_template('adyen_status.html')
