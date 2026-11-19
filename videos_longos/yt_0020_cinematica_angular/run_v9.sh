#!/bin/bash
# yt_0020 v8 (2.ª rodada de correções): hélice mais escura + setas do PH mais grossas; KH4 do T4; auditoria do PE1 (regra ω₀t); depois QA completo.
cd "$(dirname "$0")"
for L in PH PT4 PS; do ./render_v3.sh $L > log_v9run_$L.txt 2>&1 & done
./auditar.sh PE1 > /dev/null 2>&1 &
wait
echo "ondas concluídas $(date +%H:%M:%S)" > log_v9.txt
./run_fim_v8.sh
