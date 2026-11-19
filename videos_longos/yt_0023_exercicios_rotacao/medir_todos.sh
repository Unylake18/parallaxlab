#!/bin/bash
# passe a seco (SYNC=medir) de todos os lotes, 2 em paralelo → medicao_<lote>.json (depois das âncoras reais da voz)
cd "$(dirname "$0")"
rm -f medir_todos.done
printf '%s\n' PE4 PE2 PE3 PE1a PE1b PH PS | xargs -P 2 -I{} bash -c './medir.sh {} > medir_{}.out 2>&1; echo {} >> medir_todos.done'
echo FIM >> medir_todos.done
