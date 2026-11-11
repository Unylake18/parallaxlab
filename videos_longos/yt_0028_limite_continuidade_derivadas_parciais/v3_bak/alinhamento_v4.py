"""yt_0028 v4 (handoff v4 §8.2): QA de alinhamento no sistema novo (fundo violeta liso + grade que nasce dos eixos, papel.py v2).
Renderiza em 1080p SÓ os stills dos 37 alvos (still1080.sh, -s, sem vídeo) e mede no pixel:
  - a fase da grade dentro de cada painel (picos do perfil de brilho das linhas da grade, mediana entre muitas linhas/colunas);
  - a moldura nos 4 lados contra a linha da grade prevista por essa fase (resíduo ≤ 1 px);
  - a origem do painel contra o nó da grade medida (resíduo ≤ 1 px).
Do código (logs dos stills): o centro de cada seta da rede contra os nós ([alinha-setas]) e, nos alvos 07/20/22/30/31, as bordas das faixas
contra as linhas da grade ([alinha] faixa × [alinha] grade dos logs dos lotes).
Saídas: renders/v4/qa/alinhamento_v4.txt e alinhamento_v4.jpg (recorte 1:1 de um canto de painel por alvo).  uso: python alinhamento.py [--sem-render]"""
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from comparar import ALVO

U = Path(__file__).resolve().parent
Q = U / "renders" / "v4" / "qa"
D = Q / "alinhamento"
A_ = (120, 180, 1080, 900)
BE, BD = (120, 180, 840, 900), (1080, 180, 1800, 900)
C_ = [(120, 300, 600, 780), (720, 300, 1200, 780), (1320, 300, 1800, 780)]


def cel(u):
    p = .25
    while p * u < 20 and p < 1:
        p *= 2
    return p * u


# alvo → [(caixa, origem, px/u)]  (caixa None = grade de tela cheia)
PAIN = {}
for n in (1, 2, 8, 17, 18, 23, 24, 25, 26, 27, 28, 29, 35, 36, 37):
    PAIN[n] = [(A_, (600, 540), 120)]
ORD = {3: (1260, 576), 4: (1260, 576), 6: (1260, 576), 11: (1260, 576), 5: (1440, 540), 9: (1440, 576), 10: (1440, 576), 19: (1440, 576),
       14: (1260, 648), 15: (1296, 684), 16: (1296, 648)}
for n, o in ORD.items():
    PAIN[n] = [(BE, (480, 540), 144), (BD, o, 144)]
