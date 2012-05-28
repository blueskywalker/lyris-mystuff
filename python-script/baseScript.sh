#!/bin/bash

SQL_SCHEMA=getSchema.sql
SQL_DBS=getMySQLDBnames.sql
UPDATE_LIST=update.list.txt
MAKE_SCHEMA=makeFields.py
GET_HBASE=getMasterTable.py
HBASE_TABLE=/tmp/hbase_tables.txt
MYSQL_DBNAME=/tmp/mysqldbnames.txt
INDEX_LIST=/tmp/index.list.txt

function  cleanup()
{
    echo rm ${UPDATE_LIST}
    rm -f ${UPDATE_LIST}
    touch ${UPDATE_LIST}
}

function getTableTobeIndexed()
{
	mysqlQuery system  ${SQL_DBS} ${MYSQL_DBNAME}
	./filterOut.pl ${MYSQL_DBNAME} ${HBASE_TABLE} > ${INDEX_LIST}
}

function getHBaseTable()
{
	echo "executing ./${GET_HBASE} $1"
	./${GET_HBASE} $1 >  ${HBASE_TABLE}
}

function makeSchemaXml()
{
    echo "${MAKE_SCHEMA} schema.xml $(cat ${UPDATE_LIST})"
    ${MAKE_SCHEMA} schema.xml $(cat ${UPDATE_LIST}) 
}

function mysqlQuery()
{
    local USER=root
    local PASSWD=g0lyr1s
    local DBNAME=$1 
	local SQLQUERY=$2
	local OUTPUT=$3

    echo "mysql -h${MYSQL_HOST} -u${USER} -p${PASSWD}  ${DBNAME} < ${SQLQUERY} > ${OUTPUT}"
    mysql -h${MYSQL_HOST} -u${USER} -p${PASSWD}  ${DBNAME} < ${SQLQUERY} > ${OUTPUT}
}


function getSchemaFromDB()
{
    local DBNAME=$1
    local OUTNAME=${DBNAME}_schema.xml
    local TMP_OUT=/tmp/${OUTNAME}

    echo "mysqlQuery ${DBNAME} ${SQL_SCHEMA} ${TMP_OUT}"
    mysqlQuery ${DBNAME} ${SQL_SCHEMA} ${TMP_OUT}

    echo "cat ${TMP_OUT} | sed -e '1d' -e 's/\\n/ /g' -e 's/\\t/ /g' | xmllint -format - > ${OUTNAME}"
    cat ${TMP_OUT} | sed -e '1d' -e 's/\\n/ /g' -e 's/\\t/ /g' | xmllint -format - > ${OUTNAME}
    echo ${OUTNAME} >> ${UPDATE_LIST}
}

function retrieveSchema()
{
    for db in $*
    do
        getSchemaFromDB ${db}
    done
}

function modifySchema()
{
ed - schema.xml << EOF
/Lyris_TYPE
+,/Lyris_TYPE/-d
-
. r schema_snapit.xml
w
q
EOF

echo "schema.xml is modified"
}

function copyToDeploy()
{
	DST=$1

    echo "scp schema.xml root@10.3.202.149:/root/qa-backend/schema/${DST}"
    scp schema.xml root@10.3.202.149:/root/qa-backend/schema/${DST}
}


