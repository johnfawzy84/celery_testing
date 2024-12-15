import pytest

from celery.contrib.pytest import celery_app, celery_worker
from testcontainers.redis import RedisContainer
from app.tasks import add, subtract
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

@pytest.fixture(scope="module")
def redis_container():
    with RedisContainer() as redis:
        yield redis.get_client()

@pytest.fixture(scope="module")
def celery_config(redis_container):
    connection_url = f"redis://{redis_container.connection_pool.connection_kwargs["host"]}:{redis_container.connection_pool.connection_kwargs["port"]}/0"
    return {
        "broker_url": connection_url,
        "result_backend": connection_url,
    }

@pytest.fixture(scope="module")
def celery_includes():
    return ["app.tasks"]

def test_add_task(celery_app, celery_worker):
    result = add.apply_async(args=[4, 6])
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
