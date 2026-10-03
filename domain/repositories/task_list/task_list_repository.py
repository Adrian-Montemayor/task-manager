from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.task_list.task_list import TaskList


class TaskListRepository(ABC):

    @abstractmethod
    def create(self, task_list: TaskList) -> TaskList:
        pass

    @abstractmethod
    def get_by_id(self, task_list_id: UUID) -> TaskList | None:
        pass

    @abstractmethod
    def update(self, task_list: TaskList) -> TaskList:
        pass

    @abstractmethod
    def delete(self, task_list_id: UUID) -> None:
        pass
