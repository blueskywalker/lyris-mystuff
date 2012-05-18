#!/bin/bash

if [ $# -lt 1 ]
then
    echo "It needs database names."
    exit
fi

MYSQL=.mysql_set

if [ -f ${MYSQL} ]
then
    source ${MYSQL}
fi

if [ -z $MYSQL_HOST ]
then
   MYSQL_HOST=10.3.203.143
fi

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
    cat ${TMP_OUT} | sed -e '1d' -e 's/\\n/\n/g' -e 's/\\t/\t/g' > ${OUTNAME}
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
    echo scp schema.xml root@10.3.202.149:/root/qa-backend/schema
    scp schema.xml root@10.3.202.149:/root/qa-backend/schema
}

function main()
{
    cleanup
    retrieveSchema $*
    echo python ${PYTHONPRG} schema.xml $(cat ${UPDATEXML}) 
    python ${PYTHONPRG} schema.xml $(cat ${UPDATEXML}) 
    modifySchema
#    copyToDeploy
}


main $*

