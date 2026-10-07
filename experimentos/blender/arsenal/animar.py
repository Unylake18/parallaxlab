"""Renderiza um loop de um sólido do arsenal que tenha `atualizar(fase)` (cargas em movimento) — sandbox.

Rodar, a partir da raiz do repositório (o `--` separa os argumentos do Blender dos nossos):
    blender.exe -b -P experimentos/blender/arsenal/animar.py -- <id> [opções]

Opções:
    --set nome=valor     sobrescreve um parâmetro (repetível); `cargas_moveis=1` é ligado automaticamente
    --frames N           quadros do loop (padrão 30): quadro i usa fase = i/N; o loop fecha sem repetir quadro
    --res LxA            resolução (padrão 960x540)
    --amostras N         amostras do Eevee (padrão 64)
    --alpha              fundo transparente (PNG RGBA)
    --saida pasta        pasta de destino (padrão: out/arsenal_teste/<id>_loop)
"""

import argparse
import json
import sys
import time
from pathlib import Path

import bpy

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent))
import casca_oca as co  # noqa: E402
import renderizar as R  # noqa: E402
from construtores import CONSTRUTORES  # noqa: E402


def main():
    resto = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(prog="animar.py")
    ap.add_argument("solido")
    ap.add_argument("--set", action="append", default=[], dest="overrides")
    ap.add_argument("--frames", type=int, default=30)
    ap.add_argument("--res", default="960x540")
    ap.add_argument("--amostras", type=int, default=64)
    ap.add_argument("--alpha", action="store_true")
    ap.add_argument("--saida")
    a = ap.parse_args(resto)

    ficha = json.loads((AQUI / "solidos" / f"{a.solido}.json").read_text(encoding="utf-8"))
    if "cargas_moveis" not in ficha["parametros"]:
        raise SystemExit(f"'{a.solido}' não tem cargas móveis (parâmetro cargas_moveis ausente na ficha)")
    p = R.parametros(ficha, ["cargas_moveis=1", *a.overrides])
    largura, altura = (int(x) for x in a.res.lower().split("x"))
    pasta = Path(a.saida).resolve() if a.saida else co.OUT / "arsenal_teste" / f"{a.solido}_loop"
    pasta.mkdir(parents=True, exist_ok=True)

    co.limpar_cena()
    res = CONSTRUTORES[ficha["construtor"]](p)
    co.mundo()
    co.luzes()
    e = ficha["enquadramento"]
    cam = co.camera_enquadrada(co.cantos(res["enquadrar"]), azimute=e["azimute"], elevacao=e["elevacao"],
                               lente=e["lente"], margem=e["margem"], largura=largura, altura=altura)
    if res["apos_camera"]:
        res["apos_camera"](cam)
    sc = bpy.context.scene
    if not res.get("atualizar"):
        raise SystemExit(f"'{a.solido}' não devolveu atualizar(fase): sem movimento neste sólido")
    if a.alpha:
        sc.render.film_transparent = True
        sc.render.image_settings.color_mode = "RGBA"

    co.render(pasta / "_aquecimento.png", largura, altura, a.amostras)     # configura o motor e aquece shaders
    (pasta / "_aquecimento.png").unlink()
    tempos = []
    for i in range(a.frames):
        res["atualizar"](i / a.frames)
        sc.render.filepath = str(pasta / f"frame_{i + 1:04d}.png")
        t0 = time.perf_counter()
        bpy.ops.render.render(write_still=True)
        tempos.append(time.perf_counter() - t0)
    print(f"ANIMAR {a.solido} {largura}x{altura} frames={a.frames} medio={sum(tempos) / len(tempos):.2f}s "
          f"total={sum(tempos):.1f}s -> {pasta}")


if __name__ == "__main__":
    main()
