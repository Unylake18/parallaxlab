"""yt_0031 · relatórios de QA do preview v1 (renders/v1/qa/):
  flash_v1.txt          FLASH POR QUADRO (portão do kit: fórmula de caneta visível antes da vez), por lote
  sobreposicoes_v1.txt  R5 em cada gatilho (caixas de texto/MathTex entre si e com pontos marcados)
  alinhamento3d_v1.txt  rótulos do Manim (projeção Python da mesma câmera) × pontos do three.js (pontos.json) no mesmo quadro;
                        nos pousos, os 4 cantos da chapa 3D (vista de cima) × a chapa 2D (360/840 × 300/780 px)
  parado_v1.txt         trechos com a imagem parada > 3 s no preview inteiro (diferença entre quadros)
  tempos_render_v1.txt  tempo de render por bloco (registro)
uso: python qa31.py"""
import json
import re
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
QA = U / "renders" / "v1" / "qa"
ORDEM = ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PB8", "PB9", "PS"]
COM3D = ["PB1", "PB2", "PB5", "PB6", "PS"]


def log(l):
    return (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="ignore")


def flash():
    linhas, tot = [], 0
    for l in ORDEM:
        t = log(l)
        n = int(re.findall(r"\[flash-total\] \S+ (\d+)", t)[-1])
        tot += n
        linhas.append(f"{l:4s} flash = {n}")
        linhas += ["   " + x for x in re.findall(r"\[flash\].*", t)[:20]]
    (QA / "flash_v1.txt").write_text("FLASH POR QUADRO (fórmula/legenda de caneta visível antes de ser escrita), por lote\n" + "\n".join(linhas) +
                                     f"\n\nTOTAL = {tot}\n", encoding="utf-8")
    return tot


def r5():
    linhas, tot, ng = [], 0, 0
    for l in ORDEM:
        t = log(l)
        ev = re.findall(r"\[R5\].*", t)
        g = len(re.findall(r"\[gatilho\]", t))
        ng += g
        tot += len(ev)
        linhas.append(f"{l:4s} gatilhos = {g:3d}  sobreposições = {len(ev)}")
        linhas += ["   " + x for x in ev]
    (QA / "sobreposicoes_v1.txt").write_text(
        "R5 · em cada gatilho: caixas (px) dos textos e MathTex visíveis entre si e com os pontos marcados (_obst). Não cobre texto × aresta do 3D\n"
        "nem texto × linha fina (o teste é por caixa).\n\n" + "\n".join(linhas) + f"\n\nTOTAL = {tot} em {ng} gatilhos\n", encoding="utf-8")
    return tot, ng


def alinhamento():
    out, pior, n = [], 0.0, 0
    for l in COM3D:
        arq = QA / "al" / f"{l}.json"
        if not arq.exists():
            out.append(f"{l}: sem registro de rótulos")
            continue
        reg = json.loads(arq.read_text(encoding="utf-8"))
        cache, dl, nl = {}, 0.0, 0
        for lote, cena, fq, nome, x, y in reg:
            if cena not in cache:
                p = U / "threejs" / "q3d" / f"{lote}_960x540" / cena / "pontos.json"
                cache[cena] = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
            js = cache[cena].get(str(fq))
            if not js or nome not in js:
                continue
            d = max(abs(js[nome][0] - x), abs(js[nome][1] - y))
            dl, nl = max(dl, d), nl + 1
        pior, n = max(pior, dl), n + nl
        out.append(f"{l}: {nl} amostras rótulo×ponto (quadro a quadro), pior diferença = {dl:.2f} px")
        # pousos: quadros com a câmera de cima
        ped = json.loads((U / "threejs" / "pedidos3d" / f"{l}.json").read_text(encoding="utf-8"))
        esperado = {"c00": (360, 780), "c20": (840, 780), "c22": (840, 300), "c02": (360, 300)}
        for cena, lista in ped["cenas"].items():
            pts = cache.get(cena) or json.loads((U / "threejs" / "q3d" / f"{l}_960x540" / cena / "pontos.json").read_text(encoding="utf-8"))
            topo = [f for f, e in lista if abs(e["cam"]["pos"][2] - 11.575) < 0.01 and abs(e["cam"]["pos"][0] - 1) < 1e-3]
            if not topo:
                out.append(f"   {cena}: sem quadro de pouso (entra direto na câmera do alvo)")
                continue
            dc = max(max(abs(pts[str(f)][k][0] - v[0]), abs(pts[str(f)][k][1] - v[1])) for f in topo for k, v in esperado.items())
            out.append(f"   {cena}: pouso (vista de cima) em {len(topo)} quadros; cantos da chapa 3D × chapa 2D: pior = {dc:.2f} px")
    (QA / "alinhamento3d_v1.txt").write_text(
        "Alinhamento 3D × Manim. Os rótulos do Manim são presos à projeção Python da mesma câmera do c31.js (a câmera vai no estado de cada\n"
        "quadro); aqui cada posição registrada no render é comparada ao ponto que o three.js projetou no mesmo quadro (pontos.json).\n"
        "Critério: ≤ 2 px. Pousos: 0 px esperado nos 4 cantos.\n\n" + "\n".join(out) + f"\n\nTOTAL: {n} amostras, pior = {pior:.2f} px\n", encoding="utf-8")
    return pior, n


