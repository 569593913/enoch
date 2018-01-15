# -*- coding: utf-8 -*-
from ..ConditionBean import *
class BuyC:
    """
    买策略
    """

    def decide(self,listK,trend):
        k = listK[-1]
        lm1 = trend.getMerge(-1)
        lm2 = trend.getMerge(-2)
        lm3 = trend.getMerge(-3)
        lm4 = trend.getMerge(-4)
        lm6 = trend.getMerge(-6)
        lm7 = trend.getMerge(-7)
        ls2 = trend.getSegment(-2)
        if (
            lm2.slope > -0.015 and lm2.day > 5 and lm3.day > 5 and lm3.mergeNum < 5 and
            lm2.middle > max(lm4.high, lm6.high) and min(lm4.high, lm6.high) > max(lm4.low, lm6.low) and
            lm2.low > min(lm4.high, lm6.high) and lm7.low < min(lm4.low, lm6.low) and lm1.day < 3
        ):
            #        /\,
            #  /\/\/
            # /
            return ConditionBean('c', k, 'c1')
        if (
           (lm2.ratio < -0.1 or (lm2.day > 20 and lm2.isDown())) and ls2.absR * 2 < lm2.absR and
           ls2.day > 3 and lm2.high > max(lm4.high, lm6.high) and
           lm2.low > min(lm4.high, lm6.high) and lm1.day < 3 and k.ratio() > 0.01
        ):
            #        /\,
            #  /\/\/    `
            # /
            return ConditionBean('c', k, 'c1')

        return None