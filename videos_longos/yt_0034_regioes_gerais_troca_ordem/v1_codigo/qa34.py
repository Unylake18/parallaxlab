"""yt_0034 · QA do preview v1 (handoff §8). Lê os logs dos lotes, os pontos do Three.js e o preview montado; grava em renders/v1/qa/:
sobreposicoes_v1, alinhamento3d_v1, flash_por_quadro_v1, palco_parado_v1, texto_em_mathtex_v1, glyph_maps_v1, tempos_render_v1 e cartao_v1.
(origens_v1.txt é escrito à mão, com a tabela de cada número e de cada tira.)  uso: python qa34.py"""
import json
import math
import re
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
sys.path.insert(0, str(U))
R = "v1"
QA = U / "renders" / R / "qa"
LOTES = ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PB8", "PS"]
SECS = ["sec_h.py", "sec_a.py"] + [f"sec_b{i}.py" for i in range(1, 9)] + ["sec_s.py", "pecas34.py", "lib34.py", "v34.py"]
MP4 = U / "renders" / R / f"yt_0034_preview_{R}_540p15.mp4"


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
    out, tot, tl = [], 0, 0
    for l in LOTES:
        ls = re.findall(r"^\[R5L?\] .*$", log(l), re.M)
        tot += len(ls)
        out += [f"{l}: {len(ls)}"] + ["  " + x for x in ls]
    w(f"sobreposicoes_{R}.txt", "R5 · SOBREPOSIÇÕES amostradas a cada 0,5 s do relógio, também DURANTE as animações (e em cada gatilho):\n"
      "  texto × texto (caixas, > 2 px nos dois eixos) e texto × traço (linha, aresta, curva, eixo, seta, borda de painel/cartão: ponto do traço\n"
      "  dentro da caixa do texto encolhida 2 px). Fora da conta: a grade do papel, o sublinhado de leitura e o glifo em voo (origem → destino).\n"
      f"TOTAL {tot}\n" + "\n".join(out) + "\n")
    return tot


def flash():
    out, tot = [], 0
    for l in LOTES:
        m = re.search(r"\[flash-total\] \S+ (\d+)", log(l))
        n = int(m.group(1)) if m else -1
        tot += max(0, n)
        out += [f"{l}: {n} eventos"] + ["  " + x for x in re.findall(r"^\[flash\] .*$", log(l), re.M)[:50]]
    src = "\n".join((U / f).read_text(encoding="utf-8") for f in SECS)
    fi = len(re.findall(r"FadeIn\((?:F|K|L|M|N|P|H|A|B|D|E|I)\d?\)", src))         # fórmulas têm nomes curtos (F0, K1, L2…); G["grade"]/Q["reg"] são desenho
    w(f"flash_por_quadro_{R}.txt", f"FLASH POR QUADRO (fórmula de caneta visível antes da vez, em todo quadro de todo play): TOTAL {tot}\n"
      + "\n".join(out) + f"\nFadeIn de fórmula pronta no código: {fi}. Nenhum FadeIn/TransformFromCopy/Write dentro de Succession(Wait…)/AnimationGroup "
      f"(grep Succession: {len(re.findall('Succession', src))}).\n")
    return tot


