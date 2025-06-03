from models.db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Date, func


class Order(db.Model):
  __tablename__ = 'Orders'
  order_id = db.Column(db.Integer, primary_key=True)
  order_status = db.Column(db.String(1))
  buyer_name = db.Column(db.String(255))
  buyer_email = db.Column(db.String(255))
  buyer_phone = db.Column(db.String(10))
  total_price = db.Column(db.Integer)
  mem_id = db.Column(db.Integer, db.ForeignKey('Member.mem_id'))
  createdAt = db.Column(db.DateTime, default=func.now())
  updatedAt = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

  payment = relationship('Payment', back_populates='order')
