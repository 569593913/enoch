# -*- coding: utf-8 -*-
class SellC:
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
        lm3 = trend.getMerge(-3)
        if pre.ratio() < -0.08 and k.close < pre.MOC():
            return "c1"
        if (
            k.isDown() and not pre.isUp() and not pre2.isUp() and
            (k.close - pre2.close) / pre2.close < -0.03
        ):
            return "c2"
        if (
                (
                    lm1.high < lm2.high and lm2.ratio < -0.20 and
                    lm2.slope < -0.03 and (k.ratio() < -0.02 or k.close < pre.close)
                )
                or
                (
                    lm2.high < lm3.high and lm3.ratio < -0.20 and lm3.slope < -0.02 and
                    lm2.ratio > 0.05 and (k.isDown() or k.close < pre.close)
                )
                and condtionBean.buyK.date < lm1.bk.date

        ):
            # \
            #  \/`
            return "c3"
        return None

