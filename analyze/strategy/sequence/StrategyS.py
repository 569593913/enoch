# -*- coding: utf-8 -*-
from analyze.indicators.TrendArea import *
class StrategyS:
    """
    趋势策略
    """

    def __init__(self, buys, sells, trader=None, listK=[]):
        self.point = 0
        self.trend = TrendArea()
        self.condition = None
        self.listK = listK
        self.trader = trader
        self.buys = buys
        self.sells = sells

    def init(self, trader, listK=[]):
        self.trader = trader
        self.listK = listK
        self.trend = TrendArea()
        self.condition = None

    def decide(self, k):
        if k.close <= 0:
            return
        self.trend.add(k)
        self.listK.append(k)
        if len(self.listK) < 5:
            return
        if self.trader.isHold(k.code) and self.condition != None:
            for sell in self.sells:
                sellCondition = sell.decide(self.listK, self.condition, self.trend)
                if sellCondition != None:
                    self.trader.sell(k.code, k.date, k.close, condition=sellCondition)
                    self.condition = None
                    return
        else:
            for buy in self.buys:
                condition = buy.decide(self.listK, self.trend)
                if condition != None:
                    self.condition = condition
                    self.trader.buy(k.code, k.date, k.close, self.trader.cash, condition.condition)
                    return
