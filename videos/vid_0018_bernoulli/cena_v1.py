"""Primeiro preview silencioso — POR TRÁS DA FÓRMULA · EP. 06.

Da raiz, preparar o cache local antes do render (30 quadros / loop de 2 s):
uv run python -c "import sys; from pathlib import Path; sys.path.insert(0, 'experimentos/blender/arsenal'); import ponte; ponte.CACHE=Path('videos/vid_0018_bernoulli/cache3d').resolve(); ponte.main()" tubo_escoamento --res 540x960 --frames 30
uv run python -m manim -r 540,960 --fps 15 --media_dir videos/vid_0018_bernoulli/media_preview -o preview_silencioso videos/vid_0018_bernoulli/cena.py Bernoulli

MF-Tools considerado: matching de termos e trajetórias manuais bastam aqui.
Não há glyph maps dependentes de índices. O cache 3D fica dentro da unidade.
"""
import json
from contextlib import contextmanager
from pathlib import Path
import sys

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parents[2]
UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from template.config import BACKGROUND_COLOR, TEXT_COLOR, PRIMARY_COLOR, WATERMARK_PATH
from template.fonts import screen_text

sys.path.insert(0, str(ROOT / "experimentos/blender/arsenal"))
from manim_solido3d import Solido3D
import ponte
ponte.CACHE = UNIT / "cache3d"

INK, CYAN, PURPLE = TEXT_COLOR, PRIMARY_COLOR, "#AB99FF"
GOLD, RED, MUTED = "#FFD479", "#FF839E", "#ABB8D0"


@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width = config.pixel_height = 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def text(s, size=28, color=INK, width=7.6):
    with wide_pango():
        lines = [screen_text(line, size, color=color) for line in s.split("\n")]
    m = VGroup(*lines).arrange(DOWN, buff=0.16)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m


def equation(*s, y=-0.8, size=47, color=INK, width=7.6, **kwargs):
    m = MathTex(*s, font_size=size, color=color, **kwargs)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m.move_to([0, y, 0])


