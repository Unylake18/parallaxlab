#!/bin/bash
# renderiza lotes do v6 em paralelo (com auditorias): ./render_lote_v6.sh PA PT1 ... → log_<Classe>.txt
cd "$(dirname "$0")"
for c in "$@"; do ( AUDITORIA=1 ANCORAS=1 ./render.sh $c > /dev/null ) & done
wait
for c in "$@"; do echo "== $c: $(grep -c 'Traceback' log_$c.txt) erros; $(grep '\[tempo\] total' log_$c.txt)"; done
