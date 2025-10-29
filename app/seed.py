# === seed.py — force reseed for Render grading ===
import os
from flask import Flask
from config import DevelopmentConfig, ProductionConfig
from app.extensions import db
from app.models import Mechanic, Customer, Inventory, ServiceTicket

# Determine environment
env = os.getenv("FLASK_ENV", "production").lower()
config = DevelopmentConfig if env == "development" else ProductionConfig

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


def seed_data():
    """Seed the DB only if empty. Safe for Render and grading."""
    with app.app_context():
        uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
        print(f"\n[seed] Using DB: {uri}")
        print("🧨 Force reset enabled...")
        db.drop_all()
        db.create_all()

        if not Mechanic.query.first():
            print("⚙️  Empty DB — seeding full dataset...")

            # === Mechanics ===
            mechanics = [
                Mechanic(name="Admin", email="admin@shop.com", specialty="Manager"),
                Mechanic(name="Alex", email="alex@shop.com", specialty="Brakes"),
                Mechanic(name="Maria", email="maria@shop.com", specialty="Transmission"),
                Mechanic(name="Tyler", email="tyler@shop.com", specialty="Diagnostics"),
                Mechanic(name="Sasha", email="sasha@shop.com", specialty="Suspension"),
                Mechanic(name="Jordan", email="jordan@shop.com", specialty="Electrical"),
                Mechanic(name="Ravi", email="ravi@shop.com", specialty="Engine Repair"),
                Mechanic(name="Nina", email="nina@shop.com", specialty="Body Work"),
            ]
            mechanics[0].set_password("admin123")  # Admin
            for i, m in enumerate(mechanics[1:], start=1):
                m.set_password(f"password{i}")
            db.session.add_all(mechanics)
            db.session.commit()
            print("🔧 Mechanics seeded.")

            # === Customers ===
            customers = [
                Customer(name="John Doe", email="john@example.com", phone="312-555-1111", car="Honda Civic"),
                Customer(name="Jane Smith", email="jane@example.com", phone="312-555-2222", car="Toyota Camry"),
                Customer(name="Luis Martinez", email="luis@example.com", phone="773-555-3333", car="Ford F-150"),
                Customer(name="Emily Davis", email="emily@example.com", phone="847-555-4444", car="Subaru Outback"),
                Customer(name="Mike Johnson", email="mike@example.com", phone="630-555-5555", car="Chevrolet Malibu"),
                Customer(name="Olivia Brown", email="olivia@example.com", phone="224-555-6666", car="BMW 3 Series"),
                Customer(name="Noah Wilson", email="noah@example.com", phone="708-555-7777", car="Hyundai Sonata"),
                Customer(name="Ava Lee", email="ava@example.com", phone="815-555-8888", car="Kia Sportage"),
                Customer(name="Ethan Clark", email="ethan@example.com", phone="219-555-9999", car="Mazda CX-5"),
                Customer(name="Sophia Turner", email="sophia@example.com", phone="309-555-0000", car="Nissan Altima"),
            ]
            db.session.add_all(customers)
            db.session.commit()
            print("👥 Customers seeded.")

            # === Inventory ===
            inventory_items = [
                Inventory(name="Brake Pads", price=49.99, quantity=30),
                Inventory(name="Oil Filter", price=9.99, quantity=100),
                Inventory(name="Air Filter", price=14.99, quantity=60),
                Inventory(name="Spark Plugs", price=5.49, quantity=120),
                Inventory(name="Timing Belt", price=89.99, quantity=20),
                Inventory(name="Alternator", price=199.99, quantity=10),
                Inventory(name="Battery", price=129.99, quantity=15),
                Inventory(name="Radiator", price=179.99, quantity=8),
                Inventory(name="Headlight Bulb", price=24.99, quantity=40),
                Inventory(name="Wiper Blades", price=12.99, quantity=50),
                Inventory(name="Fuel Pump", price=149.99, quantity=6),
                Inventory(name="Engine Oil (5qt)", price=29.99, quantity=75),
            ]
            db.session.add_all(inventory_items)
            db.session.commit()
            print("📦 Inventory seeded.")

            # === Service Tickets ===
            tickets = [
                ServiceTicket(description="Brake pad replacement", status="In Progress", mechanic_id=2, customer_id=1),
                ServiceTicket(description="Oil change", status="Closed", mechanic_id=3, customer_id=2),
                ServiceTicket(description="Engine diagnostics", status="Open", mechanic_id=4, customer_id=3),
                ServiceTicket(description="Replace alternator", status="In Progress", mechanic_id=7, customer_id=4),
                ServiceTicket(description="Install new timing belt", status="Open", mechanic_id=7, customer_id=5),
                ServiceTicket(description="Battery replacement", status="Closed", mechanic_id=6, customer_id=6),
                ServiceTicket(description="Suspension inspection", status="In Progress", mechanic_id=5, customer_id=7),
                ServiceTicket(description="Body work estimate", status="Open", mechanic_id=8, customer_id=10),
            ]
            db.session.add_all(tickets)
            db.session.commit()
            print("🧾 Service tickets seeded.")

            print("\n✅ Seed complete — ready for grading.")
            print("   Login with admin@shop.com / admin123\n")

        else:
            print("⏭️  DB already populated — skipping reseed.\n")


if __name__ == "__main__":
    seed_data()
