"""yt_0024 v2: quadros de conferência a 1920×1080 REAIS, renderizando só a animação que contém o instante (manim -n K,K a 1080p).
O modo still (-s) pula as animações e o Fundo3D não atualiza; aqui a animação K roda normalmente (3D da animação inteira renderizado a 1080p
com os estados de threejs/pedidos3d/<L>.json). K vem dos arquivos parciais do render 540p do lote (mesma cena, mesmos índices de animação).
uso: python conf1080.py [so=H1,B2-5] → renders/conferencia/<âncora>.png"""
import os
import re
import subprocess
import sys
from pathlib import Path

import av
from PIL import Image

U = Path(__file__).resolve().parent
SO = [a for x in sys.argv[1:] if x.startswith("so=") for a in x[3:].split(",")]
PED = ["H1", "H3", "A2", "B1-3", "B1-4", "B2-3", "B2-5", "B3-5", "B4-4", "B5-2", "B5-4", "B5-5", "B6-2", "B6-3", "B6-7", "B6-8", "S1", "S2"]
LOTE = {"H": "PH", "A": "PH", "B1": "PB1", "B2": "PB2", "B3": "PB3", "B4": "PB4", "B5": "PB5", "B6": "PB6", "S": "PS"}
PY = str(U.parents[1] / ".venv" / "Scripts" / "python.exe")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe",
           NODE_PATH=str((U.parent / "yt_0022_torque" / "threejs" / "node_modules").resolve()))
D = U / "renders" / "conferencia"


def instante(l, a):
    s = (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace")
    an = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", s)]
    tt = re.search(r"\[tempo\] total ([0-9.]+)", s)
    fim = float(tt.group(1)) if tt else an[-1][1] + 10
    for k, (x, t0) in enumerate(an):
        if x == a:
            return t0 + 0.85 * ((an[k + 1][1] if k + 1 < len(an) else fim) - t0)


def faixas(l):
    mapa = U / "renders" / f"mapa_anim_{l}.txt"
    if mapa.exists():                                   # lote com > 100 animações: o Manim apaga parciais velhos; usa o mapa da passada a seco
        out, ini = [], 0
        for ln in mapa.read_text(encoding="utf-8").splitlines():
            k, fim = (int(x) for x in ln.split()[1:3])
            out.append((k, ini, fim))
            ini = fim
        return out
    pf = sorted((U / f"media_{l}/videos/cena/540p15/partial_movie_files/{l}").glob("uncached_*.mp4"))
    out, ini = [], 0
    mt = max(f.stat().st_mtime for f in pf)
    for f in pf:
        if f.stat().st_mtime < mt - 3600:          # parcial velho de outro render (índice que este render não tem)
            continue
        with av.open(str(f)) as c:
            n = sum(1 for _ in c.decode(video=0))
        out.append((int(f.stem.split("_")[1]), ini, ini + n))
        ini += n
    return out


cache = {}
for a in (SO or PED):
    l = LOTE.get(a.split("-")[0], LOTE.get(a[0]))
    f = int(round(instante(l, a) * 15))
    if l not in cache:
        cache[l] = faixas(l)
    fx = cache[l]
    K, i0, i1 = next(((k, a0, a1) for k, a0, a1 in fx if a0 <= f < a1), fx[-1])
    if (U / "threejs" / "pedidos3d" / f"{l}.json").exists():
        subprocess.run(["node", "r3d.js", "--lote", l, "--w", "1920", "--h", "1080", "--so", ",".join(str(x) for x in range(i0, i1 + 1))],
                       cwd=U / "threejs", env=ENV, capture_output=True, text=True)
    md = U / f"media_c1080_{l}_{a}"
    subprocess.run([PY, "-m", "manim", "-r", "1920,1080", "--fps", "15", "--progress_bar", "none", "--disable_caching", "-n", f"{K},{K}", "cena.py", l],
                   cwd=U, env=dict(ENV, MEDIA_DIR=str(md)), capture_output=True, text=True)
    mp4 = next(iter(sorted(md.rglob(f"{l}.mp4"))), None) or next(iter(sorted(md.rglob("uncached_*.mp4"))), None)
    ok = False
    if mp4:
        with av.open(str(mp4)) as c:
            fr = list(c.decode(video=0))
        if fr:
            fr[min(len(fr) - 1, f - i0)].to_image().convert("RGB").save(D / f"{a}.png")
            ok = True
    for x in sorted(md.rglob("*"), reverse=True):
        x.unlink() if x.is_file() else x.rmdir()
    md.rmdir()
    print(f"{a}: {l} q{f} animação {K} ({i0}–{i1}) {'ok' if ok else 'FALHOU'}", flush=True)
