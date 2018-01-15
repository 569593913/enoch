# -*- coding: utf-8 -*-
from ..ConditionBean import *
class BuyA:
    """
    买策略
    \
     \_
       \,
    """

    def decide(self,listK,trend):
        k = listK[-1]
        lm1 = trend.getMerge(-1)
        lm2 = trend.getMerge(-2)
        lm3 = trend.getMerge(-3)
        lm4 = trend.getMerge(-4)
        lm5 = trend.getMerge(-5)
        lm6 = trend.getMerge(-6)
        ls2 = trend.getSegment(-2)
        ls3 = trend.getSegment(-3)
        ls4 = trend.getSegment(-4)
        ls5 = trend.getSegment(-5)
        if(
                (
                    (
                        (lm2.ratio < -0.35 or lm2.day > 20) and ls2.absR * 2 < lm2.absR and ls2.low < ls3.low and
                        (abs(ls3.absR - ls4.absR) < 0.02 or abs(ls4.absR - ls5.absR) < 0.02 or
                            (min(ls3.low, ls5.low) > ls2.middle and max(ls3.high, ls5.high) < lm2.middle) or
                            ls3.day > 3 or ls3.ratio > 0.05) and
                        ls2.ratio < -0.05 and lm2.low < lm3.low
                    )
                    or
                    (
                        lm6.low > lm4.low and lm2.ratio < -0.05 and
                        lm2.absR * 1.5 < lm4.absR and (lm2.low - lm4.low) / lm4.low < -0.04
                    )
                    or
                    (
                        lm4.ratio < -0.2 and lm2.ratio < -0.05 and
                        lm2.absR * 1.5 < lm4.absR and lm2.low < lm4.low
                    )
                    or
                    (
                        lm4.day > 20 and lm4.ratio < -0.1 and
                        lm2.ratio < -0.05 and lm2.absR * 1.5 < lm4.absR and lm2.low < lm4.low
                    )

                )
                and k.ratio() > 0.01 and lm1.day < 3
                and (ls2.day > 3 or ls3.day > 3)

        ):
            # \
            #  \_
            #    \,
            return ConditionBean('a',k,'a1')

        lb2 = trend.getBig(-2)
        if (
            lb2.ratio < -0.3 and lm2.absR * 2 < lb2.absR and
            (lm2.ratio < -0.1 or lm2.day > 5) and k.ratio() > 0.01 and lm1.day < 3

        ):
            # \
            #  \_
            #    \,
            return ConditionBean('a', k, 'a2')
        if (
            lm4.ratio < -0.1 and lm2.absR * 1.2 < lm4.absR and
            lm4.day > lm2.day and lm2.low < lm4.low and
            k.ratio() > 0.01 and lm1.day < 4

        ):
            # \
            #  \_
            #    \,
            return ConditionBean('a', k, 'a3')
        if (
            lm6.ratio < -0.1 and lm2.absR < lm6.absR and (lm2.low - lm6.low) / lm6.low < -0.02 and
            (lm2.low - lm4.low) / lm4.low < -0.02 and lm2.ratio < -0.05 and
            lm6.middle > max(lm5.high, lm2.high) and
            lm1.day < 3 and k.ratio() > 0.01
        ):
            # \
            # \
            #  \/\/\
            #       \
            return ConditionBean('a', k, 'a4')
        if (
            lm6.ratio < -0.1 and ls2.absR * 2 < lm2.absR and  lm2.middle < max(lm5.low, lm2.low) and
            lm6.middle > max(lm5.high, lm2.high) and lm1.day < 3 and k.ratio() > 0.01
        ):
            # \
            #  \/\/\
            #       \
            return ConditionBean('a', k, 'a5')
        return None