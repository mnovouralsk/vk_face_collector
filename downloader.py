import os
import requests
from database import Database
from typing import Dict
from config import DOWNLOAD_DIR


class Downloader:
    """Скачивание фото и сохранение в базу."""

    def __init__(self, db: Database):
        self.db = db
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    def download_photo(self, user_id: int, photo: Dict) -> None:
        photo_id = photo["id"]
        sizes = photo.get("sizes", [])
        if not sizes:
            return

        # Берём самое большое фото
        best = max(sizes, key=lambda s: s["width"] * s["height"])
        url = best["url"]

        if self.db.photo_exists(user_id, photo_id):
            return  # уже скачано

        file_path = os.path.join(DOWNLOAD_DIR, f"{user_id}_{photo_id}.jpg")

        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(resp.content)
            self.db.add_photo(user_id, photo_id, url, file_path)
            print(f"✅ Скачано: {file_path}")
        except Exception as e:
            print(f"❌ Ошибка скачивания {url}: {e}")
