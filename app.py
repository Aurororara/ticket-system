from flask import Flask, render_template, jsonify, request
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

# 主頁
@app.route('/')
def index():
    return render_template('index.html')

# 購票起始頁
@app.route('/ticket/start')
def view_ticket_start():
    return render_template('ticket_start.html')

# 選擇區域
@app.route('/ticket/select-area')
def select_area():
    return render_template('select_area.html')

# 選擇票種
@app.route('/ticket/select-type')
def select_type():
    return render_template('select_type.html')

if __name__ == '__main__':
    app.run(debug=True)
