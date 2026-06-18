import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DBPath = os.path.join(BASE_DIR, "graphic_novels.db")

def connection():
    conn = sqlite3.connect(DBPath)
    conn.row_factory = sqlite3.Row
    return conn