"""yt_0036 · QA do preview v1 (handoff §8; copiado do qa35.py do yt_0035 e adaptado). Lê os logs dos lotes, os pontos e os PNGs do Three.js e o
preview montado; grava em renders/v1/qa/: sobreposicoes_v1, alinhamento3d_v1, flash_por_quadro_v1, palco_parado_v1, texto_em_mathtex_v1,
glyph_maps_v1, tempos_render_v1 e cartao_v1. (conta_inteira_v1 e origens_v1 saem do qa36_contas.py.)  uso: python qa36.py"""
import json
import math
import os
import re
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
sys.path.insert(0, str(U))
R = os.environ.get("RODADA", "v1")
QA = U / "renders" / R / "qa"
LOTES = ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PB8", "PS"]
SECS = ["sec_h.py", "sec_a.py"] + [f"sec_b{i}.py" for i in range(1, 9)] + ["sec_s.py", "j36.py", "p36.py", "pecas36.py", "lib36.py", "v36.py"]
MP4 = U / "renders" / R / f"yt_0036_preview_{R}_540p15.mp4"
# palco por âncora (máscara a 960×540): A = sem a coluna (x < 1090 px a 1080p); B = os dois planos (quadro inteiro abaixo do canto);
# C760 = coluna em x = 760 (B6-3, B7); B43 = C6 é coluna, o palco é a faixa de baixo à esquerda; B52 = as miniaturas à direita (x ≥ 1460)
PALCO = {"H1": "B", "H2": "B", "A1": "B", "B1-1": "A", "B1-2": "A", "B2-1": "B", "B3-1": "B", "B3-2": "A", "B3-3": "B", "B4-1": "B", "B4-2": "A",
         "B4-3": "B", "B5-1": "B", "B5-2": "B", "B5-3": "B", "B5-4": "A", "B6-1": "A", "B6-2": "B", "B6-3": "C760", "B6-4": "A", "B7": "C760",
         "B8": "B", "S1": "B", "S2": "B"}


def log(l, pre="log_"):
    p = U / f"{pre}{l}.txt"
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""


def ini_lotes():
    j = U / "renders" / R / f"lotes_{R}.json"
    return json.loads(j.read_text())["inicio"] if j.exists() else {}


def onde(t):
    ini = sorted(ini_lotes().items(), key=lambda x: x[1])
    lote, q0 = [x for x in ini if x[1] / 15 <= t + 1e-6][-1]
    tl = t - q0 / 15
    an = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([\d.]+)", log(lote))]
    aid = ([a for a in an if a[1] <= tl + 0.01] or [("?", 0)])[-1][0]
    return lote, aid, tl


def w(nome, txt):
    (QA / nome).write_text(txt, encoding="utf-8")


def r5():
    out, tot, totv = [], 0, 0
    for l in LOTES:
        ls = re.findall(r"^\[R5L?\] .*$", log(l), re.M)
        lv = re.findall(r"^\[R5V\] .*$", log(l), re.M)
        tot += len(ls)
        totv += len(lv)
        out += [f"{l}: R5 {len(ls)} · R5V {len(lv)}"] + ["  " + x for x in ls] + ["  " + x for x in lv]
    w(f"sobreposicoes_{R}.txt", "R5 · SOBREPOSIÇÕES amostradas em CADA QUADRO do preview (15 fps; mais fino que os 0,5 s pedidos), também durante as animações\n"
      "  (a grade que se inclina no B3-1, a malha que curva no B4-1, a câmera do B4-2, a dobra do B5-3, os lados que voam no B6-2).\n"
      "  Tipos: MathTex, Text, as duas linhas do canto, rótulos dos eixos, tiques, placas, o chip |J| = 1/2; texto × texto (caixas, > 2 px nos dois\n"
      "  eixos) e texto × traço (linha, aresta, curva, eixo, seta, borda de célula/painel/cartão/chip: ponto do traço dentro da caixa do texto\n"
      "  encolhida 2 px). Fora da conta: o papel e as famílias de retas da grade (z ≤ −9, a 'grade'), o sublinhado de leitura, o glifo em voo e o\n"
      "  PNG do 3D (a câmera do B4-2 mexe só no PNG; os rótulos presos ao 3D entram como texto).\n"
      "  v2 §7.1: entram também os voos, os glyph maps e os objetos a meio da escrita (opacidade > 0,15).\n"
      "  R5V = travessia: um glifo EM VOO passa por cima de um traço do desenho (eixo, aresta, borda de região) no caminho entre a fonte e o\n"
      "  destino, por alguns quadros; não é sobreposição parada nem texto × texto. Listada à parte.\n"
      f"TOTAL R5 {tot} · R5V (travessias em voo, amostras) {totv}\n" + "\n".join(out) + "\n")
    return tot, totv


