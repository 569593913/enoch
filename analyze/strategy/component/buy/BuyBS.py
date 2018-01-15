# -*- coding: utf-8 -*-
from ..ConditionBean import *
class BuyBS:
    """
    买策略
    """

    def decide(self,listK,trend):
        k = listK[-1]
        pre = listK[-2]
        pre2 = listK[-3]
        lm1 = trend.getMerge(-1)
        lm2 = trend.getMerge(-2)
        lm3 = trend.getMerge(-3)
        lm4 = trend.getMerge(-4)
        ls1 = trend.getSegment(-1)
        ls2 = trend.getSegment(-2)
        ls3 = trend.getSegment(-3)

        if (
            (lm1.isDown() and (lm2.day > 2 or lm2.ratio > 0.05) and abs(lm1.low - lm2.low)/lm2.low < 0.01 ) or
            (ls1.isDown() and (ls2.day > 2 or ls2.ratio > 0.05) and abs(ls1.low - ls2.low)/ls2.low < 0.01 )
        ):
            # /\
            return ConditionBean('bs', k, 'sa')
        if (
            lm1.isUp() and lm2.day > 2 and lm3.day > 3 and lm1.day < 3
            and (
                  ( (lm2.low - lm3.low)/lm3.low < 0.01 and lm2 > lm3.low ) or
                  ((k.minOC()-lm3.low)/lm3.low < 0.01 and k.minOC() > lm3.low)
                )
        ):
            # /\,
            return ConditionBean('bs', k, 'sb')
        if (
            (lm1.isDown() and lm1.day > 3 and lm2.day > 3 and (lm1.low - lm3.high)/lm3.high < 0.01 and lm1 > lm3.high)
            or (ls1.isDown() and ls1.day > 3 and ls2.day > 3 and abs(ls1.low - ls3.high)/ls3.high < 0.01 )
        ):
            #   /\
            #/\/
            return ConditionBean('bs', k, 'sc')
        if (
            lm1.isUp() and lm2.day > 2 and lm4.day > 3 and lm1.day < 3
            and (
                  ( (lm2.low - lm4.high)/lm4.high < 0.01 and lm2 > lm4.high ) or
                  ((k.minOC()-lm4.high)/lm4.high < 0.01 and k.minOC() > lm4.high)
                )
        ):
            #    /\,
            # /\/
            return ConditionBean('bs', k, 'sd')
        if (
            lm3.ratio > -0.05 and lm2.ratio>-0.05 and
            k.isDown() and pre.isUp() and pre2.isDown() and k.open > pre2.close and pre2.open > k.close
        ):
            # []^[]
            return ConditionBean('bs', k, 'se')
        if (
            lm3.ratio > -0.07 and k.isUp() and pre.isDown() and pre2.isUp() and k.close < pre2.high and k.open > pre2.low
        ):
            # ^[]^
            return ConditionBean('bs', k, 'sf')
        if (
            k.isUp() and k.close > lm3.high and k.open < lm3.low
        ):
            # ^ /
            return ConditionBean('bs', k, 'sg')
        if (
            ls2.slope < -0.05 and ls1.day < 3 and k.isUp() and k.isUp and pre.isUp()
        ):
            # |,
            return ConditionBean('bs', k, 'sh')
        if (
            ls2.day > 5 and ls1.day < 3 and k.isUp()
        ):
            # \,
            return ConditionBean('bs', k, 'si')
        if (
            pre.low < lm3.low and k.close > lm3.low and  k.isUp()
        ):
            """
            \/\  ,
               \/
            """
            return ConditionBean('bs', k, 'si')
        return None