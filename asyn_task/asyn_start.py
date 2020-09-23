from asyn_task.asyn_task_works.email_task import send_email

for i in range(1, 50):
    # 任务添加签名（延迟执行， 指定时间未执行取消）
    task = send_email.signature(countdown=10, expires=600)
    a = task.delay(i)
    print(a)
