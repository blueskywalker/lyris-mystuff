

BASE="${HOME}/Source/"
CWD=`pwd`

function fileSize()
{
	local size

	size=0
	if [ $# -gt 0 ]
	then
#		echo "/bin/ls -l $1 | awk '{print \$5}'"	
		size=$(/bin/ls -l $1 | awk '{print $5}')	
	fi
	return ${size}
}

function getBranch
{
	echo $4
}

function getRest
{
	shift 4	
	local rest
		
	for s in $*
	do
		rest=${rest}/${s}
	done

	echo ${rest}
}

function merge()
{
	PATCH=/tmp/$3.patch

#	echo "diff -b -B -u $1/$3 $2/$3 > ${PATCH}"
	diff -b -B -u $1/$3 $2/$3 > ${PATCH}	
   
    local size
    fileSize ${PATCH}
	size=$?
	local OPT
	if [ ${size} -gt 0 ]; then  
#		echo cd $1
		cd $1
		echo
		cat ${PATCH}
		OPT="n"
		read -p "Do you want to overwrite[o]/merge[m]/meld[v]/No[n] ? [n]" OPT 

		if [ ${OPT} == "o" ]; then
			echo "patch < ${PATCH}"
			patch < ${PATCH}
		elif [ ${OPT} == "m" ]; then
			echo "patch --merge < ${PATCH}"
			patch --merge < ${PATCH}
		elif [ ${OPT} == "v" ]; then
			meld $1/$3 $2/$3
		else
			echo "NO CHANGE"
		fi
    else
		echo "NO CHANGE"
	fi
}
	

if [ $# -lt 2 ]
then
	echo "syncSource.sh branch file"
    exit
fi

SPLIT=$(echo ${CWD} | tr '/' ' ' )

getBranch ${SPLIT}
REST=`getRest ${SPLIT}`

PREFIX=${BASE}$1${REST}

shift 

for f in  $*
do
#	echo "cp -pf ${CWD}/$f  ${PREFIX}/"
#	cp -pf ${CWD}/$f  ${PREFIX}/
	printf "[%40s]===============================   " $f
	merge ${PREFIX} ${CWD} $f
done
