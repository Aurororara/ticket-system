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

if __name__ == '__main__':
  app.run(debug=True)
