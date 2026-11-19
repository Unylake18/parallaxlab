"""yt_0036 · handoff final §7/§10: pranchas e stills de conferência a partir do preview final 540p (renders/final/) e dos logs dos lotes.
- qa/correcoes_final.jpg: cada quadro K01a…K15 (referencia_final/) ao lado do quadro corrigido no gatilho do item;
- qa/voos_final.jpg (K3), qa/mapas_final.jpg (K4, K12), qa/zoom_final.jpg (K6);
- qa/ancoras_final.jpg: um quadro de cada âncora no instante da 1ª palavra (24 quadros);
- stills/K01_t0.png, K01_t1.png, K01_t2.png, S2_final.png e um still por item K (stills/Kxx.png).
uso: python pranchas_final.py"""
import json
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
R = "final"
MP4 = U / "renders" / R / f"yt_0036_preview_{R}_540p15.mp4"
QA = U / "renders" / R / "qa"
ST = U / "stills"
RF = U / "referencia_final"
LOTES = ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PB8", "PS"]
INI = json.loads((U / "renders" / R / f"lotes_{R}.json").read_text())["inicio"]
try:
    FT = ImageFont.truetype("arial.ttf", 20)
except OSError:
    FT = ImageFont.load_default()


def log(l):
    return (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="ignore")


def lote_de(aid):
    for l in LOTES:
        if re.search(rf"^\[ancora\] {re.escape(aid)} ", log(l), re.M):
            return l
    raise KeyError(aid)


def t_ancora(aid):
    l = lote_de(aid)
    m = re.search(rf"^\[ancora\] {re.escape(aid)} ([\d.]+)", log(l), re.M)
    return INI[l] / 15 + float(m.group(1))


def t_gat(aid, frase, dt=0.0):
    l = lote_de(aid)
    for m in re.finditer(rf"^\[gatilho\] {re.escape(aid)}\s+([\d.]+)s .*?\) (.*)$", log(l), re.M):
        if m.group(2).strip() == frase:
            return t_ancora(aid) + float(m.group(1)) + dt
    raise KeyError((aid, frase))


def t_evento(aid, sub, dt=0.0):
    """Fim do primeiro [linha]/[voo] da âncora cujo LaTeX contém `sub` (tempo relativo à âncora)."""
    l = lote_de(aid)
    for m in re.finditer(rf"^\[(?:linha|voo)\] \S+ {re.escape(aid)}\s+([\d.]+)s (?:\S+ )?(.*)$", log(l), re.M):
        if sub.replace(" ", "") in m.group(2).replace(" ", "").replace("\\\\", "\\"):
            return t_ancora(aid) + float(m.group(1)) + dt
    raise KeyError((aid, sub))


def quadros(ts):
    alvo = sorted((max(0, round(t * 15)), k) for k, t in enumerate(ts))
    out, i = {}, 0
    c = av.open(str(MP4))
    for q, f in enumerate(c.decode(video=0)):
        while i < len(alvo) and alvo[i][0] == q:
            out[alvo[i][1]] = f.to_image()
            i += 1
        if i >= len(alvo):
            break
    c.close()
    return [out[k] for k in range(len(ts))]


