# -*- coding: utf-8 -*-
from analyze.indicators.TrendArea import *
class StrategyP:
    """
    并行策略
    """
    def __init__(self,trader,buys,sells,kCache=5,trendCache=10):
        self.trader = trader
        self.trendAreas = {}
        self.kDatas = {}
        self.kCache = kCache
        self.trendCache = trendCache
        self.buys = buys
        self.sells = sells
        self.dicCondition = {}
    def decide(self, list):
        """
        决策
        :param list:
        :return:
        """
        temp = []
        for k in list:
            code = k.code
            if code not in self.trendAreas:
                self.trendAreas[code] = TrendArea(maxLn=20)
            self.trendAreas[k.code].add(k)
            if code not in self.kDatas:
                self.kDatas[code] = []
            kl = self.kDatas[code]
            kl.append(k)
            if len(kl) > self.kCache:
                kl.remove(kl[0])
            if self.trader.isHold(k.code):
                condition = self.dicCondition[k.code]
                for sell in self.sells:
                    sellCondition = sell.decide(kl,condition,self.trendAreas[k.code])
                    if sellCondition != None:
                        print "s>>>>>%s,%s" % (k.code,sellCondition)
                        self.trader.sell(k.code,k.date,k.close,condition=sellCondition)
                        self.dicCondition[k.code] = None
            else:
                for buy in self.buys:
                    condition = buy.decide(kl,self.trendAreas[k.code])
                    if condition != None:
                        temp.append(condition)
                        self.dicCondition[k.code] = condition
        if len(temp)>0:
            amount = self.trader.cash/len(temp)
            amount = min(amount,self.trader.original/4)
            for c in temp:
                k = c.buyK
                self.trader.buy(k.code, k.date, k.close,amount, c.condition)

