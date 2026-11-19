"""QA de legibilidade (v4 §3b): contraste WCAG real de cada marcação sobre o 3D, medido no quadro composto final.

Para cada elemento, "núcleo" = pixels do traço/texto; "entorno" = anel de 1–4 px em volta (o que o olho vê junto:
halo, chip ou o próprio sólido). Contraste = (L_claro + 0,05) / (L_escuro + 0,05) entre a mediana do núcleo e o percentil
mais desfavorável do entorno (90 % se o núcleo é claro). Limiar: texto ≥ 4,5:1; linha ≥ 3:1.
  - linhas do 3D: máscara G (render3d.js --mascara), componente por componente;
  - textos/rótulos do Manim: alfa da camada (remotion/public/manim_png) com cor clara, por grupo;
  - textos do Remotion: caixas do log de QA (render com qa = true); núcleo = pixels claros da caixa.
Quadros de teste obrigatórios + amostra a cada 1 s nos trechos em que há marcação sobre o 3D.
Uso (raiz): uv run python videos/vid_0030_anel_guardanapo/qa/contraste.py [pasta_quadros]
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, binary_erosion, label

UNIT = Path(__file__).resolve().parents[1]
FPS = 15
QUADROS = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "renders" / "quadros_todos_v5"
TESTE = {"C01 trio com régua": 27.0, "C02 corte com h e triângulo": 40.0, "C03 coroa com r_int/r_ext/R": 60.0,
         "C04 disco da esfera": 90.0, "C06 anel com régua": 148.0}
N = len(list(QUADROS.glob("f*.png")))
AMOSTRA = sorted(set([round(t * FPS) for t in TESTE.values()] + list(range(0, N, FPS))))
SOBRE_3D = ("rot_aux", "C04_raio", "C06_paredes")                 # grupos do Manim desenhados sobre o 3D
REMOTION = ("regua", "rot_trio", "tag_hook", "C04_cont", "C06_cont", "C07_cont")


def lum(rgb):
    c = rgb.astype(float) / 255
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def razao(nucleo, entorno):
    if nucleo.size < 4 or entorno.size < 4:
        return None
    a = float(np.median(nucleo))
    b = float(np.percentile(entorno, 75 if a >= np.median(entorno) else 25))     # fundo local, lado desfavorável
    hi, lo = max(a, b), min(a, b)
    return round((hi + 0.05) / (lo + 0.05), 2)


log = (UNIT / "remotion" / "render_remotion_v5.log").read_text(encoding="utf-8", errors="replace")
REM = {}
for m in re.finditer(r"QA\|(\d+)\|(\[.*?\])(?:\x1b|\s*$)", log, re.M):
    REM.setdefault(int(m.group(1)), json.loads(m.group(2)))
CM = json.loads((UNIT / "media_preview" / "caixas_CenaMat.json").read_text(encoding="utf-8"))["quadros"]

TL = json.loads((UNIT / "timeline.json").read_text(encoding="utf-8"))


def K(nome, t):
    ch = TL["chaves"][nome]
    if t <= ch[0]["t"]:
        return ch[0]["v"]
    for a, b in zip(ch, ch[1:]):
        if t <= b["t"]:
            u = (t - a["t"]) / max(b["t"] - a["t"], 1e-9)
            u = u if b.get("ease") == "linear" else u * u * (3 - 2 * u)
            return a["v"] + (b["v"] - a["v"]) * u
    return ch[-1]["v"]


DISCO = lambda r: np.hypot(*np.mgrid[-r:r + 1, -r:r + 1]) <= r
res = defaultdict(list)                      # elemento → [(t, razão, tipo)]
for f in AMOSTRA:
    comp = np.asarray(Image.open(QUADROS / f"f{f:05d}.png").convert("RGB"))
    L = lum(comp)
    mk = np.asarray(Image.open(UNIT / "mask3d_540x960" / f"f{f:05d}.png").convert("RGB"))
    sol, aux = mk[..., 0] > 127, mk[..., 1] > 127
    perto = binary_dilation(sol, structure=DISCO(6))
    # (1) linhas do 3D sobre o sólido — só com as famílias de linha paradas (fora de entrada/saída)
    vis = [K("tri_vis", f / FPS) * min(1, K("tri_R", f / FPS)), K("fatia_vis", f / FPS), K("cav_tri", f / FPS) * K("cav_vis", f / FPS)]
    nucleo_aux = binary_erosion(aux, structure=np.ones((2, 2))) if all(v < 0.02 or v > 0.97 for v in vis) else np.zeros_like(aux)
    lab, n = label(nucleo_aux)
    for i in range(1, n + 1):
        c = lab == i
        if c.sum() < 25 or not (c & perto).any():
            continue
        anel = binary_dilation(c, structure=DISCO(4)) & ~binary_dilation(aux, structure=DISCO(2))
        r = razao(L[c], L[anel])
        if r is not None:
            ys, xs = np.where(c)
            cor = tuple(int(v) for v in np.median(comp[c], axis=0))
            res[f"linha 3D cor {cor}"].append((round(f / FPS, 2), r, "linha", int(xs.mean()), int(ys.mean())))
    # (2) textos do Manim sobre o 3D
    mp = np.asarray(Image.open(UNIT / "remotion" / "public" / "manim_png" / f"f{f:05d}.png"))
    alfa, claro, tinta = mp[..., 3] > 230, lum(mp[..., :3]) > 0.2, mp[..., 3] > 40
    caixas_m = [c for c in CM.get(str(f), []) if c[0].startswith(SOBRE_3D) and c[5] >= 0.7]
    # caixas que contêm outra do mesmo grupo são o chip/fundo do rótulo, não o texto: ficam fora
    texto_m = [c for c in caixas_m if not any(d is not c and d[0] == c[0] and c[1] <= d[1] and c[2] <= d[2] and d[3] <= c[3]
                                               and d[4] <= c[4] for d in caixas_m)]
    for g, x0, y0, x1, y1, op, *_ in texto_m:
        if False:
            continue
        X0, Y0, X1, Y1 = int(max(0, x0)), int(max(0, y0)), int(min(540, x1 + 1)), int(min(960, y1 + 1))
        if X1 - X0 < 3 or Y1 - Y0 < 3 or not perto[Y0:Y1, X0:X1].any():
            continue
        cx = np.zeros_like(alfa)
        cx[Y0:Y1, X0:X1] = True
        c = cx & alfa & claro
        # entorno: anel de 1 a 3 px FORA de toda a tinta (sem a borda suavizada do glifo nem as letras vizinhas)
        anel = binary_dilation(c, structure=DISCO(2)) & ~binary_dilation(cx & tinta & claro, structure=DISCO(1))
        r = razao(L[c], L[anel])
        if r is not None:
            res[f"Manim {g}"].append((round(f / FPS, 2), r, "texto", (X0 + X1) // 2, (Y0 + Y1) // 2))
    # (3) textos/réguas do Remotion
    for g, x0, y0, x1, y1, op, txt in REM.get(f, []):
        if not g.startswith(REMOTION) or op < 0.7 or g.endswith("_chamada"):
            continue
        X0, Y0, X1, Y1 = int(max(0, x0)), int(max(0, y0)), int(min(540, x1 + 1)), int(min(960, y1 + 1))
        if X1 - X0 < 2 or Y1 - Y0 < 2:
            continue
        X0, Y0, X1, Y1 = max(0, X0 - 4), max(0, Y0 - 4), min(540, X1 + 4), min(960, Y1 + 4)   # linhas finas
        sub = L[Y0:Y1, X0:X1]
        lim_t = (sub.max() + np.median(sub)) / 2                    # meio caminho entre traço e fundo
        cx = np.zeros_like(sol)
        cx[Y0:Y1, X0:X1] = sub >= max(lim_t, np.percentile(sub, 60))
        tinta = np.zeros_like(sol)
        tinta[Y0:Y1, X0:X1] = sub >= (np.median(sub) + lim_t) / 2
        anel = binary_dilation(cx, structure=DISCO(3)) & ~binary_dilation(tinta, structure=DISCO(1))
        r = razao(L[cx], L[anel])
        tipo = "linha" if (X1 - X0) < 8 or (Y1 - Y0) < 8 else "texto"
        if r is not None:
            res[f"Remotion {g} {txt[:18]}".strip()].append((round(f / FPS, 2), r, tipo, (X0 + X1) // 2, (Y0 + Y1) // 2))

lim = {"texto": 4.5, "linha": 3.0}
tabela, falhas = {}, []
for el, lst in sorted(res.items()):
    pior = min(lst, key=lambda x: x[1])
    tabela[el] = {"medidas": len(lst), "pior": pior[1], "t_pior": pior[0], "tipo": pior[2], "xy": pior[3:5],
                  "mediana": round(float(np.median([x[1] for x in lst])), 2)}
    if pior[1] < lim[pior[2]]:
        falhas.append({"elemento": el, **tabela[el]})
teste = {}
for nome, t in TESTE.items():
    f = round(t * FPS)
    teste[nome] = {el: min(x[1] for x in lst if round(x[0] * FPS) == f) for el, lst in res.items()
                   if any(round(x[0] * FPS) == f for x in lst)}
out = {"quadros_avaliados": len(AMOSTRA), "limiar": lim, "abaixo_do_limiar": falhas, "quadros_de_teste": teste,
       "por_elemento": tabela}
(UNIT / "qa" / "contraste_v5.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"abaixo_do_limiar": falhas, "quadros_de_teste": teste}, ensure_ascii=False, indent=1))
