import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

DATABASE_DIR = ROOT_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True)

DB_PATH = DATABASE_DIR / "chatbot.db"

conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False,
)

conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON")