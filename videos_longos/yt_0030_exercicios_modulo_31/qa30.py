"""yt_0030 · QA do preview (handoff v1 §8): relatórios em renders/<rodada>/qa/ a partir dos logs dos lotes e do preview emendado.
  transicoes_<r>.txt   R10: trocas de layout ([troca]) com o tempo no preview + varredura do vídeo (tela só com canto/logo > 0,8 s) + [r10] dos lotes
  holds_<r>.txt        trechos com a imagem parada > 3 s (diferença entre quadros ≤ 1/255 fora do chip) e a fala que os justifica
  sobreposicoes_<r>.txt  R5 em cada gatilho ([sobrepos] / [sobrepos-chk], render com QA_SOBREPOS=1)
  setas_na_chapa_<r>.txt R7 ([r7] setas, [r7t] textos/placas cruzando moldura, [r7l] linhas auxiliares fora da moldura)
  pausas_<r>.txt       as tags PAUSE E TENTE (início e fim no preview)
  alinhamento_<r>.txt  [alinha] chapas/grades/origens e [alinha-setas] (resíduo dos centros das setas nos nós)
uso: python qa30.py [rodada]"""
import json
import re
import sys
from pathlib import Path

import av
import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
ROOT = U.parents[1]
sys.path.insert(0, str(U))
from tempos import ANC_DADOS  # noqa: E402

