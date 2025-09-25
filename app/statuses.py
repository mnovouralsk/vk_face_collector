from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ERROR = "error"

class FileStatus(str, Enum):
    UPLOADED = "file_uploaded"
    FAILED = "file_failed"