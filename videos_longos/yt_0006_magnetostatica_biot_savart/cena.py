"""5.2 · Lei de Biot–Savart. Uma cena contínua, preview 960×540 / 15 fps, sem voz.

Paleta e gramática do yt_0005 (B magenta · corrente verde · F azul claro · fios azul claro · geometria violeta).
MF-Tools (TransformByGlyphMap): cada termo de cada equação vem de um objeto do diagrama ou da equação anterior.
SEG=<seção>[,<seção>] renderiza só esses trechos; vazio = unidade inteira.

Preview:  uv run python -m manim -r 960,540 --fps 15 videos_longos/yt_0006_magnetostatica_biot_savart/cena.py YT0006BiotSavart
"""
import json
from pathlib import Path

from base import *  # noqa: F401,F403
from sec1 import Sec1
from sec2 import Sec2
from sec3 import Sec3
from sec4 import Sec4
from sec5 import Sec5
from sec6 import Sec6
from sec7 import Sec7

SECOES = ("abertura", "regime", "geometria", "lei", "distribuidas", "clinica", "superposicao", "metodo", "trecho_finito", "infinito", "fios_forca", "espira_eixo", "checagens", "sintese", "fechamento")


class YT0006BiotSavart(Sec7, Sec6, Sec5, Sec4, Sec3, Sec2, Sec1, Base):
    def construct(self):
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(WM_W).set_opacity(WM_OP).to_corner(UR, buff=0.3)
        self.tag = txt("ELETROMAGNETISMO · MAGNETOSTÁTICA", 18, opacity=0.6).to_corner(UL, buff=0.38)
        self.add(self.wm, self.tag)
        for nome in SECOES:
            getattr(self, nome)()
        out = Path(config.media_dir) / "qa_timeline.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"sections": self.sections, "checkpoints": self.checkpoints,
                                   "layout_issues": self.layout_issues, "duration": float(self.time),
                                   "plays": self.renderer.num_plays}, ensure_ascii=False, indent=2), encoding="utf-8")
