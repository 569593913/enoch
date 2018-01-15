# -*- coding: utf-8 -*-
class MA:
    """
    move average
    attribute:
        period 均线粒度
        original 原始数据队列
        line 均线值,list类型,值为[时间,均数]
        sum 均线粒度期间的和值
    """

    def __init__(self,period):
        """
        :param  period
        """
        self.period = period
        self.original = []
        self.line = []
        self.sum = 0

    def add(self,date,data):
        """
        :param date
        :param data
        :return: None
        """
        self.original.append(data)
        length = len(self.original)
        self.sum += data
        if length>self.period:#如果大于计算个数,当前均数等于,sum加当前数,减上一个均数计算周期的第一个数,再除以周期
            self.sum -= self.original[-1 - self.period]
            self.line.append([date,self.sum/self.period])
        elif length==self.period:#如果刚好等于计算可个数,直接将sum值除以周期作为第一个均线数
            self.line.append([date,self.sum/self.period])
        else:#如果小于计算个数,则添加空值
            self.line.append([date,None])

    def get(self,i):
         """取第i个均数"""
         length = len(self.original)
         if i==None or i>=length or -i>length:
             return None;
         return self.line[i][1]

    def last(self):
        """取最后一个均数"""
        return self.get(-1)

