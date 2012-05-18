#!/bin/bash

ROOTDIR=$(dirname $0)
source ${ROOTDIR}/config.sh

MODULE=event/event-extractor

MODULELIST=${EVENT_EXTRACTORLIST}

copy-jar ${MODULE}

