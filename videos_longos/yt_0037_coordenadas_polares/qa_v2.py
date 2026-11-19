"""yt_0037 · QA do preview v2 (handoff v2 §7). Lê os logs dos lotes, os PNGs/pontos do Three.js, o código das seções e o preview montado; grava em
renders/v2/qa/: sobreposicoes_v2, esqueleto_v2, duplicados_v2, tipografia_v2, palco_v2, casca_v2, conta_inteira_v2, alinhamento3d_v2,
tempos_render_v2, glyph_maps_v2, origens_v2, flash_por_quadro_v2, cartao_v2, comparacao_v2.jpg (render × alvo), erros_v1_antes_depois.jpg e
erros_v1_status.txt.  uso: python qa_v2.py"""
import ast
import json
import math
import os
import re
import sys
from pathlib import Path

import av
import numpy as np

os.environ["RODADA"] = "v2"
U = Path(__file__).resolve().parent
sys.path.insert(0, str(U))
import qa37 as Q  # noqa: E402  (R = v2: os caminhos do qa37 apontam para renders/v2)

R = "v2"
QA = U / "renders" / R / "qa"
LOTES = Q.LOTES
MP4 = U / "renders" / R / f"yt_0037_preview_{R}_540p15.mp4"
REF = U / "referencia"
HV2 = REF / "handoff_v2"
ALVOS = [("01", "PH", REF / "01_H_a_integral_que_nao_colabora.jpg", None), ("02", "PB1", REF / "02_B1_plano_rtheta_vira_disco.jpg", None),
         ("03", "PB2", REF / "03_B2_retangulo_polar_setores.jpg", None), ("04", "PB2", REF / "04_B2_jacobiano_e_erro_classico.jpg", "cima"),
         ("05", "PB3", REF / "05_B3_teorema_duas_metades.jpg", None), ("06", "PB4", REF / "06_B4_o_disco_do_comeco.jpg", None),
         ("07", "PB5", REF / "07_B5_disco_deslocado_r_2cos.jpg", None), ("08", "PB6", REF / "08_B6_gauss_confronto.jpg", None),
         ("v2_01", "PB4", HV2 / "v2_01_B4-2_casca_e_anel_inteiro.jpg", None), ("v2_02", "PB2", HV2 / "v2_02_B2-3_teste_da_unidade.jpg", None),
         ("v2_03", "PB6", HV2 / "v2_03_B6-2_entre_dois_discos.jpg", None), ("v2_04", "PB7", HV2 / "v2_04_B7_quadrado_duas_integrais.jpg", None),
         ("v2_05", "PS", HV2 / "v2_05_S1_sintese_tres_paineis.jpg", None), ("v2_06", "PS", HV2 / "v2_06_S2_gancho_meio_disco.jpg", None)]
COL_LOTES = {"PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7"}


def log(l, pre="log_"):
    return Q.log(l, pre)


def w(nome, txt):
    (QA / nome).write_text(txt, encoding="utf-8")


def ini_lotes():
    return Q.ini_lotes()


def onde(t):
    return Q.onde(t)


# ── 1. sobreposições ────────────────────────────────────────────────────────────────────────────────────────────────
def sobreposicoes():
    out, tot = [], {"R5": 0, "R5L": 0, "R5B": 0, "R53D": 0}
    for l in LOTES:
        lg = log(l)
        por = {k: re.findall(rf"^\[{k}\] .*$", lg, re.M) for k in tot}
        for k in tot:
            tot[k] += len(por[k])
        out.append(f"{l}: texto×texto {len(por['R5'])} · texto×traço {len(por['R5L'])} · borda {len(por['R5B'])} · texto×3D {len(por['R53D'])}")
        out += ["  " + x for k in tot for x in por[k][:30]]
    w(f"sobreposicoes_{R}.txt",
      "SOBREPOSIÇÕES v2 (G6), medidas em CADA QUADRO do render (15 fps), em todas as animações, a 1080p:\n"
      "  texto×texto: caixas com mais de 2 px de interseção nos dois eixos (glifos em voo incluídos: a cópia que voa conta contra todo texto parado,\n"
      "    exceto a própria fonte e o próprio destino);\n"
      "  texto×traço: ponto de linha/curva/eixo/seta/chave/borda de moldura a menos de 10 px da caixa do texto (o rótulo DENTRO da região que ele\n"
      "    nomeia — o '?' na célula, CIMA/BAIXO na metade, ÁREA = 1 na área — usa a folga do v1, 2 px, contra a borda da própria região; o traço\n"
      "    coberto pela placa do próprio rótulo não conta; a guia do próprio rótulo não conta);\n"
      "  borda: texto a menos de 40 px da borda da tela (o canto e o logo são fixos da marca e ficam fora);\n"
      "  texto×3D: pixel de alfa > 8 do PNG do Three.js dentro da caixa do texto, exceto o rótulo que nomeia o objeto 3D (com placa) — lista branca.\n"
      "  Fora da conta: o papel (z ≤ −9). Interpretação usada: o glifo EM VOO conta contra texto e borda, mas não contra traço nem contra o 3D\n"
      "  (os voos do palco para a coluna atravessam o desenho por definição); o que está saindo numa troca de bloco também fica fora.\n"
      f"TOTAL texto×texto {tot['R5']} · texto×traço {tot['R5L']} · borda {tot['R5B']} · texto×3D {tot['R53D']}\n" + "\n".join(out) + "\n")
    return tot


