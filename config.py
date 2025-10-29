# === config.py — Flask configuration for multiple environments ===
import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    # Persistent local SQLite DB (inside /instance)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///instance/dev.db")


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///instance/testing.db")
    TESTING = True


class ProductionConfig(Config):
    uri = os.getenv("DATABASE_URL")

    if not uri:
        raise RuntimeError("DATABASE_URL not set — cannot start production")

    # Handle old postgres:// prefix
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    # Ensure SSL mode for Render
    if "sslmode" not in uri and "sqlite" not in uri:
        uri = f"{uri}?sslmode=require"

    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"sslmode": "require"},
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
