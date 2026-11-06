"""Базовая HTTP-аутентификация. Учётные записи передаются через конфигурацию приложения."""
from functools import wraps

from flask import Response, current_app, request
from werkzeug.security import check_password_hash


def check_credentials(username: str, password: str, users: dict) -> bool:
    stored = users.get(username)
    return stored is not None and check_password_hash(stored, password)


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        users = current_app.config.get("USERS", {})
        if not auth or not check_credentials(auth.username or "", auth.password or "", users):
            return Response(
                "Требуется аутентификация", 401,
                {"WWW-Authenticate": 'Basic realm="tickets"'},
            )
        request.current_user = auth.username
        return view(*args, **kwargs)
    return wrapper
