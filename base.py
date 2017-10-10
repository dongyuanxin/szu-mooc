import re
import os
import json
import requests
import random
import time

HEADER_FILE = os.path.join("config",'header.json')
LOG_FILE = os.path.join("log","unfinish.txt")

MAX_LEN = 1000
URL = 'http://www.uooc.net.cn/learn/mark'
CID = None

DATA = {
    'chapter_id':491018602,
    'cid':None,
    'hidemsg_':'true',
    'network':None,
    'resource_id':528604875,
    'section_id':769598456,
    'subsection_id':114162405,
    'video_length':MAX_LEN,
    'video_pos':'0',
}

HEADERS = {
    'Accept':'application/json, text/plain, */*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
    'Host':'www.uooc.net.cn',
    'Origin':'http://www.uooc.net.cn',
    'Proxy-Connection':'keep-alive',
    'Referer':'http://www.uooc.net.cn/learn/index',
    #'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    #'Cookie': 'uinfo=XbVIAfQqz0Y4uyps55hM0nHNS9QrI1AQdpxcf0QXWFQWz9wvJwD%2F2tEqdHiEC1nSLPs8EQLCl%2FjiXJblH1xNXIny; account=2592324965@qq.com; JSESSID=qft173qh0geurmoar6179dn7i6; _xsrf=74ec887520d113416054148fd9f1162c; user_ad_view_218.17.207.118=1; Hm_lvt_d1a5821d95582e27154fc4a1624da9e3=1505808995,1506492947,1507532618,1507535052; Hm_lpvt_d1a5821d95582e27154fc4a1624da9e3=1507535813; Hm_lvt_7c307a902207c45c0eaf86510e2c24a1=1505638725,1505709853,1506492953,1507532624; Hm_lpvt_7c307a902207c45c0eaf86510e2c24a1=1507535815'
    'User-Agent':None,
    'Cookie':None,
}

def reload():
    global CID,HEADERS
    fin = open(HEADER_FILE, 'r')
    header = json.load(fin)
    fin.close()
    HEADERS['User-Agent'] = header['User-Agent']
    HEADERS['Cookie'] = header['Cookie']
    CID = header['cid']
    return None

def get_data(cid):
    url = "http://www.uooc.net.cn/learn/getCatalogList?cid=%s&hidemsg_=true&show=" % (cid)
    url_json = requests.get(url=url,headers = HEADERS).json()['data']
    data = {'cid':cid}
    for unit in url_json:
        data['chapter_id'] = unit['id']
        if 'children' not in unit.keys():
            continue
        for chapter in unit['children']:
            if 'children' in chapter.keys(): # 每一节有多个情况
                for every_class in chapter['children']:
                    if len(every_class['icon_list'])==0:
                        continue
                    data['section_id'] = every_class['pid']
                    data['subsection_id'] = every_class['id']
                    data['resource_id'] = every_class['icon_list'][0]['id']
                    data['finished'] = every_class['finished']
                    data['name'] = every_class['name']
                    if data['finished']!=1:
                        yield data
                    # print(data)
            else:
                for every_class in chapter['icon_list']:
                    data['resource_id'] = every_class['id']
                    data['section_id'] = chapter['pid']
                    data['subsection_id'] = chapter['id']
                    data['finished']= chapter['finished']
                    data['name'] = chapter['name']
                    if data['finished']!=1:
                        yield data

def log_unfinish(class_name):
    info = "%s 可能需要您手动完成 \n" % class_name
    with open(LOG_FILE,'a',encoding="utf-8") as fout:
        fout.write(info)

def watch():
	return_top = False
	while not return_top:
		session = requests.Session()
		reload()
		class_set = get_data(CID)
		for _class in class_set:
			print("Watch",_class['name'])
			DATA['network'] = random.choice(['4', '3'])
			DATA['cid'] = CID
			DATA['chapter_id'] = _class['chapter_id']
			DATA['resource_id'] = _class['resource_id']
			DATA['subsection_id'] = _class['subsection_id']
			DATA['section_id'] = _class['section_id']
			if_log = False
			video_pos = 0
			check_pos = [0.65] # 复查点，防止传包过于频繁！！！
			while video_pos < MAX_LEN:
				if len(check_pos) and video_pos > MAX_LEN * check_pos[-1]:
					unfinish_id_list = []
					time.sleep(5) # 等待服务器缓冲
					next_class = get_data(CID)
					check_pos.pop()
					for i in next_class:
						unfinish_id_list.append(i['resource_id'])
					if _class['resource_id'] not in unfinish_id_list:
						print(" " * 8 + "start watching next")
						break
					else:
						print(" " * 8 +str(_class['resource_id'])+str(unfinish_id_list))
				plus_pos = 30 + random.random()
				video_pos += plus_pos
				try:
					DATA['video_pos'] = str(video_pos)
					answer = session.post(url=URL, data=DATA, headers=HEADERS).json()
					print("    At",video_pos,"(after plus",plus_pos,"seconds )")
					print("    Return",answer)
					if answer['data']['finished'] == 1:
						break
					if answer['code'] ==103 or len(answer['msg'])>0:
						if_log = True
						break
					if answer['msg'] == '视频进度不能拖拽'
						return_top = True
						break
				except Exception as error:
					print("    error is:",error)
					if_log = True
					break
				time.sleep(plus_pos+random.choice([0.5,1.0,2.0]))
			if return_top:
				print("="*8,"重新开始","="*8)
				return_top = False
				time.sleep(30)
				break
			if if_log:
				log_unfinish(_class['name'])
		return_top = True
	print("Watch all classes in Mooc")
	
if __name__=='__main__':
    watch()