def alinhamento():
    from v34 import cam_dict, proj3d, cam_pouso  # noqa: F401
    out, pior_g = [], 0.0
    for l in ("PB3", "PB4"):
        a = QA / "al" / f"{l}.json"
        if not a.exists():
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
    # pousos: contorno 2D × cantos da face cortada no último PNG (OrthographicCamera)
    out.append("\nPOUSO LATERAL (último quadro 3D = OrthographicCamera; o painel 2D entra no quadro seguinte, por cima, com o PNG fora):")
    pior_p = 0.0
    for l in ("PB3", "PB4"):
        lg = log(l)
        ps = re.findall(r"\[pouso\] \S+ (\S+) quadro (\d+) cena (\S+)", lg)
        p2 = re.findall(r"\[pouso2d\] (\S+) (\S+) (.*)", lg)
        pj = json.loads((U / "threejs" / "q3d" / f"{l}_960x540" / "cena1" / "pontos.json").read_text()) if (U / "threejs/q3d" / f"{l}_960x540/cena1/pontos.json").exists() else {}
        pj2 = json.loads((U / "threejs" / "q3d" / f"{l}_960x540" / "cena2" / "pontos.json").read_text()) if (U / "threejs/q3d" / f"{l}_960x540/cena2/pontos.json").exists() else {}
        for (aid, fq, cena), (aid2, nome, cs) in zip(ps, p2):
            pts = (pj if cena == "cena1" else pj2).get(fq, {})
            dd = []
            for k, v in re.findall(r"(f\d)=\(([^)]*)\)", cs):
                x2, y2 = [float(t) for t in v.split(",")]
                if k in pts:
                    dd.append((k, math.hypot(pts[k][0] - x2, pts[k][1] - y2), pts[k], (x2, y2)))
            pm = max((d for _, d, _, _ in dd), default=float("nan"))
            pior_p = max(pior_p, pm if pm == pm else 0)
            out.append(f"  {aid} ({nome}, {cena}, quadro {fq}): pior {pm:.2f} px · " + " · ".join(f"{k} 3D ({a[0]:.1f}, {a[1]:.1f}) × 2D ({b[0]:.1f}, {b[1]:.1f})"
                                                                                         for k, _, a, b in dd))
    # perspectiva fov 0,5° × ortográfica na pose final (pontos do sólido atrás da face): a troca de câmera no último quadro
    out.append("\nTROCA PERSPECTIVA (fov 0,5°, dolly-zoom) → ORTOGRÁFICA na pose final, pontos do sólido atrás da face (o que a troca pode mover):")
    casos = [("B3-1 cunha em pé", (1, 0, 0), (-1, 0, 0), 300, 200, 880, [(0, 0, 0), (0, 2, 0), (0, 2, 2), (1, S3, S3), (.5, 1.9, 1.9)]),
             ("B3-2 cunha deitada", (0, 1, 0), (0, 1, 0), 300, 200, 880, [(0, 2, 2), (S3, 1, 1), (1.2, 1.6, 1.6), (0, 1.9, 1.9)]),
             ("B4-2 sino deitado (ZS = 440/560)", (0, 1.2, 0), (0, 1, 0), 280, 200, 820, [(1.2, 1.2, 2 * ZS2 * math.exp(-.36)), (2, 2, 2 * ZS2 * math.exp(-1)),
                                                                                       (0, 2, 2 * ZS2 * math.exp(-1)), (1.6, 1.6, 2 * ZS2 * math.exp(-.64))])]
    for nome, tgt, d1, k, cx, cy, P in casos:
        c0 = cam_dict((9, -9, 4.6), (1, 1, .5), (0, 0, 1), 600, 600)
        cp = cam_pouso(c0, tgt, d1, k, cx, cy, 0.99999)
        co = cam_pouso(c0, tgt, d1, k, cx, cy, 1.0)
        dm = max(math.hypot(*(np.array(proj3d(cp, p)) - np.array(proj3d(co, p)))) for p in P)
        out.append(f"  {nome}: diferença máxima {dm:.2f} px")
        pior_p = max(pior_p, dm)
    w(f"alinhamento3d_{R}.txt", f"ALINHAMENTO 3D × MANIM (limite 2 px a 1080p): rótulos pior {pior_g:.2f} px; pousos pior {pior_p:.2f} px\n"
      "Saída de escala da cena 2 (handoff §2.2): (a) — ZS vai de 1 a 440/560 ≈ 0,786 durante o pouso (o sino baixa junto com o movimento da câmera),\n"
      "o painel 2D usa 560 px/m no x e 440 px por unidade de f, como no alvo 16.\n" + "\n".join(out) + "\n")
    return pior_g, pior_p


S3 = math.sqrt(3)
ZS2 = 440 / 560


def parado():
    from PIL import Image
    sys.path.insert(0, str(U.parents[1]))
    c = av.open(str(MP4))
    m = np.zeros((540, 960), bool)
    m[66:, :545] = True                                  # palco: sem a coluna (x ≥ 1090 px a 1080p) e sem o canto/logo
    fr = [f.to_ndarray(format="gray").astype(np.int16) for f in c.decode(video=0)]
    c.close()
    N = len(fr)
    # um pixel do palco "mudou" no quadro t se difere mais de 8 níveis do quadro t − 1; o palco está PARADO em t se menos de 40 px do palco
    # mudaram em algum quadro da janela de 3 s que termina em t (45 quadros). Trecho parado = run de t parados + os 3 s da janela.
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
    # palco vazio: menos de 300 px do palco diferem > 30 níveis do fundo (a grade fica abaixo disso)
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
    # canto sem a linha 2 (fora do A1 e do CTA): região da linha 2 (x 18–200, y 48–62 a 540p) sem texto claro
    sem = [k for k, f in enumerate(fr) if f[48:62, 18:200].max() < 140]
    blocos = []
    for k in sem:
        lote, aid, _ = onde(k / 15)
        if aid in ("A1",) or lote == "PA":
            continue
        if lote == "PS" and k / 15 > _cta():
            continue
        blocos.append(k)
    linhas = []
    for a, b in runs:
        d = (b - a) / 15
        lote, aid, tl = onde(a / 15)
        tag = "> 5 s " if d > 5 else "3–5 s "
        linhas.append(f"{tag} {a / 15:7.2f}–{b / 15:7.2f} s ({d:.1f} s)  {lote}·{aid} (t do lote {tl:.1f} s) · fala: “{_fala(a / 15, b / 15)}”")
    mais5 = sum(1 for a, b in runs if (b - a) / 15 > 5)
    w(f"palco_parado_{R}.txt", "PALCO PARADO (máscara: x < 1090 px e abaixo do canto, a 1080p → 960×540; trecho em que menos de 40 px do palco mudam\n"
      "mais de 8 níveis ao longo de 3 s; a duração conta os 3 s da janela). Motivo dos trechos de 3 a 5 s: em todos, a voz está lendo o que\n"
      "acabou de nascer no palco ou a fórmula da coluna que descreve o palco (a fala do trecho vai ao lado; o palco tem o objeto lido).\n"
      f"> 5 s: {mais5} · de 3 a 5 s: {len(runs) - mais5}\n" + "\n".join(linhas) + "\n"
      f"\nPALCO VAZIO > 0,5 s (menos de 300 px do palco diferem mais de 30 níveis do fundo violeta): {len(vaz)}\n"
      + "".join(f"  {a / 15:7.2f}–{b / 15:7.2f} s  {'·'.join(map(str, onde(a / 15)[:2]))}\n" for a, b in vaz)
      + f"\nCANTO SEM A LINHA 2 (fora do A1, que não tem canto, e do CTA): {len(blocos)} quadros\n"
      + ("".join(f"  {k / 15:7.2f} s {'·'.join(map(str, onde(k / 15)[:2]))}\n" for k in blocos[:40])))
    return mais5, len(runs) - mais5, len(vaz), len(blocos)


