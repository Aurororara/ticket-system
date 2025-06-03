from models.db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Date, func

class Location(db.Model):
  __tablename__ = 'Location'
  loc_id = db.Column(db.Integer, primary_key=True)
  loc_name = db.Column(db.String(255))
  createdAt = db.Column(db.DateTime, default=func.now())
  updatedAt = db.Column(db.DateTime, default=func.now(), onupdate=func.now())