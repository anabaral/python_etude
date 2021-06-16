# 웃대(humoruniv.com) 자료를 퍼갈 때 필요한 그림파일들을 쉽게 받으려고 만듬.
# 같은 디렉터리에 webp2jpg.bat 파일이 필요함.
#
from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup

import re, os, os.path
import subprocess
import hashlib
import argparse


def get_url(given_url):
  if not given_url.startswith("http") :
    return None
  if "thumb_crop_resize.php?" in given_url:
    if "thumb_crop_resize.php?url_enc=" in given_url:
      return None
    url = given_url.split("thumb_crop_resize.php?url=")[1].split("?")[0]
    return url
  return given_url.split("?")[0]


# 웃대 그림받기
# <div class="body_editor"> 를 찾고 
# 그 안의 <div class="simple_attach_img_div"> 들을 찾아
# img src="" > 들을 받으면 되는데
# 대개 webp 확장자라 변환이 필요함.


common_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}

parser = argparse.ArgumentParser(description='download from e-hentai.org')
parser.add_argument('url', type=str)
args = parser.parse_args()

base_dir = 'C:\\Users\\rindon\Desktop\\'
base_url = args.url

req = Request(url=base_url,  headers=common_headers)

res = urlopen(req)
html = res.read().decode('cp949')

bs = BeautifulSoup(html, 'html.parser')

pic_img_urls = []
pic_img_elts = bs.select('div#cnts div.simple_attach_img_div img')
pic_img_elts.extend(bs.select('div#cnts table div.comment_img_div img'))
pic_img_elts.extend(bs.select('div#cnts div.body_editor img'))
pic_img_elts.extend(bs.select('div#cnts div#wrap_img img'))
for pic_img_elt in pic_img_elts:
  img_url = get_url(pic_img_elt['src'])
  #print(img_url)
  pic_img_urls.append(img_url)

webp_exists=False
cnt=1
md5sums=[]
for each_img_url in pic_img_urls:
  if not each_img_url:
    continue
  each_img_ext = os.path.splitext(each_img_url)[1]
  if each_img_ext == '.webp':
    webp_exists=True
  to_filename = base_dir + ("%2.2d"% cnt) + each_img_ext
  #urlretrieve(each_img_url, filename= to_filename )
  data = urlopen(each_img_url).read()
  hash = hashlib.md5(data).hexdigest()
  if hash in md5sums:
    print('image duplicate found.')
  else:
    print(f"{each_img_url} --> {to_filename}" )
    with open(to_filename, 'wb') as f:
      f.write(data)
      f.close()
    md5sums.append(hash)
    cnt = cnt + 1

if webp_exists:
  print('webp2jpg.bat')
  os.system('webp2jpg.bat')

