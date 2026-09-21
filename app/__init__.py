from flask import Flask
from config import Config
from .models.database import init_db
from .routes.chat import chat_bp
from .routes.import_chat import import_bp
from .routes.settings import settings_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    init_db(app.config["DATABASE_PATH"])
    app.register_blueprint(chat_bp)
    app.register_blueprint(import_bp)
    app.register_blueprint(settings_bp)
    return app
