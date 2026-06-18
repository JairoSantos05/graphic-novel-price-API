import sqlite3
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

_raw_test_db = sqlite3.connect(":memory:", check_same_thread=False)
_raw_test_db.row_factory = sqlite3.Row

class SafeTestConnection:
    def cursor(self):
        return _raw_test_db.cursor()
    def commit(self):
        return _raw_test_db.commit()
    def close(self):
        pass

test_db = SafeTestConnection()

def init_test_db():
    cursor = _raw_test_db.cursor()
    cursor.execute("DROP TABLE IF EXISTS Prices")
    cursor.execute("DROP TABLE IF EXISTS graphic_novels")
    
    cursor.execute("""
        CREATE TABLE graphic_novels (
            isbn INTEGER PRIMARY KEY,
            title TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE Prices (
            date TEXT,
            retailer TEXT,
            price REAL,
            isbn INTEGER,
            url TEXT
        )
    """)
    
    cursor.execute("INSERT INTO graphic_novels VALUES (123456, 'Batman: Year One')")
    cursor.execute("INSERT INTO graphic_novels VALUES (789012, 'Watchmen')")
    cursor.execute("INSERT INTO graphic_novels VALUES (999999, 'Spiderman')")
    cursor.execute("INSERT INTO graphic_novels VALUES (888888, 'Sandman')")
    
    cursor.execute("INSERT INTO Prices VALUES ('2026-06-11', 'Store A', 19.99, 123456, 'http://storea.com')")
    cursor.execute("INSERT INTO Prices VALUES ('2026-06-12', 'Store A', 17.99, 123456, 'http://storea.com')")
    cursor.execute("INSERT INTO Prices VALUES ('2026-06-12', 'Store B', 15.50, 123456, 'http://storeb.com')")
    cursor.execute("INSERT INTO Prices VALUES ('2026-06-12', 'Store A', 29.99, 789012, 'http://storea.com')")
    cursor.execute("INSERT INTO Prices VALUES ('2026-06-12', 'Store C', 0.00, 999999, 'http://storec.com')")
    cursor.execute("INSERT INTO Prices VALUES ('2026-06-12', 'Store D', NULL, 888888, 'http://stored.com')")
    
    _raw_test_db.commit()

init_test_db()

with patch("db.connection", return_value=test_db):
    from api import app
    client = TestClient(app)

# Price tests
def test_prices_functionality():
    with patch("dbqueries.connection", return_value=test_db):
        response = client.get("/book/123456/prices")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["title"] == "Batman: Year One"

def test_prices_boundary_extreme_isbn():
    with patch("dbqueries.connection", return_value=test_db):
        response = client.get("/book/9781234567890/prices")
        assert response.status_code == 200
        assert len(response.json()) == 0

def test_prices_error_handling_missing_data():
    with patch("dbqueries.connection", return_value=test_db):
        response = client.get("/book/888888/prices")
        assert response.status_code == 200
        assert len(response.json()) == 0

# Deals tests
def test_deals_functionality():
    with patch("dbqueries.connection", return_value=test_db):
        response = client.get("/deals?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

def test_deals_boundary_limits():
    with patch("dbqueries.connection", return_value=test_db):
        response = client.get("/deals?limit=0")
        assert response.status_code == 200
        assert len(response.json()) == 0

def test_deals_error_handling_validation():
    response = client.get("/deals?limit=not-an-integer")
    assert response.status_code == 422

# History tests
def test_history_functionality():
    with patch("dbqueries.connection", return_value=test_db):
        response = client.get("/book/123456/history")
        assert response.status_code == 200
        data = response.json()
        assert data["isbn"] == 123456
        assert len(data["history"]) >= 2 

def test_history_boundary_empty():
    with patch("dbqueries.connection", return_value=test_db):
        response = client.get("/book/111111/history")
        assert response.status_code == 200
        data = response.json()
        assert len(data["history"]) == 0

def test_history_error_handling_type():
    response = client.get("/book/invalid-string-isbn/history")
    assert response.status_code == 422
