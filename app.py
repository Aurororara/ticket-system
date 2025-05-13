from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from config import Config
from models import db
from models.show import Show
from models.host import Host
from models.game import Game
from models.location import Location
from models.area import Area
from models.section import Section
from collections import defaultdict
from models.member import Member  # Member model，記得有繼承 UserMixin
from models.location import Location

app = Flask(__name__)
app.config.from_object(Config)

# 初始化資料庫
db.init_app(app)
# 建立資料表
with app.app_context():
  db.create_all()
  print("資料表已建立完成")

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
@app.route('/ticket/select-type')
def select_type():
  return render_template('select_type.html')

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
@app.route('/ticket/refund', methods=['GET', 'POST'])
def refund_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        print("收到退款申請：")
        print("姓名：", name)
        print("信箱：", email)
        print("電話：", phone)

        return "退款申請送出成功，請留意您的信箱通知。"
    return render_template('refund_form.html')

# 初始化登入管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # 如果未登入導向 login 頁面

# 載入使用者
@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))

# =======================
# 登入登出
# =======================

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
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# =======================
# 主頁與其他頁面
# =======================

@app.route('/show/test')
def test_detail():
    return "這是節目詳情測試頁"

# =======================
# 執行伺服器
# =======================



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


#跳轉至票夾跟會員頁
@app.route('/member')
def member():
    return render_template('member.html')  # 需會員介面

@app.route('/ticket')
def ticket():
    return render_template('ticket.html')  # 需票夾頁面


if __name__ == '__main__':
    app.run(debug=True)