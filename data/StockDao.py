# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import MySQLdb
# import mysql.connector.pooling
from data.S import *
from data.K import *
from sqlalchemy import create_engine
import tushare as ts
import time
from data.DBConfig import *
from datetime import datetime, timedelta
import threading
threadlocal = threading.local()


def del_stock_day(start, end=None):
    """
    删除股票数据
    :param start:
    :param end:
    :return:
    """
    if start == None:
        print("start param is None")
        return
    db = MySQLdb.connect(address, user, password, schema)
    cursor = db.cursor()
    try:
        if (end == None):
            cursor.execute("delete from stock_day where trade_date='%s' " % start)
        else:
            cursor.execute("delete from stock_day where trade_date>='%s' and trade_date<='%s'" % (start, end))
        db.commit()
    except Exception as error:
        print('An exception occurred: {}'.format(error))
        db.rollback()
    finally:
        db.close()

def get_stock_codes():
    """获取股票代码"""
    list = [];
    db = MySQLdb.connect(address, user, password, schema)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT ts_code FROM stock_basic order by ts_code" )
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
        feild = "UNIX_TIMESTAMP(STR_TO_DATE(trade_date,'%Y%m%d'))*1000 as date,open,close,high,low,vol,ts_code,amount,trade_date,pct_chg"
        if end==None:
            cursor.execute("SELECT %s FROM `stock_day` where ts_code='%s' and trade_date>='%s' order by trade_date" % (feild,code, start))
        else:
            cursor.execute("SELECT %s FROM `stock_day` where ts_code='%s' and trade_date>='%s' and trade_date<='%s' order by trade_date" % (feild,code, start, end))
        results = cursor.fetchall()
        # print('%s fetchall complete %s second' % (code, (time.time() - bg)))
        l = []
        for row in results:
            k = K(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
            k.td = row[8]
            list.append(k)
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
    # finally:
    #     db.close()
    return list

def get_day_data(date):
    """获取某天后所有股票的K线数据"""
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
        feild = "UNIX_TIMESTAMP(STR_TO_DATE(trade_date,'%Y%m%d'))*1000 as date,open,close,high,low,vol,ts_code,amount,trade_date,pct_chg"
        cursor.execute("SELECT %s FROM `stock_day` where trade_date>='%s' order by ts_code,trade_date" % (feild,date))
        results = cursor.fetchall()
        # print('%s fetchall complete %s second' % (code, (time.time() - bg)))
        l = []
        for row in results:
            k = K(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            k.td = row[8]
            k.pct_chg = row[9]
            list.append(k)
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
    # finally:
    #     db.close()
    return list

def get_statistic(begin,end=None):
    """
    获取统计信息
    :param begin:
    :param end:
    :return:
    """
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
        feild = "UNIX_TIMESTAMP(STR_TO_DATE(trade_date,'%Y%m%d'))*1000 as date,up,down,us,ds,u5,d5"
        if end != None:
            cursor.execute("SELECT %s FROM `statistic` where trade_date>='%s' and trade_date<='%s'" % (feild, begin, end))
        else:
            cursor.execute("SELECT %s FROM `statistic` where trade_date>='%s' " % (feild, begin))
        results = cursor.fetchall()
        # print('%s fetchall complete %s second' % (code, (time.time() - bg)))
        l = []
        for row in results:
            s = S(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            list.append(s)
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
    # finally:
    #     db.close()
    return list

def get_statistic_real(begin, end=None):
    """
    获取统计信息,实时算
    :param begin:
    :param end:
    :return:
    """
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
        up = " sum(case when pct_chg>0 then 1 else 0 end)"
        down = " sum(case when pct_chg<0 then 1 else 0 end)"
        u5 = " sum(case when pct_chg>=5 then 1 else 0 end)"
        d5 = " sum(case when pct_chg<=-5 then 1 else 0 end)"
        us = " sum(case when pct_chg>=9.85 then 1 else 0 end)"
        ds = " sum(case when pct_chg<=-9.85 then 1 else 0 end)"
        feild = " UNIX_TIMESTAMP(STR_TO_DATE(trade_date,'%Y%m%d'))*1000 as date"
        feild = " %s,%s up,%s down,%s us,%s ds,%s u5,%s d5" % (feild,up,down,us,ds,u5,d5)
        group = " group by trade_date"
        order = " order by trade_date"
        sql = "SELECT %s FROM `stock_day` where trade_date>='%s'  %s %s" % (feild, begin, group, order)
        if end != None:
            sql = "%s and trade_date<=%s" % (sql, end)
        # print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        # print('%s fetchall complete %s second' % (code, (time.time() - bg)))
        l = []
        for row in results:
            s = S(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            list.append(s)
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
    # finally:
    #     db.close()
    return list


# print(get_statistic_real(begin="20190101"))
# print(get_day_data("20190101"))
