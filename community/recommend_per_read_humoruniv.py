## 웃대 베스트 첫 15페이지를 읽어 조회수 대비 추천수를 퍼센트로 계산해 평균값을 구한다.
## 실행인수를 줘서 읽는 페이지 수를 조절할 수 있다.
## 
from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup


common_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}
    
num_of_pages = 15
print(f"number of pages check = {num_of_pages}")

sum=0
cnt=0
for i in range(1, num_of_pages):
    url = f"https://m.humoruniv.com/board/humor/list.html?table=pds&pg={i}"
    req = Request(url=url,  headers=common_headers)
    res = urlopen(req)
    html = res.read().decode(encoding='cp949', errors='ignore')
    bs = BeautifulSoup(html, 'html.parser')
    span_elts = bs.select("div#list_body a.list_body_href li table tr td span.blk")
    for span_elt in span_elts:
        oknum_cnt = int(span_elt.select_one("span.ok_num").text.strip())
        extra_cnt = int(span_elt.select_one("span.extra").text.strip().replace(',',''))
        recommend_per_read_as_percent = round(100 * oknum_cnt / extra_cnt, 2)
        sum = sum + recommend_per_read_as_percent
        cnt = cnt + 1

print(f"{sum} / {cnt} = {sum / cnt}")
    
