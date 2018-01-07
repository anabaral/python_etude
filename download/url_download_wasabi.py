import urllib.request
import re, os

urlbase = 'http://wasabisyrup.com/'
urlpart = 'archives/1711974'

downloadbase = 'e:/download/1'

#headers = {}
#headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0")]
urllib.request.install_opener(opener)

url = urlbase + urlpart
req = urllib.request.Request(url)
data = str(urllib.request.urlopen(req).read(), encoding="UTF-8")

title = re.search('<title>(.*)</title>', data).group(1)
title = re.sub(" *\|.*", "", title)

print("TITLE: " + title)
downloaddir = downloadbase + "/" + title
if not os.path.exists(downloaddir):
    os.makedirs(downloaddir)


cnt=1
content = data[data.find('<div class="gallery-template">') : data.find('<div id="gallery_vertical"')]
for mo in re.finditer('data-src="([^"]+)"', content):
    pic_urlpart = mo.group(1)
    pic_url = urlbase + mo.group(1)
    download_filename = '{:03d}'.format(cnt) + ".jpg"
    print (pic_url + " --> " + download_filename)
    urllib.request.urlretrieve(pic_url, downloaddir + "/" + download_filename)
    cnt = cnt + 1


