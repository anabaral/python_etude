# pip install PyQt5 beautifulsoup4 validators pyperclip opencv-python pillow numpy 
#
import re, sys, os, gc, time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QTextEdit, QFileDialog, QCheckBox
from PyQt5.QtCore import Qt
from urllib.request import Request, urlopen, urlretrieve
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import validators

import subprocess
import hashlib
import pyperclip
from PIL import ImageGrab
import cv2
import numpy as np
from http.client import InvalidURL
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
from http.client import IncompleteRead

current_loc = os.getcwd()

executor = ThreadPoolExecutor(max_workers=5)

def base_dir():
  return current_loc + "\\"

# you need
# pip install pyqt5


def get_url(given_url, elt=None):
  if not given_url.startswith("http") :
    if ("//filecache" in given_url or "//down-webp.humoruniv.com" in given_url) and elt is not None:
      # <img src="http://filecache.humoruniv.com..." OnError="...">
      # print(f"filecached] elt={elt}")
      onerror = re.search("'https?://[^']+'", elt['onerror'])
      print(f"\n\n\nonerror={onerror}")
      if not onerror:
        onerror = re.search("'//down.humoruniv.com[^']+'", elt['onerror'])
      if not onerror:
        return None
      print(f"filecached] onerror= {onerror.group(0)}")
      url = "http:" + onerror.group(0).strip("'").lstrip("http:").lstrip("https:")
      # print(f"filecached] url from onerror = {url}")
      return url
    elif "//timg.humoruniv.com/thumb_crop_resize.php?" in given_url:
      if "thumb_crop_resize.php?url_enc=" in given_url:
        return None
      url = given_url.split("thumb_crop_resize.php?url=")[1].split("?")[0]
      return url
    elif "//down.humoruniv.com/" in given_url:
      return "http:" + given_url
    elif given_url.startswith("/dvs"):  # dogdrip
      return "https://dogdrip.net" + given_url
    else:
      return None
  if "thumb_crop_resize.php?" in given_url:
    if "thumb_crop_resize.php?url_enc=" in given_url:
      return None
    url = given_url.split("thumb_crop_resize.php?url=")[1].split("?")[0]
    return url
  return given_url.split("?")[0]


