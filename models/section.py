from models.db import db

class Section(db.Model):
  __tablename__ = 'section'
  sect_id = db.Column(db.Integer, primary_key=True)
  sect_name = db.Column(db.String(255))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)