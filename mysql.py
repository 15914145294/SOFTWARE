"""
centos:
mysql忘记root密码解决

1.修改MySQL的登录设置： 
# vim /etc/my.cnf 
在[mysqld]的段中加上一句：skip-grant-tables 
例如： 
[mysqld] 
datadir=/var/lib/mysql 
socket=/var/lib/mysql/mysql.sock 
skip-grant-tables

2.重启mysql
service mysqld restart

3.登录mysql
mysql

4.修改root用户密码：
UPDATE user SET authentication_string = password ('new-password') WHERE User = 'root' ; 

5.编辑my.cnf文件删掉skip-grant-tables 这一行

6.重启mysql


为用户授权并用于远程连接
GRANT ALL PRIVILEGES ON *.* TO 'tny'@'localhost' IDENTIFIED BY 'Test1234!!' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'tny'@'%'      IDENTIFIED BY 'Test1234!!' WITH GRANT OPTION;
"""
