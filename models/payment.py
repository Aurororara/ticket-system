from models.db import db
from sqlalchemy.orm import relationship

class Payment(db.Model):
  __tablename__ = 'payment'
  payment_id = db.Column(db.Integer, primary_key=True)
  pay_method = db.Column(db.String(1))
  pay_status = db.Column(db.String(1))
  amount = db.Column(db.Integer)
  paid_time = db.Column(db.DateTime)
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)

  order = relationship('Order', back_populates='payment', uselist=False)
