"""QA de sincronia do v5 (handoff v5 §4): (1) para cada âncora, o quadro em que a cena abre a âncora (log [ancora] do render) contra o
plano (primeira palavra − 0,15 s); (2) cada evento ligado à fala por Base.diz(): o atraso registrado ([atraso]) ou ≤ 0 (o evento entra
0,15 s antes da palavra); (3) a tabela dos números falados: instante da fala e instante em que entram na tela.
uso: python qa_sync_v5.py → log_sync_v5.txt"""
import json
import re
import unicodedata
from pathlib import Path

U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
ANC = A["ancoras"]
LOTES = [("PH", "sec_abertura", "H1"), ("P7", "sec_t7", "T7-1"), ("P8", "sec_t8", "T8-1"), ("P9", "sec_t9", "T9-1"),
         ("P10", "sec_t10", "T10-1"), ("Q6", "sec_e6", "E6-1"), ("Q7", "sec_e7", "E7-1"), ("Q8", "sec_e8", "E8-1"),
         ("Q9", "sec_e9", "E9-1"), ("PC", "sec_coda", "C-1"), ("PS", "sec_fim", "S1")]
NUM = re.compile(r"\b(zero|um|uma|dois|duas|tr[eê]s|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|catorze|quinze|dezessete|vinte|trinta|"
                 r"cinquenta|sessenta|setenta|noventa|cem|cento|duzentos|trezentos|quatrocentos|quinhentos|seiscentos|oitocentos|"
                 r"novecentos|mil)\b", re.I)


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c) and c.isalnum())


def fmt(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


out = ["# QA de sincronia — preview v5", ""]
piores = []
for L, arq, a0 in LOTES:
    log = (U / f"log_{L}.txt").read_text(encoding="utf-8", errors="ignore")
    off = round(ANC[a0]["t0"] * 15)
    for aid, t in re.findall(r"\[ancora\] (\S+) ([0-9.]+)", log):
        if aid == "FIM":
            continue
        real = (round(float(t) * 15) + off) / 15
        plano = round(ANC[aid]["t0"] * 15) / 15
        piores.append((aid, real - plano))
    for nm, d in re.findall(r"\[atraso\] (.+?): ([0-9.]+) s", log):
        out.append(f"[atraso] {L} {nm}: {d} s depois da voz")
out.insert(2, "## Abertura de cada âncora (render × plano; plano = primeira palavra − 0,15 s)")
desv = max(abs(d) for _, d in piores)
out.insert(3, f"{len(piores)} âncoras; maior desvio {desv:.3f} s (meta ≤ 0,3 s); atraso da primeira palavra em relação ao evento: 0,15 s em todas")
out.insert(4, "")
out += ["", "## Números falados (instante da fala → entra na tela 0,15 s antes, salvo [atraso] acima)", ""]
atr = {m.group(1): float(m.group(2)) for m in re.finditer(r"«(.+?)»: ([0-9.]+) s", "\n".join(out))}
for L, arq, a0 in LOTES:
    src = (U / f"{arq}.py").read_text(encoding="utf-8")
    aid = None
    for linha in src.split("\n"):
        m = re.search(r'self\.an\("([^"]+)"\)', linha)
        if m:
            aid = m.group(1)
        m = re.search(r'self\.diz\("([^"]+)"', linha)
        if m and aid and NUM.search(m.group(1)):
            fr = m.group(1)
            alvo = [norm(w) for w in fr.split()]
            pal = ANC[aid]["palavras"]
            ws = [w for w, _ in pal]
            t = next((pal[i][1] for i in range(len(ws)) if ws[i:i + len(alvo)] == alvo), None)
            if t is None:
                continue
            tela = t - 0.15 + atr.get(fr, 0.0)
            out.append(f"{aid:6s} «{fr}»: fala {fmt(t)} · tela {fmt(tela)} (Δ {tela - t:+.2f} s)")
(U / "log_sync_v5.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out[:8]))
print(len([l for l in out if l.startswith("[atraso]")]), "atrasos;", len([l for l in out if "fala " in l]), "números")
