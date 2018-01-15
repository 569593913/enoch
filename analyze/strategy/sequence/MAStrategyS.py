# -*- coding: utf-8 -*-
from analyze.indicators.MA import *
class MAStrategyS:
    """
    均线策略
    """
    def __init__(self,period=None):
        self.point = 0
        self.period = period
        self.ma = MA(period)

    def init(self,trader=None,listK=[]):
        """"""
        self.trader = trader
        self.listK = listK

    def decide(self,k):
        """
        策略
        :param i: 当前在list中的位置
        :return:
        """
        self.ma.add(k.date,k.close)
        if len(self.ma.original) < self.period:
            return
        #卖策略
        if  (
                k.close < self.ma.last()
            ):
            self.trader.sell(k.code,k.date,k.close)
            return
        #买策略

        if (
               k.close > self.ma.last()
            ):
            self.trader.buy(k.code,k.date,k.close)