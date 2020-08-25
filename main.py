# 作者：三级狗
# 链接：https://www.zhihu.com/question/308600767/answer/1412824962
# 来源：知乎
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

import _thread
import http
import requests
import json
import urllib
import random
import re
import os

x = 1


def down_image(Threadname, video):
    global x
    file_name = video['title'].replace("\\", "").replace("/", "").replace("r", "").replace(":", "").replace("*", "") \
        .replace("?", "").replace("\"", "").replace("<", "").replace(">", "").replace("|", "")
    author = video["author"]
    full_file_name = 'image-{}/{}.jpg'.format(author, file_name)
    full_url = "http:" + video['pic']
    try:
        urllib.request.urlretrieve(full_url, full_file_name)
        print("{} Downloading image No.{} {}".format(Threadname, x, file_name))
        x += 1
    except urllib.error.ContentTooShortError or http.client.RemoteDisconnected:
        print('Network conditions is not good. Reloading...')
        down_image(Threadname, video)


def get_images(url):
    headers = {
        'Usar-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}
    res = requests.get(url, headers=headers)
    for video in res.json()['data']['list']['vlist']:
        # 创建线程
        try:
            _thread.start_new_thread(down_image, ("new-Thread", video,))
        except:
            print("Error: 无法启动线程")


def go(UP_UID, page_range_min, page_range_max):
    UP_index_url = "https://space.bilibili.com/{}".format(UP_UID)
    res = requests.get(UP_index_url)
    UP_name = re.findall(re.compile('<title>(.*?)的个人空间 - 哔哩哔哩'), res.text)[0]
    print(UP_name)
    # 判断目录是否存在，不存在则创建
    directory = "image-{}".format(UP_name)
    if not os.path.isdir(directory):
        print("Makeing directory……")
        os.makedirs(directory)
    for page in range(page_range_min, page_range_max + 1):
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
