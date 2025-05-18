from app import app, db
from models import (
    Member, Show, Host, Location, Game, Area, Section,
    Order, Payment, Ticket, GameArea
)
from datetime import datetime, date, time

with app.app_context():
    # ❗清空資料表（開發時用，正式環境不要加）
    db.drop_all()
    db.create_all()

    # 🧑 新增一位會員（用來登入）
    member = Member(
        mem_id=1,
        mem_name="玟潔",
        mem_acc="aurora",
        mem_email="aurora@test.com",
        mem_pwd="yeah123456",  # 若有加密請自行加密
        birthday=date(2000, 1, 1),
        mem_phone="0912345678"
    )

    # 🏢 新增主辦單位
    host = Host(
        host_id=1,
        host_name="BELIFT LAB",
        host_email="host@test.com",
        createdAt=date.today(),
        updatedAt=date.today()
    )

    # 🏟️ 新增地點
    location = Location(
        loc_id=1,
        loc_name="KSPO DOME",
        createdAt=date.today(),
        updatedAt=date.today()
    )

    # 📐 新增區段
    section = Section(
        sect_id=1,
        sect_name="搖滾區",
        createdAt=date.today(),
        updatedAt=date.today()
    )

    # 🎤 新增節目
    show = Show(
        show_id=1,
        show_name="ENHYPEN Fate+ in Seoul",
        show_desc="我好想看",
        show_pic="enhypen.jpg",
        host_id=1,
        location_id=1,
        createdAt=date.today(),
        updatedAt=date.today()
    )

    # 📅 新增一場場次（關鍵：game_status 要是 'A' 開賣中）
    game = Game(
        game_id=1,
        game_date=date(2025, 5, 31),
        game_time=time(19, 0),
        sale_start_time=datetime(2025, 5, 1, 10, 0),
        sale_end_time=datetime(2025, 5, 30, 23, 59),
        game_status="A",
        total_seats=1000,
        available_seats=998,
        show_id=1,
        createdAt=date.today(),
        updatedAt=date.today()
    )

    # 🪑 新增一個場區
    area = Area(
        area_id=1,
        area_name="A區 VIP",
        seat_count=500,
        price=7880,
        loc_id=1,
        sect_id=1,
        createdAt=date.today(),
        updatedAt=date.today()
    )

    # 🔁 將場次與場區連結（GameArea）
    game_area = GameArea(
        game_area_id=1,
        total_seats=500,
        available_seats=499,
        game_id=1,
        area_id=1,
        createdAt=date.today(),
        updatedAt=date.today()
    )

    # 💳 新增付款資料
    payment = Payment(
        payment_id=1,
        pay_method="1",
        pay_status="1",
        amount=7880,
        paid_time=datetime.now(),
        order_id=1,  # ⚠️ 須與訂單對應
        createdAt=date.today(),
        updatedAt=date.today()
    )

    # 🧾 新增訂單
    order = Order(
        order_id=1,
        order_status="1",
        buyer_name="玟潔",
        buyer_email="aurora@test.com",
        buyer_phone="0912345678",
        total_price=7880,
        mem_id=1,
        payment_id=1,
        createdAt=date.today(),
        updatedAt=date.today()
    )

    # 🎟️ 新增票券（指定給該場次＋場區）
    ticket = Ticket(
        ticket_id=1,
        seat_no="A01",
        ticket_status="1",
        order_id=1,
        game_id=1,
        area_id=1,
        createdAt=date.today(),
        updatedAt=date.today()
    )

    # ✅ 一次加入所有資料
    db.session.add_all([
        member, host, location, section, show, game,
        area, game_area, payment, order, ticket
    ])
    db.session.commit()

    print("✅ 模擬資料新增完成")
