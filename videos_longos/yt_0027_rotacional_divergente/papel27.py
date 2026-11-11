"""yt_0027: papel v2 da série de Cálculo (Kaio, 2026-11-11) PORTADO PARA A UNIDADE, sem tocar em assets/calculo/papel.py (outra sessão cuida do global
e do yt_0026). Código de `papel()` idêntico ao do prompt "fundo violeta"; o PNG do fundo é gravado em renders/fundo/ da unidade.

- Fundo da câmera: degradê violeta liso #18143A → #0F0C26 (`usar_violeta(cena)`), parado, sem grade na imagem.
- Grade: `papel(ax)` desenha quadradinhos iguais (sem linha grossa, #2B2558, traço 1,2) com a MESMA origem e unidade dos eixos.
  Passo 0,25 da unidade; se o quadradinho ficar < 20 px em 1080p, 0,5 (e depois 1). `area=(x0, x1, y0, y1)` limita a um painel.
- Sem gráfico: `papel()` = 1 u do Manim, origem no centro do quadro.
- A grade é um VGroup parado (z_index −10): entra/sai com FadeIn/FadeOut; nunca com updater.
- `placas27()`: placa lisa (o próprio degradê, borda esfumada) atrás do canto e do logo, para a grade não passar sob o texto
  (é o papel da placa lisa que o fundo27 milimetrado tinha embutida)."""
from pathlib import Path

import numpy as np
from manim import ORIGIN, RIGHT, UP, ImageMobject, Line, VGroup, config
from PIL import Image, ImageFilter

AQUI = Path(__file__).resolve().parent / "renders" / "fundo"
COR_GRADE, LARG_GRADE = "#2B2558", 1.2
TOPO, BASE = "#18143A", "#0F0C26"
MIN_PX = 20
PLACA_CANTO = (22, 124, 0, 700)        # y0, y1, x0, x1 (px a 1080p), como no fundo27
PLACA_LOGO = (34, 96, 1656, 1920)


def _degrade(w, h):
    hx = lambda c: np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)
    v = np.linspace(0, 1, h)[:, None, None] * np.ones((1, w, 1))
    return hx(TOPO) * (1 - v) + hx(BASE) * v


def arq_violeta():
    w, h = config.pixel_width, config.pixel_height
    p = AQUI / f"fundo_calculo_violeta_liso_{w}x{h}.png"
    if not p.exists():
        AQUI.mkdir(parents=True, exist_ok=True)
        Image.fromarray(_degrade(w, h).astype(np.uint8)).save(p)
    return p


def usar_violeta(cena):
    cena.camera.background_image = str(arq_violeta())
    cena.camera.init_background()


def placas27():
    """ImageMobject do quadro inteiro: o degradê com alfa só nas placas do canto e do logo (borda esfumada 16 px a 1080p)."""
    w, h = config.pixel_width, config.pixel_height
    p = AQUI / f"placas27_violeta_{w}x{h}.png"
    if not p.exists():
        AQUI.mkdir(parents=True, exist_ok=True)
        s = w / 1920
        m = Image.new("L", (w, h), 0)
        a = np.zeros((h, w), np.uint8)
        for y0, y1, x0, x1 in (PLACA_CANTO, PLACA_LOGO):
            a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)] = 255
        m = np.asarray(Image.fromarray(a).filter(ImageFilter.GaussianBlur(16 * s)), np.uint8)
        rgba = np.concatenate([_degrade(w, h).astype(np.uint8), m[..., None]], 2)
        Image.fromarray(rgba, "RGBA").save(p)
    im = ImageMobject(str(p)).set_width(config.frame_width).move_to(ORIGIN).set_z_index(-5)
    return im


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
    for m in g.get_family():
        m._sem_contorno = True                              # yt_0027: o _estilo do kit não põe contorno escuro na grade
    return g


def area_px(v, x0, y0, w, h):
    """area (unidades de `v`) de um painel dado em px de 1080p (x0, y0, largura, altura)."""
    return ((x0 - v.cx) / v.u, (x0 + w - v.cx) / v.u, (v.cy - (y0 + h)) / v.u, (v.cy - y0) / v.u)
