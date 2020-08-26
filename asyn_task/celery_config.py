from kombu import Exchange, Queue

BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
# 任务序列化和反序列化使用msgpack方案
CELERY_TASK_SERIALIZER = 'json'
# 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
CELERY_RESULT_SERIALIZER = 'json'
# 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显
CELERY_TASK_RESULT_EXPIRES = 60 * 60
# 指定接受的内容类型
CELERY_ACCEPT_CONTENT = ['json']
# 并发worker数
CELERYD_CONCURRENCY = 5

TIME_ZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = False
USE_TZ = True
CELERY_TIMEZONE = "Asia/Shanghai"

# 某个程序中出现的队列，在broker中不存在，则立刻创建它
CELERY_CREATE_MISSING_QUEUES = True
# 非常重要,有些情况下可以防止死锁
CELERYD_FORCE_EXECV = True

BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 60}
# 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
CELERY_DISABLE_RATE_LIMITS = True

# 每个worker最多执行万100个任务就会被销毁，可防止内存泄露
CELERYD_MAX_TASKS_PER_CHILD = 100

# 设置不同队列
CELERY_QUEUES = (
    Queue('base_downloader', Exchange('base_downloader'),
          routing_key='base_downloader'),
    Queue('base_parser', Exchange('base_parser'), routing_key='base_parser'),
    Queue('error_crawler', Exchange('error_crawler'), routing_key='error_crawler'),
    Queue('priority_downloader', Exchange('priority_downloader'), routing_key='priority_downloader'),
    Queue('infer_downloader', Exchange('infer_downloader'), routing_key='infer_downloader')
)

# 队列路由
CELERY_ROUTES = {
    'celery_recruit.celery_workers.downloader.request_crawler': {
        'queue': 'base_downloader', 'routing_key': 'base_downloader'},
    'celery_recruit.celery_workers.downloader.error_request_crawler': {
        'queue': 'error_crawler', 'routing_key': 'error_crawler'},
    'celery_recruit.celery_workers.downloader.priority_request_crawler': {
        'queue': 'priority_downloader', 'routing_key': 'priority_downloader'},
    'celery_recruit.celery_workers.downloader.infer_request_crawler': {
        'queue': 'infer_downloader', 'routing_key': 'infer_downloader'},
    'celery_recruit.celery_workers.parser.cfda_drugs_register_search_parse': {
        'queue': 'base_parser', 'routing_key': 'base_parser'}
}
