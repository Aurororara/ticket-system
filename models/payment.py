from models.db import db

class Payment(db.Model):
  __tablename__ = 'payment'
  payment_id = db.Column(db.Integer, primary_key=True)
  pay_method = db.Column(db.String(1))
  pay_status = db.Column(db.String(1))
  amount = db.Column(db.Integer)
  paid_time = db.Column(db.DateTime)
  order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)