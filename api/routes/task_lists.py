from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from api.schemas.task_list import TaskListCreate, TaskListResponse, TaskListUpdate
from application.use_cases.task_list.create_task_list import CreateTaskList
from application.use_cases.task_list.get_task_list import GetTaskList
from application.use_cases.task_list.update_task_list import UpdateTaskList
from application.use_cases.task_list.delete_task_list import DeleteTaskList
from infrastructure.database.connection import SessionLocal
from infrastructure.repositories.task_list.task_list_repository import (
    DBTaskListRepository,
)

router = APIRouter(prefix="/task-lists", tags=["Task Lists"])


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TaskListResponse)
def create_task_list(
    data: TaskListCreate,
    db: Session = Depends(get_db),
):
    repository = DBTaskListRepository(db)
    use_case = CreateTaskList(repository)

    task_list = use_case.execute(data.name)

    return task_list


@router.get("/{task_list_id}", response_model=TaskListResponse)
def get_task_list(
    task_list_id: UUID,
    db: Session = Depends(get_db),
):
    repository = DBTaskListRepository(db)
    use_case = GetTaskList(repository)

    task_list = use_case.execute(task_list_id)

    if task_list is None:
        raise HTTPException(
            status_code=404,
            detail="Task list not found",
        )

    return task_list


@router.put("/{task_list_id}", response_model=TaskListResponse)
def update_task_list(
    task_list_id: UUID,
    data: TaskListUpdate,
    db: Session = Depends(get_db),
):
    repository = DBTaskListRepository(db)
    use_case = UpdateTaskList(repository)

    task_list = use_case.execute(
        task_list_id=task_list_id,
        name=data.name,
    )

    if task_list is None:
        raise HTTPException(
            status_code=404,
            detail="Task list not found",
        )

    return task_list


@router.delete("/{task_list_id}", status_code=204)
def delete_task_list(
    task_list_id: UUID,
    db: Session = Depends(get_db),
):
    repository = DBTaskListRepository(db)
    use_case = DeleteTaskList(repository)

    deleted = use_case.execute(task_list_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task list not found",
        )
