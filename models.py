from pydantic import BaseModel, HttpUrl

class TaskRequest(BaseModel):
    job_id: str
    user_id: int
    photo_url: HttpUrl
    metadata: dict | None

class TaskResponse(BaseModel):
    job_id: str
    status: str
    message: str | None
