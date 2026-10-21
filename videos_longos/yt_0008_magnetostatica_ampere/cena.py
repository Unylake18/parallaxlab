"""5.3 · Divergente e rotacional de B, Lei de Ampère e aplicações. Uma cena contínua, preview 960×540 / 15 fps, sem voz.

Gramática do yt_0005/yt_0006 (B magenta · corrente verde · geometria violeta · cartões azul-escuro) e o kit do yt_0006
(MF-Tools com proveniência dos termos). Derivações N06–N10: observador r, ∇ em ciano; fonte r', ∇', J(r') em verde.
SEG=<seção>[,<seção>] renderiza só esses trechos (as demais executam sem quadros); SEG=nenhuma = fumaça.
ATE=<método> interrompe depois daquele bloco (render por trechos sem executar o resto).

Preview:  SEG=... uv run --no-sync python -m manim -r 960,540 --fps 15 videos_longos/yt_0008_magnetostatica_ampere/cena.py YT0008Ampere
"""
import json
import os
from pathlib import Path

from base import *  # noqa: F401,F403
from geo import Geo
from sec1 import Sec1
from sec2 import Sec2
from sec3 import Sec3
from sec4 import Sec4
from sec5 import Sec5
from sec6 import Sec6
from sec7 import Sec7

SECOES = ("abertura", "pergunta", "paradoxo", "sonda", "circulacao_global", "divergente",            # N01–N05
          "div_formal", "dois_nablas", "rot_formal", "delta", "segundo_termo",           # N06–N10
          "fio_finito", "fio_externo", "limite_filamentar", "superficie", "stokes",      # N11–N15
          "validade", "amp_fio", "amp_lamina", "amp_solenoide", "amp_toroide",           # N16–N20
          "comparacao", "sintese", "gancho", "cta")                                      # N21–N23 + encerramento
ATE = os.environ.get("ATE", "")


class YT0008Ampere(Sec7, Sec6, Sec5, Sec4, Sec3, Sec2, Sec1, Geo, Base):
    def construct(self):
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(WM_W).set_opacity(WM_OP).to_corner(UR, buff=0.3)
        self.tag = txt("ELETROMAGNETISMO · MAGNETOSTÁTICA", 18, opacity=0.6).to_corner(UL, buff=0.38)
        self.add(self.wm, self.tag)
        de = os.environ.get("DE", "")      # começa neste bloco (N14 em diante não dependem de estado anterior)
        for nome in SECOES[SECOES.index(de) if de else 0:]:
            getattr(self, nome)()
            if nome == ATE:
                break
        out = Path(config.media_dir) / "qa_timeline.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"sections": self.sections, "checkpoints": self.checkpoints,
                                   "layout_issues": self.layout_issues, "duration": float(self.time),
                                   "plays": self.renderer.num_plays}, ensure_ascii=False, indent=2), encoding="utf-8")
