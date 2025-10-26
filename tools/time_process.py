import math
import numpy as np
import time
import datetime
import calendar


def get_doy_str(doy_int):
    # doy_str = str(doy_int)
    # return '0' * (3 - len(doy_str)) + doy_str
    return str(doy_int).zfill(3)


# date:YYYYMMDD
# return: int
def date_to_doy(date: str):
    year = date[:4]
    month = date[4:6]
    day = date[6:]
    # print(year, month, day)
    date_base = datetime.date(int(year), 1, 1)
    date = datetime.date(int(year), int(month), int(day))
    doy = date.__sub__(date_base).days + 1
    return doy


def dates_to_doys(lis):
    return [date_to_doy(date) for date in lis]


# doy:YYYYooo
# return: str
def doy_to_date(doy):
    doy_obj = datetime.datetime.strptime(str(doy), '%Y%j')  # 将字符串转换成datetime对象
    date_str = doy_obj.strftime('%Y%m%d')  # 将datetime对象转换成字符串，格式为“YYYYMMDD”
    # print("{} → {}".format(doy, date_str))
    return date_str


def now_time(format='%Y-%m-%d %H:%M:%S'):
    now_time = time.strftime(format, time.localtime())
    # print(now_time)
    return now_time


def diff_day_num(date1, date2):
    """ date format : YYYYMMDD """
    d1 = datetime.datetime.strptime(date1, "%Y%m%d").date()
    d2 = datetime.datetime.strptime(date2, "%Y%m%d").date()
    return (d1 - d2).days


def get_pre_date(date, day_num=1):
    return (datetime.datetime.strptime(date, "%Y%m%d").date() - datetime.timedelta(days=day_num)).strftime('%Y%m%d')


def get_year_daynum(year):
    return 366 if calendar.isleap(int(str(year))) else 365
