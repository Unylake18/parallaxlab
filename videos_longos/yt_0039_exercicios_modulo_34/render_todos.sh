#!/bin/bash
cd "$(dirname "$0")"
export RODADA=final
( ./render.sh PH; ./render.sh PA; ./render.sh PE1 ) > rt_a.txt 2>&1 &
( ./render.sh PE2; ./render3d.sh PE3 ) > rt_b.txt 2>&1 &
( ./render.sh PE4; ./render.sh PE5 ) > rt_c.txt 2>&1 &
( ./render3d.sh PE6; ./render.sh PS ) > rt_d.txt 2>&1 &
wait
echo feito > render_todos.ok
