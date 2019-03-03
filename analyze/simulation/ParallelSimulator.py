# -*- coding: utf-8 -*-
from .Trader import *
import  data.KDataDao as kd
import operator
# import thread
import copy
from threading import Thread,Lock
import time
from datetime import datetime
from datetime import datetime, timedelta
class ParallelSimulator:
    """
    并行模拟器
    attribute:
         trader 初始模拟帐户
         parallelStrategy 串行交易策略
         begin: 开始时间
         end: 结束时间
    """

    def __init__(self,parallelStrategy=None,begin='2017-01-01',end=None,trader=None):
        """

        :param sequenceStrategy:
        :param begin:
        :param end:
        :param trader:
        """
        if None == trader:
            if parallelStrategy.trader != None:
                trader = parallelStrategy.trader
            else:
                trader = Trader()
        self.trader = trader
        self.parallelStrategy = parallelStrategy
        self.begin = begin
        self.end = end
        self.traderDic = {}

    def run(self,market=None,begin=None,end=None,parallelStrategy=None,threadCount=3):
        """
        串行交易模拟
        :param market:
        :param parallelStrategy: 串行交易策略
        :param begin:
        :param end:
        :param threadCount: 运行线程数,默认为3
        :return:
        """
        if None==parallelStrategy:
            parallelStrategy = self.parallelStrategy
        if None == parallelStrategy:
            raise '没有设置串行交易策略'
            return
        if None==begin:
            begin = self.begin
        if None==end:
            end = self.end

        # queueLock = Lock()
        date = datetime.strptime(begin,"%Y-%m-%d")
        endDate = datetime.strptime(end, "%Y-%m-%d")
        dic = {}
        while date <= endDate:
            #获取当天所有的股票
            listK = kd.get_day_k(date.strftime("%Y-%m-%d"))
            #分析
            if len(listK) < 1:
                date = date + timedelta(days=1)
                continue
            parallelStrategy.decide(listK)
            for k in listK:
                if self.trader.isHold(k.code):
                    dic[k.code] = k.close
            self.trader.fresh(listK[0].date,dic)
            date = date + timedelta(days=1)
            print("%s" % (date.strftime("%Y-%m-%d")))

    def getOdds(self):
        """获取胜率"""
        buyPrice = 0
        win = 0.0
        lose = 0.0
        winDic = {}
        loseDic = {}
        timeSet = set()
        for code, trader in self.traderDic.items():
            for r in trader.record:
                if r.type == 'buy':
                    buyPrice = r.price
                    continue
                timeSet.add(r.time)
                if r.price > buyPrice:
                    win += 1
                    winDic[r.time] = winDic.get(r.time,0.0) + 1
                else:
                    lose += 1
                    loseDic[r.time] = loseDic.get(r.time, 0.0) + 1
        timeSet = sorted(timeSet)
        oddsLine = []
        tw = 0.0
        tl = 0.0
        for t in timeSet:
            w = winDic.get(t,0.0)
            tw += w
            l = loseDic.get(t,0.0)
            tl += l
            oddsLine.append([t,0 if (tw+tl)==0 else tw/(tw+tl)])
        return oddsLine,win,lose,win/(win+lose)



    def result(self):
        """
        获取所有测试股票的结果
        :return:
        """
        result = []
        for code,trader in self.traderDic.items():
            result.append([code,trader.earningsLine[-1][1] if len(trader.earningsLine)>0 else 0])
        return result