class Bernoulli(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.marks = {}
        self.layout_checks = []
        self.fixed = []
        tag = text("POR TRÁS DA FÓRMULA · EP. 06", 21, CYAN).move_to([0, 6.85, 0])
        rule = Line([-3.8, 6.48, 0], [3.8, 6.48, 0], stroke_width=1.2, color=CYAN)
        brand = ImageMobject(str(WATERMARK_PATH)).set_width(1.65).move_to([0, -6.9, 0])
        self.fixed = [tag, rule, brand]
        self.add(*self.fixed)

        # 0–14 s: pergunta; a fórmula completa só aparece após a derivação.
        self.title("De onde vem Bernoulli?")
        q = text("Como a pressão vira\nmovimento e altura?", 39).move_to([0, 3.5, 0])
        mystery = equation(r"\boxed{\;?\;+\;?\;+\;?\;=\;\text{constante}\;}", y=1.1)
        core = text("A pista está no trabalho\ndas forças de pressão.", 31, CYAN).move_to([0, -2.0, 0])
        self.play(FadeIn(q, shift=UP * .2), Write(mystery), run_time=1.4)
        self.play(FadeIn(core), run_time=.7)
        self.note("Vamos acompanhar um pequeno volume de fluido.")
        self.until(14)

        # 14–24 s: teste 3D horizontal, seguido do modelo 2D geral.
        self.clear_stage("Um mesmo volume")
        solid = Solido3D("tubo_escoamento", frames=30, render="nunca")
        tube3d = solid.mobject(cena=self, largura=7.0, centro=UP * 2.3, periodo=2)
        self.play(FadeIn(tube3d), run_time=.7)
        flow = Arrow([-2.9, .25, 0], [2.9, .25, 0], color=CYAN, buff=0, stroke_width=4)
        self.play(GrowArrow(flow), run_time=.6)
        self.note("Uma linha de corrente.\nOs pontos são marcadores do movimento.")
        self.hold_to(18.4, "tubo_3d")
        tube3d.pausar()
        self.play(FadeOut(tube3d), FadeOut(flow), run_time=.5)
        diagram = self.pipe()
        self.play(FadeIn(diagram), run_time=.7)
        dv = equation(r"\Delta V=A_1\Delta x_1=A_2\Delta x_2", y=-1.5, size=43, color=GOLD)
        self.play(Write(dv), run_time=.7)
        self.note("Incompressível: o volume que entra\ncorresponde ao volume que sai.")
        self.hold_to(24, "duas_secoes")

        # 24–35 s: pressão → força, sem ainda exibir P ΔV.
        self.clear_stage("Pressão produz força")
        inlet = self.face(1)
        self.play(FadeIn(inlet), run_time=.6)
        definition = equation(r"P", "=", r"\frac{F}{A}", y=-.6, size=65)
        self.play(Write(definition), run_time=.8)
        self.note("A pressão atua sobre a área da seção.")
        self.until(28)
        force = equation(r"F_1", "=", r"P_1", r"A_1", y=-.6, size=65, color=CYAN)
        self.play(TransformMatchingTex(definition, force), run_time=1.2)
        self.note("Na entrada, a força aponta\nno sentido do avanço.")
        self.hold_to(35, "forca_PA")

        # 35–50 s: a face varre área × deslocamento; daí nasce ΔV.
        self.clear_stage("Entrada: trabalho positivo")
        geom, moving, swept, dx = self.swept_volume(1)
        self.add(geom)
        w = equation(r"W_1", "=", r"F_1", r"\Delta x_1", y=-.6, size=55)
        self.play(Write(w), run_time=.8)
        self.play(moving.animate.shift(RIGHT * 1.15), GrowFromEdge(swept, LEFT), Create(dx), run_time=1.8)
        self.note("Força e deslocamento no mesmo sentido: +")
        w = self.replace(w, equation(r"W_1", "=", r"P_1", r"A_1\Delta x_1", y=-.6, size=53))
        self.until(40.5)
        volume = equation(r"\underbrace{A_1\Delta x_1}_{\text{área}\,\times\,\text{avanço}}", "=", r"\Delta V", y=-2.3, size=44, color=GOLD)
        self.play(Write(volume), Indicate(swept, color=GOLD), run_time=1.2)
        self.note("A face varreu um volume: área × deslocamento.")
        self.hold_to(45, "area_deslocamento_volume")
        result = equation(r"W_1", "=", r"P_1", r"\Delta V", y=-.6, size=62, color=CYAN)
        w = self.replace(w, result)
        self.play(Circumscribe(w, color=CYAN), run_time=.8)
        self.hold_to(50, "trabalho_entrada")

        # 50–65 s: a força da pressão externa resiste ao avanço.
        self.clear_stage("Saída: trabalho negativo")
        geom, moving, swept, dx = self.swept_volume(2)
        self.add(geom)
        f = equation(r"F_2=P_2A_2", y=-.4, size=49, color=PURPLE)
        self.play(Write(f), run_time=.7)
        self.play(moving.animate.shift(RIGHT * 1.65), GrowFromEdge(swept, LEFT), Create(dx), run_time=1.8)
        self.note("O fluido avança; a pressão externa resiste.")
        w = equation(r"W_2", "=", "-", r"F_2", r"\Delta x_2", y=-1.7, size=50)
        w[2].set_color(RED)
        self.play(Write(w), run_time=.8)
        self.until(56)
        w = self.replace(w, equation(r"W_2", "=", "-", r"P_2", r"A_2\Delta x_2", y=-1.7, size=48))
        same = equation(r"A_2\Delta x_2=\Delta V", y=-3.2, size=42, color=GOLD)
        self.play(Write(same), run_time=.7)
        self.note("Mesmo volume transferido.\nForça contra o deslocamento: −")
        self.until(60)
        w = self.replace(w, equation(r"W_2", "=", "-", r"P_2", r"\Delta V", y=-1.7, size=59, color=PURPLE))
        w[2].set_color(RED)
        self.play(Circumscribe(w, color=PURPLE), run_time=.8)
        self.hold_to(65, "trabalho_saida")

        # 65–73 s: soma física dos trabalhos, fatoração e mesmo ΔV.
        self.clear_stage("O trabalho líquido")
        plus = equation(r"W_1=+P_1\Delta V", y=3.1, color=CYAN)
        minus = equation(r"W_2=-P_2\Delta V", y=1.7, color=PURPLE)
        self.play(FadeIn(plus), FadeIn(minus), run_time=.7)
        w = equation(r"W_P", "=", r"W_1", "+", r"W_2", y=-.2, size=55)
        self.play(Write(w), run_time=.7)
        w = self.replace(w, equation(r"W_P", "=", r"P_1\Delta V", "-", r"P_2\Delta V", y=-.2, size=49))
        w = self.replace(w, equation(r"W_P", "=", r"(P_1-P_2)\Delta V", y=-.2, size=52))
        conservation = equation(r"\Delta V=A_1\Delta x_1=A_2\Delta x_2", y=-2.2, size=40, color=GOLD)
        self.play(Write(conservation), run_time=.7)
        self.note("Entrada ajuda. Saída resiste.\nO volume é conservado.")
        self.hold_to(73, "trabalho_liquido")

        # 73–81 s: núcleo trabalho–energia e massa.
        self.clear_stage("Para onde vai esse trabalho?")
        energy = equation(r"W_P", "=", r"\Delta K", "+", r"\Delta U_g", y=2.6, size=54)
        energy[2].set_color(CYAN)
        energy[4].set_color(GOLD)
        self.play(Write(energy), run_time=.8)
        self.play(FadeIn(text("Alterar a velocidade e a altura.", 28).move_to([0, 1.25, 0])), run_time=.5)
        mass = equation(r"\rho", "=", r"\frac{m}{V}", y=-.5, size=54)
        self.play(Write(mass), run_time=.6)
        mass = self.replace(mass, equation(r"m", "=", r"\rho", r"\Delta V", y=-.5, size=65, color=GOLD))
        self.note("Densidade constante: o mesmo ΔV\ntransporta a mesma massa.")
        self.hold_to(81, "massa")

        # 81–90 s: construir K2 − K1, com a massa do volume.
        self.clear_stage("Mudar a velocidade")
        known = equation(r"K=\frac12mv^2", y=3.4, size=55, color=CYAN)
        states = VGroup(equation(r"K_1=\frac12mv_1^2", size=41), equation(r"K_2=\frac12mv_2^2", size=41)).arrange(RIGHT, buff=.6).move_to([0, 1.8, 0])
        self.play(Write(known), FadeIn(states), run_time=.7)
        k = equation(r"\Delta K", "=", r"K_2", "-", r"K_1", y=-.15, size=50)
        self.play(Write(k), run_time=.6)
        k = self.replace(k, equation(r"\Delta K", "=", r"\frac12m(v_2^2-v_1^2)", y=-.15, size=49))
        mass = equation(r"m=\rho\Delta V", y=-1.6, size=41, color=GOLD)
        self.play(FadeIn(mass), run_time=.5)
        k = self.replace(k, equation(r"\Delta K", "=", r"\frac12\rho\Delta V(v_2^2-v_1^2)", y=-.15, size=46, color=CYAN))
        self.note("Variação = estado final − estado inicial.")
        self.hold_to(90, "energia_cinetica")

        # 90–99 s: h2 − h1 ligado à geometria 2D elevada.
        self.clear_stage("Mudar a altura")
        self.add(self.pipe(details=False))
        u = equation(r"U_g=mgh", y=-.5, size=55, color=GOLD)
        self.play(Write(u), run_time=.7)
        u = self.replace(u, equation(r"\Delta U_g", "=", r"mg(h_2-h_1)", y=-.5, size=49))
        self.play(FadeIn(equation(r"m=\rho\Delta V", y=-2.0, size=41, color=GOLD)), run_time=.5)
        u = self.replace(u, equation(r"\Delta U_g", "=", r"\rho g\Delta V(h_2-h_1)", y=-.5, size=47, color=GOLD))
        self.note("Subir aumenta a energia potencial gravitacional.")
        self.hold_to(99, "energia_gravitacional")

        # 99–111 s: estado de máxima densidade algébrica, sem fórmulas antigas.
        self.clear_stage("Um único balanço de energia")
        balance = equation(r"W_P=\Delta K+\Delta U_g", y=3.1, size=53)
        self.play(Write(balance), run_time=.7)
        full = self.full_balance(volume=True)
        self.play(FadeOut(balance), Write(full), run_time=1.5)
        self.note("Trabalho líquido das pressões\n= variação cinética + variação gravitacional.")
        self.hold_to(111, "balanco_completo")

        # 111–120 s: cada ΔV explicitamente marcado e dividido.
        self.title("Dividir pelo mesmo volume")
        volumes = VGroup(*(p for row in full for p in row if p.tex_string == r"\Delta V"))
        assert len(volumes) == 3, "O balanço deve mostrar três fatores ΔV."
        boxes = VGroup(*(SurroundingRectangle(p, color=GOLD, buff=.1, stroke_width=2) for p in volumes))
        self.play(Create(boxes), run_time=.8)
        division = equation(r"\div\,\Delta V\qquad(\Delta V>0)", y=-2.5, size=40, color=GOLD)
        self.play(Write(division), run_time=.7)
        slashes = VGroup(*(Line(p.get_corner(DL), p.get_corner(UR), color=RED, stroke_width=3) for p in boxes))
        self.play(Create(slashes), run_time=.7)
        self.mark("cancelamento_volume")
        self.until(115)
        reduced = self.full_balance(volume=False)
        self.play(FadeOut(boxes), FadeOut(slashes), FadeOut(division), TransformMatchingTex(full, reduced), run_time=1.3)
        self.note("O resultado não depende do tamanho\ndo pequeno volume escolhido.")
        self.hold_to(120, "balanco_por_volume")

        # 120–127 s: abrir diferenças, mantendo os sinais rastreáveis.
        self.clear_stage("Abrir as diferenças")
        pressure = equation(r"P_1", "-", r"P_2", "=", y=3.2, size=58)
        kinetic = equation(r"\frac12\rho v_2^2", "-", r"\frac12\rho v_1^2", y=1.5, size=52, color=CYAN)
        grav = equation("+", r"\rho gh_2", "-", r"\rho gh_1", y=-.1, size=52, color=GOLD)
        expanded = VGroup(pressure, kinetic, grav)
        self.play(Write(pressure), run_time=.7)
        self.play(Write(kinetic), run_time=.8)
        self.play(Write(grav), run_time=.8)
        self.note("Estado 2 menos estado 1,\nem cada variação de energia.")
        self.hold_to(127, "diferencas_abertas")

        # 127–135 s: transporte manual de termos completos; os sinais mudam.
        self.title("Reunir cada estado")
        targets = [
            equation(r"P_1", "+", r"\frac12\rho v_1^2", "+", r"\rho gh_1", y=2.8, size=54, color=CYAN),
            equation("=", y=1.3, size=58),
            equation(r"P_2", "+", r"\frac12\rho v_2^2", "+", r"\rho gh_2", y=-.2, size=54, color=PURPLE),
        ]
        captions = VGroup(text("ESTADO 1", 22, CYAN).move_to([0, 4, 0]), text("ESTADO 2", 22, PURPLE).move_to([0, -1.35, 0]))
        # Só um termo em trânsito por vez. A igualdade permanece como referência.
        # O sinal é parte do objeto que atravessa; − transforma-se em + na chegada.
        neg_k = VGroup(kinetic[1].copy(), kinetic[2].copy()).move_to([0, .3, 0])
        neg_u = VGroup(grav[2].copy(), grav[3].copy()).move_to([0, .3, 0])
        neg_p = VGroup(pressure[1].copy(), pressure[2].copy()).move_to([0, 2.05, 0])
        self.play(FadeOut(expanded), FadeIn(targets[1]), FadeIn(captions), run_time=.4)
        self.play(FadeIn(targets[0][0]), FadeIn(VGroup(*targets[2][2:])), run_time=.3)
        self.note("Ao atravessar a igualdade, o sinal muda.")
        for moving, dest in [
            (neg_k, VGroup(targets[0][1], targets[0][2])),
            (neg_u, VGroup(targets[0][3], targets[0][4])),
        ]:
            self.play(FadeIn(moving), run_time=.2)
            self.play(Transform(moving, dest, path_arc=PI / 5), run_time=1.0)
        positive = equation("+", size=54, color=PURPLE).next_to(targets[2][0], LEFT, buff=.12)
        self.play(FadeIn(neg_p), run_time=.2)
        self.play(Transform(neg_p, VGroup(positive, targets[2][0]), path_arc=-PI / 5), run_time=1.0)
        self.play(FadeOut(neg_p[0]), FadeIn(targets[2][1]), run_time=.3)
        self.hold_to(135, "reorganizacao")

        # 135–142 s: só agora generalizar à linha de corrente.
        self.clear_stage("A mesma combinação")
        self.play(FadeIn(text("Em quaisquer dois pontos\nda mesma linha de corrente…", 31).move_to([0, 3.5, 0])), run_time=.6)
        final = self.bernoulli(y=.6)
        self.play(Write(final), run_time=1.2)
        self.play(Circumscribe(final, color=CYAN), run_time=.9)
        self.note("…essa combinação tem o mesmo valor.")
        self.hold_to(142, "bernoulli")

        # 142–155 s: mesma unidade; não afirmar que pressão é energia.
        self.clear_stage("Um orçamento por volume")
        items = [
            (r"P", "Trabalho das forças de pressão\npor unidade de volume", CYAN),
            (r"\frac12\rho v^2", "Energia cinética\npor unidade de volume", PURPLE),
            (r"\rho gh", "Energia potencial gravitacional\npor unidade de volume", GOLD),
        ]
        for i, (tex, caption, color) in enumerate(items):
            yy = 3.7 - i * 2.0
            symbol = equation(tex, y=yy, size=46, color=color).move_to([-2.65, yy, 0])
            label = text(caption, 23, width=5.35).move_to([.8, yy, 0])
            self.play(FadeIn(symbol), FadeIn(label), run_time=.6)
        units = equation(r"[P]=\frac{\mathrm N}{\mathrm m^2}=\frac{\mathrm J}{\mathrm m^3}", y=-2.1, size=43)
        self.play(Write(units), run_time=.8)
        self.note("Os três termos podem ser somados:\ntodos têm unidade de energia por volume.")
        self.until(150)
        # Orçamento ideal a mesma altura: total fixo; pressão cede à cinética.
        pbar = Rectangle(width=3.5, height=.32, fill_color=CYAN, fill_opacity=1, stroke_width=0).move_to([-1.75, -3.25, 0])
        kbar = Rectangle(width=1.8, height=.32, fill_color=PURPLE, fill_opacity=1, stroke_width=0).next_to(pbar, RIGHT, buff=0)
        ubar = Rectangle(width=1.7, height=.32, fill_color=GOLD, fill_opacity=1, stroke_width=0).next_to(kbar, RIGHT, buff=0)
        budget = VGroup(pbar, kbar, ubar).move_to([0, -3.25, 0])
        self.play(FadeIn(budget), run_time=.4)
        pnew = pbar.copy().stretch_to_fit_width(2.1).align_to(pbar, LEFT)
        knew = kbar.copy().stretch_to_fit_width(3.2).next_to(pnew, RIGHT, buff=0)
        self.play(Transform(pbar, pnew), Transform(kbar, knew), run_time=1.2)
        self.hold_to(155, "significado_unidades")

        # 155–168 s: duas leis distintas, só no caso horizontal ideal.
        self.clear_stage("Estreitamento: duas leis")
        tube3d = solid.mobject(cena=self, largura=7.0, centro=UP * 2.6, periodo=2)
        self.add(tube3d)
        self.play(FadeIn(text("1  CONTINUIDADE", 26, CYAN).move_to([0, .5, 0])), run_time=.5)
        cont = equation(r"A_1v_1=A_2v_2", y=-.45, size=48, color=CYAN)
        narrow = equation(r"A_2<A_1\quad\Rightarrow\quad v_2>v_1", y=-1.65, size=43)
        # Cortes: seção 1 no trecho largo; seção 2 no gargalo (não na outra ponta).
        labels = VGroup(
            text("1 · larga", 23, CYAN).move_to([-2.8, 1.5, 0]),
            text("2 · gargalo", 23, PURPLE).move_to([1.0, 4.7, 0]),
            Line([-2.8, 1.85, 0], [-1.9, 3.8, 0], color=CYAN, stroke_width=1.5),
            Line([.8, 4.35, 0], [-.5, 3.45, 0], color=PURPLE, stroke_width=1.5),
        )
        self.add(labels)
        self.play(Write(cont), Write(narrow), run_time=.9)
        self.note("Continuidade explica o aumento da velocidade.")
        self.hold_to(161, "estreitamento_continuidade")
        self.play(FadeOut(cont), FadeOut(narrow), run_time=.3)
        law = text("2  BERNOULLI · h₁ ≈ h₂", 26, PURPLE).move_to([0, .5, 0])
        old = [m for m in self.mobjects if isinstance(m, VGroup) and m is not labels and abs(m.get_y() - .5) < .1]
        self.play(*(FadeOut(m) for m in old), FadeIn(law), run_time=.4)
        equal = equation(r"P_1+\frac12\rho v_1^2", "=", r"P_2+\frac12\rho v_2^2", y=-.6, size=44)
        conclusion = equation(r"v_2>v_1\quad\Rightarrow\quad P_2<P_1", y=-2.15, size=44, color=PURPLE)
        self.play(Write(equal), run_time=.7)
        self.play(Write(conclusion), run_time=.6)
        self.note("Neste caso ideal e à mesma altura,\nBernoulli relaciona velocidade e pressão.")
        self.hold_to(168, "estreitamento_bernoulli")
        tube3d.pausar()

        # 168–175 s: hipóteses visíveis e fórmula final.
        self.clear_stage("Quando essa conta vale?")
        conditions = text("Fluido ideal e incompressível\nSem viscosidade\nEscoamento estacionário\nAo longo de uma linha de corrente", 29).move_to([0, 2.7, 0])
        self.play(FadeIn(conditions), run_time=.7)
        final = self.bernoulli(y=-.65)
        self.play(Write(final), run_time=.9)
        self.note("Um balanço de trabalho e energia,\nsob essas hipóteses.")
        self.hold_to(175, "hipoteses_finais")
        (UNIT / "tempos_preview.json").write_text(json.dumps({"duracao_s": round(self.time, 3), "estados": self.marks, "layout": self.layout_checks}, ensure_ascii=False, indent=2), encoding="utf-8")

    def title(self, s):
        new = text(s, 35).move_to([0, 5.6, 0])
        if hasattr(self, "heading"):
            self.remove(self.heading)
        self.heading = new
        self.add(new)
        self.check(new, s)

    def note(self, s):
        if hasattr(self, "caption"):
            self.remove(self.caption)
        self.caption = text(s, 26, MUTED).move_to([0, -4.9, 0])
        self.add(self.caption)
        self.check(self.caption, s)

    def clear_stage(self, title):
        old = [m for m in self.mobjects if m not in self.fixed]
        if old:
            self.play(*(FadeOut(m) for m in old), run_time=.4)
        self.title(title)

    def replace(self, old, new):
        self.check(new, "equação")
        self.play(TransformMatchingTex(old, new), run_time=.85)
        return new

    def until(self, t):
        if self.time > t + .12:
            raise ValueError(f"Bloco excedeu o tempo: {self.time:.3f} > {t}")
        if t > self.time:
            self.wait(t - self.time)

    def hold_to(self, t, name):
        self.mark(name)
        self.until(t)

    def mark(self, name):
        self.marks[name] = round(self.time + .2, 3)
        for m in self.mobjects:
            if m not in self.fixed and isinstance(m, (MathTex, VGroup)):
                self.check(m, name)

    def check(self, m, name):
        # UI no miolo seguro: imagem 3D tem grandes margens transparentes.
        bounds = [float(m.get_left()[0]), float(m.get_right()[0]), float(m.get_bottom()[1]), float(m.get_top()[1])]
        if bounds[0] < -4.1 or bounds[1] > 4.1 or bounds[2] < -6.1 or bounds[3] > 6.2:
            raise ValueError(f"Conteúdo fora da área segura ({name}): {bounds}")
        self.layout_checks.append({"estado": name, "limites": [round(x, 3) for x in bounds]})

    def bernoulli(self, y):
        return equation(r"P", "+", r"\frac12\rho v^2", "+", r"\rho gh", "=", r"\text{constante}", y=y, size=48)

    def full_balance(self, volume):
        dv = r"\Delta V" if volume else ""
        lhs = equation(r"(P_1-P_2)", dv, "=", y=2.6, size=51)
        k = equation(r"\frac12\rho", dv, r"(v_2^2-v_1^2)", y=.7, size=51, color=CYAN)
        u = equation("+", r"\rho g", dv, r"(h_2-h_1)", y=-1.2, size=51, color=GOLD)
        return VGroup(lhs, k, u)

    def pipe(self, details=True):
        # Vista 2D longitudinal; área transversal indicada nas faces elípticas.
        top = [(-3.4, 2.7), (-1.7, 2.8), (.1, 3.25), (1.8, 3.8), (3.1, 3.8)]
        bottom = [(-3.4, 1.35), (-1.7, 1.55), (.1, 2.3), (1.8, 3.05), (3.1, 3.05)]
        walls = VGroup(*(VMobject(color=CYAN, stroke_width=3).set_points_smoothly([np.array([x, y, 0]) for x, y in pts]) for pts in [top, bottom]))
        faces = VGroup(Ellipse(width=.35, height=1.35, color=CYAN, fill_opacity=.18).move_to([-3.4, 2.025, 0]), Ellipse(width=.26, height=.75, color=PURPLE, fill_opacity=.2).move_to([3.1, 3.425, 0]))
        arrows = VGroup(Arrow([-2.6, 2.05, 0], [-1.4, 2.15, 0], color=CYAN, buff=0), Arrow([1.1, 3.23, 0], [2.6, 3.43, 0], color=PURPLE, buff=0))
        ref = DashedLine([-3.65, .2, 0], [3.5, .2, 0], color=MUTED, stroke_width=1)
        heights = VGroup(DashedLine([-3.4, .2, 0], [-3.4, 2.025, 0], color=GOLD), DashedLine([3.1, .2, 0], [3.1, 3.425, 0], color=GOLD), equation(r"h_1", size=32, color=GOLD).move_to([-2.95, .9, 0]), equation(r"h_2", size=32, color=GOLD).move_to([3.55, 1.5, 0]))
        group = VGroup(walls, faces, arrows, ref, heights)
        if details:
            group.add(equation(r"1:\ A_1,\ P_1,\ v_1", size=32, color=CYAN).move_to([-2.3, 4.45, 0]), equation(r"2:\ A_2,\ P_2,\ v_2", size=32, color=PURPLE).move_to([2.05, 4.45, 0]))
        return group

    def face(self, section):
        color = CYAN if section == 1 else PURPLE
        area = Ellipse(width=.65, height=2.2, color=color, fill_opacity=.3).move_to([.6, 2.5, 0])
        area_label = equation(fr"A_{section}", size=45, color=color).move_to([1.7, 2.5, 0])
        force = Arrow([-2.6, 2.5, 0], [.4, 2.5, 0], color=color, buff=0, stroke_width=6)
        flabel = equation(fr"F_{section}", size=41, color=color).move_to([-1.4, 3.15, 0])
        return VGroup(area, area_label, force, flabel)

    def swept_volume(self, section):
        entrance = section == 1
        color = CYAN if entrance else PURPLE
        height, travel = (1.7, 1.15) if entrance else (1.18, 1.65)
        # Mesmo volume: altura visual menor e comprimento maior na saída.
        x, y = -1.4, 2.5
        face = Ellipse(width=.35, height=height, color=color, fill_opacity=.28).move_to([x, y, 0])
        swept = Rectangle(width=travel, height=height, color=GOLD, fill_color=GOLD, fill_opacity=.18, stroke_width=1.3).move_to([x + travel / 2, y, 0])
        finalface = face.copy().shift(RIGHT * travel).set_color(GOLD)
        swept = VGroup(swept, finalface)
        original = face.copy().set_opacity(.4)
        flow = Arrow([-.7, 4.05, 0], [1.8, 4.05, 0], color=MUTED, buff=0)
        flowlabel = text("avanço do fluido", 22, MUTED).move_to([.55, 4.55, 0])
        start, end = ([-3.3, y, 0], [x - .15, y, 0]) if entrance else ([2.8, y, 0], [x + travel + .2, y, 0])
        force = Arrow(start, end, color=color, buff=0, stroke_width=6)
        flabel = equation(fr"F_{section}=P_{section}A_{section}", size=35, color=color).move_to([-2.25 if entrance else 2.0, y + 1.15, 0])
        alabel = equation(fr"A_{section}", size=35, color=color).move_to([x - .6, y - height / 2 - .35, 0])
        bracket = BraceBetweenPoints([x, y - height / 2 - .15, 0], [x + travel, y - height / 2 - .15, 0], DOWN, color=GOLD)
        dxlabel = equation(fr"\Delta x_{section}", size=34, color=GOLD).next_to(bracket, DOWN, buff=.1)
        dx = VGroup(bracket, dxlabel)
        return VGroup(original, face, flow, flowlabel, force, flabel, alabel), face, swept, dx
