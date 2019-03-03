# -*- coding: utf-8 -*-
import sys
sys.path.append("../data")
import MySQLdb
# import mysql.connector.pooling
from data.K import *
from sqlalchemy import create_engine
import tushare as ts
import time
from data.DBConfig import *
import threading
# dbconfig = {
#     "host":"127.0.0.1",
#     "port":"3306",
#     "user":"root",
#     "password":"root",
#     "database":"stock",
# }
# pool = mysql.connector.pooling.MySQLConnectionPool(pool_name='kData',pool_size=10,**dbconfig)

threadlocal = threading.local()


def del_tick_data(code,start,end):
    """删除code股票state到end时间的分笔数据"""
    db = MySQLdb.connect(address, user, password, schema)
    cursor = db.cursor()
    try:
        if(end==None):
            cursor.execute("delete from k_data where date>'%s'  and code='%s'" % (start, code))
        else:
            cursor.execute("delete from k_data where date>'%s' and date<'%s' and code='%s'" % (start,end,code))
        db.commit()
    except Exception as error:
        print('An exception occurred: {}'.format(error))
        db.rollback()
    finally:
        db.close()

def del_k_data(code,start,end=None):
    """删除code股票state到end时间的k线数据"""
    db = MySQLdb.connect(address, user, password, schema)
    cursor = db.cursor()
    try:
        if(end==None):
            cursor.execute("delete from k_data where date>='%s'  and code='%s'" % (start, code))
        else:
            cursor.execute("delete from k_data where date>='%s' and date<='%s' and code='%s'" % (start,end,code))
        db.commit()
    except BaseException as error:
        print('an exception occurred: {}'.format(error))
        db.rollback()
    finally:
        db.close()

def del_k_day(code,start,end=None):
    """删除code股票state到end时间的k线数据"""
    db = MySQLdb.connect(address, user, password, schema)
    cursor = db.cursor()
    try:
        if(end==None):
            cursor.execute("delete from k_day where date>='%s'  and code='%s'" % (start, code))
        else:
            cursor.execute("delete from k_day where date>='%s' and date<='%s' and code='%s'" % (start,end,code))
        db.commit()
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        db.rollback()
    finally:
        db.close()

def update_k(k):
    """保存或者更新一天的K线数据"""
    db = MySQLdb.connect(address, user, password, schema)
    cursor = db.cursor()
    try:
        cursor.execute("replace into k_data(date,open,close,high,low,volume,code,turnover) "
                       "values('%s',%d,%d,%d,%d,%d,'%s',%d)" % (k.date,k.open,k.close,k.high,k.low,k.volume,k.code,k.turnover))
        db.commit()
        return True;
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        db.rollback()
        return False;
    finally:
        db.close()

def update_k_day_af_t(list):
    """
    保存或者更新一批K线数据到k_day_af_t表
    """
    db = MySQLdb.connect(address, user, password, schema)
    cursor = db.cursor()
    try:
        for k in list:
            cursor.execute("replace into k_day_af_t(date,open,close,high,low,volume,code,amount,tor,vr) " 
                           "values('%s',%s,%s,%s,%s,%s,'%s',%s,%s,%s)" %
                           (k.date,k.open,k.close,k.high,k.low,k.volume,k.code,k.amount,k.tor,k.vr))
            db.commit()
        cursor.close()
        return True;
    except Exception as error:
        print('An exception occurred: {}'.format(error))
        db.rollback()
        return False;
    finally:
        db.close()

def get_stock_codes(market=None):
    """获取股票代码"""
    list = [];
    db = MySQLdb.connect(address, user, password, schema)
    cursor = db.cursor()
    try:
        if(market==None):
            cursor.execute("SELECT * FROM stock_info order by code" )
        else:
            cursor.execute("SELECT * FROM stock_info where market='%s'  order by code" % (market))
        results = cursor.fetchall()
        for row in results:
            list.append(row[0])
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
    finally:
        db.close()
    return list