def flash():
    out, tot = [], 0
    for l in LOTES:
        m = re.search(r"\[flash-total\] \S+ (\d+)", log(l))
        n = int(m.group(1)) if m else -1
        tot += max(0, n)
        out += [f"{l}: {n} eventos"] + ["  " + x for x in re.findall(r"^\[flash\] .*$", log(l), re.M)[:50]]
    src = "\n".join((U / f).read_text(encoding="utf-8") for f in SECS[:11])
    fi = len(re.findall(r"FadeIn\((?:[A-Z]\w*\d|E\d_|K\d|G\d|F\d|C\d+|D\d|Q\d|R\d|L\d|l\d|n\d_)\b", src))
    w(f"flash_por_quadro_{R}.txt", f"FLASH POR QUADRO (fórmula de caneta visível antes da vez, verificado em TODO quadro de todo play): TOTAL {tot}\n"
      + "\n".join(out) + f"\nFadeIn de fórmula pronta nas seções: {fi}. Succession nas seções: {len(re.findall('Succession', src))} "
      f"(nenhum FadeIn/TransformFromCopy/Write dentro de Succession(Wait…)/AnimationGroup).\n")
    return tot


def _png(l, cena, fq):
    from PIL import Image
    p = U / "threejs" / "q3d" / f"{l}_960x540" / cena / f"f{int(fq):05d}.png"
    return np.array(Image.open(p).convert("RGBA")).astype(int) if p.exists() else None


def alinhamento():
    import j36
    out, pior_g = [], 0.0
    l = "PB4"
    a = QA / "al" / f"{l}.json"
    al = json.loads(a.read_text(encoding="utf-8")) if a.exists() else []
    pj = U / "threejs" / "q3d" / f"{l}_960x540" / "cena1" / "pontos.json"
    pts = json.loads(pj.read_text(encoding="utf-8")) if pj.exists() else {}
    pior, n, falta, por = 0.0, 0, 0, {}
    for _, cena, fq, nome, x, y in al:
        p = pts.get(str(fq), {}).get(nome)
        if p is None:
            falta += 1
            continue
        d = float(np.hypot(p[0] - x, p[1] - y))
        n += 1
        pior = max(pior, d)
        por[nome] = max(por.get(nome, 0.0), d)
    pior_g = pior
    out.append(f"RÓTULOS PRESOS (Manim) × PONTOS DO THREE.JS NO MESMO QUADRO: {n} medidas, pior {pior:.2f} px a 1080p; sem par: {falta}")
    out += [f"  {nm}: pior {d:.2f} px" for nm, d in sorted(por.items())]
    # decolagem e pouso: contorno do paralelogramo 2D × o do PNG no quadro da troca
    lg = log(l)
    dec = re.findall(r"\[decolagem\] \S+ \S+ quadro (\d+)", lg)
    pou = re.findall(r"\[pouso\] \S+ \S+ quadro (\d+)", lg)
    sob = re.findall(r"\[sobe\] \S+ \S+ quadro (\d+)", lg)
    M, W1, C, W2 = (330, 860), (615, 670), (425, 385), (140, 575)          # vista de cima (px a 1080p) = j36.par_xy na vista do zoom
    b2 = (min(p[0] for p in (M, W1, C, W2)), min(p[1] for p in (M, W1, C, W2)), max(p[0] for p in (M, W1, C, W2)), max(p[1] for p in (M, W1, C, W2)))
    out.append("\nDECOLAGEM / POUSO (troca 2D ↔ PNG no mesmo quadro; o PNG nesse quadro é a OrthographicCamera exata da vista de cima).")
    out.append("Medida no PNG (960×540, × 2): caixa dos pixels opacos que não são a grade do chão (paralelogramo + borda + setas, cujas pontas")
    out.append(f"caem nos vértices) contra a caixa do paralelogramo 2D {b2} (os vértices M, w1, C, w2 do 2D).")
    pior_p = 0.0
    G = np.array([0x2B, 0x25, 0x58])
    for nome, fq in [("decolagem", int(dec[0])) if dec else ("decolagem", None), ("pouso", int(pou[0])) if pou else ("pouso", None)]:
        if fq is None:
            out.append(f"  {nome}: sem marca no log")
            continue
        im = _png(l, "cena1", fq)
        if im is None:
            out.append(f"  {nome}: PNG do quadro {fq} ausente")
            continue
        mk = (im[..., 3] > 200) & (np.abs(im[..., :3] - G).max(-1) > 40)
        ys, xs = np.nonzero(mk)
        b3 = (xs.min() * 2, ys.min() * 2, (xs.max() + 1) * 2, (ys.max() + 1) * 2)
        d = max(abs(a_ - b_) for a_, b_ in zip(b3, b2))
        p3 = pts.get(str(fq), {})
        dv = max((float(np.hypot(p3[k][0] - v[0], p3[k][1] - v[1])) for k, v in (("M", M), ("w1", W1), ("C", C), ("w2", W2)) if k in p3), default=-1)
        pior_p = max(pior_p, d - 2)           # a borda de 3 px e a meia-largura da ponta saem ±2 px da caixa dos vértices
        out.append(f"  {nome} (quadro {fq}): PNG x {b3[0]}–{b3[2]} y {b3[1]}–{b3[3]} · 2D x {b2[0]}–{b2[2]} y {b2[1]}–{b2[3]} · maior diferença {d} px "
                   f"(resolução 2 px; borda ±1,5 px) · vértices projetados × 2D: {dv:.2f} px")
    # a câmera da troca: perspectiva com fov 0,5° (primeiro/último quadro em perspectiva) × a ortográfica, nos pontos da cena
    P = [(0, 0, 0), (1.5, 1, 0), (.5, 2.5, 0), (-1, 1.5, 0), (-1.125, -.5, 0), (2.875, 3, 0)]
    cp, co = j36.cam_voo(1e-3), j36.cam_voo(0.0)
    dm = max(math.hypot(*(np.array(j36.proj3d(cp, p)) - np.array(j36.proj3d(co, p)))) for p in P)
    out.append(f"  câmera: quadro em perspectiva vizinho da troca (s = 0,001) × OrthographicCamera: diferença máxima {dm:.2f} px nos cantos do chão")
    # a altura do vetor no quadro final da subida
    if sob:
        fq = int(sob[0])
        im = _png(l, "cena1", fq)
        ped = json.loads((U / "threejs" / "pedidos3d" / f"{l}.json").read_text(encoding="utf-8"))["cenas"]["cena1"]
        e = dict(ped)[fq] if fq in dict(ped) else None
        p3 = pts.get(str(fq), {})
        if im is not None and e is not None and p3:
            Lm = np.array([0xC6, 0xF2, 0x6B])
            mk = (im[..., 3] > 200) & (np.abs(im[..., :3] - Lm).max(-1) < 40)
            ys, xs = np.nonzero(mk)
            topo_png = ys.min() * 2
            m_ = p3["M"]
            u1 = j36.proj3d(e["cam"], (0, 0, 1))
            uni = m_[1] - u1[1]
            h_png = m_[1] - topo_png
            h_pts = m_[1] - p3["topo"][1]
            u325 = m_[1] - j36.proj3d(e["cam"], (0, 0, 3.25))[1]
            out.append(f"\nALTURA DO VETOR (quadro {fq}, fim da subida, sobe = {e.get('sobe')}): no PNG, M.y − topo dos pixels lima = {h_png:.0f} px "
                       f"(resolução 2 px); ponto 'topo' projetado: {h_pts:.1f} px; 1 unidade local na vertical em M: {uni:.1f} px; "
                       f"3,25 × {uni:.1f} = {3.25 * uni:.1f} px; projeção exata de (0, 0, 3,25): {u325:.1f} px "
                       f"(a diferença entre 3,25 × a unidade e a projeção exata é a perspectiva: a ponta está mais longe da câmera).")
            out.append(f"  conta: altura/unidade = {h_pts / uni:.3f} (perspectiva) · topo projetado × topo no PNG: {abs(h_pts - h_png):.1f} px")
    w(f"alinhamento3d_{R}.txt", f"ALINHAMENTO 3D × MANIM (limite 2 px a 1080p): rótulos pior {pior_g:.2f} px; decolagem/pouso pior {max(0, pior_p):.1f} px além da borda\n"
      + "\n".join(out) + "\n")
    return pior_g, pior_p


