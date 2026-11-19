#!/bin/bash
cd "$(dirname "$0")"
export RODADA=final
( ./render.sh PH; ./render.sh PE1 ) > rf_a.txt 2>&1 &
( ./render.sh PE4; ./render.sh PE5 ) > rf_b.txt 2>&1 &
( ./render3d.sh PE6 ) > rf_c.txt 2>&1 &
wait
echo feito > render_f.ok
