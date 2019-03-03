# -*- coding: utf-8 -*-
from .HoldStock import *
from .TradeRecord import *
import threading
from datetime import *
class Trader:
    """
        模拟交易者
        attribute:
             original 初始资金
             cash 当前资金
             own 当前拥有的股票,map类,key为股票代码,value为HoldStock list
             record 交易记录
             taxRate 税率
             earningsLine 收益曲线,list类型,值为[时间,当开收益]
        """

    def __init__(self, original=1000000):
        """
        :param original:初始资金
        """
        self.original = original
        self.cash = original
        self.own = {}
        self.record = []
        self.earningsLine = []
        self.taxRate = 0.002
        self.lock = threading.Lock()

    def buy(self, code, buyTime, buyPrice, buyAmount=None,condition=None):
        """
        买一只股票
        :param code: 股票代码
        :param buyTime: 购买时间,long型
        :param buyPrice: 购买价格
        :param buyAmount: 购买金额
        :return:
        """
        with self.lock:
            if buyPrice <= 0:
                print("buyPrice=0 return")
                return
            #获取可买的金额
            if buyAmount == None or buyAmount > self.cash:
                buyAmount = self.cash
            #税后可买金额
            afterTaxAmount =  0
            tax = 0
            if buyAmount*(1+self.taxRate) < self.cash:
                afterTaxAmount = buyAmount
                tax = buyAmount*self.taxRate
            else:
                tax = self.cash * self.taxRate
                afterTaxAmount = self.cash - tax
            #可买到的数量
            canBuyQuantity = afterTaxAmount / buyPrice
            if canBuyQuantity < 100:
                # print('buy code:%s quantity:%s less 100,price:%s,cash:%s,original:%s,isHold:%s' \
                #       % (code,quantity,buyPrice,self.cash,self.original,self.isHold(code)))
                return
            holdStock = HoldStock(code, buyTime, buyPrice, buyPrice, canBuyQuantity)
            if code not in self.own:
                self.own[code] = []
            self.own[code].append(holdStock)
            tradeRecord = TradeRecord(code, buyTime, "buy", buyPrice, canBuyQuantity,condition)
            self.record.append(tradeRecord)
            self.cash -= (afterTaxAmount+tax)

    def isHold(self, code):
        if (code not in self.own) or (len(self.own[code]) < 1):
            return False
        return True

    def sell(self, code, sellTime, sellPrice, quantity=None,condition=None):
        """
        卖一只股票
        :param code: 股票代码
        :param sellTime: 卖出时间,long型
        :param sellPrice: 卖出价格
        :param quantity: 卖出数量
        :return:
        """
        with self.lock:
            if self.isHold(code) == False:
                # print("%s 没有持有,不可卖!" % code)
                return
            if sellPrice <= 0:
                print('price:%s' % sellPrice)
                return
            if None == quantity:
                quantity = 0
                for hs in self.own[code]:
                    quantity += hs.quantity
            if quantity < 100:
                print('sell quantity:% less 100' % quantity)
                return
            # 获取可卖出的数量
            actualSellQuantity = 0
            holdStocks = []
            for hs in self.own[code]:  # list顺序保证先买先卖
                if quantity > 0:
                    if (sellTime - hs.buyTime) > 1000:  # 超过一天才能卖,只有天粒度的数据才能这么简单计算
                        if hs.quantity >= quantity:
                            actualSellQuantity += quantity
                            hs.quantity -= quantity
                            quantity = 0
                        else:
                            actualSellQuantity += hs.quantity
                            quantity -= hs.quantity
                            hs.quantity = 0
                if hs.quantity != 0:  # quantity为0的清理掉
                    holdStocks.append(hs)
            self.own[code] = holdStocks
            self.cash += sellPrice * actualSellQuantity
            tradeRecord = TradeRecord(code, sellTime, "sell", sellPrice, actualSellQuantity,condition)
            self.record.append(tradeRecord)

    def asset(self):
        """
        获取当前的资产
        :return:
        """
        with self.lock:
            asset = self.cash
            for hsl in self.own.values():
                for hs in hsl:
                    asset += hs.capitalisation()
            return asset

    def earnings(self):
        """
        当前收益
        :return:
        """
        return (self.asset() - self.original) / self.original

    def fresh(self,date, dic):
        """
        刷新股票的价格
        :param dic: 股票代码:价格
        :return:
        """
        with self.lock:
            for code, price in dic.items():
                for hs in self.own.get(code, []):
                    hs.currentPice = price
        self.earningsLine.append([date,self.earnings()])

    def __repr__(self):
        return "Trader{earnings=%s,asset=%s,\noriginal=%s,\ncash=%s,\nown=%s,\nrecord=%s,\nearningsLine=%s}" % \
               (self.earnings(), self.asset(), self.original, self.cash, self.own, self.record,self.earnings())