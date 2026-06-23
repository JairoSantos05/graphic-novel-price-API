import sqlite3
import os

# Dynamically locate file's folder directory on the server
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Absolute path directly to SQLite database file local copy
DBPath = os.path.join(BASE_DIR, "graphic_novels.db")

def connection():
    conn = sqlite3.connect(DBPath)

    #Configures database rows to be returned as dictionary like row objects so we
    #can read columns by their name strings (row["price"]) instead of raw number indexes.
    conn.row_factory = sqlite3.Row
    return conn