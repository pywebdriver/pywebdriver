# Copyright (C) 2019-Today ACSONE SA/NV (https://www.acsone.eu/).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import time
from collections import OrderedDict

from .base_driver import ThreadDriver


class LimitedDict(OrderedDict):
    """A dictionary that only keeps the last few added keys
    This serves as a FIFO cache"""

    def __init__(self, size=20):
        super(LimitedDict, self).__init__()
        self._max_size = size

    def __setitem__(self, key, value):
        if len(self) == self._max_size:
            self.popitem(last=False)
        super(LimitedDict, self).__setitem__(key, value)


class PaymentTerminalDriver(ThreadDriver):
    """
    This is a base driver for payment terminals
    Properties :
        * terminals : Adds the ability to serve multiple terminals from
        one instance of the driver. It is always possible to manage the
        'classic' way as the default terminal id in that case is '0'.
        By default, this contains that default '0' terminal.
    """

    def __init__(self):
        super(PaymentTerminalDriver, self).__init__()
        self._terminals = {"0": self._get_default_terminal_values("0")}
        self._transaction_uuid = int(time.time())

    def _get_default_terminal_values(self, terminal_id):
        return {
            "terminal_id": terminal_id,
            "is_terminal": True,
            "status": "disconnected",
            "transactions": LimitedDict(),
        }

    def _get_default_transaction_values(self, transaction_id):
        return {
            "transaction_id": transaction_id,
            # transaction result
            # None: unknown, transaction in progress, most probably
            # True: transaction was successful
            # False: transaction failed
            "success": None,
            # human readable transaction status,
            # set in case success if False
            "status": None,
            # technical details related to the status (in English)
            "status_details": None,
            # acquirer reference for the successful transaction,
            # can be used later for payment file reconciliation
            "reference": None,
        }

    def _get_terminal(self, terminal_id):
        # calls must be guarded by self.lock
        if terminal_id not in self._terminals:
            self._terminals[terminal_id] = self._get_default_terminal_values(
                terminal_id
            )
        return self._terminals[terminal_id]

    def _get_transaction(self, terminal_id, transaction_id):
        # calls must be guarded by self.lock
        terminal = self._get_terminal(terminal_id)
        transactions = terminal["transactions"]
        if transaction_id not in transactions:
            transactions[transaction_id] = self._get_default_transaction_values(
                transaction_id
            )
        return transactions[transaction_id]

    def _get_last_transaction(self, terminal_id):
        # calls must be guarded by self.lock
        terminal = self._get_terminal(terminal_id)
        transactions = terminal["transactions"]
        if transactions:
            return next(reversed(transactions.values()))
        return None

    def _set_terminal_status(self, terminal_id, status):
        with self.lock:
            terminal = self._get_terminal(terminal_id)
            terminal["status"] = status

    def _make_transaction_uuid(self):
        """
        :return: int
        """
        with self.lock:
            self._transaction_uuid += 1
            return self._transaction_uuid

    def begin_transaction(self, terminal_id):
        transaction_id = self._make_transaction_uuid()
        with self.lock:
            transaction = self._get_transaction(terminal_id, transaction_id)
            return transaction

    def end_transaction(
        self,
        terminal_id,
        transaction_id,
        success,
        status=None,
        status_details=None,
        reference=None,
    ):
        """Set transaction result.

        If the transaction is not known yet, create a new transaction
        object to hold the result (typically when the terminal driver
        has been restarted and we get the last transaction result).
        If the transaction is done already (success is not None),
        do nothing.

        If transaction_id is falsy, set the result on the last created
        transaction.
        """
        with self.lock:
            if transaction_id:
                transaction = self._get_transaction(terminal_id, transaction_id)
            else:
                transaction = self._get_last_transaction(terminal_id)
            if transaction and transaction.get("success") is None:
                transaction["success"] = success
                transaction["status"] = status
                transaction["status_details"] = status_details
                transaction["reference"] = reference

    def get_status(self, terminal_id="0", **kwargs):
        """
        Return Terminal status
        """
        with self.lock:
            return self._get_terminal(terminal_id)
