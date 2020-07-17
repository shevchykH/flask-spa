import copy
import hashlib

import requests
from flask import render_template, flash, url_for, current_app
from werkzeug.utils import redirect
from app.config import Config


class PiastrixPaymentService(object):

    def __init__(self, data):
        self.data = data

    def pay(self):
        currency = self.data['currency']
        if currency == Config.PIASTRIX_USD:
            current_app.logger.info('Billing for payment via Pistrix currency')
            self.payment_processor = self._payment_via_piastix_currency
        elif currency == Config.PIASTRIX_EUR:
            current_app.logger.info('Billing for payment via PAY')
            self.payment_processor = self._payment_via_pay
        else:
            current_app.logger.info('Billing for payment via other currencies')
            self.payment_processor = self._payment_via_other_currency
        return self.payment_processor()

    def _payment_via_pay(self):
        data = copy.deepcopy(Config.PISTRIX_PAY_REQUEST_TEMPLATE)
        data['shop_id'] = Config.PIASTRIX_SHOP_ID
        data['amount'] = self.data['amount']
        data['currency'] = self.data['currency']
        data['shop_order_id'] = self.data['shop_order_id']
        signature = self.calculate_signature(params=data,
                                             keys_sorted=Config.PIASTRIX_PAY_SORTED_KEYS,
                                             secret=Config.PIASTRIX_SECRET_KEY)
        data['sign'] = signature
        return render_template('form.html', data=data)

    def _payment_via_piastix_currency(self):
        data = copy.deepcopy(Config.PISTRIX_BILL_REQUEST_TEMPLATE)
        data['shop_id'] = Config.PIASTRIX_SHOP_ID
        data['shop_amount'] = self.data['amount']
        data['shop_currency'] = self.data['currency']
        data['shop_order_id'] = self.data['shop_order_id']
        data['payer_currency'] = self.data['currency']
        signature = self.calculate_signature(params=data,
                                             keys_sorted=Config.PIASTRIX_BILL_SORTED_KEYS,
                                             secret=Config.PIASTRIX_SECRET_KEY)
        data['sign'] = signature
        response = {}
        try:
            response = requests.post(Config.PIASTRIX_BILL_URL, json=data).json()
            redirect_url = response['data']['url']
            return redirect(redirect_url)
        except Exception:
            msg = response.get('message', '') if response else {}
            current_app.logger.error(f'Error has been occurred during processing bill method: {msg}')
            flash('Error has been occurred during handle a request.')
            return redirect(url_for('main.main_view'))

    def _payment_via_other_currency(self):
        data = copy.deepcopy(Config.PISTRIX_INVOICE_REQUEST_TEMPLATE)
        data['amount'] = self.data['amount']
        data['currency'] = self.data['currency']
        data['shop_id'] = Config.PIASTRIX_SHOP_ID
        data['shop_order_id'] = self.data['shop_order_id']
        data['payway'] = Config.PIASTRIX_PAYWAY
        signature = self.calculate_signature(params=data,
                                             keys_sorted=Config.PIASTRIX_INVOICE_SORTED_KEYS,
                                             secret=Config.PIASTRIX_SECRET_KEY)
        data['sign'] = signature
        response = {}
        try:
            response = requests.post(Config.PIASTRIX_INVOICE_URL, json=data).json()
            response_data = response.get('data', {})
            return render_template('invoice_form.html', data=response_data)
        except Exception:
            msg = response.get('message', '') if response else {}
            current_app.logger.error(f'Error has been occurred during processing invoice method: {msg}')
            flash('Error has been occurred during handle a request.')
            return redirect(url_for('main.main_view'))


    @staticmethod
    def calculate_signature(params, keys_sorted, secret):
        key = ':'.join(str(params[i]) for i in keys_sorted)
        key += secret
        m = hashlib.sha256()
        m.update(key.encode())
        return m.hexdigest()
