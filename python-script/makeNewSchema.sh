#!/bin/bash

ed - schema.xml << EOF
/Lyris_TYPE
+,/Lyris_TYPE/-d
-
.r newType.xml
w
q
EOF
