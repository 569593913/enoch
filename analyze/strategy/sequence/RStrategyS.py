# -*- coding: utf-8 -*-
class RStrategyS:
    """
    择时收益
    """
    def __init__(self):
        self.isHold = False
        self.trader = None

    def init(self, trader, listK=[]):
        self.trader = trader
        self.listK = listK
    def decide(self,k):
        if self.isHold == False:
            self.isHold = True
            self.trader.buy(k.code,k.date,k.close)
            return