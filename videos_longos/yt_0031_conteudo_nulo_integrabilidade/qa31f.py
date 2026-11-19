"""yt_0031 · QA da rodada com voz (handoff final §7; copiado do qa31v3.py) → renders/<RODADA>/qa/:
  parados_v3.txt       G3: trechos > 3 s em que menos de 40 px do quadro 960×540 mudam (diferença > 8 em algum canal) — com a fala do trecho
  comeco_bloco_v3.txt  G2: por bloco, a linha 2 do canto no 1º quadro e o 1º quadro com figura; palco vazio > 0,5 s no vídeo inteiro
  sobreposicoes_v3.txt G4: R5 ampliado (amostrado a cada 0,47 s durante o render, inclusive nas animações)
  glyphmaps_v3.txt     G1/§4: cada TransformByGlyphMap (tempo, bloco, A → B, pares, glifos a caneta); mapa_glifos = 0
  origens_v3.txt       toda linha de fórmula/legenda com a origem (caneta, voo, glyph map); linhas sem origem
  gatilhos_v3.txt      atraso de cada gatilho (≤ 0,2 s esperado)
  flash_v3.txt, alinhamento3d_v3.txt, tamanhos_v3.txt, tempos_render_v3.txt
uso: python qa31v3.py [--extra]"""
import json
import re
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
import os
R = os.environ.get("RODADA", "voz")
QA = U / "renders" / R / "qa"
ORDEM = ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PB8", "PB9", "PS"]
COM3D = ["PB1", "PB2", "PB5", "PB6", "PS"]
LOTES = json.loads((U / "renders" / R / f"lotes_{R}.json").read_text(encoding="utf-8"))["inicio_s"]
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))


def log(l):
    return (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="ignore")


def t_glob(l, t):
    return LOTES[l] + t


def fala_no_trecho(a, b):
    """Palavras da narração estimada no intervalo [a, b] (s do vídeo), pela posição das âncoras de cada lote no vídeo."""
    pal = []
    for l in ORDEM:
        t = log(l)
        for aid, t0 in re.findall(r"\[ancora\] (\S+) ([\d.]+)", t):
            A = ANC["ancoras"][aid]
            ini = t_glob(l, float(t0))
            ws = A["fala"].split()
            for w, tw in zip(ws, A["t"]):
                if a <= ini + tw <= b:
                    pal.append(w)
    return " ".join(pal)


def video():
    c = av.open(str(U / "renders" / R / f"yt_0031_preview_{R}_540p15.mp4"))
    for fr in c.decode(video=0):
        yield fr.to_ndarray(format="rgb24")
    c.close()


def parados_e_vazios():
    fundo = np.asarray(__import__("PIL.Image", fromlist=["Image"]).open(
        U.parents[1] / "assets" / "calculo" / "fundo_calculo_violeta_liso_960x540.png").convert("RGB"), np.int16)
    mascara = np.ones((540, 960), bool)
    mascara[:70, :360] = False          # canto (2 linhas)
    mascara[:60, 810:] = False          # logo
    ant, ini, runs, vaz, iv, i = None, None, [], [], None, 0
    for a in video():
        a16 = a.astype(np.int16)
        if ant is not None:
            d = (np.abs(a16 - ant).max(axis=2) > 8).sum()
            if d < 40:
                ini = i if ini is None else ini
            else:
                if ini is not None and (i - ini) / 15 > 3.0:
                    runs.append((ini / 15, i / 15))
                ini = None
        # palco vazio: só fundo, grade fina, canto e logo (nenhum pixel de conteúdo forte fora do canto/logo)
        conteudo = ((np.abs(a16 - fundo).max(axis=2) > 45) & mascara).sum()
        if conteudo < 150:
            iv = i if iv is None else iv
        else:
            if iv is not None and (i - iv) / 15 > 0.5:
                vaz.append((iv / 15, i / 15))
            iv = None
        ant = a16
        i += 1
    if ini is not None and (i - ini) / 15 > 3.0:
        runs.append((ini / 15, i / 15))
    return runs, vaz, i / 15


