from models.db import db
from sqlalchemy.orm import relationship

class Order(db.Model):
  __tablename__ = 'order'
  order_id = db.Column(db.Integer, primary_key=True)
  order_status = db.Column(db.String(1))
  buyer_name = db.Column(db.String(255))
  buyer_email = db.Column(db.String(255))
  buyer_phone = db.Column(db.String(20))
  total_price = db.Column(db.Integer)
  mem_id = db.Column(db.Integer, db.ForeignKey('member.mem_id'))
  payment_id = db.Column(db.Integer, db.ForeignKey('payment.payment_id'))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)

  payment = relationship('Payment', back_populates='order')
