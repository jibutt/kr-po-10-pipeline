from app.storage import create_ticket, get_ticket, init_db


def test_get_ticket_returns_none_for_other_owner(tmp_path):
    db = str(tmp_path / "s.db")
    init_db(db)
    tid = create_ticket(db, "alice", "текст")
    assert get_ticket(db, tid, "bob") is None
    assert get_ticket(db, tid, "alice")["text"] == "текст"
