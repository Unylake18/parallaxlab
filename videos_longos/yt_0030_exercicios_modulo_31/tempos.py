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


def voz_real(d):
    """Handoff final §5.2 (lógica "final" do gerar_ancoras.py do yt_0028): com alinhamento_palavras.json e audio/narracao_final.wav, os tempos
    saem da voz real, no mesmo formato. ini = 1ª palavra − 0,15 s (a 1ª âncora em 0); fim = ini da seguinte; a última termina 1,0 s depois do WAV;
    t = início real de cada token \\w+ relativo ao ini (assert: a sequência de tokens do alinhamento é a do texto)."""
    import wave
    ali, wav = AQUI / "alinhamento_palavras.json", AQUI / "audio" / "narracao_final.wav"
    if not (ali.is_file() and wav.is_file()):
        return d
    LEAD0, CAUDA = 0.15, 1.0
    with wave.open(str(wav)) as w:
        fim_wav = w.getnframes() / w.getframerate()
    toks = [(tk, p["start"]) for p in json.loads(ali.read_text(encoding="utf-8")) for tk in re.findall(r"\w+", p["word"].lower())]
    texto = [tk for aid in d["ordem"] for tk in d["ancoras"][aid]["fala"].split()]
    if [tk for tk, _ in toks] != texto:      # v4: alinhamento de outra versão do texto (ex.: v3.3 com a narração v3.4) → fica o orçamento
        import sys
        print(f"[tempos] alinhamento_palavras.json não é deste texto ({len(toks)} × {len(texto)} tokens): tempos pelo orçamento", file=sys.stderr)
        return d
    ordem, anc, k, ts = d["ordem"], d["ancoras"], 0, {}
    for aid in ordem:
        fala = anc[aid]["fala"].split()
        seg = toks[k:k + len(fala)]
        assert [x for x, _ in seg] == fala, f"{aid}: alinhamento fora do texto"
        ts[aid] = [s for _, s in seg]
        k += len(fala)
    assert k == len(toks), (k, len(toks))
    ini = {aid: (0.0 if i == 0 else round(ts[aid][0] - LEAD0, 3)) for i, aid in enumerate(ordem)}
    for i, aid in enumerate(ordem):
        a = anc[aid]
        a["ini"] = ini[aid]
        a["fim"] = ini[ordem[i + 1]] if i + 1 < len(ordem) else round(fim_wav + CAUDA, 3)
        a["dur"] = round(a["fim"] - a["ini"], 3)
        a["t"] = [round(s - a["ini"], 3) for s in ts[aid]]
    d["fonte"] = "voz real audio/narracao_final.wav (alinhamento forçado, alinhamento_palavras.json)"
    d["voz"] = round(fim_wav, 3)
    return d


ANC_DADOS = voz_real(ancoras())

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
    if "voz" in d:
        print(f"fonte: {d['fonte']} · WAV {d['voz']:.2f} s · fim da última âncora {d['ancoras'][d['ordem'][-1]]['fim']:.2f} s"
              f" · {tot / d['voz']:.3f} palavras/s")
