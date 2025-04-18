from flask import Flask
from app.api.routes import api_bp
from app.db.models import db, Record
from datetime import datetime, timedelta
import random

def seed_fake_data():
    if Record.query.count() == 0:
        print("Seeding fake data into the database...")
        start_date = datetime(2025, 4, 1)
        for day in range(10):
            current_date = start_date + timedelta(days=day)
            num_records = random.randint(5, 15)
            for _ in range(num_records):
                value = round(random.uniform(10.0, 100.0), 2)
                record = Record(value=value, timestamp=current_date)
                db.session.add(record)
        db.session.commit()
        print("Fake data seeded successfully!")

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:password@localhost:5432/insights"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_fake_data()

    app.register_blueprint(api_bp, url_prefix="/api")

    from app.dashapp.dashboard import init_dashboard
    init_dashboard(app)

    return app