def _mascara(tipo):
    m = np.zeros((540, 960), bool)
    if tipo == "A":
        m[66:, :545] = True
    elif tipo == "C760":
        m[66:, :375] = True
    elif tipo == "B43":
        m[360:, :545] = True
    elif tipo == "B52":
        m[66:, 730:] = True
    else:
        m[66:, :] = True
        m[66:120, 760:] = False                        # chip / logo
    return m


def parado():
    from PIL import Image
    sys.path.insert(0, str(U.parents[1]))
    # em fluxo (um quadro por vez): o vídeo inteiro em memória passa de 18 GB
    fundo = np.array(Image.open(str(_fundo())).convert("L").resize((960, 540)), np.int16)
    masks, tipos, par_l, cheio_l, sem, grade_l = {}, [], [], [], [], []
    ultimo = np.full((540, 960), -10 ** 6)
    ant = None
    c = av.open(str(MP4))
    for t, f_ in enumerate(c.decode(video=0)):
        f = f_.to_ndarray(format="gray").astype(np.int16)
        tp = PALCO.get(onde(t / 15)[1], "A")
        tipos.append(tp)
        if tp not in masks:
            masks[tp] = _mascara(tp)
        m = masks[tp]
        if ant is not None:
            ultimo[np.abs(f - ant) > 8] = t
        par_l.append(t >= 45 and np.count_nonzero((ultimo > t - 45) & m) < 40)
        # v2 §7.8: blocos de 60 × 60 a 1080p (30 × 30 aqui) com tinta que não é a grade (a grade fica < 50; tinta > 70)
        tin = (f > 70) & m
        cheia = (f > 46) & m                             # preenchimento de região/célula/placa (≈ 50; a linha da grade fica ≤ 43)
        bl = (tin.reshape(18, 30, 32, 30).sum(axis=(1, 3)) >= 6) | (cheia.reshape(18, 30, 32, 30).sum(axis=(1, 3)) >= 270)
        mb = m.reshape(18, 30, 32, 30).any(axis=(1, 3))
        cheio_l.append(100.0 * np.count_nonzero(bl & mb) / max(1, np.count_nonzero(mb)))
        if t % 15 == 0:                                   # GRADE NA TELA, uma amostra por segundo: blocos de 96 × 90 a 1080p não lisos
            gb = f.reshape(9, 60, 15, 64).max(axis=(1, 3)) >= 24          # blocos de 128 × 120 a 1080p: maior que o maior passo da grade (120 px)
            grade_l.append((t, 100.0 * np.count_nonzero(gb) / gb.size))
        if f[48:62, 18:200].max() < 140:
            sem.append(t)
        ant = f
    c.close()
    N = len(tipos)
    par, cheio = np.array(par_l), np.array(cheio_l)
    runs, i = [], 0
    cta = _cta()
    while i < N:
        if par[i]:
            j = i
            while j + 1 < N and par[j + 1]:
                j += 1
            if i / 15 < cta:
                runs.append((i - 45, j))
            i = j + 1
        else:
            i += 1
    vaz, i = [], 0
    while i < N:
        if cheio[i] < 15.0 and i / 15 < cta:
            j = i
            while j + 1 < N and cheio[j + 1] < 15.0:
                j += 1
            if j - i + 1 > 45:
                vaz.append((i, j))
            i = j + 1
        else:
            i += 1
    grade(grade_l, cta)
    blocos = []
    for k in sem:
        lote, aid, _ = onde(k / 15)
        if lote == "PA" or (lote == "PH" and False):
            continue
        if k / 15 > cta:
            continue
        blocos.append(k)
    linhas = []
    for a, b in runs:
        d = (b - a) / 15
        lote, aid, tl = onde(max(0, a) / 15)
        tag = "> 5 s " if d > 5 else "3–5 s "
        linhas.append(f"{tag} {a / 15:7.2f}–{b / 15:7.2f} s ({d:.1f} s)  {lote}·{aid} (t do lote {tl:.1f} s; palco {PALCO.get(aid, 'A')})")
    mais5 = sum(1 for a, b in runs if (b - a) / 15 > 5)
    w(f"palco_parado_{R}.txt", "PALCO PARADO (máscara do palco por âncora, sem a coluna e sem o canto, a 960×540: A = x < 1090 px a 1080p; B = layout de dois\n"
      "planos e cartões, quadro inteiro; C760 = coluna em x = 760; B43 = faixa de baixo à esquerda do B4-3; B52 = miniaturas do B5-2. Trecho em que\n"
      "menos de 40 px do palco mudam mais de 8 níveis ao longo de 3 s; a duração conta os 3 s da janela; o CTA final fica de fora)\n"
      f"> 5 s: {mais5} · de 3 a 5 s: {len(runs) - mais5}\n" + "\n".join(linhas) + "\n"
      f"\nPALCO VAZIO (v2 §7.8: menos de 15 % dos blocos de 60 × 60 do palco com tinta que não é a grade — traço ou texto: ≥ 6 pixels > 70 de 255; preenchimento: ≥ 30 % do bloco > 46; a linha da grade fica ≤ 43 —"
      f" por mais de 3 s; o CTA fica de fora): {len(vaz)}\n"
      + "".join(f"  {a / 15:7.2f}–{b / 15:7.2f} s ({(b - a + 1) / 15:.1f} s)  {'·'.join(map(str, onde(a / 15)[:2]))} · mínimo {cheio[a:b + 1].min():.1f} %\n"
                for a, b in vaz)
      + f"\nCANTO SEM A LINHA 2 (fora do A1, que não tem canto, e do CTA): {len(blocos)} quadros\n"
      + ("".join(f"  {k / 15:7.2f} s {'·'.join(map(str, onde(k / 15)[:2]))}\n" for k in blocos[:40])))
    return mais5, len(runs) - mais5, len(vaz), len(blocos)


