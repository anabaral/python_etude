# NEED: pip install requests
# NEED: pip install celery
#
import requests
from celery import Celery
from celery import chord

app = Celery(__name__)

@app.task
def fetch_page_by_url(url):
    res = requests.get(url)
    if int(res.status_code / 100) == 2:
        return res.text

@app.task
def merge_text(texts):
    return ''.join(texts)

tasks = []
for i in range(1, 10):
    tasks.append( fetch_page_by_url.s(
        'http://localhost:9080/{}'.format(i), i
    ))

do_chain_tasks = chord(tasks)(merge_text).get()
print(do_chain_tasks)
