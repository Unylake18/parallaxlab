#!/bin/bash
cd "$(dirname "$0")"
rm -f log_fim7.txt
./render_v3.sh PT4 > log_v9run_PT4.txt 2>&1
./run_fim_v8.sh
