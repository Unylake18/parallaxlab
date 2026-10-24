"""yt_0009 — calcula ritmo.json: fatores de escala (animações fa, esperas fw) e pad de cada intervalo entre âncoras (unidades N001..N058),
para que cada unidade da cena dure exatamente o que a voz dura.

  PLAN=1 uv run --no-sync python -m manim --dry_run ... cena.py QuemEmpurraCargasYT009   → plan.json (nominal por âncora)
  uv run --no-sync python videos_longos/yt_0009_quem_empurra_as_cargas/ritmo_sync.py       → ritmo.json + relatório

Política: sobra de tempo → animações mais lentas (até ACAP) e o resto nas esperas (cena viva por updaters); falta de tempo →
esperas encolhem (até H_MIN), depois as animações (até A_MIN); se ainda assim não couber, relata overflow."""
import json
from pathlib import Path

PASTA = Path(__file__).resolve().parent
ACAP, A_MIN, H_MIN, TAIL = 1.4, 0.70, 0.30, 3.0
HOOK_EST = 20.0
GAP = 0.5            # silêncio entre a narração v8 e o gancho


def main():
    sy = json.load(open(PASTA / "sync.json", encoding="utf-8"))
    pl = json.load(open(PASTA / "plan.json", encoding="utf-8"))
    cel = list(sy["celulas"])
    # sub-âncoras dentro de N057: cada cartão de distinção entra quando a fala chega nele (índices de palavra em sync.json)
    for k_, wi in (("N057a", 2389), ("N057b", 2399), ("N057c", 2411), ("N057d", 2418)):
        cel.append({"chave": k_, "onset": sy["words"][wi][1] - 0.25})
    cel.sort(key=lambda c: c["onset"])
    end = sy["dur"]
    if "N059" in pl:        # gancho do próximo vídeo: voz ainda não gerada → duração estimada (arquivo audio/gancho_dur.txt a substitui)
        f = PASTA / "audio" / "gancho_dur.txt"
        hook = float(f.read_text().strip()) if f.exists() else HOOK_EST
        cel.append({"chave": "N059", "onset": sy["dur"] + GAP})
        end = sy["dur"] + GAP + hook
    out, rel = {}, []
    for i, c in enumerate(cel):
        k = c["chave"]
        D = (cel[i + 1]["onset"] if i + 1 < len(cel) else end + TAIL) - c["onset"]
        na, nw = pl[k]["na"], pl[k]["nw"]
        N = na + nw
        pad = 0.0
        if N <= 0:
            fa = fw = 1.0
            pad = D
        elif D >= N:
            f = D / N
            if f <= ACAP:
                fa = fw = f
            else:
                fa = fw = ACAP
                pad = D - ACAP * N          # folga: preenchida por estímulos novos (self.fill) ou destaques
        else:
            fw = H_MIN
            fa = (D - H_MIN * nw) / na if na else 1.0
            if fa < A_MIN:
                fa = A_MIN
                fw = (D - A_MIN * na) / nw if nw else 1.0
                if fw < 0.1:
                    fw = 0.1
        tot = fa * na + fw * nw + pad
        idle = pad
        out[k] = {"fa": round(fa, 4), "fw": round(fw, 4), "pad": round(pad, 3)}
        rel.append((k, D, tot, fa, fw, pad, idle))
    json.dump(out, open(PASTA / "ritmo.json", "w", encoding="utf-8"), indent=1)
    print("unid    voz   cena   fa    fw    pad   ocioso")
    for k, D, tot, fa, fw, pad, idle in rel:
        flag = "  <<< ESTOURA" if tot > D + 0.3 else ("  << ocioso" if idle > 9 else "")
        print(f"{k}  {D:5.1f}  {tot:5.1f}  {fa:4.2f}  {fw:4.2f}  {pad:5.1f}  {idle:5.1f}{flag}")


if __name__ == "__main__":
    main()
