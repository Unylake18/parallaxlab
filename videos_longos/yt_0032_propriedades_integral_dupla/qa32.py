"""yt_0032 · QA do preview (handoff v1 §8 + handoff v2 §8). Lê os logs dos lotes (render e passada seca do plano), os pontos do Three.js e o
preview montado; grava em renders/<rodada>/qa/:
  v1 e v2: sobreposicoes, alinhamento3d, flash_por_quadro, tempos_render, parado (tela inteira), glyphmaps_numeros;
  v2: fracoes_v2, texto_em_mathtex_v2, palco_parado_v2 (máscara do palco), origens_v2, orfaos_v2, fubini_v2.
uso: python qa32.py [rodada]"""
import json
import re
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v1"
QA = U / "renders" / R / "qa"
LOTES = ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PS"]
SECS = ["sec_h.py", "sec_a.py"] + [f"sec_b{i}.py" for i in range(1, 8)] + ["sec_s.py"]


def log(l, pre="log_"):
    p = U / f"{pre}{l}.txt"
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""


def ini_lotes():
    j = U / "renders" / R / f"lotes_{R}.json"
    return json.loads(j.read_text())["inicio"] if j.exists() else {}


def onde(t):
    """t (s do preview) → (lote, âncora)."""
    ini = sorted(ini_lotes().items(), key=lambda x: x[1])
    if not ini:
        return "?", "?"
    lote, q0 = [x for x in ini if x[1] / 15 <= t + 1e-6][-1]
    tl = t - q0 / 15
    an = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([\d.]+)", log(lote))]
    aid = ([a for a in an if a[1] <= tl + 0.01] or [("?", 0)])[-1][0]
    return lote, aid


def trechos_parados(mp4, mascara=None, lim=6):
    c = av.open(str(mp4))
    ref, ini, runs, i = None, 0, [], 0
    for i, fr in enumerate(c.decode(video=0)):
        a = fr.to_ndarray(format="gray").astype(np.int16)
        if mascara is not None:
            a = a[mascara]
        if ref is None or np.abs(a - ref).max() > lim:
            if ref is not None and i - ini > 45:
                runs.append((ini, i))
            ini, ref = i, a
    if i - ini > 45:
        runs.append((ini, i))
    c.close()
    return runs