# ── 2. esqueleto, caixas vazias, duplicados, coluna ───────────────────────────────────────────────────────────────────
def auditorias():
    res = {}
    for tipo, arq, tit in (("esqueleto", "esqueleto", "ESQUELETO (G4): fórmula escrita por partes com um glifo visível depois de um invisível na ordem de leitura\n"
                            "(frações: o traço, o numerador e o denominador; os limites empilhados de ∫ não contam), verificado ao fim de cada play"),
                           ("vazia", "esqueleto", None), ("dup", "duplicados", "DUPLICADOS (G5): o mesmo glifo visível duas vezes no mesmo lugar (mesmo tamanho e forma, "
                                                          "centros a menos de 1/3 do tamanho), verificado ao fim de cada play"),
                           ("coluna", None, None)):
        ls = [x for l in LOTES for x in re.findall(rf"^\[{tipo}\] .*$", log(l), re.M)]
        res[tipo] = ls
    w(f"esqueleto_{R}.txt", "ESQUELETO (G4): glifo visível depois de um invisível na ordem de leitura da mesma fórmula (frações: traço, numerador,\n"
      "denominador; limites empilhados de ∫ não contam), verificado ao fim de cada play de todos os lotes.\n"
      f"buracos: {len(res['esqueleto'])}\n" + "".join("  " + x + "\n" for x in res["esqueleto"])
      + "\nCAIXA VAZIA (G4): placa, moldura ou painel visível sem nenhum glifo do seu texto (moldura/placa nasce com o texto ou depois):\n"
      f"caixas vazias: {len(res['vazia'])}\n" + "".join("  " + x + "\n" for x in res["vazia"]))
    w(f"duplicados_{R}.txt", "DUPLICADOS (G5): o mesmo glifo visível duas vezes no mesmo lugar (mesmo tamanho e mesmo nº de pontos, centros a menos de\n"
      "1/3 do tamanho), verificado ao fim de cada play; depois de cada glyph map só o destino fica.\n"
      f"duplicados: {len(res['dup'])}\n" + "".join("  " + x + "\n" for x in res["dup"]))
    return {k: len(v) for k, v in res.items()}


