from models.db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Date, func

class GameArea(db.Model):
  __tablename__ = 'RemainingTickets'
  game_area_id = db.Column(db.Integer, primary_key=True)
  available_seats = db.Column(db.Integer)
  disabled_available_seats = db.Column(db.Integer)
  game_id = db.Column(db.Integer, db.ForeignKey('Game.game_id'))
  area_id = db.Column(db.Integer, db.ForeignKey('Area.area_id'))
  createdAt = db.Column(db.DateTime, default=func.now())
  updatedAt = db.Column(db.DateTime, default=func.now(), onupdate=func.now())