import requests
from bs4 import BeautifulSoup
import time
import datetime
import os
import socket

# proxyPool = {
#
#     'http':'http://'+'',
#     'https':'https://'+'113.116.50.182:808'
#
# }
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
    except requests.exceptions.ConnectionError as e:
        print(e)

    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'lxml')  # .prettify()

    src = soup.find('ul',id = 'hgallery').find('img').get('src')
    src = src[:-5]
    pics_num = soup.find('div',id = 'dinfo').find('span').string
    pics_num = int(pics_num[:-3])
    album = soup.find('div',class_ = 'albumTitle').find('h1').string

    srcs = []
    srcs.append(str(src+'0.jpg'))
    for s in range(pics_num-1):
        srcs.append(''.join([src,str(s+1).rjust(3,'0')+'.jpg']))
    print(f'专辑名:\n{album}')
    print(f'图片数量:{pics_num}')


    path_0 = r'X:\百度云下载\Girls\\'  # 设置图片的保存地址
    path_1 = ''.join([path_0,str(album)])+r'\\'.replace('/',',')

    if not os.path.isdir(path_1):
        os.makedirs(path_1)  # 判断没有此路径则创建

    return srcs,path_1,pics_num


def get_pics(srcs,path):  # ,getHowMany
    """
    下载器:下载图片，出错时尝试解决，重新下载被跳过的图片  # 多线程下载

    """
    dowCount = 0
    pathExist = 0
    field_srcs = {}
    for s in srcs:
        k = srcs.index(s) + 1
        path_exist = os.path.exists(path+f'{k}.jpg')
        try:
            if not path_exist:
                if not path_exist:
                    if k % 10 == 0 or k == picsNum:
                        print(f'正在下载{k}/{picsNum}...',end = '')
                pic = requests.get(s,timeout = 10,headers = header,allow_redirects = False)
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
        # time.sleep(1)

    if picsNum-dowCount and pathExist:
        print(f'\n下载完成！共{dowCount}张图片,未下载{picsNum - dowCount}张(已存在{pathExist}张)')  # ({fieldSrcsNum}张失败)
    else:
        print(f'\n下载完成！共{dowCount}张图片')

def get_pics_threading(src):

    pass

if __name__ == '__main__':

    i = 0
    urls = []
    with open('nvshens.txt', 'r') as f:
        for line in f:
            urls.append(line.strip())

    for url in urls:
        header = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Referer': url
        }

        print('\n')
        print(f'============任务{urls.index(url)+1}============')
        srcs, path, picsNum = get_html_info(url)

        d1 = time.time()
        get_pics(srcs,path)
        d2 = time.time()

        print('总计用时:%.2fs' % (d2 - d1))
        print('\n结束时间：', datetime.datetime.now().strftime('%R'))
        i += 1

        if urls.index(url)+1 != len(urls):
            print('下载冷却中...')
            for s in range(120, 0, -1):
                mytime = f'\r倒计时 {s} 秒'
                print(mytime, end = '')
                time.sleep(1)
