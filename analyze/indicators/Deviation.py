# -*- coding: utf-8 -*-
class Deviation:
    """
    偏差
    attributes:
        period 粒度
        original 原始数据队列
        deviations list类型,值为[时间,偏差]
        absDeviations list类型,值为[时间,绝对偏差]
    """

    def __init__(self, period):
        self.period = period
        self.original = []
        self.deviations = []
        self.absDeviations = []

    def add(self, date, value):
        """
        :param  date
        :param  value
        """
        self.original.append(value)
        # 获取基准值
        base = self.original[0];
        if self.period < len(self.original):
            base = self.original[-self.period]
        # 计算偏差
        i = len(self.original) - self.period + 1 if self.period < len(self.original) else 0
        deviation = 0
        absDeviation = 0;
        while i < len(self.original):
            absDeviation += abs(self.original[i] - base)
            deviation += self.original[i] - base
            i += 1
        self.deviations.append([date, deviation / self.period])
        self.absDeviations.append([date, absDeviation / self.period])