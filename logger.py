import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class Logger:
    """
    Класс для централизованного логирования.
    Поддерживает консоль и файл с ротацией логов.
    """

    _instance = None  # синглтон

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        log_file: Optional[str] = "logs/app.log",
        log_level: int = logging.INFO,
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 3
    ):
        """
        Инициализация логгера.

        :param log_file: Путь к файлу логов.
        :param log_level: Уровень логирования (INFO, DEBUG, WARNING, ERROR).
        :param max_bytes: Максимальный размер файла перед ротацией.
        :param backup_count: Количество ротационных файлов для хранения.
        """
        if hasattr(self, "_initialized") and self._initialized:
            return  # чтобы __init__ не переинициализировался у синглтона

        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(log_level)
        self.logger.propagate = False

        # Создаём каталог для логов
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            # Ротация файлов логов
            file_handler = RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
            )
            file_formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

        # Консольный вывод
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            "[%(levelname)s] %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        self._initialized = True

    # Удобные методы
    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def exception(self, message: str):
        """Логирование исключения с traceback"""
        self.logger.exception(message)
