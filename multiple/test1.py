# NEED: pip install requests
#
import requests

def fetch_page_by_url(url):
    res = requests.get(url)

    if int(res.status_code / 100) == 2:
        return res.text

merged_text = []
for i in range(1, 10):
    result = fetch_page_by_url(
        'http://localhost:9080/{}'.format(i)
    )
    if result is not None:
        merged_text.append(result)

#print(merged_text)
print(''.join(merged_text))