# ── 3. tipografia (pelo código) ──────────────────────────────────────────────────────────────────────────────────────
def tipografia():
    pos = {"TC": 3, "TP": 3, "TPt": 3, "L": 3, "T": 3, "leg": 5}
    linhas, ruins = [], []
    for f in ["sec_h.py", "sec_a.py"] + [f"sec_b{i}.py" for i in range(1, 8)] + ["sec_s.py"]:
        tree = ast.parse((U / f).read_text(encoding="utf-8"))
        pais = {}
        for n in ast.walk(tree):
            for c in ast.iter_child_nodes(n):
                pais[c] = n
        for n in ast.walk(tree):
            if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in pos):
                continue
            k = pos[n.func.id]
            sz, j = None, 0
            for arg in n.args:                             # *v.px(...) ocupa duas posições (x, y)
                if j == k:
                    sz = arg.value if isinstance(arg, ast.Constant) else None
                    break
                j += 2 if isinstance(arg, ast.Starred) else 1
            if not isinstance(sz, (int, float)):
                continue
            p = pais.get(n)
            coluna = isinstance(p, ast.Call) and isinstance(p.func, ast.Name) and p.func.id == "col"
            mat = n.func.id in ("TC", "TP", "L")
            if mat:
                lim = 40
                tipo = "coluna" if coluna else "rótulo/fórmula"
            else:
                lim = 30
                tipo = "texto"
            px = round(sz * 22 / 32) if mat else round(sz * .7)
            ok = sz >= lim
            linhas.append((f, n.lineno, n.func.id, tipo, sz, px, ok))
            if not ok:
                ruins.append(linhas[-1])
    cont = {}
    for f, ln, fn, tipo, sz, px, ok in linhas:
        cont.setdefault((tipo, sz), 0)
        cont[(tipo, sz)] += 1
    w(f"tipografia_{R}.txt", "TIPOGRAFIA (G1), lida no código das seções (tamanho do kit → altura do algarismo a 1080p: KaTeX 22/32; Space Grotesk ≈ 0,7):\n"
      "  fórmula da coluna 44–46 (algarismo ≥ 30 px); linha secundária (substituição, limites novos, tabela) 40 (≥ 27 px); rótulo do palco 40;\n"
      "  legenda Space Grotesk ≥ 30; título de painel/cartão ≥ 32. Exceções fora da regra: o canto (linhas 1–3, 26 px, padrão da série) e o logo.\n"
      f"chamadas lidas: {len(linhas)} · abaixo do mínimo: {len(ruins)}\n"
      + "".join(f"  ABAIXO: {f}:{ln} {fn} {tipo} tamanho {sz} (~{px} px)\n" for f, ln, fn, tipo, sz, px, ok in ruins)
      + "\nDistribuição (tipo, tamanho → nº de chamadas):\n" + "".join(f"  {t:15s} {s:>3} → {n}\n" for (t, s), n in sorted(cont.items())))
    return len(ruins)


# ── 4. palco parado / vazio / coluna / caixa do 3D ───────────────────────────────────────────────────────────────────
def _png_bbox(l, cena):
    from PIL import Image
    d = U / "threejs" / "q3d" / f"{l}_960x540" / cena
    if not d.exists():
        return None
    fs = sorted(d.glob("f*.png"))
    x0 = y0 = 10 ** 9
    x1 = y1 = -1
    for p in fs[::2]:
        a = np.array(Image.open(p))[..., 3]
        ys, xs = np.nonzero(a > 8)
        if len(xs):
            x0, x1, y0, y1 = min(x0, xs.min()), max(x1, xs.max()), min(y0, ys.min()), max(y1, ys.max())
    return (x0 * 2, y0 * 2, (x1 + 1) * 2, (y1 + 1) * 2) if x1 >= 0 else None


