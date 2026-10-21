#!/bin/bash
# uso: _grupo.sh NOME DE ATE   — render 960×540/15 do trecho que começa no bloco DE e termina no bloco ATE (métodos de cena.py)
# Um processo por vez (memória). Tex copiado da fumaça. Trechos do preview:
#   t1: pergunta circulacao..divergente   _grupo.sh t1 "" divergente
#   t2: _grupo.sh t2 div_formal segundo_termo · t3: fio_finito stokes · t4: validade amp_toroide · t5: comparacao gancho
cd "$(dirname "$0")/../.."
D=videos_longos/yt_0008_magnetostatica_ampere
export UV_PROJECT_ENVIRONMENT=${UV_PROJECT_ENVIRONMENT:-/c/Users/KaioOrtiz/PycharmProjects/manim-fisica/.venv} PYTHONIOENCODING=utf-8
mkdir -p $D/renders/$1
[ -d $D/renders/$1/Tex ] || cp -r $D/renders/fumaca/Tex $D/renders/$1/ 2>/dev/null
DE="$2" ATE="$3" QA_STILLS=1 uv run --no-sync python -m manim -r 960,540 --fps 15 --media_dir $D/renders/$1 --progress_bar none -v WARNING \
  $D/cena.py YT0008Ampere > $D/renders/$1/log.txt 2>&1
echo "$1 exit $?"
