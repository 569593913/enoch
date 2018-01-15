# -*- coding: utf-8 -*-
class SellK:
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
        pre = listK[-2]
        pre2 = listK[-3]
        lm1 = trend.getMerge(-1)
        lm2 = trend.getMerge(-2)
        if ( lm1.low > lm2.low and (lm1.low-lm2.low)/lm2.low < 0.05 ):
            return False
        if (
             pre2.ratio() < -0.04 and pre.isUp() and pre.minOC() < pre2.close and
             k.isDown() and k.close < pre.minOC()
        ):
            return "k1"
        if (
             pre2.ratio() < -0.06 and pre.isUp() and pre.maxOC() < pre2.MOC() and
             k.isDown() and k.open < pre.maxOC()
        ):
            return "k2"
        if (
            k.isDown() and pre.isUp() and k.close < pre.minOC() and k.close < pre2.minOC() and
            lm1.ratio < -0.03 and lm1.up < 2 and lm1.day > 4 and lm1.isDown() and
            (k.close > lm2.middle or k.close < lm2.klow)
        ):
            return "k3"
        if (
            pre.ratio() < -0.075 and k.close < pre.MOC()
        ):
            return "k4"
        if (
            (lm2.ratio > 0.15 and k.close < pre.close and listK[-4].ratio() > 0.08 and
            k.isDown() and pre.isDown() and pre2.isDown())
        ):
            return "k5"
        if (
            k.ratio() < -0.07 and pre.ratio() > 0.05 and
            k.close < pre.open
        ):
            return "k6"
        return None

