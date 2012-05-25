#!/bin/bash
ROOTDIR=$(dirname $0)

source ${ROOTDIR}/config.sh

MODULE=search
MODULELIST=${SEARCHLIST}

copy-jar ${MODULE}
#copy-jar-lib ${MODULE}

