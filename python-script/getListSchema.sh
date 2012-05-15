#!/bin/bash

if [ $# -lt "1" ]
then
    echo "It needs database name."
    exit
fi

HOST=10.3.203.143
USER=root
PASSWD=g0lyr1s
DBNAME=$1
SQL_SCRIPT=getSchema.sql
TMP_OUT=/tmp/${DBNAME}_schema.xml

mysql -h${HOST} -u${USER} -p${PASSWD}  ${DBNAME} < ${SQL_SCRIPT} > ${TMP_OUT}

cat ${TMP_OUT} | sed -e '1d' -e 's/\\n/\n/g' -e 's/\\t/\t/g' > ${DBNAME}_schema.xml
