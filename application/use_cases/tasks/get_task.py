from uuid import UUID

from domain.entities.task.task import Task
from domain.repositories.task.task_repository import TaskRepository


class GetTask:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, task_id: UUID) -> Task | None:
        return self.repository.get_by_id(task_id)
