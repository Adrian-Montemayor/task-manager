from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Uuid

from infrastructure.database.models.base import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Uuid, primary_key=True, default=uuid4)

    list_id = Column(
        Uuid,
        ForeignKey("task_lists.id"),
        nullable=False,
    )

    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(String(50), nullable=False)
    priority = Column(String(50), nullable=False)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
