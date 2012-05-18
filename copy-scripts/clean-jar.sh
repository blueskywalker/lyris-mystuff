#!/bin/bash

echo $0
ROOTDIR=$(dirname $0)

source ${ROOTDIR}/config.sh

export SSHPASS=devdev

echo ${TARGETDIRS}

clean-jar()
{
echo sshpass -e ssh ${USER}@${TARGET} find $1 -name '*.jar' -exec rm -f {} \\\;
sshpass -e ssh ${USER}@${TARGET} find $1 -name '*.jar' -exec rm -f {} \\\;
}

for f in ${DESTBASE}/{analytics,common,core,event}
do
    clean-jar $f
done
