from celery import Celery

# test4 는 파일명이자 app 이름
# 브로커를 RabbitMQ로 사용한다고 가정. 실제 실행하면 localhost:5672 에 접속하려고 애씀.
app = Celery('test4', broker='pyamqp://guest@localhost//')

# 다음 명령으로 실행.
# celery -A test4 worker --loglevel=info

@app.task
def add(x,y):
    return x+y
