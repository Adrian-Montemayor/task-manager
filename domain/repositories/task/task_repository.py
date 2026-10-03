from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.task.task import Task
from domain.enums.task_priority import TaskPriority
from domain.enums.task_status import TaskStatus


class TaskRepository(ABC):

    @abstractmethod
    def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    def get_by_id(self, task_id: UUID) -> Task | None:
        pass

    @abstractmethod
    def update(self, task: Task) -> Task:
        pass

    @abstractmethod
    def delete(self, task_id: UUID) -> None:
        pass

    @abstractmethod
    def get_by_list(
        self,
        list_id: UUID,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
    ) -> list[Task]:
        pass
