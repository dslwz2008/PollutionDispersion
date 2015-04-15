# -*-coding:utf-8-*-
# Author: Shen Shen
# Email: dslwz2002@163.com
__author__ = 'Shen Shen'

import json
import os
import pymongo
import datetime

DATAPATH='D:/data/pm2.5/dailydata/'

# 示例数据
'''
{
    "Date_Time":"2015-1-7 0:00:00",
    "Station":"植物园",
    "Pollutant":"SO2",
    "Value":"24.3",
    "IAQI":"9",
    "QLevel":"一级",
    "Quality":"优",
    "PriPollutant":"PM10",
    "AQI":"39",
    "Avg24h":"11.6",
    "RealTimeQL":"一级",
    "FaceSign":"1",
    "Over24h":"2,2,2,2,2,2,6,12,17,17,10,13,10,13,16,16,15,14,16,18,22,24,24"
}
'''

def json2mongodb():
    # establish a connection to the database
    with pymongo.MongoClient('localhost', 27017) as client:
        coll = client['pm25']['beijing']
        filenames = os.listdir(DATAPATH)
        for n in filenames:
            obj = json.load(open(DATAPATH + n))
            datas = obj['Table']
            for d in datas:
                result = {}
                result['DateTime'] = datetime.datetime.strptime(d['Date_Time'],'%Y-%m-%d %H:%M:%S')
                result['Station'] = d['Station']
                result['Pollutant'] = d['Pollutant']
                result['Value'] = float(d['Value'])
                result['IAQI'] = int(d['IAQI'])
                result['QLevel'] = d['QLevel']
                result['Quality'] = d['Quality']
                result['PriPollutant'] = d['PriPollutant']
                result['AQI'] = int(d['AQI'])
                result['Avg24h'] = float(d['Avg24h'])
                result['RealTimeQL'] = d['RealTimeQL']
                result['FaceSign'] = int(d['FaceSign'])
                result['Over24h'] = d['Over24h']
                coll.insert(result)


if __name__ == '__main__':
    json2mongodb()