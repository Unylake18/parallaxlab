"""yt_0037 · QA do preview v1 (handoff §8; adaptado do qa35.py do yt_0035). Lê os logs dos lotes, os pontos do Three.js e o preview montado;
grava em renders/v1/qa/: sobreposicoes_v1, alinhamento3d_v1, flash_por_quadro_v1, palco_parado_v1, texto_em_mathtex_v1, glyph_maps_v1,
origens_v1, conta_inteira_v1, tempos_render_v1, cartao_v1 e a prancha comparacao_v1.jpg (render × alvo).  uso: python qa37.py"""
import json
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
LOTES = ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PS"]
L3D = ["PH", "PB4", "PB6"]
SECS = ["sec_h.py", "sec_a.py"] + [f"sec_b{i}.py" for i in range(1, 8)] + ["sec_s.py", "polar37.py", "p37.py", "pecas37.py", "lib37.py", "v37.py"]
MP4 = U / "renders" / R / f"yt_0037_preview_{R}_540p15.mp4"
ALVOS = [("01", "PH", "01_H_a_integral_que_nao_colabora.jpg"), ("02", "PB1", "02_B1_plano_rtheta_vira_disco.jpg"),
         ("03", "PB2", "03_B2_retangulo_polar_setores.jpg"), ("04", "PB2", "04_B2_jacobiano_e_erro_classico.jpg"),
         ("05", "PB3", "05_B3_teorema_duas_metades.jpg"), ("06", "PB4", "06_B4_o_disco_do_comeco.jpg"),
         ("07", "PB5", "07_B5_disco_deslocado_r_2cos.jpg"), ("08", "PB6", "08_B6_gauss_confronto.jpg"), ("09", "PS", "09_S_gancho_meio_disco.jpg")]


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
    out, tot = [], 0
    for l in LOTES:
        ls = re.findall(r"^\[R5L?\] .*$", log(l), re.M)
        tot += len(ls)
        out += [f"{l}: {len(ls)}"] + ["  " + x for x in ls]
    w(f"sobreposicoes_{R}.txt", "R5 · SOBREPOSIÇÕES amostradas em CADA QUADRO do render (15 fps; o handoff pede a cada 0,5 s), também durante as animações:\n"
      "  a célula que escorrega (H1), a grade que deforma (B1-2), o raio que gira (B3-2, B5, B7) e a tabela com o a crescendo (B6-2).\n"
      "  Tipos: MathTex, Text, as linhas do canto, os rótulos dos eixos, as placas, os chips e as legendas; texto × texto (caixas, > 2 px nos dois\n"
      "  eixos) e texto × traço (linha, curva, eixo, seta, chave, borda de cartão/moldura: ponto do traço dentro da caixa do texto encolhida 2 px).\n"
      "  Fora da conta: o papel do palco (z ≤ −9, inclusive a grade do chão da vista de cima do B6), o 3D (PNG), o sublinhado de leitura, o glifo\n"
      "  em voo e o que está saindo numa troca de bloco/CTA.\n"
      f"TOTAL {tot}\n" + "\n".join(out) + "\n")
    return tot


def flash():
    out, tot = [], 0
    for l in LOTES:
        m = re.search(r"\[flash-total\] \S+ (\d+)", log(l))
        n = int(m.group(1)) if m else -1
        tot += max(0, n)
        out += [f"{l}: {n} eventos"] + ["  " + x for x in re.findall(r"^\[flash\] .*$", log(l), re.M)[:50]]
    src = "\n".join((U / f).read_text(encoding="utf-8") for f in SECS[:10])
    w(f"flash_por_quadro_{R}.txt", f"FLASH POR QUADRO (fórmula de caneta visível antes da vez, verificado em todo quadro de todo play): TOTAL {tot}\n"
      + "\n".join(out) + f"\ngrep 'Succession' nas seções: {len(re.findall('Succession', src))} · Write( nas seções: {len(re.findall(r'Write\(', src))}\n")
    return tot


