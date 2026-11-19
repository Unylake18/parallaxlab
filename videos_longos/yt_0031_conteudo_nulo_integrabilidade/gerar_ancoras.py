"""yt_0031 (copiado do gerar_ancoras.py do yt_0027/yt_0028, modo "estimado"; modo "voz real" copiado do yt_0032 final). Lê narracao.md
(narração v2.3 fechada, seção "## 1. Narração por âncora") e grava ancoras.json:
- estimado: duração de cada âncora = 0,15 s + palavras/3 + 0,35 s; `t` = início de cada palavra (relativo à âncora), a 3 palavras/s;
- voz real (handoff final §6), quando existem audio/narracao_final.wav e alinhamento_palavras.json: cada âncora começa LEAD0 antes da 1ª
  palavra dela e termina onde a seguinte começa (contínuo, sem silêncio inserido); a 1ª começa em 0 e a última termina CAUDA s depois do fim
  do WAV. `t` = início real de cada palavra, relativo à âncora."""
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
VEL, LEAD0, RESP = 3.0, 0.15, 0.35
t = (AQUI / "narracao.md").read_text(encoding="utf-8")
t = t.split("## 1. Narração por âncora")[1].split("## 2. Texto corrido")[0]
out, ordem, ini = {}, [], 0.0
for bloco in re.split(r"^### ", t, flags=re.M)[1:]:
    cab, *resto = bloco.split("\n")
    aid = cab.split(" · ")[0].strip()
    fala = " ".join(l.lstrip("> ") for l in resto if l.startswith(">"))
    tela = " ".join(l for l in resto if l.startswith("**Tela:**"))
    fala = re.sub(r"\[[^\]]*\]", "", fala)
    pal = re.findall(r"\w+", fala.lower())
    n = len(pal)
    d = round(LEAD0 + n / VEL + RESP, 2)
    tw = [round(LEAD0 + k / VEL, 3) for k in range(n)]
    out[aid] = {"palavras": n, "ini": round(ini, 4), "fim": round(ini + d, 4), "dur": d, "tela": tela, "fala": " ".join(pal), "t": tw}
    ordem.append(aid)
    ini += d
fonte = "estimado (0,15 + palavras/3 + 0,35)"
print(sum(v["palavras"] for v in out.values()), "palavras;", len(ordem), "âncoras;", f"{int(ini // 60)}:{ini % 60:05.2f} (estimado)")

ALI = AQUI / "alinhamento_palavras.json"
WAV = AQUI / "audio" / "narracao_final.wav"
if ALI.is_file() and WAV.is_file() and "--estimado" not in sys.argv:
    import wave
    CAUDA = 1.0
    with wave.open(str(WAV)) as w:
        fim_wav = w.getnframes() / w.getframerate()
    toks = [(tk, p["start"]) for p in json.loads(ALI.read_text(encoding="utf-8")) for tk in re.findall(r"\w+", p["word"].lower())]
    k = 0
    for aid in ordem:
        a = out[aid]
        n = a["palavras"]
        seg = toks[k:k + n]
        assert [x for x, _ in seg] == a["fala"].split(), f"{aid}: alinhamento fora do texto"
        a["_s0"] = seg[0][1]
        a["_ts"] = [s for _, s in seg]
        a["nominal"] = a["dur"]
        k += n
    assert k == len(toks), (k, len(toks))
    for i, aid in enumerate(ordem):
        out[aid]["ini"] = 0.0 if i == 0 else round(out[aid]["_s0"] - LEAD0, 3)
    for i, aid in enumerate(ordem):
        a = out[aid]
        a["fim"] = round(out[ordem[i + 1]]["ini"], 3) if i + 1 < len(ordem) else round(fim_wav + CAUDA, 3)
        a["dur"] = round(a["fim"] - a["ini"], 3)
        a["t"] = [round(s - a["ini"], 3) for s in a.pop("_ts")]
        a.pop("_s0")
    fonte = "voz real audio/narracao_final.wav (alinhamento forçado)"
    print("voz real:", round(fim_wav, 2), "s;", " ".join(f"{a}={out[a]['dur']:.1f}/{out[a]['nominal']:.1f}" for a in ordem))
(AQUI / "ancoras.json").write_text(json.dumps({"ordem": ordem, "fonte": fonte, "ancoras": out}, ensure_ascii=False, indent=1), encoding="utf-8")
for a in ordem:
    print(a, out[a]["palavras"], out[a]["dur"], f"{int(out[a]['ini'] // 60)}:{out[a]['ini'] % 60:05.2f}")
