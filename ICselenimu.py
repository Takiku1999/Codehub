"""
1、文件io统一改为使用pandas #
2、配置文件读取改为使用configparser #
4、定义变量放到__init__下 #
5、多加注释 #
6、优化代码结构 #
7、修改搜索url：去掉搜索变量名中的逗号
调试方式：爬取全部页码
最终实现：爬100个型号的前两页

静态方法?不涉及对类属性操作的方法
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import configparser
import time

URL = 'https://www.ic.net.cn/'


def redConfig():
    """读取配置文件，返回表头"""

    config = configparser.ConfigParser()
    config.read('config.txt', encoding = 'utf-8')
    dataname = config.get('header', 'dataname').split(',')

    return dataname

def redCSV():
    """读取CSV文件，返回产品名称"""

    fileContent = pd.read_csv('ic0423.csv',encoding = 'gbk')
    # fileContent = fileContent.values.tolist()
    # productList = []
    # for i in fileContent:
    #     for j in i:
    #         productList.append(j)
    productList = fileContent['code']
    productFilename = fileContent['filename']
    productList = productList.values.tolist()
    productFilename = productFilename.values.tolist()

    return productList,productFilename

class SpiderIC:
    """
    通过redConfig()和redCSV()获取页数以及产品名称后传给getData()
    """

    def __init__(self,page_num,product_name,data_name):

        self.page_num = page_num
        self.product_name = product_name
        self.data_name = data_name

    def getData(self):
        """按页爬取一个产品的全部数据"""

        for page in range(1,self.page_num+1):

            # 翻页操作
            driver.get(f'https://www.ic.net.cn/search/{self.product_name}.html?page={page}')
            print(driver.current_url,page)

            # 调试选项，选择第x到第y条数据
            x = 4
            y = 6  # 53 in total
            rank = 0  # 声明变量，每条数据在本页的排名
            for i in range(x,y):

                qq1 = ''
                qq2 = ''
                i500 = ''
                date = ''
                product = ''
                factory = ''
                batchNum = ''
                totalNum = ''
                packaging = ''
                explain = ''
                place = ''
                iBrandStar = ''
                iYear = ''
                iICCP = ''
                iSSCP = ''
                iSTOCK = ''
                iVIP = ''
                iOriginal = ''
                iDaili = ''
                iHckc = ''
                iEvaluate = ''
                iPersonal = ''
                iconXianhuo = ''
                iconTuijian = ''
                iconYouxian = ''
                iconRemai = ''
                rank += 1
                time_ = time.strftime('%Y-%m-%d %H:%M:%S')

                # 获取基本信息
                # 若获取公司名称失败或为空，则跳过，可修复写入空数据的错误
                try:
                    company = driver.find_element_by_xpath(f'//*[@id="resultList"]/li[{i}]/div[2]/a').text
                except Exception:
                    continue

                try:

                    date = driver.find_element_by_xpath(f'//*[@id="resultList"]/li[{i}]/div[9]').text
                    product = self.product_name
                    factory = driver.find_element_by_xpath(f'//*[@id="resultList"]/li[{i}]/div[4]').text
                    batchNum = driver.find_element_by_xpath(f'//*[@id="resultList"]/li[{i}]/div[5]').text
                    totalNum = int(driver.find_element_by_xpath(f'//*[@id="resultList"]/li[{i}]/div[6]').text)
                    packaging = driver.find_element_by_xpath(f'//*[@id="resultList"]/li[{i}]/div[7]').text
                    explain = driver.find_element_by_xpath(f'//*[@id="resultList"]/li[{i}]/div[8]/div[1]').text
                    place = driver.find_element_by_xpath(f'//*[@id="resultList"]/li[{i}]/div[8]/div[2]').text
                    qq1 = driver.find_element_by_xpath(f'//*[@id="resultList"]/li[{i}]/div[10]/a[1]').get_attribute('title')
                    qq2 = driver.find_element_by_xpath(f'//*[@id="resultList"]/li[{i}]/div[10]/a[2]').get_attribute('title')


                except Exception:
                    pass

                # 查找 “SSCP、核查库存、500条、VIP、品牌之星、年度优秀认证、ICCP、STOCK、认证评估、原厂、代理” 图标
                try:
                    for j in range(1,5):
                        find_icon = driver.find_element_by_xpath(
                            f'//*[@id="resultList"]/li[{i}]/div[2]/p/a[{j}]').get_attribute('class')
                        if find_icon == 'sscp':
                            iSSCP = True
                        if find_icon == 'icon_hckc':
                            iHckc = True
                        if find_icon == 'icon500':
                            i500 = True
                        if find_icon == 'redvip':
                            iVIP = True
                        if find_icon == 'brandStar_icon':
                            iBrandStar = True
                        if find_icon == 'year_icon':
                            iYear = True
                        if find_icon == 'iccp':
                            iICCP = True
                        if find_icon == 'stock':
                            iSTOCK = True
                        if find_icon == 'renzheng_icon':
                            iEvaluate = True
                        # if find_icon == '':
                        #     iOriginal = True
                        # if find_icon == '':
                        #     iDaili =

                except Exception:
                    pass

                # 查找“优先”、“热卖”图标
                try:
                    for j in range(1,5):
                        find_icon2 = driver.find_element_by_xpath(
                            f'//*[@id="resultList"]/li[{i}]/div[3]/span[{j}]').get_attribute('class')
                        if find_icon2 == 'icon_youXian':
                            iconYouxian = True
                        if find_icon2 == 'icon_reMai':
                            iconRemai = True

                except Exception:
                    pass

                # 查找“推荐”图标
                try:
                    find_tuijian = driver.find_element_by_xpath(
                        f'//*[@id="resultList"]/li[{i}]/div[3]/a/span').get_attribute('class')
                    if find_tuijian == 'icon_tuiJian':
                        iconTuijian = True

                except Exception:
                    pass

                # 查找“现货排名”图标
                try:
                    find_xianhuo = driver.find_element_by_xpath(
                        f'//*[@id="resultList"]/li[{i}]/div[3]/a/span').get_attribute('class')
                    if find_xianhuo == 'icon_xianHuo':
                        iconXianhuo = True

                except Exception:
                    pass

                # 查找“个人”图标
                try:
                    find_geren = driver.find_element_by_xpath(
                        f'//*[@id="resultList"]/li[{i}]/div[2]/p/span').get_attribute('class')
                    if find_geren == 'personalicon':
                        iPersonal = True

                except Exception:
                    pass

                # 将单页数据整合到列表
                row = [
                    company,time_,page,rank,date,product,factory,batchNum,totalNum,packaging,
                    explain,place[3:],qq1,qq2,iBrandStar,iYear,iICCP,
                    iSSCP,iSTOCK,iVIP,iOriginal,iDaili,iHckc,i500,iEvaluate,
                    iPersonal,iconXianhuo,iconTuijian,iconYouxian,iconRemai,
                ]

                datadict = dict(zip(self.data_name, row))  # 将表头列表与单页数据整合为一个字典
                rows.append(datadict)   # 用以生成DataFrame的列表字典

        return rows


if __name__ == '__main__':

    ProductList,ProductFilenames = redCSV()  # 读取产品列表
    DataName = redConfig()  # 获取表头
    count = 0

    for ProductName in ProductList[0:1]:

        """
        主循环,按产品型号依次爬取
        """
        username = '13978854528'
        password = '5804167'

        # 打开主页
        driver = webdriver.Chrome()
        driver.get(URL)

        login = driver.find_element_by_class_name('loginlink').click()
        driver.find_element_by_id('username').send_keys(username)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_class_name('loginbutton').click()

        # 查找搜索框，输入产品名进入结果页面
        search = driver.find_element_by_class_name('head_searchInput')
        search.clear()
        search.send_keys(ProductName, Keys.ENTER)

        # 在结果页面查找结果数量，计算出总页数，公式:总页数=结果数/50
        results = int(driver.find_element_by_id('icCount').text)
        PageNum = int(results / 50)

        ic = SpiderIC(3, ProductName, DataName)

        rows = []  # 存放爬取的数据列表，随产品列表的迭代清空更新
        Data = ic.getData()

        # 写入CSV文件
        file1 = pd.DataFrame(Data, columns = DataName)
        file1.to_csv(f'X:\IC\IC_{ProductFilenames[count]}.csv',mode = 'w', encoding = 'utf-8-sig', index = False)

        driver.close()


        count += 1

