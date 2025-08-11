from dotenv import load_dotenv
load_dotenv()

from backend.celery_app import celery
from backend.app import create_app


flask_app = create_app()

#run celery within flask app context
celery.conf.update(flask_app.config)

#this line ensures all tasks will run with the flask app context
TaskBase = celery.Task

class ContextTask(TaskBase):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)

celery.Task = ContextTask