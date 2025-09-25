from pydantic import BaseModel
from app.statuses import TaskStatus

class TaskRequest(BaseModel):
    job_id: str          # уникальный идентификатор задачи
    user_id: int         # id пользователя
    photo_id: str        # ID файла на Google Drive
    metadata: dict | None = None  # дополнительная информация
    priority: int = 0  # чем выше число, тем выше приоритет 0 - 10

class TaskResponse(BaseModel):
    job_id: str
    status: TaskStatus
    message: str | None = None