"""Validação localizada ou render de postagem, sem sobrescrever a V4."""
import sys
from pathlib import Path
from manim import tempconfig
from cena import LinhasCarga015, UNIT

postagem = "--postagem" in sys.argv
options = {
    "pixel_width": 1080 if postagem else 540,
    "pixel_height": 1920 if postagem else 960,
    "frame_rate": 30 if postagem else 15,
    "media_dir": str(UNIT / ("media_postagem" if postagem else "media_qa_mao")),
    "tex_dir": str(UNIT / "media/Tex"),
    "output_file": "vid_0015_postagem_visual" if postagem else "vid_0015_qa_mao_direita",
    "disable_caching": True,
    "write_to_movie": True,
    "preview": False,
}
if not postagem:
    options.update(from_animation_number=90, upto_animation_number=105)
with tempconfig(options):
    scene = LinhasCarga015()
    scene.qa_frame_dir = "frames_qa_mao_direita"
    scene.qa_output = "qa_estados_postagem.json" if postagem else "qa_estados_mao_direita.json"
    scene.render()
