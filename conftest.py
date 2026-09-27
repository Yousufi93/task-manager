import pytest
import sqlite3
import database

@pytest.fixture(autouse=True)
def use_temp_databse(tmp_path, monkeypatch):
    """قبلا از هر تست اجرا میشود این صال استفاده در tasks.db یک دیتابس موقت می سازد و به جای دتابس اصذل کلار اخام میدهدذ"""
    temp_db = tmp_path / "test.db"
    def get_temp_connection():
        return sqlite3.connect(temp_db)

    #جاگزین تابع اتصال با نسخه موقت
    monkeypatch.setattr(database, "get_connection", get_temp_connection)
    database.create_table()
    yield