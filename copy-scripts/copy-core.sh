#!/bin/bash
ROOTDIR=$(dirname $0)

source ${ROOTDIR}/config.sh

MODULE=core
MODULELIST=${CORELIST}

copy-jar-lib ${MODULE}

