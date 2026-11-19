"""yt_0034 final (copiado do qa_sync.py do yt_0032): relatório de sincronização → qa/sync_<rodada>.txt. Para cada âncora: início na tela (início do
lote no vídeo emendado + instante da âncora no lote) × primeira palavra na voz; para cada gatilho do log: instante do evento × início da palavra
(alinhamento forçado). Meta: o evento não chega mais de 0,2 s depois da palavra (negativo = a imagem vem antes, o LEAD).
uso: python qa_sync.py [rodada] [fps] [prefixo do log]   (ex.: voz 15 log_  |  final1080 30 log1080_)"""
import json
import re
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "voz"
FPS = int(sys.argv[2]) if len(sys.argv) > 2 else 15
PRE = sys.argv[3] if len(sys.argv) > 3 else "log_"
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
ANC = A["ancoras"]
LOTES = ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PB8", "PS"]
ini = {}
t = 0.0
for lote in LOTES:                                  # emenda sem sobreposição: o lote começa onde o anterior termina
    ini[lote] = t
    m = re.findall(r"\[tempo\] total ([\d.]+)s", (U / f"{PRE}{lote}.txt").read_text(encoding="utf-8", errors="replace"))
    t += float(m[-1]) if m else 0.0
L = [f"yt_0034 · sincronização (rodada {R}, {FPS} fps): atraso = tela − voz (s); meta ≤ +0,20 s", ""]
ruins, an_, ga_, extras = [], [], [], []
for lote in LOTES:
    log = (U / f"{PRE}{lote}.txt").read_text(encoding="utf-8", errors="replace")
    q0 = {}
    for l in log.splitlines():
        m = re.match(r"\[ancora\] (\S+) ([0-9.]+)", l)
        if m:
            aid, tl = m.group(1), float(m.group(2))
            q0[aid] = tl
            tela, voz = ini[lote] + tl, ANC[aid]["ini"] + ANC[aid]["t"][0]
            an_.append((aid, tela, voz, tela - voz))
            if tela - voz > 0.2:
                ruins.append(f"âncora {aid}: {tela - voz:+.2f} s")
            continue
        m = re.match(r"\[gatilho\] (\S+)\s+([-0-9.]+)s \(alvo\s+([-0-9.]+)s, atraso ([-+0-9.]+)s\) (.*)", l)
        if m:
            a_, rel, _, _, fr = m.groups()
            fala = ANC[a_]["fala"].split()
            al = re.findall(r"\w+", fr.lower())
            k = next(i for i in range(len(fala)) if fala[i:i + len(al)] == al)
            tela, voz = ini[lote] + q0.get(a_, 0.0) + float(rel), ANC[a_]["ini"] + ANC[a_]["t"][k]
            ga_.append((a_, fr, tela, voz, tela - voz))
            if tela - voz > 0.2:
                ruins.append(f"gatilho {a_} «{fr}»: {tela - voz:+.2f} s")
            continue
        if l.startswith(("[estouro]", "[deriva]", "[gatilho-sem-frase]")):
            extras.append(f"{lote}: {l}")
L += extras + ["", "âncoras (início na tela × 1ª palavra na voz):"]
L += [f"  {a:5s} tela {te:8.2f} s · voz {vo:8.2f} s · {at:+.2f} s {'OK' if at <= 0.2 else 'FORA'}" for a, te, vo, at in an_]
L += ["", f"gatilhos ({len(ga_)}):"]
L += [f"  {a:5s} {at:+.2f} s  «{fr}»  (tela {te:.2f} · voz {vo:.2f}) {'OK' if at <= 0.2 else 'FORA'}" for a, fr, te, vo, at in ga_]
ats = [x[-1] for x in ga_] + [x[-1] for x in an_]
L += ["", f"resumo: {len(an_)} âncoras, {len(ga_)} gatilhos; atraso de {min(ats):+.2f} a {max(ats):+.2f} s; fora da meta (> +0,2 s): {len(ruins)}"]
L += [f"  {r}" for r in ruins]
(U / "qa").mkdir(exist_ok=True)
(U / "qa" / f"sync_{R}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L[-3 - len(ruins):]))
