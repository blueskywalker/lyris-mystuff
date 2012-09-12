#!/bin/bash

HOST=10.3.202.165
BASEDIR=/opt/lyris/searchServer/
TMP=/tmp/solr

echo ssh root@${HOST} "rm -rf ${TMP}; cp -rf ${BASEDIR} ${TMP}"
ssh root@${HOST} "rm -rf ${TMP}; cp -rf ${BASEDIR} ${TMP}"
echo scp -r root@${HOST}:${TMP}  ~/Source/lyris/
scp -r root@${HOST}:${TMP}  ~/Source/lyris/