def get_k_data(code, start, end=None):
    """获取code股票的K线数据"""
    list = [];
    cursor = initialized = getattr(threadlocal, 'cursor', None)
    if cursor == None:
        db = MySQLdb.connect(address, user, password, schema)
        threadlocal.cursor = db.cursor()
        cursor = threadlocal.cursor
    # db = pool.get_connection()
    # cursor = db.cursor()
    try:
        # bg = time.time()
        feild = "UNIX_TIMESTAMP(date)*1000 as date,open,close,high,low,volume,code,turnover"
        if end==None:
            cursor.execute("SELECT %s FROM k_data where code='%s' and date>='%s' order by date" % (feild,code, start))
        else:
            cursor.execute("SELECT %s FROM k_data where code='%s' and date>='%s' and date<='%s' order by date" % (feild,code, start, end))
        results = cursor.fetchall()
        # print('%s fetchall complete %s second' % (code, (time.time() - bg)))
        l = []
        for row in results:
            k = K(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            list.append(k)
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
    # finally:
    #     db.close()
    return list

def get_k_day_af(code, start, end=None):
    """获取code股票后复权的K线数据"""
    list = [];
    cursor = initialized = getattr(threadlocal, 'cursor', None)
    if cursor == None:
        db = MySQLdb.connect(address, user, password, schema)
        threadlocal.cursor = db.cursor()
        cursor = threadlocal.cursor
    # db = pool.get_connection()
    # cursor = db.cursor()
    try:
        # bg = time.time()
        feild = "UNIX_TIMESTAMP(date)*1000 as date,open,close,high,low,volume,code,tor,vr"
        if end==None:
            cursor.execute("SELECT %s FROM k_day_af where code='%s' and date>='%s' order by date" % (feild,code, start))
        else:
            cursor.execute("SELECT %s FROM k_day_af where code='%s' and date>='%s' and date<='%s' order by date" % (feild,code, start, end))
        results = cursor.fetchall()
        # print('%s fetchall complete %s second' % (code, (time.time() - bg)))
        for row in results:
            k = K(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
            list.append(k)
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
    # finally:
    #     db.close()
    return list


def get_update_k_data(code, start, end):
    """获取股票,如果数据库没有,就下载数据,再获取"""
    list = get_k_data(code, start, end)
    if len(list)<=0:
        print("update>>>>>"+code)
        df = ts.get_k_data(code, start="1990-01-01", retry_count=5)
        del_k_data(code,"1990-01-01")
        engine = create_engine('mysql://%s:%s@%s/%s' % (user,password,address,schema))
        df.to_sql('k_data', engine, if_exists='append', index=False)
    list = get_k_data(code, start, end)
    return list

def get_latest_date(code=None):
    """获取最近的更新时间"""
    db = MySQLdb.connect(address, user, password, schema)
    cursor = db.cursor()
    try:
        if code == None:
            cursor.execute("SELECT max(date) FROM k_data")
        else:
            cursor.execute("SELECT max(date) FROM k_data where code = '%s'" % code)
        results = cursor.fetchone()
        return  str(results[0])[0:10]
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
    finally:
        db.close()

def get_day_k(date):
    """
    获取一天所有股票的k线
    :param date:
    :return:
    """
    db = MySQLdb.connect(address, user, password, schema)
    cursor = db.cursor()
    list = []
    try:
        feild = "UNIX_TIMESTAMP(date)*1000 as date,open,close,high,low,volume,code,tor,vr"
        cursor.execute(
            "SELECT %s FROM k_day_af where date='%s'" % (feild, date))
        results = cursor.fetchall()
        # print('%s fetchall complete %s second' % (code, (time.time() - bg)))
        for row in results:
            k = K(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            list.append(k)
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
    finally:
        db.close()
    return list
# print get_update_k_data("002547","2017-01-01","2017-08-08")
# print get_latest_date()
# print get_k_data('000001','2017-01-01')
# print get_day_k("2016-12-06")