#!/usr/bin/env bash

#CORE=$(ls /opt/lyris/core/core-1*.jar)
CORE=$(ls /opt/lyris/trunk/core/target/core-1*.jar)
JAVA=java
MAIN=com.lyris.search.util.SolrIndexDelete


echo ${JAVA} -cp ${CORE} ${MAIN} $*
${JAVA} -cp ${CORE} ${MAIN} $*