class MyApp(QWidget):
  title = ''
  ref = ''

  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.setWindowTitle("웃대펌")

    hbox1 = QHBoxLayout()
    self.loc = QLineEdit(current_loc)
    self.loc.setReadOnly(True)
    self.btn_chg_loc = QPushButton('Change Loc')
    self.btn_chg_loc.clicked.connect(self.change_loc)
    
    hbox1.addWidget(self.loc)
    hbox1.addWidget(self.btn_chg_loc)

    vbox = QVBoxLayout()
    vbox.addLayout(hbox1)

    self.btn_apply = QPushButton('Apply URL')
    self.btn_apply.clicked.connect(self.apply_url)
    vbox.addWidget(self.btn_apply)

    self.btn_title = QPushButton()
    self.btn_title.setText('+title')
    self.btn_title.clicked.connect(self.get_title)
    self.btn_title.setStyleSheet("background-color: #cc9")
    vbox.addWidget(self.btn_title)
    
    hbox_ref = QGridLayout()
    self.btn_copy_video_attr = QPushButton('+video attr')
    self.btn_copy_video_attr.clicked.connect(lambda: self.copy_video_attr())
    self.btn_copy_video_attr.setStyleSheet("background-color: #cc9")
    self.btn_copy_video_attr.setMaximumWidth(200)
    hbox_ref.addWidget(self.btn_copy_video_attr, 0, 0)
    self.btn_ref = QPushButton()
    self.btn_ref.setText('+ref')
    self.btn_ref.clicked.connect(self.get_ref)
    self.btn_ref.setStyleSheet("background-color: #cc9")
    hbox_ref.addWidget(self.btn_ref, 0, 1, 1, 3)
    vbox.addLayout(hbox_ref)
    
    self.overwrite_chk = QCheckBox('overwrite')
    #self.overwrite_chk.toggle() # set checked
    self.label_clip = QLabel('Clip to 00.png', self)
    self.btn_clip_png150 = QPushButton('150%')
    self.btn_clip_png150.clicked.connect(lambda: self.copy_to_00png(1.5))
    self.btn_clip_png125 = QPushButton('125%')
    self.btn_clip_png125.clicked.connect(lambda: self.copy_to_00png(1.25))
    self.btn_clip_png100 = QPushButton('100%')
    self.btn_clip_png100.clicked.connect(lambda: self.copy_to_00png(1.0))
    
    hbox2 = QHBoxLayout()
    hbox2.addWidget(self.label_clip)
    hbox2.addWidget(self.overwrite_chk)
    hbox2.addWidget(self.btn_clip_png150)
    hbox2.addWidget(self.btn_clip_png125)
    hbox2.addWidget(self.btn_clip_png100)
    vbox.addLayout(hbox2)
    
    self.textbox_log = QTextEdit()
    vbox.addWidget(self.textbox_log)
    
    self.btn_del = QPushButton('delete all temp pics')
    self.btn_del.clicked.connect(self.del_temp_pics)
    vbox.addWidget(self.btn_del)
    
    self.setLayout(vbox)
    self.move(400, 200)
    self.show()

  def change_loc(self):
    dialog = QFileDialog()
    global current_loc
    current_loc = dialog.getExistingDirectory(None, "Select Folder")
    self.loc.setText(current_loc)

  def apply_url(self):
    executor.submit(self.apply_url_inner())
  
  
  def apply_url_inner(self):
    common_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}
    base_url = pyperclip.paste().strip()
    print("<<" + base_url + ">>")
    site_name=None
    if "humoruniv" in base_url:
        site_name="humoruniv"
    elif "ggeal" in base_url:
        site_name="ggeal"
    elif "dogdrip" in base_url:
        site_name="dogdrip"
    
    if not validators.url(base_url):
      self.btn_apply.setText('Apply URL: URL이 좀 이상함. 카피한 거 확인해봐요?')
      return
    elif site_name is None:
      self.btn_apply.setText('Apply URL: 웃대나 깨알 URL이 아닌것 같아요?')
      return
    else:
      self.btn_apply.setText('Apply URL')

    if base_url.startswith('http://m.humoruniv') or base_url.startswith('https://m.humoruniv'):
        base_url = base_url.replace('//m.humoruniv', '//web.humoruniv')
    if base_url.startswith('https://m.ggeal.com'):
        base_url = base_url.replace('https://m.ggeal.com', 'https://www.ggeal.com')

    req = Request(url=base_url,  headers=common_headers)
    try:
      res = urlopen(req)
    except urllib.error.URLError:
      self.btn_apply.setText(f"Apply URL: 받아오는데 실패했습니다. 원인불명...")
      return
    
    if site_name == "humoruniv":
        page_encoding = "cp949"
    else: # ggeal
        page_encoding = "utf-8"
    html = res.read().decode(encoding=page_encoding, errors='ignore')
    
    
    bs = BeautifulSoup(html, 'html.parser')
    #print(f"\n\n\n\n\n{html[5000:8000]}\n\n")
    # body가 빌 경우가 있네? 대기자료-->웃자 로 넘어가면
    if len(bs.select('body div')) < 1:
      self.btn_apply.setText('Apply URL: body 내용이 없네요, 대기자료가 웃자로 넘어갔나?')
      return
    
    logs = []
    pic_img_urls = []
    if site_name == "humoruniv":
        #title_elt = bs.select('title')[0]
        #title = re.sub(pattern=' ?:: 웃긴.*', repl='', string=title_elt.text)
        title_elt = bs.select('span#ai_cm_title')[0]
        self.title = re.sub(pattern='<!--[^-]+-->', repl='', string=title_elt.text)
        print(self.title)
        self.btn_title.setText(f"{self.title}")
        
        refs = []
        short_url_elt = bs.select('input#short_url')
        if len(short_url_elt) > 0:
          refs.append(short_url_elt[0]['value'])
        
        #ref_elts = bs.select('div#wrap_cbay_new table a')
        print(bs.select('div#cnts')[0].find_next_sibling("div"))
        ref_elts = bs.select('div#cnts')[0].find_next_sibling("div").select("div span a")
        print(f"ref_elts  = {ref_elts}")
        for ref_elt in ref_elts:
          if ref_elt.text:
            refs.append(ref_elt.text)
        self.ref = '\n'.join(refs)
        print(self.ref)

        self.btn_ref.setText(f"{self.ref}")
        self.btn_ref.adjustSize()
        #self.adjustSize()
        
        pic_img_elts = bs.select('#wrap_copy div.simple_attach_img_div img , #wrap_copy table div.comment_img_div img, #wrap_copy div.body_editor img, #wrap_copy div#wrap_img img')
        #pic_img_elts = bs.select('div#wrap_copy img')
        print(f"1: {pic_img_elts}")
        print(f"2: {bs.select('div.simple_attach_img_div')}")
        
        
        ## 2022-07 쯤부터 보이는 패턴 추가
        for ext_img in bs.select("#wrap_body p span#ai_cm_content p a img"):
            pic_img_urls.append(get_url(ext_img['src']))

    elif site_name == "ggeal": # ggeal
        title_elt = bs.select('title')[0]
        self.title = title_elt.text
        print(self.title)
        self.btn_title.setText(f"{self.title}")
        
        refs = []
        short_url_elt = bs.select('div#body_read div.top_area table:nth-child(2) tr td a')
        if len(short_url_elt) > 0:
          refs.append(short_url_elt[0]['href'])
        ref_a_elts = bs.select('div.ct_info_sale div div span a')
        if len(ref_a_elts) > 0:
          for ref_a in ref_a_elts:
            refs.append(ref_a['href'])
        self.ref = '\n'.join(refs)
        print(f"refs={refs}")
        
        self.btn_ref.setText(f"{self.ref}")
        self.btn_ref.adjustSize()
        self.adjustSize()
        
        pic_img_elts = bs.select("div#content_area table div.body_editor img")
        print(f"1: {pic_img_elts}")
    else: # dogdrip
        title_elt = bs.select('title')[0]
        self.title = title_elt.text.replace(" - DogDrip.Net 개드립", "")
        print(self.title)
        self.btn_title.setText(f"{self.title}")
        refs = []
        dogdrip_url = bs.find("meta", {"property":"og:url"})
        if dogdrip_url:
            print(dogdrip_url['content'])
            refs.append(dogdrip_url['content'])
        pic_img_elts = bs.select("#article_1 img")
        
    
    for pic_img_elt in pic_img_elts:
      try:
        print(f"img src candidate = {pic_img_elt['src']}")
        img_url = get_url(pic_img_elt['src'], pic_img_elt)
        print(f"1) img_url = {img_url}")
        if not img_url:  # test
          print("... not a valid url?")
          continue
        if 'filecache' in img_url:   # <img src="http://filecache.humoruniv.com..." OnError="...">
          img_url = re.search("'http://[^']+'", pic_img_elt['onerror']).group(0).strip("'")
        print(f"2) img_url = {img_url}")
        pic_img_urls.append(img_url)
      except KeyError:
        print("no src attr??" + str(pic_img_elt))
    print(f"pic pic_img_elts = {pic_img_elts}")
    print(f"pic_img_urls = {pic_img_urls}")
    
    #webp_exists=False
    cnt=1
    md5sums=[]
    for each_img_url in pic_img_urls:
      if not each_img_url:
        continue
      from os import path
      each_img_ext = path.splitext(each_img_url)[1]
      if '?' in each_img_ext:  # url 에 ? 이 있는 경우 
          each_img_ext = each_img_ext.split('?')[0]
      #if each_img_ext == '.webp':
      #  webp_exists=True
      to_filename = base_dir() + ("%2.2d"% cnt) + each_img_ext
      parsed_each_img_url = urlparse(each_img_url)
      if not parsed_each_img_url.netloc :
        print("weird url form??")
        continue
      elif 'humoruniv.com' in parsed_each_img_url.netloc:
        referer = 'http://web.humoruniv.com/'
      elif 'fmkorea.com' in parsed_each_img_url.netloc:
        referer = 'https://www.fmkorea.com/'
      elif 'dogdrip.net' in parsed_each_img_url.netloc:
        referer = 'https://dogdrip.net/'
      else:
        #referer = f"{parsed_each_img_url} ----> {parsed_each_img_url.scheme}://{parsed_each_img_url.netloc}/"
        referer = parsed_each_img_url.netloc
      #urlretrieve(each_img_url, filename= to_filename )
      print(f"Referer: {referer}")
      headers = {'Referer': referer, 
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
               + ' Chrome/120.0.0.0 Safari/537.36'}
      print(f"image url = {each_img_url}")
      #req = Request(each_img_url, b'{}', headers, method="GET")
      req = Request(each_img_url, None, headers, method="GET")
      try:
        data = urlopen(req, timeout=5).read()
      except InvalidURL as e:
        logs.append("failed to retrieve with invalid url : " + each_img_url)
        continue
      except HTTPError as e:
        logs.append("failed to retrieve with http error : " + e.reason + " : " + each_img_url)
        continue
      except ConnectionResetError as e:
        logs.append("failed to retrive with connection reset : " + each_img_url)
        continue
      except IncompleteRead as e:
        logs.append("IncompleteRead : " +each_img_url)
        continue
      except Exception as e:
        logs.append(' '.join(["failed to retrive with Unknown Exception : ", str(e.reason), " : ", each_img_url]) )
        continue
      hash = hashlib.md5(data).hexdigest()
      if hash in md5sums:
        msg = 'image duplicate found.'
        #logs.append(msg)
        print(msg)
      else:
        msg = f"{to_filename} <-- {each_img_url}"
        logs.append(f"{to_filename}")
        print(msg)
        with open(to_filename, 'wb') as f:
          f.write(data)
          f.close()
        md5sums.append(hash)
        cnt = cnt + 1
        # check cropsize and webp
        if each_img_ext != '.gif':
          encoded_img = np.frombuffer(data, dtype = np.uint8)
          img_org = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
          if img_org is not None:   # 해석 안되는 형식인 경우가 있더라 (webp 움짤)
            if each_img_ext == '.webp':
              print(to_filename + '.jpg')
              #cv2.imwrite(to_filename + '.jpg', img_org)   # 한글경로 못쓴다네
              result, image_buf = cv2.imencode('.jpg', img_org)
              with open(to_filename + '.jpg', mode='w+b') as f:
                image_buf.tofile(f)
              #os.system(f'del "{to_filename}"')
              os.remove(os.path.join(base_dir(), to_filename))
              to_filename = to_filename + '.jpg'
            height, width, channel = img_org.shape
            if width >= 8192 :
              logs.append(f'width >= 8192 need to be manually processed')
            elif width > 800 and height >= 16384:
              logs.append('pic will be cropped...')
              self.crop_img(to_filename, img_src = img_org, cropsize = 16384)
          encoded_img = None
          img_org = None
        data = None
        
    self.textbox_log.setText('\n'.join(logs))
    self.adjustSize()
    #if webp_exists:
    #  import os
    #  print('webp2jpg.bat')
    #  os.system('webp2jpg.bat')

  def get_title(self):
    pyperclip.copy(self.title)

  def get_ref(self):
    pyperclip.copy(self.ref)

  def copy_to_00png(self, scale):
    im = ImageGrab.grabclipboard()
    if im.getpixel((0, im.height - 1)) == (0,0,0,0):
        im = im.crop((0,0,im.width - 1, im.height - 2))
    if im is None:
      self.btn_apply.setText('Apply URL: 뭔가 잘못 카피한 거 아님?')
      return
    if self.overwrite_chk.isChecked():
      save_filename = '00.png'
    else:
      idx = 0
      while True:
        save_filename = '00-' + str(idx) + '.png'
        if not os.path.exists(base_dir() + save_filename):
          break
        else:
          idx = idx + 1
    im = im.resize((round(im.width * scale) , round(im.height * scale) )) if scale != 1.0 else im
    im.save(base_dir() + save_filename)
    del im
    im = None
    #gc.Collect()
    self.textbox_log.append("saved to " + save_filename)

  def del_temp_pics(self):
    files = os.listdir(base_dir())
    for file in files:
      if re.match('^[0-9][0-9][-_]?(\.webp)?[-_]?[0-9]*\.(jpg|JPG|gif|GIF|jfif|jpeg|png|PNG|mp4)$', file):
        #os.system(f"del {file}")
        os.remove(os.path.join(base_dir(), file))
    self.textbox_log.append("\n deleted temp pics")
  
  def crop_img(self, filename, img_src, cropsize = 16384, default_search_size = 1500):
    print(f'cropping {filename} ...')
    file_ext= re.search('[.](jpg|png|jpeg)$', filename).group(0)
    if img_src is None:
      img_src=cv2.imread(filename, cv2.IMREAD_COLOR)
    height, width, channel = img_src.shape
    y=0
    i=0
    while y < height:
      next_cand = min(height, y + cropsize)
      if next_cand < height:
        # 흰색으로 가로지르는 영역이 있을만한 곳을 찾음
        found = -1 
        for finding_y in range(next_cand - 1, next_cand - default_search_size, -1): # default_search_size 범위로 찾음
          flag = 0
          for finding_x in range(0,width):
            [r,g,b] = img_src[finding_y,finding_x]
            if r < 250 or g < 250 or b < 250:  # 흰색의 정의 : RGB 모두 250 이상
              flag = 1  # 흰색아님
              break
          if flag == 0: # 흰색으로 가로지르는 y좌표 발견
            found = finding_y
            break
        if found > -1:
          next_cand = found
      print(next_cand)
      dst= img_src[y:next_cand, 0:width]
      dst_filename = re.sub(file_ext + '$', '-' + str(i) + file_ext, filename)
      #cv2.imwrite(dst_filename, dst)
      result, image_buf = cv2.imencode(file_ext, dst)
      with open(dst_filename, mode='w+b') as f:
        image_buf.tofile(f)
      y = next_cand
      i = i + 1
      self.textbox_log.append(f'\n saved {dst_filename}')

  def copy_video_attr(self):
      current_text = pyperclip.paste().strip()
      print(current_text)
      video_attr= 'controls="" style="max-width:100%"'
      if not current_text:
          pyperclip.copy(video_attr)
      elif re.match("http.*\.mp4(\?.*)?", current_text):
              pyperclip.copy(f'<video {video_attr}><source src="{current_text}"/></video>')
      else:
          m = re.match('<video ([^>]*)(>.*</video>)', current_text, re.DOTALL)
          if m:
              m2 = re.match('.*(src="[^"]+").*', m.group(1))
              if m2:
                  pyperclip.copy(f'<video {video_attr} {m2.group(1)} {m.group(2)}')
              else:
                  pyperclip.copy(f'<video {video_attr}{m.group(2)}')
          else:
              pyperclip.copy(video_attr)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    # test
    #import pathlib
    #path = pathlib.Path(__file__).parent / "mp4.py"
    #print(path)
    sys.exit(app.exec_())
