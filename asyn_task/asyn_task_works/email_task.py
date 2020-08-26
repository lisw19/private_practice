import time

from asyn_task.celery_main import celery_app


@celery_app.task
def send_email(user_name):
    print(user_name, '发送email')
    time.sleep(5)
    return user_name
