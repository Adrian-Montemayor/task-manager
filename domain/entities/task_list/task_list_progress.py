from pydantic import BaseModel

from domain.entities.task.task import Task
from domain.enums.task_status import TaskStatus


class TaskListProgress(BaseModel):
    tasks: list[Task]
    completed_percentage: float

    @classmethod
    def from_tasks(cls, tasks: list[Task]) -> "TaskListProgress":
        total = len(tasks)

        if total == 0:
            return cls(tasks=[], completed_percentage=0.0)

        completed = sum(1 for task in tasks if task.status == TaskStatus.COMPLETED)

        return cls(
            tasks=tasks,
            completed_percentage=round((completed / total) * 100, 2),
        )
