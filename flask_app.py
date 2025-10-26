# === flask_app.py — app entrypoint ===
from dotenv import load_dotenv
load_dotenv()

import os
from app import create_app
from app.extensions import db
from config import DevelopmentConfig, ProductionConfig

# Detect environment
env = os.getenv("FLASK_ENV", "production").lower()
config_class = DevelopmentConfig if env == "development" else ProductionConfig

print(f"[flask_app] Environment: {env}")
print(f"[flask_app] Using: {config_class.__name__}")

# Build app
app = create_app(config_class)

# Ensure tables exist and seed if empty
from app.seed import app as seed_app, db as seed_db, Mechanic
with seed_app.app_context():
    seed_db.create_all()
    if not Mechanic.query.first():
        from app.seed import *
    print("[DB] Tables ensured + seed check complete")

# Gunicorn serves on Render; locally run `flask --app flask_app run`
if __name__ == "__main__":
    app.run()