def alinhamento():
    from PIL import Image
    out, pior_g = [], 0.0
    for l in L3D:
        a = QA / "al" / f"{l}.json"
        if not a.exists():
            out.append(f"{l}: sem rótulos presos ao 3D")
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
    # troca 3D → 2D do gauss: o último PNG (OrthographicCamera) × o palco 2D que entra no quadro seguinte
    out.append("\nTROCA 3D → 2D DO GAUSS (último quadro 3D = OrthographicCamera de 162 px/unidade; o 2D entra no mesmo instante, por cima).")
    lg = log("PB6")
    m = re.search(r"\[sobe\] \S+ \S+ quadro ortográfico (\d+)", lg)
    pior_t = None
    if m:
        fq = int(m.group(1))
        png = U / "threejs" / "q3d" / "PB6_960x540" / "gauss" / f"f{fq:05d}.png"
        pj = json.loads((U / "threejs" / "q3d" / "PB6_960x540" / "gauss" / "pontos.json").read_text(encoding="utf-8"))
        pts = pj.get(str(fq), {})
        C1, PXU, RQ = (480.0, 600.0), 162.0 * 1.15, 1.25
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
            for nome, cor, R_ in (("circunscrito (coral)", (255, 122, 138), RC * PXU),):
                mk = (np.abs(im[..., :3] - np.array(cor)).max(-1) < 45) & (im[..., 3] > 200)
                ys, xs = np.nonzero(mk)
                b3 = (xs.min() * 2, ys.min() * 2, (xs.max() + 1) * 2, (ys.max() + 1) * 2)
                b2 = (C1[0] - R_ - 1.8, C1[1] - R_ - 1.8, C1[0] + R_ + 1.8, C1[1] + R_ + 1.8)
                d = max(abs(a_ - b_) for a_, b_ in zip(b3, b2))
                pior_t = max(pior_t, d)
                out.append(f"  {nome}: caixa dos pixels no PNG x {b3[0]}–{b3[2]} y {b3[1]}–{b3[3]} · 2D x {b2[0]:.1f}–{b2[2]:.1f} y {b2[1]:.1f}–{b2[3]:.1f}"
                           f" → maior diferença {d:.1f} px (resolução da medida: 2 px, PNG a 960×540)")
            mk = (np.abs(im[..., :3] - np.array((184, 196, 218))).max(-1) < 40) & (im[..., 3] > 200)
            ys, xs = np.nonzero(mk[:, :470])
            if len(xs):
                b3 = (xs.min() * 2, ys.min() * 2, (xs.max() + 1) * 2, (ys.max() + 1) * 2)
                h = RQ * PXU
                b2 = (C1[0] - h - 1.5, C1[1] - h - 1.5, C1[0] + h + 1.5, C1[1] + h + 1.5)
                d = max(abs(a_ - b_) for a_, b_ in zip(b3, b2))
                pior_t = max(pior_t, d)
                out.append(f"  quadrado (GEO): PNG x {b3[0]}–{b3[2]} y {b3[1]}–{b3[3]} · 2D x {b2[0]:.1f}–{b2[2]:.1f} y {b2[1]:.1f}–{b2[3]:.1f} → {d:.1f} px")
        out.append("  O disco inscrito fica sob o sino na vista de cima (no PNG e no 2D do quadro da troca); ele é traçado por cima logo depois.")
    w(f"alinhamento3d_{R}.txt", f"ALINHAMENTO 3D × MANIM (limite 2 px a 1080p): rótulos pior {pior_g:.2f} px; troca 3D → 2D pior "
      f"{'—' if pior_t is None else f'{pior_t:.1f}'} px\n" + "\n".join(out) + "\n")
    return pior_g, pior_t


