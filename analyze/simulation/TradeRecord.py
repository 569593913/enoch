# -*- coding: utf-8 -*-
class TradeRecord:
    """
    交易记录
    atrribute:
         code: 股票代码
         time: 交易时间,long型
         type: 交易类型
         condtion: 买卖条件标记
         price: 交易价格
         quantity: 交易数量
    """
    def __init__(self,code,time,type,price,quantity,condition=""):
        """
        :param code: 股票代码
        :param time: 交易时间,long型
        :param type: 交易类型,buy购买,sell卖出
        :param condtion: 买卖条件标记
        :param price: 交易价格
        :param quantity: 交易数量
        """
        self.code = code
        self.time = time
        self.type = type
        self.price = price
        self.condition = condition
        self.quantity = quantity

    def __repr__(self):
        return "TradeRecord{code=%s,time=%s,type=%s,condition=%s,price=%s,quantity=%s}" % \
               (self.code,self.time,self.type,self.conditon,self.price,self.quantity)