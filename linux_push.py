#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Version : python3.6
@Author  : LiuSQ
@Time    : 2019/6/10 13:29
@Describe: 
"""
import shutil
import sys

import os

import time
from Util.ssh_helper import SSH, SSHClient

from Config.config import linux_backup, linux_site_detail

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 3:
        raise RuntimeError("传参不正确，请查看构建参数，谢谢~")
    windows_sites_detail_list = []
    center_path = ""
    dir_name = args[0].strip()
    site_names = args[1].strip()
    project_name = args[2].strip()
    site_names_list = []
    if "," in site_names:
        site_names_list = site_names.split(",")
    else:
        site_names_list.append(site_names)
    print("----需要发布的服务有" + len(site_names_list).__str__() + "个--------------------------")
    backup_path_list = linux_backup.get(project_name)
    basic_backup_path = backup_path_list[0]
    site_name_backup = backup_path_list[1]
    print("----备份文件是否存在-----")
    if not os.path.exists(basic_backup_path + site_name_backup):
        print("备份文件不存在，需要重新拉取")
        os.chdir(basic_backup_path)
        getSVN = os.popen(
            "F:\\tool_liusq\Apache-Subversion-1.10.2\\bin\\svn.exe checkout svn://10.18.192.219/root/document/发布文档/" + site_name_backup +
            " --username liusq --password liusq")
        print(getSVN.read())
    for site_name in site_names_list:
        print("------------------------------发布的是在" + dir_name + "下的" + site_name + "----------------------------")
        if not os.path.exists(basic_backup_path + site_name_backup + "\\" + dir_name + "\\测试包\\release\\" + site_name):
            raise RuntimeError("备份文件中不存在" + site_name + "的备份，请确认测试环境的发布")
        else:
            print("-------备份发版文件已经找到，进行uat发布---------------------")
            linux_site_detail_list = linux_site_detail.get(site_name)
            print("需要发布的服务器有" + len(linux_site_detail_list).__str__())
            # ["172.17.49.18", "esdyw", "land*NISSAN2000", "/data/container/tomcat_8.5.16_9081","cd /data/container/tomcat_8.5.16_9081/bin/;./shutdown.sh;./startup.sh","Tomcat started"]
            for linux_site in linux_site_detail_list:
                linux_ip = linux_site[0].strip()
                linux_username = linux_site[1].strip()
                linux_password = linux_site[2].strip()
                linux_to_release = linux_site[3]
                linux_cmd = linux_site[4]
                linux_check_str = linux_site[5]
                ssh = SSH(ip=linux_ip)
                ssh.login(username=linux_username, password=linux_password)
                ssh.upload_file(local_path=basic_backup_path + site_name_backup + "\\" + dir_name + "\\测试包\\release\\" + site_name, linux_path=linux_to_release + site_name)
                ssh.close_ssh()
                print("------------------------------------上传至服务器完毕------------------------")
                ssh_client = SSHClient(ip=linux_ip, username=linux_username, password=linux_password)
                log = ssh_client.exe_command(linux_cmd)
                log_result = log[len(log) - 1]
                if linux_check_str not in log_result:
                    ssh_client.ssh_client_close()
                    raise RuntimeError(site_name + "的服务在"+linux_ip+"上未启动成功")
                ssh_client.ssh_client_close()
                print("------------------------------------服务启动完毕-------------------------")
