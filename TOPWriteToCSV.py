import json
import os
from pymongo.mongo_client import MongoClient
import pandas as pd
import time
import datetime


def readJson():

    # 读取文件
    with open(f"Datas/SummaryTable{datetime.date.today()}.json", 'r') as jsonobj:
        datas = json.load(jsonobj)

    date = time.strftime('%Y-%m', time.localtime())
    day = time.strftime('%d', time.localtime())

    path = f'Datas/{date}'
    isExists = os.path.exists(path)

    # 定义储存数据的列表
    baseInfo = []
    ordersInfo = []

    for data in datas['trades_sold_get_response']['trades']['trade']:
        for d in data['orders']['order']:
            ordersInfo.append(d)
        del data['orders']
        baseInfo.append(data)

    # 提取出第一条数据的数据名字段并转义
    orderHeader = ordersInfo[0].keys()
    header = []
    for oh in orderHeader:
        if oh == 'status':
            oh = '交易状态'
        if oh == 'seller_rate':
            oh = '买家是否评价'
        if oh == 'sku_properties_name':
            oh = '商品属性'
        if oh == 'sku_id':
            oh = '商品类目ID'
        if oh == 'refund_id':
            oh = '退款ID'
        if oh == 'refund_status':
            oh = '退款状态'
        if oh == 'cid':
            oh = 'CID'
        if oh == 'discount_fee':
            oh = '子订单优惠额'
        if oh == 'adjust_fee':
            oh = '手动调整金额'
        if oh == 'oid':
            oh = '子订单编号'
        if oh == 'num_iid':
            oh = '商品数字编号'
        if oh == 'price':
            oh = '商品价格'
        if oh == 'num':
            oh = '购买数量'
        if oh == 'buyer_rate':
            oh = '卖家是否评价'
        if oh == 'total_fee':
            oh = '应付金额'
        if oh == 'title':
            oh = '交易标题'
        if oh == 'pic_path':
            oh = '商品图片URL'
        if oh == 'seller_type':
            oh = '卖家类型'
        if oh == 'is_daixiao':
            oh = '是否代销'
        if oh == 'payment':
            oh = '子订单实付金额'
        if oh == 'divide_order_fee':
            oh = '分摊后实付金额'
        if oh == 'consign_time':
            oh = '支付时间'
        header.append(oh)

    # file1 = pd.DataFrame(baseInfo, columns = baseHeader)
    # file3 = pd.merge(file1,file2)
    # file3.columns = header

    # 定义一个DataFrame变量，作为数据文件的内容
    file2 = pd.DataFrame(ordersInfo, columns = orderHeader)
    file2.columns = header  # 设置表头
    if not isExists:
        os.makedirs(path)  # 判断路径是否存在

    # 将数据内容写入csv文件
    file2.to_csv(f"{path}/{day}.csv",
                 mode = 'w', encoding = 'utf-8', index = False)


def connectDB():

    db_client = MongoClient('localhost')
    # 建库
    db = db_client.runoobdb
    # 建表
    db_collections = db.C1
    db_collections.delete_many({})
    # 数据入库
    for data in datas['trades_sold_get_response']['trades']['trade'][1:]:
        db_collections.insert_one(data)

    # 获取基本信息表头
    header_0 = db_collections.find()[0].keys()  # 获取基本信息表头
    header_0 = list(header_0)
    header_0.remove(header_0[0])
    header_0.remove(header_0[1])
    # 获取订单信息表头
    header_1 = db_collections.find()[0]['orders']['order'][0].keys()
    header_1 = list(header_1)
    header = ['交易状态','无物流信息', '交易编号', '交易类型','实付金额', '发货时间', '最小库存id',
              '退款状态', '卖家类型', '购买数量', '子订单运送方式',
              '是否代销', '商品属性','优惠金额', '交易标题', '单价', '子订单编号', '买家是否评价', '分摊后实付',
              '卖家是否评价', '商品类目id', '子订单优惠额', '手工调整金额', '商品数字编号', '商品总金额', '商品图片绝对路径']

    return db_collections,header,header_0,header_1

def askDB(db,h,h0,h1):
    baseInfo = []
    ordersInfo = []

    print('查询数据库...')
    for data in db.find():
        del data['_id']
        baseInfo.append(data)

    for data in db.find():
        for d in data['orders']['order']:
            ordersInfo.append(d)

    # 将数据储存到dataframe变量中，然后写入csv文件
    print('正在建表...')
    file1 = pd.DataFrame(baseInfo, columns = h0)
    file2 = pd.DataFrame(ordersInfo, columns = h1)
    file3 = pd.merge(file1,file2)
    file3.columns = h
    file3.to_csv('Datas/trades.csv', mode = 'w', encoding = 'utf-8-sig', index = False)
    print('完毕!')
