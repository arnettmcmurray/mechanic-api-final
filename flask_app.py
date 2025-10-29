# === flask_app.py — app entrypoint ===
#from dotenv import load_dotenv
#load_dotenv()

import os
from app import create_app
from config import DevelopmentConfig, ProductionConfig

env = os.getenv("FLASK_ENV", "production").lower()
config_class = DevelopmentConfig if env == "development" else ProductionConfig

print(f"[flask_app] Environment: {env}")
print(f"[flask_app] Using: {config_class.__name__}")

# Build app
app = create_app(config_class)

# === Ensure local tables only (no reseed, no drops) ===
if env == "development":
    from app.extensions import db
    with app.app_context():
        db.create_all()
        print("[DB] Local tables ensured — no seed triggered.")

# Gunicorn for Render, flask run for local
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


