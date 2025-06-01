from models.db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Date, func

class Game(db.Model):
  __tablename__ = 'game'
  game_id = db.Column(db.Integer, primary_key=True)
  game_date = db.Column(db.Date)
  game_time = db.Column(db.Time)
  sale_start_time = db.Column(db.DateTime)
  sale_end_time = db.Column(db.DateTime)
  game_status = db.Column(db.String(1))
  total_seats = db.Column(db.Integer)
  available_seats = db.Column(db.Integer)
  show_id = db.Column(db.Integer, db.ForeignKey('show.show_id'))
  createdAt = db.Column(db.DateTime, default=func.now())
  updatedAt = db.Column(db.DateTime, default=func.now(), onupdate=func.now())