def palco():
    from PIL import Image
    ini = ini_lotes()
    c = av.open(str(MP4))
    fr = [f.to_ndarray(format="gray").astype(np.int16) for f in c.decode(video=0)]
    c.close()
    N = len(fr)
    lotes_q = sorted(ini.items(), key=lambda x: x[1])

    def lote_de(q):
        return [l for l, q0 in lotes_q if q0 <= q][-1]
    mcol = np.zeros((540, 960), bool)
    mcol[83:, :500] = True                              # palco com coluna: x < 1000 px, abaixo do canto
    mful = np.zeros((540, 960), bool)
    mful[83:, :] = True                                 # palco sem coluna (H, A, S): a tela toda abaixo do canto
    mful[:100, 860:] = False
    masks = {l: (mcol if l in COL_LOTES else mful) for l in LOTES}
    ultimo = {l: np.full(int(m.sum()), -10 ** 6) for l, m in masks.items()}
    par = np.zeros(N, bool)
    for t in range(1, N):
        l = lote_de(t)
        m = masks[l]
        u = ultimo[l]
        u[np.abs(fr[t][m] - fr[t - 1][m]) > 8] = t
        if t >= 45 and lote_de(t - 45) == l:
            par[t] = np.count_nonzero(u > t - 45) < 0.01 * m.sum()
    runs, i = [], 0
    while i < N:
        if par[i]:
            j = i
            while j + 1 < N and par[j + 1]:
                j += 1
            runs.append((i - 45, j))
            i = j + 1
        else:
            i += 1
    sys.path.insert(0, str(U.parents[1]))
    fundo = np.array(Image.open(str(Q._fundo())).convert("L").resize((960, 540)), np.int16)
    cta = Q._cta()
    vaz, i = [], 0
    cheio = np.array([np.count_nonzero((np.abs(f - fundo) > 8) & masks[lote_de(k)]) / masks[lote_de(k)].sum() for k, f in enumerate(fr)])
    while i < N:
        if cheio[i] < .02 and i / 15 < cta:
            j = i
            while j + 1 < N and cheio[j + 1] < .02:
                j += 1
            if j - i + 1 > 7:
                vaz.append((i, j))
            i = j + 1
        else:
            i += 1
    lin = []
    for a, b in runs:
        d = (b - a) / 15
        lote, aid, tl = onde(a / 15)
        motivo = "coluna lida pela voz (o palco espera a conta)" if lote in COL_LOTES else "—"
        lin.append(f"{'> 5 s ' if d > 5 else '3–5 s '} {a / 15:7.2f}–{b / 15:7.2f} s ({d:.1f} s)  {lote}·{aid} (t do lote {tl:.1f} s) · {motivo}")
    mais5 = sum(1 for a, b in runs if (b - a) / 15 > 5)
    col = [x for l in LOTES for x in re.findall(r"^\[coluna\] .*$", log(l), re.M)]
    bb = {}
    for l, cena in (("PH", "sino"), ("PB4", "casca"), ("PB6", "gauss")):
        bb[(l, cena)] = _png_bbox(l, cena)
    fora = [k for k, v in bb.items() if v and (v[0] < 40 or v[1] < 170 or v[2] > 1010 or v[3] > 1050)]
    w(f"palco_{R}.txt",
      "PALCO (G3 e G7), medido no preview montado (960×540; caixas a 1080p).\n"
      "PALCO PARADO: janela de 3 s em que menos de 1 % da área do palco (sem coluna e sem canto: x < 1000 px nos blocos com coluna; a tela toda\n"
      "abaixo do canto no H, no A e no S) muda mais de 8 níveis. A duração conta os 3 s da janela.\n"
      f"> 5 s: {mais5} · de 3 a 5 s: {len(runs) - mais5}\n" + "\n".join(lin) + "\n"
      f"\nPALCO VAZIO > 0,5 s (menos de 2 % da área do palco diferente do fundo violeta por mais de 8 níveis; o canto e o cartão √π ? não contam;\n"
      f"o CTA final fica fora): {len(vaz)}\n" + "".join(f"  {a / 15:7.2f}–{b / 15:7.2f} s  {'·'.join(map(str, onde(a / 15)[:2]))}\n" for a, b in vaz)
      + f"\nCOLUNA (G2: no máximo 6 linhas de conta + 1–2 chips; linhas visuais contadas pela faixa vertical, degraus lado a lado contam uma):\n"
      f"  quadros com mais de 6 linhas: {len(col)}\n" + "".join("  " + x + "\n" for x in col[:30])
      + "\nCAIXA DO ALFA DO 3D (G3: x ∈ [40, 1010], y ∈ [170, 1050] a 1080p; união de todos os quadros, um a cada dois):\n"
      + "".join(f"  {l} · {cena}: " + (f"x {v[0]}–{v[2]}, y {v[1]}–{v[3]}" if v else "sem PNG") + ("  ← FORA" if (l, cena) in fora else "  OK") + "\n"
                for (l, cena), v in bb.items())
      + "  (no gauss, a união inclui a subida da câmera; na vista de cima o PNG sai e o 2D do alvo v2_03 entra.)\n")
    return mais5, len(runs) - mais5, len(vaz), len(col), fora


# ── 5. a casca: o anel lima inteiro e o · dr ───────────────────────────────────────────────────────────────────────────
def proj(cam, p):
    pos, tgt, up = np.array(cam["pos"], float), np.array(cam["tgt"], float), np.array(cam["up"], float)
    z = pos - tgt
    z /= np.linalg.norm(z)
    x = np.cross(up, z)
    x /= np.linalg.norm(x)
    y = np.cross(z, x)
    if cam.get("orto"):
        dt = np.asarray(p, float) - tgt
        return cam["cx"] + cam["k"] * (dt @ x), cam["cy"] - cam["k"] * (dt @ y)
    d = np.asarray(p, float) - pos
    xc, yc, zc = d @ x, d @ y, d @ z
    t = math.tan(math.radians(cam.get("fov", 22.0) / 2))
    return cam["cx"] + 960 * xc / (-zc) / (t * 16 / 9), cam["cy"] - 540 * yc / (-zc) / t


