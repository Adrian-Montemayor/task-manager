from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.schemas.task import (
    TaskCreate,
    TaskListTasksResponse,
    TaskResponse,
    TaskStatusUpdate,
    TaskUpdate,
)
from application.use_cases.tasks.create_task import CreateTask
from application.use_cases.tasks.delete_task import DeleteTask
from application.use_cases.tasks.get_task import GetTask
from application.use_cases.tasks.list_tasks import ListTasks
from application.use_cases.tasks.update_task import UpdateTask
from application.use_cases.tasks.update_task_status import UpdateTaskStatus
from domain.enums.task_priority import TaskPriority
from domain.enums.task_status import TaskStatus
from infrastructure.database.connection import SessionLocal
from infrastructure.repositories.task.task_repository import DBTaskRepository

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TaskResponse)
def create_task(
    list_id: UUID,
    data: TaskCreate,
    db: Session = Depends(get_db),
):
    repository = DBTaskRepository(db)
    use_case = CreateTask(repository)

    task = use_case.execute(
        list_id=list_id,
        title=data.title,
        description=data.description,
        priority=data.priority,
    )

    return task


@router.get("/list/{list_id}", response_model=TaskListTasksResponse)
def list_tasks(
    list_id: UUID,
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    db: Session = Depends(get_db),
):
    repository = DBTaskRepository(db)
    use_case = ListTasks(repository)

    return use_case.execute(
        list_id=list_id,
        status=status,
        priority=priority,
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    db: Session = Depends(get_db),
):
    repository = DBTaskRepository(db)
    use_case = GetTask(repository)

    task = use_case.execute(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    data: TaskUpdate,
    db: Session = Depends(get_db),
):
    repository = DBTaskRepository(db)
    use_case = UpdateTask(repository)

    task = use_case.execute(
        task_id=task_id,
        title=data.title,
        description=data.description,
        status=data.status,
        priority=data.priority,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_status(
    task_id: UUID,
    data: TaskStatusUpdate,
    db: Session = Depends(get_db),
):
    repository = DBTaskRepository(db)
    use_case = UpdateTaskStatus(repository)

    task = use_case.execute(
        task_id=task_id,
        status=data.status,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: UUID,
    db: Session = Depends(get_db),
):
    repository = DBTaskRepository(db)
    use_case = DeleteTask(repository)

    deleted = use_case.execute(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )
