import sys
import os
import time
import datetime
import pandas
from TOPWriteToCSV import readJson
from PyQt5.Qt import *
from PyQt5.QtChart import *

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
from Ui_TopMain import Ui_MainWindow as MainWindow

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import font_manager as fm, rcParams

rcParams['font.sans-serif'] = ['SimHei']  #显示中文标签
rcParams['axes.unicode_minus'] = False   #这两行需要手动设置
matplotlib.use("Qt5Agg")


buttonOriginStyle = '''
QPushButton:hover
{
background-color: rgb(106, 106, 106);
}
QPushButton
{
background-color: rgb(44, 44, 44);
color: rgb(238, 238, 238);
border:None;
}
'''

buttonClickedStyle = '''
QPushButton
{
background-color: rgb(255, 255, 255);
color: rgb(44, 44, 44);
border:None;
}
'''
date = time.strftime('%Y-%m',time.localtime())
day = time.strftime('%d',time.localtime())
path = f'Datas/SummaryTable{datetime.date.today()}.json'


class MyFigure(FigureCanvas):

    def __init__(self, width = 5, height = 4, dpi = 100):
        self.fig = Figure(figsize = (width, height), dpi = dpi)
        super(MyFigure, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)


class TopMain(QMainWindow, QApplication, MainWindow):

    def __init__(self):
        super(TopMain, self).__init__()

        self.setupUi(self)  # 主界面回调函数
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 去除主界面的边框

        # ===============今日订单控件===============
        self.tableViewToday = QtWidgets.QTableView(self.centralwidget)
        self.tableViewToday.setGeometry(QtCore.QRect(200, 90, 1050, 770))
        self.tableViewToday.setObjectName("tableView")
        self.tableViewToday.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.tableViewToday.hide()

        self.model_tableViewToday = QStandardItemModel()  # 实例化一个表格控件model

        # ===============历史订单控件================
        # 表格控件
        self.tableViewHis = QtWidgets.QTableView(self.centralwidget)
        self.tableViewHis.setGeometry(QtCore.QRect(320, 75, 1000, 930))
        self.tableViewHis.setObjectName("tableView_2")
        self.tableViewHis.setStyleSheet('background-color: rgb(255, 255, 255);border: None;')
        self.tableViewHis.hide()
        # 树形浏览控件
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(170,75, 150,930))
        self.treeView.setObjectName("treeView")
        self.treeView.setStyleSheet('background-color: rgb(255, 255, 255);border: None;')
        self.treeView.hide()

        self.model_treeView = QFileSystemModel()  # 实例化文件浏览列表model
        self.model_tableViewHis = QStandardItemModel()  # 实例化表格model
        self.path = 'Y:\PyCharm Community Edition\MyProjects\TopUI\Datas'

        self.model_treeView.setRootPath(self.path)  # 设置文件浏览列表根目录
        self.model_treeView.setNameFilters(['*.csv'])  # 设置显示扩展名为csv的文件
        self.model_treeView.setNameFilterDisables(False)  # 关闭文件名过滤
        self.treeView.setModel(self.model_treeView)  # 设置model
        self.treeView.setRootIndex(self.model_treeView.index(self.path))
        self.treeView.clicked.connect(self.showHistoryData)  # 事件绑定
        self.treeView.header().setVisible(False)  # 关闭文件浏览表头显示

        # ===============订单分类控件================
        # 跟团表格
        self.tableViewGentuan = QtWidgets.QTableView(self.centralwidget)
        self.tableViewGentuan.setGeometry(QtCore.QRect(300,200,390,580))
        self.tableViewGentuan.setObjectName("tableViewGentuan")
        self.tableViewGentuan.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.tableViewGentuan.hide()
        # 跟团字样
        self.labelGentuan = QtWidgets.QLabel(self.centralwidget)
        self.labelGentuan.setGeometry(QtCore.QRect(300,160,120,40))
        self.labelGentuan.setObjectName("labelGentuan")
        self.labelGentuan.setStyleSheet('font: 25 14pt "微软雅黑 Light";background-color: rgb(255, 255, 255)')
        self.labelGentuan.setText('跟团：总计')
        self.labelGentuan.hide()
        # 跟团统计
        self.GentuanCount = QtWidgets.QLabel(self.centralwidget)
        self.GentuanCount.setGeometry(QtCore.QRect(420,160,50,40))
        self.GentuanCount.setObjectName("GentuanCount")
        self.GentuanCount.setStyleSheet('font: 25 14pt "微软雅黑 Light";background-color: rgb(255, 255, 255)')
        self.GentuanCount.hide()

        # 包车表格
        self.tableViewBaoche = QtWidgets.QTableView(self.centralwidget)
        self.tableViewBaoche.setGeometry(QtCore.QRect(750,200,420,580))
        self.tableViewBaoche.setObjectName("tableViewBaoche")
        self.tableViewBaoche.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.tableViewBaoche.hide()
        # 包车字样
        self.labelBaoche = QtWidgets.QLabel(self.centralwidget)
        self.labelBaoche.setGeometry(QtCore.QRect(750,160,120,40))
        self.labelBaoche.setObjectName("labelBaoche")
        self.labelBaoche.setStyleSheet('font: 25 14pt "微软雅黑 Light";background-color: rgb(255, 255, 255)')
        self.labelBaoche.setText('包车：总计')
        self.labelBaoche.hide()
        # 包车统计
        self.BaocheCount = QtWidgets.QLabel(self.centralwidget)
        self.BaocheCount.setGeometry(QtCore.QRect(870,160,50,40))
        self.BaocheCount.setObjectName("BaocheCount")
        self.BaocheCount.setStyleSheet('font: 25 14pt "微软雅黑 Light";background-color: rgb(255, 255, 255)')
        self.BaocheCount.hide()

        # 实例化表格model
        self.model_Gentuan = QStandardItemModel()
        self.model_Baoche = QStandardItemModel()

        # ===================文件读取====================
        # 执行API信息获取模块
        if not os.path.exists(path):
            os.system('python2 TOPAskForJson.py')
        readJson()

        # 读取表格文件
        fileContent = pandas.read_csv(f'Datas/{date}/{day}.csv', encoding = 'utf-8')
        self.title = fileContent['交易标题'].values.tolist()
        self.status = fileContent['交易状态'].values.tolist()
        self.attribute = fileContent['商品属性'].values.tolist()
        self.goodsid = fileContent['商品数字编号'].values.tolist()
        self.tcid = fileContent['子订单编号'].values.tolist()
        self.price = fileContent['商品价格'].values.tolist()
        self.payment = fileContent['子订单实付金额'].values.tolist()
        self.num = fileContent['购买数量'].values.tolist()
        self.refund = fileContent['退款状态'].values.tolist()
        self.paytime = fileContent['支付时间'].values.tolist()

        # 将数据中的英文代码转义
        self.data_num = len(self.status)
        for i in range(self.data_num):
            if self.status[i] == 'WAIT_BUYER_CONFIRM_GOODS':
                self.status[i] = '订单创建'
            if self.status[i] == 'TRADE_CLOSED':
                self.status[i] = '交易关闭'
            if self.status[i] == 'TRADE_CLOSED_BY_TAOBAO':
                self.status[i] = '店家取消交易'
            if self.status[i] == 'WAIT_SELLER_SEND_GOODS':
                self.status[i] = '订单付款成功'
            if self.status[i] == 'WAIT_BUYER_CONFIRM_GOODS':
                self.status[i] = '订单已发货'
            if self.status[i] == 'TRADE_FINISHED':
                self.status[i] = '交易完成'
            if self.status[i] == 'WAIT_BUYER_PAY':
                self.status[i] = '等待买家付款'

        for i in range(self.data_num):
            if self.refund[i] == 'NO_REFUND':
                self.refund[i] = '未发起退款'
            if self.refund[i] == 'SUCCESS':
                self.refund[i] = '退款成功'
            if self.refund[i] == 'SELLER_REFUSE_BUYER':
                self.refund[i] = '卖家拒接退款'
            if self.refund[i] == 'CLOSED':
                self.refund[i] = '退款已取消'

        # ===============套餐销售量分析控件================
        # 横线控件
        self.Hline = QtWidgets.QLineEdit(self.centralwidget)
        self.Hline.setGeometry(QtCore.QRect(210, 650, 1000, 1))
        self.Hline.setStyleSheet("border:None;background-color:rgb(213, 213, 213)")
        self.Hline.setEnabled(False)
        self.Hline.hide()

        self.Hline1 = QtWidgets.QLineEdit(self.centralwidget)
        self.Hline1.setGeometry(QtCore.QRect(210, 650, 1000, 1))
        self.Hline1.setStyleSheet("border:None;background-color:rgb(213, 213, 213)")
        self.Hline1.setEnabled(False)
        self.Hline1.hide()

        # 垂线控件
        self.Vline = QtWidgets.QLineEdit(self.centralwidget)
        self.Vline.setGeometry(QtCore.QRect(750, 120, 1, 500))
        self.Vline.setStyleSheet("border:None;background-color:rgb(213, 213, 213)")
        self.Vline.setEnabled(False)
        self.Vline.hide()

        # “数据分析”字样
        self.stringFenxi = QtWidgets.QLabel(self.centralwidget)
        self.stringFenxi.setGeometry(QtCore.QRect(245, 635, 110,30))
        self.stringFenxi.setText("  结果分析")
        self.stringFenxi.setStyleSheet("font: 25 12pt '等线 Light';color:rgb(124, 124, 124);"
                                       "background-color:rgb(255,255,255)")
        self.stringFenxi.hide()

        self.stringFenxi1 = QtWidgets.QLabel(self.centralwidget)
        self.stringFenxi1.setGeometry(QtCore.QRect(245, 635, 110,30))
        self.stringFenxi1.setText("  结果分析")
        self.stringFenxi1.setStyleSheet("font: 25 12pt '等线 Light';color:rgb(124, 124, 124);"
                                       "background-color:rgb(255,255,255)")
        self.stringFenxi1.hide()


        # 统计套餐销售量
        list_ = {}
        for i in self.attribute:
            if i not in list_.keys() and 'nan' not in str(i):
                count = self.attribute.count(i)
                list_[i] = count

        # 统计季度收益额
        totalPayment = 0
        for i in self.payment:
            totalPayment += int(i)

        # 分析结果
        self.result = QtWidgets.QTextEdit(self.centralwidget)
        self.result.setGeometry(QtCore.QRect(210, 665, 1000,200))
        self.result.setStyleSheet("font: 25 12pt '等线 Light';color:rgb(124, 124, 124);"
                                  "background-color:rgb(255,255,255);border:None")
        self.result.hide()

        self.result1 = QtWidgets.QTextEdit(self.centralwidget)
        self.result1.setGeometry(QtCore.QRect(210, 665, 1000,200))
        self.result1.setStyleSheet("font: 25 12pt '等线 Light';color:rgb(124, 124, 124);"
                                   "background-color:rgb(255,255,255);border:None")
        self.result1.hide()

        # 定义扇形图
        self.pieChengren = QPieSeries()
        self.pieDanren = QPieSeries()
        index = 0
        # 获取套餐名的部分作为扇形图的样本名
        for k,v in list_.items():
            perc = float("%0.2f" % (v / len(self.attribute))) * 100  # 计算每个套餐在总销量中的占比
            for i in k:
                if i == '丨':
                    index = k.index(i)
            if '成人' in k:
                self.pieChengren.append(f'{k[5:index]}  {int(perc)}%', perc)
            if '单人房差' in k:
                self.pieDanren.append(f'{k[5:index]}  {int(perc)}%', perc)

        # -----------chart_1-----------
        self.chart_1 = QChart()  # 定义QChart
        self.chart_1.addSeries(self.pieChengren)  # 将扇形图添加到chart里
        self.chart_1.setTitle('成人旅游套餐')  # 设置标题
        self.chart_1.legend().setAlignment(QtCore.Qt.AlignRight)  # 将图例放置在图的右侧
        self.chart_1.legend().setFont(QtGui.QFont("微软雅黑 Light", 8))  # 设置控件字样

        # 定义charView窗口，添加chart元素，设置主窗口为父窗体，既将chartView嵌入到父窗体
        self.chartView_1 = QChartView(self.chart_1, self.frame)
        self.chartView_1.setGeometry(0, 0, 600, 550)  # 设置charview在父窗口的大小、位置
        self.chartView_1.setRenderHint(QPainter.Antialiasing)  # 设置抗锯齿
        self.chartView_1.hide()  # 将CharView窗口显示出来

        # -----------chart_2-----------
        self.chart_2 = QChart()
        self.chart_2.addSeries(self.pieDanren)
        self.chart_2.setTitle('单人旅游套餐')
        self.chart_2.legend().setAlignment(QtCore.Qt.AlignLeft)
        self.chart_2.legend().setFont(QtGui.QFont("微软雅黑 Light", 8))

        self.chartView_2 = QChartView(self.chart_2, self.frame)
        self.chartView_2.setGeometry(550, 0, 600, 550)
        self.chartView_2.setRenderHint(QPainter.Antialiasing)
        self.chartView_2.hide()

        # ===============本周分析控件================
        # 折线图父控件
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setGeometry(QtCore.QRect(165, 20, 800, 600))
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setStyleSheet("border:None")
        self.groupBox.hide()

        self.F = MyFigure(width=3, height=2, dpi=100)
        x_data,y_data,y_data2 = self.lineChart()
        self.gridlayout = QGridLayout(self.groupBox)
        self.gridlayout.addWidget(self.F,0,1)

        self.prof_1 = 0
        self.prof_2 = 0
        for i in range(len(x_data)):
            self.prof_1 += y_data[i]
            self.prof_2 += y_data2[i]

        # ===============事件绑定、重命名控件===============
        self.pushButton.clicked.connect(self.quit)
        self.pushButton_1.clicked.connect(self.pb1)  # 今日订单
        self.pushButton_2.clicked.connect(self.pb2)  # 历史订单
        self.pushButton_3.clicked.connect(self.pb3)  # 订单分类
        self.pushButton_4.clicked.connect(self.pb4)  # 套餐分析
        self.pushButton_5.clicked.connect(self.pb5)  # 本周分析

    def lineChart(self):

        x_data = ['一', '二', '三', '四', '五', '六', '日']
        y_data = [58000, 60200, 63000, 71000, 84000, 90500, 107000]
        y_data2 = [68000, 50200, 73000, 81000, 93000, 60500, 50700]

        self.F.axes.plot(x_data, y_data,label = '本周')
        self.F.axes.plot(x_data, y_data2,label = '上周')
        self.F.fig.legend()
        self.F.fig.suptitle("本周与上周销售额走势图")

        return x_data,y_data,y_data2

    def showTodayData(self):

        # 定义表头
        header = [
            '交易标题','交易状态','商品属性',
            '商品数字编号','子订单编号','商品单价',
            '实付金额','购买数量','退款状态','支付时间'
                  ]

        self.model_tableViewToday.setHorizontalHeaderLabels(header)  # 设置表头内容
        self.tableViewToday.setModel(self.model_tableViewToday)

        for i in range(self.data_num):
            self.model_tableViewToday.setItem(i, 0, QStandardItem(f'{self.title[i]}'))
            self.model_tableViewToday.setItem(i, 1, QStandardItem(f'{self.status[i]}'))
            self.model_tableViewToday.setItem(i, 2, QStandardItem(f'{self.attribute[i]}'))
            self.model_tableViewToday.setItem(i, 3, QStandardItem(f'{self.goodsid[i]}'))
            self.model_tableViewToday.setItem(i, 4, QStandardItem(f'{self.tcid[i]}'))
            self.model_tableViewToday.setItem(i, 5, QStandardItem(f'{self.price[i]}'))
            self.model_tableViewToday.setItem(i, 6, QStandardItem(f'{self.payment[i]}'))
            self.model_tableViewToday.setItem(i, 7, QStandardItem(f'{self.num[i]}'))
            self.model_tableViewToday.setItem(i, 8, QStandardItem(f'{self.refund[i]}'))
            self.model_tableViewToday.setItem(i, 9, QStandardItem(f'{self.paytime[i]}'))

    def showHistoryData(self,Qmodelidx):

        header = ['交易标题','交易状态','商品属性','商品数字编号','商品类目ID']

        self.model_tableViewHis.setHorizontalHeaderLabels(header)
        self.tableViewHis.setModel(self.model_tableViewHis)

        filepath = self.model_treeView.filePath(Qmodelidx)
        fileContent = pandas.read_csv(f'{filepath}', encoding = 'utf-8')

        title = fileContent['交易标题'].values.tolist()
        status = fileContent['交易状态'].values.tolist()
        attribute = fileContent['商品属性'].values.tolist()
        goodsid = fileContent['商品数字编号'].values.tolist()
        skuid = fileContent['商品类目ID'].values.tolist()

        data_num = len(status)
        for i in range(data_num):
            if status[i] == 'WAIT_BUYER_CONFIRM_GOODS':
                status[i] = '订单创建'
            if status[i] == 'TRADE_CLOSED':
                status[i] = '交易关闭'
            if status[i] == 'TRADE_CLOSED_BY_TAOBAO':
                status[i] = '店家取消交易'
            if status[i] == 'WAIT_SELLER_SEND_GOODS':
                status[i] = '订单付款成功'
            if status[i] == 'WAIT_BUYER_CONFIRM_GOODS':
                status[i] = '订单已发货'
            if status[i] == 'TRADE_FINISHED':
                status[i] = '交易完成'
            if status[i] == 'WAIT_BUYER_PAY':
                status[i] = '等待买家付款'

        for i in range(data_num):
            self.model_tableViewHis.setItem(i, 0, QStandardItem(f'{title[i]}'))
            self.model_tableViewHis.setItem(i, 1, QStandardItem(f'{status[i]}'))
            self.model_tableViewHis.setItem(i, 2, QStandardItem(f'{attribute[i]}'))
            self.model_tableViewHis.setItem(i, 3, QStandardItem(f'{goodsid[i]}'))
            self.model_tableViewHis.setItem(i, 4, QStandardItem(f'{skuid[i]}'))


    def classification(self):

        header = ['交易标题','商品数字编号','子订单编号']

        self.model_Gentuan.setHorizontalHeaderLabels(header)
        self.model_Baoche.setHorizontalHeaderLabels(header)

        bc = 0
        gt = 0

        # 筛选数据
        for i in self.title:
            index = self.title.index(i)
            if '包车' in i:
                self.model_Baoche.setItem(bc, 0, QStandardItem(f'{self.title[index]}'))
                self.model_Baoche.setItem(bc, 1, QStandardItem(f'{self.goodsid[index]}'))
                self.model_Baoche.setItem(bc, 2, QStandardItem(f'{self.tcid[index]}'))
                bc += 1

            if '跟团' in i:
                self.model_Gentuan.setItem(gt, 0, QStandardItem(f'{self.title[index]}'))
                self.model_Gentuan.setItem(gt, 1, QStandardItem(f'{self.goodsid[index]}'))
                self.model_Gentuan.setItem(gt, 2, QStandardItem(f'{self.tcid[index]}'))
                gt += 1

        self.tableViewGentuan.setModel(self.model_Gentuan)
        self.tableViewBaoche.setModel(self.model_Baoche)

        # 将统计的数据在控件中显示
        self.GentuanCount.setText(f'{gt} 个')
        self.BaocheCount.setText(f'{bc} 个')

    @pyqtSlot()
    def quit(self):
        self.close()

    def pd1On(self):
        # 样式变换
        self.pushButton_1.setStyleSheet(buttonClickedStyle)
        self.pushButton_2.setStyleSheet(buttonOriginStyle)
        self.pushButton_3.setStyleSheet(buttonOriginStyle)
        self.pushButton_4.setStyleSheet(buttonOriginStyle)
        self.pushButton_5.setStyleSheet(buttonOriginStyle)

        # 显示表格控件
        self.tableViewToday.show()

    def pd1Off(self):

        # 隐藏控件
        self.tableViewToday.hide()

    def pd2On(self):
        self.pushButton_2.setStyleSheet(buttonClickedStyle)
        self.pushButton_1.setStyleSheet(buttonOriginStyle)
        self.pushButton_3.setStyleSheet(buttonOriginStyle)
        self.pushButton_4.setStyleSheet(buttonOriginStyle)
        self.pushButton_5.setStyleSheet(buttonOriginStyle)

        self.tableViewHis.show()
        self.treeView.show()

    def pd2Off(self):
        self.tableViewHis.hide()
        self.treeView.hide()

    def pd3On(self):
        self.pushButton_3.setStyleSheet(buttonClickedStyle)
        self.pushButton_2.setStyleSheet(buttonOriginStyle)
        self.pushButton_1.setStyleSheet(buttonOriginStyle)
        self.pushButton_4.setStyleSheet(buttonOriginStyle)
        self.pushButton_5.setStyleSheet(buttonOriginStyle)

        self.tableViewGentuan.show()
        self.labelGentuan.show()
        self.GentuanCount.show()
        self.tableViewBaoche.show()
        self.labelBaoche.show()
        self.BaocheCount.show()

        self.label.hide()

    def pd3Off(self):
        self.tableViewGentuan.hide()
        self.labelGentuan.hide()
        self.GentuanCount.hide()
        self.tableViewBaoche.hide()
        self.labelBaoche.hide()
        self.BaocheCount.hide()

    def pd4On(self):
        self.pushButton_4.setStyleSheet(buttonClickedStyle)
        self.pushButton_2.setStyleSheet(buttonOriginStyle)
        self.pushButton_3.setStyleSheet(buttonOriginStyle)
        self.pushButton_1.setStyleSheet(buttonOriginStyle)
        self.pushButton_5.setStyleSheet(buttonOriginStyle)
        self.result1.setText("\n本周，广州出发 的套餐销售量最多，占全部销售量的20%。"
                             "客户当日下单时间多集中在 18:00 到 22:00 之间,"
                             "\n建议1、在该时间段内增加对客户或潜在客户的广告投放。"
                             "\n建议2、增加 广州出发 相关套餐的优惠券发放，以及相应的优惠活动")

        self.label.hide()
        self.chartView_1.show()
        self.chartView_2.show()
        self.Vline.show()
        self.Hline1.show()
        self.stringFenxi1.show()
        self.result1.show()

    def pd4Off(self):
        self.chartView_1.hide()
        self.chartView_2.hide()
        self.Vline.hide()
        self.Hline1.hide()
        self.stringFenxi1.hide()
        self.result1.hide()

    def pd5On(self):
        self.pushButton_5.setStyleSheet(buttonClickedStyle)
        self.pushButton_2.setStyleSheet(buttonOriginStyle)
        self.pushButton_3.setStyleSheet(buttonOriginStyle)
        self.pushButton_1.setStyleSheet(buttonOriginStyle)
        self.pushButton_4.setStyleSheet(buttonOriginStyle)
        self.result.setText(f"本周的销售额相对上周趋于平稳上升；本周与上周中，以广州、深圳为出发点的订单量都有所上升，本周最高"
                            f"\n本周总销售额为{self.prof_1},上周总销售额为{self.prof_2}")

        self.label.hide()
        self.groupBox.show()
        self.Hline.show()
        self.stringFenxi.show()
        self.result.show()

    def pd5Off(self):
        self.groupBox.hide()
        self.Hline.hide()
        self.stringFenxi.hide()
        self.result.hide()


    @pyqtSlot()
    def pb1(self):

        self.showTodayData()

        # 开关函数
        self.pd1On()
        self.pd2Off()
        self.pd3Off()
        self.pd4Off()
        self.pd5Off()

    @pyqtSlot()
    def pb2(self):

        # 开关函数
        self.pd1Off()
        self.pd2On()
        self.pd3Off()
        self.pd4Off()
        self.pd5Off()

    @pyqtSlot()
    def pb3(self):

        self.classification()

        # 开关函数
        self.pd1Off()
        self.pd2Off()
        self.pd3On()
        self.pd4Off()
        self.pd5Off()

    @pyqtSlot()
    def pb4(self):

        # 开关函数
        self.pd1Off()
        self.pd2Off()
        self.pd3Off()
        self.pd4On()
        self.pd5Off()

    @pyqtSlot()
    def pb5(self):

        # 开关函数
        self.pd1Off()
        self.pd2Off()
        self.pd3Off()
        self.pd4Off()
        self.pd5On()


if __name__ == '__main__':

    app = QApplication(sys.argv)

    Mainwindow = TopMain()
    Mainwindow.show()

    sys.exit(app.exec_())


