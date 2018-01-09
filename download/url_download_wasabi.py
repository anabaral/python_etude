import urllib.request
import re, os
#from multiprocessing import Pool
from multiprocessing import Process

urlbase = 'http://wasabisyrup.com/'
urlpart = 'archives/1711974'

downloadbase = 'e:/download/1'

#process_pool = Pool(6)

def pic_download_by_url(pic_url, dl_path):
    print(pic_url + " --> " + dl_path)
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"),
                         ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")]
    urllib.request.install_opener(opener)
    try:
        #urllib.request.urlretrieve(pic_url, dl_path)
        req = urllib.request.Request(pic_url)
        pic_data = urllib.request.urlopen(req)
        with open(dl_path, 'wb') as output:
            output.write(pic_data.read())
        return 0  # success
    except Exception as e:
        print ("Error processing " + pic_url + " with " + str(e))
        return -1




if __name__ == '__main__':
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"),
                         ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")]
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
    task_list = []
    for mo in re.finditer('data-src="([^"]+)"', content):
        pic_urlpart = mo.group(1)
        pic_url = urlbase + mo.group(1)
        download_filename = '{:03d}'.format(cnt) + ".jpg"
        #print (pic_url + " --> " + download_filename)
        #pic_download_by_url(pic_url, downloaddir + "/" + download_filename)
        task_list.append((pic_url, downloaddir + "/" + download_filename))
        cnt = cnt + 1

    #result = process_pool.map(pic_download_by_url, task_list)
    #print(result)
    processes = []
    for task in task_list:
        p = Process(target=pic_download_by_url, args=task)
        processes.append(p)
    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()