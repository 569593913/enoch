# -*- coding: utf-8 -*-
from ..ConditionBean import *
class BuyB:
    """
    买策略
    """

    def decide(self,listK,trend):
        k = listK[-1]
        lm1 = trend.getMerge(-1)
        lm2 = trend.getMerge(-2)
        lm4 = trend.getMerge(-4)
        lm5 = trend.getMerge(-5)
        lm6 = trend.getMerge(-6)
        lm7 = trend.getMerge(-7)
        ls2 = trend.getSegment(-2)
        lb1 = trend.getBig(-1)
        lb2 = trend.getBig(-2)
        lb3 = trend.getBig(-3)
        lb4 = trend.getBig(-4)
        if (
            lb3.isUp() and lb4.ratio < -0.4 and lb2.low < lb3.middle and
            k.low < lb3.middle and (lb2.day > 3 or lb3.day > 3) and
            lb2.slope > -0.02 and ls2.slope > -0.02 and (lb2 > -0.15 or k.ratio() > 0.02) and
            lb1.day < 3 and k.isUp()
        ):
            return ConditionBean('b', k, 'b1')
        if (
            lm2.low > lm4.low and lm4.absR * 2 < lm6.absR and
            lm6.low > lm5.middle and lm4.low < lm6.low and lm1.day < 3
                #                 and
                #                 (k.ratio() > 0.02 or (k.close - pre.close)/pre.close > 0.02)
        ):
            # \
            #  \
            #   \/\
            #      \/\,
            return ConditionBean('b', k, 'b2')
        if (
            lm2.low < lm4.high and lm2.low > lm4.low and
            ((lm4.low < lm6.high and lm4.low > lm6.low) or
            (lm6.low < lm4.high and lm6.low > lm4.low and lm6.day > 3)) and
            lm6.low > lm7.middle and lm1.day < 4
        ):
            #
            #
            #  /\/\/\,
            # /
            return ConditionBean('b', k, 'b3')


        return None