import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config(object):
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PIASTRIX_SECRET_KEY = 'SecretKey01'
    PIASTRIX_SHOP_ID = 5
    PIASTRIX_PAYWAY = 'payeer_rub'
    PIASTRIX_USD = 840
    PIASTRIX_EUR = 978
    PIASTRIX_RUP = 643

    PIASTRIX_PAY_SORTED_KEYS = ['amount', 'currency', 'shop_id', 'shop_order_id']
    PISTRIX_PAY_REQUEST_TEMPLATE = {
        'amount': None,
        'shop_currency': None,
        'shop_id': None,
        'shop_order_id': None,
        'payer_currency': None,
        'sign': None
    }

    PIASTRIX_BILL_URL = 'https://core.piastrix.com/bill/create'
    PIASTRIX_BILL_SORTED_KEYS = ['payer_currency', 'shop_amount', 'shop_currency', 'shop_id', 'shop_order_id']
    PISTRIX_BILL_REQUEST_TEMPLATE = {
        'shop_amount': None,
        'shop_currency': None,
        'shop_id': None,
        'shop_order_id': None,
        'payer_currency': None,
        'sign': None
    }

    PIASTRIX_INVOICE_URL = 'https://core.piastrix.com/invoice/create'
    PIASTRIX_INVOICE_SORTED_KEYS = ['amount', 'currency', 'payway', 'shop_id', 'shop_order_id']
    PISTRIX_INVOICE_REQUEST_TEMPLATE = {
        'shop_amount': None,
        'shop_currency': None,
        'shop_id': None,
        'shop_order_id': None,
        'payer_currency': None,
        'payway': None,
        'sign': None
    }

    LOGGER = {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
}
