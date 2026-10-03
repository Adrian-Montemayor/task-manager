from datetime import datetime
from uuid import UUID

from domain.entities.task.task import Task
from domain.enums.task_status import TaskStatus
from domain.repositories.task.task_repository import TaskRepository


class UpdateTaskStatus:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(
        self,
        task_id: UUID,
        status: TaskStatus,
    ) -> Task | None:
        task = self.repository.get_by_id(task_id)

        if task is None:
            return None

        task.status = status
        task.updated_at = datetime.utcnow()

        return self.repository.update(task)
