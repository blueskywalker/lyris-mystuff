#!/bin/bash
ROOTDIR=.
VERSION='1.0.9'
BASEDIR=~/Source/lyris
TARGET='10.3.9.18'
DESTBASE='/opt/lyris'
SYNC='rsync -av'
SSH=ssh
USER=root
RSYNC_PASSWORD=devdev
JARFILE=
MODULELIST=
LISTDIR=${ROOTDIR}/list
CORELIST=$(cat ${LISTDIR}/core-list.txt)
SEARCHLIST=$(cat ${LISTDIR}/search-list.txt)
COMMONLIST=$(cat ${LISTDIR}/common-list.txt)
THIRDPARTYLIST=$(cat ${LISTDIR}/thirdparty-list.txt)
ANALYTICS_CLICKTRACKLIST=$(cat ${LISTDIR}/analytics-clicktrack-list.txt)
ANALYTICS_MTALIST=$(cat ${LISTDIR}/analytics-mta-list.txt)
EVENT_EXTRACTORLIST=$(cat ${LISTDIR}/event-extractor-list.txt)
    
make-jar-file()
{
    JARFILE=${BASEDIR}/${1}/target/$(basename $1)-${VERSION}-SNAPSHOT.jar
}

create-dir() 
{
	echo ${SSH} $1 "mkdir -p $2"
	${SSH} $1 "mkdir -p $2"
}

copy-jar()
{
    local MODULE=$1
    local DESTDIR=${DESTBASE}/${MODULE}

	create-dir ${USER}@${TARGET} ${DESTDIR}

    for i in ${MODULELIST}
    do
        make-jar-file $i
        echo ${SYNC} ${JARFILE} ${USER}@${TARGET}:${DESTDIR}
        ${SYNC} ${JARFILE} ${USER}@${TARGET}:${DESTDIR}
    done
}


copy-jar-lib()
{
    local MODULE=$1
    local DESTDIR=${DESTBASE}/${MODULE}

    copy-jar $1

    echo ${SYNC} ${BASEDIR}/core/target/lib ${USER}@${TARGET}:${DESTDIR}
    ${SYNC} ${BASEDIR}/core/target/lib ${USER}@${TARGET}:${DESTDIR}
}

copy-file-list()
{
    local DESTDIR=${DESTBASE}/$1

    echo ${DESTDIR} 
    for i in ${MODULELIST}
    do
        echo ${SYNC} ${i} ${USER}@${TARGET}:${DESTDIR}
        ${SYNC} ${i} ${USER}@${TARGET}:${DESTDIR}
    done
}
