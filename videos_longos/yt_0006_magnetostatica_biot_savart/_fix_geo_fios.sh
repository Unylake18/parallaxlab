#!/bin/bash
cd /c/Users/Pichau/PycharmProjects/manim-fisica
D=videos_longos/yt_0006_magnetostatica_biot_savart; R=$D/renders
for g in "g1 geometria" "g2 infinito,fios"; do set -- $g; rm -rf $R/$1; mkdir -p $R/$1; cp -r $R/f1/Tex $R/$1/Tex; bash $D/_grupo.sh $1 $2 >> $R/fix.log 2>&1; done
echo FIX_DONE >> $R/fix.log
