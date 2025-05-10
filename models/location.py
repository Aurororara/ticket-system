from models.db import db

class Location(db.Model):
  __tablename__ = 'location'
  loc_id = db.Column(db.Integer, primary_key=True)
  loc_name = db.Column(db.String(255))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)