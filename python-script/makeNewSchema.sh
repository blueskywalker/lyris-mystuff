#!/bin/bash

function newSchema
{
ed - schema.xml << EOF
/Lyris_TYPE
+,/Lyris_TYPE/-d
-
. r schema_snapit.xml
w
q
EOF
}


function getExist
{
ed - schema.xml << EOF
/Lyris_TYPE
+,/Lyris_TYPE/w $1
q
EOF

}

getExist $*
