#!/bin/bash

PLATFORM=DEV

if [ $# -ge 1 -a $1 == "qa" ]
then
PLATFORM=QA
fi

echo scp schema.xml root@10.3.202.149:/root/qa-backend/schema/${PLATFORM}
scp schema.xml root@10.3.202.149:/root/qa-backend/schema/${PLATFORM}
