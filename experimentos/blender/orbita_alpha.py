"""Teste de integração: sequência PNG com alpha (câmera orbitando a casca) — sandbox.

Rodar a partir da raiz do repositório:
    blender.exe -b -P experimentos/blender/orbita_alpha.py

Gera out/orbita_alpha/frame_0001.png ... (960x540, 15 fps, fundo transparente) e imprime o tempo por frame.
Sem keyframes: a rotação é definida frame a frame por Python (mais simples de sincronizar com o Manim).
"""

import math
import sys
import time
from pathlib import Path

import bpy
from mathutils import Matrix

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402

N_FRAMES = 30            # 2 s a 15 fps
GIRO_GRAUS = 40          # varredura total da câmera em torno do eixo Z
PASTA = co.OUT / "orbita_alpha"


def main():
    PASTA.mkdir(parents=True, exist_ok=True)
    co.limpar_cena()
    obj = co.criar_casca_oca()
    co.material_casca(obj)
    co.mundo()
    co.luzes()
    # A câmera gira +θ em torno de Z; equivale ao objeto girar -θ. Enquadrar todo o arco evita cortes.
    base = co.cantos([obj])
    arco = [Matrix.Rotation(-math.radians(GIRO_GRAUS * k / 8), 4, "Z") @ p
            for k in range(9) for p in base]
    co.camera_enquadrada(arco, margem=0.07)

    sc = bpy.context.scene
    # Pivô vazio na origem; a câmera é filha dele, então girar o pivô orbita a câmera.
    pivo = bpy.data.objects.new("Pivo", None)
    bpy.context.collection.objects.link(pivo)
    sc.camera.parent = pivo

    sc.render.film_transparent = True                 # fundo vira alpha
    sc.render.image_settings.color_mode = "RGBA"

    # Mesma configuração de render da casca (Eevee, 960x540, Standard).
    co.render(PASTA / "_aquecimento.png")             # configura o motor e aquece shaders
    (PASTA / "_aquecimento.png").unlink()

    tempos = []
    for i in range(N_FRAMES):
        t = i / (N_FRAMES - 1)
        pivo.rotation_euler[2] = math.radians(GIRO_GRAUS * t)
        sc.render.filepath = str(PASTA / f"frame_{i + 1:04d}.png")
        t0 = time.perf_counter()
        bpy.ops.render.render(write_still=True)
        tempos.append(time.perf_counter() - t0)

    print(f"TEMPO_POR_FRAME medio={sum(tempos) / len(tempos):.2f}s "
          f"max={max(tempos):.2f}s total={sum(tempos):.1f}s frames={N_FRAMES}")


main()
