"""Dez capas do VID23 / EXERCÍCIO RESOLVIDO · EP. 07, no compositor oficial da série.

uv run --no-sync python videos/vid_0023_angulo_puxar_caixa/gerar_capas.py
Escreve só em videos/vid_0023_angulo_puxar_caixa/capas e media/vid_0023_capas.
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from manim import (
    DOWN, LEFT, RIGHT, UP, Arc, Arrow, DashedLine, Dot, Line, MathTex,
    Rectangle, Scene, VGroup, VMobject, tempconfig,
)

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
OUT = UNIT / "capas"
MEDIA = ROOT / "media" / "vid_0023_capas"
sys.path.insert(0, str(ROOT))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


g = load("capa9", ROOT / "videos/vid_0009_campo_solenoide/gerar_capa.py")
g.SERIE = "EXERCÍCIO RESOLVIDO · EP. 07"
CY, MG, VI, WH = g.CYAN, g.MAGENTA, "#9C8CFF", g.WHITE
MU, M, GRAV = 0.5, 20, 9.8
TH = math.degrees(math.atan(MU))  # 26,565°


def F(theta_deg):
    t = math.radians(theta_deg)
    return MU * M * GRAV / (math.cos(t) + MU * math.sin(t))


def tex(s, color=WH, size=85):
    return MathTex(s, color=color, font_size=size)


def label(s, color=WH, size=55):
    return g.screen_text(s, size, color=color)


def arrow(w=1.0):
    return Arrow(LEFT * w / 2, RIGHT * w / 2, buff=0, color=WH,
                 stroke_width=7, tip_length=0.22)


def seta(p0, p1, color, width=6):
    return Arrow(p0, p1, buff=0, color=color, stroke_width=width, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.5)


def caixa(w=1.5, h=1.1):
    return Rectangle(width=w, height=h, fill_color="#185286", fill_opacity=1,
                     stroke_color="#B5D8FF", stroke_width=3)


def chao(w=5.0):
    return Line(LEFT * w / 2, RIGHT * w / 2, color="#7295E6", stroke_width=4)


def puxar(theta, comprimento=2.2, rotulo=True, cor=MG):
    """Caixa sobre o chão, corda saindo do canto superior direito num ângulo theta."""
    b = caixa().move_to([0, 0.55, 0])
    floor = chao().move_to([0, 0, 0])
    start = np.array([0.75, 0.55, 0])
    end = start + comprimento * np.array([math.cos(math.radians(theta)),
                                          math.sin(math.radians(theta)), 0])
    parts = [floor, b, seta(start, end, cor, 7)]
    if rotulo and theta > 1:
        arc = Arc(radius=0.9, start_angle=0, angle=math.radians(theta), arc_center=start,
                  color=CY, stroke_width=4)
        t = tex(r"\theta", CY, 52).move_to(start + 1.3 * np.array(
            [math.cos(math.radians(theta / 2)), math.sin(math.radians(theta / 2)), 0]))
        parts += [arc, t]
    return VGroup(*parts)


def coluna(*parts, buff=0.35):
    return VGroup(*parts).arrange(DOWN, buff=buff)


def linha(*parts, buff=0.6):
    return VGroup(*parts).arrange(RIGHT, buff=buff)


def grafico(w=5.0, h=3.0, marcar=True):
    xs = np.linspace(0, 80, 120)
    ys = [F(x) for x in xs]
    lo, hi = 84, 112

    def p(x, y):
        return np.array([x / 80 * w, (y - lo) / (hi - lo) * h, 0])

    eixos = VGroup(Line(p(0, lo), p(80, lo), color=WH, stroke_width=3),
                   Line(p(0, lo), p(0, hi), color=WH, stroke_width=3))
    curva = VMobject(color=CY, stroke_width=7)
    curva.set_points_smoothly([p(x, y) for x, y in zip(xs, ys)])
    parts = [eixos, curva]
    if marcar:
        dot = Dot(p(TH, F(TH)), color=MG, radius=0.13)
        guia = DashedLine(p(TH, lo), p(TH, F(TH)), color=MG, stroke_width=3)
        parts += [guia, dot]
    grp = VGroup(*parts)
    return grp


def p1():
    return linha(puxar(TH), tex(r"\tan\theta=\mu", CY, 100))


def p2():
    a = coluna(puxar(0, rotulo=False), tex(r"98\ \mathrm{N}", VI, 75))
    b = coluna(puxar(TH), tex(r"\approx 87{,}65\ \mathrm{N}", CY, 75))
    return linha(a, arrow(0.9), b, buff=0.5)


def p3():
    return linha(tex(r"98\ \mathrm{N}", VI, 120), tex(r"\longrightarrow", WH, 100),
                 tex(r"87{,}65\ \mathrm{N}", CY, 120), buff=0.5)


def p4():
    return coluna(label("ÂNGULO IDEAL", CY, 50), tex(r"\tan\theta=\mu", WH, 160))


def p5():
    b = caixa().move_to([0, 0.55, 0])
    floor = chao().move_to([0, 0, 0])
    c = b.get_center()
    th = math.radians(TH)
    parts = [floor, b,
             seta(c + UP * 0.55, c + UP * 1.55, WH, 6),
             seta(c + DOWN * 0.55, c + DOWN * 1.45, VI, 6),
             seta(c + RIGHT * 0.75, c + RIGHT * 0.75 + 2.0 * np.array([math.cos(th), math.sin(th), 0]), MG, 7),
             seta(c + LEFT * 0.75, c + LEFT * 2.1, CY, 6)]
    diag = VGroup(*parts)
    eq = VGroup(tex(r"N=mg-F\sin\theta", CY, 80),
                tex(r"f_{s,\max}=\mu N", WH, 80)).arrange(DOWN, buff=0.35)
    return linha(diag, eq, buff=0.7)


def p6():
    g_ = grafico()
    rot = tex(r"\theta\approx 26{,}6^\circ", MG, 60).next_to(g_, DOWN, buff=0.3)
    return VGroup(g_, rot)


def p7():
    return linha(puxar(0, rotulo=False), tex(r"?", MG, 220), buff=0.9)


def p8():
    return linha(grafico(4.2, 2.8), tex(r"F(\theta)=\frac{\mu mg}{\cos\theta+\mu\sin\theta}", CY, 70),
                 buff=0.7)


def p9():
    b = caixa().move_to([0, 0.55, 0])
    floor = chao().move_to([0, 0, 0])
    start = np.array([0.75, 0.55, 0])
    th = math.radians(TH)
    fx, fy = 2.6 * math.cos(th), 2.6 * math.sin(th)
    end = start + np.array([fx, fy, 0])
    diag = VGroup(floor, b, seta(start, end, MG, 7),
                  seta(start, start + np.array([fx, 0, 0]), CY, 6),
                  seta(start, start + np.array([0, fy, 0]), VI, 6),
                  DashedLine(start + np.array([fx, 0, 0]), end, color=WH, stroke_width=2),
                  DashedLine(start + np.array([0, fy, 0]), end, color=WH, stroke_width=2))
    eq = VGroup(tex(r"F\cos\theta", CY, 80), tex(r"F\sin\theta", VI, 80)).arrange(DOWN, buff=0.4)
    return linha(diag, eq, buff=0.7)


def p10():
    return coluna(tex(r"-10{,}6\%", MG, 190), label("DE FORÇA", WH, 55), buff=0.25)


VARIANTS = [
    ("QUAL O MELHOR ÂNGULO", "PARA PUXAR UMA CAIXA?", p1),
    ("HORIZONTAL OU INCLINADO:", "QUAL GASTA MENOS?", p2),
    ("DE 98 N PARA 87,65 N?", "SÓ MUDANDO O ÂNGULO", p3),
    ("O ÂNGULO IDEAL", "TEM UMA FÓRMULA", p4),
    ("INCLINAR A CORDA", "REDUZ O ATRITO?", p5),
    ("A FORÇA CAI, MAS", "DEPOIS VOLTA A SUBIR", p6),
    ("PUXAR RENTE AO CHÃO", "É O MAIS FÁCIL?", p7),
    ("A FORÇA MÍNIMA", "TEM UM ÂNGULO", p8),
    ("DUAS FORÇAS", "EM DISPUTA", p9),
    ("DEZ POR CENTO", "MENOS FORÇA", p10),
]


def render_art(build, number):
    class Quadro(Scene):
        def construct(self):
            art = build()
            art.scale_to_fit_height(6)
            if art.width > 15:
                art.scale_to_fit_width(15)
            art.move_to([0, 0, 0])
            self.add(art)

    with tempconfig(dict(frame_width=16, frame_height=9, pixel_width=3200,
                         pixel_height=1800, transparent=True, format="png",
                         save_last_frame=True, write_to_movie=False,
                         media_dir=str(MEDIA), tex_dir=str(MEDIA / "Tex"),
                         text_dir=str(MEDIA / "texts"), verbosity="WARNING",
                         disable_caching=True, output_file=f"arte_{number:02d}")):
        scene = Quadro()
        scene.render()
        art = Image.open(scene.renderer.file_writer.image_file_path).convert("RGBA")
        return art.crop(art.getchannel("A").getbbox())


def contact(files):
    for page in range(2):
        tw, th, gap = 270, 480, 18
        sheet = Image.new("RGB", (5 * tw + 6 * gap, th + 100), "#050816")
        draw = ImageDraw.Draw(sheet)
        font = ImageFont.truetype(g.BOLD, 24)
        for slot, path in enumerate(files[page * 5:page * 5 + 5]):
            x = gap + slot * (tw + gap)
            sheet.paste(Image.open(path).resize((tw, th), Image.Resampling.LANCZOS), (x, 18))
            draw.text((x + tw / 2, 530), f"OPÇÃO {page * 5 + slot + 1:02d}",
                      fill=WH, font=font, anchor="mm")
        sheet.save(OUT / f"comparativo_{page + 1:02d}.jpg", quality=95, subsampling=0)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files, entries = [], []
    background = g.base()
    g.base = lambda: background.copy()
    for number, (first, last, build) in enumerate(VARIANTS, 1):
        size = min(g.fit(t, g.BOLD, 870, 150).size for t in (first, last))
        lines = [([(first, "white")], size), ([(last, "grad")], size)]
        image = g.cover(lines, render_art(build, number))
        assert image.size == (1080, 1920)
        path = OUT / f"capa_{number:02d}.png"
        image.save(path, optimize=True)
        files.append(path)
        entries.append(dict(opcao=number, titulo=f"{first} / {last}", arquivo=path.name,
                            resolucao=[1080, 1920], serie=g.SERIE))
        print(f"Pronta: {path}", flush=True)
    contact(files)
    (OUT / "opcoes.json").write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    print("10 capas + 2 comparativos concluídos.")


if __name__ == "__main__":
    main()
