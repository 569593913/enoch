# -*- coding: utf-8 -*-
from analyze.indicators.MA import *
from analyze.indicators.Deviation import *
from analyze.indicators.Trend import  *
class ViewDataFactory:
    """
    视图数据工厂
    """

    @staticmethod
    def getCandlestick(list):
        """
        获取蜡烛图数据
        :param list:
        :return:返回K线和成交
        """
        data = []
        volume = []
        for k in list:
            # K线
            data.append([k.date, k.open, k.high, k.low, k.close])
            preClose = k.close
            # 成交量
            volume.append([k.date, k.volume])
        return data,volume

    @staticmethod
    def getMA(list,periodTuple):
        """
        获取均线
        :param list:
        :param periodTuple: 均线粒度
        :return: 返回dic,key均线粒度,value为均线
        """
        madic = {}
        for period in periodTuple:
            madic[period] = MA(period)
        for k in list:
            for ma in madic.values():
                ma.add(k.date,k.close)
        return madic

    @staticmethod
    def getTradeFlag(list,donwColor=None,upColor=None):
        """
        获取交易标记
        :param list: 交易记录
        :param donwColor: 阴线颜色
        :param upColor: 阳线颜色
        :return:
        """
        flags = []
        for r in list:
            if "buy" == r.type:
                # flags.append({"x": r.time, "title": r.type[:1],"text":r.condition,"fillColor": upColor})
                flags.append({"x":r.time,"title":r.condition,"text":("%s:%s") % (r.type,r.condition),"fillColor":upColor})
            else:
                flags.append({"x":r.time,"title":r.condition,"text":("%s:%s") % (r.type,r.condition),"fillColor": donwColor})
        return flags

    @staticmethod
    def getDeviation(listK, periodTuple):
        deviationDic = {}
        for period in periodTuple:
            deviationDic[period] = Deviation(period)
        for k in listK:
            for dev in deviationDic.values():
                dev.add(k.date, k.MOC())
        return deviationDic

    @staticmethod
    def getTrendLine(listK):
        trend = Trend()
        for k in listK:
            trend.add(k)
        return ViewDataFactory.trend2Line(trend);

    @staticmethod
    def trend2Line(trend):
        line = []
        for seg in trend.segments:
            line.append([seg.ek.date, seg.ek.extra])
        merge = []
        for m in trend.merges:
            merge.append([m.ek.date, m.ek.extra])
        big = []
        if len(trend.bigs) > 0:
            big.append([trend.bigs[0].bk.date, trend.bigs[0].bk.extra])
        for b in trend.bigs:
            big.append([b.ek.date, b.ek.extra])
        return line, merge, big

    @staticmethod
    def __trend2AreaRang(areas,listK):
        areaRange = []
        temp = set()
        for k in listK:
            temp.add(k.date)
        for area in areas:
            if len(area.segments) < 2:
                continue
            date = area.segments[0].bk.date
            endDate = area.segments[-2].ek.date
            # areaRange.append([date,None,None])
            while date <= endDate:
                if date in temp:
                    areaRange.append([date, area.low, area.high])
                date += 24 * 60 * 60 * 1000
            areaRange.append([endDate, None, None])
        return areaRange

    @staticmethod
    def trend2AreaRang(trend,listK):
        areaRange = ViewDataFactory.__trend2AreaRang(trend.areas,listK)
        # mareaRange = ViewDataFactory.__trend2AreaRang(trend.mareas, listK)
        return areaRange#,mareaRange
