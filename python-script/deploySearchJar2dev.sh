#!/bin/bash

if [ $# -lt 1 ]
then
   echo "It need Search-*.jar file to be copied"
   exit
fi

SEARCH_CLUSTER=$(echo 10.3.202.{165,166,167})
END_CORE=6
SOURCE=$1
COPY='rsync -av'


echo ${SEARCH_CLUSTER}


for m in ${SEARCH_CLUSTER}
do
   	echo ${COPY} ${SOURCE}  root@${m}:/opt/lyris/searchServer/lib/${SOURCE}
done

