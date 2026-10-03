from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from domain.enums.task_priority import TaskPriority
from domain.enums.task_status import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    priority: TaskPriority


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus
    priority: TaskPriority


class TaskResponse(BaseModel):
    id: UUID
    list_id: UUID
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime


class TaskListTasksResponse(BaseModel):
    tasks: list[TaskResponse]
    completed_percentage: float


class TaskStatusUpdate(BaseModel):
    status: TaskStatus
