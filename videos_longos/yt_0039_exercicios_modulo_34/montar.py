"""yt_0039 · monta o preview v1: concatena media_<LOTE>/videos/cena/540p15/<LOTE>.mp4 na ordem do cena.LOTES (sem recodificar) em
renders/v1/yt_0039_preview_v1_540p15.mp4 e grava renders/v1/inicio_lotes.json (início de cada lote no MP4, s)."""
import json
import subprocess
from pathlib import Path

import av

import os as _os
RV = _os.environ.get("RODADA", "v2")
AQUI = Path(__file__).resolve().parent
ORDEM = ["PH", "PA", "PE1", "PE2", "PE3", "PE4", "PE5", "PE6", "PS"]
OUT = AQUI / "renders" / RV
OUT.mkdir(parents=True, exist_ok=True)
lst, ini, t = [], {}, 0.0
for c in ORDEM:
    f = AQUI / f"media_{c}" / "videos" / "cena" / "540p15" / f"{c}.mp4"
    assert f.exists(), f
    with av.open(str(f)) as k:
        s = k.streams.video[0]
        d = float(s.frames / 15) if s.frames else float(k.duration / 1e6)
    ini[c] = round(t, 4)
    t += d
    lst.append(f"file '{f.as_posix()}'")
(OUT / "lista.txt").write_text("\n".join(lst) + "\n", encoding="utf-8")
dst = OUT / f"yt_0039_preview_{RV}_540p15.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(OUT / "lista.txt"), "-c", "copy", "-an", str(dst)], check=True)
(OUT / "inicio_lotes.json").write_text(json.dumps(ini, indent=1), encoding="utf-8")
print(dst, f"{int(t // 60)}:{t % 60:05.2f}", ini)
