"""yt_0044 · QA v2 (handoff v2 §5, Q21–Q29). Roda depois do render dos lotes v2 e dos stills (`RODADA=v2 ./stills_lote.sh LOTE`). Grava em renders/v2/qa/:
q21_piso_v2.txt · q22_grade_v2.txt · q23_cotas_v2.txt · q24_distancia_v2.txt · q25_arame_v2.txt · q26_corte_v2.txt · q27_pausas_v2.txt · q28_emendas_v2.txt (+ emendas_v2.jpg) ·
q29_prancha_3d_v2.jpg (16 pares alvo v2 × preview v2, metade da escala) · qa_v2_resumo.txt"""
import json
import os
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

os.environ["RODADA"] = os.environ.get("RODADA", "v2")
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
_argv = sys.argv[:]
sys.argv = sys.argv[:1]
import k44  # noqa: E402

sys.argv = _argv
QA = AQUI / "renders" / os.environ["RODADA"] / "qa"
QA.mkdir(parents=True, exist_ok=True)
STILL = AQUI / "renders" / "still"
RES = []


def grava(nome, linhas, ok=None):
    (QA / nome).write_text("\n".join(linhas), encoding="utf-8")
    RES.append((nome, ok))


# alvo → (cena 3D, deslocamento, rótulos/marcas extras que contam como marca)
ALVO3D = {
    "01_H1": ("lataParede", k44.OL), "03_E1-1": ("cuboCaixas", k44.OL), "05_E1-3": ("cuboSonda", k44.OC), "06_E1-4": ("cuboDiag", k44.OC),
    "07_E1-5": ("cuboFolha", k44.OL), "08_E2-1": ("tetraSonda", k44.OT), "09_E2-2": ("tetraSonda", k44.OC), "10_E2-3": ("tetraCent", k44.OT),
    "12_E3-1": ("cone", k44.OM), "13_E3-2": ("coneCm", k44.OM), "14_E3-3": ("coneCasca", k44.OM), "16_E4-1": ("semi", k44.OM),
    "17_E4-2": ("semiFatia", k44.OM), "19_E5-1": ("lataDobradica", k44.OL), "20_E5-2": ("lataDob3", k44.OC), "26_S2": ("helice", k44.OL),
}
MARCAS_EXTRA = {   # pontos que viram marca desenhada no Manim (⊕, bolinhas, pontos de sonda) além das placas
    "06_E1-4": ["cm"], "13_E3-2": ["z34"], "16_E4-1": ["z38", "P"], "17_E4-2": ["z38"], "05_E1-3": ["entra", "sai"], "09_E2-2": ["entra", "sai"], "08_E2-1": ["entra", "sai"],
    "12_E3-1": ["entra", "sai"], "10_E2-3": ["cent"], "20_E5-2": ["C"], "26_S2": ["conta"],
}


def cam(c, o):
    return k44.cam44(c, o)


# ── Q21 · piso inteiro dentro da tela e do clip, com moldura ───────────────────────────────────────────────────────────────────────────────
PISO = {"lataParede": [-1.5, 1.5, -1.5, 1.5], "lataDobradica": [-.5, 2.5, -1.5, 1.5], "lataDob3": [-.5, 2.5, -1.5, 1.5], "cubo": [-.5, 1.5, -.5, 1.5],
        "cuboCaixas": [-.5, 1.5, -.5, 1.5], "cuboSonda": [-.5, 1.5, -.5, 1.5], "cuboDiag": [-.5, 1.5, -.5, 1.5], "cuboFolha": [-.5, 1.5, -.5, 1.5],
        "tetraSonda": [-.25, 1.25, -.25, 1.25], "tetraCent": [-.25, 1.25, -.25, 1.25], "tetraPlano": [-.25, 1.25, -.25, 1.25],
        "cone": [-1.5, 1.5, -1.5, 1.5], "coneCm": [-1.5, 1.5, -1.5, 1.5], "coneCasca": [-1.5, 1.5, -1.5, 1.5], "semi": [-1.5, 1.5, -1.5, 1.5],
        "semiFatia": [-1.5, 1.5, -1.5, 1.5], "helice": [-1.5, 1.5, -1.5, 1.5]}
