#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Version : python3.6
@Author  : LiuSQ
@Time    : 2019/3/14 17:16
@Describe: 
"""
import sys

import os

import xlrd
import xlwt
from Util.ssh_helper import SSH, SSHClient
from xlutils.copy import copy
from Config.config import VERSION, EMP_BASIC_PATH_GIT, EMP_BASIC_PATH, WAR_NAME, command

# git rev-parse HEAD 获取git最新一次提交的ID
if __name__ == '__main__':
    args = sys.argv[1:]
    parameter_first = args[0]
    project_names = []
    if "," in parameter_first:
        project_names = parameter_first.split(",")
    else:
        project_names.append(parameter_first)
    print("需要打包的个数为：" + len(project_names).__str__())
    err_num = 0
    print("--------------------------------------------拉取开发代码，并创建测试分支------------------------------------------------")
    branch_name = args[1].strip()
    commit_id = args[2].strip()
    if "_" in branch_name:
        version_branch = branch_name.split("_")[1]
    elif "-" in branch_name:
        version_branch = branch_name.split("-")[1]
    branch_name_new = "release-" + version_branch
    print("需要备份的版本号为：" + version_branch)
    os.chdir(EMP_BASIC_PATH_GIT)

    checkout = "git checkout " + commit_id
    print("执行的命令为：" + checkout)
    checkout_cmd = os.popen(checkout)
    checkout_log = checkout_cmd.read()
    print(checkout_log)

    del_branch = "git branch -d " + branch_name_new
    print("执行的命令为：" + del_branch)
    del_branch_cmd = os.popen(del_branch)
    del_branch_log = del_branch_cmd.read()
    print(del_branch_log)

    checkout_local = "git checkout -b " + branch_name_new + " " + commit_id
    print("执行的命令为：" + checkout_local)
    checkout_local_cmd = os.popen(checkout_local)
    checkout_local_log = checkout_local_cmd.read()
    print(checkout_local_log)

    get_branch = "git branch -a"
    print("执行的命令为：" + get_branch)
    get_origin_branch_cmd = os.popen(get_branch)
    get_origin_branch_log = get_origin_branch_cmd.read()
    print(get_origin_branch_log)
    if "remotes/origin/" + branch_name_new in get_origin_branch_log:
        del_origin_branch_cmd = os.popen("git push origin --delete " + branch_name_new)
        print("执行的命令为：" + "git push origin --delete " + branch_name_new)
        del_origin_branch_log = del_origin_branch_cmd.read()
        print(del_origin_branch_log)

    push = "git push origin " + branch_name_new + ":" + branch_name_new
    print("执行的命令为：" + push)
    push_cmd = os.popen(push)
    push_log = push_cmd.read()
    print(push_log)
    print("--------------------------------------------创建分支完成------------------------------------------------")
    for project_name in project_names:
        try:
            print(
                "------------------------------------------当前打包的是" + project_name + "--------------------------------------------")
            os.chdir(EMP_BASIC_PATH_GIT)
            log = os.popen("git rev-parse HEAD")
            version = log.read()
            print("---------------------------------------" + version)
            dir_name = ""
            war_name = project_name.split(".")[0]
            dir_name = war_name
            if war_name == 'authCenter':
                dir_name = 'authcenter'
            path = EMP_BASIC_PATH_GIT + "\\" + dir_name
            print("组成的路径为：" + path)
            basic_path = path
            if project_name != "js.zip":
                os.chdir(path)
                pop_cmd = "mvn clean package -DskipTests -Ptest"
                os_popen = os.popen(pop_cmd)
                os_popen_log = os_popen.read()
                print(os_popen_log)
                if "BUILD FAILURE" in os_popen_log:
                    raise RuntimeError(dir_name + "构建失败，请查看log")
                basic_path = path + "\\target"
            print("--------------------------------------mvn打包完毕---------------------------------------")
            from_path = basic_path + "\\" + project_name
            print("编译后的war文件路径为：" + from_path)
            TO = "/home/zdtest/release/" + project_name
            commend_cmd = ""
            check_string = ""
            if project_name == "zd.jar" or project_name == "serverService.jar":
                TO = "/home/zdtest/release/" + project_name
                commend_cmd = "cd /home/zdtest/release/;./jar_test.sh release " + project_name + ";source /etc/profile;./jar_test.sh start " + project_name + ";./jar_test.sh status " + project_name
                check_string = "is running. Pid is"
            print("from :" + from_path)
            print("to :" + TO)
            ssh = SSH(ip="xxxx")
            ssh.login(username="zdtest", password="Zd@")
            ssh.upload_file(local_path=from_path, linux_path=TO)
            ssh.close_ssh()
            print("--------------------------------------war包上传完毕---------------------------------------")
            print("svn 开始准备")
            if os.path.exists(EMP_BASIC_PATH + "\\员工APP"):
                print("版本文件存在，进行update升级")
                os.chdir(EMP_BASIC_PATH + "\\员工APP")
                cleanup = os.popen("F:\\xxx\Apache-Subversion-1.10.2\\bin\\svn.exe cleanup")
                print(cleanup.read())
                update = os.popen("F:\\xxxx\Apache-Subversion-1.10.2\\bin\\svn.exe update")
                print(update.read())
            else:
                print("版本文件不存在，进行下载")
                os.chdir(EMP_BASIC_PATH)
                getSVN = os.popen(
                    "F:\\tool_liusq\Apache-Subversion-1.10.2\\bin\\svn.exe checkout svn://1xxx/root/document/发布文档/员工APP "
                    "--username liusq --password liusq")
                print(getSVN.read())
            print("---------------------------------------------备份库拉取完毕---------------------------------------------")
            if project_name == "zd.jar" or project_name == "serverService.jar":
                print("----------需要启动为jar包-----")
                ssh_client = SSHClient(ip="10.xxx", username="root", password="@user")
                log = ssh_client.exe_command(commend_cmd)
                log_result = log[len(log) - 1]
                if check_string not in log_result:
                    ssh_client.ssh_client_close()
                    raise RuntimeError(project_name + "的服务未启动成功")
                ssh_client.ssh_client_close()
            elif project_name in WAR_NAME:
                command_lists = command.get(project_name)
                command_port = command_lists[0]
                command_site = command_lists[1]
                command_release = "cd /home/zdtest/release/;source /etc/profile;./releaseAutotest.sh " + command_port + " " + command_site + ";./restartAutotest.sh " + command_port + " " + command_site
                ssh_client = SSHClient(ip="10.1", username="root", password="@user")
                log_war = ssh_client.exe_command(command_release)
                ssh_client.ssh_client_close()
            print("--------------------------------------服务启动完毕---------------------------------------")
            print("需要修改的名称是：" + war_name)
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            style = xlwt.XFStyle()
            style.alignment = alignment
            style.font.height = 215
            workbook = xlrd.open_workbook(VERSION, formatting_info=True)
            sheet = workbook.sheet_by_name("user Information")
            nrows = sheet.nrows  # 获取excel表格的行数
            rows = sheet.ncols  # 获取excel表格的列数
            workbook_now = copy(workbook)
            sheet_now = workbook_now.get_sheet("user Information")
            for row in range(nrows):
                print(sheet.cell(row, 0).value)
                if sheet.cell(row, 0).value == war_name:
                    sheet_now.write(row, 1, version, style)
                    sheet_now.write(row, 2, branch_name_new, style)
            workbook_now.save(VERSION)
        except Exception as e:
            err_num += 1
            print("================================截获到异常为：" + e.__str__())
    if err_num != 0:
        raise RuntimeError("有" + err_num.__str__() + "个站，谢谢~")
