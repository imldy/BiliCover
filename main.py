# 作者：三级狗
# 链接：https://www.zhihu.com/question/308600767/answer/1412824962
# 来源：知乎
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

import _thread
import requests
import json
import urllib
import random

x = 1


def down_image(Threadname, video):
    global x
    file_name = video['title'].replace("\\", "").replace("/", "").replace("r", "").replace(":", "").replace("*", "") \
        .replace("?", "").replace("\"", "").replace("<", "").replace(">", "").replace("|", "")
    urllib.request.urlretrieve("http:" + video['pic'], 'image-Thread/%s.jpg' % file_name)
    print("{} Downloading image No.{} {}".format(Threadname, x, file_name))
    x += 1


def get_images(url):
    headers = {
        'Usar-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}
    res = requests.get(url, headers=headers, timeout=(0.5, 1))
    for video in res.json()['data']['list']['vlist']:
        # 创建两个线程
        try:
            _thread.start_new_thread(down_image, ("new-Thread", video,))
        except:
            print("Error: 无法启动线程")


def go(UP_UID, page_range_min, page_range_max):
    for page in range(page_range_min, page_range_max):
        print("正在进行第{}页".format(page))
        url = 'https://api.bilibili.com/x/space/arc/search?mid={}&ps=30&tid=0&pn={}&keyword=&order=pubdate&jsonp=jsonp' \
            .format(UP_UID, page)
        get_images(url)


if __name__ == '__main__':
    UP_UID = 72956117  # UP主的UID
    page_range_min = 1  # 查看UP主投稿视频页数，确定最大限制页码
    page_range_max = 10  # 查看UP主投稿视频页数，确定最大限制页码
    go(UP_UID, page_range_min, page_range_max)
    while 1:
        pass
