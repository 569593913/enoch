# -*- coding: utf-8 -*-
import requests
import json
import KDataDao as kd
from K import *

def souhu_k(code,begin,end):
    """
    爬取搜狐数据,未除权
    :param code: 股票代码,普通股票为cn_股票代码,上证指数为zs_000001
    :param begin: 开始日期,格式为20170101
    :param end: 结束日期,格式为20170101
    :return:
    """
    url = "http://q.stock.sohu.com/hisHq?code=%s&start=%s&end=%s&order=D&period=d" \
          % (code,begin,end)
    print url
    r = requests.request('get',url,timeout=10)
    data = json.loads(r.content)[0]['hq']
    for d in data:
        k = K()
        k.code = code
        k.date = d[0]
        k.open = float(d[1])
        k.close = float(d[2])
        k.low = float(d[5])
        k.high = float(d[6])
        k.volume = float(d[7])
        kd.update_k(k)
    print 'complete code:%s,begin:%s,end:%s' %(code,begin,end)

def update_by_souhu_year(code='zs_000001',begin=19900101,end=20171001):
    """
    通过搜狐接口更新数据,把时间分割成一年一年的时间段来更新
    :param code:
    :param begin:
    :param end:
    :return:
    """
    while begin < end:
        try:
            souhu_k(code,begin,begin+10003)
            begin += 10000
        except BaseException as error:
            print(code + ' An exception occurred: {}'.format(error))