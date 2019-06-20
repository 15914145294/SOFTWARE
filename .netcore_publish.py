#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Version : python3.6
@Author  : LiuSQ
@Time    : 2019/3/7 11:38
@Describe: 
"""
import sys
import os
import time

from Util.file_helper import FileHelper

from Tool.FTPTool import FTP, call_remote_bat

basic_date = "D:\Program Files (x86)\Jenkins\workspace"


def del_file(path):
    """
    删除文件夹下全部文件
    :param path:
    """
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)


if __name__ == '__main__':
    args = sys.argv[1:]
    project = args[0]
    where_menu = args[1]
    csp_str = ""
    local_dir = ""
    remote_dir = ""
    print(project)
    time.sleep(5)
    if "LoanCore_publish" in project:
        csp_str = "E:\Zac.LoanCore\Src\Zac.LoanCore.Apis\Zac.LoanCore.Apis.csproj"
        local_dir = "D:\Publish.Test\Zac.LoanCore"
        if where_menu == "Bs.LoanCore":
            remote_dir = "\\New.LoanCore"
        elif where_menu == "Zac.LoanCore":
            remote_dir = "\\Zac.LoanCore"
        cmd = "dotnet publish -c Test23  -o " + local_dir + " " + csp_str + " --source http://nuget.zhongan.com.cn/nuget --source http://nuget-remote.zhongan.com.cn/v3/index.json"
    elif "TradeCore_publish" in project:
        csp_str = "E:\Zac.TradeCore\Src\Zac.TradeCore.Apis\Zac.TradeCore.Apis.csproj"
        local_dir = "D:\IISSites\TradeCore"
        if where_menu == "Bs.TradeCore":
            remote_dir = "\\New.Zac.TradeCore"
        elif where_menu == "Zac.TradeCore":
            remote_dir = "\\Zac.TradeCore"
        cmd = "dotnet publish -c Test23  -o " + local_dir + " " + csp_str + " --source http://nuget.zhongan.com.cn/nuget --source http://nuget-remote.zhongan.com.cn/v3/index.json"
    elif "PayGateway_publish" in project:
        csp_str = "E:\Zac.Plugs.PayGateway\Src\Zac.PayGeteway.Apis\Zac.PayGateway.Apis.csproj"
        local_dir = "D:\publish\paygate"
        remote_dir = "\\Zac.Plugs.PayGateway"
        cmd = "dotnet publish -f netcoreapp2.0  -r win-x86 -c Test23  -o " + local_dir + " " + csp_str + " --source http://nuget.zhongan.com.cn/nuget --source http://nuget-remote.zhongan.com.cn/v3/index.json"
        os.chdir("C:\Program Files\dotnet")
    elif "BasicCore_publish" in project:
        csp_str="E:\Zac.BasicCore\Src\Zac.BasicCore.Apis\Zac.BasicCore.Apis.csproj"
        local_dir = "D:\publish\BasicCore"
        remote_dir = "\\Zac.BasicCore"
        cmd = "dotnet publish -c Release  -o " + local_dir + " " + csp_str + " --source http://nuget.zhongan.com.cn/nuget --source http://nuget-remote.zhongan.com.cn/v3/index.json"
    elif "AdminSites_publish" in project:
        csp_str = "E:\Zac.AdminSites\src\Zac.AdminSites.csproj"
        local_dir = "E:\Zac.AdminSites\src\\bin\Test\\netcoreapp2.2\publish"
        remote_dir = "\\Zac.AdminSites"
        release_cmd = "dotnet restore --source http://nuget.zhongan.com.cn/nuget --source " \
                      "http://nuget-remote.zhongan.com.cn/v3/index.json "+csp_str
        release = os.popen(release_cmd)
        release_log = release.read()
        print(release_log)
        cmd = "\"C:\Program Files (x86)\Microsoft Visual Studio\\2017\Enterprise\MSBuild\\15.0\Bin\MSBuild.exe\"" \
              " /t:Rebuild " \
              "/p:Configuration=release" \
              " /p:environment=test" \
              " /p:PublishProfile=test" \
              " /p:DeployOnBuild=true " \
              "/p:AllowUntrustedCertificate=True " \
              "/p:ExcludeGeneratedDebugSymbol=true " \
              "/p:ExcludeXmlAssemblyFiles=false " \
              "/p:AllowUnsafeBlocks=true " \
              "/p:DebugSymbols=false " \
              "/p:DebugType=none " \
              "/p:SkipExtraFilesOnServer=Trues  "+csp_str
    elif "ApiGateway_publish" in project:
        csp_str = "E:\Zac.ApiGateway.Public\src\Creekdream.ApiGateway\Creekdream.ApiGateway.csproj"
        local_dir = "D:\publish\ApiGateway"
        remote_dir = "\\Zac.ApiGateway.Public"
        cmd = "dotnet publish -c Release  -o " + local_dir + " " + csp_str + " --source http://nuget.xxx.com.cn/nuget --source http://nuget-remote.xxx.com.cn/v3/index.json"
    print(csp_str)
    print(where_menu)
    print("---------------------------环境初始化----------------------------------------")
    del_file(local_dir)
    print("---------------------------开始编译代码--------------------------------------")
    os.chdir("C:\Program Files\dotnet")
    print("执行的命令是：" + cmd)
    begin = os.popen(cmd)
    cmdResult = begin.read()
    print(cmdResult)
    print("---------------------------删除无需上传文件-------------------------------------")
    listdir = os.listdir(local_dir)
    for dir in listdir:
        if (dir.startswith("appsettings") and dir.endswith(".json")) or dir.endswith(".config"):
            print("删除的文件名称为：" + dir)
            os.remove(local_dir + "\\" + dir)
    # print("----------------------------关闭站点---------------------------------------------")
    # call_remote_bat(state="stop", site_name=where_menu)
    # call_remote_bat(state="stop", site_name="Temp.TradeCore")

    print("---------------------------开始上传编译结果-------------------------------------")
    time.sleep(10)
    ftp = FTP("10.xxx")
    ftp.login(username="administrator", password="Za888888!")
    ftp.upload_file_tree_update(local_dir=local_dir, remote_dir=remote_dir,basic_local_dir=local_dir,basic_remote_dir=remote_dir)
    # print("----------------------------启动站点---------------------------------------------")
    # call_remote_bat(state="start", site_name=where_menu)
    # call_remote_bat(state="start", site_name="Temp.TradeCore")

