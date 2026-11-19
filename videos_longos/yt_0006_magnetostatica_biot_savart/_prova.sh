#!/bin/bash
cd /c/Users/Pichau/PycharmProjects/manim-fisica
D=videos_longos/yt_0006_magnetostatica_biot_savart; R=$D/renders; LOG=$R/prova.log
run() { n=$1; secs=$2; rm -rf $R/$n; mkdir -p $R/$n; cp -r $R/f1/Tex $R/$n/Tex; bash $D/_grupo.sh $n "$secs" >> $LOG 2>&1; }
: > $LOG; rm -f $R/prova_done.txt
run p1 abertura,geometria
run p2 espira
echo OK > $R/prova_done.txt
