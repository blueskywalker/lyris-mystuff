#!/bin/bash
ROOTDIR=$(dirname $0)

source ${ROOTDIR}/config.sh

MODULELIST=${THIRDPARTYLIST}
copy-file-list thirdparty



