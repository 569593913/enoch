# -*- coding: utf-8 -*-
class RStrategy:
    """
    择时收益
    """
    def __init__(self):
        self.isHold = False

    def init(self,*args):
        """"""

    def decide(self,list,trader,i):
        if self.isHold == False:
            self.isHold = True
            k = list[i]
            trader.buy(k.code,k.date,k.close)
            return