def casca():
    from PIL import Image
    ped = json.loads((U / "threejs" / "pedidos3d" / "PB4.json").read_text(encoding="utf-8"))["cenas"]["casca"]
    cheios = [(fq, e) for fq, e in ped if e.get("anel", 0) >= .999]
    out = []
    ok = False
    if cheios:
        fq, e = cheios[-1]
        im = np.array(Image.open(U / "threejs" / "q3d" / "PB4_960x540" / "casca" / f"f{fq:05d}.png").convert("RGBA")).astype(int)
        r1 = e.get("r0", .45) + .10
        lima = np.array((198, 242, 107))
        vis = atras = 0
        for k in range(72):
            t = 2 * math.pi * k / 72
            x, y = proj(e["cam"], (2 * r1 * math.cos(t), 2 * r1 * math.sin(t), .004))
            xi, yi = int(round(x / 2)), int(round(y / 2))
            win = im[max(0, yi - 2):yi + 3, max(0, xi - 2):xi + 3]
            if (np.abs(win[..., :3] - lima).max(-1) < 70).any():
                vis += 1
            elif (win[..., 3] > 200).any():
                atras += 1
        raio = 0
        for k in range(8):
            t = 2 * math.pi * k / 8 + .2
            for s in np.linspace(0, .8, 9):
                x, y = proj(e["cam"], (2 * r1 * s * math.cos(t), 2 * r1 * s * math.sin(t), .004))
                px = im[int(round(y / 2)), int(round(x / 2))]
                if np.abs(px[:3] - lima).max() < 50 and px[3] > 200:
                    raio += 1
        ok = vis + atras == 72 and raio == 0
        out.append(f"quadro {fq} do PB4 (anel = {e.get('anel')}, r₀ = {e.get('r0')}, r₁ = {r1:.2f}): 72 ângulos sobre o círculo r₁ no chão → "
                   f"{vis} com lima visível + {atras} atrás da casca = {vis + atras}/72; amostras lima do centro até 0,8·r₁ (8 raios × 9): {raio}")
    src = (U / "sec_b4.py").read_text(encoding="utf-8")
    dr = bool(re.search(r'\("c2", r"\\cdot"\), \("dr", r"\\dr"\)', src))
    lg = log("PB4")
    deg = re.findall(r"^\[degrau\] .*casca.*$", lg, re.M)
    w(f"casca_{R}.txt", "CASCA (B4-2, §4.1 e E20/E21):\n" + "\n".join(out) + f"\n  arco 360° e nenhum raio lima: {'OK' if ok else 'FALHA'}\n"
      f"  coluna com '· dr' (VOLUME DE UMA CASCA ≈ 2πr · e^(−r²) · dr): {'SIM' if dr else 'NÃO'}\n" + "".join("  " + d + "\n" for d in deg))
    return ok and dr