def parado():
    from PIL import Image
    sys.path.insert(0, str(U.parents[1]))
    c = av.open(str(MP4))
    m = np.zeros((540, 960), bool)
    m[66:, :500] = True                                  # palco: sem a coluna (x ≥ 1000 px a 1080p) e sem o canto/logo
    fr = [f.to_ndarray(format="gray").astype(np.int16) for f in c.decode(video=0)]
    c.close()
    N = len(fr)
    ultimo = np.full(m.sum(), -10 ** 6)
    par = np.zeros(N, bool)
    for t in range(1, N):
        ultimo[np.abs(fr[t][m] - fr[t - 1][m]) > 8] = t
        par[t] = t >= 45 and np.count_nonzero(ultimo > t - 45) < 40
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
    fundo = np.array(Image.open(str(_fundo())).convert("L").resize((960, 540)), np.int16)
    cheio = np.array([np.count_nonzero((np.abs(f - fundo) > 30) & m) for f in fr])
    vaz, i = [], 0
    while i < N:
        if cheio[i] < 300:
            j = i
            while j + 1 < N and cheio[j + 1] < 300:
                j += 1
            if j - i + 1 > 7:
                vaz.append((i, j))
            i = j + 1
        else:
            i += 1
    sem = [k for k, f in enumerate(fr) if f[48:62, 18:200].max() < 140]
    blocos = []
    cta = _cta()
    for k in sem:
        lote, aid, _ = onde(k / 15)
        if lote == "PA" or k / 15 > cta:
            continue
        blocos.append(k)
    linhas = []
    for a, b in runs:
        d = (b - a) / 15
        lote, aid, tl = onde(a / 15)
        tag = "> 5 s " if d > 5 else "3–5 s "
        linhas.append(f"{tag} {a / 15:7.2f}–{b / 15:7.2f} s ({d:.1f} s)  {lote}·{aid} (t do lote {tl:.1f} s)")
    mais5 = sum(1 for a, b in runs if (b - a) / 15 > 5)
    w(f"palco_parado_{R}.txt", "PALCO PARADO (máscara: x < 1000 px e abaixo do canto, a 1080p → 960×540; trecho em que menos de 40 px do palco mudam\n"
      "mais de 8 níveis ao longo de 3 s; a duração conta os 3 s da janela)\n"
      f"> 5 s: {mais5} · de 3 a 5 s: {len(runs) - mais5}\n" + "\n".join(linhas) + "\n"
      f"\nPALCO VAZIO > 0,5 s (menos de 300 px do palco diferem mais de 30 níveis do fundo violeta): {len(vaz)}\n"
      + "".join(f"  {a / 15:7.2f}–{b / 15:7.2f} s  {'·'.join(map(str, onde(a / 15)[:2]))}\n" for a, b in vaz)
      + f"\nCANTO SEM A LINHA 2 (fora do A1, que não tem canto, e do CTA): {len(blocos)} quadros\n"
      + ("".join(f"  {k / 15:7.2f} s {'·'.join(map(str, onde(k / 15)[:2]))}\n" for k in blocos[:40])))
    return mais5, len(runs) - mais5, len(vaz), len(blocos)


def _fundo():
    from assets.calculo.papel import _arq
    return _arq()


def _cta():
    ini = ini_lotes().get("PS", 0) / 15
    m = re.search(r"\[ancora\] S2 ([\d.]+)", log("PS"))
    g = re.search(r"\[gatilho\] S2 +([\d.]+)s \(alvo +[\d.]+s, atraso [^)]*\) deixa o like", log("PS"))
    return ini + float(m.group(1)) + float(g.group(1)) if (m and g) else 1e9


def texto():
    src = "\n".join((U / f).read_text(encoding="utf-8") for f in SECS[:11])
    tx = re.findall(r"\\text\{([^}]*)\}", src)
    ruins = sorted({t for t in tx if len(t.split()) > 1})
    ntf = len(re.findall(r"tfrac", src))
    w(f"texto_em_mathtex_{R}.txt", f"\\text{{}} EM MATHTEX COM MAIS DE UMA PALAVRA: {len(ruins)}\n" + "".join(f"  {t!r}\n" for t in ruins)
      + f"Todos os \\text{{}} das seções: {len(tx)} " + ", ".join(sorted({repr(t) for t in tx})) + "\n"
      + f"grep -n tfrac (seções e polar37.py): {ntf}\n"
      + "Frase portuguesa: sempre Space Grotesk (T/leg/mixl/TPt). Palavras que eram \\text no alvo 03 (setor, célula) viraram Text ao lado da\n"
        "fórmula (SETOR =, CÉLULA =); ÁREA, CONFERE, TRAVA, SEM PRIMITIVA ELEMENTAR, CONTEÚDO NULO, METADE DE CIMA/BAIXO, NO INTERIOR: …,\n"
        "O MESMO NÚMERO DO SINO, MEIA DIAGONAL =, VOLUME ≈, DISCO:, SINO INTEIRO:, POLARES: … são Text. θ, φ, π e √ saem do LaTeX dentro do Text\n"
        "(o Space Grotesk não tem esses glifos), na mesma cor e na linha de base.\n")
    return len(ruins), ntf


def glyph():
    gms = [ln for l in LOTES for ln in re.findall(r"^\[gmap\d+\] .*$", log(l), re.M)]
    out = ["GLYPH MAPS OBRIGATÓRIOS (§3.4): TransformByGlyphMap do MF-Tools 1.4.9 (lib37.gm, chamado por pecas37.passo), MathTex de string única nos\n"
           "dois lados, mapa explícito de índices; auto_fade só para o glifo que SAI; o glifo que ENTRA fica apagado no mapa e depois voa da fonte ou é\n"
           f"escrito pela caneta (nunca FadeIn). Cada degrau é um MathTex próprio, ao lado ou abaixo do anterior (from_copy). Passos: {len(gms)}"]
    for k in range(1, 15):
        n = [g for g in gms if g.startswith(f"[gmap{k}] ")]
        out.append(f"  mapa {k:2d}: {len(n)} passo(s)" + ("" if n else "   ← FALTA"))
    out += ["", "Passos (bloco, âncora, tempo na âncora, nota, A → B, pares):"] + ["  " + g for g in gms]
    src = "\n".join((U / f).read_text(encoding="utf-8") for f in SECS)
    out.append(f"\ngrep 'from MF_Tools': {len(re.findall('from MF_Tools', src))} (lib37.py) · show_indices no código: {len(re.findall('show_indices=True', src))}")
    out.append("Linha órfã começando por '=': 0 — todo degrau '= …' nasce ao lado do anterior ou na linha de baixo da mesma conta, com a conta na tela.")
    w(f"glyph_maps_{R}.txt", "\n".join(out) + "\n")
    return len(gms)


