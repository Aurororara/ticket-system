
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from config import Config
from models import db
from models.host import Host
from models.location import Location
from models.section import Section
from collections import defaultdict
from models.member import Member  # Member model，記得有繼承 UserMixin
from models.location import Location
from models import Ticket, Order, Game, Show, Area, GameArea

app = Flask(__name__)
app.config.from_object(Config)

# 初始化資料庫
db.init_app(app)
# 建立資料表
with app.app_context():
  db.create_all()
  print("資料表已建立完成")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 這裡以後你會處理資料寫入資料庫
        # 現在就先讓他跳轉回首頁
        return redirect(url_for('index'))
    return render_template('register.html')

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

#退款表單
@app.route('/ticket/refund/<order_id>', methods=['GET', 'POST'])
def refund_detail(order_id):
    order = Order.query.filter_by(id=order_id).first()

    if not order:
        return "找不到此訂單", 404

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        print("✅ 收到退款申請：")
        print("姓名：", name)
        print("信箱：", email)
        print("電話：", phone)

        return "退款申請送出成功，請留意您的信箱通知。"

    return render_template("refund_form.html", order_id=order.id, order=order)


# 初始化登入管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # 如果未登入導向 login 頁面

# 載入使用者
@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))

# =======================
# 會員資料
# =======================
@app.route('/member-info')
def member_info():
    user = {
        "name": "小明",
        "phone": "0912345678",
        "birthdate": "2006-03-25",
        "disability": "無"  # 或 "有"
    }
    return render_template('member_info.html', user=user)

# =======================
# 登入登出
# =======================
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # 查找用戶
        user = Member.query.filter_by(mem_email=email).first()
        if user and check_password_hash(user.mem_pwd, password):
            login_user(user)
            return redirect(url_for('member_info'))  # 登入成功後跳轉到 member_info 頁面
        else:
            error = '電子郵件或密碼錯誤'
    
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# =======================
# 修改密碼
# =======================
@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    # 模擬目前登入的使用者資料
    user = {
        "name": "小明",
        "phone": "0912345678",
        "birthdate": "2006-03-25"  # 格式：YYYY-MM-DD
    }

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('密碼不一致，請重新輸入', 'danger')
            return render_template('change_password.html', user=user)

        # 這裡應該寫密碼更新的資料庫邏輯
        flash('密碼已成功更新！', 'success')
        return redirect(url_for('change_password'))

    return render_template('change_password.html', user=user)

# =======================
# 主頁與其他頁面
# =======================
@app.route('/show/test')
def test_detail():
    return "這是節目詳情測試頁"

# =======================
# 執行伺服器
# =======================

#我的票夾
@app.route('/my-tickets')
@login_required
def my_tickets():
    tickets = (
        db.session.query(Ticket, Game, Show, Area)
        .join(Order, Ticket.order_id == Order.order_id)
        .join(Game, Ticket.game_id == Game.game_id)
        .join(Show, Game.show_id == Show.show_id)
        .join(Area, Ticket.area_id == Area.area_id)
        .filter(Order.mem_id == current_user.id)
        .all()
    )
    return render_template('my_tickets.html', tickets=tickets)



#節目詳情頁
@app.route('/show/<int:show_id>')
def show_detail(show_id):  # 這裡改為 show_detail_by_id
    show = Show.query.get_or_404(show_id)
    host = Host.query.get(show.host_id)
    location = Location.query.get(show.location_id)

    show_data = {
        'show_name': show.show_name,
        'show_desc': show.show_desc,
        'show_pic': show.show_pic,
        'createdAt': show.createdAt,
        'host': {'host_name': host.host_name if host else "未知主辦"},
        'location': {'loc_name': location.loc_name if location else "未知地點"}
    }

    return render_template('show_detail.html', show=show_data)

@app.route('/member')
def member():
    return render_template('member.html')  # 需會員介面

@app.route('/ticket')
def ticket():
    return render_template('ticket.html')  # 需票夾頁面

if __name__ == '__main__':
    app.run(debug=True)