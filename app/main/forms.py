from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

from app.config import Config


class PaymentForm(FlaskForm):
    USD = Config.PIASTRIX_USD
    EUR = Config.PIASTRIX_EUR
    RUP = Config.PIASTRIX_RUP
    CURRENCY = [
        (USD, 'USD'),
        (EUR, 'EUR'),
        (RUP, 'RUP'),
    ]
    payment_amount = FloatField('PaymentRecord amount', validators=[DataRequired(), NumberRange(min=0)])
    currency = SelectField('Currency', choices=CURRENCY, validate_choice=False)
    product_description = TextAreaField('Product description', validators=[DataRequired()])
    submit = SubmitField('Pay')
