from models.db import db

class GameArea(db.Model):
  __tablename__ = 'game_area'
  game_area_id = db.Column(db.Integer, primary_key=True)
  total_seats = db.Column(db.Integer)
  available_seats = db.Column(db.Integer)
  game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'))
  area_id = db.Column(db.Integer, db.ForeignKey('area.area_id'))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)