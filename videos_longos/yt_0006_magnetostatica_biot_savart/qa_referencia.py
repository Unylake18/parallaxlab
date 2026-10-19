"""Render de QA: apenas o fechamento atual do 5.1, sem editar sua unidade."""
import importlib.util
import sys
from pathlib import Path
from manim import ImageMobject, UR, UL, tempconfig

sys.dont_write_bytecode = True
UNIT=Path(__file__).resolve().parent
path=UNIT.parent/"yt_0005_magnetostatica_forca_lorentz"/"cena.py"
spec=importlib.util.spec_from_file_location("referencia_51",path)
ref=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


class QAContinuidade51(ref.YT0005MagnetostaticaM1):
    def construct(self):
        self.wm=ImageMobject(str(ref.WATERMARK_PATH)).set_width(ref.WM_W).set_opacity(ref.WM_OP).to_corner(UR,buff=0.3)
        self.tag=ref.txt(ref.HEADER,18,opacity=0.6).to_corner(UL,buff=0.38)
        self.add(self.wm,self.tag)
        self.b09_fios()  # código real atual, sem cópia nem alteração


if __name__=="__main__":
    with tempconfig({"media_dir":str(UNIT/"renders"/"referencia_51"),"pixel_width":960,"pixel_height":540,"frame_rate":15,"progress_bar":"none","verbosity":"WARNING"}):
        QAContinuidade51().render()
