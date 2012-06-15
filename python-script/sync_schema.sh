#!/bin/bash

echo "rsync -av root@10.3.202.149:/root/solrWorkSpace/schema/DEV/schema.xml ."
rsync -av root@10.3.202.149:/root/solrWorkSpace/schema/DEV/schema.xml .
