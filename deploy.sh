#!/bin/bash
#/home/release
homepath=$(pwd)
nowTime=$(date "+%F_%T")
nowDay=$(date "+%F")
deployroot=/data/jar
logroot=/data/logs
#环境选择 dev test uat online

environment=$0
# #*删除第一个_及其左边的字符串  ##*删除最后一个_及其左边的字符串
# %.*删除最后一个.及其右边的字符串   %%.*删除第一个.及其右边的字符
# eg:environment = jar_uat.sh
environment=${environment##*_} # uat.sh
environment=${environment%%.*} # uat

#JVM="-server -Xms128m -Xmx128m -XX:PermSize=32M -XX:MaxNewSize=64m -XX:MaxPermSize=64m -Djava.awt.headless=true -XX:+CMSClassUnloadingEnabled -XX:+CMSPermGenSweepingEnabled"
JVM=
APP_NAME=
APP_PATH=
APP_LOG=
CONFIG_URI=

##########环境对应的配置中心地址，可根据实际情况调整此处配置
if [ $environment == 'dev' ]; then
        CONFIG_URI=http://
elif [ $environment == 'test' ]; then
        CONFIG_URI=http://
#elif [ $environment == 'uat' ]; then
#       CONFIG_URI=http://
elif [ $environment == 'online' ]; then
        CONFIG_URI=
fi

echo "当前启动环境[${environment}]  配置中心[${CONFIG_URI}]"



#使用说明，用来提示输入参数 sh jar_uat.sh start   serverName
usage(){
    echo "Usage: sh $0 [start|stop|restart|status|release] [{packageName}.jar]"
    exit 1
}

#检测jar包是否存在,不存在返回0，存在返回1   
is_exist_appfile(){
  if [ ! -f $homepath/$APP_NAME ];then

        echo "$APP_PATH/$APP_NAME文件不存在"
        return 0
  else
    return 1
  fi
}

#检查程序进程是否在运行,不存在返回0，存在返回1
is_exist_proc(){
  
  #查询包含app的进程|排除grep命令|排除当前脚本运行的进程
  pid=`ps -ef|grep $APP_NAME|grep -v grep|grep -v $0|awk '{print $2}' `
  echo "ps -ef|grep $APP_NAME|grep -v grep|grep -v $0|awk '{print $2}' "
  
  #如果不存在返回0，存在返回1     
  if [ -z "${pid}" ]; then
   return 0
  else
    return 1
  fi
}

#启动方法
start(){
  is_exist_proc
  if [ $? -eq "1" ]; then
    echo "${APP_NAME} is already running. pid=${pid} ."
	release
	#jar启动默认读取命令对应路径下的配置，所以要先切到部署路径再执行命令
	if [ $? -eq "1" ];then
		doit
	else
		echo "bakup $APP_PATH/$APP_NAME $APP_PATH/$APP_NAME.$nowTime faild!"
	fi
  else
	echo "${APP_NAME} is not running ."
  fi
}


doit(){
cd $APP_PATH
	#java $JVM -jar $APP_PATH/$APP_NAME &
	#set -x 
	echo "java $JVM -Dspring.profiles.active=${environment} -Dspring.cloud.config.uri="${CONFIG_URI}" -jar $APP_PATH/$APP_NAME >/dev/null 2>&1 &"
	java $JVM -Dspring.profiles.active=${environment} -Dspring.cloud.config.uri="${CONFIG_URI}" -jar $APP_PATH/$APP_NAME >/dev/null 2>&1 &
	#set +x
	#java -jar $APP_PATH/$APP_NAME &
	cd $homepath
	echo "tail -f $APP_LOG"
}

#停止方法
stop(){
  is_exist_proc
  if [ $? -eq "1" ]; then
    kill -9 $pid
        echo "${APP_NAME} is stop SUCCESS."
  else
    echo "WARN ${APP_NAME} is not running"
  fi  
}

#输出运行状态
status(){
  is_exist_proc
  if [ $? -eq "1" ]; then
    echo "${APP_NAME} is running. Pid is ${pid}"
  else
    echo "WARN ${APP_NAME} is NOT running."
  fi
}

#重启
restart(){
  stop
  start
}
release(){
        stop 
        # remove jar
        mkdir -p $APP_PATH/bakup
		# /data/jar/outService/outService.jar  -->/data/jar/outService/bakup/outService.date
        cp $APP_PATH/$APP_NAME $APP_PATH/bakup/$APP_NAME.$nowTime
        rm -rf $APP_PATH/$APP_NAME
        echo "bakup $APP_PATH/$APP_NAME $APP_PATH/$APP_NAME.$nowTime SUCCESS"

        sleep 1


        cp $homepath/$APP_NAME $APP_PATH/
        echo "copy $homepath/$APP_NAME  TO $APP_PATH/ SUCCESS"
        echo "release $APP_NAME SUCCESS"
		return 1
}


actionType=$1
serverName=$2

#set -x
# is not null
if [ $actionType ] && [ $serverName ]; then

        APP_NAME=$serverName
        APP_CONTENT=${serverName%%.*} # outService
        APP_PATH=$deployroot/$APP_CONTENT # /data/jar/outService
        APP_LOG=$logroot/$APP_CONTENT/$APP_CONTENT"_"info.log
        JVM="-server -Xms128m -Xmx512m"

        echo "${APP_PATH}.jar"

        #是否存在应用包文件
        is_exist_appfile
        if [ $? -eq "1" ]; then
                #根据输入参数，选择执行对应方法，不输入则执行使用说明
                case "$actionType" in
                "start")
                        start
                        ;;
                "stop")
                        stop
                        ;;
                "status")
                        status
                        ;;
                "restart")
                        restart
                        ;;
                "release")
                        release
                        ;;
                *)
                        usage
                        ;;
                esac
        else
                echo "${APP_NAME} is NOT exist."
        fi

else
        usage
fi
#set +x
