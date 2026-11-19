"""yt_0024 v2: quadros de conferência a 1920×1080 REAIS (handoff v2 §8.3) e zip de QA sem .mp4.
Para cada âncora pedida: instante t = início + 85 % da âncora no lote (linhas [ancora] do log_<L>.txt); o 3D desse quadro é renderizado a
1920×1080 (r3d.js --so, com os mesmos estados de threejs/pedidos3d/<L>.json) e o Manim roda a 1920×1080 com STILL=t e -s (quadro parado real).
uso: python conferencia24.py [rodada] [so=H1,B2-5]   → renders/conferencia/<âncora>.png, renders/prancha_conferencia.png, renders/qa_yt0024_<rodada>.zip"""
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v2"
SO = [a for x in sys.argv[2:] if x.startswith("so=") for a in x[3:].split(",")]
PED = ["H1", "H3", "A2", "B1-3", "B1-4", "B2-3", "B2-5", "B3-5", "B4-4", "B5-2", "B5-4", "B5-5", "B6-2", "B6-3", "B6-7", "B6-8", "S1", "S2"]
LOTE = {"H": "PH", "A": "PH", "B1": "PB1", "B2": "PB2", "B3": "PB3", "B4": "PB4", "B5": "PB5", "B6": "PB6", "S": "PS", "EN": "PS"}
PY = str(U.parents[1] / ".venv" / "Scripts" / "python.exe")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe",
           NODE_PATH=str((U.parent / "yt_0022_torque" / "threejs" / "node_modules").resolve()))
D = U / "renders" / "conferencia"
D.mkdir(parents=True, exist_ok=True)


def lote_de(a):
    return LOTE.get(a.split("-")[0], LOTE.get(a[0]))


def instante(l, a):
    s = (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace")
    an = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", s)]
    tt = re.search(r"\[tempo\] total ([0-9.]+)", s)
    fim = float(tt.group(1)) if tt else an[-1][1] + 10
    for k, (x, t0) in enumerate(an):
        if x == a:
            t1 = an[k + 1][1] if k + 1 < len(an) else fim
            return t0 + 0.85 * (t1 - t0)
    raise KeyError(a)


feitos = []
for a in (SO or PED):
    l = lote_de(a)
    t = round(instante(l, a), 3)
    f = int(round(t * 15))
    ped = U / "threejs" / "pedidos3d" / f"{l}.json"
    if ped.exists():
        so = ",".join(str(x) for x in range(max(0, f - 2), f + 3))
        r = subprocess.run(["node", "r3d.js", "--lote", l, "--w", "1920", "--h", "1080", "--so", so], cwd=U / "threejs", env=ENV, capture_output=True, text=True)
        if r.returncode:
            print(a, "3D falhou:", r.stderr[-300:])
    md = U / f"media_still_{l}_{a}"
    r = subprocess.run([PY, "-m", "manim", "-r", "1920,1080", "--fps", "15", "--progress_bar", "none", "--disable_caching", "-s", "cena.py", l],
                       cwd=U, env=dict(ENV, STILL=str(t), MEDIA_DIR=str(md)), capture_output=True, text=True)
    pngs = sorted(md.glob("images/cena/*.png"))
    if not pngs:
        print(a, "still falhou:", (r.stdout + r.stderr)[-400:])
        continue
    Image.open(pngs[-1]).convert("RGB").save(D / f"{a}.png")
    for x in sorted(md.rglob("*"), reverse=True):
        x.unlink() if x.is_file() else x.rmdir()
    md.rmdir()
    feitos.append((a, l, t))
    print(f"{a}: {l} t = {t:.2f} s (q{f}) → {D / (a + '.png')}")

ims = []
for a in PED:
    arq = D / f"{a}.png"
    if arq.exists():
        im = Image.open(arq).convert("RGB").resize((960, 540), Image.LANCZOS)
        ImageDraw.Draw(im).text((8, 6), a, fill=(255, 230, 0))
        ims.append(im)
P = Image.new("RGB", (960 * 3, 540 * ((len(ims) + 2) // 3)))
for k, im in enumerate(ims):
    P.paste(im, ((k % 3) * 960, (k // 3) * 540))
P.save(U / "renders" / "prancha_conferencia.png")
z = U / "renders" / f"qa_yt0024_{R}.zip"
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in sorted((U / "renders").glob("prancha_*_v2.png")) + [U / "renders" / "prancha_objetos.png", U / "renders" / "prancha_conferencia.png"]:
        if f.exists():
            zf.write(f, f"pranchas/{f.name}")
    for f in sorted(D.glob("*.png")):
        zf.write(f, f"conferencia_1920x1080/{f.name}")
    for f in sorted((U / "renders" / "objetos").glob("*")):
        zf.write(f, f"objetos_1920x1080/{f.name}")
    for f in sorted((U / "renders" / "casos").glob("*.png")):
        zf.write(f, f"casos_antes_depois/{f.name}")
    for nome in ("qa.txt", "casos_31.txt", "portao_triagem.txt", "fisica_conferencia.txt", "parado.txt", "flash.txt"):
        f = U / "renders" / nome
        if f.exists():
            zf.write(f, nome)
    for f in sorted(U.glob("log_aud_*.txt")) + sorted(U.glob("cor_operador_*.json")):
        zf.write(f, f"auditoria/{f.name}")
    for nome in ("ficha.md", "narracao_v1.md", "ancoras.json", "mesa_tab.json", "capitulos_youtube.txt"):
        if (U / nome).exists():
            zf.write(U / nome, nome)
print(json.dumps({"quadros": len(ims), "zip": str(z), "mb": round(z.stat().st_size / 1e6, 1)}))
