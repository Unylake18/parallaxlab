"""yt_0028 (copiado do yt_0027): emenda as seções do preview na ordem do vídeo SEM reencodar (remux dos pacotes H.264, PyAV; as seções saem do Manim com os mesmos
parâmetros). Cada seção já começa e termina no papel vazio (com a linha 1 do canto), então o corte entre seções é limpo.
Saídas em renders/: preview_yt0027_<rodada>_960x540.mp4; quadros_<rodada>.json (quadro
absoluto do início de cada âncora); capitulos_<rodada>_sem_b7.txt; duracoes_estimadas.json ganha a duração de cada âncora no render.
uso: python montar_preview.py [rodada]"""
import json
import re
import sys
from pathlib import Path

import av

U = Path(__file__).resolve().parent
RODADA = sys.argv[1] if len(sys.argv) > 1 else "final"
M = lambda c: U / f"media_{c}/videos/cena/540p15/{c}.mp4"
CAP = {"PH": "O QUADRADINHO QUE DEFORMA", "PB1": "CHEGAR PERTO", "PB2": "QUANDO O LIMITE NÃO EXISTE", "PB3": "CONTINUIDADE", "PB4": "DERIVADA PARCIAL",
       "PB5": "O ENGANO", "PB6": "A TABELA", "PB7": "QUATRO NÚMEROS, QUATRO MEDIDAS", "PS": "RESUMO"}
BASE = ["PH", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PS"]


def emenda(lotes, saida):
    out = av.open(str(saida), "w")
    so = None
    off, quadros, caps = 0, {}, []
    for nome in lotes:
        c = av.open(str(M(nome)))
        s = c.streams.video[0]
        if so is None:
            so = out.add_stream_from_template(s)
        tb = s.time_base
        d = int(round(1 / (15 * tb)))                       # duração de um quadro na base de tempo
        n = s.frames
        for p in c.demux(s):
            if p.dts is None:
                continue
            p.pts += off
            p.dts += off
            p.stream = so
            out.mux(p)
        log = (U / f"log_{nome}.txt").read_text(encoding="utf-8", errors="replace")
        q0 = off // d
        caps.append((CAP[nome], q0 / 15))
        for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log):
            quadros[m.group(1)] = q0 + round(float(m.group(2)) * 15)
        off += n * d
        c.close()
    out.close()
    return off // d, quadros, caps


res = {}
(U / "renders" / RODADA).mkdir(parents=True, exist_ok=True)
saida = U / "renders" / RODADA / f"yt_0028_preview_{RODADA}_540p15.mp4"
nq, quadros, caps = emenda(BASE, saida)
(U / "renders" / RODADA / f"quadros_{RODADA}.json").write_text(json.dumps(quadros, indent=0), encoding="utf-8")
(U / "renders" / RODADA / f"capitulos_{RODADA}.txt").write_text("\n".join(f"{int(t) // 60}:{int(t) % 60:02d} {c}" for c, t in caps) + "\n", encoding="utf-8")
res = {"saida": str(saida), "quadros": nq, "duracao_s": round(nq / 15, 1), "min": round(nq / 15 / 60, 2)}
ordem = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ordem"]
de = json.loads((U / "duracoes_estimadas.json").read_text(encoding="utf-8"))
ini = [quadros[a] for a in ordem]
for a, i0, i1 in zip(ordem, ini, ini[1:] + [nq]):
    de["ancoras"][a]["dur_render_s"] = round((i1 - i0) / 15, 2)
de["render_" + RODADA] = {"total_s": res["duracao_s"], "nota": "dur_render_s = do início da âncora ao início da seguinte no preview (inclui as saídas de seção); estimado, sem voz"}
(U / "duracoes_estimadas.json").write_text(json.dumps(de, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=1))
