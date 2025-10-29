# === __init__.py — main app factory with auto dev.db handling ===
import os
from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from app.extensions import db, ma, migrate, limiter, cache
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.customers import customers_bp
from app.blueprints.inventory import inventory_bp
from config import DevelopmentConfig, TestingConfig, ProductionConfig

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

def create_app(config_name=None):
    app = Flask(__name__)

    # === Pick config ===
    env = os.getenv("FLASK_ENV", "production").lower()
    config_map = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }
    app.config.from_object(config_map.get(env, ProductionConfig))
    print(f"[INIT] Loaded {env} configuration")

    # === Init extensions ===
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cache.init_app(app)

    # === Auto-create dev.db (if missing) ===
    if env == "development":
        instance_dir = os.path.join(app.root_path, "..", "instance")
        os.makedirs(instance_dir, exist_ok=True)
        db_path = os.path.join(instance_dir, "dev.db")
        with app.app_context():
            if not os.path.exists(db_path):
                db.create_all()
                db.session.commit()
                print("[DB] Created new dev.db in instance/")
            else:
                print("[DB] dev.db already exists — skipping creation.")

    # === Register blueprints ===
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    # === Seed trigger route ===
    try:
        from app.blueprints.seed_trigger.routes import seed_trigger_bp
        app.register_blueprint(seed_trigger_bp)
        print("[INIT] /seed route loaded.")
    except Exception as e:
        print(f"[INIT] Failed to load seed route: {e}")

    # === CORS setup ===
    CORS(
        app,
        resources={r"/*": {"origins": [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "https://mechanics-api.onrender.com",
            "https://react-mechanic-api.onrender.com",
        ]}},
        supports_credentials=True,
        expose_headers=["Content-Type", "Authorization"],
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )

    # === Swagger UI ===
    swagger_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Mechanic Workshop API"}
    )
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

    # === Root + health check ===
    @limiter.exempt
    @app.route("/", methods=["GET"])
    def root():
        return {"message": "Mechanic Workshop API is live", "docs": "/api/docs"}, 200

    @limiter.exempt
    @app.route("/ping", methods=["GET"])
    def ping():
        db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "Unknown")
        return {"status": "ok", "env": env, "database": db_uri}, 200

    return app
