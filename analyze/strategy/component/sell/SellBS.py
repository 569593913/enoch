# -*- coding: utf-8 -*-
class SellBS:
    """
    卖策略
     /\
       \
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
        ls1 = trend.getSegment(-1)
        ls2 = trend.getSegment(-2)
        lm2 = trend.getMerge(-3)
        # lm4 = trend.getMerge(-4)
        if (
            (k.isDown() and lm2.isDown() and lm2.bk.maxOC() > k.close and (lm2.bk.minOC() - k.close)/k.close < 0.03)
            #     or
            # (ls2.isDown() and ls2.bk.maxOC() > k.close and (ls2.bk.minOC() - k.close) / k.close < 0.03)
        ):
            """
            /\/
            """
            return "ba"
            # lm4 = trend.getMerge(-4)
        if (
            ( (k.isDown() and ls1.ratio > 0.1) or (ls2.ratio > 0.1 and ls1.day < 3) )
            and (k.close < pre.middle() or k.close < pre.MOC())
        ):
            """
             /`
            /
            """
            return "bb"
        if  k.maxOC() < ls2.low:
            """
             /\
               \
            """
            return "bc"
        if  k.isDown() and k.close < pre2.close and pre.close < pre2.close:
            return "bd"
        if k.close < condtionBean.buyK.low:
            return "bs"
        return None

