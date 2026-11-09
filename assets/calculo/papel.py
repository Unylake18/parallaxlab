"""Fundo de papel milimetrado da série de longos de Cálculo I–IV (padrão aprovado pelo Kaio em 2026-11-09).

- O fundo entra como imagem da câmera (`usar_papel(cena)`), nunca como ImageMobject e sem nada se mexendo no fundo.
- Grade grossa a cada 1 u do Manim (120 px em 1080p) e fina a cada 0,2 u, com um cruzamento grosso na origem do quadro.
- `eixos_no_papel(...)`: a origem do gráfico cai num cruzamento grosso e a unidade é múltipla de 0,2 u, então as marcas do eixo
  ficam em cima das linhas do papel (conferido no pixel).
- `janela(cena, ax)`: exceção para gráfico que não encaixa (unidade quebrada, perspectiva). Apaga a grade atrás dos eixos com
  bordas suaves; gera um PNG por cena, uma vez só.
"""
from pathlib import Path
import numpy as np
from manim import Axes, config
from PIL import Image, ImageDraw, ImageFilter

AQUI = Path(__file__).parent


def _arq(nome):
    w, h = config.pixel_width, config.pixel_height
    p = AQUI / f"{nome}_{w}x{h}.png"
    if not p.exists():                                  # outra resolução: reamostra a de 1080p
        p2 = AQUI / f"{nome}_{w}x{h}_gerado.png"
        if not p2.exists():
            Image.open(AQUI / f"{nome}_1920x1080.png").resize((w, h), Image.LANCZOS).save(p2)
        p = p2
    return p


def usar_papel(cena, arquivo=None):
    cena.camera.background_image = str(arquivo or _arq("fundo_calculo_milimetrado"))
    cena.camera.init_background()


def eixos_no_papel(origem, x_range, y_range, unidade=1.0, unidade_y=None, **kw):
    o = np.round(np.array([*origem, 0][:3], float))
    ux = max(0.2, round(unidade / 0.2) * 0.2)
    uy = max(0.2, round((unidade_y or unidade) / 0.2) * 0.2)
    ax = Axes(x_range=x_range, y_range=y_range, x_length=(x_range[1] - x_range[0]) * ux,
              y_length=(y_range[1] - y_range[0]) * uy, tips=False, **kw)
    ax.shift(o - ax.c2p(0, 0))
    return ax


def janela(cena, ax, folga=0.35, op=0.9, nome=None):
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
