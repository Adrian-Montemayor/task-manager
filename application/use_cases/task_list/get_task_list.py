from uuid import UUID

from domain.entities.task_list.task_list import TaskList
from domain.repositories.task_list.task_list_repository import TaskListRepository


class GetTaskList:

    def __init__(self, repository: TaskListRepository):
        self.repository = repository

    def execute(self, task_list_id: UUID) -> TaskList | None:
        return self.repository.get_by_id(task_list_id)