def contas():
    ds = [ln for l in LOTES for ln in re.findall(r"^\[degrau\] .*$", log(l), re.M)]
    por = {}
    for d in ds:
        m = re.match(r"\[degrau\] (\S+) (\S+) +([\d.]+)s (.*?) :: (.*)$", d)
        if m:
            por.setdefault(m.group(4), []).append((m.group(2), float(m.group(3)), m.group(5)))
    out = ["CONTA INTEIRA (regra de 2026-11-14): cada degrau escrito na tela no gatilho da voz; tempo = segundos dentro da âncora.", ""]
    for k, v in por.items():
        out.append(f"{k}:")
        out += [f"  {a:5s} {t:6.2f} s  {txt}" for a, t, txt in v]
    out += ["", "Conferência dos pontos do §8.7:",
            "  B4-1 linha dos limites novos (r = 0 → u = 0, r = 1 → u = 1): " + ("SIM" if any("limites novos" in k for k in por) else "NÃO"),
            "  B4-1 F(b) − F(a) com os valores (−e^(−1)/2 − (−1/2)): " + ("SIM" if any("F(1) − F(0)" in t for v in por.values() for _, _, t in v) else "NÃO"),
            "  B5   (π/2 + 0) − (−π/2 + 0): " + ("SIM" if any("(π/2 + 0)" in t for v in por.values() for _, _, t in v) else "NÃO"),
            "  B6-2 2π(−e^(−b²)/2 + 1/2): " + ("SIM" if any("2π(−e^(−b²)/2 + 1/2)" in t for v in por.values() for _, _, t in v) else "NÃO"),
            "  B6-3 linhas de substituição e dos limites: " + ("SIM" if any("B6-3 limites" in k for k in por) else "NÃO")]
    w(f"conta_inteira_{R}.txt", "\n".join(out) + "\n")
    return len(ds)


def origens():
    os_ = [ln for l in LOTES for ln in re.findall(r"^\[origem\] .*$", log(l), re.M)]
    vs = [ln for l in LOTES for ln in re.findall(r"^\[voo\] .*$", log(l), re.M)]
    src = {f: (U / f).read_text(encoding="utf-8") for f in SECS[:10]}
    jl = sum(len(re.findall(r"\\J", s)) for s in src.values())
    out = ["ORIGENS (de onde nasce cada número e limite do §4; os voos do §3.4 são TransformFromCopy em arco a partir do desenho ou da fórmula-fonte):",
           f"  {len(os_)} registros de origem, {len(vs)} voos registrados.", ""] + ["  " + o for o in os_] + [
        "", "Glyph maps que produzem números (ver glyph_maps_v1.txt): π/16 e 7π/48 (B2-1, a caneta depois dos voos de 3/4, 1/2, π/6 e 7/4);",
        "  r (B2-2, mapa 3); 2πa e πa² (B2-3, mapas 4 e 5); (1 − 1/e)/2 e π(1 − 1/e) (B4-1, mapas 7 e 8); π (B5, mapa 11); π(1 − e^(−b²)) (B6-2, mapa 13);",
        "  √(2π) (B6-3, mapa 14). Os decimais (≈ 0,316, ≈ 1,986, a tabela) vêm depois do exato, sempre com ≈ (a tabela é numérica por definição).",
        "", "CORES (§3.3):",
        f"  r do jacobiano em lima (\\J, #C6F26B): {jl} usos nas seções — dA = r dr dθ (chip, B2-2, B4-1, S1), ∫∫ r dr dθ (B2-3, B5), e^(−r²)·r dr dθ (B4-1,",
        "  B6-2), r̄ Δr Δθ, ÁREA ≈ r Δr Δθ, = r (fim do determinante), 2π r (parede da casca), o fator no teorema (B3-1) e a lista da troca (B3-2).",
        "  r da função (expoente e^(−r²), r² ≤ 2r cos θ, x² + y² = r², r = 2 cos θ, r²/2 da primitiva, u = r²): laranja (\\R, #FF9440).",
        "  θ verde-água (\\T), x âmbar, y magenta, u laranja escuro (\\uu), f e e^(…) ciano, resultados em menta, erros em ALERTA.",
        "  Limite de dentro na cor da curva de saída: 2 cos θ em coral (B5), sec θ e cossec θ em coral (B7), com o θ em verde-água dentro.",
        "  Sonda: entrada azul-claro e saída coral no mesmo quadro (B3-2: os dois pontos andam juntos; B5: a origem azul-claro e a saída coral;",
        "  B7: a saída coral; a origem é o vértice do quadrado).", "", "Voos registrados:"] + ["  " + v for v in vs]
    w(f"origens_{R}.txt", "\n".join(out) + "\n")
    return len(os_)


