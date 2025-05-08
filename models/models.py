from models import db

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

class Host(db.Model):
  __tablename__ = 'host'
  host_id = db.Column(db.Integer, primary_key=True)
  host_name = db.Column(db.String(255))
  host_email = db.Column(db.String(255))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)

class Location(db.Model):
  __tablename__ = 'location'
  loc_id = db.Column(db.Integer, primary_key=True)
  loc_name = db.Column(db.String(255))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)

class Game(db.Model):
  __tablename__ = 'game'
  game_id = db.Column(db.Integer, primary_key=True)
  game_date = db.Column(db.Date)
  game_time = db.Column(db.Time)
  sale_start_time = db.Column(db.DateTime)
  sale_end_time = db.Column(db.DateTime)
  game_status = db.Column(db.String(1))
  total_seats = db.Column(db.Integer)
  available_seats = db.Column(db.Integer)
  show_id = db.Column(db.Integer, db.ForeignKey('show.show_id'))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)

class Area(db.Model):
  __tablename__ = 'area'
  area_id = db.Column(db.Integer, primary_key=True)
  area_name = db.Column(db.String(255))
  seat_count = db.Column(db.Integer)
  price = db.Column(db.Integer)
  loc_id = db.Column(db.Integer, db.ForeignKey('location.loc_id'))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)

class GameArea(db.Model):
  __tablename__ = 'game_area'
  game_area_id = db.Column(db.Integer, primary_key=True)
  total_seats = db.Column(db.Integer)
  available_seats = db.Column(db.Integer)
  game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'))
  area_id = db.Column(db.Integer, db.ForeignKey('area.area_id'))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)

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

class Order(db.Model):
  __tablename__ = 'order'
  order_id = db.Column(db.Integer, primary_key=True)
  order_status = db.Column(db.String(1))
  buyer_name = db.Column(db.String(255))
  buyer_email = db.Column(db.String(255))
  buyer_phone = db.Column(db.String(20))
  total_price = db.Column(db.Integer)
  mem_id = db.Column(db.Integer, db.ForeignKey('member.mem_id'))
  payment_id = db.Column(db.Integer, db.ForeignKey('payment.payment_id'))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)

class Ticket(db.Model):
  __tablename__ = 'ticket'
  ticket_id = db.Column(db.Integer, primary_key=True)
  seat_no = db.Column(db.String(4))
  ticket_status = db.Column(db.String(1))
  order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
  game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'))
  area_id = db.Column(db.Integer, db.ForeignKey('area.area_id'))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)

class Payment(db.Model):
  __tablename__ = 'payment'
  payment_id = db.Column(db.Integer, primary_key=True)
  pay_method = db.Column(db.String(1))
  pay_status = db.Column(db.String(1))
  amount = db.Column(db.Integer)
  paid_time = db.Column(db.DateTime)
  order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
  createdAt = db.Column(db.Date)
  updatedAt = db.Column(db.Date)
