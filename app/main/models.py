from datetime import datetime

from app.app import db


class PaymentRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<PaymentRecord {}>'.format(self.id)
