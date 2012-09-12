#!/bin/bash

if [ $# -lt 2 ]
then
    echo "$0 orgid suborgid"
    exit
fi

TABLENAME=$1_$2_master_lyris

echo "TableDrop.py ${TABLENAME}"

./TableDrop.py ${TABLENAME}

