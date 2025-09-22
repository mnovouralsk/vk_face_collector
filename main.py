import logging
from fastapi import FastAPI, UploadFile, File

from fileManager import FileManager
from logger import Logger
from config import DOWNLOAD_DIR


log = Logger(log_file="logs/my_app.log", log_level=logging.DEBUG)
app = FastAPI()
fm = FileManager(DOWNLOAD_DIR)

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)) -> dict:
    """
    Принимает изображение и сохраняет его на сервер.
    """
    uploaded_file: UploadFile = file

    # Проверяем, что файл реально пришёл
    if not uploaded_file.filename:
        log.exception("Не указан файл для загрузки")
        return {"status": "error", "message": "Не указан файл для загрузки"}

    try:
        file_bytes: bytes = await uploaded_file.read()
        saved_path: str | None = fm.save_image(file_bytes, uploaded_file.filename)
        if saved_path:
            return {"status": "success", "path": saved_path}
        else:
            log.error("Не удалось сохранить изображение")
            return {"status": "error", "message": "Не удалось сохранить изображение"}
    except Exception as e:
        return {"status": "error", "message": str(e)}