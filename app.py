# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, get_flashed_messages
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from config import Config
from models import db
from models.host import Host
from models.location import Location
from models.section import Section
from collections import defaultdict
from models.member import Member  # Member model，記得有繼承 UserMixin
from models.location import Location
from models.refund import Refund
from models import Ticket, Order, Game, Show, Area, GameArea, Payment
from datetime import datetime, timedelta, date
from markupsafe import Markup
from models.game import Game
from flask_migrate import Migrate
import re

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'nanarosearca'

# 初始化資料庫
db.init_app(app)

# ✅ 正確順序：app 建立好後，再傳給 Migrate
migrate = Migrate(app, db)

# 初始化登入管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
  db.create_all()
  print("資料表已建立完成")
with app.app_context():
    from models.show import Show
    print("✅ Shows in DB:")
    #for show in Show.query.all():
        #print(show.show_name)


# 註冊會員

@app.route('/register', methods=['GET', 'POST'])
def register():
    def validate_password(password):
        # 至少8碼，包含至少一個大寫與一個小寫字母
        # 密碼至少8碼，包含至少一個大寫與一個小寫字母
        pattern = r'^(?=.*[a-z])(?=.*[A-Z]).{8,}$'
        return re.match(pattern, password)

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

        # 密碼格式驗證
        if not validate_password(password):
            flash('密碼必須至少8碼且包含大小寫字母', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('密碼不一致，請重新輸入', 'danger')
            return render_template('register.html')

        # 檢查電子郵件是否已註冊
        if Member.query.filter_by(mem_email=email).first():
            flash('此電子郵件已被註冊', 'danger')
            return render_template('register.html')

        # 密碼雜湊
        hashed_pwd = generate_password_hash(password)

        # 建立新會員
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

#搜尋節目
@app.route('/search')
def search():
    keyword = request.args.get('keyword', '')
    # 範例：搜尋節目
    shows = Show.query.filter(Show.show_name.contains(keyword)).all() if keyword else []
    return render_template('search_result.html', keyword=keyword, shows=shows)


#只能註冊一次
@app.route('/check_exist')
def check_exist():
    email = request.args.get('email')
    phone = request.args.get('phone')
    exists = False

    if email:
        exists = db.session.query(Member.mem_id).filter_by(mem_email=email).first() is not None
    elif phone:
        exists = db.session.query(Member.mem_id).filter_by(mem_phone=phone).first() is not None

    return jsonify({'exists': exists})


# =======================
# 登入管理初始化
# =======================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))

# =======================
# 登入
# =======================


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    # 取得所有 flashed 訊息並翻譯
    messages = get_flashed_messages()
    translated_messages = []
    for msg in messages:
        if msg == "Please log in to access this page.":
            translated_messages.append("請先登入以瀏覽此頁面")
        else:
            translated_messages.append(msg)

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Member.query.filter_by(mem_email=email).first()
        if user and check_password_hash(user.mem_pwd, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            error = '電子郵件或密碼錯誤'

    return render_template('login.html', error=error, messages=translated_messages)



@app.route('/logout')
def logout():
    logout_user()
    flash("您已成功登出")
    return redirect(url_for('index'))


# =======================
# 修改密碼
# =======================
from werkzeug.security import check_password_hash

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if not check_password_hash(current_user.mem_pwd, old_password):
            flash('舊密碼錯誤', 'danger')
            return render_template('change_password.html', user=current_user)

        if new_password != confirm_password:
            flash('密碼不一致，請重新輸入', 'danger')
            return render_template('change_password.html', user=current_user)

        current_user.mem_pwd = generate_password_hash(new_password)
        current_user.updatedAt = datetime.now()
        db.session.commit()

        flash('密碼已成功更新，請重新登入', 'success')
        
        # 強制登出
        logout_user()
        return redirect(url_for('login'))  # 登出後導向登入頁面

    return render_template('change_password.html', user=current_user)




# =======================
# 會員資料頁
# =======================
@app.route('/member')
@login_required
def member_info():
    return render_template('member_info.html', user=current_user)

# =======================
# 首頁
# =======================
@app.route('/')
def index():
    # 取得前端送出的篩選參數
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    sort_by = request.args.get('sort_by', 'start_date')  # 預設排序依 start_date

    query = Show.query

    # 日期範圍篩選
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            query = query.filter(Show.start_date >= start_date)
        except ValueError:
            pass

    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            query = query.filter(Show.start_date <= end_date)
        except ValueError:
            pass

    # 排序
    if sort_by == 'start_date':
        query = query.order_by(Show.start_date.asc())
    elif sort_by == 'ticket_start_date':
        # 假設你有 ticket_start_date 欄位，若無則先不用這段
        query = query.order_by(Show.ticket_start_date.asc())
    else:
        query = query.order_by(Show.start_date.asc())  # 預設

    all_shows = query.all()

    # 近期節目（輪播），不受篩選影響，還是依開始日期取前6筆
    carousel_shows = Show.query.order_by(Show.start_date.asc()).limit(6).all()

    return render_template('index.html',
                           carousel_shows=carousel_shows,
                           shows=all_shows)

@app.route('/api/buy', methods=['POST'])
def buy_ticket():
  data = request.get_json()
  ticket_id = data.get('ticket_id')

  for ticket in tickets:
    if ticket['id'] == ticket_id and ticket['stock'] > 0:
      ticket['stock'] -= 1
      return jsonify({"message": "搶票成功！剩餘：" + str(ticket['stock'])})
  return jsonify({"message": "搶票失敗，可能已售完"}), 400

# # 購票起始頁
# @app.route('/ticket/<int:show_id>/start')
# def view_ticket_start(show_id):
#   show_result = db.session.query(Show, Host, Location)\
#     .join(Host, Show.host_id == Host.host_id)\
#     .join(Location, Show.location_id == Location.loc_id)\
#     .filter(Show.show_id == show_id)\
#     .first()
#   if not show_result:
#     return "節目不存在", 404
#   # 取得 show 下的所有 game 資訊 (一對多)
#   games = db.session.query(Game).filter(Game.show_id == show_id).all()

#   # 拆解 tuple (show, host, location)
#   s, host, location = show_result

#   return render_template('ticket_start.html', s=s, host=host, location=location, games=games,now=datetime.now())

# 購票選擇區域
@app.route('/ticket/<int:game_id>/select-area')
@login_required
def select_area(game_id):
    game_result = db.session.query(Game, Show, Host, Location)\
        .join(Show, Game.show_id == Show.show_id)\
        .join(Host, Show.host_id == Host.host_id)\
        .join(Location, Show.location_id == Location.loc_id)\
        .filter(Game.game_id == game_id).first()
    if not game_result:
        return "場次不存在", 404
    
    # 解構查詢結果
    game, show, host, location = game_result
    # 查詢所有該場地的區域與其區段
    area_results = db.session.query(Area, Section, GameArea)\
        .join(Section, Area.sect_id == Section.sect_id)\
        .join(GameArea, Area.area_id == GameArea.area_id)\
        .filter(GameArea.game_id == game_id).all()
    
    # 對應 area_id → GameArea
    grouped_areas = defaultdict(list)
    for area, section, game_area in area_results:
        grouped_areas[section.sect_name].append({
            'area': area,
            'available': game_area.available_seats,
            'disabled': game_area.disabled_available_seats
        })
    return render_template('select_area.html', show=show, host=host, location=location, game=game, grouped_areas=grouped_areas)

# 購票選擇票種
@app.route('/ticket/<int:game_id>/<int:area_id>/select-type')
@login_required
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
    if game_area_data.available_seats <= 0 and game_area_data.disabled_available_seats <= 0:
        return "此區已售完", 400
    return render_template('select_type.html', game=game, show=show, host=host, location=location, area=area, available_seats=game_area_data.available_seats,disabled_available_seats=game_area_data.disabled_available_seats)

# 鎖定訂單
@app.route('/ticket/<int:game_id>/<int:area_id>/lock-order', methods=['POST'])
@login_required
def lock_order(game_id, area_id):
    full_quantity = int(request.form.get('full_ticket_quantity', 0))
    disabled_quantity = int(request.form.get('disabled_ticket_quantity', 0))
    total_quantity = full_quantity + disabled_quantity

    game_area = db.session.query(GameArea).filter_by(game_id=game_id, area_id=area_id).first()
    if not game_area or game_area.available_seats < full_quantity:
        return "票數不足或區域無效", 400
    if game_area.disabled_available_seats < disabled_quantity:
        return "超過此區可售身障票數量", 400

    game_area.available_seats -= full_quantity
    game_area.disabled_available_seats -= disabled_quantity

    area = db.session.query(Area).filter_by(area_id=area_id).first()
    ticket_price = area.price if area else 0
    disabled_ticket_price = area.disabled_price if area else 0
    new_order = Order(
        buyer_name=current_user.mem_name,
        buyer_email=current_user.mem_email,
        buyer_phone=current_user.mem_phone,
        total_price=(ticket_price * full_quantity) + (disabled_ticket_price * disabled_quantity),
        mem_id=current_user.mem_id,
        order_status='N',
        createdAt= datetime.now()
    )
    db.session.add(new_order)
    db.session.flush()

    used_seat_nos = db.session.query(Ticket.seat_no).filter_by(game_id=game_id, area_id=area_id).all()
    used_seat_nos = {seat_no for (seat_no,) in used_seat_nos}
    seat_pool = [f"A{i:03}" for i in range(1, area.seat_count + area.disabled_seats + 1)]
    available_seat_nos = [seat for seat in seat_pool if seat not in used_seat_nos]

    if len(available_seat_nos) < total_quantity:
        return "剩餘座位不足", 400

    for i in range(full_quantity):
        seat_no = available_seat_nos[i]
        ticket = Ticket(
            seat_no=seat_no,
            ticket_status='L',
            is_disabled=False,
            order_id=new_order.order_id,
            game_id=game_id,
            area_id=area_id,
            createdAt= datetime.now()
        )
        db.session.add(ticket)

    for i in range(disabled_quantity):
        seat_no = available_seat_nos[full_quantity + i]
        ticket = Ticket(
            seat_no=seat_no,
            ticket_status='L',
            is_disabled=True,
            order_id=new_order.order_id,
            game_id=game_id,
            area_id=area_id,
            createdAt= datetime.now()
        )
        db.session.add(ticket)

    db.session.commit()
    return redirect(url_for('select_payment', order_id=new_order.order_id))


# 購票ATM方式付款
@app.route('/ticket/select-atm/<int:order_id>')
@login_required
def select_atm(order_id):
    # 根據 order_id 取得訂單資訊顯示
    order = Order.query.filter_by(order_id=order_id, order_status='N').first()
    if not order:
        return redirect(url_for('index'))

    # 取得付款資訊
    payment = Payment.query.filter_by(order_id=order_id).first()

    # 設定繳費期限為當前時間 + 15 分鐘
    due_time = datetime.now() + timedelta(minutes=15)
    formatted_due_time = due_time.strftime('%Y/%m/%d %H:%M')

    # 取得訂單中所有票券與區域
    tickets = db.session.query(Ticket).filter_by(order_id=order_id).all()
    if tickets:
        game = Game.query.get(tickets[0].game_id)
        show = Show.query.get(game.show_id)
        location = Location.query.get(show.location_id)
    else:
        game = show = location = None
    return render_template(
        'atm.html',
        order=order,
        payment=payment,
        payment_due_time=formatted_due_time,
        tickets=tickets,
        show=show,
        game=game,
        location=location
    )

# 購票creditcard方式付款
@app.route('/ticket/select-creditcard/<int:order_id>')
@login_required
def select_creditcard(order_id):
    order = Order.query.filter_by(order_id=order_id, order_status='N').first()
    if not order:
        return redirect(url_for('index'))
    print(order.payment)
    payment = Payment.query.filter_by(order_id=order_id).first()
    tickets = Ticket.query.filter_by(order_id=order_id).all()
    show = None
    if tickets:
        game = Game.query.get(tickets[0].game_id)
        show = Show.query.get(game.show_id)
        location = Location.query.get(show.location_id)
    else:
        game = show = location = None
    return render_template('creditcard.html', order=order, payment=payment, show=show, tickets=tickets, game=game, location=location)



# 購票完成頁面
@app.route('/ticket/order-complete/<int:order_id>')
@login_required
def order_complete(order_id):
    order = Order.query.filter_by(order_id=order_id, order_status='Y').first()
    if not order:
        return redirect(url_for('index'))
    tickets = Ticket.query.filter_by(order_id=order_id).all()

    # 預設使用第一張票取得相關資訊
    if tickets:
        game = Game.query.get(tickets[0].game_id)
        show = Show.query.get(game.show_id)
        location = Location.query.get(show.location_id)
    else:
        game = show = location = None

    return render_template(
        'order_complete.html',
            order=order,
            tickets=tickets,
            show=show,
            game=game,
            location=location
        )
    # return render_template('order_complete.html')


# 退款表單
@app.route('/ticket/refund/<int:order_id>', methods=['GET', 'POST'])
@login_required
def refund_detail(order_id):
    order = Order.query.get(order_id)
    ticket = Ticket.query.filter_by(order_id=order_id).first()
    show = Show.query.get(ticket.game_id) if ticket else None
    location = Location.query.get(show.location_id) if show else None

    amount = order.total_price if order else 0
    game = Game.query.get(ticket.game_id) if ticket else None
    datetime_str = None
    if game and game.game_date and game.game_time:
        show_datetime = datetime.combine(game.game_date, game.game_time)
        datetime_str = show_datetime.strftime('%Y/%m/%d(%a) %H:%M')

    refund = Refund.query.filter_by(order_id=order_id).first()
    if refund:
        if refund.refund_status == 'approved':
            status_display = '已完成'
        elif refund.refund_status == 'rejected':
            status_display = '已拒絕'
        else:
            status_display = refund.refund_status  # fallback 顯示原始狀態

        message = f"此訂單已申請退款，狀態為：{status_display}"
        return render_template("refund_form.html", message=message, order=None)

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        if not name or not email or not phone:
            message = "請填寫完整退款資訊"
            return render_template("refund_form.html", message=message, order={
                'order_id': order.order_id,
                'show': show,
                'location': location,
                'datetime': datetime_str or '未知',
                'amount': amount
            })

        now = datetime.now()

        if game and game.game_date and game.game_time:
            show_datetime = datetime.combine(game.game_date, game.game_time)
            if now < show_datetime - timedelta(days=1):
                refund_status = 'approved'
                message = "退款申請已完成，請留意您的信箱通知。"

                refund_request = Refund(
                    order_id=order.order_id,
                    name=name,
                    email=email,
                    phone=phone,
                    refund_status=refund_status,
                    createdAt=now,
                    updatedAt=now
                )
                db.session.add(refund_request)

                order.order_status = 'C'
                order.updatedAt = now

                tickets = Ticket.query.filter_by(order_id=order.order_id).all()
                for ticket in tickets:
                    game_area = db.session.query(GameArea).filter_by(
                        game_id=ticket.game_id, area_id=ticket.area_id).first()
                    if game_area:
                        if ticket.is_disabled:
                            game_area.disabled_available_seats += 1
                        else:
                            game_area.available_seats += 1

                db.session.commit()

                # 成功後不再顯示表單
                return render_template("refund_form.html", message=message, order=None)
            else:
                refund_status = 'rejected'
                message = "退款申請被拒絕，請確認是否已超過演出前一天。"
                refund_request = Refund(
                    order_id=order.order_id,
                    name=name,
                    email=email,
                    phone=phone,
                    refund_status=refund_status,
                    createdAt=now,
                    updatedAt=now
                )
                db.session.add(refund_request)
                db.session.commit()

                return render_template("refund_form.html", message=message, order=None, form_allowed=False)

    # GET 預設頁面
    return render_template("refund_form.html", message=None, order={
        'order_id': order.order_id,
        'show': show,
        'location': location,
        'datetime': datetime_str or '未知',
        'amount': amount
    })




# 我的票夾
@app.route('/my-tickets')
@login_required
def my_tickets():
    orders = Order.query.filter_by(mem_id=current_user.mem_id).all()
    order_data = []
    order_ids = [order.order_id for order in orders]

    refunds = Refund.query.filter(Refund.order_id.in_(order_ids)).all()
    refund_status_map = {refund.order_id: refund.refund_status for refund in refunds}

    for order in orders:
        tickets = (
            db.session.query(Ticket, Game, Show, Area)
            .join(Game, Ticket.game_id == Game.game_id)
            .join(Show, Game.show_id == Show.show_id)
            .join(Area, Ticket.area_id == Area.area_id)
            .filter(Ticket.order_id == order.order_id)
            .all()
        )
        order_data.append({
            'order': order,
            'tickets': tickets,
            'refund_status': refund_status_map.get(order.order_id, None)
        })

    return render_template('my_ticket.html', order_data=order_data)


#節目詳情頁
@app.route('/show/<int:show_id>')
def show_detail(show_id):
    show = Show.query.get_or_404(show_id)
    host = Host.query.get(show.host_id)
    location = Location.query.get(show.location_id)

    show_data = {
        'show_id': show.show_id,
        'show_name': show.show_name,
        'show_desc': show.show_desc,
        "start_date": show.start_date.strftime('%Y/%m/%d') if show.start_date else None,
        "end_date": show.end_date.strftime('%Y/%m/%d') if show.end_date else None,
        'show_pic': show.show_pic,
        'createdAt': show.createdAt,
        'host': {
            'host_name': host.host_name if host else "未知主辦",
            'host_email': host.host_email if host else "未知信箱"
        },
        'location': {
            'loc_name': location.loc_name if location else "未知地點"
        }
    }

    return render_template('show_detail.html', show=show_data)
#節目詳情跳轉至購票起始頁
@app.route("/ticket/purchase/<int:show_id>")
def ticket_start(show_id):
    show = Show.query.get(show_id)
    if not show:
        abort(404)
    host = Host.query.get(show.host_id)
    location = Location.query.get(show.location_id)
    games = Game.query.filter_by(show_id=show.show_id).all()
    return render_template("ticket_start.html", s=show, host=host, location=location, games=games,now=datetime.now())

#換行
@app.template_filter('nl2br')
def nl2br_filter(s):
    if s is None:
        return ''
    return Markup(s.replace("\n", "<br>\n"))


# 訂單詳情頁
@app.route('/order/<int:order_id>')
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    tickets = db.session.query(Ticket, Game, Show, Area, Location)\
    .join(Game, Ticket.game_id == Game.game_id)\
    .join(Show, Game.show_id == Show.show_id)\
    .join(Area, Ticket.area_id == Area.area_id)\
    .join(Location, Show.location_id == Location.loc_id)\
    .filter(Ticket.order_id == order_id).all()
    refund = Refund.query.filter_by(order_id=order_id).first()
    refund_status = refund.refund_status if refund else None
    return render_template('order_detail.html', order=order, tickets=tickets, refund_status=refund_status)

# 選擇付款
@app.route('/ticket/select-payment/<int:order_id>')
def select_payment(order_id):
    order = Order.query.filter_by(order_id=order_id, order_status='N').first()
    if not order:
        return redirect(url_for('index'))
    tickets = Ticket.query.filter_by(order_id=order_id).all()
    if not tickets:
        return "找不到此訂單的票券", 404
   
    game = Game.query.get(tickets[0].game_id)
    show = Show.query.get(game.show_id)
    host = Host.query.get(show.host_id)
    location = Location.query.get(show.location_id)

    member = Member.query.get(order.mem_id)
    if not member:
      return "尚未建立會員資料，請先新增會員", 404

    return render_template(
        'select_payment.html',
        show=show,
        game=game,
        host=host,
        location=location,
        member=member,
        order=order
    )

@app.route('/ticket/select-payment-method', methods=['POST'])
def select_payment_method():
  order_id = request.form.get('order_id')
  pay_method = request.form.get('pay_method')

  order = Order.query.filter_by(order_id=order_id, order_status='N').first()
  if not order:
    return redirect(url_for('index'))

  # 建立 Payment 記錄
  payment = Payment(
      pay_method='C' if pay_method == 'creditcard' else 'A',  # C:信用卡, A:ATM
      pay_status='N',  # N:未付款
      amount=order.total_price,
      paid_time=None,
      createdAt=datetime.now(),
      updatedAt=datetime.now()
  )
  db.session.add(payment)
  db.session.flush()  # 讓 payment_id 生成，但還沒 commit

  # 更新 Order 紀錄
  order.payment_id = payment.payment_id
  order.updatedAt = datetime.now()

  db.session.commit()  # 一次性提交所有變更

  # 根據付款方式導向相應頁面
  if pay_method == 'creditcard':
      return redirect(url_for('select_creditcard', order_id=order_id))
  elif pay_method == 'atm':
      return redirect(url_for('select_atm', order_id=order_id))
  else:
      return "未知的付款方式", 400
  
@app.route('/ticket/confirm-payment', methods=['POST'])
def confirm_payment():
  order_id = request.form.get('order_id')
  order = Order.query.filter_by(order_id=order_id, order_status='N').first()
  if not order:
      return redirect(url_for('index'))
  payment = Payment.query.filter_by(order_id=order_id).first()

  if payment:
    payment.pay_status = 'Y'
    payment.paid_time = datetime.now()
    payment.updatedAt = datetime.now()

  order.order_status = 'Y'
  order.updatedAt = datetime.now()

  db.session.commit()

  return redirect(url_for('order_complete', order_id=order_id))

if __name__ == '__main__':
    with app.app_context():
        from models import Show
        from datetime import datetime

        shows = Show.query.all()
        for s in shows:
            if isinstance(s.start_date, str):
                s.start_date = datetime.strptime(s.start_date, '%Y-%m-%d').date()
            if isinstance(s.end_date, str):
                s.end_date = datetime.strptime(s.end_date, '%Y-%m-%d').date()
        db.session.commit()
        print("✔ 已修正所有 start_date 和 end_date 格式")

    app.run(debug=True)
