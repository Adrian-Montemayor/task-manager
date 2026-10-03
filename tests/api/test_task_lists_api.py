def test_create_task_list(client):
    response = client.post("/task-lists/", json={"name": "Groceries"})

    assert response.status_code == 200
    assert response.json()["name"] == "Groceries"


def test_create_task_list_without_name_fails(client):
    response = client.post("/task-lists/", json={"name": ""})

    assert response.status_code == 422


def test_get_task_list(client):
    created = client.post("/task-lists/", json={"name": "Groceries"}).json()

    response = client.get(f"/task-lists/{created['id']}")

    assert response.status_code == 200
    assert response.json()["name"] == "Groceries"


def test_get_unknown_task_list_returns_404(client):
    response = client.get("/task-lists/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404


def test_update_task_list(client):
    created = client.post("/task-lists/", json={"name": "Groceries"}).json()

    response = client.put(
        f"/task-lists/{created['id']}",
        json={"name": "Weekly Groceries"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Weekly Groceries"


def test_delete_task_list(client):
    created = client.post("/task-lists/", json={"name": "Groceries"}).json()

    response = client.delete(f"/task-lists/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/task-lists/{created['id']}").status_code == 404