def grade(amostras, cta):
    """v2 §1.5 / §7.2: cobertura da grade na tela inteira, uma amostra por segundo."""
    s2 = re.search(r"\[fundo\] S2 ([\d.]+)", log("PS"))
    t_s2 = ini_lotes().get("PS", 0) / 15 + float(s2.group(1)) - 2.0 if s2 else 1e9    # o t do [fundo] é o do lote, no fim do fade de 1,8 s
    linhas, ok, exc, ruins = [], 0, 0, []
    for q, cob in amostras:
        t = q / 15
        lote, aid, tl = onde(t)
        ex = None
        if t >= cta:
            ex = "CTA (liso)"
        elif t >= t_s2:
            ex = "S2: a grade quadrada some (gancho do S2), liso até o CTA"
        elif lote == "PB4" and aid == "B4-2" and cob < 95:
            ex = "trecho 3D do B4-2 (liso)"
        if ex:
            exc += 1
            continue
        if cob >= 95:
            ok += 1
        else:
            ruins.append(f"  {int(t // 60)}:{t % 60:05.2f} {lote}·{aid} (t do lote {tl:.1f} s): {cob:.1f} %")
    tot = ok + len(ruins)
    w(f"grade_na_tela_{R}.txt", "GRADE NA TELA (v2 §1: papel na tela inteira, 1920 × 1080): uma amostra por segundo do preview; a tela é dividida em 15 × 9\n"
      "blocos (128 × 120 px a 1080p, maior que o maior passo da grade) e um bloco conta como coberto se não é liso (algum pixel ≥ 24 de 255: a linha da grade ou qualquer tinta; o\n"
      "violeta liso fica em 15–18). Aceite: ≥ 95 % em 100 % das amostras fora das exceções (o 3D do B4-2, o S2 depois que a grade quadrada some e o CTA).\n"
      f"AMOSTRAS fora das exceções: {tot} · ≥ 95 %: {ok} ({100.0 * ok / max(1, tot):.1f} %) · abaixo: {len(ruins)} · nas exceções: {exc}\n"
      + "\n".join(ruins) + "\n")
    return ok, len(ruins), exc


