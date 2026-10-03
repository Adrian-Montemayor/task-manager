from datetime import datetime
from uuid import UUID

from domain.entities.task.task import Task
from domain.enums.task_priority import TaskPriority
from domain.enums.task_status import TaskStatus
from domain.repositories.task.task_repository import TaskRepository


class UpdateTask:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(
        self,
        task_id: UUID,
        title: str,
        description: str | None,
        status: TaskStatus,
        priority: TaskPriority,
    ) -> Task | None:
        task = self.repository.get_by_id(task_id)

        if task is None:
            return None

        task.title = title
        task.description = description
        task.status = status
        task.priority = priority
        task.updated_at = datetime.utcnow()

        return self.repository.update(task)
