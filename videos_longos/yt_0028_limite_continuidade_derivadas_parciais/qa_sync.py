"""yt_0028 final §5.4: relatório de sincronização → qa/sync.txt. Para cada âncora: início na tela (quadro absoluto do preview emendado, quadros_<rodada>.json)
× primeira palavra na voz; para cada gatilho do log: instante do evento na tela × início da palavra na voz (alinhamento forçado). Meta: o evento não chega
mais de 0,2 s depois da palavra (negativo = a imagem vem antes, o LEAD). Também lista [estouro], [deriva] e [gatilho-sem-frase].
uso: python qa_sync.py [rodada] [fps] [prefixo do log]   (ex.: final 15 log_  |  final1080 30 log1080_)"""
import json
import re
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "final"
FPS = int(sys.argv[2]) if len(sys.argv) > 2 else 15
PRE = sys.argv[3] if len(sys.argv) > 3 else "log_"
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
ANC, ordem = A["ancoras"], A["ordem"]
Q = json.loads((U / "renders" / R / f"quadros_{R}.json").read_text(encoding="utf-8"))
LOTES = ["PH", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PS"]
L = [f"yt_0028 · sincronização (rodada {R}, {FPS} fps): atraso = tela − voz (s); meta ≤ +0,20 s", ""]
ruins, linhas_anc, extras = [], [], []
for lote in LOTES:
    log = (U / f"{PRE}{lote}.txt").read_text(encoding="utf-8", errors="replace")
    aid = None
    for l in log.splitlines():
        m = re.match(r"\[ancora\] (\S+) ([0-9.]+)", l)
        if m:
            aid = m.group(1)
            tela = Q[aid] / FPS
            voz = ANC[aid]["ini"] + ANC[aid]["t"][0]
            at = tela - voz
            linhas_anc.append((aid, tela, voz, at))
            if at > 0.2:
                ruins.append(f"âncora {aid}: {at:+.2f} s")
            continue
        m = re.match(r"\[gatilho\] (\S+)\s+([-0-9.]+)s \(alvo\s+([-0-9.]+)s, atraso ([-+0-9.]+)s\) (.*)", l)
        if m:
            a_, rel, alvo, _, fr = m.groups()
            fala = ANC[a_]["fala"].split()
            al = re.findall(r"\w+", fr.lower())
            k = next(i for i in range(len(fala)) if fala[i:i + len(al)] == al)
            tela = Q[a_] / FPS + float(rel)
            voz = ANC[a_]["ini"] + ANC[a_]["t"][k]
            at = tela - voz
            extras.append((a_, fr, tela, voz, at))
            if at > 0.2:
                ruins.append(f"gatilho {a_} «{fr}»: {at:+.2f} s")
            continue
        if l.startswith(("[estouro]", "[deriva]", "[gatilho-sem-frase]")):
            L.append(f"{lote}: {l}")
L += ["", "âncoras (início da âncora na tela × 1ª palavra na voz):"]
for aid, tela, voz, at in linhas_anc:
    L.append(f"  {aid:5s} tela {tela:8.2f} s · voz {voz:8.2f} s · {at:+.2f} s {'OK' if at <= 0.2 else 'FORA'}")
L += ["", f"gatilhos ({len(extras)}):"]
for a_, fr, tela, voz, at in extras:
    L.append(f"  {a_:5s} {at:+.2f} s  «{fr}»  (tela {tela:.2f} · voz {voz:.2f}) {'OK' if at <= 0.2 else 'FORA'}")
ats = [x[-1] for x in extras] + [x[-1] for x in linhas_anc]
L += ["", f"resumo: {len(linhas_anc)} âncoras, {len(extras)} gatilhos; atraso de {min(ats):+.2f} a {max(ats):+.2f} s; fora da meta (> +0,2 s): {len(ruins)}"]
L += [f"  {r}" for r in ruins]
(U / "qa").mkdir(exist_ok=True)
(U / "qa" / f"sync_{R}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L[-3 - len(ruins):]))