def moldura_vazia():
    ls = [(l, x) for l in LOTES for x in re.findall(r"^\[MV\] .*$", log(l), re.M)]
    w(f"moldura_vazia_{R}.txt", "MOLDURA VAZIA (v2 §7.3): RoundedRectangle (moldura, painel, caixa, cartão, selo; Rectangle e SurroundingRectangle são da mesma família)\n"
      "sem nenhum objeto visível com o centro dentro dela por mais de 0,5 s, checado em todo quadro de todo lote (o chip do canto e o papel ficam\n"
      f"de fora). Esperado: 0.\nTOTAL {len(ls)}\n" + "".join(f"  {l}: {x}\n" for l, x in ls))
    return len(ls)


def margem():
    ls = [(l, x) for l in LOTES for x in re.findall(r"^\[MARGEM\] .*$", log(l), re.M)]
    w(f"margem_{R}.txt", "MARGEM (v2 §7.6): objetos visíveis a menos de 48 px da borda do quadro (1080p), checados em todo quadro; fora da conta: o canto,\n"
      f"o logo, o chip do canto e o papel. Cada objeto é listado uma vez (o primeiro quadro em que encosta). Esperado: 0.\nTOTAL {len(ls)}\n"
      + "".join(f"  {l}: {x}\n" for l, x in ls))
    return len(ls)


def tamanho():
    """v2 §6 / §7.4: menor dígito (corpo normal) por coluna e âncora."""
    por, rot = {}, []
    for l in LOTES:
        for m in re.finditer(r"^\[tam\] \S+ (\S+)\s+([\d.]+)s size=(\d+) dig=([\d.]+) x=(\d+) (.*)$", log(l), re.M):
            aid, size, dig, x, tx = m.group(1), int(m.group(3)), float(m.group(4)), int(m.group(5)), m.group(6)
            if tx.lstrip("'").startswith("\\\\Ge{"):             # rótulo GEO do desenho (pedaço da figura, legenda do ponto): não é linha da coluna
                rot.append(f"  {l}·{aid}: {dig:.1f} px (size {size}) {tx[:60]}")
                continue
            k = (l, aid)
            if k not in por or dig < por[k][0]:
                por[k] = (dig, size, x, tx)
    ruins = [(k, v) for k, v in por.items() if v[0] < 26]
    w(f"tamanho_{R}.txt", "TAMANHO (v2 §6 / §7.4): menor altura do dígito em corpo normal nas linhas da coluna (as que crescem por caneta, voo ou glyph map),\n"
      "por âncora, a 1080p. O dígito é medido no '2' do próprio L no tamanho da linha (40 → 26,7 px; 48 → 32,0 px). Os dígitos de índice (limites de\n"
      "integral, expoentes, os 1 e 2 de [ ]₁²) saem no scriptstyle do TeX, ≈ 70 % do corpo, e não entram na conta.\n"
      f"Esperado: ≥ 26 px (≥ 32 px nas linhas-chave). ÂNCORAS: {len(por)} · abaixo de 26 px: {len(ruins)}\n"
      + "".join(f"  {l}·{aid}: {v[0]:.1f} px (size {v[1]}, x = {v[2]}) {v[3][:70]}\n" for (l, aid), v in sorted(por.items(), key=lambda kv: kv[0]))
      + "\nRÓTULOS GEO DO DESENHO (não são linha da coluna; o tamanho segue o desenho, como no v1):\n" + "\n".join(sorted(set(rot))) + "\n")
    return len(ruins)


_TK = re.compile(r"\\(?:X|Y|uu|vv|du|dv|dX|dY|Du|Dv|pu|pv|xu|xv|yu|yv|JJ|Jq|f|veci|veck|sen|cos|int|iint|sum|det|partial|alpha|varphi|wedge|cdot|times|"
                 r"Rightarrow|to|le|neq|cong|approx|infty|theta|pi)(?![A-Za-z])|[A-Za-z0-9]|[+\-=()|<>,/^_]")