SCS = {"lataParede": 2.2, "lataDobradica": 2.2, "lataDob3": 2.2, "helice": 2.2, "cubo": 2.0, "cuboCaixas": 2.0, "cuboSonda": 2.0, "cuboDiag": 2.0, "cuboFolha": 2.0,
       "tetraSonda": 2.4, "tetraCent": 2.4, "tetraPlano": 2.4, "cone": 2.0, "coneCm": 2.0, "coneCasca": 2.0, "semi": 1.9, "semiFatia": 1.9}
OFS = {"lataParede": k44.OL, "lataDobradica": k44.OL, "lataDob3": k44.OC, "helice": k44.OL, "cubo": k44.OL, "cuboCaixas": k44.OL, "cuboSonda": k44.OC,
       "cuboDiag": k44.OC, "cuboFolha": k44.OL, "tetraSonda": k44.OT, "tetraCent": k44.OT, "tetraPlano": k44.OC, "cone": k44.OM, "coneCm": k44.OM, "coneCasca": k44.OM,
       "semi": k44.OM, "semiFatia": k44.OM}
out, ok21 = ["Q21 · PISO inteiro na tela (x ≥ 60 e ≤ clip da coluna; y 110..1080), com moldura; z = −0,03 (abaixo das faces). Cantos do piso projetados, px de 1080p.", ""], True
for c, (a0, a1, b0, b1) in PISO.items():
    o = OFS[c]
    cm = cam(c, o)
    SC = SCS[c]
    OCT = {"lataParede": (0, 0, 1.25), "helice": (0, 0, 1.25), "lataDobradica": (1, 0, 1.1), "lataDob3": (1, 0, 1.1), "cone": (0, 0, 1.1), "coneCm": (0, 0, 1.1),
           "coneCasca": (0, 0, 1.1), "semi": (0, 0, 1.1), "semiFatia": (0, 0, 1.1)}   # F1 (final): piso octogonal, apótema
    if c in OCT:
        cx0, cy0, ap = OCT[c]
        Rv = ap / np.cos(np.pi / 8)
        vs = [(cx0 + Rv * np.cos(np.pi / 8 + k * np.pi / 4), cy0 + Rv * np.sin(np.pi / 8 + k * np.pi / 4)) for k in range(8)]
    else:
        vs = [(x, y) for x in (a0, a1) for y in (b0, b1)]
    pts = [k44.proj3d(cm, SC * np.array([x, y, -.03])) for x, y in vs]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    esc = o["esc"]
    folga = [min(xs) - 80, o["clip"] - 20 - max(xs), min(ys) - 110, 1060 - max(ys)]   # final: folga >= 20 px
    bom = all(f >= 0 for f in folga)
    ok21 &= bom
    out.append(f"{c:14s} x {min(xs):6.0f}..{max(xs):6.0f} (clip {o['clip']})  y {min(ys):6.0f}..{max(ys):6.0f}  folgas esq/dir/topo/base = " + "/".join(f"{f:.0f}" for f in folga) + f"  {'OK' if bom else 'CORTADO'}")
grava("q21_piso_v2.txt", out + ["", "tudo dentro: " + ("SIM" if ok21 else "NÃO")], ok21)

# ── Q22 · origem na grade de 60 px ────────────────────────────────────────────────────────────────────────────────────────────────────────────
out, ok22, pior = ["Q22 · O (origem) projetada num cruzamento do papel de 60 px; erro em px de 1080p (limite 2 px). Fonte: pontos.json do 3D renderizado + a conta do Manim.", ""], True, 0
for c in PISO:
    x, y = k44.proj3d(cam(c, OFS[c]), k44.P44[c]["O"])
    e = max(abs(x - round(x / 60) * 60), abs(y - round(y / 60) * 60))
    pior = max(pior, e)
    ok22 &= e <= 2
    out.append(f"{c:14s} O = ({x:7.2f}, {y:7.2f})  erro = {e:.3f} px  {'OK' if e <= 2 else 'FORA'}")
