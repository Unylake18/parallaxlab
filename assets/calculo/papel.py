"""Papel da série de longos de Cálculo I–IV, v2 (Kaio, 2026-11-11): fundo violeta liso + grade de quadradinhos que NASCE DOS EIXOS.

- Fundo da câmera: degradê violeta liso (`usar_papel(cena)`), parado, sem grade na imagem.
- Grade: `papel(ax)` desenha quadradinhos iguais (sem linha grossa) com a MESMA origem e unidade dos eixos -> alinha por construção.
  Passo padrão 0,25 da unidade do gráfico; se o quadradinho ficar < 20 px em 1080p, passa sozinho para 0,5 (e depois 1).
  `passo=` força outro valor quando o vídeo pedir. `area=(x0, x1, y0, y1)` (unidades do gráfico) limita a grade a um painel.
- Sem gráfico na cena: `papel()` usa a unidade padrão (1 u do Manim, origem no centro do quadro).
- A grade é um VGroup parado (z_index -10): entra/sai com FadeIn/FadeOut; nunca com updater.
- Compatibilidade v1: `_arq("fundo_calculo_milimetrado")`/`_arq("fundo_calculo_liso")` e `janela(...)` continuam funcionando com os PNGs antigos
  (unidades de Cálculo ainda não migradas importam `janela`).
"""
import os
from pathlib import Path
import numpy as np
from manim import Axes, Line, VGroup, config, ORIGIN, RIGHT, UP
from PIL import Image

AQUI = Path(__file__).parent
COR_GRADE, LARG_GRADE = "#2B2558", 1.2
TOPO, BASE = "#18143A", "#0F0C26"
MIN_PX = 20
VIOLETA = "fundo_calculo_violeta_liso"


def _arq(nome=VIOLETA):
    w, h = config.pixel_width, config.pixel_height
    p = AQUI / f"{nome}_{w}x{h}.png"
    if p.exists():
        return p
    if nome != VIOLETA:                                 # PNG antigo (v1) em outra resolução: reamostra o de 1080p
        p2 = AQUI / f"{nome}_{w}x{h}_gerado.png"
        if not p2.exists():
            Image.open(AQUI / f"{nome}_1920x1080.png").resize((w, h), Image.LANCZOS).save(p2)
        return p2
    hx = lambda c: np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)
    v = np.linspace(0, 1, h)[:, None, None] * np.ones((1, w, 1))
    tmp = p.with_name(f"{p.stem}.{os.getpid()}.tmp.png")      # escrita atômica: renders em paralelo não leem o PNG pela metade
    Image.fromarray((hx(TOPO) * (1 - v) + hx(BASE) * v).astype(np.uint8)).save(tmp)
    os.replace(tmp, p)
    return p


def usar_papel(cena, arquivo=None):
    cena.camera.background_image = str(arquivo or _arq())
    cena.camera.init_background()


class _Padrao:
    """Eixos 'virtuais' da unidade padrão: 1 u do Manim, origem no centro do quadro."""
    def c2p(self, x, y):
        return ORIGIN + RIGHT * x + UP * y


def papel(ax=None, area=None, passo=None, cor=COR_GRADE, largura=LARG_GRADE):
    ax = ax or _Padrao()
    o = np.array(ax.c2p(0, 0)); ux = ax.c2p(1, 0)[0] - o[0]; uy = ax.c2p(0, 1)[1] - o[1]
    px_u = config.pixel_width / config.frame_width          # px por unidade do Manim
    if passo is None:
        passo = 0.25
        while min(abs(ux), abs(uy)) * passo * px_u * 1920 / config.pixel_width < MIN_PX and passo < 1:
            passo *= 2                                      # 0,25 -> 0,5 -> 1
    if area is None:
        fw, fh = config.frame_width / 2, config.frame_height / 2
        area = ((-fw - o[0]) / ux, (fw - o[0]) / ux, (-fh - o[1]) / uy, (fh - o[1]) / uy)
    x0, x1, y0, y1 = area
    ks = lambda a, b: np.arange(np.ceil(min(a, b) / passo - 1e-9), np.floor(max(a, b) / passo + 1e-9) + 1) * passo
    g = VGroup(*[Line(ax.c2p(x, y0), ax.c2p(x, y1)) for x in ks(x0, x1)],
               *[Line(ax.c2p(x0, y), ax.c2p(x1, y)) for y in ks(y0, y1)])
    g.set_stroke(cor, largura).set_z_index(-10)
    g.passo = passo
    return g


def eixos_no_papel(origem, x_range, y_range, unidade=1.0, unidade_y=None, **kw):
    """Mantido por compatibilidade (v1). Com a grade nascendo dos eixos, não é mais preciso encaixar; só cria e posiciona os eixos."""
    ux, uy = unidade, unidade_y or unidade
    ax = Axes(x_range=x_range, y_range=y_range, x_length=(x_range[1] - x_range[0]) * ux,
              y_length=(y_range[1] - y_range[0]) * uy, tips=False, **kw)
    ax.shift(np.array([*origem, 0][:3], float) - ax.c2p(0, 0))
    return ax


def janela(cena, ax, folga=0.35, op=0.9, nome=None):
    """OBSOLETA (v1), mantida só para não quebrar unidades ainda não migradas: apaga a grade do milimetrado antigo atrás dos eixos.
    No papel v2 não é necessária (a grade nasce dos eixos)."""
    from PIL import ImageDraw, ImageFilter
    w, h = config.pixel_width, config.pixel_height
    k = w / config.frame_width
    x0, y0 = ax.c2p(ax.x_range[0], ax.y_range[0])[:2]
    x1, y1 = ax.c2p(ax.x_range[1], ax.y_range[1])[:2]
    caixa = [(x0 - folga + config.frame_width / 2) * k, (config.frame_height / 2 - y1 - folga) * k,
             (x1 + folga + config.frame_width / 2) * k, (config.frame_height / 2 - y0 + folga) * k]
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle(caixa, radius=40 * k / 120, fill=255)
    m = np.array(m.filter(ImageFilter.GaussianBlur(28 * k / 120)), float)[..., None] / 255 * op
    a = np.array(Image.open(_arq("fundo_calculo_milimetrado")).convert("RGB"), float)
    b = np.array(Image.open(_arq("fundo_calculo_liso")).convert("RGB"), float)
    saida = AQUI / f"janela_{nome or type(cena).__name__}_{w}x{h}.png"
    Image.fromarray((a * (1 - m) + b * m).astype(np.uint8)).save(saida)
    usar_papel(cena, saida)
    return saida