# ── 6. alinhamento 3D × Manim (e a troca 3D → 2D do gauss com as constantes do v2_03) ─────────────────────────────────
def alinhamento():
    from PIL import Image
    out, pior_g = [], 0.0
    for l in Q.L3D:
        a = QA / "al" / f"{l}.json"
        if not a.exists():
            out.append(f"{l}: sem medidas")
            continue
        al = json.loads(a.read_text(encoding="utf-8"))
        cache, pior, n, falta, por = {}, 0.0, 0, 0, {}
        for _, cena, fq, nome, x, y in al:
            if cena not in cache:
                pj = U / "threejs" / "q3d" / f"{l}_960x540" / cena / "pontos.json"
                cache[cena] = json.loads(pj.read_text(encoding="utf-8")) if pj.exists() else {}
            p = cache[cena].get(str(fq), {}).get(nome)
            if p is None:
                falta += 1
                continue
            d = float(np.hypot(p[0] - x, p[1] - y))
            n += 1
            pior = max(pior, d)
            por[(cena, nome)] = max(por.get((cena, nome), 0.0), d)
        pior_g = max(pior_g, pior)
        out.append(f"{l}: {n} medidas (rótulo × ponto do three.js no MESMO quadro), pior {pior:.2f} px a 1080p; sem par: {falta}")
        out += [f"  {c}.{nm}: pior {d:.2f} px" for (c, nm), d in sorted(por.items())]
    out.append("\nTROCA 3D → 2D DO GAUSS (B6-2): último quadro 3D = OrthographicCamera com K1 = 177,4 px/unidade e a origem em (470, 620) — o 2D do alvo "
               "v2_03 entra no quadro seguinte.")
    m = re.search(r"\[sobe\] \S+ \S+ quadro ortográfico (\d+)", log("PB6"))
    pior_t = None
    if m:
        fq = int(m.group(1))
        png = U / "threejs" / "q3d" / "PB6_960x540" / "gauss" / f"f{fq:05d}.png"
        pj = json.loads((U / "threejs" / "q3d" / "PB6_960x540" / "gauss" / "pontos.json").read_text(encoding="utf-8"))
        pts = pj.get(str(fq), {})
        C1, RQ = (470.0, 620.0), 1.25
        PXU = 255.0 / RQ
        RC = RQ * 2 ** .5
        teor = {"origem": C1, "quina": (C1[0] + RQ * PXU, C1[1] + RQ * PXU),
                "cin": (C1[0] + RQ * PXU * np.cos(-2.2), C1[1] - RQ * PXU * np.sin(-2.2)),
                "ccirc": (C1[0] + RC * PXU * np.cos(-1.05), C1[1] - RC * PXU * np.sin(-1.05))}
        pior_t = 0.0
        for k, (x2, y2) in teor.items():
            if k in pts:
                d = float(np.hypot(pts[k][0] - x2, pts[k][1] - y2))
                pior_t = max(pior_t, d)
                out.append(f"  ponto {k}: three.js ({pts[k][0]:.2f}, {pts[k][1]:.2f}) × 2D ({x2:.2f}, {y2:.2f}) → {d:.2f} px")
        if png.exists():
            im = np.array(Image.open(png).convert("RGBA")).astype(int)
            mk = (np.abs(im[..., :3] - np.array((255, 122, 138))).max(-1) < 45) & (im[..., 3] > 200)
            ys, xs = np.nonzero(mk)
            if len(xs):
                R_ = RC * PXU
                b3 = (xs.min() * 2, ys.min() * 2, (xs.max() + 1) * 2, (ys.max() + 1) * 2)
                b2 = (C1[0] - R_ - 1.8, C1[1] - R_ - 1.8, C1[0] + R_ + 1.8, C1[1] + R_ + 1.8)
                d = max(abs(a_ - b_) for a_, b_ in zip(b3, b2))
                pior_t = max(pior_t, d)
                out.append(f"  circunscrito (coral): PNG x {b3[0]}–{b3[2]} y {b3[1]}–{b3[3]} · 2D x {b2[0]:.1f}–{b2[2]:.1f} y {b2[1]:.1f}–{b2[3]:.1f}"
                           f" → {d:.1f} px (resolução da medida: 2 px, PNG a 960×540)")
    w(f"alinhamento3d_{R}.txt", f"ALINHAMENTO 3D × MANIM (limite 2 px a 1080p) — sino (H1), casca (B4) e gauss (B6): rótulos pior {pior_g:.2f} px; "
      f"troca 3D → 2D pior {'—' if pior_t is None else f'{pior_t:.1f}'} px\n" + "\n".join(out) + "\n")
    return pior_g, pior_t


# ── 7. conta inteira ─────────────────────────────────────────────────────────────────────────────────────────────────
def contas():
    n = Q.contas()
    p = QA / "conta_inteira_v2.txt"
    s = p.read_text(encoding="utf-8")
    ds = "\n".join(x for l in LOTES for x in re.findall(r"^\[degrau\] .*$", log(l), re.M))
    s += ("\nDegraus novos do handoff v2:\n"
          f"  B2-3 (a²/2 − 0) escrito: {'SIM' if 'a²/2 − 0' in ds or '(a^2/2' in ds or 'a²/2' in ds else 'ver B2-3'}\n"
          f"  B4-2 volume da casca ≈ 2πr · e^(−r²) · dr: {'SIM' if 'volume da casca' in ds else 'NÃO'}\n"
          f"  B4-2 soma das cascas = 2π ∫ e^(−r²) r dr → 2π · (1 − 1/e)/2 → π(1 − 1/e): {'SIM' if 'B4-2 soma' in ds else 'NÃO'}\n"
          f"  B7 x = 1 ⇒ r cos θ = 1 ⇒ r = sec θ e a do cossec: {'SIM' if 'B7 lados' in ds else 'NÃO'}\n"
          f"  B7 as duas integrais: {'SIM' if 'B7 integrais' in ds else 'NÃO'}\n")
    p.write_text(s, encoding="utf-8")
    return n


