

if [ $# -lt 4 ]
then
	echo "HbaseMasterGrep.sh orgid subOrgid column pattern output[option]"
	exit
fi

TABLENAME="$1_$2_master_lyris"
COLUMN=$3
PATTERN=$4
OUTPUT=$5

echo ./HbaseColumnGrep.py ${TABLENAME} ${COLUMN} ${PATTERN} ${OUTPUT}
./HbaseColumnGrep.py ${TABLENAME} ${COLUMN} ${PATTERN} ${OUTPUT}
