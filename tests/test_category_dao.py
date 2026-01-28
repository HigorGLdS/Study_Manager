from database.category_dao import CategoryDAO

def test_insert_and_fetch_categories(db, monkeypatch):
    monkeypatch.setattr("database.category_dao.sqlite3.connect", lambda _: db)

    dao = CategoryDAO()
    dao.insert("Backend")
    dao.insert("Frontend")

    cats = dao.fetch_all()
    names = [c["name"] for c in cats]

    assert "Backend" in names
    assert "Frontend" in names