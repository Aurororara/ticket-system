from app import app, db
from models import (
    Member, Show, Host, Location, Game, Area, Section,
    Order, Payment, Ticket, GameArea
)
from datetime import datetime, date, time, timedelta
from werkzeug.security import generate_password_hash

with app.app_context():
    # Clear existing data (for development only, do not use in production)
    db.drop_all()
    db.create_all()

    # Debug prints for date and timedelta
    print("date.today():", date.today())
    print("timedelta(days=30):", timedelta(days=30))
    print("date.today() + timedelta(days=30):", date.today() + timedelta(days=30))

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

    # Add a game (show date 30 days from now)
    db.session.add(show)
    db.session.commit()  # Commit to get show_id

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
    payment = Payment(
        pay_method="C",
        pay_status="Y",
        amount=5000,
        paid_time=datetime.now(),
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # Add an order
    order = Order(
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

    # Add a ticket
    ticket = Ticket(
        seat_no="A001",
        ticket_status="L",
        order_id=1,
        game_id=1,
        area_id=1,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # Add all to session and commit
    db.session.add_all([
        member, host, location, section, show, game,
        area, game_area, payment, order, ticket
    ])
    db.session.commit()

    print("Seed data added successfully.")
