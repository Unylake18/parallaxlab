"""yt_0034 · QA extra do preview v3 (handoff v3 §9): CONTAS (cada degrau com o tempo e a frase que o dispara), aberturas, glyph maps a 50 %,
gancho, áreas das fatias (valores), durações por âncora × tabela do §7. Lê os logs dos lotes, renders/v3/lotes_v3.json e o preview montado.
uso: python qa_v3.py  →  renders/v3/qa/contas_v3.txt, aberturas_v3.jpg/.txt, glyph_maps_meio_v3.jpg, gancho_v3.jpg, areas_v3.txt, duracoes_v3.txt"""
import json
import os
import math
import re
from pathlib import Path

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
R = os.environ.get("RODADA", "v3")      # final: RODADA=final540
QA = U / "renders" / R / "qa"
QA.mkdir(parents=True, exist_ok=True)
MP4 = U / "renders" / R / f"yt_0034_preview_{R}_540p15.mp4"
INI = json.loads((U / "renders" / R / f"lotes_{R}.json").read_text(encoding="utf-8"))["inicio"]
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
FONTE = ImageFont.truetype(str(U.parents[1] / "assets" / "fonts" / "space_grotesk" / "SpaceGrotesk-Bold.ttf"), 22)
LOTE_DE = {"H0": "PH", "H1": "PH", "H2": "PH", "A1": "PA", "B1-1": "PB1", "B1-2": "PB1", "B1-3": "PB1", "B2-1": "PB2", "B2-2": "PB2", "B3-1": "PB3",
           "B3-2": "PB3", "B4-1": "PB4", "B4-2": "PB4", "B4-2b": "PB4", "B4-3": "PB4", "B5-1": "PB5", "B5-2": "PB5", "B6-1": "PB6", "B7-1": "PB7",
           "B7-2": "PB7", "B8": "PB8", "S1": "PS", "S2": "PS"}


def log(l):
    return (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="ignore")


def ancora_lote(l):
    return {a: float(t) for a, t in re.findall(r"^\[ancora\] (\S+) ([\d.]+)", log(l), re.M)}


def gatilhos():
    """(âncora, frase) → tempo no vídeo montado (s)."""
    out = {}
    for l, q0 in INI.items():
        al = ancora_lote(l)
        for aid, t, fr in re.findall(r"^\[gatilho\] (\S+)\s+([\d.]+)s .*?\) (.*)$", log(l), re.M):
            out[(aid, fr.strip())] = q0 / 15 + al.get(aid, 0.0) + float(t)
    return out


