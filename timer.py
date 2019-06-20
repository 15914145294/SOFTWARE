# -*- coding:utf-8 _*-
""" 
@author:Administrator 
@file: time_tool.py 
Description :
@time: 2019/06/10 
"""
import datetime
import time


def parse_timestr(time_str, flag=True):
    """
    将时间字符串转换为时间戳格式time.mktime(t)
    :param time_str: 时间字符串,格式为：2019-01-01 12:12:12 或 2019-01-01
    :param flag:标志位，决定输入时间的格式
    :return:
    """
    if flag:
        struct_time = time.strftime(time_str, "%Y-%m-%d %H:%M:%S")
    else:
        struct_time = time.strftime(time_str, "%Y-%m-%d")
    return time.mktime(struct_time)


def parse_timestamp(time_stamp, flag=True):
    """
    将时间戳转换为字符串    time.strftime()
    :param time_stamp: 时间戳格式
    :param flag:
    :return: 时间字符串,格式为：2019-01-01 12:12:12 或 2019-01-01
    """
    localtime = time.localtime(time_stamp)
    if flag:
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
    else:
        time_str = time.strftime("%Y-%m-%d", localtime)
    return time_str


def range_day(interval_day):
    """
    获取指定天数内的日期列表
    :param interval_day: 指定天数
    :return:
    """
    c_time = (int(time.time() / (24 * 3600)) + 1) * 24 * 3600
    day_range_str = c_time - 24 * 3600 * interval_day
    day_list = [parse_timestamp(t, flag=False) for t in range(day_range_str, c_time, 24 * 3600)]
    return day_list


def is_workday(time_str):
    """
    传入时间字符串，判断传入的时间是否为工作日
    :param time_str: 时间格式为"2019-06-10 10:10:20" 或者 "2019-06-10"
    :return: True/False
    """
    workday_list = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    holiday_list = ["Sat", "Sun"]
    struct_time = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    day = time.strftime("%a", struct_time)
    if day in workday_list:
        return True
    return False


def is_holiday(time_str):
    """
    传入时间字符串，判断传入的时间是否为周末
    :param time_str: 时间格式为"2019-06-10 10:10:20" 或者 "2019-06-10"
    :return: True/False
    """
    workday_list = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    holiday_list = ["Sat", "Sun"]
    struct_time = time.strptime(time_str, "%Y-%m-%d %Y:%H:%S")
    day = time.strftime("%a", struct_time)
    if day in holiday_list:
        return True
    return False


def get_day_list(start_timestamp, end_timestamp, flag=True):
    """
    获取开始时间戳，结束时间戳之前的日期列表
    :param start_timestamp: 开始时间戳
    :param end_timestamp: 结束时间戳
    :return: 日期列表
    """
    tmp = range(int(start_timestamp), int(end_timestamp), 24 * 3600)
    if flag:
        tmp_range = [{"day_str": parse_timestamp(i, flag=False)} for i in tmp]

    else:
        tmp_range = [parse_timestamp(i, flag=False) for i in tmp]
    return tmp_range


def get_workday_count(start_timestamp, end_timestamp):
    """
    获取30天内的工作天数
    :param start_timestamp:
    :param end_timestamp:
    :param flag:
    :return: 工作天数
    """
    day_list = range(int(start_timestamp), int(end_timestamp) + 3600 * 24, 3600 * 24)
    day_str_list = [parse_timestamp(t, flag=False) for t in day_list if is_workday(parse_timestamp(t))]
    return len(day_str_list)


def convert_timestr_to_datetime(timestr, flag=True):
    """
    将时间字符串转换为datetime格式
    :param timestr: 时间字符串，例如：2019-01-01 12:12:12 或者 2019.01.01 12:12:12
    :param flag:
    :return:
    """
    if flag:
        try:
            tmp_datetime = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
        except:
            tmp_datetime = datetime.datetime.strptime(timestr, "%Y-%m-%d")
    else:
        try:
            tmp_datetime = datetime.datetime.strptime(timestr, "%Y.%m.%d %H:%M:%S")
        except:
            tmp_datetime = datetime.datetime.strptime(timestr, "%Y.%m.%d")
    return tmp_datetime


def parse_dur_time(d1, d2):
    """
    获取两个datetime时间 间隔的日期数(天数，小时数和秒数)
    :param d1: 开始时间
    :param d2: 结束时间
    :return:
    """
    dur_str = ""
    d2 = convert_timestr_to_datetime(d2)
    d1 = convert_timestr_to_datetime(d1)
    dur_day = (d2 - d1).days
    dur_second = (d2 - d1).seconds
    if dur_day > 0:
        dur_str = "%s天" % str(dur_day)
    if dur_second - 3600 > 0:
        dur_hours = dur_second // 3600
        dur_str += "%s小时" % str(dur_hours)
    if dur_second % 3600 > 60:
        dur_minu = (dur_second % 3600) // 60
        dur_str += "%s分钟" % str(dur_minu)
    dur_str += "%s秒" % (dur_second % 60)

    return dur_str


if __name__ == "__main__":
    print(parse_dur_time('2019-06-06 08:10:20', '2019-06-10'))
