from sqlalchemy.orm import Session
from uuid import UUID

from domain.entities.task_list.task_list import TaskList
from domain.repositories.task_list.task_list_repository import TaskListRepository
from infrastructure.database.models.task.task import TaskModel
from infrastructure.database.models.task_list.task_list import TaskListModel


class DBTaskListRepository(TaskListRepository):

    def __init__(self, session: Session):
        self.session = session

    def _to_entity(self, model: TaskListModel) -> TaskList:
        return TaskList(
            id=model.id,
            name=model.name,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def create(self, task_list: TaskList) -> TaskList:
        model = TaskListModel(
            id=task_list.id,
            name=task_list.name,
            created_at=task_list.created_at,
            updated_at=task_list.updated_at,
        )

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        return self._to_entity(model)

    def get_by_id(self, task_list_id: UUID) -> TaskList | None:
        model = (
            self.session.query(TaskListModel)
            .filter(TaskListModel.id == task_list_id)
            .first()
        )

        if model is None:
            return None

        return self._to_entity(model)

    def update(self, task_list: TaskList) -> TaskList | None:
        model = (
            self.session.query(TaskListModel)
            .filter(TaskListModel.id == task_list.id)
            .first()
        )

        if model is None:
            return None

        model.name = task_list.name
        model.updated_at = task_list.updated_at

        self.session.commit()
        self.session.refresh(model)

        return self._to_entity(model)

    def delete(self, task_list_id: UUID) -> None:
        model = (
            self.session.query(TaskListModel)
            .filter(TaskListModel.id == task_list_id)
            .first()
        )

        if model is None:
            return

        self.session.query(TaskModel).filter(TaskModel.list_id == task_list_id).delete(
            synchronize_session=False
        )

        self.session.delete(model)
        self.session.commit()
