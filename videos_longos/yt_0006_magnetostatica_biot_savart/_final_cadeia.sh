#!/bin/bash
# render final 1080p30: grupos 1–7 em sequência (o 8 é "teste", já pronto). Um processo por vez (RAM).
D=/c/Users/Pichau/PycharmProjects/manim-fisica/videos_longos/yt_0006_magnetostatica_biot_savart
rm -f $D/renders/final/cadeia_done.txt
bash $D/_render_final.sh g1 "abertura,regime,geometria,lei"
bash $D/_render_final.sh g2 "distribuidas,clinica"
bash $D/_render_final.sh g3 "superposicao,metodo"
bash $D/_render_final.sh g4 "trecho"
bash $D/_render_final.sh g5 "infinito,fios"
bash $D/_render_final.sh g6 "espira,algebra_espira"
bash $D/_render_final.sh g7 "centro,distante"
echo OK > $D/renders/final/cadeia_done.txt
