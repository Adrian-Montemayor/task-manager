from datetime import datetime
from uuid import UUID, uuid4

from domain.entities.task.task import Task
from domain.enums.task_priority import TaskPriority
from domain.enums.task_status import TaskStatus
from domain.repositories.task.task_repository import TaskRepository


class CreateTask:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(
        self,
        list_id: UUID,
        title: str,
        description: str | None,
        priority: TaskPriority,
    ) -> Task:
        now = datetime.utcnow()

        task = Task(
            id=uuid4(),
            list_id=list_id,
            title=title,
            description=description,
            status=TaskStatus.TODO,
            priority=priority,
            created_at=now,
            updated_at=now,
        )

        return self.repository.create(task)
