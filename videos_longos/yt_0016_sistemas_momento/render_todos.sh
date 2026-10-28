#!/bin/bash
# renderiza todos os lotes do preview v1 (4 em paralelo) → media_<Lote>/videos/cena/540p15/<Lote>.mp4
cd "$(dirname "$0")"
LOTES=${@:-"PH P7 P8 P9 P10 Q6 Q7 Q8 Q9 PC PS"}
printf "%s\n" $LOTES | xargs -P 4 -I{} ./render.sh {}
for c in $LOTES; do echo "$c: $(grep -c -i 'Traceback' log_$c.txt) erros; $(grep '\[tempo\] total' log_$c.txt)"; done
