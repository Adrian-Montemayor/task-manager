from datetime import datetime
from uuid import UUID

from domain.entities.task_list.task_list import TaskList
from domain.repositories.task_list.task_list_repository import TaskListRepository


class UpdateTaskList:

    def __init__(self, repository: TaskListRepository):
        self.repository = repository

    def execute(
        self,
        task_list_id: UUID,
        name: str,
    ) -> TaskList | None:
        task_list = self.repository.get_by_id(task_list_id)

        if task_list is None:
            return None

        task_list.name = name
        task_list.updated_at = datetime.utcnow()

        return self.repository.update(task_list)
