from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from domain.enums.task_priority import TaskPriority
from domain.enums.task_status import TaskStatus


class Task(BaseModel):
    id: UUID
    list_id: UUID
    title: str
    description: str | None = None
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime
