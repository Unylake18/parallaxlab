#!/bin/bash
cd "$(dirname "$0")"
awk 'NF>=2 {print $1, $2}' stills_final.txt | sort -u | xargs -P 5 -L 1 ./still.sh > stills_final.log 2>&1
echo FIM >> stills_final.log
