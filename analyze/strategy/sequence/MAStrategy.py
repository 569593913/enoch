# -*- coding: utf-8 -*-
from analyze.indicators.MA import *
class MAStrategy:
    """
    均线策略
    """
    def __init__(self,period):
        self.point = 0
        self.period = period
        self.ma = MA(period)

    def init(self,*args):
        """"""

    def decide(self,list,trader,i):
        """
        策略
        :param list: 测试数据
        :param trader: 交易者
        :param i: 当前在list中的位置
        :return:
        """
        k = list[i]
        pre = list[i-1]
        self.ma.add(k.date,k.close)
        if len(self.ma.original) < self.period:
            return
        #卖策略
        if  (
                k.close < self.ma.last()
            ):
            trader.sell(k.code,k.date,k.close)
            return
        #买策略

        if (
               k.close > self.ma.last()
            ):
            trader.buy(k.code,k.date,k.close)