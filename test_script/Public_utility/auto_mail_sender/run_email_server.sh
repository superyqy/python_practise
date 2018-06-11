#! /bin/sh
pid=`ps -ef |grep "python ./mail_sender.py"|grep -v grep |awk '{print $2}'`
if [ "a$pid" != "a" ]; then
  #kill -9 $pid
  echo 'this process already running'
  exit 1
fi

nohup python ./mail_sender.py > mail_server.log 2>&1 &