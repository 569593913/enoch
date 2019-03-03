# -*- coding: utf-8 -*-
class Gap:
    """
    缺口分析
    attributes:
        ratio: 缺口幅度,默认3%
        top：顶部的窗口数组
        bottom：底部的窗口数组
    """

    def __init__(self,ratio=0.03):
        """
        :param ratio: 缺口幅度
        """
        self.top = []
        self.bottom = []
        self.ratio = ratio
        self.preK = None

    def fresh(self,k):
        """
        1、判断是否消除了窗口，有则移除相应的窗口,为了节约性能，一个K线消除一个方向多个窗口的情况也只消除最外的窗口
        2、判断是否产生新的窗口，有则保存到top或者bottom中
        :param k: K线对象
        :return: None
        """
        if len(self.bottom) > 0:
            window = self.bottom[-1]
            if k.close < window.low:
                self.bottom.pop()
        if len(self.top) > 0:
            window = self.top[-1]
            if k.close > window.high:
                self.top.pop()
        if self.preK == None:
            self.preK = k
            return
        if (k.low - self.preK.high)/self.preK.high >= self.ratio:
            self.bottom.append(Window(k.date,k.low,self.preK.high))
        elif (self.preK.low-k.high)/k.high >= self.ratio :
            self.top.append(Window(k.date,k.high,self.preK.low))
        self.preK = k



    def support(self,date,price,prePrice,interval=100):
        """
        判断否有支撑力
        :param date: 当前日期
        :param price: 价格
        :param prePrice: 前一天价格，当不为None时，price > prePrice则返回Fasle
        :param interval: 间隔天数
        :return: True or False
        """
        if len(self.bottom)<1:
            return False
        interval = 1000*60*60*24*interval
        window = self.bottom[-1]
        flag = prePrice == None or price < prePrice

        return flag == True and price <  window.high and price > window.low and date - window.date < interval

    def pressure(self,price):
        """
        判断是否有压力
        :param price: 价格
        :return: True or False
        """
        if len(self.top)<1:
            return False
        window = self.top[-1]
        return price >  window.low and price < window.high

class Window:
    """
    窗口对象
    attributes:
        date: 日间
        high: 最大值
        low: 最小值
        ratio：变化率
    """

    def __init__(self,date,high,low):
        """
        :param date: 日期
        :param high: 最大值
        :param low: 最小值
        """
        self.date = date
        self.high = high
        self.low = low
        self.ratio = high - low / low