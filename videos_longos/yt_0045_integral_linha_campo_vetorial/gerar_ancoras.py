"""yt_0045 (copiado do gerar_ancoras.py do yt_0043, modo "estimado" do preview; sem o bloco da voz real). Lê referencia/yt_0045_narracao_v1_2_final.md
(um bloco "### <âncora> · …" por âncora, fala nas linhas "> …", gatilhos na linha **Gatilhos:** '"frase"→…') e grava:
- ancoras.json: duração de cada âncora = 0,15 s + palavras/3 + 0,35 s; `t` = início de cada palavra (relativo à âncora), a 3 palavras/s;
- duracoes_estimadas.json: âncora → {palavras, ini, fim, dur, gatilhos: {frase: instante absoluto}}."""
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
VEL, LEAD0, RESP = 3.0, 0.15, 0.35
t = (AQUI / "referencia" / "yt_0045_narracao_v1_2_final.md").read_text(encoding="utf-8")
t = t[t.index("### H1 ·"):]
out, ordem, ini, gats = {}, [], 0.0, {}
ALIAS = {}
for bloco in re.split(r"^### ", t, flags=re.M)[1:]:
    cab, *resto = bloco.split("\n")
    aid = cab.split(" · ")[0].strip()
    fala = " ".join(l.lstrip("> ") for l in resto if l.startswith(">"))
    tela = " ".join(l for l in resto if l.startswith("**Tela:**"))
    fala = re.sub(r"\[[^\]]*\]", "", fala)
    pal = re.findall(r"\w+", fala.lower())
    n = len(pal)
    nf = len([w for w in fala.split() if re.search(r"\w", w)])      # palavras faladas (como na tabela da narração)
    d = round(LEAD0 + nf / VEL + RESP, 2)
    tw = [round(LEAD0 + (nf / n) * k / VEL, 3) for k in range(n)]
    gl = " ".join(l for l in resto if l.startswith("**Gatilhos:**"))
    frases = re.findall(r'"([^"]+)"', gl)
    g, k0 = {}, 0
    for fr in frases:
        alvo = re.findall(r"\w+", ALIAS.get(fr, fr).lower())
        k = next((i for i in range(k0, n) if pal[i:i + len(alvo)] == alvo), None)       # a ocorrência depois do gatilho anterior
        if k is None:
            k = next((i for i in range(n) if pal[i:i + len(alvo)] == alvo), None)
        g[fr] = None if k is None else round(ini + tw[k], 3)
        k0 = k if k is not None else k0
    out[aid] = {"palavras": nf, "ini": round(ini, 4), "fim": round(ini + d, 4), "dur": d, "tela": tela, "fala": " ".join(pal), "t": tw}
    gats[aid] = g
    ordem.append(aid)
    ini += d
(AQUI / "ancoras.json").write_text(json.dumps({"ordem": ordem, "fonte": "estimado (0,15 + palavras/3 + 0,35)", "ancoras": out}, ensure_ascii=False, indent=1),
                                   encoding="utf-8")
(AQUI / "duracoes_estimadas.json").write_text(json.dumps(
    {"fonte": "narração v1.1 (referencia/yt_0045_narracao_v1_2_final.md), 3 palavras/s (0,15 + palavras/3 + 0,35); gatilhos = instante absoluto da 1ª palavra da frase",
     "total_s": round(ini, 2),
     "ancoras": {a: {"palavras": out[a]["palavras"], "ini": out[a]["ini"], "fim": out[a]["fim"], "dur": out[a]["dur"], "gatilhos": gats[a]} for a in ordem}},
    ensure_ascii=False, indent=1), encoding="utf-8")
print(sum(v["palavras"] for v in out.values()), "palavras;", len(ordem), "âncoras;", f"{int(ini // 60)}:{ini % 60:05.2f}")
for a in ordem:
    sem = [f for f, v in gats[a].items() if v is None]
    print(a, out[a]["palavras"], out[a]["dur"], f"{int(out[a]['ini'] // 60)}:{out[a]['ini'] % 60:05.2f}", len(gats[a]), "gatilhos", ("SEM: " + str(sem)) if sem else "")


# ── final (handoff final §6): tempo REAL da voz (audio/narracao_final.wav + alinhamento forçado em alinhamento_palavras.json) ──────────────
# Copiado do gerar_ancoras.py do yt_0028. Cada âncora começa LEAD0 antes da 1ª palavra dela e termina onde a seguinte começa (contínuo, sem
# silêncio inserido); a 1ª começa em 0 e a última termina CAUDA s depois do fim do WAV. `t` = início real de cada palavra, relativo à âncora.
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
        n = len(a["fala"].split())                                  # tokens \w+ (hífen = 2, como no alinhamento)
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
    (AQUI / "ancoras.json").write_text(json.dumps({"ordem": ordem, "fonte": "voz real audio/narracao_final.wav (alinhamento forçado)", "ancoras": out},
                                                  ensure_ascii=False, indent=1), encoding="utf-8")
    print("voz real:", round(fim_wav, 2), "s;", " ".join(f"{a}={out[a]['dur']:.1f}/{out[a]['nominal']:.1f}" for a in ordem))