def _tokens(tx):
    tx = re.sub(r"\\(?:Uc|Vc|Co|Az|Lm|Ci|Am|Mg|Ge|Al|Ce|Cu|Rb)\{", "{", tx)
    tx = re.sub(r"\\(?:dfrac|frac|left|right|Big|big|qquad|quad|operatorname|begin|end|bmatrix|text)", " ", tx)
    tx = re.sub(r"\[[^\]]*\]$", "", tx.strip())
    return _TK.findall(tx)


def derivada():
    """v2 §7.5: como cada linha da coluna nasceu (mapa, voo, caneta) e a fração de glifos herdados da linha de cima."""
    import ast
    out, ruins, n = [], [], 0
    for l in LOTES:
        ant, vistos = None, {}
        col_tx = set()                                   # só as linhas da coluna (Lp, as que gravam [tam]); rótulos do desenho e textos ficam de fora
        for mt in re.finditer(r"^\[tam\] .* x=\d+ (.*)$", log(l), re.M):
            try:
                col_tx.add(re.sub(r" \[[^\]]*\]$", "", ast.literal_eval(mt.group(1)))[:55])
            except Exception:
                pass
        for m in re.finditer(r"^\[linha\] \S+ (\S+)\s+([\d.]+)s (\S+) (.*)$", log(l), re.M):
            aid, t, como, tx = m.group(1), float(m.group(2)), m.group(3), m.group(4)
            try:
                tx = ast.literal_eval(tx)
            except Exception:
                pass
            base = re.sub(r" \[[^\]]*\]$", "", tx)
            parte = base != tx
            if base[:55] not in col_tx or base.startswith("\\Ge{"):       # rótulos GEO do desenho não são linha da coluna
                continue
            if base in vistos:
                vistos[base].add(como if not parte else ("caneta parcial" if como == "pena" else como))
                continue
            vistos[base] = {como if not parte else ("caneta parcial" if como == "pena" else como)}
            n += 1
            tk, ta = _tokens(base), (_tokens(ant) if ant else [])
            her = 0
            if ta:
                pool = list(ta)
                for x in tk:
                    if x in pool:
                        pool.remove(x)
                        her += 1
            fr = 100.0 * her / max(1, len(tk))
            if como == "gm":
                nasc = "mapa"
            elif como == "voo" or parte:
                nasc = "voo + caneta"
            else:
                nasc = "caneta"
            flag = nasc == "caneta" and fr > 50 and len(tk) >= 4
            if flag:
                ruins.append(f"{l}·{aid} {t:.2f}s {base[:70]}")
            out.append(f"  {l}·{aid} {t:7.2f}s {nasc:13s} herdados {fr:5.1f} %{'  ← CANETA COM > 50 % HERDADO' if flag else ''}  {base[:80]}")
            ant = base
    w(f"linha_derivada_{R}.txt", "LINHA DERIVADA (v2 §4 / §7.5): cada linha da coluna, na ordem em que nasce, com o modo (mapa = TransformByGlyphMap de uma\n"
      "cópia da linha de cima ou do degrau anterior; voo + caneta = termos que voam do desenho ou da linha de cima e o resto a caneta; caneta = tudo\n"
      "novo) e a fração dos símbolos dela que já estavam na linha de cima (a linha anterior na ordem do log; contagem por símbolo do LaTeX, sem\n"
      "cores e sem espaçamentos; linhas de < 4 símbolos não contam). Esperado: nenhuma linha a caneta com > 50 % de herdados.\n"
      f"LINHAS: {n} · CANETA COM > 50 % HERDADO: {len(ruins)}\n" + "".join(f"  {r}\n" for r in ruins) + "\nTODAS:\n" + "\n".join(out) + "\n")
    return len(ruins)