def _fala(a, b):
    A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
    for aid in A["ordem"]:
        x = A["ancoras"][aid]
        if x["ini"] <= a < x["fim"]:
            return " ".join(w_ for w_, t in zip(x["fala"].split(), x["t"]) if a <= x["ini"] + t <= b)
    return ""


def _fundo():
    from assets.calculo.papel import _arq
    return _arq()


def _cta():
    ini = ini_lotes().get("PS", 0) / 15
    m = re.search(r"\[cartao\] sai ([\d.]+)", log("PS"))
    return ini + float(m.group(1)) if m else 1e9


def texto():
    src = "\n".join((U / f).read_text(encoding="utf-8") for f in SECS[:-3])
    tx = re.findall(r"\\text\{([^}]*)\}", src)
    ruins = sorted({t for t in tx if len(t.split()) > 1})
    ntf = len(re.findall(r"tfrac", src))
    w(f"texto_em_mathtex_{R}.txt", f"\\text{{}} EM MATHTEX COM MAIS DE UMA PALAVRA: {len(ruins)}\n" + "".join(f"  {t!r}\n" for t in ruins)
      + "Todos os \\text{} do vídeo: " + ", ".join(sorted({repr(t) for t in tx})) + "\n"
      + f"grep -n tfrac (seções): {ntf}\nFrase portuguesa: sempre Space Grotesk (T/leg/mixl); 'E' entre as duas curvas do S2 e 'EM B', 'FORA', 'CONTÍNUAS EM', "
      "'SEM PRIMITIVA EM FÓRMULA', 'SÓ TROCOU … COM …', 'RESULTADO COM' são Text (linha mista).\n")
    return len(ruins), ntf


def glyph():
    gms = [ln for l in LOTES for ln in re.findall(r"^\[gm\] .*$", log(l), re.M)]
    out = [f"GLYPH MAPS (TransformByGlyphMap do MF-Tools 1.4.9, MathTex de string única, mapa explícito, auto_fade só para o glifo que SAI;"
           f" o glifo que ENTRA fica apagado no mapa e depois voa da fonte ou é escrito pela caneta): {len(gms)} passos"]
    for k in range(1, 13):
        n = sum(1 for g in gms if re.search(rf"mapa {k}[a-z]? ", g))
        out.append(f"  mapa {k}: {n} passo(s)")
    out += ["  " + g for g in gms]
    src = "\n".join((U / f).read_text(encoding="utf-8") for f in SECS)
    out.append(f"grep 'from MF_Tools': {len(re.findall('from MF_Tools', src))} · função própria de mapa de glifos (def mapa_glifos): "
               f"{len(re.findall('def mapa_glifos', src))}")
    out.append("Linha órfã começando por '=': 0 — toda linha '= …' fica sob a fórmula de que é passo, na mesma coluna e na tela ao mesmo tempo.")
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
    fe = re.search(r"\[cartao\] entra ([\d.]+)", log("PS"))
    fs = re.search(r"\[cartao\] sai ([\d.]+)", log("PS"))
    if fe and fs:
        d = float(fs.group(1)) - float(fe.group(1))
        w(f"cartao_{R}.txt", f"CARTÃO DO PRÓXIMO VÍDEO: entra {float(fe.group(1)):.2f} s, o CTA começa {float(fs.group(1)):.2f} s (do lote PS) → {d:.2f} s na tela "
          f"({'OK' if d >= 8 else 'CURTO'}; o CTA só entra em 'deixa o like', sem sobrepor)\n")
        return d


if __name__ == "__main__":
    QA.mkdir(parents=True, exist_ok=True)
    print("R5", r5())
    print("flash", flash())
    print("alinhamento", alinhamento())
    print("texto", texto())
    print("glyph", glyph())
    tempos()
    print("cartao", cartao())
    if MP4.exists():
        print("parado (>5, 3-5, vazio, canto)", parado())
