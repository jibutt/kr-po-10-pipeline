"""Учебный веб-сервис обращений: приложение Flask."""
from flask import Flask

from .storage import init_db
from .views import bp


def create_app(db_path: str = "tickets.db") -> Flask:
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path
    init_db(db_path)
    app.register_blueprint(bp)
    return app
