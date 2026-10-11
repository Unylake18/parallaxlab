"""Dez capas de VID20 / EP.07, preservando o compositor oficial da série.

uv run --no-sync python videos/vid_0020_integral_dupla_volume/gerar_capas.py
Somente arquivos desta unidade e media/vid_0020_capas são escritos.
"""
import importlib.util
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from manim import (
    DOWN, LEFT, RIGHT, UP, Arrow, DoubleArrow, Line, MathTex,
    Scene, VGroup, tempconfig,
)

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
OUT = UNIT / "capas"
MEDIA = ROOT / "media" / "vid_0020_capas"
sys.path.insert(0, str(ROOT))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


g = load("capa9", ROOT / "videos/vid_0009_campo_solenoide/gerar_capa.py")
c = load("integral20", UNIT / "cena.py")
g.SERIE = "POR TRÁS DA FÓRMULA · EP. 07"
CY, MG, VI, WH = g.CYAN, g.MAGENTA, "#9C8CFF", g.WHITE


def tex(s, color=WH, size=85):
    return MathTex(s, color=color, font_size=size)


def field(n=4):
    group = c.make_column_field(n)
    for col in group:
        for face, color in zip(col, ("#185286", "#413B8C", "#7295E6")):
            face.set_fill(color, 1).set_stroke("#B5D8FF", 0.65)
    return group


def solid():
    shell = c.make_volume_shell().set_fill(VI, 0.30)
    wire = c.make_surface_wireframe().set_stroke(CY, 2.4, 1)
    return VGroup(c.make_base_grid(4), shell, wire)


def arrow():
    return Arrow(LEFT * 0.5, RIGHT * 0.5, buff=0, color=WH,
                 stroke_width=7, tip_length=0.22)


def row(*parts):
    for part in parts:
        part.scale_to_fit_height(3.7 if not isinstance(part, Arrow) else 0.32)
    return VGroup(*parts).arrange(RIGHT, buff=0.55)


def selected_column():
    cell = next(p for p in c.partition(4) if (p['i'], p['j']) == c.SELECTED)
    col = c.make_column(cell, selected=True)
    col.set_z_index(10)
    base = c.cell_polygon(cell, fill_color=CY, fill_opacity=0.65,
                          stroke_color=CY, stroke_width=3).set_z_index(12)
    p = c.project_xyz
    x, y, d, h = cell['x0'], cell['y0'], cell['d'], cell['h']
    foot, top = p(x + d, y, 0), p(x + d, y, h)
    measure = DoubleArrow(foot + RIGHT * 0.5, top + RIGHT * 0.5,
                          buff=0, color=MG, stroke_width=4, tip_length=0.16)
    label = tex(r"f(x_i,y_j)", MG, 40).next_to(measure, RIGHT, buff=0.14)
    da = tex(r"\Delta A", CY, 42).next_to(base, DOWN, buff=0.15)
    dv = tex(r"\Delta V", VI, 42).next_to(col, LEFT, buff=0.15)
    return VGroup(c.make_base_grid(4).set_opacity(0.50), col, base, measure, label, da, dv)


def panel_1():
    equation = VGroup(tex(r"\iint_R f(x,y)\,dA", CY, 105),
                      tex(r"=\ V", VI, 105)).arrange(DOWN, buff=0.3)
    return row(solid(), equation)


def panel_2():
    formula = VGroup(tex(r"\Delta V\approx", VI, 95),
                     tex(r"f(x_i,y_j)\,\Delta A", WH, 95)).arrange(DOWN, buff=0.3)
    return row(selected_column(), formula)


def panel_3():
    return row(field(4), arrow(), solid())


def panel_4():
    labels = VGroup(g.screen_text("ÁREA", 60, color=CY), tex(r"\times", WH, 95),
                    g.screen_text("ALTURA", 60, color=MG), tex(r"=\ \Delta V", VI, 95))
    labels.arrange(DOWN, buff=0.12)
    return row(selected_column(), labels)


def panel_5():
    equation = VGroup(tex(r"\sum f(x_i,y_j)\,\Delta A", VI, 92),
                      tex(r"\longrightarrow", WH, 70),
                      tex(r"\iint_R f(x,y)\,dA", CY, 92)).arrange(DOWN, buff=0.15)
    return row(field(6), equation)


def panel_6():
    equation = VGroup(tex(r"z=4-x^2-y^2", CY, 95),
                      tex(r"R=[-1,1]^2", VI, 70)).arrange(DOWN, buff=0.7)
    return row(solid(), equation)


def panel_7():
    geom = VGroup(solid().set_opacity(0.50), c.make_section(0).set_z_index(50))
    equation = VGroup(g.screen_text("ÁREA DA SEÇÃO", 45, color=CY),
                      tex(r"\int\!\bigl(\int f\,dy\bigr)\,dx", WH, 90),
                      g.screen_text("VOLUME TOTAL", 45, color=VI)).arrange(DOWN, buff=0.4)
    return row(geom, equation)


def panel_8():
    return row(tex(r"\iint_R", CY, 170), arrow(), solid())


def panel_9():
    def tagged(n):
        geom = field(n).scale_to_fit_height(3.4)
        return VGroup(geom, tex(fr"{n}\times{n}", CY if n == 4 else VI, 55)
                      .next_to(geom, DOWN, buff=0.2))
    return row(tagged(4), arrow(), tagged(16))


def panel_10():
    base = c.make_base_grid(4).set_stroke(CY, 3)
    # Mesma escala espacial entre base e colunas; sem inventar outra superfície.
    base.scale_to_fit_width(3.5)
    cols = field(4).scale_to_fit_width(3.5)
    surf = solid().scale_to_fit_width(3.5)
    return VGroup(base, arrow(), cols, arrow(), surf).arrange(RIGHT, buff=0.32, aligned_edge=DOWN)


VARIANTS = [
    ("POR QUE A INTEGRAL", "CALCULA VOLUME?", panel_1),
    ("O QUE ESSA FÓRMULA", "ESTÁ SOMANDO?", panel_2),
    ("DE PEQUENAS COLUNAS", "A UM VOLUME", panel_3),
    ("ÁREA VEZES ALTURA", "EM CADA PONTO", panel_4),
    ("UMA SOMA INFINITA", "RECONSTRÓI O SÓLIDO", panel_5),
    ("INTEGRAL DUPLA", "VOLUME SOB A SUPERFÍCIE", panel_6),
    ("DUAS INTEGRAIS", "UM SÓ VOLUME", panel_7),
    ("DE ONDE VEM", "A INTEGRAL DUPLA?", panel_8),
    ("COLUNAS MENORES", "UMA SOMA MELHOR", panel_9),
    ("DO QUADRADO", "AO VOLUME", panel_10),
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
    # A base da série é idêntica nas dez opções. Cache local, sem alterar o helper compartilhado.
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
                            resolucao=[1080,1920], fonte="Space Grotesk Bold / Medium",
                            serie=g.SERIE))
        print(f"Pronta: {path}", flush=True)
    contact(files)
    (OUT / "opcoes.json").write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    with zipfile.ZipFile(UNIT / "capas_vid20_ep07.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for path in files + sorted(OUT.glob("comparativo_*.jpg")) + [OUT / "opcoes.json"]:
            z.write(path, path.name)
    print("10 capas + 2 comparativos + ZIP concluídos.")


if __name__ == "__main__":
    main()