def mmss(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


# ── 1 · CONTAS: cada degrau, na ordem, com a frase que o dispara (o código escreve o degrau logo depois do gatilho) ──
CONTAS = {
    "C1 · B1-3 · a área π (substituição trigonométrica que o desenho entrega)": [
        ("B1-3", "fica a integral de", "∬_B 1 dA → = ∫₀² √(4 − x²) dx (mapa 3a: a de dentro vira o comprimento)"),
        ("B1-3", "liga o ponto", "O2: o ponto da fatia na circunferência"),
        ("B1-3", "é um raio", "O2: o raio até ele"),
        ("B1-3", "de tamanho dois", "O2: rótulo 2 no raio"),
        ("B1-3", "chamando de teta", "O2: o ângulo θ a partir do eixo y"),
        ("B1-3", "o xis é dois", "O2: cateto horizontal x = 2 sen θ (âmbar)"),
        ("B1-3", "é dois cosseno de", "O2: cateto vertical √(4 − x²) = 2 cos θ (magenta)"),
        ("B1-3", "então dê xis é", "x = 2 sen θ (voa do desenho) ⇒ dx = 2 cos θ dθ"),
        ("B1-3", "os limites mudam junto", "x = 0 → θ = 0"),
        ("B1-3", "e xis igual a dois", "x = 2 → θ = π/2"),
        ("B1-3", "a integral vira a", "= ∫₀^{π/2} 2cos θ · 2cos θ dθ (os 2 cos θ voam da altura e do dx)"),
        ("B1-3", "quatro cosseno ao quadrado", "= ∫₀^{π/2} 4 cos² θ dθ"),
        ("B1-3", "um mais cosseno de", "cos² θ = (1 + cos 2θ)/2"),
        ("B1-3", "a primitiva fica", "= 2[θ + sen 2θ/2]₀^{π/2}"),
        ("B1-3", "em pi sobre dois dá", "= 2(π/2 + 0)"),
        ("B1-3", "em zero dá zero", "− 2(0 + 0)"),
        ("B1-3", "resultado pi", "= π"),
        ("B1-3", "a geometria confirma", "a escada sobe; chip ∫₀² √(4 − x²) dx = π"),
        ("B1-3", "um quarto de pi", "π · 2²/4 = π (o 2 voa do raio) + chave UM QUARTO DO DISCO"),
    ],
    "C2 · B3-1 · cunha em pé": [
        ("B3-1", "a integral de dentro", "∫₀^{√(4−x²)} y dy"),
        ("B3-1", "é ípsilon ao quadrado", "= [y²/2]₀^{√(4−x²)}"),
        ("B3-1", "no limite de cima", "= (√(4−x²))²/2"),
        ("B3-1", "no de baixo zero", "− 0²/2"),
        ("B3-1", "fica quatro menos", "= (4 − x²)/2"),
        ("B3-1", "base vezes altura", "BASE · ALTURA / 2 (base e altura acendem no triângulo)"),
        ("B3-1", "agora a de fora", "∫₀² (4 − x²)/2 dx (a fração voa da linha de cima)"),
        ("B3-1", "o meio sai", "= ½[4x − x³/3]₀²"),
        ("B3-1", "em dois oito", "= ½[(8 − 8/3)"),
        ("B3-1", "em zero zero", "− (0 − 0)]"),
        ("B3-1", "metade de dezesseis", "= ½ · 16/3"),
        ("B3-1", "oito terços de quilo", "= 8/3"),
    ],
    "C3 · B3-2 · cunha deitada (substituição com limite invertido)": [
        ("B3-2", "a integral de dentro", "∫₀^{√(4−y²)} y dx"),
        ("B3-2", "ípsilon vezes xis", "= y[x]₀^{√(4−y²)}"),
        ("B3-2", "altura vezes comprimento", "= y√(4 − y²) (ALTURA y · COMPRIMENTO √(4 − y²) no retângulo)"),
        ("B3-2", "agora a de fora", "∫₀² y√(4 − y²) dy"),
        ("B3-2", "quase a derivada", "o y e o y² de dentro da raiz acendem (menta)"),
        ("B3-2", "chama u de", "u = 4 − y²"),
        ("B3-2", "dê u é menos", "⇒ du = −2y dy"),
        ("B3-2", "então ípsilon dê ípsilon", "o y que multiplica e o −2y acendem juntos; ⇒ y dy = −du/2"),
        ("B3-2", "os limites mudam junto", "y = 0 → u = 4"),
        ("B3-2", "e ípsilon igual a dois", "y = 2 → u = 0"),
        ("B3-2", "o menos inverte", "= −½∫₄⁰ √u du"),
        ("B3-2", "fica meio da", "= ½∫₀⁴ u^{1/2} du"),
        ("B3-2", "a primitiva de raiz", "= ½[⅔ u^{3/2}]₀⁴"),
        ("B3-2", "meio vezes dois terços", "= ½ · ⅔ · 8"),
        ("B3-2", "oito terços de novo", "= 8/3 ✓"),
    ],
    "C4 · B4-2b · sino, passo 3": [
        ("B4-2b", "a de dentro é", "∫₀^y e^(−y²) dx"),
        ("B4-2b", "sai para fora", "= e^(−y²)[x]₀^y"),
        ("B4-2b", "altura vezes comprimento", "= y e^(−y²) (o y voa da chave COMPRIMENTO)"),
        ("B4-2b", "agora a de fora", "∫₀¹ y e^(−y²) dy"),
        ("B4-2b", "quase a derivada do", "o y e o −y² do expoente acendem"),
        ("B4-2b", "chama u de", "u = y²"),
        ("B4-2b", "dê u é dois", "⇒ du = 2y dy"),
        ("B4-2b", "então ípsilon dê ípsilon", "⇒ y dy = du/2"),
        ("B4-2b", "ípsilon igual a zero", "y = 0 → u = 0"),
        ("B4-2b", "e ípsilon igual a um", "y = 1 → u = 1"),
        ("B4-2b", "fica meio da", "= ½∫₀¹ e^(−u) du"),
        ("B4-2b", "a primitiva é menos", "= ½[−e^(−u)]₀¹"),
        ("B4-2b", "em um menos", "= ½(−e^(−1)"),
        ("B4-2b", "em zero menos", "− (−e⁰))"),
        ("B4-2b", "menos menos um", "= (1 − 1/e)/2"),
        ("B4-2b", "metade disso", "≈ (1 − 0,368)/2"),
        ("B4-2b", "zero vírgula três", "≈ 0,316"),
    ],
    "C5 · B5-1 · triângulo de baixo, em pé": [
        ("B5-1", "a integral de dentro", "∫₀^x (x² + y²) dy (o x voa do rótulo y = x)"),
        ("B5-1", "a primitiva em ípsilon", "= [x²y + y³/3]₀^x"),
        ("B5-1", "igual a xis dá", "= (x³ + x³/3)"),
        ("B5-1", "em zero zero", "− 0"),
        ("B5-1", "somando quatro terços", "= 4x³/3"),
        ("B5-1", "a de fora", "∫₀² 4x³/3 dx (o 4x³/3 voa)"),
        ("B5-1", "à quarta sobre", "= (4/3)[x⁴/4]₀²"),
        ("B5-1", "em dois xis à", "= (4/3)(16/4 − 0)"),
        ("B5-1", "dezesseis terços de quilo", "= 16/3"),
    ],
    "C6 · B5-2 · o mesmo triângulo, deitado": [
        ("B5-2", "entra na diagonal", "∫_y² (x² + y²) dx (y e 2 voam dos rótulos)"),
        ("B5-2", "a primitiva em xis", "= [x³/3 + y²x]_y²"),
        ("B5-2", "igual a dois oito", "= (8/3 + 2y²)"),
        ("B5-2", "igual a ípsilon ípsilon", "− (y³/3 + y³)"),
        ("B5-2", "subtraindo oito terços", "= 8/3 + 2y² − 4y³/3"),
        ("B5-2", "a primitiva disso", "∫₀² (8/3 + 2y² − 4y³/3) dy = [8y/3 + 2y³/3 − y⁴/3]₀²"),
        ("B5-2", "dá dezesseis terços", "= 16/3 + 16/3 − 16/3"),
        ("B5-2", "sobra dezesseis terços", "= 16/3 ✓"),
    ],
    "C7 · B6-1 · sen(x³) (substituição u = x³)": [
        ("B6-1", "e a de dentro dá", "∫₀^{x²} sen(x³) dy"),
        ("B6-1", "vezes ípsilon de", "linha a: = sen(x³)·[y]₀^{x²} (glyph map D4a)"),
        ("B6-1", "até xis ao quadrado xis", "linha b: = sen(x³)·(x² − 0) (o x² voa da chave do comprimento no painel ESTA FATIA)"),
        ("B6-1", "xis ao quadrado vezes", "= x² sen(x³) (o − 0 acende em GEO e fica)"),
        ("B6-1", "aqui trouxe xis", "∫₀¹ x² sen(x³) dx"),
        ("B6-1", "quase a derivada de", "o x² e o x³ acendem juntos"),
        ("B6-1", "chama u de", "u = x³"),
        ("B6-1", "dê u é três", "⇒ du = 3x² dx ⇒ x² dx = du/3"),
        ("B6-1", "xis de zero a um", "x = 0 → u = 0 · x = 1 → u = 1"),
        ("B6-1", "fica um terço", "= ⅓∫₀¹ sen u du"),
        ("B6-1", "a primitiva é menos", "= ⅓[−cos u]₀¹"),
        ("B6-1", "menos cosseno de um", "= ⅓(−cos 1 + cos 0)"),
        ("B6-1", "resultado um menos", "= (1 − cos 1)/3"),
        ("B6-1", "zero vírgula um", "≈ 0,153"),
    ],
    "C8 · B7-1 · telhado (comprimento = saída − entrada nas duas ordens)": [
        ("B7-1", "vira duas integrais", "EM PÉ: ∫₋₁⁰ (1 + x) dx + ∫₀¹ (1 − x) dx"),
        ("B7-1", "à esquerda a primitiva", "= [x + x²/2]₋₁⁰"),
        ("B7-1", "de menos um a zero", "= (0 − (−½))"),
        ("B7-1", "à direita a primitiva", "+ [x − x²/2]₀¹"),
        ("B7-1", "de zero a um dá meio", "+ (½ − 0)"),
        ("B7-1", "meio mais meio", "= ½ + ½ = 1"),
        ("B7-1", "fatiando deitado", "a escada sobe; chip EM PÉ: ½ + ½ = 1"),
        ("B7-1", "saída menos a entrada", "DEITADO: ∫₀¹ [(1 − y) − (y − 1)] dy (o 1 − y voa do rótulo coral, o y − 1 do azul-claro)"),
        ("B7-1", "dois menos dois ípsilon", "= ∫₀¹ (2 − 2y) dy"),
        ("B7-1", "a primitiva é dois", "= [2y − y²]₀¹"),
        ("B7-1", "em um dois menos", "= (2 − 1) − 0"),
        ("B7-1", "uma conta só a", "= 1"),
    ],
    "C9 · B8 · Ana e Bia, 7/16 pelo complemento": [
        ("B8", "olha o que fica", "O2: os dois triângulos de fora nos cantos"),
        ("B8", "com catetos de", "O2: chaves nos catetos, 3/4"),
        ("B8", "cada um tem área", "FORA = 2 · ½ · (3/4)²"),
        ("B8", "nove dezesseis avos", "= 9/16"),
        ("B8", "é um menos", "CHANCE = 1 − 9/16"),
        ("B8", "sete dezesseis avos", "= 7/16"),
        ("B8", "quase quarenta e", "≈ 44%"),
    ],
}


def contas():
    gt = gatilhos()
    out = ["CONTAS (handoff v3 §2 e §9.1): cada degrau, o instante no preview v3 (o degrau é escrito logo depois do gatilho) e a frase que o dispara.",
           "Formato: tempo · âncora · \"frase\" · degrau. AUSENTE = gatilho não encontrado no log (degrau faltando).", ""]
    falta = 0
    for nome, passos in CONTAS.items():
        out.append(nome)
        for aid, fr, deg in passos:
            t = gt.get((aid, fr))
            if t is None:
                falta += 1
                out.append(f"   AUSENTE  {aid:6s} \"{fr}\" · {deg}")
            else:
                out.append(f"   {mmss(t):>8s}  {aid:6s} \"{fr}\" · {deg}")
        out.append("")
    out.insert(2, f"Degraus: {sum(len(p) for p in CONTAS.values())} · ausentes: {falta}")
    (QA / f"contas_{R}.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    return falta


def quadros(ts):
    want = {round(t * 15): t for t in ts}
    res = {}
    with av.open(str(MP4)) as c:
        for i, f in enumerate(c.decode(video=0)):
            if i in want:
                res[want[i]] = f.to_image()
            if i > max(want):
                break
    return [res[t] for t in ts]


def folha(imgs, rots, saida, cols=3, w=640):
    h = w * 9 // 16
    linhas = math.ceil(len(imgs) / cols)
    o = Image.new("RGB", (cols * (w + 10) + 10, linhas * (h + 40) + 10), (12, 10, 30))
    d = ImageDraw.Draw(o)
    for k, (im, r) in enumerate(zip(imgs, rots)):
        x, y = 10 + (k % cols) * (w + 10), 10 + (k // cols) * (h + 40)
        d.text((x, y), r, font=FONTE, fill=(240, 240, 255))
        o.paste(im.resize((w, h)), (x, y + 30))
    o.save(saida, quality=88)


def palco_cheio(im):
    """px do palco (x < 1090 a 1080p, abaixo do canto) que diferem > 30 níveis do fundo violeta, a 960×540."""
    a = np.asarray(im.convert("L"), np.int16)
    m = a[80:, :545]
    fundo = np.median(m)
    return int(np.count_nonzero(np.abs(m - fundo) > 30))


def aberturas():
    gt = gatilhos()
    ts = [0.0, 2.0, 5.0, 9.0, 12.0, 15.0]
    b41 = INI["PB4"] / 15 + ancora_lote("PB4")["B4-1"]
    b61 = INI["PB6"] / 15 + ancora_lote("PB6")["B6-1"]
    t2 = [b41 + k for k in range(5)] + [b61 + k for k in range(5)]
    ims = quadros(ts + t2)
    rots = [f"H0 {mmss(t)}" for t in ts] + [f"B4-1 +{k} s" for k in range(5)] + [f"B6-1 +{k} s" for k in range(5)]
    folha(ims, rots, QA / f"aberturas_{R}.jpg")
    linhas = ["ABERTURAS (§9.4): quadros em 0:00, 0:02, 0:05, 0:09, 0:12, 0:15 (H0) e os 4 primeiros segundos do B4-1 e do B6-1, um por segundo.",
              "Palco ocupado = px do palco que diferem > 30 níveis do fundo (palco vazio < 300)."]
    for r, im in zip(rots, ims):
        n = palco_cheio(im)
        linhas.append(f"  {r:14s} palco {n:6d} px  {'VAZIO' if n < 300 else 'ok'}")
    (QA / f"aberturas_{R}.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")


def glyph_meio():
    ts, rots = [], []
    for l, q0 in INI.items():
        for lote, aid, t, nota in re.findall(r"^\[gm\] (\S+) (\S+) ([\d.]+) pares=\d+ (.*?) ::", log(l), re.M):
            tm = q0 / 15 + float(t) + 0.6
            ts.append(tm)
            rots.append(f"{aid} {mmss(tm)} · {nota[:44]}")
    ims = quadros(ts)
    folha(ims, rots, QA / f"glyph_maps_meio_{R}.jpg")
    return len(ts)


def gancho():
    gt = gatilhos()
    t0 = gt[("S2", "mas quando ela")]
    t1 = gt[("S2", "a saída troca")]
    tc = INI["PS"] / 15 + float(re.findall(r"^\[marca\] v3_07 ([\d.]+)", log("PS"), re.M)[0])
    ts = [t0 + 1.0, t0 + 2.8, t1 + 1.7, tc]
    ims = quadros(ts)
    folha(ims, ["antes (y ≈ 2,4)", "na passagem (y = 3)", "depois (y = 3,5)", "cartão com os 3 itens"], QA / f"gancho_{R}.jpg", cols=2, w=800)


def areas():
    A = lambda x: math.sqrt(math.pi) / 2 * (math.erf(1) - math.erf(x))
    l = ["ÁREAS DAS FATIAS (§9.3), conferidas por conta direta (math):",
         f"  sino em pé  A(0,2) = ∫₀,₂¹ e^(−y²) dy = (√π/2)(erf 1 − erf 0,2) = {A(.2):.4f}  → 0,549",
         f"  sino deitado A(0,6) = 0,6 · e^(−0,36) = {.6 * math.exp(-.36):.4f}  → 0,419",
         f"  cunha em pé  A(1) = (4 − 1)/2 = {(4 - 1) / 2:.4f}  → 1,5",
         f"  cunha deitada A(1) = 1 · √(4 − 1) = {math.sqrt(3):.4f}  → 1,73",
         f"  sino: ∫₀¹ A(y) dy = ∫₀¹ y e^(−y²) dy = (1 − 1/e)/2 = {(1 - 1 / math.e) / 2:.5f} (e ∫₀¹ A(x) dx dá o mesmo: "
         f"{sum(A((k + .5) / 4000) for k in range(4000)) / 4000:.5f} pela soma de Riemann)",
         f"  cunha: ∫₀² (4 − x²)/2 dx = {8 / 3:.4f} = 8/3 = ∫₀² y√(4 − y²) dy",
         "  Os pontos do desenho: GA.px(0,2, A(0,2)) e GB.px(0,6, A(0,6)) (sec_b4) · GA.px(1, 1,5) e GB.px(1, √3) (sec_b3).",
         "  Quadros finais ao lado dos alvos v3_04 e v3_05: comparacao_v3.jpg."]
    (QA / f"areas_{R}.txt").write_text("\n".join(l) + "\n", encoding="utf-8")


def duracoes():
    tab = {"H0": 16.0, "H1": 66.7, "H2": 22.3, "A1": 20.3, "B1-1": 66.0, "B1-2": 57.7, "B1-3": 89.7, "B2-1": 52.7, "B2-2": 52.7, "B3-1": 69.3, "B3-2": 112.7,
           "B4-1": 38.3, "B4-2": 53.3, "B4-2b": 67.0, "B4-3": 44.7, "B5-1": 50.0, "B5-2": 55.0, "B6-1": 84.3, "B7-1": 81.0, "B7-2": 42.3, "B8": 63.7,
           "S1": 41.7, "S2": 56.0}
    ini = {}
    for l, q0 in INI.items():
        for a, t in ancora_lote(l).items():
            ini[a] = q0 / 15 + t
    ordem = sorted(ini, key=ini.get)
    tot = json.loads((U / "renders" / R / f"lotes_{R}.json").read_text())["duracao_s"]
    l = [f"DURAÇÕES (§9.7): total do preview {mmss(tot)} ({tot:.1f} s) × tabela do §7 21:43 de voz (+ respiros de 0,5 s por âncora e 3 s do CTA).",
         "âncora   início no preview   duração no preview   voz (§7)   diferença"]
    for k, a in enumerate(ordem):
        fim = ini[ordem[k + 1]] if k + 1 < len(ordem) else tot
        d = fim - ini[a]
        l.append(f"  {a:6s} {mmss(ini[a]):>10s}   {d:8.1f} s   {tab.get(a, 0):8.1f} s   {d - tab.get(a, 0):+6.1f} s")
    (QA / f"duracoes_{R}.txt").write_text("\n".join(l) + "\n", encoding="utf-8")


if __name__ == "__main__":
    print("contas ausentes", contas())
    aberturas()
    print("glyph maps", glyph_meio())
    gancho()
    areas()
    duracoes()
    print("ok")
