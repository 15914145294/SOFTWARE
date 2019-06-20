# -*- coding:utf-8 _*-
""" 
@author:Administrator 
@file: clear_device.py 
Description : 用于定时清理过时的备份文件以及不需要的日志文件
@time: 2019/06/06 
"""
import os
import re
import time

BASE_JAR_DIR = r'/data/jar'
BASE_LOG_DIR = r'/data/logs'
dir_list = [BASE_JAR_DIR, BASE_LOG_DIR]


class DeviceClear(object):


    def __init__(self):
        self.backup_dir = []
        self.log_dir = []
        self.file_list = []
        self.dir_l = []
        self.list_dir()
        self.back_jar_list = []
        self.log_file_list = []
        print(self.log_dir)
        print(self.backup_dir)

        # print(self.backup_dir)

    def list_dir(self):
        """
        获取备份文件件以及日志文件夹其中日志文件夹过滤nginx的日志
        :return:
        """
        for path in dir_list:
            for root, dirs, files in os.walk(path):
                # 排除nginx目录
                for d in dirs:
                    if 'nginx' not in d:
                        self.dir_l.append(os.path.join(root, d))

        for b in self.dir_l:
            # 获取备份文件目录
            if 'bakup' in b:
                self.backup_dir.append(b)
                # 获取日志文件目录
            elif 'logs' in b:
                self.log_dir.append(b)

    def get_files(self):
        """
        1）获取需要删除的jar包文件
        2）获取需要删除的日志文件
        3）删除获取到的jar包以及日志文件
        :param path:
        :return:
        """
        for path in self.backup_dir:
            # jar包格式：outerService.jar.2019-03-14_16:21:58
            for root, dirs, files in os.walk(path):
                for f in files:
                    try:
                        # ('csManager.jar.2019-06-05_20:20:40', ':=', True)
                        if len(re.split("jar\.|_", f)) >2:
                            file=re.split("jar\.|_", f)[1]
                        if self.Caltime(file):
                            self.back_jar_list.append(os.path.join(root, f))
                    except:
                        continue


        for path in self.log_dir:
            # 日志文件格式：csc_info.2019-04-15.0.log
            for root, dirs, files in os.walk(path):
                for f in files:
                    try:
                        if len(re.split("\.", f)[1])>2:
                            m=re.match('.*?(\d+-\d+-\d+).*',f).groups()[0]
                        if self.Caltime(m):
                            self.log_file_list.append(os.path.join(root, f))
                    except:
                        continue


    def Caltime(self, v_date):
        """
        计算日期，只取三天内的文件
        :return:
        """
        import datetime
        v_time = time.strptime(v_date, "%Y-%m-%d")
        sys_time = datetime.datetime.now().strftime('%Y-%m-%d')
        now_time = time.strptime(sys_time, '%Y-%m-%d')

        date1 = datetime.datetime(v_time[0], v_time[1], v_time[2])
        date2 = datetime.datetime(now_time[0], now_time[1], now_time[2])
        # 返回两个变量相差的值，就是相差天数,
        if int(str(date2 - date1).split(" ")[0]) >= 3:
            return True
        return False

    def remove(self):
        self.get_files()
        print(self.back_jar_list)
        for i in self.back_jar_list:
            os.remove(i)
        print(self.log_file_list)
        for j in self.log_file_list:
            os.remove(j)
        return "To remove files,success"


if __name__ == "__main__":
    print(DeviceClear().remove())
