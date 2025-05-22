from app import app, db
from models import (
    Member, Show, Host, Location, Game, Area, Section,
    Order, Payment, Ticket, GameArea
)
from datetime import datetime, date, time
from werkzeug.security import generate_password_hash

with app.app_context():
    # ❗清空資料表（開發時用，正式環境不要加）
    db.drop_all()
    db.create_all()

    # 🧑 新增一位會員（用來登入）
    member = Member(
        mem_id=1,
        mem_name="玟潔",
        mem_email="aurora@test.com",
        mem_pwd=generate_password_hash("123456"),  # 密碼已加密
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

    show = Show(
        show_id=1,
        show_name="ENHYPEN 'WALK THE LINE' Summer edition",
        show_desc="我好想看",
        show_pic="enhypen.jpg",
        host_id=2,
        location_id=2,
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

    from datetime import timedelta, date, datetime, time

    new_show = Show(
        show_id=3,
        show_name="FATE+ in Seoul",
        show_desc="Exciting new show in Seoul",
        show_pic="fateplus_seoul.jpg",
        host_id=1,  # Assuming host_id=1 exists
        location_id=1,  # Assuming location_id=1 exists
        createdAt=date.today(),
        updatedAt=date.today()
    )

    new_game = Game(
        game_id=3,
        game_date=date.today() + timedelta(days=30),
        game_time=time(19, 0),
        sale_start_time=datetime.combine(date.today(), time(0, 0)),
        sale_end_time=datetime.combine(date.today() + timedelta(days=29), time(23, 59, 59)),
        game_status="A",
        total_seats=1000,
        available_seats=1000,
        show_id=3,
        createdAt=date.today(),
        updatedAt=date.today()
    )

    new_area = Area(
        area_id=3,
        area_name="General Admission",
        seat_count=1000,
        price=5000,
        loc_id=1,
        sect_id=1,
        createdAt=date.today(),
        updatedAt=date.today()
    )

    new_game_area = GameArea(
        game_area_id=3,
        total_seats=1000,
        available_seats=1000,
        game_id=3,
        area_id=3,
        createdAt=date.today(),
        updatedAt=date.today()
    )

    db.session.add_all([new_show, new_game, new_area, new_game_area])
    db.session.commit()
    print("✅ 新增 FATE+ in Seoul show 和相關資料完成")

    # 新增會員的訂單、付款和票券資料，包含 FATE+ in Seoul show 的票
    new_payment = Payment(
        payment_id=2,
        pay_method="1",
        pay_status="1",
        amount=5000,
        paid_time=datetime.now(),
        createdAt=date.today(),
        updatedAt=date.today()
    )

    new_order = Order(
        order_id=2,
        order_status="1",
        buyer_name="玟潔",
        buyer_email="aurora@test.com",
        buyer_phone="0912345678",
        total_price=5000,
        mem_id=1,
        payment_id=2,
        createdAt=date.today(),
        updatedAt=date.today()
    )

    new_ticket = Ticket(
        ticket_id=2,
        seat_no="GA01",
        ticket_status="1",
        order_id=2,
        game_id=3,
        area_id=3,
        createdAt=date.today(),
        updatedAt=date.today()
    )

    db.session.add_all([new_payment, new_order, new_ticket])
    db.session.commit()
    print("✅ 新增 FATE+ in Seoul show 的訂單、付款和票券資料完成")
