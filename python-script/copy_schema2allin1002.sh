#!/bin/bash

CORE_END=6
HOST=10.3.9.18
USER=root
DEST=/opt/lyris/searchServer/solrMulticore/core

for NO in $(seq 0 ${CORE_END})
do
    echo "scp schema.xml ${USER}@${HOST}:${DEST}/core${NO}/conf"
    scp schema.xml ${USER}@${HOST}:${DEST}${NO}/conf
done
