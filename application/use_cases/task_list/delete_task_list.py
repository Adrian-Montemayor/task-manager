from uuid import UUID

from domain.repositories.task_list.task_list_repository import TaskListRepository


class DeleteTaskList:

    def __init__(self, repository: TaskListRepository):
        self.repository = repository

    def execute(self, task_list_id: UUID) -> bool:
        task_list = self.repository.get_by_id(task_list_id)

        if task_list is None:
            return False

        self.repository.delete(task_list_id)
        return True
