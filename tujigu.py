import requests
from bs4 import BeautifulSoup
import time
import os
import re
import socket
import datetime

header = {
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
}
proxyPool = {

    'http':'http://'+'',
    'https':'https://'+'113.116.50.182:808'

}
url_local = r'file:/Y:/PyCharm Community Edition 2019.3.2/My_Code/Spider/html2.txt'

def get_html_info(u):
    """
    解析器：解析网页，获取专辑名，图片数量以及图片链接,创建本地下载路径
    #     提取链接的同时下载，提高效率
    #     使用代理ip避免屏蔽

    """

    response = ''
    try:
        print(f'目标地址:\n{u}')
        response = requests.get(u, headers = header)
        # print('Done')
    except requests.exceptions.ConnectionError as e:
        print(e)

    # print('解析网页...',end = '')
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'lxml')  # .prettify()
    # print('Done')

    # print('获取资源信息...',end = '')
    get_album = soup.find('div',class_ = 'content').find_all('img')  # 获取专辑名
    album = get_album[0].get('alt')[:-1]
    get_pics_num = soup.find('p', text = re.compile('图片数量'))  # 获取图片数量
    all_pics = int(get_pics_num.string[-4:-1])
    get_pics_url = get_album[0].get('src')

    srcs = []
    for s in range(all_pics):
        # srcs[s+1] = (''.join([get_pics_url[:-6], '/' + str(s + 1)]) + '.jpg')
        srcs.append(''.join([get_pics_url[:-6],'/'+str(s+1)])+'.jpg')  # 根据图片数量以及第一页的地址得出全部图片的链接
    # print('Done')
    print(f'专辑名:\n{album}')
    print(f'图片数量:{all_pics}')


    path_0 = r'X:\百度云下载\Girls\\'  # 设置图片的保存地址
    path_1 = ''.join([path_0,str(album)])+r'\\'.replace('/',',')

    # print('创建本地储存路径...',end = '')
    if not os.path.isdir(path_1):
        os.makedirs(path_1)  # 判断没有此路径则创建
    # print('Done\n')


    return srcs,path_1,all_pics


def get_pics(srcs,path):  # ,getHowMany
    """
    下载器:下载图片，出错时尝试解决，重新下载被跳过的图片  # 多线程下载

    """
    dowCount = 0
    pathExist = 0
    field_srcs = {}
    print('正在下载...\n')
    for s in srcs:
        k = srcs.index(s) + 1
        path_exist = os.path.exists(path+f'{k}.jpg')
        try:
            if not path_exist:
                if k % 10 == 0 or k == picsNum:
                    print(f'正在下载{k}/{picsNum}...',end = '')
                pic = requests.get(s,timeout = 10,headers = header)
                not_writalbe = False
            else:
                print(f'第{k}张已存在，跳过')
                pathExist += 1
                continue

        except requests.exceptions.ConnectionError:
            print(f'第{k}张连接失败，跳过')
            not_writalbe = True
            field_srcs[k] = s
            continue

        except socket.timeout:
            print(f'第{k}张下载超时，跳过')
            not_writalbe = True
            field_srcs[k] = s
            continue

        except requests.exceptions.ReadTimeout:
            print(f'第{k}张读取超时，跳过')
            not_writalbe = True
            field_srcs[k] = s
            continue

        if not not_writalbe:
            with open(f'{path}'+str(k)+'.jpg','wb') as file:
                file.write(pic.content)
                dowCount += 1
        if k % 10 == 0 or k == picsNum:
            print('Done!')

    if picsNum-dowCount and pathExist:
        print(f'\n下载完成！共{dowCount}张图片,未下载{picsNum - dowCount}张(已存在{pathExist}张)')  # ({fieldSrcsNum}张失败)
    else:
        print(f'\n下载完成！共{dowCount}张图片')

def get_pics_threading(src):

    pass

if __name__ == '__main__':

    urls = []
    with open('girls.txt', 'r') as urlfile:
        for line in urlfile:
            urls.append(line.strip())

    for url in urls:
        print('\n')
        print(f'============任务{urls.index(url)+1}============')
        srcs, path, picsNum = get_html_info(url)

        d1 = time.time()
        get_pics(srcs,path)
        d2 = time.time()

        print('总计用时:%.2fs' % (d2 - d1))
        print('\n结束时间：', datetime.datetime.now().strftime('%R'))

        if urls.index(url)+1 != len(urls):
            print('下载冷却中...')
            for s in range(300, 0, -1):
                mytime = f'\r倒计时 {s} 秒'
                print(mytime, end = '')
                time.sleep(1)

    with open('girls.txt','a') as f:
        f.write(f"\n结束时间：{datetime.datetime.now().strftime('%R')}")