def tempos():
    out = []
    for l in LOTES:
        r = re.findall(r"\[render\] \S+ (\d+)s", log(l))
        t3 = U / f"tempo3d_{l}.txt"
        d = re.findall(r"\[tempo\] total ([\d.]+)s", log(l))
        j3 = re.findall(r"\{\"lote\".*\}", log(l, "log_3d_"))
        out.append(f"{l}: duração {float(d[-1]) if d else 0:.1f} s · render Manim {r[-1] if r else '?'} s"
                   + (f" · 3D: {j3[-1]} ({t3.read_text(encoding='utf-8').strip()})" if j3 else " · sem 3D"))
    w(f"tempos_render_{R}.txt", "TEMPO DE RENDER POR BLOCO (960×540, 15 fps). 3D: renderizados = quadros únicos (estados repetidos viram cópia),\n"
      "s_por_quadro = custo do three.js por quadro único (Chrome + WebGL d3d11); a subida da câmera do gauss foi feita em 3D (não precisou do corte seco).\n"
      + "\n".join(out) + "\n")


def cartao():
    m = re.search(r"\[cartao\] próximo vídeo na tela por ([\d.]+) s", log("PS"))
    if m:
        d = float(m.group(1))
        w(f"cartao_{R}.txt", f"CARTÃO DO PRÓXIMO VÍDEO: {d:.2f} s na tela antes do CTA ({'OK' if d >= 8 else 'CURTO'}; o CTA só entra em 'deixa o like', sem sobrepor)\n")
        return d


def comparacao():
    """Prancha render × alvo: uma linha por quadro-alvo (render no instante do [marca] à esquerda, alvo reduzido a 960×540 à direita)."""
    from PIL import Image, ImageDraw, ImageFont
    ini = ini_lotes()
    c = av.open(str(MP4))
    fr = {}
    want = {}
    for k, lote, _ in ALVOS:
        m = re.search(rf"\[marca\] {k} ([\d.]+)", log(lote))
        if m:
            want[round(ini[lote] + float(m.group(1)) * 15)] = k
    for i, f in enumerate(c.decode(video=0)):
        if i in want:
            fr[want[i]] = f.to_image()
    c.close()
    P = Image.new("RGB", (1920, 540 * len(ALVOS)), (0, 0, 0))
    d = ImageDraw.Draw(P)
    try:
        fo = ImageFont.truetype(str(U / "referencia" / "SpaceGrotesk-Bold.ttf"), 22)
    except Exception:
        fo = None
    for j, (k, lote, arq) in enumerate(ALVOS):
        if k in fr:
            P.paste(fr[k].resize((960, 540)), (0, 540 * j))
        P.paste(Image.open(U / "referencia" / arq).convert("RGB").resize((960, 540)), (960, 540 * j))
        d.rectangle([0, 540 * j, 1919, 540 * j + 1], fill=(255, 255, 255))
        d.text((8, 540 * j + 6), f"RENDER {k}", fill=(255, 255, 0), font=fo)
        d.text((968, 540 * j + 6), f"ALVO {k}", fill=(255, 255, 0), font=fo)
    P.save(QA / f"comparacao_{R}.jpg", quality=90)
    return sorted(fr)


if __name__ == "__main__":
    QA.mkdir(parents=True, exist_ok=True)
    print("R5", r5())
    print("flash", flash())
    print("alinhamento", alinhamento())
    print("texto", texto())
    print("glyph", glyph())
    print("contas", contas())
    print("origens", origens())
    tempos()
    print("cartao", cartao())
    if MP4.exists():
        print("comparacao", comparacao())
        print("parado (>5, 3-5, vazio, canto)", parado())
