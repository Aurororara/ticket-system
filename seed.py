from app import app, db
from models import (
    Member, Show, Host, Location, Game, Area, Section,
    Order, Payment, Ticket, GameArea
)
from models.refund import Refund
from datetime import datetime, date, time, timedelta
from werkzeug.security import generate_password_hash

with app.app_context():
    # Clear existing data (for development only, do not use in production)
    db.drop_all()
    db.create_all()

    # Add a member
    member = Member(
        mem_name="Test User",
        mem_email="testuser@example.com",
        mem_pwd=generate_password_hash("TestPass123"),
        mem_phone="0912345678",
        birthday=date(2006, 10, 11),
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # Add a host
    host = Host(
        host_name="Sample Host",
        host_email="host@example.com",
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # Add a location
    location = Location(
        loc_name="Sample Venue",
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # Add a section
    section = Section(
        sect_name="General Admission",
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # Add a show with existing project image
    show = Show(
        show_name="Fate+ in Seoul",
        show_desc="This is a sample show.",
        show_pic="show1.jpg",  # Using existing image from static/img/
        host_id=1,
        location_id=1,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    db.session.add(show)
    db.session.commit()  # Commit to get show_id

    # Add a game (show date 30 days from now)
    game = Game(
        game_date=date.today() + timedelta(days=30),
        game_time=time(19, 0),
        sale_start_time=datetime.combine(date.today(), time(0, 0)),
        sale_end_time=datetime.combine(date.today() + timedelta(days=29), time(23, 59, 59)),
        game_status="A",
        total_seats=1000,
        available_seats=1000,
        show_id=show.show_id,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # Add an area
    area = Area(
        area_name="VIP Area",
        seat_count=500,
        price=5000,
        loc_id=1,
        sect_id=1,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # Add a game area
    game_area = GameArea(
        total_seats=500,
        available_seats=500,
        disabled_available_seats=500,
        game_id=1,
        area_id=1,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # Add a payment
    payment1 = Payment(
        pay_method="C",
        pay_status="Y",
        amount=5000,
        paid_time=datetime.now(),
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    payment2 = Payment(
        pay_method="C",
        pay_status="Y",
        amount=5000,
        paid_time=datetime.now(),
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # Add two orders: one refundable, one not refundable (refund sent day before show)
    order1 = Order(
        order_status="Y",
        buyer_name="Test User",
        buyer_email="testuser@example.com",
        buyer_phone="0912345678",
        total_price=5000,
        mem_id=1,
        payment_id=1,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    order2 = Order(
        order_status="Y",
        buyer_name="Test User",
        buyer_email="testuser@example.com",
        buyer_phone="0912345678",
        total_price=5000,
        mem_id=1,
        payment_id=2,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # Add tickets for both orders
    ticket1 = Ticket(
        seat_no="A001",
        ticket_status="L",
        order_id=1,
        game_id=1,
        area_id=1,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    ticket2 = Ticket(
        seat_no="A002",
        ticket_status="L",
        order_id=2,
        game_id=1,
        area_id=1,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # Add a refund request for order1 (refundable)
    refund1 = Refund(
        order_id=1,
        name="Test User",
        email="testuser@example.com",
        phone="0912345678",
        refund_status="pending",
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # Add a refund request for order2 (not refundable, sent day before show)
    refund2 = Refund(
        order_id=2,
        name="Test User",
        email="testuser@example.com",
        phone="0912345678",
        refund_status="rejected",
        createdAt=datetime.now() - timedelta(days=1),
        updatedAt=datetime.now() - timedelta(days=1)
    )

    # Add all to session and commit
    db.session.add_all([
        member, host, location, section, show, game,
        area, game_area, payment1, payment2, order1, order2,
        ticket1, ticket2, refund1, refund2
    ])
    db.session.commit()

    print("Seed data with two orders (one refundable, one not) added successfully.")
