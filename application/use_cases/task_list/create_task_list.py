from uuid import uuid4
from datetime import datetime

from domain.entities.task_list.task_list import TaskList
from domain.repositories.task_list.task_list_repository import TaskListRepository


class CreateTaskList:

    def __init__(self, repository: TaskListRepository):
        self.repository = repository

    def execute(self, name: str) -> TaskList:
        now = datetime.utcnow()

        task_list = TaskList(
            id=uuid4(),
            name=name,
            created_at=now,
            updated_at=now,
        )

        return self.repository.create(task_list)
