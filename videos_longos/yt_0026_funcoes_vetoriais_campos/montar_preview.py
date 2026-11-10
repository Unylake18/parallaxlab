"""yt_0026: emenda as seções do preview na ordem do vídeo SEM reencodar (remux dos pacotes H.264, PyAV; as seções saem do Manim com os mesmos
parâmetros). Cada seção já começa e termina no papel vazio (com a linha 1 do canto), então o corte entre seções é limpo.
Saídas em renders/: preview_yt0026_<rodada>_sem_b7_960x540.mp4 e ..._com_b7_960x540.mp4; quadros_<rodada>_{sem,com}_b7.json (quadro
absoluto do início de cada âncora); capitulos_<rodada>_sem_b7.txt; duracoes_estimadas.json ganha a duração de cada âncora no render.
uso: python montar_preview.py [rodada]"""
import json
import re
import sys
from pathlib import Path

import av

U = Path(__file__).resolve().parent
RODADA = sys.argv[1] if len(sys.argv) > 1 else "v1"
M = lambda c: U / f"media_{c}/videos/cena/540p15/{c}.mp4"
CAP = {"PT": "ABERTURA DO CÁLCULO III", "PAH": "MESMA FÓRMULA, DOIS DESENHOS", "PB1": "QUE FUNÇÃO É ESSA", "PB2": "TRANSFORMAÇÃO", "PB3": "A DOBRA",
       "PB4": "PARA O ESPAÇO", "PB5": "CAMPO VETORIAL", "PB6": "DE VOLTA AO REDEMOINHO", "PB7": "NO ESPAÇO", "PS": "RESUMO"}
BASE = ["PT", "PAH", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6"]


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
for tag, lotes in (("sem_b7", BASE + ["PS"]), ("com_b7", BASE + ["PB7", "PS"])):
    saida = U / "renders" / f"preview_yt0026_{RODADA}_{tag}_960x540.mp4"
    nq, quadros, caps = emenda(lotes, saida)
    (U / "renders" / f"quadros_{RODADA}_{tag}.json").write_text(json.dumps(quadros, indent=0), encoding="utf-8")
    (U / "renders" / f"capitulos_{RODADA}_{tag}.txt").write_text("\n".join(f"{int(t) // 60}:{int(t) % 60:02d} {c}" for c, t in caps) + "\n", encoding="utf-8")
    res[tag] = {"saida": str(saida), "quadros": nq, "duracao_s": round(nq / 15, 1), "min": round(nq / 15 / 60, 2)}
    if tag == "com_b7":
        ordem = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ordem"]
        de = json.loads((U / "duracoes_estimadas.json").read_text(encoding="utf-8"))
        ini = [quadros[a] for a in ordem]
        fins = ini[1:] + [nq]
        for a, i0, i1 in zip(ordem, ini, fins):
            de["ancoras"][a]["dur_render_s"] = round((i1 - i0) / 15, 2)
        de["render_" + RODADA] = {"com_b7_s": res["com_b7"]["duracao_s"], "sem_b7_s": res["sem_b7"]["duracao_s"],
                                  "nota": "dur_render_s = do início da âncora ao início da seguinte no preview com B7 (inclui as saídas de seção)"}
        (U / "duracoes_estimadas.json").write_text(json.dumps(de, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=1))
