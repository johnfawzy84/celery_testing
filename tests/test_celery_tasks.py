import pytest
from celery.contrib.pytest import celery_app, celery_worker
from testcontainers.redis import RedisContainer
from tasks import add, subtract

@pytest.fixture(scope="module")
def redis_container():
    with RedisContainer() as redis:
        yield redis

@pytest.fixture(scope="module")
def celery_config(redis_container):
    return {
        "broker_url": redis_container.get_connection_url(),
        "result_backend": redis_container.get_connection_url(),
    }

@pytest.fixture(scope="module")
def celery_includes():
    return ["tasks"]

def test_add_task(celery_app, celery_worker):
    result = add.apply_async(args=[4, 6])
    assert result.get(timeout=10) == 10

def test_subtract_task(celery_app, celery_worker):
    result = subtract.apply_async(args=[10, 4])
    assert result.get(timeout=10) == 6

def test_chain_tasks(celery_app, celery_worker):
    from celery_app import chain
    result = chain(add.s(4, 6), subtract.s(2)).apply_async()
    assert result.get(timeout=10) == 8
