#!/bin/bash

SQL_SCRIPT=getSchema.sql
UPDATEXML=update.list.txt
PYTHONPRG=makeFields.py

function  cleanup()
{
    echo rm ${UPDATEXML}
    rm -f ${UPDATEXML}
    touch ${UPDATEXML}
}


function getSchemaFromDB()
{
    local USER=root
    local PASSWD=g0lyr1s
    local DBNAME=$1
    local OUTNAME=${DBNAME}_schema.xml
    local TMP_OUT=/tmp/${OUTNAME}

    echo "mysql -h${MYSQL_HOST} -u${USER} -p${PASSWD}  ${DBNAME} < ${SQL_SCRIPT} > ${TMP_OUT}"
    mysql -h${MYSQL_HOST} -u${USER} -p${PASSWD}  ${DBNAME} < ${SQL_SCRIPT} > ${TMP_OUT}
    echo "cat ${TMP_OUT} | sed -e '1d' -e 's/\\n/ /g' -e 's/\\t/ /g' | xmllint -format - > ${OUTNAME}"
    cat ${TMP_OUT} | sed -e '1d' -e 's/\\n/ /g' -e 's/\\t/ /g' | xmllint -format - > ${OUTNAME}
    echo ${OUTNAME} >> ${UPDATEXML}
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
	DST = shift

    echo "scp schema.xml root@10.3.202.149:/root/qa-backend/schema/${DST}"
    scp schema.xml root@10.3.202.149:/root/qa-backend/schema/${DST}
}

