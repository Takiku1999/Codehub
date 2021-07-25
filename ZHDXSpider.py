import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pymongo.mongo_client import MongoClient
import pymongo.errors
import pprint
from datetime import datetime
import time
from multiprocessing import Process,Lock,Pool
from openpyxl import load_workbook

def spider_for_bd():
    url = 'http://top.baidu.com/category?c=513&fr=topindex'

    strhtml = requests.get(url)
    strhtml.encoding = strhtml.apparent_encoding

    soup = BeautifulSoup(strhtml.text,'lxml')
    news_box = soup.find_all('h2')[0]
    all_topics = news_box.find_parent('div',class_ = 'box-cont')

    for i in range(0, 10):
        result = {}
        result['title'] = all_topics.find_all('a',class_ = 'list-title')[i].string  # 10
        add_data(result)
    for l in range(0,len(all_topics.find_all('span',class_ = 'icon-rise'))):
        result = {}
        result['heat'] = all_topics.find_all('span',class_ = 'icon-rise')[l].string  # 9
        add_data(result)
    for o in range(0,len(all_topics.find_all('span',class_ = 'icon-fall'))):
        result = {}
        result['heat'] = all_topics.find_all('span',class_ = 'icon-fall')[o].string  # 1
        add_data(result)

def spider_for_sc(a,b):
    result = {}
    url = 'https://www.shanghairanking.cn/rankings/bcur/2020'
    # strhtml = requests.get(url)
    # strhtml.encoding = strhtml.apparent_encoding  # 修改解码方式防止乱码
    # soup = BeautifulSoup(strhtml.text, 'lxml')  # 将lxml解析器解析到的网页标签储存到soup变量

    url_local = 'file:///Y:/PyCharm%20Community%20Edition%202019.3.2/My_Code/Spider/index.html'
    strhtml = urlopen(url_local)  # 获取网页标签
    soup = BeautifulSoup(strhtml,'lxml')

    # with open('index.html','w',encoding = 'utf-8') as f:
    #     f.write(str(soup))

    # print(f'Process {name} is now running...')
    f = load_workbook('result.xlsx')
    sheet = f.active
    sheet['A1'].value = '排名'
    sheet['B1'].value = '校名'
    sheet['C1'].value = '所在地'
    sheet['D1'].value = '分数'

    for i in range(a, b):
        result['_id'] = i + 1
        tag_a = soup.select('td')[i*6+1]
        result['name'] = tag_a.find('a').string.strip()
        result['area'] = soup.find_all('td')[i*6+2].string.strip()
        result['score'] = soup.find_all('td')[i*6+4].string.strip()

        # add_data(result)
        # lock.acquire()

        ranking = 'A'+str(i+2)
        name = 'B'+str(i+2)
        area = 'C'+str(i+2)
        score = 'D'+str(i+2)
        sheet[ranking].value = result['_id']
        sheet[name].value = result['name']
        sheet[area].value = result['area']
        sheet[score].value = float(result['score'])

        # lock.release()

    f.save('result.xlsx')

    f.close()

# ======================
def add_data(dic):
    mongoCollection.insert_one(dic)

def check_data():
    i = 0
    for get in mongoCollection.find():  # {'_id':1}
        pprint.pprint(get)
        i += 1
    if i == 0:
        print('\n***数据库为空***')
    else:
        print('\n@总计:', i,'条数据')

def del_data():
    mongoCollection.remove()  # delete_many({'_id':1})
# ======================

if __name__ == '__main__':

    # lock = Lock()

    try:
        mongoClient = MongoClient('localhost', 27017)
        print('\n***连接数据库成功***')

        mongoDatabase = mongoClient.site
        mongoCollection = mongoDatabase.myDB

    except pymongo.errors.PyMongoError as e:
        print('fatal error:', e)

    while 1:
        print("\n===数据库模式===")

        n = input("\n选择操作 a/c/d/cc:\n--按q退出--\n> ")

        if n == 'c':
            check_data()
            continue
        elif n == 'a':

            d1 = time.time()
            print('开始时间：',datetime.now())
            print('\n爬取中...')

            pool = Pool()
            for i in range(2):
                pool.apply_async(spider_for_sc,(i*6,i*5+5))
            pool.close()
            pool.join()

            # spider1 = Process(target = spider_for_sc, args = (0, 5))
            # spider2 = Process(target = spider_for_sc, args = (6, 10))
            # spider1.start()
            # spider2.start()
            # spider1.join()
            # spider2.join()

            i = 0
            for get in mongoCollection.find():
                i += 1
            if i == 0:
                print('\n***未添加任何数据***')
            else:
                print('\n***添加数据成功***')
                print('\n@总计:', i, '条数据')
            d2 = time.time()
            print('结束时间：',datetime.now(),'\n总计用时:%.2fs' % (d2-d1))

            continue
        elif n == 'd':
            del_data()
            print('\n***删除数据成功***')

            continue
        elif n == 'cc':
            import subprocess
            r = subprocess.call(["Y:\PyCharm Community Edition 2019.3.2\My_Code\Spider\\result.xlsx"])
            # print('Exit code',r)

            continue
        elif n == 'q':
            exit()

