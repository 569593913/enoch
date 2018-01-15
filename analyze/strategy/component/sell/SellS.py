# -*- coding: utf-8 -*-
class SellS:
    """
    卖策略
     /\
       \
    """
    def __init__(self, condtions):
        """
        :param condtions: 条件
        """
        self.condtions = condtions

    def decide(self, listK, condtionBean, trend=None):
        if condtionBean.group not in self.condtions:
            return None
        k = listK[-1]
        # lm1 = self.trend.getMerge(-1)
        ls2 = trend.getSegment(-2)
        # lm3 = self.trend.getMerge(-3)
        # lm4 = self.trend.getMerge(-4)
        if k.close < condtionBean.buyK.minOC() and k.close < ls2.low:
            return "s1"
        return None

