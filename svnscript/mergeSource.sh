TRUNK="https://svn-ev.dev.corp.lyris.com/svn/svn/DEV/nexus/trunk"
BASE="${HOME}/Source/"
CWD=`pwd`
SVN_EDITOR=emacs
SPLIT=$(echo ${CWD} | tr '/' ' ' )

parse_svn_branch() {
  parse_svn_url | sed -e 's#^'"$(parse_svn_repository_root)"'##g' | awk -F / '{print "(svn::"$3"/"$4")"}'
}
parse_svn_url() {
  svn info 2>/dev/null | grep -e '^URL*' | sed -e 's#^URL: *\(.*\)#\1#g '
}

parse_svn_repository_root() {
  svn info 2>/dev/null | grep -e '^Repository Root:*' | sed -e 's#^Repository Root: *\(.*\)#\1\/#g '
}

function getBranch
{
	echo $4:$(parse_svn_branch)
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

	
function merge
{
    getBranch ${SPLIT}
    REST=`getRest ${SPLIT}`
    
    echo "svn merge ${OPT}  ${REVISION}${TRUNK}${REST}/$1 $1"
    svn merge ${OPT} ${REVISION}${TRUNK}${REST}/$1 $1
}

function usage
{
cat << EOF
usage : $(basename $0) [option] file
    This script supports merging with trunk.

    OPTIONS:
        -h : this message
        -c : single revision
        -r : revision range with 'start:end'

EOF
}

function parseOpt
{
    
    while getopts "hc:r:" OPTION
    do
        case ${OPTION} in
            h) 
                usage 
                exit 1
                ;;
            c)
                OPT="-c $OPTARG"
                ;;
            r)
                OPT="-r $OPTARG"
                ;;
            ?)  usage
                exit
                ;;
        esac
    done

    shift $(($OPTIND - 1))

    TARGET=$1
    if [ -z $TARGET ]
    then
        usage
        exit
    fi
}

function main
{
    parseOpt $*

    merge  $TARGET
}

main $*
