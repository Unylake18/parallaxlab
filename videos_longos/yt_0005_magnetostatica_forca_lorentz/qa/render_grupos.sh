#!/bin/bash
# uso: render_grupos.sh LARGURA,ALTURA FPS PASTA_SAIDA PARALELO   (renderiza os grupos de seções em processos independentes)
RES=$1; FPS=$2; OUT=$3; P=${4:-2}
U=videos_longos/yt_0005_magnetostatica_forca_lorentz
mkdir -p $U/$OUT
GR=("pre,D,K" "Kend,rest0,A,C,B,Bx,E,F,F2" "G,H,I,J")
roda() {
  i=$1; segs=$2
  CRF=14 SEGS=$segs PYTHONIOENCODING=utf-8 uv run --no-sync python -m manim -r $RES --fps $FPS --disable_caching \
    --media_dir $U/$OUT/m$i -o g$i.mp4 $U/cena.py YT0005MagnetostaticaM1 > $U/$OUT/g$i.log 2>&1
  echo "grupo $i ($segs): saiu $?" >> $U/$OUT/status.txt
}
export -f roda; export U OUT RES FPS
rm -f $U/$OUT/status.txt
for i in 0 1 2; do echo "$i|${GR[$i]}"; done | xargs -P $P -I{} bash -c 'IFS="|" read i s <<< "{}"; roda $i "$s"'
echo FIM >> $U/$OUT/status.txt
