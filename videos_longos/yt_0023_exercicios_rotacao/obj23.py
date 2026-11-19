"""Prancha de objetos (v2 §7.1): carretel, volante, haste, pêndulo de discos e régua em 3/4 e frontal, com CONCÊNTRICO.
python obj23.py → renders/prancha_objetos.png + renders/conc_objetos.txt"""
import json, os, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
U = Path(__file__).resolve().parent
sys.path.insert(0, str(U))
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
from pecas23 import cam_car, cam_vol, cam_obl, cam_reg, estado_regua  # noqa: E402
import conc23  # noqa: E402

def fr(K, xc, yc, camx=0.0, camz=0.0):
    return {"modo": "frente", "K": K, "xc": xc, "yc": yc, "camx": camx, "camz": camz, "fov": 14}

CASOS = [
    ("carretel", "GERAL", {"th": 0.4, "trava": 1, "cam": cam_car(0.0, K=5.0, xc=-1.0, yc=0.7)}),
    ("carretel", "PERFIL", {"th": 0.4, "trava": 1, "cam": cam_obl(0.0, 4.0, [0.0, 0.0, 0.0], K=5.2, xc=-1.0, yc=0.7, fov=9.0)}),
    ("carretel", "EXPLODIDO", {"th": 0.4, "trava": 1, "explode": 1.0, "cam": cam_obl(-25.0, 12.0, [0.0, -0.03, 0.0], K=5.2, xc=-1.0, yc=0.7, fov=9.0)}),
    ("carretel", "frontal", {"th": 0.4, "trava": 0, "foco": "pequeno", "cam": cam_car(1.0)}),
    ("volante", "GERAL", {"th": 0.6, "cam": cam_vol(0.0, K=5.4, xc=-1.0, yc=0.8)}),
    ("volante", "CORTE", {"th": 0.0, "corte": 1.0, "cord": False, "cam": cam_obl(-18.0, 8.0, [0.0, 0.0, 0.0], K=5.2, xc=-1.0, yc=0.8, fov=9.0)}),
    ("volante", "EXPLODIDO", {"th": 0.0, "explode": 1.0, "cam": cam_obl(-35.0, 12.0, [0.0, 0.0, 0.0], K=5.0, xc=-1.0, yc=0.8, fov=9.0)}),
    ("volante", "frontal", {"th": 0.6, "foco": "anel", "cam": cam_vol(1.0, K=5.4, xc=-1.0, yc=0.8)}),
    ("haste", "3/4", {"th": 0.0, "cam": cam_obl(-62.0, 16.0, [0.25, 0, 0], K=5.2, xc=-3.6, yc=0.85, fov=16)}),
    ("haste", "frontal", {"th": 0.5, "cam": fr(5.2, -4.9, 0.85)}),
    ("pendulo", "3/4", {"p": [[0, 0, 0.30, 0.08, 1]], "cam": cam_obl(-62.0, 14.0, [0, 0, -0.15], K=9.0, xc=-5.0, yc=0.4, fov=16)}),
    ("pendulo", "frontal", {"p": [[-5.2 / 9, 1.75 / 9, 0.30, 0.08, 1]], "cam": fr(9.0, 0.0, 0.0)}),
]
er = estado_regua(0.0, massa_ponta=True)
CASOS.append(("regua", "frontal", dict(er, moeda_meio=False, cam=cam_reg())))

env = dict(os.environ, CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe",
           NODE_PATH=str((U / "../yt_0022_torque/threejs/node_modules").resolve()))
od = U / "renders/objetos"; od.mkdir(parents=True, exist_ok=True)
ims, linhas = [], []
for cena, vista, e in CASOS:
    png = od / f"{cena}_{vista.replace('/', '-')}.png"
    out = subprocess.run(["node", "r3d.js", "--sonda", cena, "--estado", json.dumps(e), "--png", str(png)], cwd=U / "threejs",
                         env=env, capture_output=True, text=True)
    js = [l for l in out.stdout.splitlines() if l.startswith("{")]
    pts = json.loads(js[-1])["pts"] if js else {}
    if cena == "regua":
        linhas.append(f"{cena:9s} {vista:8s} (régua do yt_0022: dobradiça com pino; sem pontos3d de conferência)")
    else:
        r = conc23.medir(pts or {})
        fl = conc23.falhas(r)
        linhas.append(f"{cena:9s} {vista:8s} " + "  ".join(f"{k} {v:.2f}" for k, v in r.items()) + ("  → FALHA " + ",".join(fl) if fl else "  → OK"))
    bg = Image.open(U / "fundo_lab_ex.png").convert("RGB").resize((960, 540)) if (U / "fundo_lab_ex.png").exists() else Image.new("RGB", (960, 540), (8, 14, 34))
    if png.exists():
        fg = Image.open(png).convert("RGBA"); bg.paste(fg, (0, 0), fg)
    im = bg.resize((480, 270)); ImageDraw.Draw(im).text((6, 4), f"{cena} {vista}", fill=(255, 255, 0)); ims.append(im)
cols = 4; rows = (len(ims) + cols - 1) // cols
pr = Image.new("RGB", (480 * cols, 270 * rows))
for k, im in enumerate(ims):
    pr.paste(im, ((k % cols) * 480, (k // cols) * 270))
pr.save(U / "renders/prancha_objetos.png")
(U / "renders/conc_objetos.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("\n".join(linhas))
