# -*- coding: utf-8 -*-
class SellZone:
    """
    卖策略

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

        la1 = trend.getArea(-1)
        la2 = trend.getArea(-2)
        la3 = trend.getArea(-3)
        la4 = trend.getArea(-4)
        lm1 = trend.getMerge(-1)
        lm2 = trend.getMerge(-2)
        if (la1.getSegSize() == 1 and k.close < la2.low):
            return "z"
        return None

