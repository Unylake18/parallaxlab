#!/bin/bash
cd "$(dirname "$0")"
export RODADA=final
( ./render.sh PE2 ) > rp_a.txt 2>&1 &
( ./render3d.sh PE3 ) > rp_b.txt 2>&1 &
( ./render.sh PE4 ) > rp_c.txt 2>&1 &
( ./render3d.sh PE6 ) > rp_d.txt 2>&1 &
wait
echo feito > render_p.ok
