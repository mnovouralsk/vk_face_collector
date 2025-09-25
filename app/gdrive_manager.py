import os
import logging
from typing import Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
import io

class GDriveManager:
    """
    Модуль для работы с Google Drive:
    - загрузка файлов
    - хранение файлов в указанной папке
    """

    def __init__(self, credentials_json: str, folder_id: str, logger: Optional[logging.Logger] = None):
        """
        :param credentials_json: путь к JSON-файлу с сервисным аккаунтом Google
        :param folder_id: ID папки на Google Drive, куда будут загружаться файлы
        """
        self.folder_id = folder_id
        self.logger = logger or logging.getLogger(__name__)
        self.service = self._authenticate(credentials_json)

    def _authenticate(self, credentials_json: str):
        try:
            creds = service_account.Credentials.from_service_account_file(
                credentials_json,
                scopes=["https://www.googleapis.com/auth/drive.file"]
            )
            service = build("drive", "v3", credentials=creds)
            self.logger.info("Успешно аутентифицирован в Google Drive")
            return service
        except Exception as e:
            self.logger.exception("Ошибка аутентификации Google Drive: %s", str(e))
            raise

    def upload_file(self, file_bytes: bytes, filename: str, mime_type: str = "image/jpeg") -> str | None:
        """
        Загружает файл на Google Drive в указанную папку.
        :param file_bytes: содержимое файла
        :param filename: имя файла на Drive
        :param mime_type: MIME тип (по умолчанию image/jpeg)
        :return: ID загруженного файла или None при ошибке
        """
        try:
            file_metadata = {
                "name": filename,
                "parents": [self.folder_id]
            }
            media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype=mime_type)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id"
            ).execute()

            file_id = file.get("id")
            self.logger.info("Файл %s успешно загружен на Google Drive (ID: %s)", filename, file_id)
            return file_id
        except Exception as e:
            self.logger.exception("Ошибка при загрузке файла %s на Google Drive: %s", filename, str(e))
            return None


    def download_file(self, file_id: str, save_path: str) -> bool:
        """
        Скачивает файл с Google Drive.
        :param file_id: ID файла на Google Drive
        :param save_path: Локальный путь для сохранения
        :return: True если скачано успешно, иначе False
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            fh = io.FileIO(save_path, "wb")
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                self.logger.debug("Скачано %.2f%%", (status.progress() * 100))

            self.logger.info("Файл успешно скачан: %s", save_path)
            return True
        except Exception as e:
            self.logger.exception("Ошибка при скачивании файла %s: %s", file_id, str(e))
            return False