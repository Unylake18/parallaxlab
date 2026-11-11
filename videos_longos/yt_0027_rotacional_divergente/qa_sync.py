"""yt_0027 final §5.4: relatório de sincronização → qa/sync.txt (e qa/sync.json).
Para cada uma das 43 âncoras: início da imagem no vídeo × 1ª palavra na voz (alinhamento forçado). Para cada gatilho (gat/em): atraso do evento visual
em relação ao alvo (LEAD 0,09 s antes da palavra). Meta: atraso ≤ 0,2 s. Também lista [estouro], [gatilho-sem-frase] e a deriva de cada lote.
uso: python qa_sync.py [prefixo_log=log_]   (log_ = preview 540p; log1080_ = render final)"""
import json
import re
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
PRE = sys.argv[1] if len(sys.argv) > 1 else "log_"
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
ordem, anc = A["ordem"], A["ancoras"]
LOTES = ["PHA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PF", "PB7", "PS"]
lin, js, ruins = [], {"ancoras": {}, "gatilhos": []}, []
abs0 = 0.0
for L in LOTES:
    log = (U / f"{PRE}{L}.txt").read_text(encoding="utf-8", errors="replace")
    an = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log)]
    tot = float(re.search(r"\[tempo\] total ([0-9.]+)s", log).group(1))
    for aid, tl in an:
        t_img = abs0 + tl
        t_pal = anc[aid]["ini"] + anc[aid]["t"][0]             # 1ª palavra na voz
        d = t_img - (t_pal - 0.15)                             # 0 = imagem 0,15 s antes da palavra (LEAD do handoff)
        js["ancoras"][aid] = {"imagem_s": round(t_img, 3), "palavra_s": round(t_pal, 3), "atraso_s": round(d, 3)}
        if d > 0.2:
            ruins.append(f"âncora {aid}: imagem {d:+.2f}s depois do previsto")
    for m in re.finditer(r"\[gatilho\] (\S+)\s+([0-9.]+)s \(alvo\s+([0-9.]+)s, atraso ([+-][0-9.]+)s\) (.*)", log):
        g = {"lote": L, "ancora": m.group(1), "atraso_s": float(m.group(4)), "frase": m.group(5).strip()}
        js["gatilhos"].append(g)
        if g["atraso_s"] > 0.2:
            ruins.append(f"gatilho {g['ancora']} «{g['frase']}»: {g['atraso_s']:+.2f}s")
    for m in re.finditer(r"\[(estouro|gatilho-sem-frase|deriva)\] (.*)", log):
        lin.append(f"[{m.group(1)}] {L}: {m.group(2).strip()}")
    abs0 += tot
lin.insert(0, f"vídeo: {abs0:.2f}s · voz: {anc[ordem[-1]]['fim'] - 1.0:.2f}s (+1 s de cauda no CTA)")
g = js["gatilhos"]
lin += ["", f"âncoras: {len(js['ancoras'])}/43 · maior atraso da imagem {max(v['atraso_s'] for v in js['ancoras'].values()):+.2f}s · "
        f"menor {min(v['atraso_s'] for v in js['ancoras'].values()):+.2f}s",
        f"gatilhos: {len(g)} · maior atraso {max(x['atraso_s'] for x in g):+.2f}s · acima de 0,2 s: {sum(x['atraso_s'] > 0.2 for x in g)}", ""]
lin.append("| âncora | imagem (s) | 1ª palavra (s) | imagem − (palavra − 0,15) | gatilhos | maior atraso |")
lin.append("|---|---:|---:|---:|---:|---:|")
for a in ordem:
    v = js["ancoras"].get(a)
    ga = [x["atraso_s"] for x in g if x["ancora"] == a]
    lin.append(f"| {a} | {v['imagem_s']:.2f} | {v['palavra_s']:.2f} | {v['atraso_s']:+.2f} | {len(ga)} | {max(ga) if ga else 0:+.2f} |" if v else f"| {a} | — | | | | |")
lin += ["", "acima de 0,2 s:"] + (ruins or ["nenhum"])
(U / "qa").mkdir(exist_ok=True)
(U / "qa" / ("sync.txt" if PRE == "log_" else "sync_1080.txt")).write_text("\n".join(lin) + "\n", encoding="utf-8")
(U / "qa" / ("sync.json" if PRE == "log_" else "sync_1080.json")).write_text(json.dumps(js, ensure_ascii=False, indent=1), encoding="utf-8")
print("\n".join(lin[:6] + lin[-12:]))
