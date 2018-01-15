# -*- coding: utf-8 -*-
class Base:
    """
    串行策略基础类
    """

    def decide(self,list,trader,i):
        """
        策略
        :param list: 测试数据
        :param trader: 交易者
        :param i: 当前在list中的位置
        :return:
        """
        raise "decide need implement"