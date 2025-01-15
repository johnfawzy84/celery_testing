from celery.contrib.pytest import celery_worker,celery_app
from ..app.tasks import add, subtract, add_absolute_values, sub_absolute_values
from fastapi.testclient import TestClient
from ..app.main import app
from celery import shared_task

client = TestClient(app)

def test_add_pure(celery_app,celery_worker):
    assert add.delay(4, 4).get(timeout=10) == 8

def test_add_task(celery_app, celery_worker):
    print(celery_app)
    result = add.delay(4, 6)
    assert result.get(timeout=10) == 10

def test_subtract_task(celery_app, celery_worker):
    result = subtract.apply_async(args=[10, 4])
    assert result.get(timeout=10) == 6

def test_add_endpoint(celery_app, celery_worker):
    response = client.post("/tasks/add", json={"x": 4, "y": 6})
    assert response.status_code == 200
    task_id = response.json()["task_id"]
    result = add.AsyncResult(task_id)
    assert result.get(timeout=10) == 10
    assert result.task_id == task_id

def test_subtract_endpoint():
    response = client.post("/tasks/subtract", json={"x": 10, "y": 4})
    assert response.status_code == 200
    task_id = response.json()["task_id"]
    result_response = client.get(f"/tasks/{task_id}/result")
    assert result_response.status_code == 200
    assert result_response.json()["result"] == 6

def test_add_absolute_values_chain(celery_app, celery_worker):
    response = client.post("/tasks/add?x=-4&y=-6")
    assert response.status_code == 200
    task_id = response.json()["task_id"]
    result = add_absolute_values.AsyncResult(task_id)
    assert result.get(timeout=10) == 10
    assert result.task_id == task_id

def test_sub_absolute_values_chain(celery_app, celery_worker):
    test_sub = celery_app.task(subtract)
    test_sub_chain = celery_app.task(sub_absolute_values)
    # Aktualisieren Sie die sub_absolute_values-Task, um die neue subtract-Task zu verwenden
    sub_absolute_values.update_state(task_id=test_sub_chain.name, state='PENDING')

    response = client.post("/tasks/subtract?x=-6&y=-4")
    assert response.status_code == 200
    task_id = response.json()["task_id"]
    result = test_sub_chain.AsyncResult(task_id)
    assert result.get(timeout=10) == 2
    assert result.task_id == task_id