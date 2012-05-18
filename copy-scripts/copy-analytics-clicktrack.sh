#!/bin/bash
ROOTDIR=$(dirname $0)

OOTDIR=/home/jerry/workspace/scripts/copyIndexEnv

source ${ROOTDIR}/config.sh

MODULE=analytics/analytics-clicktrack

MODULELIST=${ANALYTICS_CLICKTRACKLIST}

copy-jar ${MODULE}

