"""yt_0014 — costuras entre os grupos do render final: quanto cada grupo começa atrasado no master em relação à cena.

O relógio do Manim é exato nas seções puladas e quantizado em quadros nas renderizadas; cada grupo sai com 1–2 quadros a mais e o atraso
se acumula nas emendas. Aqui medimos: atraso_k = (quadros dos grupos anteriores)/30 − (instante exato do início do grupo k).
montar_sync.py insere esse atraso (incremental) como silêncio curto na pausa de fala antes da primeira âncora do grupo,
e desloca a legenda e os capítulos junto. Uso: uv run --no-sync python costuras.py   (depois montar_sync.py e montar_final.py)
"""
import json
import re
from pathlib import Path

import av

P = Path(__file__).resolve().parent
GRUPOS = [("hook", None), ("c04", "C04-1"), ("c07", "C07-1"), ("c09", "C09-1"), ("c12", "C12-1")]   # (primeira seção, primeira âncora)
tempo = {}
for lin in (P / "tempo_exato.log").read_text(encoding="utf-8", errors="ignore").replace("\r", "\n").splitlines():
    m = re.match(r"\[tempo\] (\w+):\s+([0-9.]+) s", lin.strip())
    if m:
        tempo[m.group(1)] = float(m.group(2))
tempo.setdefault("hook", 0.0)
saida, quadros = [], 0
for i, (sec, aid) in enumerate(GRUPOS, 1):
    atraso = quadros / 30 - tempo[sec]
    if aid:
        saida.append({"grupo": i, "secao": sec, "ancora": aid, "inicio": tempo[sec], "quadros_antes": quadros, "atraso": round(atraso, 4)})
    with av.open(str(P / "media_final" / "videos" / "cena" / "1080p30" / f"grupo{i}.mp4")) as c:
        quadros += sum(1 for _ in c.demux(c.streams.video[0]) if _.dts is not None)
(P / "final").mkdir(exist_ok=True)
(P / "final" / "costuras.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
for s in saida:
    print(s)
print("quadros totais", quadros)
