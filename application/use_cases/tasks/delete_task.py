from uuid import UUID

from domain.repositories.task.task_repository import TaskRepository


class DeleteTask:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, task_id: UUID) -> bool:
        task = self.repository.get_by_id(task_id)

        if task is None:
            return False

        self.repository.delete(task_id)
        return True
