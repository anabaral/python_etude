import re, sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QTextEdit, QFileDialog
from PyQt5.QtCore import Qt
from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import validators

import subprocess
import hashlib
import pyperclip
from PIL import ImageGrab
import cv2
import numpy as np
from http.client import InvalidURL

current_loc = os.getcwd()

def base_dir():
  return current_loc + "\\"

# you need
# pip install pyqt5


def get_url(given_url):
  if not given_url.startswith("http") :
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

    btn_apply = QPushButton('Apply URL')
    btn_apply.clicked.connect(self.apply_url)
    vbox.addWidget(btn_apply)

    self.btn_title = QPushButton()
    self.btn_title.setText('title')
    self.btn_title.clicked.connect(self.get_title)
    self.btn_title.setStyleSheet("background-color: #cc9")
    vbox.addWidget(self.btn_title)
    
    self.btn_ref = QPushButton()
    self.btn_ref.setText('ref')
    self.btn_ref.clicked.connect(self.get_ref)
    self.btn_ref.setStyleSheet("background-color: #cc9")
    vbox.addWidget(self.btn_ref)
    
    self.btn_clip_png125 = QPushButton('Clip to 00.png(125%)')
    self.btn_clip_png125.clicked.connect(lambda: self.copy_to_00png(1.25))
    self.btn_clip_png100 = QPushButton('Clip to 00.png(100%)')
    self.btn_clip_png100.clicked.connect(lambda: self.copy_to_00png(1.0))
    
    hbox2 = QHBoxLayout()
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
    current_loc = dialog.getExistingDirectory(None, "Select Folder")
    self.loc.setText(current_loc)

  def apply_url(self):
    common_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}
    base_url = pyperclip.paste().strip()
    print("<<" + base_url + ">>")
    if not validators.url(base_url):
      self.btn_title.setText('뭔가 잘못 카피한 거 아님?')
      return

    req = Request(url=base_url,  headers=common_headers)
    
    res = urlopen(req)
    html = res.read().decode('cp949')
    
    bs = BeautifulSoup(html, 'html.parser')
    #print(html)
    # body가 빌 경우가 있네? 대기자료-->웃자 로 넘어가면
    if len(bs.select('body div')) < 1:
      self.btn_title.setText('body 내용이 없네요, 대기자료가 웃자로 넘어갔나?')
      return
    
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
    
    ref_elts = bs.select('div#wrap_cbay_new table a')
    for ref_elt in ref_elts:
      if ref_elt.text:
        refs.append(ref_elt.text)
    self.ref = '\n'.join(refs)
    print(self.ref)

    self.btn_ref.setText(f"{self.ref}")
    
    logs = []
    pic_img_urls = []
    pic_img_elts = bs.select('div#cnts div.simple_attach_img_div img')
    pic_img_elts.extend(bs.select('div#cnts table div.comment_img_div img'))
    pic_img_elts.extend(bs.select('div#cnts div.body_editor img'))
    pic_img_elts.extend(bs.select('div#cnts div#wrap_img img'))
    for pic_img_elt in pic_img_elts:
      try:
        img_url = get_url(pic_img_elt['src'])
      except KeyError:
        import os
        #print("no src attr??" + str(pic_img_elt))
      #print(img_url)
      pic_img_urls.append(img_url)
    
    webp_exists=False
    cnt=1
    md5sums=[]
    for each_img_url in pic_img_urls:
      if not each_img_url:
        continue
      from os import path
      each_img_ext = path.splitext(each_img_url)[1]
      if each_img_ext == '.webp':
        webp_exists=True
      to_filename = base_dir() + ("%2.2d"% cnt) + each_img_ext
      #urlretrieve(each_img_url, filename= to_filename )
      headers = {'Referer': 'http://web.humoruniv.com/', 
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
               + ' Chrome/91.0.4472.114 Safari/537.36'}
      req = Request(each_img_url, b'{}', headers, method="GET")
      try:
        data = urlopen(req).read()
      except InvalidURL as e:
        logs.append("failed to retrieve invalid url : " + each_img_url)
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
        # check cropsize
        if not to_filename.endswith('.gif'):
          encoded_img = np.frombuffer(data, dtype = np.uint8)
          img_org = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
          height, width, channel = img_org.shape
          if width >= 8192 :
            logs.append(f'width >= 8192 need to be manually processed')
          elif width > 800 and height >= 8192:
            logs.append('pic will be cropped...')
            self.crop_img(to_filename, img_src = img_org, cropsize = 8192)
          data = None
          encoded_img = None
          img_org = None
        
    self.textbox_log.setText('\n'.join(logs))
    if webp_exists:
      import os
      print('webp2jpg.bat')
      os.system('webp2jpg.bat')

  def get_title(self):
    pyperclip.copy(self.title)

  def get_ref(self):
    pyperclip.copy(self.ref)

  def copy_to_00png(self, scale):
    im = ImageGrab.grabclipboard()
    if im is None:
      self.btn_title.setText('뭔가 잘못 카피한 거 아님?')
      return
    im.resize((round(im.width * scale) , round(im.height * scale) )).save(base_dir() + '00.png')
    self.textbox_log.append("\n saved to 00.png")

  def del_temp_pics(self):
    files = os.listdir(base_dir())
    for file in files:
      if re.match('^[0-9][0-9][-_]?(\.webp)?[-_]?[0-9]*\.(jpg|gif|jfif|png|mp4)$', file):
        os.system(f"del {file}")
    self.textbox_log.append("\n deleted temp pics")
  
  def crop_img(self, filename, img_src, cropsize = 8192):
    import cv2
    import re
    print(f'cropping {filename} ...')
    file_ext= re.search('[.](jpg|png|jpeg)$', filename).group(0)
    if img_src is None:
      img_src=cv2.imread("01.jpg", cv2.IMREAD_COLOR)
    height, width, channel = img_src.shape
    y=0
    i=0
    while y < height:
      next = min(height, y + cropsize)
      dst= img_src[y:next, 0:width]
      dst_filename = re.sub(file_ext + '$', '-' + str(i) + file_ext, filename)
      cv2.imwrite(dst_filename, dst)
      y = next
      i = i + 1
      self.textbox_log.append(f'\n saved {dst_filename}')



if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = MyApp()
  # test
  #import pathlib
  #path = pathlib.Path(__file__).parent / "mp4.py"
  #print(path)
  sys.exit(app.exec_())
