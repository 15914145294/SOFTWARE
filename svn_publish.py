# -*-coding:utf-8-*-
import shutil
import sys
import os
from Util.e_mail import Email
from Config.config import BD_BASIC_PATH, EMAIL_SERVER, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_PERSON, BD_VERSION
from Tool.ReportUtil import ReportUtils

if __name__ == '__main__':
    args = sys.argv[1:]
    isNeedAdd = False
    names = []
    file_name = args[1]
    if "," in args[0]:
        print("有多个需要打包")
        packages = args[0].split(",")
        for name in packages:
            names.append(name)
    else:
        names.append(args[0])
    try:
        print("svn 开始准备")
        if os.path.exists(BD_BASIC_PATH + "\\BD"):
            print("版本文件存在，进行update升级")
            os.chdir(BD_BASIC_PATH + "\\BD")
            cleanup = os.popen("F:\\tool_liusq\Apache-Subversion-1.10.2\\bin\\svn.exe cleanup")
            print(cleanup.read())
            update = os.popen("F:\\tool_liusq\Apache-Subversion-1.10.2\\bin\\svn.exe update")
            print(update.read())
        else:
            print("版本文件不存在，进行下载")
            os.chdir(BD_BASIC_PATH)
            getSVN = os.popen(
                "F:\\tool_liusq\Apache-Subversion-1.10.2\\bin\\svn.exe checkout svn://XXX/root/document/发布文档/BD "
                "--username xxx --password xxx")
            print(getSVN.read())
        for package_name in names:
            warName = package_name
            print("--------------------------------------"+package_name)
            if package_name == "bdOut":
                warName = "bd"
            if os.path.exists(BD_BASIC_PATH + "\BD\\" + file_name + "\测试包\\release\\" + warName + ".jar"):
                isNeedAdd = False
                print("war包原存在")
                os.remove(BD_BASIC_PATH + "\BD\\" + file_name + "\测试包\\release\\" + warName + ".jar")
            else:
                print("war包不存在")
                isNeedAdd = True
            shutil.copyfile(
                BD_BASIC_PATH + "\zac.bd\src\\trunk\\" + package_name + "\\target\\" + warName + ".jar",
                BD_BASIC_PATH + "\BD\\" + file_name + "\测试包\\release\\" + warName + ".jar")
            print("war包复制完成")
            if isNeedAdd:
                print("add 文件")
                os.chdir(BD_BASIC_PATH + "\BD")
                publishPresenceMorePopenos = os.popen(
                    "F:\\tool_liusq\Apache-Subversion-1.10.2\\bin\\svn.exe add " + file_name + "\测试包\\release\\" + warName + ".jar")
                print(publishPresenceMorePopenos.read())
        if os.path.exists(BD_BASIC_PATH + "\BD\\" + file_name + "\测试包\\version.xls"):
            isNeedAddVersion = False
            print("version文件原存在")
            os.remove(BD_BASIC_PATH + "\BD\\" + file_name + "\测试包\\version.xls")
        else:
            print("version.xls不存在")
            isNeedAddVersion = True
        shutil.copyfile(
            BD_VERSION,
            BD_BASIC_PATH + "\BD\\" + file_name + "\测试包\\version.xls")
        print("------------------------------------------------version.xls复制完成--------------------------------------")
        if isNeedAddVersion:
            print("add version.xls文件")
            os.chdir(BD_BASIC_PATH + "\\BD")
            publishPresenceMorePopenos = os.popen(
                "F:\\tool_liusq\Apache-Subversion-1.10.2\\bin\\svn.exe add " + file_name + "\测试包\\version.xls")
            print(publishPresenceMorePopenos.read())
        finish = os.popen("F:\\tool_liusq\Apache-Subversion-1.10.2\\bin\\svn.exe commit -m \"autotest\" ")
        print(finish.read())
    except Exception as e:
        print("报错信息为："+e.__str__())
        utils = ReportUtils()
        report = utils.report_create_fail()
        email = Email(title='【BD】BD发版后数据同步', receiver=EMAIL_PERSON, server=EMAIL_SERVER, sender=EMAIL_SENDER,
                      password=EMAIL_PASSWORD, message=report)
        email.send()
