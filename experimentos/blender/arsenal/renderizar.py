"""Constrói um sólido do arsenal a partir do JSON e renderiza um still (sandbox).

Rodar, a partir da raiz do repositório (o `--` separa os argumentos do Blender dos nossos):
    blender.exe -b -P experimentos/blender/arsenal/renderizar.py -- <id> [opções]

Opções:
    --set nome=valor     sobrescreve um parâmetro (repetível), ex.: --set raio=1.5 --set n_cargas=60
    --res LxA            resolução (padrão 960x540)
    --amostras N         amostras do Eevee (padrão 64)
    --alpha              fundo transparente (PNG RGBA)
    --saida caminho.png  destino (padrão: previews/<id>.png sem overrides; senão out/arsenal_teste/)
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
from construtores import CONSTRUTORES  # noqa: E402


def ler_argumentos():
    resto = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(prog="renderizar.py")
    ap.add_argument("solido")
    ap.add_argument("--set", action="append", default=[], dest="overrides")
    ap.add_argument("--res", default="960x540")
    ap.add_argument("--amostras", type=int, default=64)
    ap.add_argument("--alpha", action="store_true")
    ap.add_argument("--saida")
    return ap.parse_args(resto)


def parametros(ficha, overrides):
    p = {k: v["valor"] for k, v in ficha["parametros"].items()}
    for o in overrides:
        nome, valor = o.split("=", 1)
        if nome not in p:
            raise SystemExit(f"Parâmetro desconhecido '{nome}'. Válidos: {', '.join(p)}")
        p[nome] = type(p[nome])(float(valor)) if isinstance(p[nome], (int, float)) else valor
    return p


def main():
    a = ler_argumentos()
    ficha = json.loads((AQUI / "solidos" / f"{a.solido}.json").read_text(encoding="utf-8"))
    # preview padrão (sem overrides na linha de comando): a ficha pode pedir um estado ilustrativo via `preview_set`
    p = parametros(ficha, a.overrides or ficha.get("preview_set", []))
    largura, altura = (int(x) for x in a.res.lower().split("x"))

    if a.saida:
        destino = Path(a.saida).resolve()   # relativo = contra a pasta de onde o Blender foi chamado
        destino.parent.mkdir(parents=True, exist_ok=True)
    elif not a.overrides and (largura, altura) == (960, 540) and not a.alpha:
        destino = AQUI / ficha["preview"]
    else:
        pasta = co.OUT / "arsenal_teste"
        pasta.mkdir(parents=True, exist_ok=True)
        destino = pasta / f"{a.solido}_{largura}x{altura}.png"

    co.limpar_cena()
    res = CONSTRUTORES[ficha["construtor"]](p)
    co.mundo()
    co.luzes()
    e = ficha["enquadramento"]
    cam = co.camera_enquadrada(co.cantos(res["enquadrar"]), azimute=e["azimute"], elevacao=e["elevacao"],
                               lente=e["lente"], margem=e["margem"], largura=largura, altura=altura)
    if res["apos_camera"]:
        res["apos_camera"](cam)
    if a.alpha:
        bpy.context.scene.render.film_transparent = True
        bpy.context.scene.render.image_settings.color_mode = "RGBA"

    t0 = time.perf_counter()
    co.render(destino, largura, altura, a.amostras)
    print(f"ARSENAL {a.solido} {largura}x{altura} amostras={a.amostras} alpha={a.alpha} "
          f"tempo={time.perf_counter() - t0:.2f}s -> {destino}")


if __name__ == "__main__":
    main()
