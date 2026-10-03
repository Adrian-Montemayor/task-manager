import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

TEST_DB_PATH = "./test_task_manager.db"

if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)

os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"

from main import app
from infrastructure.database.connection import SessionLocal
from infrastructure.database.models.task.task import TaskModel
from infrastructure.database.models.task_list.task_list import TaskListModel


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def clean_database():
    yield

    with SessionLocal() as db:
        db.execute(delete(TaskModel))
        db.execute(delete(TaskListModel))
        db.commit()
