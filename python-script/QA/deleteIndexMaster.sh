#!/bin/bash

if [ $# -lt 2 ]
then
	echo "$0 orgId subOrgId"
	exit
fi

./HBaseTableDrop.sh $1 $2
./deleteSolrIndexWith.py $1 $2

