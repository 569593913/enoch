# -*- coding: utf-8 -*-
import MySQLdb
from Log import *
from DBConfig import *
def insert(log):
    """保存或者更新一批K线数据"""
    db = MySQLdb.connect(address, user, password, schema)
    cursor = db.cursor()
    try:
        sql = "replace into stock.update_log(code,extra,type,flag,update_time,begin_date,end_date) " \
              "values('%s','%s',%s,%s,now(),'%s','%s')" \
              % (log.code, log.extra, log.type, log.flag, log.begin_date, log.end_date)
        cursor.execute(sql)
        db.commit()
        return True;
    except Exception as error:
        print('An exception occurred: {}'.format(error))
        db.rollback()
        return False;
    finally:
        db.close()

def getNeedUpdateCode(type,beginDate,endDate,market=None):
    """
    查询需要更新的数据
    type 1日向后复权
    beginDate 开始日期
    endDate 结束日期
    """
    db = MySQLdb.connect(address, user, password, schema)
    cursor = db.cursor()
    list = []
    try:
        sql2 = None
        sql1 = "select code from stock.update_log where flag = -1 and type = %s and begin_date = '%s' and end_date = '%s'" % (type,beginDate,endDate)
        if market == None:
            sql2 = " select code from stock.stock_info i  WHERE NOT EXISTS " \
                  "(select null from stock.update_log u where " \
                  "u.code = i.code and u.flag = 1 and type = %s and begin_date = '%s' and end_date = '%s')" % (type,beginDate,endDate)
        else:
            sql2 = " select code from stock.stock_info i  WHERE NOT EXISTS " \
                   "(select null from stock.update_log u where " \
                   "u.code = i.code and u.flag = 1 and type = %s and begin_date = '%s' and end_date = '%s') and market = '%s' " % (
                   type, beginDate, endDate, market)
        sql = sql1 + " union " + sql2
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            list.append(row[0])
    except Exception as error:
        print('An exception occurred: {}'.format(error))
        db.rollback()
    finally:
        cursor.close()
        db.close()
    return list
