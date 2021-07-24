# coding=utf-8
import top.api
import json
import datetime
from top.api.base import TopException

url = 'gw.api.taobao.com'
appkey = '29144250'
secret = '952c5db99521878b431a542119de3839'
sessionkey = '6101d25998dffad3c9c8f10bfd62a25561db478478c45d72200678018680'
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



