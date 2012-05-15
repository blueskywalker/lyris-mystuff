#!/bin/bash

SEARCH_CLUSTER='10.3.202.165 10.3.202.166 10.3.202.167'
END_CORE=6
SOURCE=schema.xml
COPY='rsync -av'

for m in ${SEARCH_CLUSTER}
do
    for c in $(seq 0 ${END_CORE})
    do
	echo ""
    	echo ${COPY} ${SOURCE}  root@${m}:/opt/lyris/searchServer/solrMulticore/core${c}/conf/${SOURCE}
    	${COPY} ${SOURCE}  root@${m}:/opt/lyris/searchServer/solrMulticore/core${c}/conf/${SOURCE}
    done
done

