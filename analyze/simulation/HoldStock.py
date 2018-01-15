# -*- coding: utf-8 -*-
class HoldStock:
    """
    持有的股票
    attribute:
         code:股票代码
         buyTime:够买时间,long型
         buyPrice:够买价格
         currentPice:当前价格
         quantity:拥有数量
    """

    def __init__(self,code,buyTime,buyPrice,currentPice,quantity):
        """
        :param code:股票代码
        :param buyTime:购买时间,long型
        :param buyPrice:购买价格
        :param currentPice:当前价格
        :param quantity:拥有数量
        """
        self.code = code
        self.buyTime = buyTime
        self.buyPrice = buyPrice
        self.quantity = quantity
        self.currentPice = currentPice


    def capitalisation(self):
        """
        获取当前市值
        :return:
        """
        return self.quantity*self.currentPice

    def __repr__(self):
        """
        :return:
        """
        return "HoldStock{code=%s,buyTime=%s,buyPrice=%s,currentPice=%s,quantity=%s}" % \
               (self.code,self.buyTime,self.buyPrice,self.currentPice,self.quantity)
