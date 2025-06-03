from flask_login import UserMixin
from models.db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Date, func

class Member(UserMixin, db.Model):  # ← 加上 UserMixin
  __tablename__ = 'Member'
  mem_id = db.Column(db.Integer, primary_key=True)
  mem_name = db.Column(db.String(255))
  mem_email = db.Column(db.String(255))
  mem_pwd = db.Column(db.String(255))
  birthday = db.Column(db.Date)
  mem_phone = db.Column(db.String(10))
  createdAt = db.Column(db.DateTime, default=func.now())
  updatedAt = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

  def get_id(self):
    return str(self.mem_id)  # 這樣 Flask-Login 才知道登入的是誰