def finais():
    """handoff final §7: DUPLICADOS (K3), CONTORNO (K3), ÓRFÃOS (K5), LEGIBILIDADE (K4/K10/K12), VOO × TRAÇO por voo, CANTO, HOLDS."""
    res = {}
    for tag, nome, desc in (("DUP", "duplicados_por_quadro", "DUPLICADOS (K3): em todo quadro, dois glifos com a mesma forma (mesmo nº de pontos, tamanho ± 10 %), de "
                             "textos diferentes, com centros a menos de 1/3 do tamanho e ≥ 1,5 px (a cópia exatamente sobre a fonte, que some em fade no lugar, "
                             "não se vê), por mais de 2 quadros seguidos (os 2 primeiros quadros de cada voo ficam de fora)."),
                            ("CONTORNO", "contorno_pouso", "CONTORNO DEPOIS DO POUSO (K3): glifo parado (nem sendo escrito nem voando há 0,2 s) com contorno > 0,5 px."),
                            ("ORFAO", "orfaos", "ÓRFÃOS (K5): objeto de topo visível < 40 × 40 px, só de glifos, que não é rótulo/tique/vértice nem glifo de linha da "
                             "coluna nem termo em voo, por mais de 0,3 s."),
                            ("LEG", "legibilidade_mapas", "LEGIBILIDADE (K4, K10, K12): em todo quadro (glyph maps, voos e trocas de página), glifos de textos "
                             "diferentes e de forma diferente sobrepostos em mais de 30 % da menor caixa por mais de 0,3 s. Os buracos do K4(b) fecham na mesma "
                             "linha logo depois de os pares saírem (sem buraco aberto > 0,6 s por construção).")):
        ls = [(l, x) for l in LOTES for x in re.findall(rf"^\[{tag}\] .*$", log(l), re.M)]
        res[tag] = len(ls)
        w(f"{nome}_{R}.txt", f"{desc}\nTOTAL {len(ls)}\n" + "".join(f"  {l}: {x}\n" for l, x in ls))
    # voo × traço: amostras R5V agrupadas por voo (o mesmo texto em quadros seguidos) → duração de cada travessia
    out, ruins = [], 0
    for l in LOTES:
        ev = [(m.group(1), float(m.group(2)), m.group(3)) for m in re.finditer(r"^\[R5V\] (\S+)\s+([\d.]+)s '(.*?)' atravessa", log(l), re.M)]
        grupos = []
        for aid, t, tx in ev:
            if grupos and grupos[-1][0] == aid and grupos[-1][2] == tx and t - grupos[-1][3] <= 0.08:
                grupos[-1][3] = t
            else:
                grupos.append([aid, t, tx, t])
        for aid, t0, tx, t1 in grupos:
            d = t1 - t0 + 1 / 15
            if d > 0.2:
                ruins += 1
            out.append(f"  {l}·{aid} {t0:7.2f}s {d:.2f} s {'> 0,2 s' if d > 0.2 else 'ok'}  {tx[:60]}")
    res["VOOTRACO"] = ruins
    w(f"voo_traco_{R}.txt", "VOO × TRAÇO DO DESENHO (K3): cada voo que passa por cima de um traço (eixo, aresta, borda de região), com a duração da "
      f"travessia; limite 0,2 s por voo. Voos acima do limite: {ruins}\n" + "\n".join(out) + "\n")
    # canto: a troca da linha 2 cai no 1º play da âncora (mesmo instante do [ancora]); quadros com canto de outra âncora
    out, ruins = [], 0
    for l in LOTES:
        anc = {m.group(1): float(m.group(2)) for m in re.finditer(r"^\[ancora\] (\S+) ([\d.]+)", log(l), re.M)}
        anc.update({m.group(1): float(m.group(2)) for m in re.finditer(r"^\[ancora-real\] (\S+) ([\d.]+)", log(l), re.M)})
        for m in re.finditer(r"^\[canto\] (\S+) ([\d.]+) (.*)$", log(l), re.M):
            aid, t, txt = m.group(1), float(m.group(2)), m.group(3)
            dt = t - anc.get(aid, t)
            q = round(dt * 15)
            if q > 0:
                ruins += q
            out.append(f"  {l}·{aid}: troca em {t:.2f} s (âncora em {anc.get(aid, float('nan')):.2f} s; {q} quadro(s) de atraso) → {txt}")
    res["CANTO"] = ruins
    w(f"canto_{R}.txt", "CANTO (K1, K9): a linha 2 do canto troca no 1º play de cada âncora (troca seca, no mesmo quadro do início da âncora); "
      f"quadros com o canto de outra âncora: {ruins}\n" + "\n".join(out) + "\n")
    # holds
    hs = [x for l in LOTES for x in re.findall(r"^\[hold\] .*$", log(l), re.M)]
    hs += [x for l in LOTES for x in re.findall(r"^\[zoom\] .*$", log(l), re.M)] + [x for l in LOTES for x in re.findall(r"^\[k8\] .*$", log(l), re.M)]
    hs += [x for l in LOTES for x in re.findall(r"^\[k15\] .*$", log(l), re.M)]
    w(f"holds_{R}.txt", "HOLDS E MEDIDAS DOS ITENS K: C18.8 ✓ ≥ 2,0 s (K9) · 8/3 ≥ 2,5 s (K10) · zoom × MNPQ ≤ 2 px (K6) · planos do B5-3 (K8) · células do S2 (K15)\n"
      + "\n".join(hs) + "\n")
    return res


def _fundo():
    from assets.calculo.papel import _arq
    return _arq()


def _cta():
    ini = ini_lotes().get("PS", 0) / 15
    m = re.search(r"\[cta\] ([\d.]+)", log("PS"))
    return ini + float(m.group(1)) if m else 1e9


