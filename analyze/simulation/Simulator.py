# -*- coding: utf-8 -*-
from .Trader import *
import  data.KDataDao as kd
class Simulator:
    """
    模拟器,模拟交易
    attribute:
         trader 模拟帐户
         parallelStrategy 并行交易策略
         sequenceStrategy 串行交易策略
         begin: 开始时间
         end: 结束时间
    """

    def __init__(self,sequenceStrategy=None,parallelStrategy=None,begin='2017-01-01',end=None,trader=None):
        """
        初始化模拟器
        :param trader:
        :param parallelStrategy: 并行交易策略
        :param sequenceStrategy: 串行交易策略
        :param begin: 开始时间
        :param end: 结束时间
        """
        if None==trader:
            trader = Trader()
        self.trader = trader
        self.parallelStrategy = parallelStrategy
        self.sequenceStrategy = sequenceStrategy
        self.begin = begin
        self.end = end


    def runParallel(self,parallelStrategy=None,begin=None,end=None):
        """
        并行交易模拟
        :param parallelStrategy: 并行交易策略
        :param begin:
        :param end:
        :return:
        """
        if None==begin:
            begin = self.begin
        if None==end:
            end = self.end
        if None==parallelStrategy:
            parallelStrategy = self.parallelStrategy
        if None == parallelStrategy:
            raise '没有设置并行交易策略'
            return

    def runSingle(self,code,sequenceStrategy=None,begin=None,end=None,list=None):
        """
         单个交易模拟
        :param code: 股票编号
        :param sequenceStrategy: 串行交易策略
        :param begin:
        :param end:
        :return:
        """
        if None==sequenceStrategy:
            sequenceStrategy = self.sequenceStrategy
        if None == sequenceStrategy:
            raise '没有设置串行交易策略'
        if None==begin:
            begin = self.begin
        if None==end:
            end = self.end
        # 获取数据
        if None==list:
            list = kd.get_k_data(code,begin,end)
        if len(list)<1:
            print('%s begin:%s,end:%s 没有测试数据' % (code,begin,end))
            return
        i = 0
        while i<len(list):
            sequenceStrategy.decide(list, self.trader, i)
            self.trader.fresh(list[i].date, {code: list[i].close})
            i+=1


    def runSequence(self,market=None,sequenceStrategy=None,begin=None,end=None):
        """
        串行交易模拟
        :param market:
        :param sequenceStrategy: 串行交易策略
        :param begin:
        :param end:
        :return:
        """
        if None==sequenceStrategy:
            sequenceStrategy = self.sequenceStrategy
        if None == sequenceStrategy:
            raise '没有设置串行交易策略'
            return
        if None==begin:
            begin = self.begin
        if None==end:
            end = self.end
        # 获取股票池
        codes = kd.get_stock_codes(market)
        for code in codes:
            # 获取股票数据
            list = kd.get_k_data(code, begin, end)
            if len(list) < 1:
                print('%s begin:%s,end:%s 没有测试数据' % (code, begin, end))
                continue
            i = 0
            while i < len(list):
                sequenceStrategy.decide(list, self.trader, i)
                self.trader.fresh(list[i].date, {code:list[i].close})
                i += 1