"""yt_0030 · tempos do preview silencioso (handoff v1 §6): cada parágrafo da narração canônica (narracao.md, Anexo A do handoff) é uma
âncora; a palavra k do parágrafo cai em (palavras antes + k) ÷ 3 s (orçamento a 3 palavras por segundo). A cena só pede gatilhos por
FRASE (`self.gat("pausa o vídeo e tenta")`), então, na fase da voz, basta trocar este arquivo pelos tempos medidos no WAV contínuo
(mesmo formato: ini, fim, dur, fala, t) sem mexer na cena.

uso: python tempos.py → imprime a tabela dos blocos (palavras, início, duração) e grava ancoras.json (cópia para conferência)."""
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PPS = 3.0                       # palavras por segundo do orçamento
ARQ = AQUI / "narracao.md"

# nome do bloco no narracao.md (### <nome> · título) → prefixo das âncoras
BLOCOS = {"H": "H", "A": "A", "D1": "D1", "D2": "D2", "D3": "D3", "D3b": "D3b", "D4": "D4", "D5": "D5", "P2": "P2",
          "A1": "A1", "A2": "A2", "A4": "A4", "A3": "A3", "S": "S"}


def _paragrafos():
    bloco, out = None, []
    for par in re.split(r"\n\s*\n", ARQ.read_text(encoding="utf-8")):
        par = par.strip()
        m = re.match(r"###\s+(\S+)\s+·", par)
        if m:
            bloco = BLOCOS[m.group(1)]
            par = par[m.end():].split("\n", 1)[1].strip() if "\n" in par else ""
            if not par:
                continue
        if bloco is None or not par or par.startswith("#") or par.startswith("*("):
            continue
        out.append((bloco, par))
    return out


def ancoras():
    ordem, anc, n0, cont = [], {}, 0, {}
    for bloco, par in _paragrafos():
        cont[bloco] = cont.get(bloco, 0) + 1
        aid = f"{bloco}-{cont[bloco]}"
        limpo = re.sub(r"\[[^\]]*\]", " ", par)
        palavras = limpo.split()
        fala, t = [], []
        for k, w in enumerate(palavras):
            for tok in re.findall(r"\w+", w.lower()):
                fala.append(tok)
                t.append(round(k / PPS, 4))
        ini = n0 / PPS
        dur = len(palavras) / PPS
        anc[aid] = {"ini": round(ini, 4), "fim": round(ini + dur, 4), "dur": round(dur, 4), "fala": " ".join(fala), "t": t,
                    "bloco": bloco, "palavras": len(palavras)}
        ordem.append(aid)
        n0 += len(palavras)
    return {"ordem": ordem, "fonte": f"orçamento a {PPS:g} palavras/s (narracao.md, Anexo A do handoff v1)", "ancoras": anc}


ANC_DADOS = ancoras()

if __name__ == "__main__":
    d = ANC_DADOS
    (AQUI / "ancoras.json").write_text(json.dumps(d, ensure_ascii=False, indent=0), encoding="utf-8")
    por = {}
    for a in d["ordem"]:
        x = d["ancoras"][a]
        b = por.setdefault(x["bloco"], [0, x["ini"], 0.0, 0])
        b[0] += x["palavras"]
        b[2] += x["dur"]
        b[3] += 1
    tot = 0
    for b, (n, ini, dur, k) in por.items():
        tot += n
        print(f"{b:4s} {n:5d} palavras  {k:2d} parágrafos  início {int(ini) // 60}:{ini % 60:05.2f}  duração {dur:6.1f} s")
    print(f"total {tot} palavras = {tot / PPS:.1f} s = {int(tot / PPS) // 60}:{tot / PPS % 60:04.1f}")
