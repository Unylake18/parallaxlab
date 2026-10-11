"""Registra a cena sem render de quadros e distribui o tempo do áudio em operações."""
import json
from pathlib import Path
import sys
import numpy as np
from manim import tempconfig

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0, str(UNIT))
from cena_final import PlanejarIntegral020

OUT = ROOT / "media/vid_0020_final"
FPS = 30


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    recorded = OUT / "planejamento/operacoes_originais.json"
    if not recorded.is_file():
        with tempconfig({"media_dir": str(OUT / "planejamento"), "pixel_width": 270, "pixel_height": 480,
                         "frame_rate": FPS, "dry_run": True, "write_to_movie": False, "progress_bar": "none",
                         "verbosity": "WARNING", "disable_caching": True}):
            scene = PlanejarIntegral020(skip_animations=True)
            scene.render()
    native = json.loads(recorded.read_text(encoding="utf-8"))
    operations, boundaries = native["operations"], native["boundaries"]
    boundaries.update(soma_colunas=boundaries["geracao_16_colunas"] + 4,
                      separacao_inicio=boundaries["integral_y_isolada"] + 1,
                      resultado_decimal=boundaries["resultado_exato"] + 2,
                      mensagem_final=boundaries["payoff"] + 4)
    anchors = json.loads((UNIT / "sync.json").read_text())["anchors"]
    locations = [(name, boundaries[name], round(time * FPS)) for name, time in anchors]
    assert locations[0][1] == 0 and locations[-1][1] == len(operations)
    assert all(a[1] < b[1] and a[2] < b[2] for a, b in zip(locations, locations[1:])), locations
    algebra_start, algebra_end = boundaries["integral_iterada"], boundaries["payoff"]
    schedule = []
    intervals = []
    for (name, a, start), (next_name, b, end) in zip(locations, locations[1:]):
        block = operations[a:b]
        budget = end - start
        desired = np.array([max(1, min(round(op["duration"] * FPS), int(1.25 * FPS)))
                            if algebra_start <= op["index"] < algebra_end and not op["pause"]
                            else max(1, round(op["duration"] * FPS)) for op in block])
        original = desired.copy()
        holds = np.zeros(len(block), dtype=int)
        if desired.sum() > budget:
            # Comprime o bloco para caber na fala, preservando pelo menos um quadro por operação.
            weights = np.maximum(desired - 1, 0)
            fractional = weights / weights.sum() * (budget - len(block))
            desired = 1 + np.floor(fractional).astype(int)
            for i in np.argsort(-(fractional - np.floor(fractional)))[:budget - desired.sum()]:
                desired[i] += 1
        else:
            slack = budget - desired.sum()
            pauses = [i for i, op in enumerate(block) if op["pause"]]
            if pauses:
                weights = desired[pauses] / desired[pauses].sum()
                extra = np.floor(weights * slack).astype(int)
                for i in np.argsort(-(weights * slack - extra))[:slack - extra.sum()]:
                    extra[i] += 1
                desired[pauses] += extra
            else:
                holds[-1] = slack
        assert desired.sum() + holds.sum() == budget
        for op, frames, hold in zip(block, desired, holds):
            schedule.append(dict(**op, frames=int(frames), hold_after=int(hold)))
        intervals.append(dict(from_anchor=name, to_anchor=next_name, start=start / FPS, end=end / FPS,
                              motion_seconds=sum(int(n) for n, op in zip(desired, block) if not op["pause"]) / FPS,
                              pause_seconds=(sum(int(n) for n, op in zip(desired, block) if op["pause"]) + int(holds.sum())) / FPS))
    total_frames = round(171.8 * FPS)
    plan = dict(fps=FPS, lead_frames=locations[0][2], tail_frames=total_frames - locations[-1][2],
                total_frames=total_frames, anchors=[dict(name=n, boundary=i, frame=f) for n, i, f in locations],
                operations=schedule, intervals=intervals)
    assert plan["lead_frames"] + sum(op["frames"] + op["hold_after"] for op in schedule) + plan["tail_frames"] == total_frames
    assert max(op["frames"] / FPS for op in schedule[algebra_start:algebra_end] if not op["pause"]) <= 1.25
    (UNIT / "timing_final.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print(json.dumps(dict(operations=len(operations), frames=total_frames, seconds=total_frames / FPS,
                         longest_algebra_motion=max(op["frames"] / FPS for op in schedule[algebra_start:algebra_end] if not op["pause"]))), flush=True)


if __name__ == "__main__":
    main()
