from models.db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Date, func


class Payment(db.Model):
  __tablename__ = 'Payment'
  payment_id = db.Column(db.Integer, primary_key=True)
  pay_method = db.Column(db.String(1))
  pay_status = db.Column(db.String(1))
  amount = db.Column(db.Integer)
  paid_time = db.Column(db.DateTime)
  order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'))
  createdAt = db.Column(db.DateTime, default=func.now())
  updatedAt = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

  order = relationship('Order', back_populates='payment', uselist=False)
