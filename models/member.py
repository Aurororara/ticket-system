from flask_login import UserMixin
from models.db import db

class Member(UserMixin, db.Model):  # ← 加上 UserMixin
  __tablename__ = 'member'
  mem_id = db.Column(db.Integer, primary_key=True)
  mem_name = db.Column(db.String(255))
  mem_email = db.Column(db.String(255))
  mem_pwd = db.Column(db.String(255))
  birthday = db.Column(db.Date)
  mem_phone = db.Column(db.String(20))
  createdAt = db.Column(db.DateTime)
  updatedAt = db.Column(db.DateTime)

  def get_id(self):
    return str(self.mem_id)  # 這樣 Flask-Login 才知道登入的是誰
