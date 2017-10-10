import os
import requests
import time
import random

MAX_LEN = 1000
url = 'http://www.uooc.net.cn/learn/mark'

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
    'chapter_id':491018602,
    'cid':'528604875',
    'hidemsg_':'true',
    'network':None,
    'resource_id':528604875,
    'section_id':769598456,
    'subsection_id':114162405,
    'video_length':MAX_LEN,
    'video_pos':'0',
}
# {'cid': '528604875', 'chapter_id': 491018602, 'section_id': 1548174271, 'subsection_id': 1421668107, 'resource_id': 1556002726, 'finished': 0, 'name': '9.5.4\xa0JCheckBox'}
# {'cid': '528604875', 'chapter_id': 491018602, 'section_id': 1548174271, 'subsection_id': 896107628, 'resource_id': 324658684, 'finished': 0, 'name': '9.5.5\xa0JComboBox'}
# {'cid': '528604875', 'chapter_id': 491018602, 'section_id': 1548174271, 'subsection_id': 190274881, 'resource_id': 1475629874, 'finished': 0, 'name': '9.5.6\xa0JTextField&JPasswordField'}
# {'cid': '528604875', 'chapter_id': 491018602, 'section_id': 769598456, 'subsection_id': 114162405, 'resource_id': 528604875, 'finished': 0, 'name': '9.6.4 习题'}

def watch_class():
    session = requests.Session()
    # for every_class
    video_pos = 0
    while video_pos<MAX_LEN:
        plus_pos = 30+random.random()
        video_pos += plus_pos
        DATA['video_pos'] = str(video_pos)
        DATA['network'] = random.choice(['4', '3'])
        answer = session.post(url=url,data = DATA,headers = HEADERS).json()
        print(answer)
        if_break = answer['data']['finished'] == 1 or answer['code'] == 103
        if if_break:
            break
        print(plus_pos,video_pos)
        print(answer)

        time.sleep(plus_pos)

if __name__=='__main__':
    print(self.url)