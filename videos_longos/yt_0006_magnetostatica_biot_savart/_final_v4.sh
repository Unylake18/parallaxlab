#!/bin/bash
# Preview v3: um trecho por vez (dois processos em paralelo estouram a memória), depois junção.
cd /c/Users/Pichau/PycharmProjects/manim-fisica
D=videos_longos/yt_0006_magnetostatica_biot_savart; R=$D/renders; LOG=$R/v4.log
run() { n=$1; secs=$2; rm -rf $R/$n; mkdir -p $R/$n; cp -r $R/f1/Tex $R/$n/Tex; bash $D/_grupo.sh $n "$secs" >> $LOG 2>&1; }
rm -f $R/v4_done.txt; : > $LOG
run m6 espira,algebra_espira
run m8 sintese,fechamento
run m2 distribuidas,clinica
run m4 trecho
run m5 infinito,fios
run m7 centro,distante
run m1 abertura,regime,geometria,lei
run m3 superposicao,metodo
V=$R/preview/YT0006BiotSavart_acabamento_v4.mp4; rm -f $V
uv run python $D/juntar.py $V $(for c in m1 m2 m3 m4 m5 m6 m7 m8; do echo $R/$c/videos/cena/540p15/YT0006BiotSavart.mp4; done) >> $LOG 2>&1
echo "CONCLUIDO $V" >> $LOG; echo OK > $R/v4_done.txt
