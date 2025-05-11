from flask_login import UserMixin
from models.db import db

class Member(UserMixin, db.Model):
    __tablename__ = 'member'
    mem_id = db.Column(db.Integer, primary_key=True)
    mem_name = db.Column(db.String(255))
    mem_acc = db.Column(db.String(255))     # 可以作為帳號
    mem_email = db.Column(db.String(255))   # 登入信箱
    mem_pwd = db.Column(db.String(255))     # 加密後密碼
    birthday = db.Column(db.Date)
    mem_phone = db.Column(db.String(20))
    createdAt = db.Column(db.Date)
    updatedAt = db.Column(db.Date)

    def get_id(self):
        return str(self.mem_id)  # Flask-Login 預設要能回傳 id