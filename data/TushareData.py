# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
import KDataDao as kd
import threading
from K import *
import time
from Log import *
import LogDao as logDao
from datetime import datetime, timedelta
from DBConfig import *
import tushare as ts
ts.set_token('64579ca6c4c7b19130eb58f8b5781841d9aceda9ba7a48356ad58060')
pro = ts.pro_api()
engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8' % (user, password, address, schema),encoding='utf-8')



def update_k_data(code,start,end=None):
    """更新一只股票的K线数据"""
    begin = time.time()
    df = None
    if(end==None):
        df = ts.get_k_data(code,autype='hfq', start=start,retry_count=3)
    else:
        df = ts.get_k_data(code,autype='hfq',  start=start, end=end,retry_count=3)
    kd.del_k_data(start=start, end=end,code=code)
    df.to_sql('k_data', engine, if_exists='append', index=False)
    print("%s complete %s~%s use:%ss" % (code,start,end,time.time()-begin))

def update_k_day_af_t(cons,code,start,end=None):
    """
    更新一只股票的K线数据,新接口
    """
    begin = time.time()
    df = None
    if(end==None):
        df = ts.bar(code,conn=cons,adj='hfq',freq="D",start_date=start,factors=['vr','tor'],retry_count=3)
    else:
        df = ts.bar(code,conn=cons,adj='hfq',freq="D",start_date=start,end_date=end,factors=['vr','tor'],retry_count=3)
    # kd.del_k_day(start=start, end=end,code=code)
    list = []
    for index, row in df.iterrows():
        tor = float(row['tor']) if row['tor']!='nan' else 0
        vr = float(row['vr']) if row['vr'] != 'nan' else 0
        k = K(index,row['open'],row['close'],row['high'],row['low'],row['vol'],row['code'],row['amount'],tor,vr)
        list.append(k)
    beginInsert = time.time()
    kd.update_k_day_af_t(list)
    print("%s complete start=%s end=%s total=%ss insert=%ss" % (code,start,end,(time.time()-begin),(time.time()-beginInsert)))

def update_today_all():
    """更新今天所有数据"""
    df=ts.get_today_all()
    i = 0;
    while (i<len(df)):
        k = K()
        k.high=df.high[i]
        k.date=time.strftime("%Y-%m-%d",time.localtime())
        k.close=df.trade[i]
        k.code=df.code[i]
        k.low=df.low[i]
        k.open=df.open[i]
        k.turnover=df.turnoverratio[i]
        k.volume=df.volume[i]
        kd.update_k(k)
        i+=1
        print(k.code+"complete>>>"+str(i))

class KDataUpdateThread (threading.Thread):
    queueLock = threading.Lock()

    def __init__(self,list,begin,end,func,log=True):
        threading.Thread.__init__(self)
        self.list = list
        self.begin = begin
        self.end = end
        self.func = func
        self.log = log
        # self.cons = ts.get_apis()
        self.failure = []

    def run(self):
        code = None
        while True:
            if len(self.list)>0:
                KDataUpdateThread.queueLock.acquire()
                try:
                    code = self.list.pop()
                finally:
                    KDataUpdateThread.queueLock.release()
            else:
                break;
            flag = -1
            try:
                # self.func(self.cons,code, self.begin, self.end)
                begin = self.begin
                if self.begin == None:
                    begin = kd.get_latest_date(code)
                    now = str(datetime.now())[0:10]
                    if begin > now:
                        continue
                self.func(code, begin, self.end)
                flag = 1
                continue
            except Exception as error:
                print('%s %s~%s %s' % (code,self.begin,self.end,error))
                self.failure.append(code)
            finally:
                pass
                if self.log == True:
                    logDao.insert(Log(code, 1, flag, self.begin, self.end))


def update_period_k_data(begin=None,end=None,market=None,threadCount=3):
    """
    更新数据,当begin为None时,
    :param begin:
    :param end:
    :param market:
    :param threadCount:
    :return:
    """
    list = kd.get_stock_codes(market)
    if threadCount==None:
        threadCount = 5
    tds = []
    for i in range(threadCount):
        # t = KDataUpdateThread(list,begin,end,update_k_day_af_t)
        t = KDataUpdateThread(list,begin,end,update_k_data,False)
        t.start()
        tds.append(t)
    for t in tds:
        t.join()
    failure = []
    for t in tds:
        failure.append(t.failure)
    print("failure:"+str(failure))

def update_k_year(byear,eyear,threadCount=3,market=None,log=True):
    """
    按年更新数据
    byear 开始年,整型
    eyear 结束年,整型
    threadCount 线程数
    :return:
    """
    year = eyear
    failure = []
    while year >= byear:
        begin = "%s-01-01" % year
        end = "%s-01-05" % (year+1)
        # end = "%s-12-20" % (year )
        list = logDao.getNeedUpdateCode(1,begin,end,market)
        if len(list) < 1:
            year -= 1
            continue
        tds = []
        for i in range(threadCount):
            # t = KDataUpdateThread(list,begin,end,update_k_day_af_t)
            t = KDataUpdateThread(list, begin, end, update_k_data,log)
            t.start()
            tds.append(t)
        for t in tds:
            t.join()
        for t in tds:
            failure.append(t.failure)
        print("%s %s~%s complete!" % (market,begin,end))
        year -= 1
    print("failure:%s %s" % (len(failure),str(failure)))


# begin = time.time()
# df = ts.bar("000002",conn=ts.get_apis(),freq="1min", start_date='2017-01-02',end_date='2017-01-03',factors=['vr','tor'],retry_count=10)
# print df
# print 'complete %s second' %  (time.time()-begin)
# update_k_year(1990,2018,5,'sza',True);
# update_k_year(1990,2018,5,'sha',True);
# update_period_k_data()
# update_k_data('601218',start='2018-01-26')
# print ts.get_k_data('601218',autype='hfq', start='2018-01-26',retry_count=3)
