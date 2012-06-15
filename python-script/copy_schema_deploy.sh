#!/bin/bash

PLATFORM=DEV

if [[ $# -ge 1 && $1 ==  "qa" ]]
then
PLATFORM=QA
fi

echo scp schema.xml root@10.3.202.149:/root/solrWorkSpace/schema/${PLATFORM}
scp schema.xml root@10.3.202.149:/root/solrWorkSpace/schema/${PLATFORM}
