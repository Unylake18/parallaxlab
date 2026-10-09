"""Acrescenta " · EP. 05" à tag do canto superior esquerdo do render final já pronto (sem renderizar a cena de novo).

A cena (cena.py) já escreve a tag completa; este script só corrige o MP4 de postagem existente: renderiza a tag nova com o
mesmo texto/estilo da cena (Space Grotesk, 20, opacidade 0,65, canto superior esquerdo), apaga a região da tag antiga com a cor
de fundo (não há estrelas ali) e cola a nova em todos os quadros.

Uso, na raiz do repositório:
    uv run python videos/vid_0016_torricelli_alcance/patch_tag_ep.py ENTRADA.mp4 SAIDA.mp4
"""
from fractions import Fraction
from pathlib import Path
import sys

import av
import numpy as np
from PIL import Image

UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(UNIT))
from cena import text      # noqa: E402  (mesma função de texto da cena)
from manim import Scene, UP, LEFT, tempconfig  # noqa: E402

TAG = "DA EQUAÇÃO AO FENÔMENO · EP. 05"


def renderizar_tag(w, h):
    class Quadro(Scene):
        def construct(self):
            self.add(text(TAG, 20, opacity=0.65).to_corner(UP + LEFT, buff=0.4))

    with tempconfig({"frame_width": 9, "frame_height": 16, "pixel_width": w, "pixel_height": h, "transparent": True, "format": "png",
                     "save_last_frame": True, "write_to_movie": False, "media_dir": str(UNIT / "media_tag"), "verbosity": "WARNING",
                     "disable_caching": True, "output_file": "tag"}):
        cena = Quadro()
        cena.render()
        return Image.open(cena.renderer.file_writer.image_file_path).convert("RGBA")


def main(entrada, saida):
    with av.open(entrada) as inp:
        v = inp.streams.video[0]
        w, h, fps = v.width, v.height, float(v.average_rate)
    tag = renderizar_tag(w, h)
    x0, y0, x1, y1 = tag.getchannel("A").point(lambda p: 255 if p > 0 else 0).getbbox()
    x0, y0, x1, y1 = max(x0 - 8, 0), max(y0 - 8, 0), min(x1 + 8, w), min(y1 + 8, h)
    tag_rgba = np.asarray(tag).astype(np.float32)
    alfa = tag_rgba[y0:y1, x0:x1, 3:4] / 255.0
    cor_tag = tag_rgba[y0:y1, x0:x1, :3]
    if cor_tag[alfa[..., 0] > 0.55].max() < 200:            # PNG com alfa pré-multiplicado: recupera a cor reta
        cor_tag = np.where(alfa > 0.01, cor_tag / np.maximum(alfa, 0.01), 0)
    print(f"tag: caixa {x0},{y0} -> {x1},{y1}; {w}x{h}, {fps} fps")
    with av.open(entrada) as inp, av.open(saida, "w") as out:
        ent = inp.streams.video[0]
        s = out.add_stream("libx264", rate=round(fps))
        s.width, s.height, s.pix_fmt = w, h, "yuv420p"
        s.options = {"crf": "14", "preset": "medium"}
        for n, frame in enumerate(inp.decode(ent)):
            arr = frame.to_ndarray(format="rgb24")
            fundo = arr[(y0 + y1) // 2 - 2:(y0 + y1) // 2 + 3, x1 + 30:x1 + 35].reshape(-1, 3).mean(0)   # fundo liso ao lado da tag
            reg = np.empty((y1 - y0, x1 - x0, 3), np.float32)
            reg[:] = fundo
            reg = reg * (1 - alfa) + cor_tag * alfa
            arr[y0:y1, x0:x1] = np.clip(reg + 0.5, 0, 255).astype(np.uint8)
            novo = av.VideoFrame.from_ndarray(arr, format="rgb24")
            novo.pts, novo.time_base = n, Fraction(1, round(fps))
            for pacote in s.encode(novo):
                out.mux(pacote)
            if n % 600 == 0:
                print(f"{n} quadros", flush=True)
        for pacote in s.encode(None):
            out.mux(pacote)
    print("pronto", saida)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
