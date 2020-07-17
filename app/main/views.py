from flask import Blueprint, render_template, current_app
from app.main.forms import PaymentForm
from app.main.models import db, PaymentRecord
from app.billing.api import PiastrixPaymentService

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/', methods=['GET', 'POST'])
def main_view():
    current_app.logger.info('Processing payment request')
    form = PaymentForm()
    if form.validate_on_submit():
        currency = int(form.currency.data)
        payment_amount = form.payment_amount.data
        description = form.product_description.data
        payment = PaymentRecord(amount=payment_amount, currency=currency, description=description)
        db.session.add(payment)
        db.session.commit()
        data = {'currency': currency, 'amount': payment_amount, 'desctiption': description, 'shop_order_id': payment.id}
        billing_service = PiastrixPaymentService(data=data)
        return billing_service.pay()
    return render_template('index.html', title='Payment', form=form)
