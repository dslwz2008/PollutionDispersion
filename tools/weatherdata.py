# -*-coding:utf-8-*-
# Author: Shen Shen
# Email: dslwz2002@163.com
__author__ = 'Shen Shen'

import os
import sys
import pymongo
import requests
import requests.exceptions
import xml.etree.cElementTree as ET
from qqmail import *
from datetime import datetime,timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

RAWDATA='rawdata/'
INVALIDDATA=-999
mail_list = ['67070868@qq.com', ]
mail_ins = QQMail("584544233", "dslwz020415")

def tryParse(t, value, min, max):
    try:
        val = t(value)
        if val < min or val > max:
            return INVALIDDATA
        return val
    except ValueError:
        return INVALIDDATA


# 请求url，获取原始字符串，保存一份到原始文件，并返回字符串
def get_raw_data(url,cid):
    try:
        r = requests.get(url)
        rawstr = r.text.encode('utf-8')
        filename = '%s%s-%s.xml' % (RAWDATA, datetime.now().strftime('%Y%m%d%H'), cid)
        with open(filename, 'w') as fp:
            fp.write(rawstr)
        return rawstr
    except requests.exceptions.RequestException, e:
        # hadnle exception
        print(e.message)
        mail_ins.send(mail_list, "get_raw_data error", e.message)
        return None

# 对原始xml字符串进行解析，并返回json格式
def save_weather_data(rawstr):
    try:
        root = ET.fromstring(rawstr)
        result = {}
        result['countyid'] = tryParse(int, root.attrib['id'], 0, sys.maxint)
        result['ptime'] = datetime.strptime(root.attrib['ptime'],'%y-%m-%d %H:%M')
        result['city'] = root.attrib['city']
        child = root[0]# 只要最新的一条记录
        result['hour'] = tryParse(int, child.attrib['h'], 0, 23)
        result['wd'] = tryParse(int, child.attrib['wd'], -50, 50)
        result['fx'] = tryParse(int, child.attrib['fx'], 0, 360)
        result['fl'] = tryParse(int, child.attrib['fl'], 0, 15)
        result['js'] = tryParse(float, child.attrib['js'], 0, 2000.0)
        result['sd'] = tryParse(int, child.attrib['sd'], 0, 100)
        # establish a connection to the database
        with pymongo.MongoClient('localhost', 27017) as client:
            coll = client['weather']['beijing']
            coll.insert_one(result)
    except Exception,e:
        print(e.message)
        mail_ins.send(mail_list, "get_raw_data error", e.message)
        return None

def gen_url():
    ids = []
    urls = []
    base = 'http://flash.weather.com.cn/sk2/%s.xml'
    with open('ids.txt', 'r') as fp:
        for line in fp:
            idstr = line.splitlines()[0]
            ids.append(idstr)
            urls.append(base % idstr)
    return urls,ids

def worker():
    urls,cids = gen_url()
    for idx in range(len(urls)):
        print('handling %s, url: %s' % (cids[idx], urls[idx], ))
        save_weather_data(get_raw_data(urls[idx], cids[idx]))

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(worker, 'interval', hours=1, start_date=datetime.now()+timedelta(seconds=2))
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