RODADA = sys.argv[1] if len(sys.argv) > 1 else "v1"
R = U / "renders" / RODADA
OUT = R / "qa"
OUT.mkdir(parents=True, exist_ok=True)
INFO = json.loads((R / f"lotes_{RODADA}.json").read_text(encoding="utf-8"))
INI = {k: v / 15 for k, v in INFO["inicio"].items()}
ORDEM = list(INFO["inicio"])
LOG = {l: (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace") for l in ORDEM}
mmss = lambda t: f"{int(t) // 60}:{t % 60:05.2f}"


def ancora_t(lote):
    return {m.group(1): float(m.group(2)) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", LOG[lote])}


def fala_em(t_abs):
    """Âncora e trecho da fala (orçamento) no instante absoluto t."""
    A = ANC_DADOS["ancoras"]
    for aid in ANC_DADOS["ordem"]:
        a = A[aid]
        if a["ini"] <= t_abs < a["fim"]:
            k = int((t_abs - a["ini"]) * 3)
            pal = a["fala"].split()
            return aid, " ".join(pal[max(0, k - 2):k + 10])
    return "-", ""


def transicoes():
    L = [f"yt_0030 {RODADA} · R10 (handoff §2.5/§5): o layout novo entra enquanto o antigo sai; nenhuma tela com menos de um objeto além do canto e do logo "
         f"por mais de 0,8 s. Entre lotes, a costura de 0,4 s (montar.py) sobrepõe a saída do lote anterior à entrada do seguinte.", "", "TROCAS DE LAYOUT:"]
    n = 0
    for l in ORDEM:
        for m in re.finditer(r"\[troca\] \S+ (\S+) ([0-9.]+) (.+)", LOG[l]):
            n += 1
            L.append(f"  {n:2d}. {mmss(INI[l] + float(m.group(2)))}  {l:5s} {m.group(1):6s} {m.group(3)}")
    r10 = sum(int(m.group(1)) for l in ORDEM for m in re.finditer(r"\[r10-total\] \S+ (\d+)", LOG[l]))
    L += ["", f"[r10] nos lotes (quadro a quadro, durante as animações): {r10} trechos de tela vazia > 0,8 s"]
    # varredura do vídeo emendado: conteúdo fora do canto (x < 900, y < 140), do logo (x > 800, y < 70) e do chip (x > 780, y > 470), a 960×540
    fundo = np.asarray(Image.open(ROOT / "assets/calculo/fundo_calculo_violeta_liso_960x540.png").convert("RGB"), np.int16)
    mask = np.ones((540, 960), bool)
    mask[:70, :] = False
    mask[:140, :480] = False
    mask[470:, 780:] = False
    c = av.open(str(R / f"yt_0030_preview_{RODADA}_540p15.mp4"))
    vazios, run, ini = [], 0, 0
    for i, fr in enumerate(c.decode(video=0)):
        a = fr.to_ndarray(format="rgb24").astype(np.int16)
        d = np.abs(a - fundo).max(axis=2)
        cheio = (d[mask] > 24).sum() > 40
        if not cheio:
            if run == 0:
                ini = i
            run += 1
        else:
            if run > 12:
                vazios.append((ini, run))
            run = 0
    c.close()
    L.append(f"varredura do preview emendado: {len(vazios)} trechos com a tela só com canto/logo por mais de 0,8 s")
    for i0, k in vazios:
        L.append(f"  {mmss(i0 / 15)} · {k / 15:.2f} s")
    L.append("")
    L.append(f"OCORRÊNCIAS: {len(vazios) + r10}")
    (OUT / f"transicoes_{RODADA}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    return len(vazios) + r10


def holds():
    c = av.open(str(R / f"yt_0030_preview_{RODADA}_540p15.mp4"))
    prev, run, ini, out = None, 0, 0, []
    for i, fr in enumerate(c.decode(video=0)):
        a = np.asarray(fr.to_ndarray(format="rgb24"), np.int16)[:, :, 1]
        a[470:, 780:] = 0                       # o chip PAUSE E TENTE não conta como movimento
        if prev is not None and np.abs(a - prev).max() <= 3:
            if run == 0:
                ini = i - 1
            run += 1
        else:
            if run + 1 > 45:
                out.append((ini, run + 1))
            run = 0
        prev = a
    c.close()
    if run + 1 > 45:
        out.append((ini, run + 1))
    L = [f"yt_0030 {RODADA} · holds > 3 s (imagem parada; o chip PAUSE E TENTE não conta). Em todos a voz continua (WAV contínuo): o quadro fica parado "
         f"enquanto a fala explica o que está na tela. Motivo = o trecho da narração no início do hold.", ""]
    for i0, k in out:
        t0 = i0 / 15
        aid, txt = fala_em(t0 + 0.5)
        flag = "  ← > 6 s" if k / 15 > 6 else ""
        L.append(f"{mmss(t0)} · {k / 15:5.2f} s · {aid:6s} · fala: «{txt}…»{flag}")
    L += ["", f"total: {len(out)} holds > 3 s; {sum(1 for _, k in out if k / 15 > 6)} acima de 6 s"]
    (OUT / f"holds_{RODADA}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    return out


def sobreposicoes():
    L = [f"yt_0030 {RODADA} · R5 (sobreposição) medida em cada gatilho e no fim de cada âncora: texto × texto (caixas) e seta × texto (a seta INTEIRA, "
         f"haste e ponta, + 4 px + meia espessura).", ""]
    tot, chk = 0, 0
    for l in ORDEM:
        f = U / f"log_sob_{l}.txt"
        Ls = f.read_text(encoding="utf-8", errors="replace") if f.exists() else LOG[l]
        oc = re.findall(r"\[sobrepos\] (.+)", Ls)
        ck = re.findall(r"\[sobrepos-chk\] .+: (\d+) textos, (\d+) setas visíveis, (\d+) ocorrências", Ls)
        chk += len(ck)
        tot += len(oc)
        L.append(f"{l:5s}: {len(ck):3d} checagens · {len(oc)} ocorrências")
        L += [f"   {o}" for o in oc]
    L += ["", f"TOTAL: {chk} checagens · {tot} ocorrências"]
    (OUT / f"sobreposicoes_{RODADA}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    return tot


def setas_na_chapa():
    L = [f"yt_0030 {RODADA} · R7 (seta na chapa), quadro a quadro durante as animações: seta a ≥ 18 px da moldura da sua chapa; nenhum texto ou placa "
         f"cruzando moldura; linhas auxiliares (retas, diagonais, paredes, hachuras, hipérboles, eixos) recortadas na moldura.", ""]
    T = [0, 0, 0]
    for l in ORDEM:
        a = re.search(r"\[r7-total\] \S+ (\d+) ocorrências em (\d+)", LOG[l])
        b = re.search(r"\[r7t-total\] \S+ (\d+)", LOG[l])
        c = re.search(r"\[r7l-total\] \S+ (\d+)", LOG[l])
        v = [int(a.group(1)), int(b.group(1)), int(c.group(1))]
        T = [x + y for x, y in zip(T, v)]
        L.append(f"{l:5s}: setas {v[0]} · textos/placas {v[1]} · linhas {v[2]} (quadros checados: {a.group(2)})")
        L += [f"   {o}" for o in re.findall(r"(\[r7[tl]?\] .+)", LOG[l])[:20]]
    L += ["", f"TOTAL: setas {T[0]} · textos/placas {T[1]} · linhas {T[2]}"]
    (OUT / f"setas_na_chapa_{RODADA}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    return T


def pausas():
    L = [f"yt_0030 {RODADA} · PAUSE E TENTE (chip no canto inferior direito; FadeIn 0,3 s · ≈ 3 s · FadeOut 0,3 s; a voz não para)", ""]
    n = 0
    for l in ORDEM:
        for m in re.finditer(r"\[pausa\] \S+ (\S+) ([0-9.]+) ([0-9.]+)", LOG[l]):
            n += 1
            L.append(f"{n:2d}. {m.group(1):6s} {mmss(INI[l] + float(m.group(2)))} → {mmss(INI[l] + float(m.group(3)))}")
    L += ["", f"total: {n} (esperado: 10)"]
    (OUT / f"pausas_{RODADA}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    return n


def alinhamento():
    L = [f"yt_0030 {RODADA} · alinhamento (px a 1080p). Cada painel: a grade nasce da origem da vista (passo 0,25 u; 0,5 u se < 20 px); a moldura tem de cair "
         f"numa linha da grade nos 4 lados (resíduo ≤ 1 px) e a origem num nó; os centros das setas de rede, nos nós.", ""]
    piores = 0.0
    for l in ORDEM:
        grades = re.findall(r"\[alinha\] grade (.+?) origem \(([-0-9.]+), ([-0-9.]+)\) ([0-9.]+) px/u, quadradinho ([0-9.]+) px ([-0-9.]+) ([-0-9.]+) ([-0-9.]+) ([-0-9.]+)", LOG[l])
        chapas = re.findall(r"\[alinha\] chapa (.+?) ([-0-9.]+) ([-0-9.]+) ([-0-9.]+) ([-0-9.]+)$", LOG[l], re.M)
        vistos = set()
        for g in grades:
            nome, cx, cy, u, c = g[0], float(g[1]), float(g[2]), float(g[3]), float(g[4])
            box = next(((float(a), float(b), float(cc), float(d)) for n_, a, b, cc, d in chapas if n_.strip() == nome.strip()), None)
            if box is None or (nome, box) in vistos:
                continue
            vistos.add((nome, box))
            res = max(abs((box[0] - cx) / c - round((box[0] - cx) / c)) * c, abs((box[2] - cx) / c - round((box[2] - cx) / c)) * c,
                      abs((box[1] - cy) / c - round((box[1] - cy) / c)) * c, abs((box[3] - cy) / c - round((box[3] - cy) / c)) * c)
            piores = max(piores, res)
            L.append(f"{l:5s} {nome[:44]:44s} moldura {tuple(int(v) for v in box)} · origem ({cx:.0f}, {cy:.0f}) · {u:g} px/u · quadradinho {c:g} px · resíduo {res:.2f} px")
        for m in re.finditer(r"\[alinha-setas\] (.+?) \| origem .+?\| (\d+) setas \| resíduo ([0-9.]+) px", LOG[l]):
            L.append(f"{l:5s}   setas · {m.group(1)[:40]:40s} {m.group(2):>4s} setas · resíduo dos centros nos nós {m.group(3)} px")
    L += ["", f"maior resíduo moldura × grade: {piores:.2f} px",
          "Observação: nos cartões (layout C) a rede tem passo 0,75 u (handoff §2.4) e o quadradinho da grade é 0,5 u, então metade das setas fica a meio",
          "quadradinho dos nós (resíduo 15 px) por definição; nos layouts A e B (passo 0,5 u) o resíduo esperado é 0."]
    (OUT / f"alinhamento_{RODADA}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    return piores


if __name__ == "__main__":
    print("transições (ocorrências):", transicoes())
    print("sobreposições:", sobreposicoes())
    print("setas na chapa:", setas_na_chapa())
    print("pausas:", pausas())
    print("alinhamento (pior resíduo px):", alinhamento())
    h = holds()
    print("holds > 3 s:", len(h), "· > 6 s:", sum(1 for _, k in h if k / 15 > 6))
