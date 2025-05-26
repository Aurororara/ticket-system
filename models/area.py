from models.db import db

class Area(db.Model):
  __tablename__ = 'area'
  area_id = db.Column(db.Integer, primary_key=True)
  area_name = db.Column(db.String(255))
  seat_count = db.Column(db.Integer)
  price = db.Column(db.Integer)
  disabled_price = db.Column(db.Integer)
  disabled_seats = db.Column(db.Integer)    
  loc_id = db.Column(db.Integer, db.ForeignKey('location.loc_id'))
  sect_id = db.Column(db.Integer, db.ForeignKey('section.sect_id'))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)