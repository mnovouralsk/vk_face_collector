import os
import sqlite3
from typing import Optional, Tuple


class Database:
    """Класс для работы с SQLite."""

    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self) -> None:
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS photos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    photo_id INTEGER,
                    url TEXT,
                    file_path TEXT,
                    embedding BLOB,  -- эмбеддинг лица
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, photo_id)
                )
            """)

    def add_photo(self, user_id: int, photo_id: int, url: str, file_path: str, embedding: Optional[bytes] = None) -> None:
        """Добавляет фото с эмбеддингом."""
        with self.conn:
            self.conn.execute("""
                INSERT OR IGNORE INTO photos (user_id, photo_id, url, file_path, embedding)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, photo_id, url, file_path, embedding))


    def add_photo(self, user_id: int, photo_id: int, url: str, file_path: str) -> None:
        """Добавляет фото, если его ещё нет."""
        with self.conn:
            self.conn.execute("""
                INSERT OR IGNORE INTO photos (user_id, photo_id, url, file_path)
                VALUES (?, ?, ?, ?)
            """, (user_id, photo_id, url, file_path))

    def photo_exists(self, user_id: int, photo_id: int) -> bool:
        """Проверяет, есть ли фото в базе."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT 1 FROM photos WHERE user_id = ? AND photo_id = ?
        """, (user_id, photo_id))
        return cur.fetchone() is not None
