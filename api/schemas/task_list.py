from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TaskListCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class TaskListUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class TaskListResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
