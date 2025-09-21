from database import Database
from vk_client import VKClient
from downloader import Downloader

from config import DB_PATH


def main():
    db = Database(DB_PATH)
    vk = VKClient()
    dl = Downloader(db)

    # Пример: поиск пользователей по городу (id 1 = Москва)
    users = vk.get_users_by_city(city_id=1, count=5)

    for user in users:
        user_id = user["id"]
        print(f"\n=== Пользователь {user_id} ===")

        photos = vk.get_photos(owner_id=user_id, count=10)
        for photo in photos:
            dl.download_photo(user_id, photo)


if __name__ == "__main__":
    main()
