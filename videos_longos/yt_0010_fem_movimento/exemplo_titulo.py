"""Exemplo estático (1 quadro) do espaçamento título/cabeçalho/campo: estado do N30 (barra solta, equação)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cena import *  # noqa: F401,F403
from cena import FemMovimentoYT010, Ap


class ExemploTitulo(FemMovimentoYT010):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        ap = self.ap = Ap()
        self.tag = txt("ELETROMAGNETISMO · FEM DE MOVIMENTO E REGRA DO FLUXO MAGNÉTICO", 24, opacity=0.78) \
            .to_corner(UL, buff=0.32).set_z_index(40)
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(0.45).to_corner(UR, buff=0.3)
        self.wm.set_z_index(40)
        self.tag.scale(0.66, about_point=self.tag.get_corner(UL)).set_opacity(0.3)
        self.add(self.tag, self.wm)
        self.hd, self.E = None, VGroup()
        self.Tu, self.Tvd, self.Tw, self.Tf, self.Tfb = (ValueTracker(0) for _ in range(5))
        self.mk_labels()
        self.mk_legend()
        s, cx, cy, f = LAYOUTS["left"]
        for tr, v in ((ap.s, s), (ap.cx, cx), (ap.cy, cy), (ap.fol, f), (ap.clx, CLIPX["left"]), (ap.oAll, 1), (ap.oB, 1),
                      (ap.oBar, 1), (ap.oU, 1), (ap.oI, 1), (ap.oF, 1), (ap.oP, 1), (ap.cur, 0.6), (ap.heat, 0.4),
                      (ap.fm, 0.6), (ap.ua, 0.6), (ap.xb, 2.0)):
            tr.set_value(v)
        ap.mode = "decay"
        ap.tt.set_value(0.5)
        ap.tick(0.0)
        self.add(always_redraw(ap.build))
        for k in ("u", "I", "Fm", "R", "Pm"):
            self.L[k].v.set_value(1)
        self.add(self.legend)
        self.H("Segunda lei de Newton")
        self.add(self.hd)
        f2 = M("m", r"\frac{du}{dt}", "=", r"-\frac{B^2l^2}{R}", "u").move_to(P3(EQX, 1.6))
        self.add(f2, boxed(f2), MathTex(r"m:\ \text{massa da barra}", font_size=26, color=DIM).move_to(P3(EQX, 0.3)))
        bt = MathTex(r"t=0\ \cdot\ \text{soltura}", font_size=34, color=WHITE)
        self.add(VGroup(bt, boxed(bt, color=CYAN, buff=0.16, width=3)).move_to(P3(-3.4, -1.75)))
        self.add(self.glossary(["m", "R", "u", "tau"]) if False else VGroup())
