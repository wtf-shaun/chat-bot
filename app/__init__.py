"""Application factory and runtime wiring."""
from flask import Flask

from config import Config
from app.models.database import init_db
from app.routes.chat import chat_bp
from app.routes.import_chat import import_bp
from app.routes.settings import settings_bp


def create_app(config_class: type[Config] = Config) -> Flask:
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    init_db(app.config["DATABASE_PATH"])
    app.register_blueprint(chat_bp)
    app.register_blueprint(import_bp)
    app.register_blueprint(settings_bp)
    app.config.setdefault("JSON_SORT_KEYS", False)
    return app
