# -*- coding: utf-8 -*-
from datetime import datetime
class Segment:
    """
    线段
    attributes:
        bk 开始点的K线
        ek 结束点的K线
        low 最低点
        high 最高点
        middle 中点
        ratio 变化率
        absR 绝对变化率
        slope 斜率
        day 交易日
        up 阳线数,不包含起点
        direction 方向(up,down)
        mergeNum 合并的线段个数
    """

    def __init__(self, bk, ek, direction, day=0, mergeNum=0, up=0):
        self.bk = bk
        self.ek = ek
        self.direction = direction
        self.mergeNum = mergeNum
        self.up = up
        self.day = day
        self._process()

    def __repr__(self):
        return "Segment[bk=%s,ek=%s,low=%s,high=%s,ratio=%s,slope=%s,day=%s,mergeNum=%s]" % \
               (self.bk,self.ek,self.low,self.high,self.ratio,self.slope,self.day,self.mergeNum)

    def khigh(self):
        return max(self.bk.high, self.ek.high)

    def klow(self):
        return min(self.bk.low, self.ek.low)

    def endPoint(self, k):
        """
        设置终点
        """
        self.ek = k
        self._process()
        #放在这里是为了排除起始点是阳的情况
        if self.direction == "up":
            self.up += 1

    def _process(self):
        """
        生成数据
        low 最低点
        high 最高点
        middle 中点
        ratio 变化率
        absR 绝对变化率
        slope 斜率
        """
        self.low = min(self.bk.extra, self.ek.extra)
        self.high = max(self.bk.extra, self.ek.extra)
        self.middle = (self.bk.extra + self.ek.extra) / 2
        self.ratio = (self.ek.extra - self.bk.extra) / self.bk.extra
        self.absR = abs(self.ratio)
        self.day += 1
        self.slope = self.ratio / self.day


    def isUp(self):
        return self.direction == "up"

    def isDown(self):
        return self.direction == "down"

    def height(self):
        if self.bk == None or self.ek == None:
            return 0
        return abs(self.bk.extra - self.ek.extra)



class Trend:
    """
    趋势指标
    attributes:
        segments:线段Segment集合
        merges:合并后的Segment集合
        bigs:大线段
    """

    def __init__(self,rule=None):
        """
        """
        self.segments = []
        self.merges = []
        self.bigs = []
        self.rule = rule

    def add(self, k):
        self.__addSegment(k)
        self.__addMerge(k)
        self.__addBig(k)

    def __add(self, list, k):
        if self.rule != None:
            k.extra = self.rule(k)
        else:
            k.extra = k.close
        direction = ''
        if len(list) < 1:
            list.append(Segment(k, k, direction))
            return
        s = list[-1]
        if k.extra > s.ek.extra:
            direction = 'up'
        elif k.extra <= s.ek.extra:
            direction = 'down'
        if s.direction == direction:
            list[-1].endPoint(k)
        else:
            s = list[-1]
            list.append(Segment(s.ek, k, direction, 1))

    def __addSegment(self, k):
        self.__add(self.segments, k)

    def __addMerge(self, k):
        self.__add(self.merges, k)
        self.__merge()

    def __merge(self):
        if len(self.merges) < 3:
            return
        l1 = self.getMerge(-1)
        l2 = self.getMerge(-2)
        l3 = self.getMerge(-3)
        flag = False
        if l1.direction == 'up' and l2.low > l3.middle and l2.high < l1.middle:
            flag = True
        elif l1.direction == 'down' and l2.high < l3.middle and l2.low > l1.middle:
            flag = True
        elif (l2.absR < 0.02 or l2.day < 3) and (
                    (l1.isUp() and l1.low > l3.low and l1.high > l3.high) or (l1.isDown() and l1.high < l3.high and l1.low < l3.low)
                    ):
            flag = True
        if flag == True:
            self.merges.remove(l1)
            self.merges.remove(l2)
            self.merges.remove(l3)
            self.merges.append(Segment(l3.bk,
                                       l1.ek,
                                       l1.direction,
                                       l1.day + l2.day + l3.day - 3,
                                       l1.mergeNum + l2.mergeNum + l3.mergeNum + 1,
                                       l1.up + l2.up + l3.up
                                       )
                               )
            self.__merge()
        # print "%s merge:l1.middle=%s,l2.high=%s,ls2.low=%s,ls3.middle=%s" % (datetime.fromtimestamp(l1.eDate/1000.0-24*60*60),l1.middle(),l2.high(),l2.low(),l3.middle())


    def __addBig(self, k):
        self.__add(self.bigs, k)
        self.__mergeBig()

    def __mergeBig(self):
        if len(self.bigs) < 3:
            return
        l1 = self.getBig(-1)
        l2 = self.getBig(-2)
        l3 = self.getBig(-3)
        flag = False
        if l1.direction == 'up' and l2.low > l3.middle and l2.high < l1.middle:
            flag = True
        elif l1.direction == 'down' and l2.high < l3.middle and l2.low > l1.middle:
            flag = True
        elif (l2.absR < 0.05 or l2.day < 10) and \
                ((l1.isUp() and l1.high > l3.high and l1.low > l3.low) or
                     (l1.isDown() and l1.low < l3.low and l1.high < l3.high)
                 ):
            flag = True
        # elif l2.day < 2 and ((l1.high() > l3.high() and l1.isUp()) or (l1.low() > l3.low() and l1.isDown())):
        #             flag = True
        if flag == True:
            self.bigs.remove(l1)
            self.bigs.remove(l2)
            self.bigs.remove(l3)

            self.bigs.append(Segment(l3.bk,
                                     l1.ek,
                                     l1.direction,
                                     l1.day + l2.day + l3.day - 3,
                                     l1.mergeNum + l2.mergeNum + l3.mergeNum + 1,
                                     l1.up + l2.up + l3.up
                                     )
                             )
            self.__mergeBig()


    def getBig(self, i):
        ln = len(self.bigs)
        if ln == 0:
            return None
        if i > 0 and i >= ln:
            i = ln - 1
        elif i < 0 and abs(i) > ln:
            i = 0
        return self.bigs[i]

    def getSegment(self, i):
        ln = len(self.segments)
        if ln == 0:
            return None
        if i > 0 and i >= ln:
            i = ln - 1
        elif i < 0 and abs(i) > ln:
            i = 0
        return self.segments[i]

    def getMerge(self, i):
        ln = len(self.merges)
        if ln == 0:
            return None
        if i > 0 and i >= ln:
            i = ln - 1
        elif i < 0 and abs(i) > ln:
            i = 0
        return self.merges[i]

