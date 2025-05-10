from models.db import db

class Host(db.Model):
  __tablename__ = 'host'
  host_id = db.Column(db.Integer, primary_key=True)
  host_name = db.Column(db.String(255))
  host_email = db.Column(db.String(255))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)