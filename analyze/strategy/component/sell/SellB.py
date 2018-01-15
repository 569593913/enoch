# -*- coding: utf-8 -*-
from ..ConditionBean import *
class SellB:
    """
    卖策略

    """
    def __init__(self,condtions):
        """
        :param condtions: 条件
        """
        self.condtions = condtions

    def decide(self,listK,condtionBean,trend=None):
        if condtionBean.group not in self.condtions:
            return None
        k = listK[-1]
        pre = listK[-2]
        lm1 = trend.getMerge(-1)
        lm2 = trend.getMerge(-2)
        lm3 = trend.getMerge(-3)
        lm4 = trend.getMerge(-4)
        lm5 = trend.getMerge(-5)
        lm6 = trend.getMerge(-6)
        ls1 = trend.getSegment(-1)
        ls2 = trend.getSegment(-2)
        ls3 = trend.getSegment(-3)
        lb2 = trend.getBig(-2)
        lb3 = trend.getBig(-3)
        lb5 = trend.getBig(-5)
        if (
            condtionBean.buyK.date < lm2.bk.date and lm2.isUp() and k.close < lm2.middle and
            lm2.middle > lm3.high and lm3.ratio < -0.07
        ):
            #       /\
            #     /   \
            # /\/
            return "b1"
        if (
            lm1.isDown() and k.ratio() < -0.02 and (lm2.ratio > 0.05 or lm2.day > 4) and
            lm2.high < lm3.high and lm2.low > lm5.high
        ):
            #     /\,~
            # /\/
            return "b2"
        if (
            k.high < min(lm2.low, lm4.low, lm6.low) and k.close > condtionBean.buyK.low
        ):
            return "b3"
        if (
            lb2.ratio > 0.2 and lm2.high > lm3.middle and lm3.high > lm2.middle and
            k.MOC() < lm2.low and k.ratio() < -0.03 and
            ((lb2.high > lb3.middle and lb2.high < lb3.high) or (lb2.high > lb5.middle and lb2.high < lb5.high))
        ):
            # \
            # \     /\/\
            #  \  /     \
            #   \/
            # \
            # \      /\/\
            #  \    /    \
            #   \/\/
            return "b4"
        if (
                (
                    ( (ls1.ratio > 0.08 and ls1.slope > 0.02) or (ls3.ratio > 0.08 and ls3.slope > 0.02) ) and
                    k.ratio() < 0.007 and pre.ratio() < 0.007 and k.close < pre.close
                )
                or (ls1.ratio > 0.15 and ls1.slope > 0.05 and k.ratio() < -0.01)
                or (ls2.day > 3 and ls2.slope > 0.06)
                or (lm1.ratio > 0.25 and pre.ratio() > 0.07 and k.ratio() < -0.02)
        ):
            # |`
            # |
            return "b5"
        return None