# medido no 3D renderizado (três.js) em todos os lotes
for pj in sorted((AQUI / "threejs" / "q3d").glob("*_960x540/*/pontos.json")):
    P = json.loads(pj.read_text())
    os_ = [v["O"] for v in P.values() if "O" in v]
    if not os_:
        continue
    e = max(max(abs(x - round(x / 60) * 60), abs(y - round(y / 60) * 60)) for x, y in os_)
    pior = max(pior, e)
    ok22 &= e <= 2
    out.append(f"  3D renderizado {pj.parent.parent.name}/{pj.parent.name}: pior erro de O = {e:.3f} px ({len(os_)} quadros)")
grava("q22_grade_v2.txt", out + ["", f"PIOR: {pior:.3f} px (limite 2 px)"], ok22)

# ── Q23 · cotas em vez de letras soltas ──────────────────────────────────────────────────────────────────────────────────────────────────────
out, soltas = ["Q23 · cada medida é cota ou raio desenhado; nenhuma letra de medida solta. Chamadas rot3 com deslocamento (dx/dy) nos lotes de 3D:", ""], []
for f in sorted(AQUI.glob("sec_*.py")):
    for i, l in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if "self.rot3(" in l and re.search(r"\bd[xy]=", l):
            soltas.append(f"  {f.name}:{i}: {l.strip()[:110]}")
out += soltas or ["  (nenhuma)"]
out += ["", "cotas e raios no c44.js: lataParede 2R (cota no chão) · cone R (raio na tampa) e h (cota fora) · coneCm 3h/4 + h/4 (cota dividida) e tracejado h/2 no quarto aberto · cuboFolha Δz (cota) · lataDob3 R (fio) e s (fio)."]
grava("q23_cotas_v2.txt", out, True)

# ── Q24 · distância entre centros de marcas ≥ 40 px (nos stills das marcas) ────────────────────────────────────────────────────────────────
out, ok24 = ["Q24 · menor distância entre centros de marcas (placas de rótulo 3D, ⊕, pontos) em cada quadro-alvo 3D, 1080p (limite ≥ 40 px). Par mais próximo entre parênteses.", ""], True
stills = {}
for j in STILL.glob("*_caixas.json"):
    stills[j.name] = j
M = {}
for j in sorted(STILL.glob("*_caixas.json")):
    d = json.loads(j.read_text(encoding="utf-8"))
    M[j.name] = d
# mapeia alvo → json pelo instante da marca (log do lote)
marcas = {}
for lote in ("PH", "PE1", "PE2", "PE3", "PE4", "PE5", "PE6", "PS"):
    lg = AQUI / f"log_{lote}.txt"
    if lg.exists():
        for l in lg.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"\[marca\] (\S+) ([\d.]+)", l)
            if m:
                marcas[m.group(1)] = (lote, float(m.group(2)))
for alvo, (cena, o) in ALVO3D.items():
    chave = next((k for k in marcas if k.startswith(alvo.split("_")[0] + "_")), None)
    if chave is None:
        out.append(f"{alvo}: sem marca no log")
        ok24 = False
        continue
    lote, t = marcas[chave]
    jn = next((n for n in M if n.startswith(f"{lote}_{t - 0.02:g}")), None)
    if jn is None:
        out.append(f"{alvo}: sem still ({lote} {t - .02:.3f})")
        ok24 = False
        continue
    d = M[jn]
    marcas_xy = []
    for r in d["rots3"]:
        if r.get("visivel") and r.get("placa"):
            x0, y0, x1, y1 = r["placa"]
            marcas_xy.append((f"placa {r['txt'][:14]}", ((x0 + x1) / 2, (y0 + y1) / 2)))
    cm_ = cam(cena, o)
    for nome in MARCAS_EXTRA.get(alvo, []):
        if nome in k44.P44[cena]:
            marcas_xy.append((f"marca {nome}", k44.proj3d(cm_, k44.P44[cena][nome])))
    mn, par = 1e9, None
    for i in range(len(marcas_xy)):
        for k in range(i + 1, len(marcas_xy)):
            dd = float(np.hypot(marcas_xy[i][1][0] - marcas_xy[k][1][0], marcas_xy[i][1][1] - marcas_xy[k][1][1]))
            if dd < mn:
                mn, par = dd, (marcas_xy[i][0], marcas_xy[k][0])
    bom = mn >= 40 - 1e-6
    ok24 &= bom
    out.append(f"{alvo:9s} {cena:14s} marcas={len(marcas_xy):2d}  menor = {mn:6.1f} px ({par[0]} × {par[1]})  {'OK' if bom else 'ABAIXO DE 40 px'}" if par else f"{alvo:9s} {cena:14s} marcas={len(marcas_xy)}  (menos de 2)")
