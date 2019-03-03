# -*- coding: utf-8 -*-
from .Base import *
class StrategyS1(Base):
    """

    """

    def decide(self,list,trader,i):
        """
        策略
        :param list: 测试数据
        :param trader: 交易者
        :param i: 当前在list中的位置
        :return:
        """
        self.sell(list,trader,i)
        self.buy(list, trader, i)

    def buy(self,list,trader,i):
        """
        买策略
        :param list:
        :param trader:
        :param i:
        :return:
        """
        if trader.isHold(list[i].code) == True:
            return
        if list[i].isUp():
            trader.buy(list[i].code,list[i].date,list[i].close)

    def sell(self, list, trader, i):
        """
        卖策略
        :param list:
        :param trader:
        :param i:
        :return:
        """
        if trader.isHold(list[i].code) == False:
            return
        if list[i].isDown():
            trader.sell(list[i].code,list[i].date,list[i].close)