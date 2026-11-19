#!/bin/bash
cd "$(dirname "$0")"
awk '{print $1, $2}' stills_v2.txt | xargs -P 5 -L 1 ./still.sh > stills_v2.log 2>&1
echo FIM >> stills_v2.log
