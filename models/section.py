from models.db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Date, func

class Section(db.Model):
  __tablename__ = 'section'
  sect_id = db.Column(db.Integer, primary_key=True)
  sect_name = db.Column(db.String(255))
  createdAt = db.Column(db.DateTime, default=func.now())
  updatedAt = db.Column(db.DateTime, default=func.now(), onupdate=func.now())