def lote_de(t):
    return [l for l, v in LOTES.items() if v <= t + 1e-6][-1]


def mmss(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


def main():
    QA.mkdir(parents=True, exist_ok=True)
    runs, vaz, total = parados_e_vazios()
    linhas = []
    for a, b in runs:
        dur = b - a
        cls = "> 5 s" if dur > 5 else "3–5 s"
        linhas.append(f"{mmss(a)} – {mmss(b)}  ({dur:4.1f} s, {cls})  {lote_de(a)}  | fala: «{fala_no_trecho(a, b)}»")
    n5 = sum(1 for a, b in runs if b - a > 5)
    (QA / f"parados_{R}.txt").write_text(
        "G3 · parado = trecho em que menos de 40 px do quadro 960×540 mudam (diferença > 8 em algum canal), quadro a quadro, por mais de 3 s.\n"
        "Motivo: a fala do trecho (voz real, alinhamento forçado) vai ao lado; entre 3 e 5 s o critério do handoff aceita a voz lendo a tela.\n\n"
        f"{len(runs)} trechos > 3 s · {n5} trechos > 5 s · duração do vídeo {mmss(total)}\n\n" + "\n".join(linhas) + "\n", encoding="utf-8")
    # começo de bloco
    cb = []
    for l in ORDEM:
        t = log(l)
        antes = re.search(r'ANTES = "([^"]+)"', (U / f"sec_{l[1:].lower() if l != 'PH' else 'h'}.py").read_text(encoding="utf-8")) if l not in ("PH", "PA") else None
        p0 = re.findall(r"\[play\] 0 ([\d.]+) ([\d.]+)", t)
        cb.append(f"{l:4s} início {mmss(LOTES[l])}  linha 2 do canto no 1º quadro: {('sim · ' + antes.group(1)) if antes else 'bloco sem canto (H, A)'}"
                  f"  · 1ª animação começa em {float(p0[0][0]) if p0 else -1:.2f} s")
    cb.append("")
    cb.append(f"palco vazio > 0,5 s (só fundo, grade, canto e logo) no vídeo inteiro: {len(vaz)}")
    cb += [f"   {mmss(a)} – {mmss(b)} ({b - a:.1f} s) {lote_de(a)}" for a, b in vaz]
    (QA / f"comeco_bloco_{R}.txt").write_text("G2 · começo de bloco\n\n" + "\n".join(cb) + "\n", encoding="utf-8")
    # R5 ampliado
    r5, tot = [], 0
    for l in ORDEM:
        ev = re.findall(r"\[R5b\] (\S+) +([\d.]+)s (.*)", log(l))
        tot += len(ev)
        r5.append(f"{l:4s} ocorrências = {len(ev)}")
        r5 += [f"   {aid} {mmss(t_glob(l, float(tt)))}  {txt}" for aid, tt, txt in ev]
    (QA / f"sobreposicoes_{R}.txt").write_text(
        "G4 · R5 ampliado (final §7): a cada 0,2 s, inclusive durante as animações e com os glifos EM TRÂNSITO (voos, mapas, ReplacementTransform), a caixa de todo texto/MathTex visível contra:\n"
        "outros textos; linhas, arestas, bordas de chapa/painel/cartão/lupa e setas (pontas incluídas); pontos; e as arestas 3D (borda da chapa,\n"
        "eixos e quinas do bloco, pela mesma projeção do three.js). Cada ocorrência é listada uma vez, no instante em que começa.\n\n"
        + "\n".join(r5) + f"\n\nTOTAL = {tot}\n", encoding="utf-8")
    emb, ne = [], 0
    for l in ORDEM:
        ev = re.findall(r"\[embolado\] (\S+) +([\d.]+)s (.*)", log(l))
        ne += len(ev)
        emb.append(f"{l:4s} ocorrências = {len(ev)}")
        emb += [f"   {aid} {mmss(t_glob(l, float(tt)))}  {txt}" for aid, tt, txt in ev]
    (QA / f"embolados_{R}.txt").write_text("Glifos embolados (final §7): em TODO quadro de animação, dois glifos de objetos diferentes com > 30 % da menor caixa "
                                         "em comum (a cópia sobre o próprio texto de origem/destino não conta)\n\n" + "\n".join(emb) + f"\n\nTOTAL = {ne}\n",
                                         encoding="utf-8")
    # glyph maps e origens
    gm, orig, falta = [], [], []
    for l in ORDEM:
        t = log(l)
        gm += [f"{l:4s} {mmss(t_glob(l, float(x[0])))} {x[1]}" for x in re.findall(r"\[glyphmap\] +([\d.]+) (.*)", t)]
        orig += [f"{l:4s} {mmss(t_glob(l, float(x[0])))} {x[1]}" for x in re.findall(r"\[origem\] +([\d.]+) (.*)", t)]
        falta += re.findall(r"\[origem-falta\] (.*)", t)
    codigo = "".join((U / f).read_text(encoding="utf-8") for f in ["v31.py"] + [f"sec_{s}.py" for s in ("h", "a", "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9", "s")])
    n_mg = len(re.findall(r"\bmapa_glifos\(", codigo))
    (QA / f"glyphmaps_{R}.txt").write_text(
        "G1 · TransformByGlyphMap (MF-Tools 1.4.9, MathTex de string única; CombineTex quando a origem são duas linhas). Glifo que sai: FadeOut\n"
        "(auto_fade); glifo que entra: a caneta (CanetaIntro como introdutor do próprio TransformByGlyphMap), nunca FadeIn.\n\n"
        + "\n".join(gm) + f"\n\nTOTAL = {len(gm)} glyph maps · chamadas a mapa_glifos no código = {n_mg}\n", encoding="utf-8")
    (QA / f"origens_{R}.txt").write_text("Origem de cada linha de fórmula/legenda (tempo no vídeo, bloco, origem | texto | fonte)\n\n" + "\n".join(orig)
                                       + f"\n\nLINHAS SEM ORIGEM (vistas na tela sem caneta, voo ou glyph map): {len(falta)}\n" + "\n".join(falta) + "\n", encoding="utf-8")
    # gatilhos
    gt, n2 = [], 0
    for l in ORDEM:
        for x in re.findall(r"\[gatilho\] (\S+) +([\d.]+)s \(alvo +([\d.]+)s, atraso ([+-][\d.]+)s\) (.*)", log(l)):
            at = float(x[3])
            n2 += at > 0.2
            gt.append(f"{l:4s} {x[0]:5s} {x[1]:>7}s  atraso {at:+.2f} s {'  <-- > 0,2 s' if at > 0.2 else ''}  «{x[4]}»")
    (QA / f"gatilhos_{R}.txt").write_text(f"Gatilhos (evento ligado a uma palavra da voz real): {len(gt)}; com atraso > 0,2 s: {n2}\n\n" + "\n".join(gt) + "\n",
                                        encoding="utf-8")
    # flash
    fl = [(l, int(re.findall(r"\[flash-total\] \S+ (\d+)", log(l))[-1])) for l in ORDEM]
    (QA / f"flash_{R}.txt").write_text("FLASH POR QUADRO (fórmula/legenda visível antes da caneta)\n\n" + "\n".join(f"{l:4s} {n}" for l, n in fl)
                                     + f"\n\nTOTAL = {sum(n for _, n in fl)}\n", encoding="utf-8")
    # alinhamento 3D
    out, pior, nn = [], 0.0, 0
    for l in COM3D:
        reg = json.loads((QA / "al" / f"{l}.json").read_text(encoding="utf-8")) if (QA / "al" / f"{l}.json").exists() else []
        cache, dl, nl = {}, 0.0, 0
        for lote, cena, fq, nome, x, y in reg:
            if cena not in cache:
                pp = U / "threejs" / "q3d" / f"{lote}_960x540" / cena / "pontos.json"
                cache[cena] = json.loads(pp.read_text(encoding="utf-8")) if pp.exists() else {}
            js = cache[cena].get(str(fq))
            if js and nome in js:
                dl, nl = max(dl, max(abs(js[nome][0] - x), abs(js[nome][1] - y))), nl + 1
        pior, nn = max(pior, dl), nn + nl
        out.append(f"{l}: {nl} amostras rótulo × ponto, pior = {dl:.2f} px")
        ped = json.loads((U / "threejs" / "pedidos3d" / f"{l}.json").read_text(encoding="utf-8"))
        esp = {"c00": (360, 780), "c20": (840, 780), "c22": (840, 300), "c02": (360, 300)}
        for cena, lista in ped["cenas"].items():
            pts = json.loads((U / "threejs" / "q3d" / f"{l}_960x540" / cena / "pontos.json").read_text(encoding="utf-8"))
            topo = [f for f, e in lista if abs(e["cam"]["pos"][2] - 11.575) < 0.01 and abs(e["cam"]["pos"][0] - 1) < 1e-3]
            if topo:
                dc = max(max(abs(pts[str(f)][k][0] - v[0]), abs(pts[str(f)][k][1] - v[1])) for f in topo for k, v in esp.items())
                out.append(f"   {cena}: pouso em {len(topo)} quadros; cantos 3D × chapa 2D: pior = {dc:.2f} px")
            else:
                out.append(f"   {cena}: sem pouso (entra/sai por troca de cena)")
    (QA / f"alinhamento3d_{R}.txt").write_text("Alinhamento 3D × Manim (≤ 2 px; pousos: 0 px)\n\n" + "\n".join(out) + f"\n\nTOTAL {nn} amostras, pior = {pior:.2f} px\n",
                                            encoding="utf-8")
    # tamanhos (G6)
    (QA / f"tamanhos_{R}.txt").write_text(
        "G6 · tamanhos mínimos aplicados no código (v31.py): T()/leg() ≥ 24 px a 1080p; TC() com índice, expoente ou fração ≥ 34 px\n"
        "(índice ≈ 0,7 × 34 ≈ 24 px ≥ 22 px); TC() sem índice ≥ 24 px. Como o mínimo é imposto na criação, nenhum texto sai menor.\n"
        "ε/2 com \\frac (B7-2, 40 px). As quatro caixas do B7-3 a 38 px.\n", encoding="utf-8")
    # tempos
    tl = []
    for l in ORDEM:
        t = log(l)
        r_ = re.findall(r"\[render\] \S+ (\d+)s", t)
        t3 = U / f"tempo3d_{l}.txt"
        tl.append(f"{l:4s} vídeo {float(re.findall(r'[[]tempo[]] total ([0-9.]+)s', t)[-1]):7.2f} s  render Manim {int(r_[-1]) if r_ else 0:4d} s"
                  + (f"  + seca/three.js {re.findall(r'(\d+)s', t3.read_text())[-1]} s" if t3.exists() else ""))
    (QA / f"tempos_render_{R}.txt").write_text("Tempo de render por bloco (960×540/15 fps; 3 lotes em paralelo)\n\n" + "\n".join(tl) + "\n", encoding="utf-8")
    print("parados", len(runs), ">5s", n5, "| embolados", ne, "| vazios", len(vaz), "| R5", tot, "| glyphmaps", len(gm), "mapa_glifos", n_mg, "| sem origem", len(falta),
          "| gatilhos >0,2", n2, "| flash", sum(n for _, n in fl), "| alinhamento", round(pior, 2))


if __name__ == "__main__" and "--extra" not in __import__("sys").argv:
    main()


# ── v3 (§0 e §3.6): cortes por bloco e costuras entre lotes ──────────────────────────────────────────────
REFEITOS = ["H1", "H2", "A1", "B1-2", "B1-3", "B1-4", "B2-1", "B2-2", "B3-1", "B3-2", "B3-3", "B4-1", "B4-2", "B4-3", "B5-1", "B5-2", "B6-1",
            "B6-2", "B6-3", "B7-1", "B7-2", "B7-3", "B7-4", "B8-1", "B8-2", "B9-1", "S1", "S2"]


def ancoras_video():
    """[(aid, início no vídeo, fim no vídeo)] pelas marcas [ancora] dos logs."""
    out = []
    for l in ORDEM:
        for aid, t0 in re.findall(r"\[ancora\] (\S+) ([\d.]+)", log(l)):
            out.append([aid, t_glob(l, float(t0))])
    tot = json.loads((U / "renders" / R / f"lotes_{R}.json").read_text(encoding="utf-8"))["total_s"]
    return [(a, t, out[k + 1][1] if k + 1 < len(out) else tot) for k, (a, t) in enumerate(out)]


def cortes():
    import subprocess
    d = U / "renders" / R / "blocos"
    d.mkdir(parents=True, exist_ok=True)
    feitos = []
    for aid, a, b in ancoras_video():
        if aid in REFEITOS:
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i",
                            str(U / "renders" / R / f"yt_0031_preview_{R}_540p15.mp4"), "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                            "-an", str(d / f"{aid}.mp4")], check=True)
            feitos.append(f"{aid:5s} {mmss(a)} – {mmss(b)}")
    (QA / f"blocos_{R}.txt").write_text("Cortes por bloco refeito (renders/v3/blocos/<bloco>.mp4)\n\n" + "\n".join(feitos) + "\n", encoding="utf-8")
    return feitos


def costuras():
    from PIL import Image, ImageDraw, ImageFont
    fonte = ImageFont.truetype(str(U.parents[1] / "assets" / "fonts" / "space_grotesk" / "SpaceGrotesk-Bold.ttf"), 22)
    ini = [LOTES[l] for l in ORDEM]
    alvos = {}
    for k in range(1, len(ORDEM)):
        q = int(round(ini[k] * 15))
        alvos[q - 1] = (k, 0)
        alvos[q] = (k, 1)
    qs = {}
    for i, a in enumerate(video()):
        if i in alvos:
            qs[alvos[i]] = Image.fromarray(a)
    w, h = 640, 360
    img = Image.new("RGB", (2 * w + 30, (len(ORDEM) - 1) * (h + 40) + 10), (12, 10, 30))
    dr = ImageDraw.Draw(img)
    linhas = []
    for k in range(1, len(ORDEM)):
        y = 10 + (k - 1) * (h + 40)
        dr.text((10, y), f"{ORDEM[k - 1]} (último quadro)  |  {ORDEM[k]} (primeiro quadro) · costura em {mmss(ini[k])}", font=fonte, fill=(240, 240, 255))
        A, B = qs[(k, 0)], qs[(k, 1)]
        img.paste(A.resize((w, h)), (10, y + 30))
        img.paste(B.resize((w, h)), (w + 20, y + 30))
        dif = np.abs(np.asarray(A, np.int16) - np.asarray(B, np.int16)).max(axis=2)
        linhas.append(f"{ORDEM[k - 1]} → {ORDEM[k]}  {mmss(ini[k])}  pixels que mudam (> 8) na costura: {(dif > 8).sum()} de {dif.size}")
    img.save(QA / f"costuras_{R}.jpg", quality=88)
    (QA / f"costuras_{R}.txt").write_text("Costuras entre lotes: último quadro de um lote × primeiro do seguinte (prancha costuras_v3.jpg)\n\n"
                                          + "\n".join(linhas) + "\n", encoding="utf-8")


if __name__ == "__main__" and "--extra" in __import__("sys").argv:
    print("\n".join(cortes()))
    costuras()
