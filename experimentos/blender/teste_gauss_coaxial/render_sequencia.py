"""Teste de cena 3D montada no Blender: cabo coaxial + cilindro gaussiano que cresce + setas de E no vão (sandbox).

Nada aqui altera o arsenal nem o yt_0002: o script só IMPORTA os construtores existentes (coaxial, gaussiana, setas) e monta,
numa única cena Blender, um conjunto novo. O Manim (cena_manim.py) usa a sequência de PNG com alpha só para texto, fórmulas e
gráfico por cima.

Rodar, a partir da raiz do repositório:
    blender.exe -b -P experimentos/blender/teste_gauss_coaxial/render_sequencia.py -- [opções]

Opções:
    --frames N        quadros da sequência (padrão 90); o quadro i tem raio r = r0 + (r1 - r0) * i / (N - 1)
    --res LxA         resolução (padrão 1120x784, a proporção do painel 3D da cena Manim)
    --amostras N      amostras do Eevee (padrão 64)
    --r0 / --r1       raio inicial e final da gaussiana (padrão 0.25 e 1.95; coaxial a = 0.5, b = 1.5)
    --saida pasta     destino (padrão renders/teste_gauss_coaxial/<LxA>/; `renders/` é ignorado pelo Git)
"""

import argparse
import json
import math
import sys
import time
from pathlib import Path

import bpy

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(AQUI.parent))
import casca_oca as co  # noqa: E402
import coaxial as cx  # noqa: E402
import gaussiana as ga  # noqa: E402
import vetores3d as v3  # noqa: E402

RAIO_A, RAIO_B, COMPRIMENTO = 0.5, 1.5, 5.0     # coaxial (padrão do arsenal)
COMP_GAUSS = 3.0                                # comprimento (finito) do cilindro gaussiano
AZ, EL, LENTE, MARGEM = -23, 17, 50, 0.04       # mesmo ponto de vista do coaxial do arsenal


def argumentos():
    resto = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(prog="render_sequencia.py")
    ap.add_argument("--frames", type=int, default=90)
    ap.add_argument("--res", default="1120x784")
    ap.add_argument("--amostras", type=int, default=64)
    ap.add_argument("--r0", type=float, default=0.25)
    ap.add_argument("--r1", type=float, default=1.95)
    ap.add_argument("--saida")
    return ap.parse_args(resto)


def gaussiana(r):
    """Gaussiana cilíndrica: lateral contínua (contribui ao fluxo), tampas tracejadas (E ⟂ n̂ nelas)."""
    return ga.criar_gaussiana_cilindrica(r, COMP_GAUSS, lateral_continua=1, tampas_continuas=0, n_linhas=4, faces=1)


def remover(objs):
    for o in objs:
        bpy.data.objects.remove(o, do_unlink=True)


def setas_do_vao():
    """Campo E confinado ao vão a < r < b: radial para fora (carga positiva dentro), em ciano (cor reservada ao campo)."""
    mat = v3.material_cor("CampoVao", "campo_eletrico", 2.2)
    r_ini, comp = RAIO_A + 0.12, 0.62
    out = []
    for x, graus in ((-1.7, 118), (-0.55, 138), (0.55, 158), (1.7, 124), (0.0, 108)):
        t = math.radians(graus)
        d = (0.0, math.cos(t), math.sin(t))
        out.append(v3.seta((x, r_ini * d[1], r_ini * d[2]), d, mat, comprimento=comp))
    return out


def main():
    a = argumentos()
    largura, altura = (int(x) for x in a.res.lower().split("x"))
    pasta = Path(a.saida).resolve() if a.saida else RAIZ / "renders" / "teste_gauss_coaxial" / a.res
    pasta.mkdir(parents=True, exist_ok=True)

    co.limpar_cena()
    _, externo, _ = cx.criar_coaxial(raio_a=RAIO_A, raio_b=RAIO_B, comprimento=COMPRIMENTO)
    setas_do_vao()
    co.mundo()
    co.luzes()
    # câmera fixa: enquadra o coaxial e a gaussiana no raio máximo (assim nada sai do quadro durante o crescimento)
    maxima = gaussiana(a.r1)
    pontos = co.cantos([externo, maxima[-1]])
    remover(maxima)
    cam = co.camera_enquadrada(pontos, azimute=AZ, elevacao=EL, lente=LENTE, margem=MARGEM, largura=largura, altura=altura)
    import cilindro_macico as cm  # noqa: E402
    cm.ajustar_profundidade(cam, externo)
    sc = bpy.context.scene
    sc.render.film_transparent = True
    sc.render.image_settings.color_mode = "RGBA"

    co.render(pasta / "_aquecimento.png", largura, altura, a.amostras)
    (pasta / "_aquecimento.png").unlink()
    tempos = []
    for i in range(a.frames):
        r = a.r0 + (a.r1 - a.r0) * i / (a.frames - 1)
        objs = gaussiana(r)
        sc.render.filepath = str(pasta / f"frame_{i + 1:04d}.png")
        t0 = time.perf_counter()
        bpy.ops.render.render(write_still=True)
        tempos.append(time.perf_counter() - t0)
        remover(objs)
    (pasta / "meta.json").write_text(json.dumps(
        {"frames": a.frames, "r0": a.r0, "r1": a.r1, "a": RAIO_A, "b": RAIO_B, "res": a.res, "amostras": a.amostras},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"TESTE_GAUSS_COAXIAL {largura}x{altura} frames={a.frames} medio={sum(tempos) / len(tempos):.2f}s "
          f"total={sum(tempos):.1f}s -> {pasta}")


if __name__ == "__main__":
    main()
