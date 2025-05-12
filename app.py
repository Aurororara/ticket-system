from flask import Flask, render_template, jsonify, request, redirect, url_for
from config import Config
from models import db
from models.show import Show
from models.host import Host
from models.game import Game
from models.location import Location
from models.area import Area
from models.section import Section
from collections import defaultdict
from models.game_area import GameArea
from models.order import Order
from models.ticket import Ticket


app = Flask(__name__)
app.config.from_object(Config)

# 初始化資料庫
db.init_app(app)
# 建立資料表
with app.app_context():
  db.create_all()
  print("資料表已建立完成")


# 模擬票券資料（你也可以接資料庫）
tickets = [
  {"id": 1, "title": "ENHYPEN 演唱會", "stock": 10},
  {"id": 2, "title": "IU 台北場", "stock": 5}
]

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/api/tickets')
def get_tickets():
  return jsonify({"tickets": tickets})

@app.route('/api/buy', methods=['POST'])
def buy_ticket():
  data = request.get_json()
  ticket_id = data.get('ticket_id')

  for ticket in tickets:
    if ticket['id'] == ticket_id and ticket['stock'] > 0:
      ticket['stock'] -= 1
      return jsonify({"message": "搶票成功！剩餘：" + str(ticket['stock'])})
  return jsonify({"message": "搶票失敗，可能已售完"}), 400

# 購票起始頁
@app.route('/ticket/<int:show_id>/start')
def view_ticket_start(show_id):
  show_result = db.session.query(Show, Host, Location)\
    .join(Host, Show.host_id == Host.host_id)\
    .join(Location, Show.location_id == Location.loc_id)\
    .filter(Show.show_id == show_id)\
    .first()
  if not show_result:
    return "節目不存在", 404
  # 取得 show 下的所有 game 資訊 (一對多)
  games = db.session.query(Game).filter(Game.show_id == show_id).all()

  # 拆解 tuple (show, host, location)
  s, host, location = show_result

  return render_template('ticket_start.html', s=s, host=host, location=location, games=games)

# 購票選擇區域
@app.route('/ticket/<int:game_id>/select-area')
def select_area(game_id):
  # 查詢場次及關聯節目資訊
  game_result = db.session.query(Game, Show, Host, Location)\
    .join(Show, Game.show_id == Show.show_id)\
    .join(Host, Show.host_id == Host.host_id)\
    .join(Location, Show.location_id == Location.loc_id)\
    .filter(Game.game_id == game_id)\
    .first()

  if not game_result:
    return "場次不存在", 404

  game, show, host, location = game_result

   # 查詢 Area 與 Section
  area_results = db.session.query(Area, Section)\
  .join(Section, Area.sect_id == Section.sect_id)\
  .filter(Area.loc_id == show.location_id)\
  .all()

  # 分群 {sect_name: [areas]}
  grouped_areas = defaultdict(list)
  for area, section in area_results:
    grouped_areas[section.sect_name].append(area)

  return render_template('select_area.html',
  show=show,
  host=host,
  location=location,
  game=game,
  grouped_areas=grouped_areas)

# 購票選擇票種
@app.route('/ticket/<int:game_id>/<int:area_id>/select-type')
def select_type(game_id, area_id):
  # 查詢場次與區域對應的 GameArea
  game_area = db.session.query(GameArea, Game, Show, Host, Location, Area)\
  .join(Game, GameArea.game_id == Game.game_id)\
  .join(Show, Game.show_id == Show.show_id)\
  .join(Host, Show.host_id == Host.host_id)\
  .join(Location, Show.location_id == Location.loc_id)\
  .join(Area, GameArea.area_id == Area.area_id)\
  .filter(GameArea.game_id == game_id, GameArea.area_id == area_id)\
  .first()

  if not game_area:
    return "查無此場次或區域", 404

  game_area_data, game, show, host, location, area = game_area
  
  # 檢查剩餘座位
  if game_area_data.available_seats <= 0: return "此區已售完" , 400
  # 傳遞資料至模板
  return render_template( 'select_type.html' ,
    game=game, show=show, host=host, location=location, area=area, available_seats=game_area_data.available_seats )

# 購票選擇票種
@app.route('/ticket/<int:game_id>/<int:area_id>/lock-order', methods = ['POST'])
def lock_order(game_id, area_id):
  full_quantity = int(request.form.get('full_ticket_quantity', 0))
  disabled_quantity = int(request.form.get('disabled_ticket_quantity', 0))
  total_quantity = full_quantity + disabled_quantity

  # 檢查票數
  game_area = db.session.query(GameArea).filter_by(game_id = game_id, area_id = area_id).first()
  if not game_area or game_area.available_seats < total_quantity:
    return "票數不足或區域無效", 400

  # 扣除可售票數
  game_area.available_seats -= total_quantity

# 查詢票價
  area = db.session.query(Area).filter_by(area_id=area_id).first()
  ticket_price = area.price if area else 0

  # 建立訂單
  new_order = Order(
    order_status='N',  # N: 未付款
    buyer_name='待填寫',
    buyer_email='待填寫',
    buyer_phone='待填寫',
    total_price= (ticket_price * full_quantity) + (2000 * disabled_quantity),
    mem_id=None,
    payment_id=None
  )
  db.session.add(new_order)
  db.session.flush()  # 取得 new_order.order_id

  # 取得該區域已用過的 seat_no
  used_seat_nos = db.session.query(Ticket.seat_no)\
    .filter_by(game_id=game_id, area_id=area_id)\
    .all()
  used_seat_nos = {seat_no for (seat_no,) in used_seat_nos}

  # 預設座位池（例：A001 ~ A1000）
  seat_pool = [f"A{i:03}" for i in range(1, game_area.total_seats + 1)]

  # 選擇尚未使用的座位
  available_seat_nos = [seat for seat in seat_pool if seat not in used_seat_nos]

  if len(available_seat_nos) < total_quantity:
    return "剩餘座位不足", 400

  # 建立 Ticket
  for i in range(total_quantity):
    seat_no = available_seat_nos[i]
    ticket = Ticket(
      seat_no=seat_no,
      ticket_status='L',
      order_id=new_order.order_id,
      game_id=game_id,
      area_id=area_id
    )
    db.session.add(ticket)

  # 提交所有變更
  db.session.commit()

  # 跳轉到選擇交易方式
  return redirect(url_for('select_payment', order_id=new_order.order_id))

# 購票付款方式
@app.route('/ticket/select-payment')
def select_payment():
  return render_template('select_payment.html')

# 購票ATM方式付款
@app.route('/ticket/select-atm')
def select_atm():
  return render_template('atm.html')

# 購票creditcard方式付款
@app.route('/ticket/select-creditcard')
def select_creditcard():
  return render_template('creditcard.html')

# 購票完成頁面
@app.route('/ticket/order-complete')
def order_complete():
  return render_template('order_complete.html')

if __name__ == '__main__':
  app.run(debug=True)
