from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Uuid

from infrastructure.database.models.base import Base


class TaskListModel(Base):
    __tablename__ = "task_lists"

    id = Column(Uuid, primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
