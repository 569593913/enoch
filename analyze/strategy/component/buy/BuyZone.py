# -*- coding: utf-8 -*-
from ..ConditionBean import *
class BuyZone:
    """
    买策略
    """

    def decide(self,listK,trend):
        k = listK[-1]
        pre = listK[-2]
        la1 = trend.getArea(-1)
        la2 = trend.getArea(-2)
        la3 = trend.getArea(-3)
        if (la1.getSegSize() == 1 and la2.low < la3.low and la2.ratio < la3.ratio and
            la2.day * 2 < la3.day and la2.getSegSize() > 4 and k.isUp()):
            return ConditionBean('z', k, 'z1')

        # if (la1.getSegSize() == 1 and la2.low < la3.low and (k.close - la2.high)/la2.high < 0.2 and
        #         (la2.ratio < la3.ratio or la2.day * 2 < la3.day) and
        #             k.close > la2.high and k.close > la3.high
        #     ):
        #     return ConditionBean('z', k, 'z2')

        # if ( (la1.getSegSize() > 8 or la1.day > 25) and (la2.getSegSize() > 8 or la2.day > 25) and
        #         k.close > la1.high and k.isUp() and la1.low < la2.low and
        #         (k.close - la1.high)/la1.high < 0.2
        #     ):
        #     """
        #      _____
        #     |_____|____ /
        #           |____|
        #     """
        #     return ConditionBean('z', k, 'z3')

        # if ((la2.getSegSize() > 8 or la2.day > 25) and (la3.getSegSize() > 8 or la3.day > 25) and
        #             k.close > la2.high and k.isUp() and la2.low < la3.low and
        #                 (k.close - la2.high) / la2.high < 0.2
        #     ):
        #     """
        #      _____
        #     |_____|____ /
        #           |____|
        #     """
        #     return ConditionBean('z', k, 'z4')

        if (la1.getSegSize() == 1 and (la2.getSegSize() > 8 or la2.day > 25) and
                    k.close > la2.high and k.isUp() and la2.low < la3.low and
                        (k.close - la2.high) / la2.high < 0.2
            ):
            """
             ___
            |___|______ /
                |______|
            """
            return ConditionBean('z', k, 'z5')
        return None