"""yt_0026 (adaptado do gerador do yt_0022). Lê narracao.md (Anexo A do handoff v2) e grava ancoras.json com o tempo NOMINAL de cada âncora:
a fala começa 0,15 s depois da tela, 2,7 palavras/s (só palavras faladas: sem tags [ ] nem cabeçalho `tela:`), e 0,35 s de respiro no fim.
`t` = início de cada palavra (relativo à âncora), para os gatilhos.
Tempos ESTIMADOS: a duração definitiva sai da voz real."""
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
VEL, LEAD0, RESP = 2.7, 0.15, 0.35
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
    a = {"palavras": n, "ini": round(ini, 4), "fim": round(ini + d, 4), "dur": d, "nominal": d, "tela": tela, "fala": " ".join(pal), "t": tw}
    out[aid] = a
    ordem.append(aid)
    ini += d
(AQUI / "ancoras.json").write_text(json.dumps({"ordem": ordem, "ancoras": out}, ensure_ascii=False, indent=1), encoding="utf-8")
tot = sum(v["palavras"] for v in out.values())
semb7 = sum(v["dur"] for k, v in out.items() if not k.startswith("B7"))
print(tot, "palavras;", round(ini / 60, 2), "min com B7;", round(semb7 / 60, 2), "min sem B7")
(AQUI / "duracoes_estimadas.json").write_text(json.dumps(
    {"nota": "ESTIMADO: 0,15 s + palavras/2,7 + 0,35 s por âncora (fala nominal); a cena pode esticar onde a construção pede (ver render)",
     "total_com_b7_s": round(ini, 1), "total_sem_b7_s": round(semb7, 1),
     "ancoras": {k: {"palavras": out[k]["palavras"], "dur_s": out[k]["dur"]} for k in ordem}}, ensure_ascii=False, indent=1), encoding="utf-8")

# ── v9: tempo REAL da voz (audio/narracao_v4.wav, alinhamento forçado em alinhamento_palavras.json) ──────────────────────────────────────
# Cada âncora começa LEAD0 antes da 1ª palavra dela e termina onde a seguinte começa (contínuo, sem silêncio inserido); a 1ª começa em 0 e a
# última termina CAUDA s depois do fim do WAV. `t` = início real de cada palavra, relativo ao início da âncora.
ALI = AQUI / "alinhamento_palavras.json"
if ALI.is_file():
    import wave
    CAUDA = 1.0
    with wave.open(str(AQUI / "audio" / "narracao_v4.wav")) as w:
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
        a = out[aid]
        a["ini"] = 0.0 if i == 0 else round(a["_s0"] - LEAD0, 3)
    for i, aid in enumerate(ordem):
        a = out[aid]
        a["fim"] = round(out[ordem[i + 1]]["ini"], 3) if i + 1 < len(ordem) else round(fim_wav + CAUDA, 3)
        a["dur"] = round(a["fim"] - a["ini"], 3)
        a["t"] = [round(s - a["ini"], 3) for s in a.pop("_ts")]
        a.pop("_s0")
    (AQUI / "ancoras.json").write_text(json.dumps({"ordem": ordem, "fonte": "voz real audio/narracao_v4.wav (alinhamento forçado)", "ancoras": out},
                                                  ensure_ascii=False, indent=1), encoding="utf-8")
    print("voz real:", round(fim_wav, 2), "s;", " ".join(f"{a}={out[a]['dur']:.1f}/{out[a]['nominal']:.1f}" for a in ordem))