def grade(ims, rot, cols, saida, titulo, esc=1.0):
    w, h = int(ims[0].width * esc), int(ims[0].height * esc)
    linhas = (len(ims) + cols - 1) // cols
    P = Image.new("RGB", (cols * w + (cols + 1) * 8, linhas * (h + 30) + 50), (14, 12, 28))
    d = ImageDraw.Draw(P)
    d.text((10, 12), titulo, fill=(250, 220, 90), font=FT)
    for k, (im, r) in enumerate(zip(ims, rot)):
        x, y = 8 + (k % cols) * (w + 8), 50 + (k // cols) * (h + 30)
        P.paste(im.resize((w, h)), (x, y + 24))
        d.text((x, y + 2), r, fill=(230, 230, 230), font=FT)
    P.save(saida, quality=88)
    print(saida, P.size)


def main():
    QA.mkdir(parents=True, exist_ok=True)
    ST.mkdir(exist_ok=True)
    K = [("K01a", lambda: 0.0, "quadro 0: eixos + trapézio nascendo; canto A INTEGRAL QUE TRAVA"),
         ("K01b", lambda: 2.0, "t = 2,0 s: trapézio completo e a integral escrita"),
         ("K02", lambda: t_gat("B3-3", "é o meio do trapézio", 0.25), "chip: moldura e |J| = nascem juntos"),
         ("K03a", lambda: t_evento("B3-3", r"\right|=\Lm{\dfrac{1}{2}}", -0.3), "voo do 1/2 sem cópia deslocada"),
         ("K03b", lambda: t_ancora("B6-2") - 0.6, "|J| = 1/2 voando para o chip"),
         ("K03c", lambda: t_gat("B6-3", "por fora um meio", 1.6), "∫ desce sem cruzar a linha de cima"),
         ("K03d", lambda: t_gat("B6-4", "vezes o fator", 0.3), "3 sai sem cruzar o rótulo"),
         ("K03e", lambda: t_gat("B7", "quatro menos dois", 0.6), "½(2·2 − 2·1) sem cruzar o colchete"),
         ("K04a", lambda: t_gat("B3-2", "abrindo o produto", 0.6), "linha nova nasce abaixo"),
         ("K04b", lambda: t_gat("B3-2", "o bê dê cancela", 1.6), "pares saem; buracos fecham na linha"),
         ("K04c", lambda: t_gat("B6-3", "fica vê vezes", 2.0), "só o trecho novo nasce à direita"),
         ("K04d", lambda: t_evento("B6-4", "2^2-1^2", -0.3), "2² − 1² sem sobreposição"),
         ("K05", lambda: t_gat("B4-1", "muda de ponto para ponto", 0.2), "o 'O F' é o começo da caneta (não é órfão)"),
         ("K06a", lambda: t_gat("B4-2", "dá zoom numa célula", 0.3), "antes do zoom: o mapa de calor apaga"),
         ("K06b", lambda: t_gat("B4-2", "dá zoom numa célula", 1.9), "meio do zoom: sem tela verde"),
         ("K06c", lambda: t_gat("B4-2", "dá zoom numa célula", 3.6), "fim do zoom = MNPQ (sem corte)"),
         ("K07", lambda: t_gat("B4-2", "o lado mn é a", 1.0), "M = φ(0,75; 0,5) é a 1ª linha da coluna"),
         ("K08a", lambda: t_gat("B5-3", "dobra por cima", 1.5), "planos grandes enquanto a coluna está vazia"),
         ("K08b", lambda: t_ancora("B5-4") - 0.5, "C18.8 ✓ ainda na tela (≥ 2 s)"),
         ("K09", lambda: t_ancora("B5-4") + 0.4, "1º quadro do B5-4: canto CONFERINDO O TEOREMA"),
         ("K10a", lambda: t_gat("B5-4", "oito terços", 1.0), "= 8/3 escrito e parado"),
         ("K10b", lambda: t_gat("B5-4", "sem jacobiano", 1.6), "8/3 voa para COM J: ÁREA = 8/3"),
         ("K11", lambda: t_gat("B6-3", "o vê está congelado", 2.2), "v CONGELADO fora do trapézio"),
         ("K12", lambda: t_gat("B6-3", "por fora um meio", 0.2), "troca de página em dois tempos"),
         ("K13", lambda: t_gat("B6-4", "vezes o fator", 0.5), "voo dentro de x ≤ 1872"),
         ("K14", lambda: t_gat("A1", "fala pessoal", 2.5), "título escrito nos 3 primeiros s"),
         ("K15", lambda: t_gat("S2", "debaixo do sino", 1.5), "duas células, chave, MENOR/MAIOR, cartão de 3 linhas")]
    ts, ok = [], []
    for nome, f, _ in K:
        try:
            ts.append(f())
            ok.append(True)
        except Exception as e:                                   # noqa: BLE001
            print("sem tempo:", nome, e)
            ts.append(0.0)
            ok.append(False)
    fr = quadros(ts + [0.0, 1.0, 2.0])
    k01 = fr[-3:]
    for im, nm in zip(k01, ("K01_t0", "K01_t1", "K01_t2")):
        im.save(ST / f"{nm}.png")
    linhas = []
    for (nome, _, desc), t, im, o in zip(K, ts, fr, ok):
        im.save(ST / f"{nome}.png")
        ref = RF / f"{nome}.jpg"
        if not ref.exists():
            ref = RF / f"{nome[:3]}.jpg"
        a = Image.open(ref).convert("RGB").resize((960, 540)) if ref.exists() else Image.new("RGB", (960, 540))
        row = Image.new("RGB", (1920, 580), (14, 12, 28))
        row.paste(a, (0, 40))
        row.paste(im.resize((960, 540)), (960, 40))
        d = ImageDraw.Draw(row)
        d.text((8, 8), f"{nome} · v2 (erro)", fill=(255, 120, 120), font=FT)
        d.text((968, 8), f"{nome} · final {int(t // 60)}:{t % 60:05.2f} · {desc}" + ("" if o else " (SEM TEMPO)"), fill=(150, 240, 150), font=FT)
        linhas.append(row)
    P = Image.new("RGB", (1920, 588 * len(linhas)), (0, 0, 0))
    for k, r in enumerate(linhas):
        P.paste(r, (0, k * 588))
    P.save(QA / "correcoes_final.jpg", quality=86)
    print(QA / "correcoes_final.jpg", P.size)
    fr[len(K) - 1].save(ST / "S2_final.png")                           # o K15 é o último da lista
    # voos (K3): um quadro a cada ~0,13 s (2 quadros a 15 fps) durante cada voo
    mom = [("K3a B3-3 1/2", t_evento("B3-3", r"\right|=\Lm{\dfrac{1}{2}}") - 1.0),
           ("K3b B6-1 → chip", t_ancora("B6-2") - 1.4),
           ("K3c B6-3 ∫", t_gat("B6-3", "por fora um meio", 0.9)),
           ("K3d B6-4 3", t_gat("B6-4", "vezes o fator", 0.0)),
           ("K3e B7 ½(2·2 − 2·1)", t_gat("B7", "quatro menos dois", 0.0))]
    ims, rot = [], []
    for nome, t0 in mom:
        tt = [t0 + 0.1333 * k for k in range(8)]
        for t, im in zip(tt, quadros(tt)):
            ims.append(im)
            rot.append(f"{nome} {t:.2f}s")
    grade(ims, rot, 8, QA / "voos_final.jpg", "K3 · voos: um quadro a cada 2 quadros (0,13 s) durante o voo", esc=0.5)
    # mapas (K4, K12): B3-2 a cada 0,5 s e B6-3 (troca de página) a cada 0,5 s
    t1, t2 = t_gat("B3-2", "abrindo o produto", -0.5), t_gat("B3-2", "sobra menos bê cê", 1.5)
    tt = [t1 + 0.5 * k for k in range(int((t2 - t1) / 0.5) + 1)][:28]
    t3 = t_gat("B6-3", "por fora um meio", -0.5)
    tt2 = [t3 + 0.5 * k for k in range(8)]
    fr2 = quadros(tt + tt2)
    grade(fr2, [f"B3-2 {t:.1f}s" for t in tt] + [f"B6-3 {t:.1f}s" for t in tt2], 6, QA / "mapas_final.jpg",
          "K4 · B3-2 (mapas e cancelamento) e K12 · B6-3 (troca de página), um quadro a cada 0,5 s", esc=0.5)
    # zoom (K6): a cada 0,25 s
    tz = t_gat("B4-2", "dá zoom numa célula", -0.5)
    tt = [tz + 0.25 * k for k in range(24)]
    grade(quadros(tt), [f"{t:.2f}s" for t in tt], 6, QA / "zoom_final.jpg", "K6 · zoom do B4-1 para o B4-2, a cada 0,25 s", esc=0.5)
    # as 24 âncoras na 1ª palavra
    A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
    ords = A["ordem"]
    tv = [A["ancoras"][a]["ini"] + A["ancoras"][a]["t"][0] for a in ords]
    grade(quadros(tv), [f"{a} · voz {t:.2f}s" for a, t in zip(ords, tv)], 6, QA / "ancoras_final.jpg",
          "um quadro de cada âncora no instante da 1ª palavra (tempo da voz = tempo do vídeo)", esc=0.5)


if __name__ == "__main__":
    main()