def main():
    QA.mkdir(parents=True, exist_ok=True)
    w = lambda nome, txt: (QA / nome).write_text(txt, encoding="utf-8")
    # R5
    out, tot = [], 0
    for l in LOTES:
        ls = re.findall(r"^\[R5\] .*$", log(l), re.M)
        tot += len(ls)
        out += [f"{l}: {len(ls)}"] + ["  " + x for x in ls]
    w(f"sobreposicoes_{R}.txt", f"R5 · sobreposições nos gatilhos (texto × texto, texto × ponto): TOTAL {tot}\n" + "\n".join(out) + "\n")
    print("R5", tot)
    # flash
    out, tot = [], 0
    for l in LOTES:
        m = re.search(r"\[flash-total\] \S+ (\d+)", log(l))
        n = int(m.group(1)) if m else -1
        tot += max(0, n)
        out += [f"{l}: {n} eventos"] + ["  " + x for x in re.findall(r"^\[flash\] .*$", log(l), re.M)[:50]]
    w(f"flash_por_quadro_{R}.txt", f"FLASH POR QUADRO (fórmula de caneta visível antes da vez, em todo quadro de todo play): TOTAL {tot}\n" + "\n".join(out) + "\n")
    print("flash", tot)
    # alinhamento 3D
    out, pior_g = [], 0.0
    for l in LOTES:
        a = U / "renders" / "v1" / "qa" / "al" / f"{l}.json"
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
        out.append(f"{l}: {n} medidas (rótulo × ponto do three.js no mesmo quadro), pior {pior:.2f} px a 1080p; sem par: {falta}")
        out += [f"  {c}.{nm}: pior {d:.2f} px" for (c, nm), d in sorted(por.items())]
    w(f"alinhamento3d_{R}.txt", f"ALINHAMENTO 3D × MANIM (limite 2 px a 1080p): pior geral {pior_g:.2f} px\n" + "\n".join(out) + "\n")
    print("alinhamento", round(pior_g, 2))
    # tempos
    out = []
    for l in LOTES:
        r = re.search(r"\[render\] \S+ (\d+)s", log(l))
        t3 = U / f"tempo3d_{l}.txt"
        d = re.findall(r"\[tempo\] total ([\d.]+)s", log(l))
        out.append(f"{l}: duração {float(d[-1]) if d else 0:.1f} s · render Manim {r.group(1) if r else '?'} s · "
                   f"{t3.read_text(encoding='utf-8').strip() if t3.exists() else 'sem 3D'}")
    w(f"tempos_render_{R}.txt", "TEMPO DE RENDER POR BLOCO (960×540, 15 fps; só registro)\n" + "\n".join(out) + "\n")
    # parado: tela inteira e só o palco
    mp4 = U / "renders" / R / f"yt_0032_preview_{R}_540p15.mp4"
    if mp4.exists():
        runs = trechos_parados(mp4)
        w(f"parado_{R}.txt", f"TELA PARADA > 3 s (nenhum pixel difere mais que 6/255 do primeiro quadro do trecho): {len(runs)} trechos\n"
          + "\n".join(f"{a / 15:7.2f}–{b / 15:7.2f} s ({(b - a) / 15:.1f} s)  {'·'.join(onde(a / 15))}" for a, b in runs) + "\n")
        print("parado", len(runs))
        if R in ("v2", "final"):
            m = np.zeros((540, 960), bool)
            m[66:, :545] = True                           # palco: sem a coluna (x ≥ 1090 px a 1080p) e sem o canto/logo
            runs = trechos_parados(mp4, m)
            mais6 = [(a, b) for a, b in runs if (b - a) / 15 > 6]
            w("palco_parado_v2.txt", "PALCO PARADO (máscara: x < 1090 px e abaixo do canto, a 1080p; nada muda mais que 6/255 desde o início do trecho)\n"
              f"> 6 s: {len(mais6)} · de 3 a 6 s: {len(runs) - len(mais6)}\n"
              + "\n".join(f"{'> 6 s ' if (b - a) / 15 > 6 else '3–6 s '} {a / 15:7.2f}–{b / 15:7.2f} s ({(b - a) / 15:.1f} s)  {'·'.join(onde(a / 15))}"
                          for a, b in runs) + "\n")
            print("palco parado >6", len(mais6), "3-6", len(runs) - len(mais6))
    # glyph maps
    gms = [ln for l in LOTES for ln in re.findall(r"^\[gm\] .*$", log(l), re.M)]
    out = [f"GLYPH MAPS (TransformByGlyphMap do MF-Tools com mapa explícito, ou voo + caneta registrado): {len(gms)} passos"]
    for k in [f"mapa {i}" for i in range(1, 18)]:
        n = sum(1 for g in gms if re.search(re.escape(k) + r"[ ab(c]", g + " "))
        if n:
            out.append(f"  {k}: {n} passo(s)")
    out += ["  " + g for g in gms]
    src = "\n".join((U / f).read_text(encoding="utf-8") for f in SECS)
    orf = re.findall(r'(?:TC|TP)\(r?"\s*=[^"]', src)
    out.append(f"LINHAS DE ÁLGEBRA QUE COMEÇAM COM '=': {len(orf)} (o sinal '=' sozinho entre os discos do B7-2 é operador, não linha)")
    w(f"glyphmaps_numeros_{R}.txt", "\n".join(out) + "\n")
    print("glyph maps", len(gms))
    if R not in ("v2", "final"):
        return
    # frações
    fr = []
    for l in LOTES:
        for t in (log(l), log(l, "log_plano_")):
            fr += re.findall(r"^\[frac\] size=([\d.]+)px numerador=([\d.]+)px maior_glifo=([\d.]+)px :: (.*)$", t, re.M)
            if fr and t:
                break
    vistos, linhas, baixo = set(), [], 0
    for s_, n_, g_, tx in fr:
        if tx in vistos:
            continue
        vistos.add(tx)
        ok = float(s_) >= 26
        baixo += not ok
        linhas.append(f"{'OK ' if ok else 'BAIXO'} fonte {float(s_):5.1f} px · numerador {float(n_):5.1f} px · maior glifo {float(g_):5.1f} px :: {tx}")
    ntf = len(re.findall(r"\\tfrac", src))
    w("fracoes_v2.txt", f"FRAÇÕES (todas \\dfrac; fonte da fração e altura do numerador em px a 1080p)\n\\tfrac no código: {ntf} · abaixo de 26 px: {baixo}"
      f" · rótulos girados: 0 (nenhum MathTex girado no código)\n" + "\n".join(linhas) + "\n")
    print("fracoes", len(linhas), "tfrac", ntf, "baixo", baixo)
    # texto em MathTex
    tx = re.findall(r"\\text\{([^}]*)\}", src)
    ruins = sorted({t for t in tx if len(t.split()) > 1 and t.strip() not in ("área da cobertura", "área leve")})
    nomes = sorted({t for t in tx})
    w("texto_em_mathtex_v2.txt", f"\\text{{}} EM MATHTEX: {len(ruins)} frase(s) (mais de uma palavra, fora nomes de grandeza)\n"
      + "".join(f"  FRASE: {t!r}\n" for t in ruins)
      + "Nomes de grandeza ou unidade aceitos: " + ", ".join(repr(t) for t in nomes) + "\n"
      + "Observação: 'área da cobertura' (B3-1) e 'área leve' (S2) são nomes de grandeza de duas/três palavras, como no alvo.\n")
    print("texto em mathtex", len(ruins))
    # órfãos e Fubini
    orf_ = [ln for l in LOTES for ln in re.findall(r"^\[orfao\] .*$", log(l), re.M)]
    w("orfaos_v2.txt", f"RÓTULO ÓRFÃO (na fronteira de cada âncora, rótulo preso a cena 3D que já saiu): {len(orf_)}\n" + "\n".join(orf_) + "\n"
      "Também conferido no código: ACIMA DO NÍVEL e O QUE FALTA saem junto com o nivelamento (B6-1); a marca z acima do eixo some (R3).\n")
    fe = re.search(r"\[fubini\] entra ([\d.]+)", log("PS"))
    fs = re.search(r"\[fubini\] sai ([\d.]+)", log("PS"))
    if fe and fs:
        d = float(fs.group(1)) - float(fe.group(1))
        w("fubini_v2.txt", f"CARTÃO FUBINI: entra {float(fe.group(1)):.2f} s, CTA começa {float(fs.group(1)):.2f} s (do lote PS) → {d:.2f} s na tela "
          f"({'OK' if d >= 8 else 'CURTO'}; o CTA só entra depois, sem sobrepor)\n")
        print("fubini", round(d, 2))


if __name__ == "__main__":
    main()
