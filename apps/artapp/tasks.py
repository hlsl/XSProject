import time

from XSProject.celery import app

@app.task
def sendMail(to, msg):
    time.sleep(5)
    print('向', to, '发送:', msg, '成功')

    return 'ok'


