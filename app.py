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



#節目詳情頁
@app.route('/show/<int:show_id>')
def show_detail(show_id):
    show = {
        'show_name': '台北商業大學第一屆校慶',
        'show_desc': '一場為學生打造的熱鬧校慶活動！',
        'show_pic': '/static/images/sample.jpg',
        'createdAt': '2025-03-10',
        'host': {'host_name': '近雄國際'},
        'location': {'loc_name': '高雄巨蛋'}
    }
    return render_template('show_detail.html', show=show)

#跳轉至票夾跟會員頁
@app.route('/member')
def member():
    return render_template('member.html')  # 需會員介面

@app.route('/ticket')
def ticket():
    return render_template('ticket.html')  # 需票夾頁面


if __name__ == '__main__':
  app.run(debug=True)