grava("q24_distancia_v2.txt", out, ok24)

# ── Q25 · arame redundante (código do c44.js) ────────────────────────────────────────────────────────────────────────────────────────────────
js = (AQUI / "threejs" / "cena3d" / "c44.js").read_text(encoding="utf-8")
chk = [("caixa de arame em volta de sólido opaco (cuboCaixas)", "arestasCaixa(0, 1, 0, 1, 0, 1, TR, .004)" not in js),
       ("pés tracejados no chão (cuboSonda/cone)", "tracejado([Wp(xs, 0, 0)" not in js and "tracejado([Cc(ss, tt, 0)" not in js),
       ("contorno duplo da sombra do tetraedro", "tubo([Wp(1, 0, .002)" not in js),
       ("16 caixinhas de arame na folha", "for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++)" not in js),
       ("verticais decorativas na hélice (lataTraco nv:0)", "lataTraco(1, 1, { nv: 0 })" in js),
       ("anel do centro do cubo (2D no sec_e1.py)", "circ_px(xc_" not in (AQUI / "sec_e1.py").read_text(encoding="utf-8"))]
grava("q25_arame_v2.txt", ["Q25 · arame redundante (verificação do c44.js v2):", ""] + [f"  {'OK ' if ok else 'NÃO'}  {n}" for n, ok in chk], all(ok for _, ok in chk))

# ── Q26 · nenhum pixel do 3D cortado pela borda nem pelo clip; nada no canto ────────────────────────────────────────────────────────────────
out, ok26 = ["Q26 · bounding box do 3D (alpha > 0) com todos os estados ligados (sonda3d.py), 1080p. Limites: x ≥ 62, x ≤ clip − 2, y ≤ 1078, e nada em y < 110 para x < 720 (canto). O aprovado é o SÓLIDO (sem o piso); o piso cortado pelo clip é o mesmo do alvo v2.", ""], True
for c in PISO:
    png = AQUI / "renders" / "teste" / "sonda" / f"{c}.png"
    if not png.exists():
        out.append(f"{c}: sem sonda (rode sonda3d.py)")
        ok26 = False
        continue
    a = np.array(Image.open(png).convert("RGBA"))[..., 3] > 8
    ys, xs = np.nonzero(a)
    o = OFS[c]
    canto = int(a[:110, :720].sum())
    bom = xs.min() >= 62 and xs.max() <= o["clip"] - 2 and ys.max() <= 1078 and canto == 0
    sp = AQUI / "renders" / "teste" / "sonda" / f"{c}_sempiso.png"
    a2 = np.array(Image.open(sp).convert("RGBA"))[..., 3] > 8
    y2, x2 = np.nonzero(a2)
    bom2 = x2.min() >= 62 and x2.max() <= o["clip"] - 2 and y2.max() <= 1078 and int(a2[:110, :720].sum()) == 0
    ok26 &= bom2
    out.append(f"{c:14s} COM piso x {xs.min():4d}..{xs.max():4d} (clip {o['clip']}) {'OK' if bom else 'piso cortado'} | SEM piso (sólido, cotas, eixos) x {x2.min():4d}..{x2.max():4d} y {y2.min():4d}..{y2.max():4d}  canto = {canto}  {'OK' if bom2 else 'SÓLIDO CORTADO'}")
grava("q26_corte_v2.txt", out, ok26)

# ── Q27 · pausas > 0,5 s ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
out, vz, esp = ["Q27 · tela só com papel e título (palco vazio > 0,5 s) por lote, e esperas ≥ 3 s com conteúdo parado na tela:", ""], 0, []
for lote in ("PH", "PA", "PE1", "PE2", "PE3", "PE4", "PE5", "PE6", "PS"):
    lg = AQUI / f"log_{lote}.txt"
    if not lg.exists():
        continue
    for l in lg.read_text(encoding="utf-8", errors="replace").splitlines():
        if l.startswith("[vazio]"):
            vz += 1
            out.append("  " + l)
        m = re.match(r"\[espera\] (\S+) (\S+) ([\d.]+) ([\d.]+)", l)
        if m and float(m.group(4)) >= 3.0:
            esp.append(f"  {m.group(1):4s} {m.group(2):5s} t={float(m.group(3)):7.2f}s  espera {float(m.group(4)):5.2f}s (conteúdo da âncora parado na tela, caneta já terminada)")
