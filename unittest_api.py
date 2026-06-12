import sqlite3
from unittest.mock import patch
from fastapi.testclient import TestClient

test_db = sqlite3.connect(":memory:", check_same_thread=False)

def init_test_db():
    cursor = test_db.cursor()
    cursor.execute("DROP TABLE IF EXISTS Prices")
    cursor.execute("""
        CREATE TABLE Prices (
            date TEXT,
            retailer TEXT,
            price REAL,
            isbn INTEGER
        )
    """)
    cursor.execute("INSERT INTO Prices (date, retailer, price, isbn) VALUES ('2026-06-11', 'Store A', 19.99, 123456)")
    cursor.execute("INSERT INTO Prices (date, retailer, price, isbn) VALUES ('2026-06-12', 'Store A', 17.99, 123456)")
    test_db.commit()

init_test_db()

with patch("db.connection", return_value=test_db):
    from api import app
    client = TestClient(app)

def test_get_book_history():
    with patch("dbqueries.connection", return_value=test_db):
        response = client.get("/book/123456/history")
        
        assert response.status_code == 200
        data = response.json()
        assert data["isbn"] == 123456
        assert len(data["history"]) == 2