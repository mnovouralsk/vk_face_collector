import logging
import os
from fastapi import FastAPI, UploadFile, File

from app.errors import ErrorCode, get_error, ERRORS
from fileManager import FileManager
from app.logger import Logger
from config import DOWNLOAD_DIR
from app.models import TaskRequest, TaskResponse
from app.task_queue import TaskQueue
from app.statuses import TaskStatus



log = Logger(log_file="logs/my_app.log", log_level=logging.DEBUG)
app = FastAPI()
fm = FileManager(DOWNLOAD_DIR)
queue = TaskQueue()

UPLOAD_DIR = "uploads"

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...), oid: str = "") -> dict:
    """
    Принимает изображение и сохраняет его на сервер.
    """

    if not file.filename:
        err = get_error(ErrorCode.FILE_NOT_PROVIDED)
        log.warning("Попытка загрузить файл без имени: %s", err["message"])
        return {"status": "error", "error": err}

    if not oid:
        err = get_error(ErrorCode.OID_NOT_PROVIDED)
        log.warning("OID не передан: %s", err["message"])
        return {"status": "error", "error": err}

    try:
        file_bytes: bytes = await file.read()
        ext = os.path.splitext(file.filename)[1]  # .jpg, .png и т.д.
        saved_filename = f"{oid}{ext}"

        saved_path: str = fm.save_image(file_bytes, file.filename)
        if saved_path:
            log.info("Файл успешно сохранён: %s", saved_path)
            return {"status": "success", "path": saved_path}

        err = get_error(ErrorCode.FILE_SAVE_ERROR)
        log.error("Ошибка при сохранении изображения: %s", err["message"])
        return {"status": "error", "error": err}

    except Exception as e:
        err = get_error(ErrorCode.INTERNAL_SERVER_ERROR)
        log.exception("Неожиданная ошибка при загрузке файла: %s", str(e))
        return {"status": "error", "error": err}



@app.post("/submit-task", response_model=TaskResponse)
async def submit_task(task: TaskRequest):
    """
    Получает задачу от бота и ставит её в очередь
    """
    task_dict = task.dict()
    task_redis_id = queue.enqueue_task(task_dict)

    if not task_redis_id:
        return TaskResponse(
            job_id=task.job_id,
            status=TaskStatus.ERROR,
            message="Не удалось поставить задачу в очередь"
        )

    return TaskResponse(
        job_id=task.job_id,
        status=TaskStatus.PENDING,
        message=None
    )