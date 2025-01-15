import pytest
from testcontainers.redis import RedisContainer
from celery import Celery
from celery.contrib.testing.worker import start_worker
@pytest.fixture(scope="session")
def redis_container():
    with RedisContainer() as redis:
        yield redis.get_client()

#pytest_plugins = ("celery.contrib.pytest",)  # <-- Important!

@pytest.fixture(scope="session")
def celery_config(redis_container):
    connection_url = f"redis://{redis_container.client().connection.host}:{redis_container.client().connection.port}/0"
    return {
        "broker_url": connection_url,
        "result_backend": connection_url,
    }

@pytest.fixture(scope="session")
def celery_worker_parameters():
    return {"without_heartbeat": False}

@pytest.fixture(scope='session')
def celery_enable_logging():
    return True

@pytest.fixture(scope="session")
def celery_includes():
    return ["app.tasks"]

# @pytest.fixture(scope="session")
# def celery_app(celery_config):
#     app = Celery("test_app",backend=celery_config["result_backend"],broker=celery_config["broker_url"])
#     return app

# @pytest.fixture(scope="session")
# def celery_worker(celery_app):
#     with start_worker(celery_app, perform_ping_check=False) as worker:
#         yield worker
