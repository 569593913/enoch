# -*- coding: utf-8 -*-
class K:
    """
    attributes:
    date,open,close,high,low,volume,code
    pct_chg 当天涨幅
    amount 成交额
    tor 换手率turnover
    vr 量比
    """
    def __init__(self,date=0,open=0,close=0,high=0,low=0,volume=0,code='',amount=0,tor=0,vr=0,pct_chg=0):
        self.date = date
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.code = code
        self.tor = tor
        self.amount = amount
        self.vr = vr
        self.pct_chg = pct_chg

    def isUp(self):
        """是否是阳线"""
        return self.open < self.close

    def isDown(self):
        """是否是阴线"""
        return self.open > self.close

    def ratio(self):
        """变化率"""
        if self.open==0:
            return 0
        return (self.close-self.open)/self.open

    def minOC(self):
        """获取开盘价和收盘价中的最小值"""
        return min(self.close,self.open)

    def maxOC(self):
        """获取开盘价和收盘价中的最大值"""
        return max(self.close,self.open)

    def MOC(self):
        """开盘和收盘中间位置的价格"""
        return (self.close+self.open)/2;
    def middle(self):
        """最高价和最低价中间位置的价格"""
        return (self.high+self.low)/2;
    def ULR(self):
        """上引线变化率"""
        return (self.high-self.maxOC())/self.maxOC()
    def DLR(self):
        """下引线变化率"""
        return (self.low-self.minOC())/self.minOC()
    def ratioAbs(self):
        """变化率绝对值"""
        return abs(self.ratio())
    def isUS(self):
        """是否涨停"""
        return self.pct_chg>9.85
    def isDS(self):
        """是否跌停"""
        return self.pct_chg<-9.85

    def __repr__(self):
        return "{date=%s,open=%s,close=%s,high=%s,low=%s,volume=%s,code=%s,tor=%s,pct_chg=%s}" \
               % (self.date,self.open,self.close,self.high,self.low,self.volume,self.code,self.tor,self.pct_chg)

