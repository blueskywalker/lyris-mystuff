#!/bin/bash
ROOTDIR=$(dirname $0)

source ${ROOTDIR}/config.sh

MODULE=analytics/analytics-mta

MODULELIST=${ANALYTICS_MTALIST}

copy-jar ${MODULE}

