from models.db import db

class Member(db.Model):
  __tablename__ = 'member'
  mem_id = db.Column(db.Integer, primary_key=True)
  mem_name = db.Column(db.String(255))
  mem_acc = db.Column(db.String(255))
  mem_email = db.Column(db.String(255))
  mem_pwd = db.Column(db.String(255))
  birthday = db.Column(db.Date)
  mem_phone = db.Column(db.String(20))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)