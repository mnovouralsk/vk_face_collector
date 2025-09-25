import redis
import json
from typing import Any

from config import REDIS_URL
from app.logger import Logger

log = Logger()

class TaskQueue:
    """
    Работа с очередью задач для Face Processor с поддержкой приоритетов.
    Используем Redis Sorted Set для хранения задач.
    """

    QUEUE_KEY = "face_tasks"

    def __init__(self, redis_url: str = REDIS_URL):
        try:
            self.redis = redis.Redis.from_url(redis_url)
            self.redis.ping()
            log.info("Успешно подключились к Redis")
        except redis.RedisError as e:
            log.exception("Ошибка подключения к Redis: %s", str(e))

    def enqueue_task(self, task: dict[str, Any]) -> str | None:
        """
        Добавляет задачу в очередь с учётом приоритета.

        :param task: Словарь с данными задачи, должен содержать 'priority' (int)
        :return: job_id задачи или None при ошибке
        """
        try:
            task_serialized = json.dumps(task)
            score = task.get("priority", 0)  # по умолчанию 0
            self.redis.zadd(self.QUEUE_KEY, {task_serialized: score})
            log.info("Задача добавлена с приоритетом %s: %s", score, task.get("job_id"))
            return task.get("job_id")
        except redis.RedisError as e:
            log.exception("Ошибка при добавлении задачи в очередь: %s", str(e))
            return None
        except Exception as e:
            log.exception("Неожиданная ошибка при добавлении задачи: %s", str(e))
            return None

    def dequeue_task(self) -> dict | None:
        """
        Получает задачу с наивысшим приоритетом и удаляет её из очереди.

        :return: Словарь задачи или None, если очередь пуста
        """
        try:
            tasks = self.redis.zrevrange(self.QUEUE_KEY, 0, 0)
            if not tasks:
                return None
            task_serialized = tasks[0]
            # удаляем задачу из очереди
            self.redis.zrem(self.QUEUE_KEY, task_serialized)
            task = json.loads(task_serialized)
            log.info("Задача извлечена: %s", task.get("job_id"))
            return task
        except redis.RedisError as e:
            log.exception("Ошибка при получении задачи из очереди: %s", str(e))
            return None
        except Exception as e:
            log.exception("Неожиданная ошибка при получении задачи: %s", str(e))
            return None

    def queue_length(self) -> int:
        """
        Возвращает количество задач в очереди.
        """
        try:
            length = self.redis.zcard(self.QUEUE_KEY)
            return length
        except Exception as e:
            log.exception("Ошибка при получении длины очереди: %s", str(e))
            return 0