#!/bin/bash

SEARCH_CLUSTER=10.3.9.18
END_CORE=6
SOURCES="solrconfig.xml solrcore.properties"
COPY='rsync -av'


echo ${SEARCH_CLUSTER}


for m in ${SEARCH_CLUSTER}
do
    for c in $(seq 0 ${END_CORE})
    do
	for src in ${SOURCES}
	do
	    echo ${COPY} ${src}  root@${m}:/opt/lyris/searchServer/solrMulticore/core${c}/conf/${SOURCE}
	    ${COPY} ${src}  root@${m}:/opt/lyris/searchServer/solrMulticore/core${c}/conf/${SOURCE}
	done
    done
done

