import os
import requests
import time
import random

MAX_LEN = 300

HEADERS = {
    'Accept':'application/json, text/plain, */*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
    'Host':'www.uooc.net.cn',
    'Origin':'http://www.uooc.net.cn',
    'Proxy-Connection':'keep-alive',
    'Referer':'http://www.uooc.net.cn/learn/index',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Cookie': 'uinfo=XbVIAfQqz0Y4uyps55hM0nHNS9QrI1AQdpxcf0QXWFQWz9wvJwD%2F2tEqdHiEC1nSLPs8EQLCl%2FjiXJblH1xNXIny; account=2592324965@qq.com; JSESSID=qft173qh0geurmoar6179dn7i6; _xsrf=74ec887520d113416054148fd9f1162c; user_ad_view_218.17.207.118=1; Hm_lvt_d1a5821d95582e27154fc4a1624da9e3=1505808995,1506492947,1507532618,1507535052; Hm_lpvt_d1a5821d95582e27154fc4a1624da9e3=1507535813; Hm_lvt_7c307a902207c45c0eaf86510e2c24a1=1505638725,1505709853,1506492953,1507532624; Hm_lpvt_7c307a902207c45c0eaf86510e2c24a1=1507535815'
}

DATA = {
    'chapter_id':'491018602',
    'cid':'528604875',
    'hidemsg_':'true',
    'network':'4',
    'resource_id':'417613408',
    'section_id':'1548174271',
    'subsection_id':'1993299670',
    'video_length':str(300+random.random()),
    'video_pos':'0',

}
session = requests.Session()
url = 'http://www.uooc.net.cn/learn/index#/528604875/491018602/1548174271/283226613/1682507818/subsection'
url = 'http://www.uooc.net.cn/learn/mark'


def data_in_url(url):
    pass

video_pos = 0


while video_pos<MAX_LEN:
    plus_pos = 30+random.random()
    video_pos += plus_pos
    DATA['video_pos'] = str(video_pos)
    answer = session.post(url=url,data = DATA,headers = HEADERS)
    print(plus_pos,video_pos)
    print(answer.json())
    time.sleep(plus_pos)

