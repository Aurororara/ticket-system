from models.db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Date, func

class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticket_id = db.Column(db.Integer, primary_key=True)
    seat_no = db.Column(db.String(4))
    ticket_status = db.Column(db.String(1))
    is_disabled = db.Column(db.Boolean, default=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'))
    area_id = db.Column(db.Integer, db.ForeignKey('area.area_id'))
    createdAt = db.Column(db.DateTime, default=func.now())
    updatedAt = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    area = db.relationship('Area', backref='tickets')