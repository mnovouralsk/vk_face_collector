import logging
import os
from fastapi import FastAPI, UploadFile, File

import errors
from fileManager import FileManager
from logger import Logger
from config import DOWNLOAD_DIR



log = Logger(log_file="logs/my_app.log", log_level=logging.DEBUG)
app = FastAPI()
fm = FileManager(DOWNLOAD_DIR)

UPLOAD_DIR = "uploads"

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...), oid: str = "") -> dict:
    """
    Принимает изображение и сохраняет его на сервер.
    """

    if not file.filename:
        log.warning("Попытка загрузить файл без имени")
        return {"status": "error", "message": errors.FILE_NOT_PROVIDED}

    if not oid:
        log.warning("OID не указан")
        return {"status": "error", "message": errors.OID_NOT_PROVIDED}

    try:
        file_bytes: bytes = await file.read()
        ext = os.path.splitext(file.filename)[1]  # .jpg, .png и т.д.
        saved_filename = f"{oid}{ext}"

        saved_path: str = fm.save_image(file_bytes, file.filename)
        if saved_path:
            log.info("Файл успешно сохранён: %s", saved_path)
            return {"status": "success", "path": saved_path}

        log.error("Ошибка при сохранении изображения")
        return {"status": "error", "message": errors.FILE_SAVE_ERROR}

    except Exception as e:
        log.exception("Неожиданная ошибка при загрузке файла: %s", str(e))
        return {"status": "error", "message": errors.INTERNAL_SERVER_ERROR}