#!/bin/bash
cd "$(dirname "$0")"
export RODADA=final
( ./render.sh PH; ./render.sh PA; ./render.sh PE1; ./render.sh PS ) > rg_a.txt 2>&1 &
( ./render.sh PE2; ./render3d.sh PE3 ) > rg_b.txt 2>&1 &
( ./render3d.sh PE4; ./render3d.sh PE5 ) > rg_c.txt 2>&1 &
( ./render3d.sh PE6 ) > rg_d.txt 2>&1 &
wait
echo feito > render_g.ok