def texto():
    src = "\n".join((U / f).read_text(encoding="utf-8") for f in SECS[:12])
    tx = re.findall(r"\\text\{([^}]*)\}", src)
    ruins = sorted({t for t in tx if len(t.split()) > 1})
    ntf = len(re.findall(r"tfrac", src))
    w(f"texto_em_mathtex_{R}.txt", f"\\text{{…}} EM MATHTEX COM MAIS DE UMA PALAVRA (seções + j36.py): {len(ruins)}\n" + "".join(f"  {t!r}\n" for t in ruins)
      + "Todos os \\text{} das seções: " + (", ".join(sorted({repr(t) for t in tx})) or "nenhum") + "\n"
      + f"grep -n tfrac (seções + j36.py): {ntf}\n"
      "Frase portuguesa: sempre Space Grotesk (T/leg/mixl/rotm/mixLp, linhas mistas Text + MathTex com respiro ≥ 14 px): ÁREA, ARCO, CAIXA:, CÉLULA,\n"
      "COMPRIMENTO, PRIMITIVA EM, CONFERE:, PLANO, PAPEL:, DETERMINAR, COM, DE CLASSE, NO ABERTO, INVERSÍVEL NO INTERIOR DE, NO INTERIOR DE,\n"
      "INTEGRÁVEL EM, CONSTANTE, CONGELADO, LADO, EXATA, RAZÃO, JACOBIANO, LATITUDE, ENTRADA, SAÍDA, = O JACOBIANO, ALTURA = ÁREA DO PARALELOGRAMO.\n")
    return len(ruins), ntf


def glyph():
    gms = [ln for l in LOTES for ln in re.findall(r"^\[gm\] .*$", log(l), re.M)]
    v1 = [ln for l in LOTES for ln in re.findall(r"^\[voo1\] .*$", log(l), re.M)]
    out = [f"GLYPH MAPS (TransformByGlyphMap do MF-Tools 1.4.9, MathTex de string única, mapa explícito; auto_fade só para o glifo que SAI; o glifo que"
           f" ENTRA fica apagado no mapa e depois voa da fonte ou é escrito pela caneta): {len(gms)} passos"]
    for k in range(1, 18):
        n = sum(1 for g in gms if re.search(rf"pares=\d+ C?{k}[b ]", g))
        out.append(f"  mapa {k:2d}: {n} passo(s)")
    out += ["", "TODOS OS PASSOS (lote, âncora, t do lote em s, nº de pares, mapa, origem → destino):"] + ["  " + g for g in gms]
    out += ["", f"PASSOS DE UM PAR SÓ (origem: o termo voa da linha anterior; não é manipulação): {len(v1)}"] + ["  " + g for g in v1]
    src = "\n".join((U / f).read_text(encoding="utf-8") for f in SECS)
    out.append(f"\ngrep 'from MF_Tools': {len(re.findall('from MF_Tools', src))} · função própria de mapa de glifos (def mapa_glifos): "
               f"{len(re.findall('def mapa_glifos', src))}")
    out.append("Linha órfã começando por '=': 0 — toda linha '= …' é continuação, logo abaixo da linha de que é passo, na mesma coluna e na tela junto dela.")
    w(f"glyph_maps_{R}.txt", "\n".join(out) + "\n")
    return len(gms)


def tempos():
    out = []
    for l in LOTES:
        r = re.search(r"\[render\] \S+ (\d+)s", log(l))
        t3 = U / f"tempo3d_{l}.txt"
        d = re.findall(r"\[tempo\] total ([\d.]+)s", log(l))
        j3 = re.findall(r"\{\"lote\".*\}", log(l, "log_3d_"))
        out.append(f"{l}: duração {float(d[-1]) if d else 0:.1f} s · render Manim {r.group(1) if r else '?'} s"
                   + (f" · 3D: {j3[-1]} ({t3.read_text(encoding='utf-8').strip()})" if j3 else " · sem 3D"))
    w(f"tempos_render_{R}.txt", "TEMPO DE RENDER POR BLOCO (960×540, 15 fps; só registro). 3D: renderizados = quadros únicos (estados repetidos viram cópia),\n"
      "s_por_quadro = custo do three.js por quadro único (Chrome + WebGL d3d11).\n" + "\n".join(out) + "\n")


def cartao():
    m = re.search(r"\[cartao\] \S+ sai [\d.]+ \(([\d.]+) s na tela\)", log("PS"))
    p = re.findall(r"\[pausa\] (\S+) ([\d.]+) (entra|sai)", log("PB7"))
    txt = ""
    d = None
    if m:
        d = float(m.group(1))
        txt += f"CARTÃO DO PRÓXIMO VÍDEO: {d:.2f} s na tela antes do CTA ({'OK' if d >= 8 else 'CURTO'}; o CTA entra depois, sem sobrepor)\n"
    if len(p) >= 2:
        dp = float(p[1][1]) - float(p[0][1])
        txt += f"PAUSE E TENTE (B7): entra {p[0][1]} s, sai {p[1][1]} s do lote: {dp:.2f} s na tela ({'OK' if dp >= 3 else 'CURTO'})\n"
    w(f"cartao_{R}.txt", txt)
    return d


if __name__ == "__main__":
    QA.mkdir(parents=True, exist_ok=True)
    print("R5 (R5, R5V)", r5())
    print("moldura vazia", moldura_vazia())
    print("margem", margem())
    print("tamanho < 26 px", tamanho())
    print("linha derivada (caneta > 50 %)", derivada())
    print("finais", finais())
    print("flash", flash())
    print("alinhamento", alinhamento())
    print("texto", texto())
    print("glyph", glyph())
    tempos()
    print("cartao", cartao())
    if MP4.exists():
        print("parado (>5, 3-5, vazio, canto)", parado())
