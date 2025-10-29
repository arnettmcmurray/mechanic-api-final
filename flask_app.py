# === flask_app.py — unified entrypoint for dev + prod ===
import os
from app import create_app

env = os.getenv("FLASK_ENV", "production").lower()
print(f"[flask_app] Environment: {env}")

# Create app based on environment
app = create_app()

# === Print active database ===
with app.app_context():
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "Unknown")
    masked_uri = db_uri.replace(os.getenv("DATABASE_URL", ""), "[RENDER_DB_URL]") if "postgres" in db_uri else db_uri
    print(f"[flask_app] Connected to: {masked_uri}")

# === Run ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
