from models.db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Date, func

class Area(db.Model):
  __tablename__ = 'Area'
  area_id = db.Column(db.Integer, primary_key=True)
  area_name = db.Column(db.String(255))
  seat_count = db.Column(db.Integer)
  price = db.Column(db.Integer)
  disabled_price = db.Column(db.Integer)
  disabled_seats = db.Column(db.Integer)    
  loc_id = db.Column(db.Integer, db.ForeignKey('Location.loc_id'))
  sect_id = db.Column(db.Integer, db.ForeignKey('Section.sect_id'))
  createdAt = db.Column(db.DateTime, default=func.now())
  updatedAt = db.Column(db.DateTime, default=func.now(), onupdate=func.now())