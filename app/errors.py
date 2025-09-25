# errors.py
from enum import Enum
from typing import TypedDict

class ErrorInfo(TypedDict):
    code: int
    message: str

class ErrorCode(str, Enum):
    FILE_NOT_PROVIDED = "FILE_NOT_PROVIDED"
    FILE_SAVE_ERROR = "FILE_SAVE_ERROR"
    OID_NOT_PROVIDED = "OID_NOT_PROVIDED"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"

# Словарь ошибок с кодом и сообщением
ERRORS: dict[ErrorCode, ErrorInfo] = {
    ErrorCode.FILE_NOT_PROVIDED: {"code": 1001, "message": "Файл не указан"},
    ErrorCode.FILE_SAVE_ERROR: {"code": 1002, "message": "Ошибка сохранения файла"},
    ErrorCode.OID_NOT_PROVIDED: {"code": 1003, "message": "OID не указан"},
    ErrorCode.INTERNAL_SERVER_ERROR: {"code": 1004, "message": "Внутренняя ошибка сервера"},
    ErrorCode.UNKNOWN_ERROR: {"code": 1005, "message": "Неизвестная ошибка"},
}

# Пример функции для быстрого получения ошибки
def get_error(code: ErrorCode) -> ErrorInfo:
    return ERRORS.get(code, ERRORS[ErrorCode.UNKNOWN_ERROR])
