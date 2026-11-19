#!/bin/bash
# Espera o render do yt_0005 terminar e então refaz o preview do yt_0006 (trechos pendentes + junção).
# Não mata nenhum processo python (o render do 0005 é de outra unidade).
cd /c/Users/Pichau/PycharmProjects/manim-fisica
D=videos_longos/yt_0006_magnetostatica_biot_savart
LOG=$D/renders/apos_0005.log
echo "[$(date)] aguardando render do yt_0005 (PIDs 17496 24368)" > $LOG

alive() { powershell -NoProfile -c "if (Get-Process -Id $1 -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }"; }
while alive 17496 || alive 24368; do sleep 30; done
echo "[$(date)] yt_0005 terminou; iniciando yt_0006" >> $LOG

for c in c3 c1 c2 c7 c8; do
  rm -rf $D/renders/$c; mkdir -p $D/renders/$c; cp -r $D/renders/v4s/Tex $D/renders/$c/Tex
done
$D/_grupo.sh c3 clinica,superposicao,metodo >> $LOG 2>&1
$D/_grupo.sh c1 abertura,regime,geometria,lei >> $LOG 2>&1
$D/_grupo.sh c2 distribuidas >> $LOG 2>&1
$D/_grupo.sh c7 centro,distante >> $LOG 2>&1
$D/_grupo.sh c8 sintese,fechamento >> $LOG 2>&1

R=$D/renders
V=$R/preview/YT0006BiotSavart_preview.mp4
rm -f $V
uv run python $D/juntar.py $V $(for c in c1 c2 c3 c4 c5 c6 c7 c8; do echo $R/$c/videos/cena/540p15/YT0006BiotSavart.mp4; done) >> $LOG 2>&1
echo "[$(date)] CONCLUIDO: $V" >> $LOG
echo CONCLUIDO > $R/apos_0005_done.txt
