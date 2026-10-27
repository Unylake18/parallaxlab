"""Confere confinamento, quantidade e movimento na geometria real da cena."""
import importlib.util
import json
from pathlib import Path

import numpy as np
from manim import ValueTracker

UNIT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cena_vid21", UNIT / "cena.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
scene = module.CicloTermodinamico021()
volume, pressure, temperature = ValueTracker(1), ValueTracker(1), ValueTracker(1)
vessel = scene.compact_piston(volume, pressure, temperature, with_readout=False)
gas, cloud = vessel[1], vessel.particles
samples = 0
for process in ("AB", "BC", "CA"):
    for alpha in np.linspace(0, 1, 241):
        v = 1+3*alpha if process == "AB" else 4 if process == "BC" else 4-3*alpha
        p = 1 if process == "AB" else 1+3*alpha if process == "BC" else v
        volume.set_value(v)
        pressure.set_value(p)
        temperature.set_value(v*p)
        gas.update(0)
        cloud.update(1/60)
        assert len(cloud) == 36
        for dot in cloud:
            assert dot.get_left()[0] >= gas.get_left()[0]
            assert dot.get_right()[0] <= gas.get_right()[0]
            assert dot.get_bottom()[1] >= gas.get_bottom()[1]
            assert dot.get_top()[1] <= gas.get_top()[1]
            assert dot.get_top()[1] <= gas.get_top()[1]-.08
        samples += 1

speeds = []
for temp in (1, 4, 16):
    temperature.set_value(temp)
    particles = scene.gas_particles(gas, temperature)
    before = np.array([dot.get_center() for dot in particles])
    particles.update(.0001)
    after = np.array([dot.get_center() for dot in particles])
    speeds.append(float(np.median(np.linalg.norm(after-before, axis=1))/.0001))
assert np.allclose(np.array(speeds)/speeds[0], [1, 2, 4])

temperature.set_value(1)
last = np.array([dot.get_center() for dot in cloud])
last_delta = None
rebounds = 0
for _ in range(300):
    cloud.update(1/60)
    points = np.array([dot.get_center() for dot in cloud])
    delta = points-last
    if last_delta is not None:
        rebounds += int(np.count_nonzero(delta[:, :2]*last_delta[:, :2] < 0))
    last, last_delta = points, delta
assert rebounds > 0

report = dict(particles=36, containment_samples=samples, containment="ok",
              speed_at_relative_T_1_4_16=speeds, speed_ratios=[1, 2, 4],
              rebounds_detected=rebounds, fixed_particle_count="ok",
              model="Ilustração 2D qualitativa; rapidez sqrt(T); posições transportadas com o domínio")
(Path(__file__).parent / "modelo.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(report, ensure_ascii=False))
