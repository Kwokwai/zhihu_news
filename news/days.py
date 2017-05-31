#-*- coding:utf8 -*-

import datetime


def yesterday_date(_date):
    now_date = datetime.datetime.strptime(_date, "%Y%m%d")
    prev_date = now_date - datetime.timedelta(days=1)
    return prev_date.strftime("%Y%m%d")


def tomoorow_date(_date):
    now_date = datetime.datetime.strptime(_date, "%Y%m%d")
    next_date = now_date + datetime.timedelta(days=1)
    return next_date.strftime("%Y%m%d")


def today(_date):
    if datetime.datetime.now().strftime("%Y%m%d") == _date:
        return True
    else:
        return False


def get_today(_date):
    return datetime.datetime.now().strftime("%Y%m%d")

