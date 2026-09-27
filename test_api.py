from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

# ----------------GET /tasks ---------------

def test_get_tasks_returns_list():
    """باید یک لسیت برگردانده شود"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ------------ POST  /tasks -------------


def test_create_task():
    """ POST /tasks باید تسک جدید بسازید"""
    response = client.post("/tasks", json={"title": "تست تسک جدید"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task created"
    assert data["title"] == "تست تسک جدید"



def test_create_task_missing_title():
    """باد خط ۴۲۲ بدهید  POST /tasks"""
    response = client.post("/tasks", json={})
    assert response.status_code == 422


    #------------------ PATCH  /tasks/{id}/done ------------
def test_mark_task_done():
    """PATCH باید  انجام بدهید """
    client.post("/tasks", json={"title": "تست برای علامت"})


    # اول تسک ID پیدا کردن 
    tasks = client.get("/tasks").json()
    task_id = tasks[-1]["id"]

    #علامت زدن 
    response = client.patch(f"/tasks/{task_id}/done")
    assert response.status_code == 200
    assert response.json()["message"] == "Task marked as done"


    # done = true

    tasks = client.get("/tasks").json()
    updated_task = next(t for t in tasks if t["id"] == task_id)
    assert updated_task["done"] is True

def test_mark_done_nonexistent_task():
    """برای تست های ناموجودی """
    response = client.patch("/tasks/99999/done")
    assert response.status_code == 404

    #-----------------DEDELET /tasks/{id} ------

def test_delete_task():
    """باید تسک را حذف بسازیم """
    client.post("/tasks", json={"title": "تسک برای حذف"})

    #ID پیداکردن 
    tasks = client.get("/tasks").json()
    task_id = tasks[-1]["id"]


    #برای  حذف
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted"


    #تایید که دیکر نیست
    tasks_after = client.get("/tasks").json()
    ids_after = [t["id"] for t in tasks_after]
    assert task_id not in ids_after


def test_delete_nonexistent_task():
    """برای تسک ناموجود باید ۴۰۴ بدهد """
    response = client.delete("/tasks/99999")
    assert response.status_code == 404