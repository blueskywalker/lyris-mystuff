#!/bin/bash

LIST=$(echo "list '^web_behavior'" | hbase shell | grep "^web_behavior")
CWD=$(pwd)

for table in $LIST
do
    CMM=$(echo $table | tr '_' ' ' | awk '{print "/opt/lyris/scripts/indexWebBehavior.sh $3,$4";}') 
    $CMM
done
