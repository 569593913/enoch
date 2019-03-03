# -*- coding: utf-8 -*-
class S:
    """
    attributes:
    date:日期
    up:上涨
    down:下跌
    us:涨停
    ds:跌停
    u5:涨5%
    d5:跌5%
    """
    def __init__(self,date=0,up=0,down=0,us=0,ds=0,u5=0,d5=0):
        self.date = date
        self.up = up
        self.down = down
        self.us = us
        self.ds = ds
        self.u5 = u5
        self.d5 = d5




    def __repr__(self):
        return '{date='+str(self.date)+',up='+str(self.up)+',down='+str(self.down)+\
               ',us='+str(self.us)+',ds='+str(self.ds)+',u5='\
               +str(self.u5)+',d5='+str(self.d5)+'}'

