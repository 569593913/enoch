# -*- coding: utf-8 -*-
from ..ConditionBean import *
class BuyD:
    """
    买策略
    """

    def decide(self,listK,trend):
        k = listK[-1]
        pre = listK[-2]
        lm1 = trend.getMerge(-1)
        lm2 = trend.getMerge(-2)
        lm3 = trend.getMerge(-3)
        lm4 = trend.getMerge(-4)
        lm5 = trend.getMerge(-5)
        lm6 = trend.getMerge(-6)
        lm7 = trend.getMerge(-7)
        ls1 = trend.getSegment(-1)
        if (
            abs((lm2.low - lm6.low) / lm6.low) < 0.04 and lm3.low > lm6.low and
            lm2.low > lm6.low and max(lm2.absR, lm5.absR) * 2 < lm6.absR and
            lm1.day < 3 and max(lm2.low, lm6.low) < lm7.middle and lm2.isDown()
        ):
            # \
            # \   /\/\
            #  \/     \,
            return ConditionBean('d', k, 'd1')

        if (
            lm6.ratio < -0.04 and abs(max(lm5.high, lm2.high) - lm6.middle) / lm2.middle < 0.05 and
            lm2.low > lm6.low and lm3.low > lm6.low and lm2.ratio < -0.1 and lm2.slope < -0.03 and
            lm2.isDown()
        ):
            # \
            # \   /\/\
            #  \/     \,
            return ConditionBean('d', k, 'd2')


        if (
            lm2.isDown() and lm3.ratio > 0.06 and lm3.day > 3 and lm2.low > lm4.high and
            (lm2.low - lm4.high) / lm4.high < 0.05 and  k.ratio() > 0.02 and lm1.day < 4
        ):
            #
            #     /\,
            # /\/
            return ConditionBean('d', k, 'd3')

        if (
            (
                ( lm1.ratio < -0.25 and k.ratio() > 0.02  and
                  ( (lm1.slope < -0.04 and lm1.mergeNum > 1) or (lm1.ratio < -0.4 and ls1.slope < -0.04) )
                )
                or
                 ( lm2.ratio < -0.25 and  lm1.up < 3 and lm1.ratio < 0.1 and
                    (
                        ( lm2.slope < -0.04 and lm2.mergeNum > 1 and k.ratio() > 0.02) or (lm2.ratio < -0.4 and lm2.slope < -0.02 and not k.isDown())
                    )
                )
            )

        ):
            # \
            # \
            #  \,
            return ConditionBean('d', k, 'd4')

        if (
            k.low > pre.high and lm2.day > 3 and pre.close < lm2.high and
            k.close > lm2.high and (lm2.low > lm3.low or lm2.day < lm3.day)
        ):
            #
            #      ,
            # \/\/
            return ConditionBean('d', k, 'd5')

        if (
            lm1.isUp() and k.close > lm2.high and pre.close < lm2.high and
            lm2.low > lm3.low and (lm2.low - lm3.low) / lm3.low < 0.03 and
             abs(lm4.low - lm5.low) / lm5.low < 0.03
        ):
            #
            #        ,
            # /\/\/\/
            return ConditionBean('d', k, 'd6')

        return None