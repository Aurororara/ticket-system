from flask import Flask, render_template, jsonify, request
from config import Config
from models import db

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
@app.route('/ticket/start')
def view_ticket_start():
  return render_template('ticket_start.html')

# 購票選擇區域
@app.route('/ticket/select-area')
def select_area():
    return render_template('select_area.html')

# 購票選擇票種
@app.route('/ticket/select-type')
def select_type():
    return render_template('select_type.html')

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

if __name__ == '__main__':
  app.run(debug=True)
