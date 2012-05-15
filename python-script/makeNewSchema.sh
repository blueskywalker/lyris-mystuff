#!/bin/bash

ed - schema.xml << EOF
/Lyris_TYPE
+,/Lyris_TYPE/-d
-
. r schema_snapit.xml
w
q
EOF
