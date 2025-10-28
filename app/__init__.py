from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
# from dotenv import load_dotenv
import os

# === Extensions ===
from app.extensions import db, ma, migrate, limiter, cache
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.customers import customers_bp
from app.blueprints.inventory import inventory_bp
from config import DevelopmentConfig, TestingConfig, ProductionConfig

# === Load env ===
# load_dotenv()

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'


def create_app(config_name=None):
    app = Flask(__name__)

    # === Config selection ===
    env = os.getenv("FLASK_ENV", "production").lower()
    config_map = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }
    app.config.from_object(config_map.get(env, ProductionConfig))
    print(f"[INIT] Loaded {env} configuration")

    # === Initialize extensions ===
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cache.init_app(app)

    # === Register blueprints BEFORE CORS ===
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    # === Apply CORS after routes exist ===
    CORS(
        app,
        resources={r"/*": {"origins": [
            # Local development
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5000",
            "http://127.0.0.1:5000",
            # Production (Render)
            "https://mechanic-api.onrender.com",
            "https://react-mechanic-api.onrender.com"
        ]}},
        supports_credentials=True,
        expose_headers=["Content-Type", "Authorization"],
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )

    # === Swagger setup ===
    swagger_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Mechanic Workshop API"}
    )
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

    # === Root ===
    @limiter.exempt
    @app.route("/", methods=["GET"])
    def root():
        return {
            "message": "Mechanic Workshop API is live",
            "docs": "/api/docs",
        }, 200

    # === Health check ===
    @limiter.exempt
    @app.route("/ping", methods=["GET"])
    def ping():
        return {
        "status": "ok",
        "env": app.config.get("ENV", os.getenv("FLASK_ENV", "production"))
    }, 200

    return app