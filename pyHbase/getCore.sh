
REPOSITORY=${HOME}/.m2/repository
NOCORE=3

if [ ! $# -eq 2 ]
then
	echo "It needs OrgId SubOrgId"
	exit
fi

#echo java -classpath ${REPOSITORY}/org/apache/hadoop/hadoop-core/0.20.2-cdh3u3/hadoop-core-0.20.2-cdh3u3.jar:${REPOSITORY}/com/lyris/search/1.0.9-SNAPSHOT/search-1.0.9-SNAPSHOT.jar  com.lyris.search.util.SearchMulticoreHash 3 lyris uptilt

java -classpath ${REPOSITORY}/org/apache/hadoop/hadoop-core/0.20.2-cdh3u3/hadoop-core-0.20.2-cdh3u3.jar:${REPOSITORY}/com/lyris/search/1.0.9-SNAPSHOT/search-1.0.9-SNAPSHOT.jar  com.lyris.search.util.SearchMulticoreHash ${NOCORE} $1 $2

