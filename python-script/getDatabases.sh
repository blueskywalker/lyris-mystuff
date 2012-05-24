#!/bin/bash

HOST=10.3.203.143
USER=root
PASSWD=g0lyr1s
DBNAME=$1
SQL_SCRIPT=getSchema.sql
TMP_OUT=/tmp/${DBNAME}_schema.xml

DBS=$(echo "show databases;" | mysql -h${HOST} -u${USER} -p${PASSWD} | sed -e '1d')

for db in ${DBS}
do
	echo DB- ${db}
done

