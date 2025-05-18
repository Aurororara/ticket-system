from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from config import Config
from models import db
from models.host import Host
from models.location import Location
from models.section import Section
from collections import defaultdict
from models.member import Member  # Member model，記得有繼承 UserMixin
from datetime import datetime
from models.location import Location
from models.refund import Refund
from datetime import datetime
from models import Ticket, Order, Game, Show, Area, GameArea

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'nanarosearca'

# 初始化資料庫
db.init_app(app)

# 初始化登入管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
  db.create_all()
  print("資料表已建立完成")

# 註冊會員
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        birthday_str = request.form.get('birthday')

        if not birthday_str:
            flash('請填寫出生年月日', 'danger')
            return render_template('register.html')

        try:
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
        except ValueError:
            flash('日期格式錯誤，請使用YYYY-MM-DD格式', 'danger')
            return render_template('register.html')

        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('密碼不一致，請重新輸入', 'danger')
            return render_template('register.html')

        if Member.query.filter_by(mem_email=email).first():
            flash('此電子郵件已被註冊', 'danger')
            return render_template('register.html')

        hashed_pwd = generate_password_hash(password)
        new_member = Member(
            mem_name=name,
            mem_email=email,
            mem_pwd=hashed_pwd,
            mem_phone=phone,
            birthday=birthday,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        db.session.add(new_member)
        db.session.commit()
        login_user(new_member)
        flash('註冊成功，歡迎加入！', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/')
def index():
  return render_template('index.html')

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
    game_result = db.session.query(Game, Show, Host, Location)\
        .join(Show, Game.show_id == Show.show_id)\
        .join(Host, Show.host_id == Host.host_id)\
        .join(Location, Show.location_id == Location.loc_id)\
        .filter(Game.game_id == game_id).first()
    if not game_result:
        return "場次不存在", 404
    game, show, host, location = game_result
    area_results = db.session.query(Area, Section)\
        .join(Section, Area.sect_id == Section.sect_id)\
        .filter(Area.loc_id == show.location_id).all()
    grouped_areas = defaultdict(list)
    for area, section in area_results:
        grouped_areas[section.sect_name].append(area)
    return render_template('select_area.html', show=show, host=host, location=location, game=game, grouped_areas=grouped_areas)

# 購票選擇票種
@app.route('/ticket/<int:game_id>/<int:area_id>/select-type')
def select_type(game_id, area_id):
    game_area = db.session.query(GameArea, Game, Show, Host, Location, Area)\
        .join(Game, GameArea.game_id == Game.game_id)\
        .join(Show, Game.show_id == Show.show_id)\
        .join(Host, Show.host_id == Host.host_id)\
        .join(Location, Show.location_id == Location.loc_id)\
        .join(Area, GameArea.area_id == Area.area_id)\
        .filter(GameArea.game_id == game_id, GameArea.area_id == area_id).first()
    if not game_area:
        return "查無此場次或區域", 404
    game_area_data, game, show, host, location, area = game_area
    if game_area_data.available_seats <= 0:
        return "此區已售完", 400
    return render_template('select_type.html', game=game, show=show, host=host, location=location, area=area, available_seats=game_area_data.available_seats)

# 購票選擇票種
@app.route('/ticket/<int:game_id>/<int:area_id>/lock-order', methods=['POST'])
def lock_order(game_id, area_id):
    full_quantity = int(request.form.get('full_ticket_quantity', 0))
    disabled_quantity = int(request.form.get('disabled_ticket_quantity', 0))
    total_quantity = full_quantity + disabled_quantity

    game_area = db.session.query(GameArea).filter_by(game_id=game_id, area_id=area_id).first()
    if not game_area or game_area.available_seats < total_quantity:
        return "票數不足或區域無效", 400

    game_area.available_seats -= total_quantity

    area = db.session.query(Area).filter_by(area_id=area_id).first()
    ticket_price = area.price if area else 0
    new_order = Order(
        order_status='N',
        buyer_name='待填寫',
        buyer_email='待填寫',
        buyer_phone='待填寫',
        total_price=(ticket_price * full_quantity) + (2000 * disabled_quantity),
        mem_id=None,
        payment_id=None
    )
    db.session.add(new_order)
    db.session.flush()

    used_seat_nos = db.session.query(Ticket.seat_no)\
        .filter_by(game_id=game_id, area_id=area_id).all()
    used_seat_nos = {seat_no for (seat_no,) in used_seat_nos}
    seat_pool = [f"A{i:03}" for i in range(1, game_area.total_seats + 1)]
    available_seat_nos = [seat for seat in seat_pool if seat not in used_seat_nos]

    if len(available_seat_nos) < total_quantity:
        return "剩餘座位不足", 400

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

    db.session.commit()
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
@app.route('/ticket/refund/<int:order_id>', methods=['GET', 'POST'])
def refund_detail(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        abort(404, description="找不到此訂單")

    # Check if refund request already exists for this order
    existing_refund = Refund.query.filter_by(order_id=order_id).first()
    if existing_refund:
        return "此訂單已申請退款，請勿重複申請。", 400

    # 透過訂單編號查詢票券
    ticket = db.session.query(Ticket).filter_by(order_id=order_id).first()
    show = None
    location = None
    datetime_str = None
    if ticket:
        show = Show.query.get(ticket.game_id)
        location = Location.query.get(show.location_id) if show else None
        datetime_str = show.createdAt.strftime('%Y/%m/%d(%a) %H:%M') if show and show.createdAt else None

    # Check if current time is at least 1 hour before show start time
    if show and show.createdAt:
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        show_start = show.createdAt
        if now > show_start - timedelta(hours=1):
            return "退款申請必須在演出開始前一小時提出。", 400

    amount = order.total_price - 20  # 扣除20元手續費

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        if not name or not email or not phone:
            return "請填寫完整退款資訊", 400

        refund_request = Refund(
            order_id=order.order_id,
            name=name,
            email=email,
            phone=phone,
            refund_status='pending',
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        db.session.add(refund_request)
        db.session.commit()

        return "退款申請送出成功，請留意您的信箱通知。"

    return render_template("refund_form.html", order={
        'order_id': order.order_id,
        'event': show.show_name if show else '未知',
        'location': location.loc_name if location else '未知',
        'datetime': datetime_str if datetime_str else '未知',
        'amount': amount
    })

# 管理員更新退款狀態
@app.route('/admin/refund/<int:refund_id>/update', methods=['POST'])
def update_refund_status(refund_id):
    refund = Refund.query.get_or_404(refund_id)
    new_status = request.form.get('refund_status')
    if new_status not in ['pending', 'approved', 'rejected']:
        return "無效的退款狀態", 400
    refund.refund_status = new_status
    refund.updatedAt = datetime.utcnow()
    db.session.commit()
    return f"退款狀態已更新為 {new_status}"

@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))

# 登入登出
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Member.query.filter_by(mem_email=email).first()
        if user and check_password_hash(user.mem_pwd, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            error = '電子郵件或密碼錯誤'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    logout_user()
    flash("您已成功登出")
    return redirect(url_for('index'))

# 修改密碼
@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('密碼不一致，請重新輸入', 'danger')
            return render_template('change_password.html', user=current_user)

        hashed_pwd = generate_password_hash(new_password)
        current_user.mem_pwd = hashed_pwd
        current_user.updatedAt = datetime.now()
        db.session.commit()

        flash('密碼已成功更新！', 'success')
        return redirect(url_for('change_password'))

    return render_template('change_password.html', user=current_user)

# 會員資料頁
@app.route('/member')
@login_required
def member_info():
    return render_template('member_info.html', user=current_user)

# 我的票夾
@app.route('/my-tickets')
@login_required
def my_tickets():
    tickets = (
        db.session.query(Ticket, Game, Show, Area)
        .join(Order, Ticket.order_id == Order.order_id)
        .join(Game, Ticket.game_id == Game.game_id)
        .join(Show, Game.show_id == Show.show_id)
        .join(Area, Ticket.area_id == Area.area_id)
        .filter(Order.mem_id == current_user.mem_id)
        .all()
    )
    return render_template('my_ticket.html', tickets=tickets)

# 節目詳情
@app.route('/show/test')
def test_detail():
    return "這是節目詳情測試頁"

#節目詳情頁
@app.route('/show/<int:show_id>')
def show_detail(show_id):
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


# 訂單詳情頁
@app.route('/order/<int:order_id>')
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    tickets = db.session.query(Ticket, Game, Show, Area)\
        .join(Game, Ticket.game_id == Game.game_id)\
        .join(Show, Game.show_id == Show.show_id)\
        .join(Area, Ticket.area_id == Area.area_id)\
        .filter(Ticket.order_id == order_id).all()
    return render_template('order_detail.html', order=order, tickets=tickets)

# 啟動伺服器
if __name__ == '__main__':
    app.run(debug=True)