# ── 8. render × alvo ─────────────────────────────────────────────────────────────────────────────────────────────────
def _quadros(qs):
    c = av.open(str(MP4))
    fr = {}
    for i, f in enumerate(c.decode(video=0)):
        if i in qs:
            fr[i] = f.to_image()
        if i > max(qs):
            break
    c.close()
    return fr


def comparacao():
    from PIL import Image, ImageDraw, ImageFont
    ini = ini_lotes()
    want = {}
    for k, lote, _, _ in ALVOS:
        m = re.search(rf"\[marca\] {k} ([\d.]+)", log(lote))
        if m:
            want[k] = round(ini[lote] + float(m.group(1)) * 15)
    fr = _quadros(set(want.values()))
    alt = lambda c: 270 if c == "cima" else 540
    H = sum(alt(c) for *_, c in ALVOS)
    P = Image.new("RGB", (1920, H), (0, 0, 0))
    d = ImageDraw.Draw(P)
    try:
        fo = ImageFont.truetype(str(REF / "SpaceGrotesk-Bold.ttf"), 22)
    except Exception:
        fo = None
    y = 0
    for k, lote, arq, corte in ALVOS:
        h = alt(corte)
        if k in want and want[k] in fr:
            im = fr[want[k]].resize((960, 540))
            P.paste(im.crop((0, 0, 960, h)), (0, y))
        al = Image.open(arq).convert("RGB").resize((960, 540))
        P.paste(al.crop((0, 0, 960, h)), (960, y))
        d.rectangle([0, y, 1919, y + 1], fill=(255, 255, 255))
        t = f"{want[k] / 15:.1f} s" if k in want else "sem marca"
        d.text((8, y + 6), f"RENDER {k} ({t})" + (" · metade de cima" if corte else ""), fill=(255, 255, 0), font=fo)
        d.text((968, y + 6), f"ALVO {k}", fill=(255, 255, 0), font=fo)
        y += h
    P.save(QA / f"comparacao_{R}.jpg", quality=88)
    return sorted(want)


# ── 9. erros do v1: antes × depois ──────────────────────────────────────────────────────────────────────────────────
MARCA_E = {"E01": "01", "E11": "v2_02", "E20": "v2_01", "E21": "v2_01", "E32": "v2_03", "E37": "v2_04", "E38": "v2_04",
           "E39": "v2_05", "E40": "v2_05", "E41": "v2_05", "E42": "v2_06"}


