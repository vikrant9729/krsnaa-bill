# Run this script once to create all tables in your PostgreSQL database
from app import db, app

with app.app_context():
    db.create_all()
    print("✅ All tables created successfully.")
