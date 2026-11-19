"""yt_0041 (copiado do gerar_ancoras.py do yt_0037, modo "estimado"). Lê referencia/yt_0041_narracao_v1_4.md (um bloco "### <âncora> · …" por âncora,
fala nas linhas "> …", gatilhos nas linhas '- "frase"→…' ou '"frase"→…' depois de **Gatilhos:**) e grava:
- ancoras.json: duração de cada âncora = 0,15 s + palavras/3 + 0,35 s (handoff §6); `t` = início de cada palavra (relativo à âncora), a 3 palavras/s;
- duracoes_estimadas.json: âncora → {palavras, ini, fim, dur, gatilhos: {frase: instante absoluto}}.
Na fase de voz, ancoras.json passa a seguir o WAV contínuo (alinhamento forçado)."""
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
VEL, LEAD0, RESP = 3.0, 0.15, 0.35
t = (AQUI / "referencia" / "yt_0042_narracao_v1.md").read_text(encoding="utf-8")
t = t[t.index("### H1 ·"):t.index("## Leitura dos símbolos")]
out, ordem, ini, gats = {}, [], 0.0, {}
# frases de gatilho da narração que não estão literalmente na fala (diferença de redação): procura a frase equivalente da fala
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
    gl = " ".join(l for l in resto if "→" in l)
    frases = re.findall(r'"([^"]+)"\s*(?:/[^→]*)?→', gl) + re.findall(r'"([^"]+)"\s*/', gl)
    g, k0 = {}, 0
    frases = sorted(dict.fromkeys(frases), key=lambda f: gl.index(f'"{f}"'))           # na ordem em que aparecem na lista de gatilhos
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
    {"fonte": "narração v1.4 (referencia/yt_0041_narracao_v1_4.md), 3 palavras/s (0,15 + palavras/3 + 0,35); gatilhos = instante absoluto da 1ª palavra da frase",
     "total_s": round(ini, 2),
     "ancoras": {a: {"palavras": out[a]["palavras"], "ini": out[a]["ini"], "fim": out[a]["fim"], "dur": out[a]["dur"], "gatilhos": gats[a]} for a in ordem}},
    ensure_ascii=False, indent=1), encoding="utf-8")
print(sum(v["palavras"] for v in out.values()), "palavras;", len(ordem), "âncoras;", f"{int(ini // 60)}:{ini % 60:05.2f}")
for a in ordem:
    sem = [f for f, v in gats[a].items() if v is None]
    print(a, out[a]["palavras"], out[a]["dur"], f"{int(out[a]['ini'] // 60)}:{out[a]['ini'] % 60:05.2f}", len(gats[a]), "gatilhos", ("SEM: " + str(sem)) if sem else "")
