# 오유 네임드였던 방콕고양이 님 글에 태클을 달기 위해 만든 스크립트.
# http://todayhumor.com/?databox_74439 에 있는 그림들이 태클을 위해 준비했던 것임
# (지금은 방콕고양이님이 탈퇴하셔서 소용 없지만.. 스크립트 기법을 남기는 의미에서 저장함..)
# - 17:59:00 쯤부터 실행하면 3초마다 페이지 검사해서 감지함.
# - 태클 댓글을 올리는 건 로그인 권한이 필요한데 직접 구현하는 건 까다로워서 이미 로그인된 크롬에 새탭을 띄우는 식으로 구현함.
# - 태클 댓글을 너무 일찍 띄우면 의심받기도 하고 너무 1등만 하면 긴장감이 없으니 적당히 랜덤 시간을 기다린 후 태클 들어감.
# - 나는 새 탭이 뜨기를 기다렸다 들어가서 추천하면 됨.

import urllib.request
from urllib.parse import quote
import re, time, datetime, random
import webbrowser
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))

hdr = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}


img_url = 'http://thimg.todayhumor.co.kr/upfile/202106/1623400625161348c79041447a8d5913eb7ecd7edf__mn117629__w500__h282__f653996__Ym202106__ANIGIF.gif'
img_url_encoded= urllib.parse.quote(img_url, safe='')


finished=False
while not finished:
    request = urllib.request.Request('http://www.todayhumor.co.kr/board/list.php?table=humordata&page=1', headers = hdr) 
    with urllib.request.urlopen(request) as response:
        html = response.read().decode('utf-8')
        z = re.search('href="([^"]+)"[^>]+>심심풀이로 볼만한.*\n.*class=\'list_name_member\'>방콕고양이', html)
        if z:
            found_url = z.group(1)
            z_no = re.search('[&]no=([0-9]+)[&]', found_url).group(1)
            insert_memo_url = 'http://www.todayhumor.co.kr/board/ajax_memo_insert.php?table=humordata&no=' + z_no + '&table_memo_no=memo&parent_id=' + z_no + '&memo_parent_table=humordata&m_name=우가가&memo=' + img_url_encoded + '&upfile=&img_pos=up'
            time.sleep(random.randint(3,7))
            webbrowser.get('chrome').open(insert_memo_url)
            finished = True
            #ok_flag = ?
            #ok_url = 'http://www.todayhumor.co.kr/board/ajax_ok.php?ok_flag=' + ok_flag + '&table=humordata&no=' + z_no
            #webbrowser.get('chrome').open(ok_url)
    print(datetime.datetime.now())
    time.sleep(3)

print('Done')

