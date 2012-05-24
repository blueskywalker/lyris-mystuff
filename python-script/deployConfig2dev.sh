#!/bin/bash

if [ $# -lt 1 ]
then
   echo "It need configuration file to be copied"
   exit
fi

SEARCH_CLUSTER=$(echo 10.3.202.{165,166,167})
END_CORE=6
SOURCE=$1
COPY='rsync -av'


echo ${SEARCH_CLUSTER}


for m in ${SEARCH_CLUSTER}
do
    for c in $(seq 0 ${END_CORE})
    do
    	echo ${COPY} ${SOURCE}  root@${m}:/opt/lyris/searchServer/solrMulticore/core${c}/conf/${SOURCE}
#    	${COPY} ${SOURCE}  root@${m}:/opt/lyris/searchServer/solrMulticore/core${c}/conf/${SOURCE}
    done
done

