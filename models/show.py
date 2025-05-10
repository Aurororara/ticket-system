from models.db import db

class Show(db.Model):
    __tablename__ = 'show'
    show_id = db.Column(db.Integer, primary_key=True)
    show_name = db.Column(db.String(255))
    show_desc = db.Column(db.Text)
    show_pic = db.Column(db.Text)
    host_id = db.Column(db.Integer, db.ForeignKey('host.host_id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.loc_id'))
    createdAt = db.Column(db.Date)
    updatedAt = db.Column(db.Date)