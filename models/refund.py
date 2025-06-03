from models.db import db
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Date, func


class Refund(db.Model):
    __tablename__ = 'Refund'
    refund_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    refund_status = db.Column(db.String(20), default='pending')  # e.g., pending, approved, rejected
    createdAt = db.Column(db.DateTime, default=func.now())
    updatedAt = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    order = db.relationship('Order', backref=db.backref('refunds', lazy=True))
