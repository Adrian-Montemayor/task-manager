from uuid import UUID

from sqlalchemy.orm import Session

from domain.entities.task.task import Task
from domain.enums.task_priority import TaskPriority
from domain.enums.task_status import TaskStatus
from domain.repositories.task.task_repository import TaskRepository
from infrastructure.database.models.task.task import TaskModel


class DBTaskRepository(TaskRepository):

    def __init__(self, session: Session):
        self.session = session

    def _to_entity(self, model: TaskModel) -> Task:
        return Task(
            id=model.id,
            list_id=model.list_id,
            title=model.title,
            description=model.description,
            status=model.status,
            priority=model.priority,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def create(self, task: Task) -> Task:
        model = TaskModel(
            id=task.id,
            list_id=task.list_id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        return self._to_entity(model)

    def get_by_id(self, task_id: UUID) -> Task | None:
        model = self.session.query(TaskModel).filter(TaskModel.id == task_id).first()

        if model is None:
            return None

        return self._to_entity(model)

    def update(self, task: Task) -> Task | None:
        model = self.session.query(TaskModel).filter(TaskModel.id == task.id).first()

        if model is None:
            return None

        model.title = task.title
        model.description = task.description
        model.status = task.status
        model.priority = task.priority
        model.updated_at = task.updated_at

        self.session.commit()
        self.session.refresh(model)

        return self._to_entity(model)

    def delete(self, task_id: UUID) -> None:
        model = self.session.query(TaskModel).filter(TaskModel.id == task_id).first()

        if model is None:
            return

        self.session.delete(model)
        self.session.commit()

    def get_by_list(
        self,
        list_id: UUID,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
    ) -> list[Task]:
        query = self.session.query(TaskModel).filter(TaskModel.list_id == list_id)

        if status is not None:
            query = query.filter(TaskModel.status == status.value)

        if priority is not None:
            query = query.filter(TaskModel.priority == priority.value)

        models = query.all()

        return [self._to_entity(model) for model in models]