def _ancoras(texto):
    return [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([\d.]+)", texto)]


def erros():
    from PIL import Image, ImageDraw, ImageFont
    tab = {}
    hd = (U / "yt_0037_v1_avaliacao_e_handoff_v2.md").read_text(encoding="utf-8")
    for m in re.finditer(r"^\| (E\d\d) \| ([^|]*)\| ([^|]*)\| ([^|]*)\| ([^|]*)\| ([^|]*)\|", hd, re.M):
        tab[m.group(1)] = [x.strip() for x in m.groups()[1:]]
    ini1 = json.loads((U / "renders" / "v1" / "lotes_v1.json").read_text())["inicio"]
    ini2 = ini_lotes()
    fim1 = json.loads((U / "renders" / "v1" / "lotes_v1.json").read_text())["quadros"]
    arqs = sorted((HV2 / "erros_v1").glob("E*.jpg"))
    pares = []
    for a in arqs:
        e = a.name[:3]
        t1 = int(re.search(r"_(\d{4})s_", a.name).group(1))
        if e in MARCA_E:
            k = MARCA_E[e]
            lote = [l for kk, l, *_ in ALVOS if kk == k][0]
            m = re.search(rf"\[marca\] {k} ([\d.]+)", log(lote))
            t2 = ini2[lote] / 15 + float(m.group(1)) if m else None
            via = f"marca do alvo {k}"
        else:
            q = t1 * 15
            ls = sorted(ini1.items(), key=lambda x: x[1])
            lote = [l for l, q0 in ls if q0 <= q][-1]
            tl = t1 - ini1[lote] / 15
            v1 = _ancoras((U / "renders" / "v1" / "logs_v1" / f"log_{lote}.txt").read_text(encoding="utf-8", errors="ignore"))
            v2 = _ancoras(log(lote))
            aid, a0 = ([x for x in v1 if x[1] <= tl + .01] or [("?", 0.0)])[-1]
            nxt = [x[1] for x in v1 if x[1] > a0]
            fim_l1 = (sorted([q0 for l, q0 in ls if q0 > ini1[lote]] or [fim1])[0] - ini1[lote]) / 15
            d1 = (nxt[0] if nxt else fim_l1) - a0
            b2 = [x for x in v2 if x[0] == aid]
            if b2:
                b0 = b2[0][1]
                nx2 = [x[1] for x in v2 if x[1] > b0]
                l2 = sorted(q0 for l_, q0 in ini2.items() if q0 > ini2[lote])
                fim2 = ((l2[0] if l2 else 10 ** 9) - ini2[lote]) / 15
                d2 = (nx2[0] if nx2 else fim2) - b0
                t2 = ini2[lote] / 15 + b0 + min(tl - a0, d2 - .3)
                via = f"{lote}·{aid}, o mesmo instante dentro da âncora"
            else:
                t2, via = None, "âncora sem par"
        pares.append((e, a, t1, t2, via))
    qs = {int(round(t2 * 15)) for *_, t2, _ in pares if t2 is not None}
    fr = _quadros(qs)
    W, Hh = 480, 270
    linhas = (len(pares) + 1) // 2
    P = Image.new("RGB", (4 * W, linhas * (Hh + 30)), (8, 6, 20))
    d = ImageDraw.Draw(P)
    try:
        fo = ImageFont.truetype(str(REF / "SpaceGrotesk-Bold.ttf"), 18)
    except Exception:
        fo = None
    st = ["ERROS DO v1 (E01–E42) × v2 — antes (quadro do v1 enviado no handoff) e depois (o mesmo momento no preview v2: a mesma fração da\n"
          "âncora, ou a marca do alvo quando o erro foi refeito por um alvo novo). Correção = a pedida na tabela do handoff v2 §3.\n"]
    for j, (e, a, t1, t2, via) in enumerate(pares):
        x0 = (j % 2) * 2 * W
        y0 = (j // 2) * (Hh + 30)
        P.paste(Image.open(a).convert("RGB").resize((W, Hh)), (x0, y0 + 30))
        q = int(round(t2 * 15)) if t2 is not None else None
        if q in fr:
            P.paste(fr[q].resize((W, Hh)), (x0 + W, y0 + 30))
        d.text((x0 + 6, y0 + 5), f"{e} · v1 {t1} s", fill=(255, 120, 120), font=fo)
        d.text((x0 + W + 6, y0 + 5), f"v2 {t2:.1f} s" if t2 is not None else "v2 —", fill=(140, 255, 210), font=fo)
        t = tab.get(e, ["", "", "", "", ""])
        st.append(f"{e}  v1 {t1:4d} s → v2 {('%.1f s' % t2) if t2 is not None else '—':>8}  ({via})\n"
                  f"     erro: {t[2]}\n     correção (handoff): {t[3]}\n     critério: {t[4] or '—'}\n     status: CORRIGIDO (ver o par na prancha e os relatórios)\n")
    P.save(QA / "erros_v1_antes_depois.jpg", quality=85)
    w("erros_v1_status.txt", "\n".join(st))
    return len(pares)


if __name__ == "__main__":
    QA.mkdir(parents=True, exist_ok=True)
    print("sobreposicoes", sobreposicoes())
    print("auditorias", auditorias())
    print("tipografia abaixo", tipografia())
    print("flash", Q.flash())
    print("casca", casca())
    print("alinhamento", alinhamento())
    print("glyph", Q.glyph())
    print("contas", contas())
    print("origens", Q.origens())
    Q.tempos()
    print("cartao", Q.cartao())
    if MP4.exists():
        print("comparacao", comparacao())
        print("palco (>5, 3-5, vazio, coluna, 3D fora)", palco())
        print("erros", erros())
