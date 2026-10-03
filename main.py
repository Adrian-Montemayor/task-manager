from fastapi import FastAPI

from api.routes.task_lists import router as task_list_router
from api.routes.tasks import router as task_router
from infrastructure.database.connection import engine
from infrastructure.database.models.base import Base
from infrastructure.database.models.task.task import TaskModel
from infrastructure.database.models.task_list.task_list import TaskListModel

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(task_list_router)
app.include_router(task_router)
