"""yt_0030 · handoff final §5.5 (copiado do yt_0028): relatório de sincronização → qa/sync.txt (e qa/sync_<rodada>.txt).
Tempo na tela = quadro absoluto de início do lote (renders/<rodada>/lotes_<rodada>.json, gravado pelo montar.py) + tempo no lote (log).
  · âncoras: [ancora] × 1ª palavra da âncora na voz;
  · gatilhos: [gatilho] × início da palavra da frase (alinhamento forçado);
  · fins de sublinhado: [fim-leitura] (fim do FadeOut) × a palavra da frase `ate=` menos o LEAD.
Meta: o evento não chega mais de 0,2 s depois da palavra (negativo = a imagem vem antes, o LEAD). Também confere o início de cada lote
(= ini da 1ª âncora × fps, ±1 quadro) e lista [estouro], [deriva], [gatilho-sem-frase], leituras e PAUSE E TENTE.
uso: python qa_sync.py [rodada] [fps] [prefixo do log]   (ex.: final 15 log_  |  final1080 30 log1080_)"""
import json
import re
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "final"
FPS = int(sys.argv[2]) if len(sys.argv) > 2 else 15
PRE = sys.argv[3] if len(sys.argv) > 3 else "log_"
LEAD = 0.09
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
ANC, ordem = A["ancoras"], A["ordem"]
J = json.loads((U / "renders" / R / f"lotes_{R}.json").read_text(encoding="utf-8"))
INI = J["inicio"]
LOTES = ["PH", "PD1", "PD2", "PD3", "PD3B", "PD4", "PD5", "PA1", "PA2", "PA4", "PA3", "PS"]


def k_frase(aid, fr):
    fala = ANC[aid]["fala"].split()
    al = re.findall(r"\w+", fr.lower())
    return next(i for i in range(len(fala)) if fala[i:i + len(al)] == al)


L = [f"yt_0030 · sincronização (rodada {R}, {FPS} fps, fonte dos tempos: {A.get('fonte', '?')}): atraso = tela − voz (s); meta ≤ +0,20 s", ""]
ruins, anc_l, gat_l, fim_l, avisos, emendas = [], [], [], [], [], []
leit, pausas = 0, 0
for lote in LOTES:
    log = (U / f"{PRE}{lote}.txt").read_text(encoding="utf-8", errors="replace")
    q_lote = INI[lote]
    t_anc = {}
    prim = True
    for l in log.splitlines():
        m = re.match(r"\[ancora\] (\S+) ([0-9.]+)", l)
        if m:
            aid, tl = m.group(1), float(m.group(2))
            t_anc[aid] = tl
            tela = q_lote / FPS + tl
            voz = ANC[aid]["ini"] + ANC[aid]["t"][0]
            at = tela - voz
            anc_l.append((aid, tela, voz, at))
            if at > 0.2:
                ruins.append(f"âncora {aid}: {at:+.2f} s")
            if prim:
                esp = round(ANC[aid]["ini"] * FPS)
                emendas.append((lote, aid, q_lote + round(tl * FPS), esp))
                prim = False
            continue
        m = re.match(r"\[gatilho\] (\S+)\s+([-0-9.]+)s \(alvo\s+([-0-9.]+)s, atraso ([-+0-9.]+)s\) (.*)", l)
        if m:
            a_, rel, _, _, fr = m.groups()
            tela = q_lote / FPS + t_anc[a_] + float(rel)
            voz = ANC[a_]["ini"] + ANC[a_]["t"][k_frase(a_, fr)]
            at = tela - voz
            gat_l.append((a_, fr, tela, voz, at))
            if at > 0.2:
                ruins.append(f"gatilho {a_} «{fr}»: {at:+.2f} s")
            continue
        m = re.match(r"\[fim-leitura\] (\d+) (\S+) ([0-9.]+) (.*)", l)
        if m:
            n_, a_, tl, fr = m.groups()
            tela = q_lote / FPS + float(tl)
            voz = ANC[a_]["ini"] + ANC[a_]["t"][k_frase(a_, fr)] - LEAD
            at = tela - voz
            fim_l.append((n_, a_, fr, tela, voz, at))
            if at > 0.2:
                ruins.append(f"fim da leitura {n_} ({a_}) «{fr}»: {at:+.2f} s")
            continue
        if l.startswith("[leitura]"):
            leit += 1
        if l.startswith(("[estouro]", "[deriva]", "[gatilho-sem-frase]")):
            avisos.append(f"{lote}: {l}")
for lote, _, _, _ in emendas:
    pass
pausas = sum(len(re.findall(r"pausa\(", (U / f).read_text(encoding="utf-8"))) for f in [p.name for p in U.glob("sec_*.py")])
L += ["emendas (quadro absoluto da 1ª âncora de cada lote × ini da âncora × fps; meta ±1 quadro):"]
pior_em = 0
for lote, aid, q, esp in emendas:
    pior_em = max(pior_em, abs(q - esp))
    L.append(f"  {lote:5s} {aid:6s} quadro {q:6d} · esperado {esp:6d} · {q - esp:+d} {'OK' if abs(q - esp) <= 1 else 'FORA'}")
L += ["", "avisos do log:"] + [f"  {x}" for x in avisos] + (["  nenhum"] if not avisos else [])
L += ["", "âncoras (início da âncora na tela × 1ª palavra na voz):"]
for aid, tela, voz, at in anc_l:
    L.append(f"  {aid:5s} tela {tela:8.2f} s · voz {voz:8.2f} s · {at:+.2f} s {'OK' if at <= 0.2 else 'FORA'}")
L += ["", f"gatilhos ({len(gat_l)}):"]
for a_, fr, tela, voz, at in gat_l:
    L.append(f"  {a_:5s} {at:+.2f} s  «{fr}»  (tela {tela:.2f} · voz {voz:.2f}) {'OK' if at <= 0.2 else 'FORA'}")
L += ["", f"fins de sublinhado ({len(fim_l)}; alvo = palavra da frase `ate` − LEAD):"]
for n_, a_, fr, tela, voz, at in fim_l:
    L.append(f"  leitura {n_:>2s} {a_:5s} {at:+.2f} s  «{fr}»  (tela {tela:.2f} · alvo {voz:.2f}) {'OK' if at <= 0.2 else 'FORA'}")
ats = [x[-1] for x in gat_l] + [x[-1] for x in anc_l] + [x[-1] for x in fim_l]
sem = sum(1 for x in avisos if "gatilho-sem-frase" in x)
L += ["", f"resumo: {len(anc_l)} âncoras, {len(gat_l)} gatilhos, {len(fim_l)} fins de sublinhado, {leit} leituras, {pausas} chamadas de pausa no código; "
          f"atraso de {min(ats):+.2f} a {max(ats):+.2f} s; fora da meta (> +0,2 s): {len(ruins)}; [gatilho-sem-frase] {sem}; pior emenda {pior_em} quadro(s)"]
L += [f"  {r}" for r in ruins]
(U / "qa").mkdir(exist_ok=True)
(U / "qa" / f"sync_{R}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
if R == "final":
    (U / "qa" / "sync.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L[-1 - len(ruins):]))
