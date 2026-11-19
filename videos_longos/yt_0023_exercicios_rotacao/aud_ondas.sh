#!/bin/bash
cd "$(dirname "$0")"
a() { for L in "$@"; do ./auditar.sh $L > /dev/null 2>&1 & done; wait; }
a PH PE1a PE1b; a PE2 PE3 PE4; a PS
echo fim > aud.done
