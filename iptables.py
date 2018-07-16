"""

centos:
  server端telnet port 如是通的而client telnet时不通，

则应将需要的端口进行暴露
 iptables -I INPUT -p tcp --dport 6379 -j ACCEPT
 service iptables save # 保存暴露的端口
 service iptables restart # 重启iptables
 service iptables status # 查看iptables

"""
