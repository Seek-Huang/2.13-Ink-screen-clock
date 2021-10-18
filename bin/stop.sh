#!/bin/bash
dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
pid=`ps -ef |grep $dir/main.py | grep -v grep |awk '{print $2}'`
for id in $pid
do
    kill -9 $id
done