PAIN[21] = [(BE, (480, 540), 180), (BD, (1170, 540), 180)]
PAIN[20] = [(BE, (480, 540), 120), (BD, (1440, 540), 120)]
for n in (12, 32, 33, 34):
    PAIN[n] = [(c, ((c[0] + c[2]) // 2, 540), 60) for c in C_]
CHEIA = {7: ((600, 540), 240), 13: ((960, 540), 120), 22: ((600, 840), 88), 30: ((480, 420), 120), 31: ((360, 780), 150)}


def roda():
    tarefas = [(n, lote, round(f(), 2)) for n, (lote, f) in ALVO.items()]

    def um(t):
        n, lote, tt = t
        if (D / f"still1080_{n:02d}.png").exists():
            return f"{n:02d} já existe"
        r = subprocess.run(["bash", str(U / "still1080.sh"), lote, str(tt), f"{n:02d}"], capture_output=True, text=True, cwd=U)
        return r.stdout.strip()
    with ThreadPoolExecutor(6) as ex:
        for linha in ex.map(um, tarefas):
            print(linha, flush=True)


def picos(perf, lo, c, o):
    """Posições (sub-px) dos picos de um perfil 1D que começa em `lo`; casa cada pico com a linha prevista o + k·c mais próxima."""
    base = np.median(perf)
    des = []
    for i in range(2, len(perf) - 2):
        if perf[i] >= perf[i - 1] and perf[i] > perf[i + 1] and perf[i] > base + 3:
            w = perf[i - 1:i + 2] - base
            x = i + (w[2] - w[0]) / (2 * (2 * w[1] - w[0] - w[2]) + 1e-9) + lo + 0.5   # centro do pixel
            k = round((x - o) / c)
            d = x - (o + k * c)
            if abs(d) < c / 4:
                des.append(d)
    return (float(np.median(des)) if des else None), len(des)


def perfil(a, eixo, caixa, margem=6):
    x0, y0, x1, y1 = caixa
    lum = a.mean(2)
    reg = lum[y0 + margem:y1 - margem, x0 + margem:x1 - margem]
    if eixo == "x":
        return np.median(reg, axis=0), x0 + margem
    return np.median(reg, axis=1), y0 + margem


def borda(a, eixo, fixo, alvo, w=6):
    """Centro dos pixels claros da moldura (#CDC3F0 a 38 %) perto de `alvo` ao atravessar a borda."""
    lum = a.mean(2)
    perf = lum[fixo, alvo - w:alvo + w] if eixo == "x" else lum[alvo - w:alvo + w, fixo]
    base = np.median(perf)
    claros = np.nonzero(perf > base + 25)[0]
    if not len(claros):
        return None
    pes = perf[claros] - base
    return float((claros * pes).sum() / pes.sum()) + alvo - w + 0.5


def mede():
    L = ["yt_0028 v4 · alinhamento (§8.2) — fundo violeta liso, grade do eixo (papel.py v2); stills 1080p dos 37 alvos; critério ≤ 1 px",
         "por painel: fase da grade medida (picos do perfil de brilho; desvio mediano à grade prevista pela origem do eixo),",
         "moldura nos 4 lados (centro dos pixels claros) contra a linha da grade, origem contra o nó medido.", ""]
    pior = {"fase": 0.0, "moldura": 0.0, "setas": 0.0, "faixa": 0.0}
    for n, (lote, _) in ALVO.items():
        f = D / f"still1080_{n:02d}.png"
        if not f.exists():
            L.append(f"{n:02d} {lote}: still ausente")
            continue
        a = np.asarray(Image.open(f).convert("RGB"), float)
        itens = PAIN.get(n, [])
        if n in CHEIA:
            o, u = CHEIA[n]
            itens = [((max(0, o[0] - 2000), 150, 1910, 1070), o, u, True)]
        for it in itens:
            caixa, o, u = it[:3]
            cheia = len(it) > 3
            c = cel(u)
            if cheia:
                caixa = (0, 150, 1920, 1075)
            pr, lo = perfil(a, "x", caixa)
            dx, nx = picos(pr, lo, c, o[0])
            pr, lo = perfil(a, "y", caixa)
            dy, ny = picos(pr, lo, c, o[1])
            fs = max(abs(dx or 0), abs(dy or 0))
            pior["fase"] = max(pior["fase"], fs)
            txt = f"{n:02d} {lote:4s} {'tela cheia' if cheia else 'painel ' + str(caixa)} origem {o} {u} px/u (quadradinho {c:g} px): " \
                  f"fase da grade x {dx:+.2f} ({nx} linhas) · y {dy:+.2f} ({ny} linhas) → origem no nó: resíduo {fs:.2f} px" \
                if dx is not None and dy is not None else f"{n:02d} {lote:4s} {caixa}: grade não medida (x {nx}, y {ny} linhas)"
            if not cheia:
                x0, y0, x1, y1 = caixa
                ym, xm = (y0 + y1) // 2 + int(c / 2), (x0 + x1) // 2 + int(c / 2)
                med = {"esq": borda(a, "x", ym, x0), "dir": borda(a, "x", ym, x1), "topo": borda(a, "y", xm, y0), "base": borda(a, "y", xm, y1)}
                # linha da grade prevista na borda = alvo + fase medida
                gx, gy = (dx or 0), (dy or 0)
                res = {k: (None if v is None else v - (al + (gx if k in ("esq", "dir") else gy)))
                       for (k, v), al in zip(med.items(), (x0, x1, y0, y1))}
                ok = [abs(v) for v in res.values() if v is not None]
                r = max(ok) if ok else None
                pior["moldura"] = max(pior["moldura"], r or 0)
                txt += "\n      moldura × linha da grade: " + "  ".join(f"{k} {res[k]:+.2f}" if res[k] is not None else f"{k} —" for k in res) + \
                       f"  → {'OK' if r is not None and r <= 1 and fs <= 1 else 'VER'}"
            else:
                txt += f"  → {'OK' if fs <= 1 else 'VER'}"
            L.append(txt)
        lg = D / f"log_still_{n:02d}.txt"
        if lg.exists():
            for m in re.finditer(r"^\[alinha-setas\] (.*?) \| (.*?) \| (\d+) setas \| resíduo ([0-9.]+) px$", lg.read_text(encoding="utf-8", errors="replace"), re.M):
                pior["setas"] = max(pior["setas"], float(m.group(4)))
                L.append(f"      rede «{m.group(1)}» ({m.group(2)}): {m.group(3)} setas, centro × nó: resíduo {float(m.group(4)):.2f} px")
    # faixas e eixos nos alvos de gráfico (registro dos lotes)
    L += ["", "faixas (bordas) contra as linhas da grade do mesmo lote ([alinha] faixa × [alinha] grade):"]
    for log in sorted(U.glob("log_P*.txt")):
        t = log.read_text(encoding="utf-8", errors="replace")
        grades = [(float(m.group(1)), float(m.group(2)), float(m.group(4)), m.group(0)) for m in
                  re.finditer(r"origem \((-?[0-9.]+), (-?[0-9.]+)\) ([0-9.]+) px/u, quadradinho ([0-9.]+) px", t)]
        vistos = set()
        for m in re.finditer(r"^\[alinha\] faixa (.*?) (-?[0-9.]+) (-?[0-9.]+) (-?[0-9.]+) (-?[0-9.]+)$", t, re.M):
            v = tuple(float(m.group(k)) for k in range(2, 6))
            if v in vistos or not grades:
                continue
            vistos.add(v)

            def rg(g):
                ox, oy, c, _ = g
                rx = max(abs((x - ox) / c - round((x - ox) / c)) * c for x in (v[0], v[2]))
                ry = max(abs((y - oy) / c - round((y - oy) / c)) * c for y in (v[1], v[3]))
                return max(rx if v[0] == v[2] else 0.0, ry if v[1] == v[3] else 0.0)
            r, g = min((rg(g), g) for g in grades)
            pior["faixa"] = max(pior["faixa"], r)
            L.append(f"  {log.stem[4:]:4s} {m.group(1)}: ({v[0]:.0f}, {v[1]:.0f}) – ({v[2]:.0f}, {v[3]:.0f}) × grade origem ({g[0]:.0f}, {g[1]:.0f}), "
                     f"quadradinho {g[2]:g}: resíduo {r:.2f} px")
    L += ["", "eixos: nos alvos 07, 20, 22, 30 e 31 os eixos passam pela origem da vista, que é a origem da grade (mesma Vista) → resíduo 0 por construção;",
          "a fase medida acima confirma o nó da origem no pixel.", "",
          f"PIOR: fase/origem {pior['fase']:.2f} px · moldura {pior['moldura']:.2f} px · setas {pior['setas']:.2f} px · faixas {pior['faixa']:.2f} px"]
    (Q / "alinhamento_v4.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(l for l in L if "VER" in l or l.startswith("PIOR") or "ausente" in l))
    tiles, fonte = [], ImageFont.load_default()
    for n in ALVO:
        f = D / f"still1080_{n:02d}.png"
        if not f.exists():
            continue
        im = Image.open(f).convert("RGB")
        x, y = (PAIN[n][0][0][0], PAIN[n][0][0][1]) if n in PAIN else CHEIA[n][0]
        t = im.crop((x - 100, y - 100, x + 100, y + 100)).resize((200, 200))
        T = Image.new("RGB", (200, 218), (12, 10, 30))
        T.paste(t, (0, 18))
        ImageDraw.Draw(T).text((4, 3), f"{n:02d} ({x}, {y})", fill=(255, 220, 90), font=fonte)
        tiles.append(T)
    cols = 8
    pr = Image.new("RGB", (cols * 200, ((len(tiles) + cols - 1) // cols) * 218), (0, 0, 0))
    for i, T in enumerate(tiles):
        pr.paste(T, ((i % cols) * 200, (i // cols) * 218))
    pr.save(Q / "alinhamento_v4.jpg", quality=92)


if __name__ == "__main__":
    if "--sem-render" not in sys.argv:
        roda()
    mede()
