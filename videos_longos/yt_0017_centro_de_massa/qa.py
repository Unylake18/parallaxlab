"""QA do vídeo inteiro (handoff v4 §5) → renders/qa.txt: alinhamento Manim × Three.js, cacos, degradê e cor por token, física (os números
de conferência de todos os lotes), duração por âncora (narração v3.1 × cena), PAUSAS (trechos ≥ 4 s, com âncora), FUNDO (quadros com mais
de 40% de pixels abaixo de luminância 0,03, fora do A1/EN1), EN2 ⊕ × MÉDIA, transição hook → T1 sem salto de brilho, auditorias por lote.
uso: python qa.py [exceções.txt]"""
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
PY = sys.executable
LOTES = ["PH", "P1", "P2", "P3", "P4", "P5"]
NOMES = {"PH": "hook + abertura", "P1": "T1", "P2": "T2", "P3": "T3", "P4": "T4", "P5": "E1, E2, síntese, encerramento"}
EXC = [l.rstrip() for l in open(sys.argv[1], encoding="utf-8")] if len(sys.argv) > 1 else []
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
logs = {c: (U / f"log_{c}.txt").read_text(encoding="utf-8", errors="replace") for c in LOTES}
run = lambda *a: subprocess.run([PY, *a], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=U).stdout
video = lambda c: U / f"media_{c}/videos/cena/540p15/{c}.mp4"
anc = {c: [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", logs[c])] for c in LOTES}
W, H = 960, 540
px = lambda p: np.array([(p[0] + 8) / 16 * W, (4.5 - p[1]) / 9 * H])

out = ["# yt_0017 · vídeo inteiro (handoff v4 de 2026-10-29) · QA do preview 960×540 / 15 fps", ""]
out += ["## Alinhamento Manim × Three.js (quadro a quadro)"]
for c in LOTES:
    if (U / f"qa_overlay_{c}.json").exists():
        out += [f"{c}: " + l for l in run("qa_3d.py", c).splitlines() if l.startswith("[qa]")]
out += ["", "## Cacos da granada (VOLUME DOS CACOS e CENTROIDE × FÍSICA)"]
out += [l for l in run("qa_cacos.py", "PH", "P2", "P3", "P5").splitlines() if l.startswith("[cacos]")] + [""]

out += ["## EN2 ⊕ × MÉDIA (⊕ da cena × média ponderada das posições dos blocos, todo quadro)"]
ov = json.loads((U / "qa_overlay_P5.json").read_text(encoding="utf-8")).get("en2", {})
d = [float(np.linalg.norm(px(v["cm"]) - px(v["media"]))) for v in ov.values()]
out += [f"{len(d)} quadros; pior {max(d):.4f} px" if d else "sem registro"]
ovb = json.loads((U / "qa_overlay_P3.json").read_text(encoding="utf-8")).get("blocos", {})
db = [float(np.linalg.norm(px(v["cm"]) - px(v["media"]))) for v in ovb.values()]
out += [f"T3-6 (blocos): {len(db)} quadros; pior {max(db):.4f} px" if db else ""]
ovc = json.loads((U / "qa_overlay_P5.json").read_text(encoding="utf-8")).get("canoa", {})
xs = [v["x_cm"][0] for v in ovc.values()]
out += [f"E2 (canoa): X_cm do sistema em {len(xs)} quadros: {min(xs):.6f} a {max(xs):.6f} m (fixo em 2 m)" if xs else "", ""]

out += ["## Degradê e cor por token (G15, G12)"]
for c in LOTES:
    out += [f"{c}: " + l for l in logs[c].splitlines() if l.startswith("[degrade]") or l.startswith("[cor] tokens")]
out += [""]

out += ["## Física (números de conferência)"]
out += (U / "renders/qa_fisico_lote1.txt").read_text(encoding="utf-8").strip().splitlines()
from fractions import Fraction as Fr
out += [f"T3-6: K antes = ½·2·6² = {0.5 * 2 * 36:g} J; V_cm = 2·6/3 = {2 * 6 / 3:g} m/s; ½·3·4² = {0.5 * 3 * 16:g} J; K_rel = {36 - 24} J",
        f"T4-4: X = (L³/3)/(L²/2) = 2L/3 = {2 * 2 / 3:.4f} m com L = 2 m",
        f"E1 (três triângulos): Y = (¼·⅙ + ¼·½ + ¼·½)/¾ = {(Fr(1, 4) * Fr(1, 6) + Fr(1, 4) * Fr(1, 2) * 2) / Fr(3, 4)} m",
        f"E1 (massa negativa): Y = (1·½ − ¼·⅚)/(1 − ¼) = {(Fr(1, 2) - Fr(1, 4) * Fr(5, 6)) / Fr(3, 4)} m (o mesmo ponto); desafio: ⊕ a "
        f"{abs(-Fr(1, 4) * Fr(1, 4) / Fr(3, 4))} m do centro (não falado)",
        f"E2: X_cm = (75·3 + 150·1,5)/225 = {(75 * 3 + 150 * 1.5) / 225:g} m; 75(−3 + Δx_c) + 150 Δx_c = 0 → Δx_c = {75 * 3 / 225:g} m; Δx_r = {-3 + 1:g} m; "
        f"falta {1.0 - 0.8:.2f} m",
        f"EN2: V_cm = (2·2 + 1·(−2))/3 = {(2 * 2 - 2) / 3:.4f} m/s = v_f", ""]

out += ["## Duração por âncora (narração v3.1: palavras e duração a 2,7 palavras/s × duração real da cena)",
        "âncora   palavras   fala (s)   cena (s)   diferença"]
tf = tc = 0.0
for c in LOTES:
    for (a, t0), (_, t1) in zip(anc[c], anc[c][1:]):
        f = ANC[a]["dur"]
        tf += f
        tc += t1 - t0
        out.append(f"{a:8s} {ANC[a]['palavras']:8d} {f:10.2f} {t1 - t0:10.2f} {t1 - t0 - f:+10.2f}")
out += [f"{'total':8s} {'':8s} {tf:10.2f} {tc:10.2f} {tc - tf:+10.2f}", ""]
out += ["## Tempo: âncoras em que a cena passa da fala (> 0,2 s)"]
t_ = [f"{c}: {l}" for c in LOTES for l in logs[c].splitlines() if l.startswith("[tempo]") and "total" not in l]
out += (t_ or ["nenhuma"]) + [""]

out += ["## PAUSAS (trechos parados ≥ 4 s, com âncora)"]
out += [l for l in run("parados.py", *LOTES).splitlines() if l.startswith("[pausa]")] + [""]

out += ["## FUNDO (quadros com > 40% dos pixels abaixo de luminância 0,03; fora do A1/EN1)"]
ruins, medias = [], {}
for c in LOTES:
    isenta = [(t0, t1) for (a, t0), (_, t1) in zip(anc[c], anc[c][1:]) if a in ("A1", "EN1")]
    cont = av.open(str(video(c)))
    for i, fr in enumerate(cont.decode(video=0)):
        a_ = np.asarray(fr.to_image().resize((240, 135)), dtype=np.float32) / 255
        Y = 0.2126 * a_[..., 0] + 0.7152 * a_[..., 1] + 0.0722 * a_[..., 2]
        medias.setdefault(c, []).append(float(Y.mean()))
        t = i / 15
        if (Y < 0.03).mean() > 0.4 and not any(t0 <= t < t1 for t0, t1 in isenta):
            ruins.append((c, t))
    cont.close()
out += [f"{len(ruins)} quadro(s) fora" + ("" if not ruins else ": " + ", ".join(f"{c} {t:.1f}s" for c, t in ruins[:40]))]
m_ph, m_p1 = medias["PH"], medias["P1"]
out += [f"transição A4 → T1-1 (luminância média): último quadro do A4 {m_ph[-6]:.3f} · meio do crossfade (o céu do laboratório) "
        f"{float(np.mean(np.asarray(__import__('PIL.Image', fromlist=['Image']).open(U / 'fundo_lab.png').convert('L').resize((240, 135)))) / 255):.3f} · "
        f"primeiro quadro do T1-1 {m_p1[5]:.3f}", ""]

out += ["## Auditorias por lote (TEXTO PEQUENO, FORA DA MARGEM, SOBREPOSICAO, SEM PALCO, TEXTO SOBRE OBJETO, OBJETO FORA DA MARGEM, PAR FORA DE SINCRONIA, "
        "DEGRADÊ FORA DO ⊕, COR POR TOKEN)"]
for c in LOTES:
    au = [l for l in logs[c].splitlines() if l.startswith("[audit]")]
    tipos = Counter(re.sub(r"^\[audit\]\s+[0-9.]+s ", "", l).split(" '")[0].split(" mola")[0].split(" corpo")[0].split(" Line")[0].split(" VM")[0].strip() for l in au)
    out.append(f"{c} ({NOMES[c]}): {len(au)} linha(s)" + (" · " + ", ".join(f"{k} ×{v}" for k, v in tipos.items()) if au else " · zero"))
    out += au
out += ["", "### Exceções justificadas (o resto zerou)"] + EXC
out += ["", "## Capítulos"] + (U / "renders/capitulos_completo.txt").read_text(encoding="utf-8").strip().splitlines()
(U / "renders/qa.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
