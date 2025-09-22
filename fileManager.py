import errno
import logging
import io
from pathlib import Path
from PIL import Image

from logger import Logger

class FileManager:
    log = Logger(log_file="logs/my_app.log", log_level=logging.DEBUG)

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(FileManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, base_dir="."):
        self.base_dir = base_dir

    def create_file(
            self,
            path: str,
            name: str,
            extension: str,
            content: str | None,
            create_only_dir: bool = False
        ) -> str | None:
        """
        Создаёт файл с заданным расширением и обрабатывает исключения.

        :param path: Путь до папки (будет создана, если её нет).
        :param name: Имя файла без расширения.
        :param extension: Расширение файла (например, 'txt', 'db', 'json').
        :param content: Текст для записи в файл (по умолчанию None = пустой файл).
        :return: Полный путь к файлу или None при ошибке.
        """
        try:
            Path(path).mkdir(parents=True, exist_ok=True)

            if create_only_dir:
                self.log.info(f"✅ Папка создана: {path}")
                return str(Path(path))

            file_path = Path(path) / f"{name}.{extension}"

            if not file_path.exists():
                with open(file_path, "w", encoding="utf-8") as f:
                    if content:
                        f.write(content)
                self.log.info(f"✅ Файл создан: {file_path}")
            else:
                self.log.error(f"ℹ️ Файл уже существует: {file_path}")

            return str(file_path)

        except PermissionError:
            self.log.exception("❌ Ошибка: нет прав на запись в каталог.")
        except FileNotFoundError:
            self.log.exception("❌ Ошибка: указан некорректный путь.")
        except FileExistsError:
            self.log.exception("❌ Ошибка: файл с таким именем уже существует (режим 'x').")
        except IsADirectoryError:
            self.log.exception("❌ Ошибка: по указанному пути существует папка, а не файл.")
        except BlockingIOError:
            self.log.exception("❌ Ошибка: файл занят другой программой.")
        except OSError as e:
            if e.errno == errno.ENOSPC:
                self.log.exception("❌ Ошибка: файловая система переполнена.")
            else:
                self.log.exception(f"❌ Ошибка ОС: {e}")
        except Exception as e:
            self.log.exception(f"❌ Непредвиденная ошибка: {e}")

        return None

        # Пимер использования

        # fm = FileManager()

        # # Создать папку
        # fm.create_file("data", "", "", create_only_dir=True)

        # # Создать пустой файл
        # fm.create_file("data", "empty_file", "txt")

        # # Создать файл с текстом
        # fm.create_file("data", "hello", "txt", content="Привет, мир!")

        # # Создать файл из списка
        # lines = ["Первый элемент", "Второй элемент", "Третий элемент"]
        # fm.create_file("data", "list_file", "txt", content="\n".join(lines))


    def save_image(self, file_bytes: bytes, filename: str) -> str | None:
        """
        Сохраняет изображение в папку base_dir.

        :param file_bytes: Содержимое файла в байтах
        :param filename: Имя файла с расширением
        :return: Полный путь к сохраненному файлу или None при ошибке
        """
        try:
            # Проверяем, можно ли открыть изображение через PIL
            image = Image.open(io.BytesIO(file_bytes))
            image.verify()  # проверка корректности

            # Создаём путь к файлу
            file_path = f'{self.base_dir} / {filename}'

            # Сохраняем файл
            with open(file_path, "wb") as f:
                f.write(file_bytes)

            return str(file_path)
        except Exception as e:
            print(f"Ошибка при сохранении изображения: {e}")
            return None