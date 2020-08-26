from asyn_task.asyn_task_works.email_task import send_email

for i in range(1, 20):
    a = send_email.delay(i)
    print(a)
