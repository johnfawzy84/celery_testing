from .celery import app

@app.task
def add(x, y):
    return x + y

@app.task
def subtract(x, y):
    return x - y