"""HTTP-маршруты сервиса обращений."""
from flask import Blueprint, current_app, jsonify, request

from .auth import login_required
from .storage import create_ticket, get_ticket

bp = Blueprint("tickets", __name__)

MAX_TEXT_LENGTH = 500


@bp.post("/tickets")
@login_required
def create():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text")
    if not isinstance(text, str) or not text.strip():
        return jsonify(error="Поле text обязательно"), 400
    if len(text) > MAX_TEXT_LENGTH:
        return jsonify(error=f"Длина text не более {MAX_TEXT_LENGTH} символов"), 400
    ticket_id = create_ticket(current_app.config["DB_PATH"], request.current_user, text)
    return jsonify(id=ticket_id), 201


@bp.get("/tickets/<int:ticket_id>")
@login_required
def read(ticket_id: int):
    ticket = get_ticket(current_app.config["DB_PATH"], ticket_id, request.current_user)
    if ticket is None:
        # Одинаково для «нет такого» и «чужое»: существование записи не раскрывается
        return jsonify(error="Не найдено"), 404
    return jsonify(ticket)
