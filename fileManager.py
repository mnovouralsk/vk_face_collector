from pathlib import Path
from typing import Optional
import errno

class FileManager:


    def create_file(
            path: str,
            name: str,
            extension: str,
            content: Optional[str] = None,
            create_only_dir: bool = False
        ) -> Optional[str]:
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
                print(f"✅ Папка создана: {path}")
                return str(Path(path))

            file_path = Path(path) / f"{name}.{extension}"

            if not file_path.exists():
                with open(file_path, "w", encoding="utf-8") as f:
                    if content:
                        f.write(content)
                print(f"✅ Файл создан: {file_path}")
            else:
                print(f"ℹ️ Файл уже существует: {file_path}")

            return str(file_path)

        except PermissionError:
            print("❌ Ошибка: нет прав на запись в каталог.")
        except FileNotFoundError:
            print("❌ Ошибка: указан некорректный путь.")
        except FileExistsError:
            print("❌ Ошибка: файл с таким именем уже существует (режим 'x').")
        except IsADirectoryError:
            print("❌ Ошибка: по указанному пути существует папка, а не файл.")
        except BlockingIOError:
            print("❌ Ошибка: файл занят другой программой.")
        except OSError as e:
            if e.errno == errno.ENOSPC:
                print("❌ Ошибка: файловая система переполнена.")
            else:
                print(f"❌ Ошибка ОС: {e}")
        except Exception as e:
            print(f"❌ Непредвиденная ошибка: {e}")

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