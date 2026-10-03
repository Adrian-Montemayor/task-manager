from uuid import UUID

from domain.entities.task_list.task_list_progress import TaskListProgress
from domain.enums.task_status import TaskStatus
from domain.enums.task_priority import TaskPriority
from domain.repositories.task.task_repository import TaskRepository


class ListTasks:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(
        self,
        list_id: UUID,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
    ) -> TaskListProgress:
        tasks = self.repository.get_by_list(
            list_id=list_id,
            status=status,
            priority=priority,
        )

        return TaskListProgress.from_tasks(tasks)