def parado(lim=3.0, tol=0.6):
    """Trechos em que nenhum pixel muda mais que o ruído (média da diferença absoluta < tol/255) por mais de `lim` s."""
    lotes = json.loads((U / "renders" / "v1" / "lotes_v1.json").read_text(encoding="utf-8"))["inicio_s"]
    anc = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
    c = av.open(str(U / "renders" / "v1" / "yt_0031_preview_v1_540p15.mp4"))
    ant, ini, runs, i = None, None, [], 0
    for fr in c.decode(video=0):
        a = fr.to_ndarray(format="gray")[::2, ::2].astype(np.int16)
        if ant is not None:
            d = np.abs(a - ant)
            mexe = (d > 12).sum() > 6
            if not mexe:
                ini = i if ini is None else ini
            else:
                if ini is not None and (i - ini) / 15 > lim:
                    runs.append((ini / 15, i / 15))
                ini = None
        ant = a
        i += 1
    c.close()
    linhas = []
    for a, b in runs:
        lote = [l for l, t in lotes.items() if t <= a][-1]
        linhas.append(f"{int(a // 60)}:{a % 60:05.2f} – {int(b // 60)}:{b % 60:05.2f}  ({b - a:4.1f} s)  lote {lote}")
    (QA / "parado_v1.txt").write_text(f"Trechos com a imagem parada por mais de {lim:.0f} s (nenhum movimento além de 6 px com diferença > 12/255)\n"
                                      f"no preview inteiro: {len(runs)} trechos.\n\n" + "\n".join(linhas) + "\n", encoding="utf-8")
    return runs


def tempos():
    linhas, tot = [], 0
    for l in ORDEM:
        t = log(l)
        r = re.findall(r"\[render\] \S+ (\d+)s", t)
        s = int(r[-1]) if r else 0
        t3 = (U / f"tempo3d_{l}.txt")
        s3 = int(re.findall(r"(\d+)s", t3.read_text())[-1]) if t3.exists() else 0
        dur = float(re.findall(r"\[tempo\] total ([\d.]+)s", t)[-1])
        q3 = ""
        l3 = U / f"log_3d_{l}.txt"
        if l3.exists():
            m = re.findall(r'"renderizados":(\d+),"copiados":(\d+),"segundos":([\d.]+),"s_por_quadro":([\d.]+)', l3.read_text(encoding="utf-8", errors="ignore"))
            if m:
                q3 = f"  3D: {m[-1][0]} quadros novos + {m[-1][1]} cópias em {m[-1][2]} s ({m[-1][3]} s/quadro)"
        tot += s + s3
        linhas.append(f"{l:4s} vídeo {dur:7.2f} s   render Manim {s:4d} s" + (f"   + passagem seca e three.js {s3:4d} s" if s3 else "") + q3)
    (QA / "tempos_render_v1.txt").write_text("Tempo de render por bloco (960×540, 15 fps; 3 lotes em paralelo; só para registro)\n\n" + "\n".join(linhas) +
                                             f"\n\nsoma = {tot / 60:.1f} min de máquina\n", encoding="utf-8")


if __name__ == "__main__":
    print("flash", flash())
    print("R5", r5())
    print("alinhamento", alinhamento())
    tempos()
    print("parado", len(parado()))
