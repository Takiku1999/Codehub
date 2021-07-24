# coding=utf-8
'''
此为python2文件，在TOPUI.py中通过dos指令运行
'''
import top.api
import json
import datetime
from top.api.base import TopException

url = 'gw.api.taobao.com'
appkey = ''
secret = ''
sessionkey = ''
port = 80

try:
    req = top.api.TradesSoldGetRequest(url,port)
    req.set_app_info(top.appinfo(appkey,secret))
    req.fields = "tid,status,payment,orders"

    resp = req.getResponse(sessionkey)
    with open('Datas/{}{}.json'.format('SummaryTable', datetime.date.today()), 'w') as jsonobj:
        json.dump(resp, jsonobj)

except TopException:
    print('本机IP不在响应服务器的白名单中')



