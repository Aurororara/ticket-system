from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from config import Config
from models import db
from models.member import Member  # Member model，記得有繼承 UserMixin

app = Flask(__name__)
app.config.from_object(Config)

# 初始化資料庫
db.init_app(app)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show/<program_name>')
def show_detail(program_name):
    return f"這是 {program_name} 的節目詳情頁"

@app.route('/show/test')
def test_detail():
    return "這是節目詳情測試頁"

@app.route('/ticket/start')
def view_ticket_start():
    return render_template('ticket_start.html')

@app.route('/ticket/select-area')
def select_area():
    return render_template('select_area.html')

@app.route('/ticket/select-type')
def select_type():
    return render_template('select_type.html')

# =======================
# 執行伺服器
# =======================

if __name__ == '__main__':
    app.run(debug=True)
