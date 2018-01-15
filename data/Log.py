# -*- coding: utf-8 -*-
class Log:
    """
    code 股票代码
    extra 额外参数
    type 类型:1日K线后复权
    flag 标记:-1失败,1成功
    update_time 更新时间
    begin_date 开始日期
    end_date 结束日期

    """
    def __init__(self,code,type,flag,begin_date,end_date,extra="",update_time=None):
        self.code = code
        self.extra = extra
        self.type = type
        self.flag = flag
        self.update_time = update_time
        self.begin_date = begin_date
        self.end_date = end_date