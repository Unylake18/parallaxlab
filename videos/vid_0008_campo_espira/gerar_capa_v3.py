"""Variações da capa do vid_0008; opção 7 é o refinamento final.

Uso: uv run python videos/vid_0008_campo_espira/gerar_capa_v3.py 7
"""

from pathlib import Path
import sys

import numpy as np
from manim import Arrow, DashedLine, Dot, Line, VGroup
from PIL import Image

from gerar_capa import CYAN, BLUE, MAGENTA, VIOLET, WHITE, render_rgba
from gerar_capa_v2 import cover, formula, grafico_neon, neon
from comum import tex


UNIT = Path(__file__).resolve().parent
OUT = UNIT / "capas_v3"
HEADLINE = [([("VOCÊ DECOROU", "white")], 150),
            ([("ESSA FÓRMULA?", "grad")], 150)]
HEADLINE_DE_ONDE = [([("DE ONDE VEM?", "white")], 150),
                    ([("ESSA FÓRMULA?", "grad")], 150)]


def espira_com_eixo(loop=1.20, eixo=2.35, destaque=False, eixo_refinado=False):
    """Espira em ciano/magenta; R, z, I e P seguem as cores da cena."""
    from manim import PI

    ponto = lambda a: np.array([0.53 * loop * np.sin(a), loop * np.cos(a), 0.0])
    traseira = neon([ponto(a) for a in np.linspace(PI, 2 * PI, 90)],
                   [BLUE, VIOLET, MAGENTA], 17)
    dianteira = neon([ponto(a) for a in np.linspace(0, PI, 90)],
                    [MAGENTA, VIOLET, CYAN], 17)
    centro = np.array([0.0, 0.0, 0.0])
    p = np.array([eixo, 0.0, 0.0])
    g = VGroup(traseira, dianteira)
    g.add(
        DashedLine(centro, p + [0.35, 0, 0], dash_length=0.13)
        .set_stroke(BLUE, 8 if eixo_refinado else (7 if destaque else 5),
                    1.0 if destaque else 0.85),
        Arrow(centro, ponto(0.77), buff=0, stroke_width=6,
              tip_length=0.22, color=CYAN),
        tex("R", 55, CYAN).move_to([-0.30, 0.70, 0]),
        tex("I", 56, MAGENTA).move_to([-0.94, -0.15, 0]),
        Dot(p, 0.30, color=MAGENTA).set_opacity(0.20 if destaque else 0),
        Dot(p, 0.22 if destaque else 0.17, color=MAGENTA),
        tex("P", 60 if destaque else 52, MAGENTA).move_to(p + [0, 0.43 if destaque else 0.39, 0]),
        tex("z", 53, BLUE).move_to([eixo + 0.47, -0.35, 0]),
    )
    return g


def painel(numero):
    """Variações sutis da escala do desenho e da posição do gráfico."""
    if numero == 7:
        desenho = espira_com_eixo(1.18, 2.20, destaque=True, eixo_refinado=True)
        desenho.move_to([-3.10, 0.03, 0])
        expressao = formula(76)
        expressao.scale_to_fit_width(6.10)
        expressao.move_to([2.225, 0.15, 0])
        return VGroup(desenho, expressao)
    if numero == 6:
        desenho = espira_com_eixo(1.18, 2.20, destaque=True).move_to([-3.10, 0.03, 0])
        expressao = formula(76)
        expressao.scale_to_fit_width(6.10)
        expressao.move_to([2.225, 0.03, 0])
        return VGroup(desenho, expressao)
    if numero in (4, 5):
        desenho = espira_com_eixo(1.18, 2.20).move_to([-3.10, 0.03, 0])
        expressao = formula(76)
        expressao.scale_to_fit_width(5.55)
        expressao.move_to([2.50, 0.03, 0])
        return VGroup(desenho, expressao)
    settings = {
        1: (1.18, 2.20, 67, 1.22, 0.47, -1.30),
        2: (1.30, 2.30, 64, 1.05, 0.42, -1.37),
        3: (1.22, 2.25, 70, 0.92, 0.38, -1.42),
    }
    loop, eixo, font, gw, gh, gy = settings[numero]
    desenho = espira_com_eixo(loop, eixo).move_to([-3.10, 0.03, 0])
    expressao = formula(font)
    expressao.scale_to_fit_width(5.0)
    expressao.move_to([2.30, 0.52, 0])
    grafico = grafico_neon(w=gw, h=gh, preenche=False)
    grafico.scale_to_fit_width(1.95 if numero == 1 else 1.75)
    grafico.move_to([3.55, gy, 0])
    return VGroup(desenho, expressao, grafico)


def suavizar_magenta_direita(imagem):
    """Reduz apenas o brilho roxo escuro no interior direito do card."""
    pixels = np.asarray(imagem.convert("RGB")).copy()
    trecho = pixels[1195:1420, 520:850].astype(np.float32)
    r, g, b = trecho[:, :, 0], trecho[:, :, 1], trecho[:, :, 2]
    magenta_escuro = (r > g + 10) & (b > g + 20) & (g < 90)
    horizontal = np.sin(np.linspace(0, np.pi, trecho.shape[1], dtype=np.float32))[None, :]
    vertical = np.minimum(1, np.minimum(np.arange(trecho.shape[0]),
                                        np.arange(trecho.shape[0])[::-1]) / 18)[:, None]
    fator = 1 - (0.18 * horizontal * vertical * magenta_escuro)
    pixels[1195:1420, 520:850] = (trecho * fator[:, :, None]).astype(np.uint8)
    return Image.fromarray(pixels, "RGB")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    numeros = (int(sys.argv[1]),) if len(sys.argv) > 1 else (1, 2, 3, 4, 5, 6, 7)
    for numero in numeros:
        headline = HEADLINE_DE_ONDE if numero == 5 else HEADLINE
        imagem = cover(headline, render_rgba(lambda n=numero: painel(n), 420))
        if numero in (6, 7):
            imagem = suavizar_magenta_direita(imagem)
        caminho = OUT / ("capa_refinada_final.png" if numero == 7
                         else f"capa_opcao_{numero}.png")
        imagem.save(caminho, optimize=True)
        print(caminho)
        if numero == 7:
            oficial = UNIT / "capa_instagram.png"
            imagem.save(oficial, optimize=True)
            print(oficial)


if __name__ == "__main__":
    main()
