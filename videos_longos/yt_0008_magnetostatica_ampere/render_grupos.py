"""yt_0008 — render por grupos com o sincronismo da voz (estado de cada seção vem de qa_timeline.json de uma fumaça).

  uv run --no-sync python videos_longos/yt_0008_magnetostatica_ampere/render_grupos.py prev|final [FUMACA_DIR]
prev  = 960×540 / 15 fps (QA) → renders/prev_gN/ ; final = 1920×1080 / 30 fps (CRF 14 pelo template) → renders/final_gN/
Renderiza os 5 grupos em sequência e escreve renders/<modo>_ok.json. Pula grupo já renderizado.
"""
import json
import os
import subprocess
import sys
import time
import ctypes
from pathlib import Path

U = Path(__file__).resolve().parent
ROOT = U.parents[1]
ctypes.windll.kernel32.SetThreadExecutionState(0x80000001)   # ES_CONTINUOUS | ES_SYSTEM_REQUIRED: o PC não dorme enquanto isto roda
modo = sys.argv[1]
GRUPOS = [("g1", "", "divergente"), ("g2", "div_formal", "segundo_termo"), ("g3", "fio_finito", "stokes"),
          ("g4", "validade", "amp_toroide"), ("g5", "comparacao", "")]
res, fps = ("960,540", "15") if modo == "prev" else ("1920,1080", "30")
ant = U / "renders"          # o estado de cada grupo é o fim do anterior (mesma grade de 1/15 s no preview e no final): usa sempre o preview
log = U / "renders" / f"{modo}_log.txt"
for nome, de, ate in GRUPOS:
    out = U / "renders" / f"{modo}_{nome}"
    if list(out.glob("videos/cena/*/YT0008Ampere.mp4")):
        continue
    out.mkdir(parents=True, exist_ok=True)
    if not (out / "Tex").exists() and (U / "renders" / "sync3" / "Tex").exists():
        subprocess.run(["cmd", "/c", "xcopy", str(U / "renders" / "sync3" / "Tex"), str(out / "Tex"), "/E", "/I", "/Q", "/Y"], capture_output=True)
    env = dict(os.environ, DE=de, ATE=ate, PYTHONIOENCODING="utf-8", UV_PROJECT_ENVIRONMENT=os.environ.get(
        "UV_PROJECT_ENVIRONMENT", r"C:\Users\KaioOrtiz\PycharmProjects\manim-fisica\.venv"))
    if modo == "prev":
        env["QA_STILLS"] = "1"
    if de:
        n = int(nome[1:])
        t0, ev0, win = json.loads((ant / f"prev_g{n - 1}" / "qa_timeline.json").read_text(encoding="utf-8"))["fim_estado"]
        env.update(T0=str(t0), EV0=str(ev0))
        if win:
            env["WIN0"] = json.dumps(win)
    t = time.time()
    with open(out / "log.txt", "w", encoding="utf-8") as f:
        r = subprocess.run(["uv", "run", "--no-sync", "python", "-m", "manim", "-r", res, "--fps", fps, "--media_dir", str(out),
                            "--progress_bar", "none", "-v", "WARNING", str(U / "cena.py"), "YT0008Ampere"], cwd=ROOT, env=env, stdout=f, stderr=subprocess.STDOUT)
    with open(log, "a", encoding="utf-8") as f:
        f.write(f"{nome} DE={de!r} ATE={ate!r} exit {r.returncode} em {time.time() - t:.0f} s\n")
    if r.returncode:
        sys.exit(r.returncode)
(U / "renders" / f"{modo}_ok.json").write_text(json.dumps({"grupos": [g[0] for g in GRUPOS]}), encoding="utf-8")
