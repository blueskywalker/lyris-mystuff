#!/bin/bash

if [ ! $# -eq 1 ]
then
    echo "It needs master's ip or hostname."
    exit
fi

BASEDIR=$(dirname $0)
HOST=$1
END_CORE=6
SLAVE_CONFIG=/tmp/solrcore.properties

function main 
{
echo "rm -rf ${SLAVE_CONFIG}"
rm -rf ${SLAVE_CONFIG}

echo touch ${SLAVE_CONFIG}
touch ${SLAVE_CONFIG}

echo "enable.master=false" >> ${SLAVE_CONFIG}
echo "enable.slave=true" >> ${SLAVE_CONFIG}
echo "master.host=${HOST}" >> ${SLAVE_CONFIG}

for c in $(seq 0 ${END_CORE})
do
   echo "cp -fp ${SLAVE_CONFIG} ${BASEDIR}/solrMulticore/core${c}/conf"
   cp -fp ${SLAVE_CONFIG} ${BASEDIR}/solrMulticore/core${c}/conf
done

}

main 
