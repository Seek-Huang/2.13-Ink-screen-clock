#!/bin/bash
f_name=main.py
dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
logdir=${dir%/*}
pid=`ps -ef |grep $dir/$f_name | grep -v grep |awk '{print $2}'`
for id in $pid
do
    kill -9 $id
done
nohup /usr/bin/python3 -u $dir/$f_name > $logdir/log/info.log 2>&1 &