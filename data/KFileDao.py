# -*- coding: utf-8 -*-
import MySQLdb
# import mysql.connector.pooling
import time
import threading
import os
from DBConfig import *
def updateFromFile(dir,fileName,db):
    """从一个文件里面更新数据"""
    strs = fileName.split("#")
    if len(strs) != 2:
        raise "文件格式不正确 %s" % fileName
    code = strs[1].split(".")[0].strip()
    cursor = db.cursor()
    with open(dir+"/"+fileName, "r") as f:
        lines = f.readlines()
        sql = "replace into k_day_af(date,code,open,high,low,close,volume,amount) VALUES ('%s','%s',%s,%s,%s,%s,%s,%s)"
        for line in lines:
            ds = line.split(",")
            #简单数据校验
            if len(ds[0]) != 10:
                continue
            cursor.execute(sql % (ds[0].strip(),code,ds[1].strip(),ds[2].strip(),ds[3].strip(),ds[4].strip(),ds[5].strip(),ds[6].strip()))
            db.commit()
    print "file %s complete" % fileName
    cursor.close()

def updateFromFiles(dir,threadCount):
    files = os.listdir(dir)
    print len(files)
    tds = []
    for i in range(threadCount):
        t = UpdateThread(files,dir)
        t.start()
        tds.append(t)
    for t in tds:
        t.join()
    failure = []
    for t in tds:
        failure.append(t.failure)
    print "failure:" + str(failure)


class UpdateThread (threading.Thread):
    queueLock = threading.Lock()

    def __init__(self,list,dir):
        threading.Thread.__init__(self)
        self.list = list
        self.dir = dir
        self.failure = []

    def run(self):
        fileName = None
        db = MySQLdb.connect(address, user, password, schema)
        try:
            while True:
                if len(self.list)>0:
                    UpdateThread.queueLock.acquire()
                    try:
                        fileName = self.list.pop()
                    finally:
                        UpdateThread.queueLock.release()
                else:
                    break;
                try:
                    updateFromFile(self.dir,fileName,db)
                    continue
                except Exception as error:
                    print(fileName + ' An exception occurred: {}'.format(error))
                    self.failure.append(fileName)
        except Exception as error:
            print(fileName + ' An exception occurred: {}'.format(error))
        finally:
            db.close()

updateFromFiles("/Users/enoch/Documents/stock/sha",10)