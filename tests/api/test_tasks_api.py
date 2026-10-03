def create_task_list(client):
    response = client.post("/task-lists/", json={"name": "Groceries"})
    return response.json()


def create_task(client, task_list_id, title="Buy milk"):
    response = client.post(
        f"/tasks/?list_id={task_list_id}",
        json={"title": title, "priority": "high"},
    )
    return response.json()


def test_create_task(client):
    task_list = create_task_list(client)

    response = client.post(
        f"/tasks/?list_id={task_list['id']}",
        json={"title": "Buy milk", "priority": "high"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Buy milk"
    assert response.json()["status"] == "todo"


def test_create_task_without_list_id(client):
    response = client.post(
        "/tasks/",
        json={"title": "Buy milk", "priority": "high"},
    )

    assert response.status_code == 422


def test_get_task(client):
    task_list = create_task_list(client)
    task = create_task(client, task_list["id"])

    response = client.get(f"/tasks/{task['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == task["id"]


def test_get_unknown_task(client):
    response = client.get("/tasks/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404


def test_update_task(client):
    task_list = create_task_list(client)
    task = create_task(client, task_list["id"])

    response = client.put(
        f"/tasks/{task['id']}",
        json={
            "title": "Buy oat milk",
            "description": "1 liter",
            "status": "in_progress",
            "priority": "medium",
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Buy oat milk"
    assert response.json()["status"] == "in_progress"


def test_change_task_status(client):
    task_list = create_task_list(client)
    task = create_task(client, task_list["id"])

    response = client.patch(
        f"/tasks/{task['id']}",
        json={"status": "completed"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_delete_task(client):
    task_list = create_task_list(client)
    task = create_task(client, task_list["id"])

    response = client.delete(f"/tasks/{task['id']}")

    assert response.status_code == 204
    assert client.get(f"/tasks/{task['id']}").status_code == 404


def test_list_tasks(client):
    task_list = create_task_list(client)
    create_task(client, task_list["id"], title="Milk")
    create_task(client, task_list["id"], title="Bread")

    response = client.get(f"/tasks/list/{task_list['id']}")

    assert response.status_code == 200
    assert len(response.json()["tasks"]) == 2


def test_list_tasks_shows_completed_percentage(client):
    task_list = create_task_list(client)
    task = create_task(client, task_list["id"])
    create_task(client, task_list["id"], title="Bread")
    client.patch(f"/tasks/{task['id']}", json={"status": "completed"})

    response = client.get(f"/tasks/list/{task_list['id']}")

    assert response.json()["completed_percentage"] == 50.0
