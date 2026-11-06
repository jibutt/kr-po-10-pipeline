"""Функциональные (TC-01) и негативные (TC-02..TC-05) сценарии из таблицы 5 пояснительной записки."""


def test_tc01_create_and_read_valid_ticket(client, alice):
    created = client.post("/tickets", json={"text": "Не работает вход"}, headers=alice)
    assert created.status_code == 201
    ticket_id = created.get_json()["id"]

    read = client.get(f"/tickets/{ticket_id}", headers=alice)
    assert read.status_code == 200
    assert read.get_json() == {"id": ticket_id, "owner": "alice", "text": "Не работает вход"}


def test_tc02_empty_required_field_rejected(client, alice):
    response = client.post("/tickets", json={"text": "   "}, headers=alice)
    assert response.status_code == 400
    assert "обязательно" in response.get_json()["error"]


def test_tc02_missing_field_rejected(client, alice):
    response = client.post("/tickets", json={}, headers=alice)
    assert response.status_code == 400


def test_tc03_too_long_text_rejected(client, alice):
    response = client.post("/tickets", json={"text": "a" * 501}, headers=alice)
    assert response.status_code == 400
    assert "500" in response.get_json()["error"]


def test_tc03_boundary_length_accepted(client, alice):
    response = client.post("/tickets", json={"text": "a" * 500}, headers=alice)
    assert response.status_code == 201


def test_tc04_other_user_cannot_read_ticket(client, alice, bob):
    ticket_id = client.post("/tickets", json={"text": "секрет Алисы"}, headers=alice).get_json()["id"]

    response = client.get(f"/tickets/{ticket_id}", headers=bob)
    assert response.status_code == 404
    assert "секрет" not in response.get_data(as_text=True)


def test_tc04_nonexistent_ticket_same_response_as_foreign(client, alice, bob):
    ticket_id = client.post("/tickets", json={"text": "x"}, headers=alice).get_json()["id"]
    foreign = client.get(f"/tickets/{ticket_id}", headers=bob)
    missing = client.get("/tickets/999999", headers=bob)
    assert foreign.status_code == missing.status_code == 404
    assert foreign.get_json() == missing.get_json()


def test_tc05_sql_payload_stored_as_data(client, alice):
    payload = "x'); DROP TABLE tickets; --"
    created = client.post("/tickets", json={"text": payload}, headers=alice)
    assert created.status_code == 201
    ticket_id = created.get_json()["id"]

    read = client.get(f"/tickets/{ticket_id}", headers=alice)
    assert read.get_json()["text"] == payload

    # Таблица на месте: обращение по-прежнему читается
    again = client.get(f"/tickets/{ticket_id}", headers=alice)
    assert again.status_code == 200


def test_unauthenticated_request_rejected(client):
    response = client.post("/tickets", json={"text": "x"})
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers


def test_wrong_password_rejected(client):
    from tests.conftest import basic
    response = client.post("/tickets", json={"text": "x"}, headers=basic("alice", "wrong"))
    assert response.status_code == 401
