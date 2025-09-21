import os
from database import Database
from vk_client import VKClient
from downloader import Downloader

from config import DB_PATH, ACCESS_TOKEN, USERS_FILE

def get_user_ids_from_group(group_ids, vk):
    """
    Получает уникальные ID пользователей из указанных групп ВКонтакте.

    :param group_ids: Список идентификаторов групп ВКонтакте.
    :param vk: Экземпляр класса VKApi для работы с API ВКонтакте.
    :return: Список уникальных ID пользователей.
    """
    user_ids = set()  # Используем множество для автоматического удаления дубликатов
    for group in group_ids:
        try:
            group_user_ids = vk.get_users_groupVK(group)
            if group_user_ids is not None:
                user_ids.update(group_user_ids)
            else:
                print(f"Не удалось получить пользователей из группы {group}: пустой ответ от API.")
        except Exception as e:
            print(f"Ошибка при получении пользователей из группы {group}: {e}")
    return list(user_ids)

def merge_unique(list1, list2):
    """
    Объединяет два списка с исключением дубликатов.

    :param list1: Первый список элементов.
    :param list2: Второй список элементов.
    :return: Объединённый список уникальных элементов.
    """
    # Используем объединение множеств для получения уникальных элементов
    return list(set(list1) | set(list2))

def main():
    """
    Основная функция для получения ID пользователей из групп ВКонтакте и сохранения их в файл.
    Обновляет файл `users_file` новыми ID пользователей, исключая дубликаты.
    """
    print('Обновление USERS_IDS.txt...')
    try:
        vk = VKClient(ACCESS_TOKEN)

        # Проверяем существование файла, создаём новый, если отсутствует
        if not os.path.exists(USERS_FILE):
            print(f"Файл {USERS_FILE} не найден. Создаю новый файл.")
            FileManager.save_data_to_file(USERS_FILE, [])

        # Получаем новые ID пользователей из групп
        new_user_ids = get_user_ids_from_group(group_ids, vk)

        # Читаем предыдущие ID пользователей из файла
        prev_user_ids = FileManager.read_data_from_file(users_file)

        # Если чтение файла вернуло None, инициализируем пустой список
        if prev_user_ids is None:
            prev_user_ids = []

        # Объединяем новые и предыдущие ID, удаляя дубликаты
        user_ids = merge_unique(new_user_ids, prev_user_ids)

        print(f'Новых пользователей: {len(user_ids) - len(prev_user_ids)}')
        print(f'Всего пользователей: {len(user_ids)}')

        # Очищаем файл и сохраняем обновленный список ID пользователей
        FileManager.clear_file(users_file)
        FileManager.save_data_to_file(users_file, user_ids)

    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == '__main__':
    main()

# def main():
#     db = Database(DB_PATH)
#     vk = VKClient()
#     dl = Downloader(db)

#     # Пример: поиск пользователей по городу (id 1 = Москва)
#     users = vk.get_users_by_city(city_id=1, count=5)

#     for user in users:
#         user_id = user["id"]
#         print(f"\n=== Пользователь {user_id} ===")

#         photos = vk.get_photos(owner_id=user_id, count=10)
#         for photo in photos:
#             dl.download_photo(user_id, photo)


# if __name__ == "__main__":
#     main()
