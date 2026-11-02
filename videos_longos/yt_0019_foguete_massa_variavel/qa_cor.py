"""yt_0019 v5 — auditoria de cor (handoff v5 §3.6) → renders/cor.txt.
Para cada 10º quadro do preview: pixels "claros" = V > 140 (HSV); "coloridos" = claros com S > 90. Por capítulo: % colorido médio, saturação mediana dos claros
com S > 40 ("tinta"), quadros com < 10% colorido. Também os 10 quadros com menos cor do vídeo e a comparação com o v4 (se existir).
uso: python qa_cor.py [rodada=v5] [rodada_anterior=v4]"""
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v8"
ANT = sys.argv[2] if len(sys.argv) > 2 else "v7"
CAPS = [("Abertura", 0, 81.6), ("T1", 81.6, 175.7), ("T2", 175.7, 389.6), ("T3", 389.6, 586.5), ("T4", 586.5, 664.6), ("E1", 664.6, 792.6), ("E2", 792.6, 952.1), ("E3", 952.1, 1080.6), ("Síntese", 1080.6, 1133)]   # v9 (voz: 18,9 min)


def hsv(rgb):
    x = rgb.astype(np.float32) / 255.0
    mx, mn = x.max(axis=2), x.min(axis=2)
    d = mx - mn
    s = np.where(mx > 0, d / np.maximum(mx, 1e-6), 0.0)
    return mx * 255.0, s * 255.0


def medir(arq):
    c = av.open(str(arq))
    fps = float(c.streams.video[0].average_rate)
    out = []
    for i, fr in enumerate(c.decode(c.streams.video[0])):
        if i % 10:
            continue
        img = np.asarray(fr.to_image().resize((480, 270)))
        v, s = hsv(img)
        v[:30, :] = 0          # título e canto
        v[:, -110:][:30] = 0   # logo
        claro = v > 140
        n = claro.sum()
        colorido = (claro & (s > 90)).sum()
        tinta = s[claro & (s > 40)]
        out.append((i / fps, 100.0 * colorido / max(1, n), float(np.median(tinta)) if tinta.size > 50 else 0.0))
    return out


def resumo(medidas):
    tab = []
    for nome, a, b in CAPS:
        m = [x for x in medidas if a <= x[0] < b]
        if not m:
            tab.append((nome, 0, 0, 0, 0))
            continue
        tab.append((nome, np.mean([x[1] for x in m]), np.median([x[2] for x in m if x[2] > 0] or [0]), sum(1 for x in m if x[1] < 10), len(m)))
    return tab


atual = medir(U / "renders" / f"preview_yt0019_{R}_960x540.mp4")
ant_arq = U / "renders" / f"preview_yt0019_{ANT}_960x540.mp4"
ant = medir(ant_arq) if ant_arq.exists() else None
ta, tb = resumo(atual), (resumo(ant) if ant else None)
L = [f"# yt_0019 — auditoria de cor ({R}); colorido = claro (V>140) com S>90; tinta = claros com S>40", ""]
L.append("| capítulo | % colorido " + ANT + " | % colorido " + R + " | sat. mediana " + ANT + " | sat. mediana " + R + " | quadros < 10% (" + R + ") |")
L.append("|---|---|---|---|---|---|")
for k, (nome, pc, sat, pobres, n) in enumerate(ta):
    pa = f"{tb[k][1]:.0f}%" if tb else "—"
    sa = f"{tb[k][2]:.0f}" if tb else "—"
    L.append(f"| {nome} | {pa} | {pc:.0f}% | {sa} | {sat:.0f} | {pobres}/{n} ({100 * pobres / max(1, n):.0f}%) |")
tot = np.mean([x[1] for x in atual])
L += ["", f"- vídeo inteiro: {tot:.1f}% colorido; saturação mediana da tinta {np.median([x[2] for x in atual if x[2] > 0]):.0f}",
      f"- metas: ≥ 30% colorido em todo capítulo · saturação mediana ≥ 120 · quadros < 10% colorido ≤ 5% do capítulo"]
falha = [nome for nome, pc, sat, pobres, n in ta if pc < 30 or sat < 120 or pobres > 0.05 * max(1, n)]
L.append("- capítulos que não atingiram todas as metas: " + (", ".join(falha) if falha else "nenhum"))
L += ["", "## 10 quadros com menos cor"]
for t, pc, sat in sorted(atual, key=lambda x: x[1])[:10]:
    L.append(f"- {int(t // 60)}:{int(t % 60):02d} — {pc:.1f}% colorido")
(U / "renders" / "cor.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
