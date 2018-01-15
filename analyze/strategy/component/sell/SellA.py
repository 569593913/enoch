# -*- coding: utf-8 -*-
from ..ConditionBean import *
class SellA:
    """
    卖策略

        ,.
     /\/
    /
    """
    def __init__(self,condtions):
        """
        :param condtions: 条件
        """
        self.condtions = condtions


    def decide(self,listK,condtionBean,trend=None):
        if condtionBean.group not in self.condtions:
            return None
        lm1 = trend.getMerge(-1)
        lm2 = trend.getMerge(-2)
        lm3 = trend.getMerge(-3)
        lm4 = trend.getMerge(-4)
        if lm1.day < 3 and lm2.high > lm3.high and lm2.ratio < lm4.ratio and lm2.ratio > 0.07:
            return "a1"
        return None

