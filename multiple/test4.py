from celery import Celery
from celery import chord
from celery import signature

app = Celery(__name__)

@app.task
def add(x, y):
    return x + y

@app.task
def tsum(numbers):
    return sum(numbers)

result = add(2,2)
print(result)

result = signature('tasks.add', args=(2, 2), countdown=10)
print(result())

print(add.s(2,2))