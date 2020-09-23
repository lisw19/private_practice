from celery import Celery

# 定义celery对象
celery_app = Celery('asyn_task', include=['asyn_task.asyn_task_works.email_task'])
celery_app.config_from_object('asyn_task.celery_config')

if __name__ == '__main__':
    celery_app.start()
