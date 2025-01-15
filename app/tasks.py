from .celery_app import app
from celery import shared_task


@shared_task
def add(x=0, y=0):
    return x + y

@app.task
def subtract(x, y):
    return x - y

@shared_task
def abs_value(x):
    return abs(x)

from celery import chain

@shared_task
def add_absolute_values(x, y):
    x_new = abs_value.s(x)()
    return chain(abs_value.s(y), add.s(x_new)).apply_async()

@app.task
def sub_absolute_values(x, y):
    y_new = abs_value.s(y)()
    return chain(abs_value.s(x), subtract.s(y_new)).apply_async()