from datetime import datetime
from uuid import uuid4

import pytest

from domain.entities.task.task import Task
from domain.entities.task_list.task_list_progress import TaskListProgress
from domain.enums.task_priority import TaskPriority
from domain.enums.task_status import TaskStatus


def build_task(status: TaskStatus) -> Task:
    now = datetime(2026, 1, 1)

    return Task(
        id=uuid4(),
        list_id=uuid4(),
        title="Test task",
        description=None,
        status=status,
        priority=TaskPriority.MEDIUM,
        created_at=now,
        updated_at=now,
    )


@pytest.mark.parametrize(
    ("statuses", "expected"),
    [
        ([], 0.0),
        ([TaskStatus.TODO], 0.0),
        ([TaskStatus.COMPLETED], 100.0),
        ([TaskStatus.COMPLETED, TaskStatus.TODO], 50.0),
        ([TaskStatus.COMPLETED, TaskStatus.TODO, TaskStatus.IN_PROGRESS], 33.33),
        (
            [TaskStatus.COMPLETED, TaskStatus.COMPLETED, TaskStatus.TODO],
            66.67,
        ),
        (
            [
                TaskStatus.COMPLETED,
                TaskStatus.COMPLETED,
                TaskStatus.COMPLETED,
                TaskStatus.TODO,
            ],
            75.0,
        ),
    ],
)
def test_completed_percentage(statuses, expected):
    progress = TaskListProgress.from_tasks([build_task(status) for status in statuses])

    assert progress.completed_percentage == expected


def test_from_tasks_keeps_the_tasks():
    tasks = [build_task(TaskStatus.COMPLETED), build_task(TaskStatus.TODO)]

    progress = TaskListProgress.from_tasks(tasks)

    assert progress.tasks == tasks


def test_empty_list_does_not_raise_zero_division():
    progress = TaskListProgress.from_tasks([])

    assert progress.tasks == []
    assert progress.completed_percentage == 0.0
