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
   MYSQL_HOST=10.3.213.144
fi

source baseScript.sh

function main()
{
    cleanup
    retrieveSchema $*
    echo python ${PYTHONPRG} schema.xml $(cat ${UPDATEXML}) 
    python ${PYTHONPRG} schema.xml $(cat ${UPDATEXML}) 
    modifySchema
    copyToDeploy QA
}


main $*

