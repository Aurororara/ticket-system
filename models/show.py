from models.db import db
from sqlalchemy import Date, func
from flask_sqlalchemy import SQLAlchemy


class Show(db.Model):
    __tablename__ = 'Show'
    show_id = db.Column(db.Integer, primary_key=True)
    show_name = db.Column(db.String(255))
    show_desc = db.Column(db.Text)
    show_pic = db.Column(db.Text)
    start_date = db.Column(Date)
    end_date = db.Column(Date)
    host_id = db.Column(db.Integer, db.ForeignKey('Host.host_id'))
    location_id = db.Column(db.Integer, db.ForeignKey('Location.loc_id'))
    createdAt = db.Column(db.DateTime, default=func.now())
    updatedAt = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<Show {self.show_name}>'