# -*- coding: utf-8 -*-
from Trader import *
import  data.KDataDao as kd
import operator
import thread
import copy
from threading import Thread,Lock
import time
class SequenceSimulatorS:
    """
    串行模拟器
    attribute:
         trader 初始模拟帐户
         traderDic 模拟帐户池,一只股票一个帐户,dic类型,key为股票代码,value为模拟帐户
         sequenceStrategy 串行交易策略
         begin: 开始时间
         end: 结束时间
    """

    def __init__(self,sequenceStrategy=None,begin='2017-01-01',end=None,trader=None):
        """

        :param sequenceStrategy:
        :param begin:
        :param end:
        :param trader:
        """
        if None == trader:
            trader = Trader()
        self.trader = trader
        self.sequenceStrategy = sequenceStrategy
        self.begin = begin
        self.end = end
        self.traderDic = {}

    def run(self,market=None,begin=None,end=None,sequenceStrategy=None,threadCount=3):
        """
        串行交易模拟
        :param market:
        :param sequenceStrategy: 串行交易策略
        :param begin:
        :param end:
        :param threadCount: 运行线程数,默认为3
        :return:
        """
        if None==sequenceStrategy:
            sequenceStrategy = self.sequenceStrategy
        if None == sequenceStrategy:
            raise '没有设置串行交易策略'
            return
        if None==begin:
            begin = self.begin
        if None==end:
            end = self.end

        # 获取股票池
        codes = kd.get_stock_codes(market)
        queueLock = Lock()
        def threadMethod(name):
            print "%s begin run" % name
            while True:
                code = None
                try:
                    queueLock.acquire()
                    if len(codes) < 1:
                        break;
                    code = codes.pop()
                finally:
                    queueLock.release()
                # print "%s begin run %s left:%s" % (name,code,len(codes))
                trader = Trader(self.trader.original)
                self.traderDic[code] = trader
                # 获取股票数据
                # bg = time.time()
                list = kd.get_k_day_af(code, begin, end)
                # print '%s complete %s second %s' % (code, (time.time() - bg),len(list))
                if len(list) < 10:
                    # print '%s begin:%s,end:%s 没有测试数据' % (code, begin, end)
                    continue
                i = 0
                sequenceStrategy.init(trader)
                for k in list:
                    sequenceStrategy.decide(k)
                    trader.fresh(k.date, {code:k.close})

            print "%s end run" % name
        threads = []
        for i in range(threadCount):
            t = Thread(target=threadMethod,args=('thread-%s' % i,))
            t.start()
            threads.append(t)
        threadMethod('thread-main')
        for t in threads:
            t.join()

    def earningsLines(self):
        """
        获取平均收益曲线,最大收益曲线,最小收益曲线
        :return: 平均收益曲线,最大收益股票代码,最大收益曲线,最小收益股票代码,最小收益曲线
        """
        avgEarningsLine = None
        maxEarningsLine = None
        maxCode = None
        minEarningsLine = None
        minCode = None
        avgDic = {}
        count = len(self.traderDic)
        for code,trader in self.traderDic.items():
            if len(trader.earningsLine) < 1:
                continue
            if None==maxEarningsLine:
                maxCode = code
                minCode = code
                maxEarningsLine = trader.earningsLine
                minEarningsLine = trader.earningsLine
                continue

            if trader.earningsLine[-1][1] > maxEarningsLine[-1][1]:
                maxEarningsLine = trader.earningsLine
                maxCode = code
            if trader.earningsLine[-1][1] < minEarningsLine[-1][1]:
                minEarningsLine = trader.earningsLine
                minCode = code
            for d in trader.earningsLine:
                avgDic[d[0]] = avgDic.get(d[0], 0) + d[1]/count
        avgEarningsLine = sorted(avgDic.items(), key=operator.itemgetter(0))
        return avgEarningsLine,maxCode,maxEarningsLine,minCode,minEarningsLine

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