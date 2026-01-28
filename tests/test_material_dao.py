from database.material_dao import MaterialDAO

def test_insert_and_fetch_material(db, monkeypatch):
    monkeypatch.setattr("database.material_dao.sqlite3.connect", lambda _: db)

    cur = db.cursor()
    cur.execute("INSERT INTO categories (name) VALUES ('Backend')")
    cat_id = cur.lastrowid
    db.commit()

    dao = MaterialDAO()
    dao.insert({
        "title": "Clean Code",
        "author": "Robert Martin",
        "type": "Livro",
        "progress": 50,
        "category_id": cat_id
    })

    mats = dao.fetch_all()
    assert len(mats) == 1
    assert mats[0]["category"] == "Backend"