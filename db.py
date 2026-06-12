import sqlite3
import os

DBPath = os.getenv("DATABASE_URL", "graphic_novels.db")
def connection(db_path = None):
    return sqlite3.connect(db_path or DBPath)