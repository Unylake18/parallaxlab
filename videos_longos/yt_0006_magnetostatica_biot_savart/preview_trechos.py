"""Render localizado, sem tocar nas cenas de referência.

uv run --no-sync python -m manim -r 960,540 --fps 15 --media_dir ... preview_trechos.py RevisaoEspira
"""
import json
from pathlib import Path
from manim import ImageMobject, UR, UL, ValueTracker, Line, config
from cena import YT0006BiotSavart, WATERMARK_PATH, WM_W, WM_OP, txt, BLUE_L


class TrechoBase(YT0006BiotSavart):
    def iniciar(self):
        self.wm=ImageMobject(str(WATERMARK_PATH)).set_width(WM_W).set_opacity(WM_OP).to_corner(UR,buff=.3)
        self.tag=txt("ELETROMAGNETISMO · MAGNETOSTÁTICA",18,opacity=.6).to_corner(UL,buff=.38)
        self.add(self.wm,self.tag)

    def finalizar(self,name):
        out=Path(config.media_dir)/f"qa_trecho_{name}.json"
        out.write_text(json.dumps({"checkpoints":self.checkpoints,"sections":self.sections,"motion_windows":self.motion_windows,"layout_issues":self.layout_issues,"plays":self.renderer.num_plays},ensure_ascii=False,indent=2),encoding="utf-8")


class RevisaoEspira(TrechoBase):
    def construct(self):
        self.iniciar()
        self.espira_no_eixo()
        self.checagens_espira()
        self.finalizar("espira")


class RevisaoInicio(TrechoBase):
    def construct(self):
        self.iniciar()
        self.abertura()
        self.regime_magnetostatico()
        self.geometria_local()
        self.biot_savart()
        self.finalizar("inicio")


class RevisaoTrecho(TrechoBase):
    def construct(self):
        self.iniciar()
        self.trecho_finito()
        self.limite_infinito()
        self.forca_entre_fios()
        self.finalizar("trecho")


class RevisaoPausa(TrechoBase):
    """Verifica fluxo numa pausa real e o custo do prefixo estático do Cairo."""
    def construct(self):
        self.iniciar()
        self.section("pausa","Corrente estacionária: fluxo sem acúmulo")
        self.add(Line([-6,0,0],[-1,0,0],color=BLUE_L,stroke_width=6))
        self.add(self.flow([lambda u:[-6+5*u,0,0]],count=8))
        self.show_eq(r"\frac{\partial\rho}{\partial t}=0\quad\Rightarrow\quad\nabla\cdot\mathbf J=0",y=1.2,size=36)
        self.caption("Sem acúmulo local; a corrente continua atravessando a região")
        self.hold(4)
