"""yt_0028 (copiado do yt_0027; 2,8 palavras/s pelo handoff v1.2 §6). Lê narracao.md (Anexo A do handoff v1) e grava ancoras.json com o tempo NOMINAL de cada âncora:
a fala começa 0,15 s depois da tela, 2,7 palavras/s (só palavras faladas: sem tags [ ] nem cabeçalho `tela:`), e 0,35 s de respiro no fim.
`t` = início de cada palavra (relativo à âncora), para os gatilhos. Tempos ESTIMADOS: a duração definitiva sai da voz real."""
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
VEL, LEAD0, RESP = 2.8, 0.15, 0.35
t = (AQUI / "narracao.md").read_text(encoding="utf-8")
out, ordem, ini = {}, [], 0.0
for bloco in re.split(r"^### ", t, flags=re.M)[1:]:
    cab, *resto = bloco.split("\n")
    aid = cab.split(" · ")[0].strip()
    tela = cab.split("tela:", 1)[1].strip() if "tela:" in cab else ""
    fala = " ".join(l for l in resto if l.strip() and not l.startswith(("---", "#")))
    fala = re.sub(r"\[[^\]]*\]", "", fala)
    pal = re.findall(r"\w+", fala.lower())
    n = len(pal)
    d = round(LEAD0 + n / VEL + RESP, 2)
    tw = [round(LEAD0 + k / VEL, 3) for k in range(n)]
    out[aid] = {"palavras": n, "ini": round(ini, 4), "fim": round(ini + d, 4), "dur": d, "nominal": d, "tela": tela, "fala": " ".join(pal), "t": tw}
    ordem.append(aid)
    ini += d
(AQUI / "ancoras.json").write_text(json.dumps({"ordem": ordem, "ancoras": out}, ensure_ascii=False, indent=1), encoding="utf-8")
tot = sum(v["palavras"] for v in out.values())
print(tot, "palavras;", len(ordem), "âncoras;", round(ini / 60, 2), "min a 2,8 p/s;", round((ini - sum(0.5 for _ in ordem)) * 2.7 / 3.0 / 60, 2), "min a 3,0 p/s (aprox.)")
(AQUI / "duracoes_estimadas.json").write_text(json.dumps(
    {"nota": "ESTIMADO: 0,15 s + palavras/2,8 + 0,35 s por âncora (fala nominal); a cena pode esticar onde a construção pede (ver render). Não são tempos medidos.",
     "palavras": tot, "total_nominal_s": round(ini, 1), "total_nominal_min": round(ini / 60, 2),
     "ancoras": {k: {"palavras": out[k]["palavras"], "dur_s": out[k]["dur"]} for k in ordem}}, ensure_ascii=False, indent=1), encoding="utf-8")

# ── final (handoff final §5): tempo REAL da voz (audio/narracao_final.wav, alinhamento forçado em alinhamento_palavras.json) ──────────────────
# Cada âncora começa LEAD0 antes da 1ª palavra dela e termina onde a seguinte começa (contínuo, sem silêncio inserido); a 1ª começa em 0 e a
# última termina CAUDA s depois do fim do WAV. `t` = início real de cada palavra, relativo ao início da âncora.
ALI = AQUI / "alinhamento_palavras.json"
WAV = AQUI / "audio" / "narracao_final.wav"
if ALI.is_file() and WAV.is_file():
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
    (AQUI / "ancoras.json").write_text(json.dumps({"ordem": ordem, "fonte": "voz real audio/narracao_final.wav (alinhamento forçado)", "ancoras": out},
                                                  ensure_ascii=False, indent=1), encoding="utf-8")
    print("voz real:", round(fim_wav, 2), "s;", " ".join(f"{a}={out[a]['dur']:.1f}/{out[a]['nominal']:.1f}" for a in ordem))
