from celery import Celery
from celery_insight import Insight

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

insight = Insight(app)