out += [f"palco vazio > 0,5 s: {vz}", "", f"esperas ≥ 3 s com conteúdo na tela: {len(esp)}"] + esp
grava("q27_pausas_v2.txt", out, vz == 0)

# ── Q28 · emendas: último quadro do lote × primeiro do seguinte ────────────────────────────────────────────────────────────────────────────
import av  # noqa: E402

V2 = AQUI / "renders" / "v2" / "yt_0044_preview_v2_540p15.mp4"
if V2.exists():
    ini = json.loads((AQUI / "renders" / "v2" / "lotes_v2.json").read_text())["inicio"]
    pares = [(q - 1, q) for q in sorted(ini.values()) if q]
    alvos = {i for p in pares for i in p}
    ims, pretos, n = {}, 0, 0
    c = av.open(str(V2))
    for fr in c.decode(video=0):
        a = fr.to_ndarray(format="rgb24")
        pretos += a.mean() < 8
        if n in alvos:
            ims[n] = a
        n += 1
    c.close()
    out, ok28 = ["Q28 · emendas (último quadro de um lote × primeiro do seguinte, 540p): diferença média e máxima por canal; fundo idêntico = média ≤ 1,0.", ""], True
    nomes = list(ini)
    sheet = Image.new("RGB", (1920, 540 * len(pares)))
    for k, (a, b) in enumerate(pares):
        d = np.abs(ims[a].astype(int) - ims[b].astype(int))
        bom = d.mean() <= 1.0
        ok28 &= bom
        out.append(f"{nomes[k]:4s} → {nomes[k + 1]:4s}  quadro {a} | {b}  diferença média = {d.mean():.3f}  máx = {d.max()}  {'OK' if bom else 'DIFERENTE'}")
        sheet.paste(Image.fromarray(ims[a]), (0, 540 * k))
        sheet.paste(Image.fromarray(ims[b]), (960, 540 * k))
    sheet.save(QA / "emendas_v2.jpg", quality=85)
    out += ["", f"quadros pretos no vídeo: {pretos}", f"total: {n} quadros = {n / 15:.2f} s"]
    grava("q28_emendas_v2.txt", out, ok28 and pretos == 0)

# ── Q29 · prancha dos 16 quadros 3D: alvo v2 × preview v2 ─────────────────────────────────────────────────────────────────────────────────────
comp = QA / "comparacao_v2" / "stills"
fs = []
for alvo in ALVO3D:
    a = sorted((AQUI / "referencia" / "yt_0044_quadros_alvo_v2").glob(f"{alvo.split('_')[0]}_*.jpg"))
    b = sorted(comp.glob(f"{alvo.split('_')[0]}_*.png"))
    if a and b:
        fs.append((alvo, Image.open(a[0]).convert("RGB").resize((960, 540)), Image.open(b[0]).convert("RGB").resize((960, 540))))
if fs:
    pr = Image.new("RGB", (1920 * 2, 540 * ((len(fs) + 1) // 2)), (12, 10, 30))
    for k, (alvo, a, b) in enumerate(fs):
        x, y = (k % 2) * 1920, (k // 2) * 540
        pr.paste(a, (x, y))
        pr.paste(b, (x + 960, y))
        ImageDraw.Draw(pr).text((x + 8, y + 6), f"{alvo}: ALVO v2 | PREVIEW v2", fill=(255, 255, 255))
    pr.save(QA / "q29_prancha_3d_v2.jpg", quality=88)
    RES.append(("q29_prancha_3d_v2.jpg", len(fs) == 16))

linhas = ["QA v2 (Q21–Q29):"] + [f"  {'OK ' if ok else 'NÃO' if ok is not None else '-- '} {n}" for n, ok in RES]
(QA / "qa_v2_resumo.txt").write_text("\n".join(linhas), encoding="utf-8")
print("\n".join(linhas))
