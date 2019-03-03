# -*- coding: utf-8 -*-
from datetime import datetime
from .Trend import *

class Area:
    """
    attributes:
        segments:线段Segment集合
        high:区域最高值,最后个线段不参与计算
        low:区域最低值,最后个线段不参与计算
        maxLow:最大的底点
        minHigh:最低的高点
        day:天数,为了减少判断,当为空时,天数为1,最后个线段不参与计算
        ratio:最高最低的变化率
    """
    def __init__(self,segments=[]):
        self.segments = segments
        self.high = float('-inf')
        self.low = float('inf')
        self.maxLow = float('-inf')
        self.minHigh = float('inf')
        self.day = 0
        i = 1
        for seg in self.segments:
            self.maxLow = max(seg.low, self.maxLow)
            self.minHigh = min(seg.high, self.minHigh)
            if i == len(self.segments):
                break
            self.high = max(seg.high, self.high)
            self.low = min(seg.low, self.low)
            self.day += seg.day
            i += 1
        self.day -= len(self.segments) - 2
        self.ratio = (self.high - self.low)/self.low

    def append(self,seg):
        """
        添加线段
        :param seg:
        :return:
        """
        ls = self.segments[-1]
        self.segments.append(seg)
        self.maxLow = max(seg.low, self.maxLow)
        self.minHigh = min(seg.high, self.minHigh)
        self.day += ls.day - 1
        self.high = max(ls.high, self.high)
        self.low = min(ls.low, self.low)
        self.ratio = (self.high - self.low) / self.low

    def getSegSize(self):
        """
        获取线段个数
        :return:
        """
        return len(self.segments)

    def __repr__(self):
        return 'Area[high=%s,low=%s,maxLow=%s,minHigh=%s,day=%s,segments=%s] ' % (self.high,self.low,self.maxLow,self.minHigh,self.day,self.segments)


class TrendArea (Trend):
    """
    区域趋势
    attributes:
        areas 区域
    """
    def __init__(self,rule=None,maxLn=None):
        """
        """
        Trend.__init__(self,rule)
        self.areas = []
        self.maxLn = maxLn

    def add(self, k):
        """
        添加K线生成趋势
        :param k:
        :return:
        """
        ls = self.getSegment(-1)
        Trend.add(self,k)
        if ls != self.getSegment(-1):
            self.__area()
        if self.maxLn != None:
            if len(self.areas) > self.maxLn:
                self.areas.remove(self.areas[0])
            if len(self.segments) > self.maxLn:
                self.segments.remove(self.segments[0])
            if len(self.merges) > self.maxLn:
                self.merges.remove(self.merges[0])
            if len(self.bigs) > self.maxLn:
                self.bigs.remove(self.bigs[0])

    def __merge(self):
        la2 = self.getArea(-2)
        la3 = self.getArea(-3)
        flag = False
        if la2.high > la3.high and la2.low < la3.low:
            flag = True
        elif la3.high > la2.high and la3.low < la2.low:
            flag = True
        if flag == True:
            self.areas.remove(la2)
            self.areas.remove(la3)
            a = Area(la3.segments + la2.segments)
            a.maxLow = min(la3.maxLow,la2.maxLow)
            a.minHigh = min(la3.minHigh,la2.minHigh)
            self.areas.insert(-1,a)
            self.__merge()

    def __area(self):
        """
        添加区域
        :return:
        """
        ls = self.getSegment(-2)
        la = self.getArea(-1)
        if la==None or ls.high < la.maxLow or ls.low > la.minHigh:
            self.areas.append(Area([ls]))
        else:
            la.append(ls)
        self.__merge()


    def getArea(self,i):
        """
        获取区域
        :param i:
        :return:
        """
        ln = len(self.areas)
        if ln == 0:
            return None
        if i > 0 and i >= ln:
            i = ln - 1
        elif i < 0 and abs(i) > ln:
            i = 0
        return self.areas[i]
