"""yt_0009 — auditoria de sincronia fala × cena.

Uso:  DBG=1 SYNC=ritmo.json manim ... > log ; depois
      uv run --no-sync python auditoria_sync.py LOG.txt [VIDEO.mp4]

1) Cada âncora (unidade da narração) da cena tem de começar no instante em que a voz começa essa unidade (tolerância 0,15 s).
2) Se o vídeo for dado: procura trechos de ≥ 2 s sem mudança visível (tela parada) e lista a unidade a que pertencem.
"""
import json
import re
import sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent
GAP, HOOK_EST = 0.5, 20.0


def onsets():
    sy = json.load(open(PASTA / "sync.json", encoding="utf-8"))
    cel = {c["chave"]: c["onset"] for c in sy["celulas"]}
    for k_, wi in (("N057a", 2389), ("N057b", 2399), ("N057c", 2411), ("N057d", 2418)):
        cel[k_] = sy["words"][wi][1] - 0.25
    f = PASTA / "audio" / "gancho_dur.txt"
    cel["N059"] = sy["dur"] + GAP
    return cel, sy["dur"] + GAP + (float(f.read_text()) if f.exists() else HOOK_EST)


def main():
    log = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
    cel, fim = onsets()
    got = {}
    for m in re.finditer(r"\[ANC\] (N\d+\w?) t_cena=\s*([\d.]+) tgt=\s*([\d.]+) emit_s=\s*([\d.]+)", log):
        got[m.group(1)] = float(m.group(4))
    bad = 0
    print("unidade   fala(s)   cena(s)   delta")
    for k, t in sorted(cel.items(), key=lambda kv: kv[1]):
        if k not in got:
            print(f"{k:8s} {t:8.2f}   --  (âncora ausente na cena)")
            bad += 1
            continue
        d = got[k] - t
        flag = "  <<<" if abs(d) > 0.15 else ""
        bad += abs(d) > 0.15
        print(f"{k:8s} {t:8.2f} {got[k]:8.2f} {d:+7.2f}{flag}")
    extra = sorted(set(got) - set(cel))
    print(f"\nâncoras fora da fala: {extra}")
    print(f"fim da fala+gancho: {fim:.2f} s ; unidades fora de 0,15 s: {int(bad)}")
    if len(sys.argv) > 2:
        import av
        import numpy as np
        c = av.open(sys.argv[2])
        s = c.streams.video[0]
        prev, ts, d = None, [], []
        for x in c.decode(s):
            g = np.asarray(x.to_image().convert("L").resize((160, 90)), dtype=np.float32)
            if prev is not None:
                d.append(float(np.abs(g - prev)[8:].mean()))
                ts.append(float(x.pts * s.time_base))
            prev = g
        fps = len(ts) / max(ts[-1] - ts[0], 1e-6)
        runs, st = [], None
        for i, v in enumerate(d + [1.0]):
            if v < 0.05:
                st = i if st is None else st
            else:
                if st is not None and (i - st) / fps >= 2.0:
                    runs.append((ts[st], (i - st) / fps))
                st = None
        un = sorted(got.items(), key=lambda kv: kv[1])

        def unidade(t):
            u = "?"
            for k, v in un:
                if v <= t:
                    u = k
            return u
        print(f"\ntrechos parados ≥ 2 s: {len(runs)}")
        for t, dur in runs:
            print(f"  t={t:7.1f}s  {dur:4.1f}s  {unidade(t)}")


if __name__ == "__main__":
    main()
