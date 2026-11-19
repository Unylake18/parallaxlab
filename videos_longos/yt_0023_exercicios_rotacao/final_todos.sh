#!/bin/bash
# render final 1080p/30 de todos os lotes, 2 em paralelo (3D + Manim por lote); PH refaz a medição antes (ordem dos eventos do hook mudou)
cd "$(dirname "$0")"
rm -f final_todos.done
job(){ C=$1; [ "$C" = "PH" ] && ./medir.sh PH > medir_PH.out 2>&1; ./render_f1080.sh $C > run_F_$C.txt 2>&1; echo "$C $(date +%H:%M)" >> final_todos.done; }
export -f job
printf '%s\n' PE4 PE2 PE3 PE1a PE1b PH PS | xargs -P 2 -I{} bash -c 'job {}'
echo FIM >> final_todos.done
