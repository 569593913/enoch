# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
import StockDao as sd
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

def update_stock_basic():
    """
    更新股票列表（tushare pro接口）
    :return:
    """
    df = pro.query('stock_basic', exchange_id='',fields='ts_code,symbol,name,fullname,enname,exchange_id,curr_type,list_status,list_date,delist_date,is_hs')
    print(df)
    df.to_sql('stock_basic', engine, if_exists='replace', index=False)

def update_stock_day(trade_date):
    """
    更新股票数据 (tushare pro接口）
    :return:
    """
    df = pro.daily(trade_date=trade_date)
    i = 0;
    while True:
        try:
            sd.del_stock_day(start=trade_date)
            df.to_sql('stock_day', engine, if_exists='append', index=False)
            break
        except Exception as error:
             i = i + 1
             if i > 3:
                 raise error
    print('%s complete' % trade_date)






def update_period_stock_day(begin,end=None):
    """
    更新一段时间日线数据
    :param trade_date:
    :return:
    """
    endDay = None
    if end == None:
        endDay = datetime.today()
    else:
        endDay =  datetime.strptime(str(end), '%Y%m%d')
    currentDay = datetime.strptime(str(begin), '%Y%m%d')
    while (endDay - currentDay).days >= 0:
        weekno = currentDay.weekday()
        if weekno<5:
            update_stock_day(currentDay.strftime('%Y%m%d'))
        currentDay = currentDay + timedelta(days=1)

# update_stock_basic()
# update_stock_day(20180921)
# update_period_stock_day(20100101)
# update_period_stock_day(20011120,20100101)
update_period_stock_day(20190301)