"""ancoras.json a partir da voz gravada (a voz manda): dur = entrada (0,15 s) + fala real + respiro.
Respiro: 0,75 s entre âncoras; 1,2 s antes de cada troca de capítulo; 1,4 s nas pausas protegidas do handoff v7 (⊕ no haltere, a granada
explodindo, o termo cruzado zerando no T3-4, o resultado do exercício final). A fala de cada âncora (sem tags) vai junto: `self.em()` encaixa
cada entrada da cena na palavra, distribuída na duração real da fala.
uso: python ancoras_voz.py"""
import json
import re
from pathlib import Path

U = Path(__file__).resolve().parent
ENTRA, RESPIRO, CAPITULO, PROTEGIDA = 0.15, 0.75, 1.2, 1.4
CAPITULOS = {"A1", "T1-1", "T2-1", "T3-1", "T4-1", "E1-1", "E2-1", "S1", "EN1", "EN2"}     # a âncora ANTES destas ganha 1,2 s
PROTEGIDAS = {"T1-1", "H2", "T3-4", "E2-4"}                                           # estas ganham 1,4 s no fim

t = (U / "narracao_tags_v4_2.md").read_text(encoding="utf-8")
t = t[t.index("## Por âncora"):t.index("## Texto corrido")]
falas = {b.split("\n", 1)[0].strip(): " ".join(re.sub(r"\[[^\]]*\]", "", b.split("\n", 1)[1]).split())
         for b in re.split(r"^### ", t, flags=re.M)[1:]}
voz = json.loads((U / "audio/ancoras_v42/duracoes.json").read_text(encoding="utf-8"))
ordem = list(falas)
anc = {}
for k, a in enumerate(ordem):
    prox = ordem[k + 1] if k + 1 < len(ordem) else None
    resp = PROTEGIDA if a in PROTEGIDAS else CAPITULO if prox in CAPITULOS else RESPIRO
    s = voz[a]["fala"]
    anc[a] = {"palavras": len(re.findall(r"\w+", falas[a])), "dur": round(ENTRA + s + resp, 3), "fala": falas[a],
              "voz_ini": ENTRA, "voz_s": round(s, 3), "respiro": resp}
(U / "ancoras.json").write_text(json.dumps({"ordem": ordem, "ancoras": anc}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(anc)} âncoras; vídeo {sum(v['dur'] for v in anc.values()) / 60:.2f} min; fala {sum(v['voz_s'] for v in anc.values()) / 60:.2f} min")
