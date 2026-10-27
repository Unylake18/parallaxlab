"""N01–N18 · preview silencioso horizontal da queda orbital.

uv run python -m manim -r 960,540 --fps 15 --media_dir videos_longos/yt_0007_orbita_queda_continua/media_preview videos_longos/yt_0007_orbita_queda_continua/cena.py OrbitaQuedaContinua007

SO=7,8 seleciona blocos independentes para depuração. Não há áudio ou sincronização.
O modelo usa SI; projeção, ampliação local e compressão de tempo são só gráficas.
"""

from contextlib import contextmanager
import json
import math
import os
from pathlib import Path
import sys

import numpy as np
from manim import (
    AnimationGroup, Arrow, Circle, Create, DashedLine, DashedVMobject,
    DecimalNumber, Dot, DoubleArrow, Ellipse, FadeIn, FadeOut, ImageMobject,
    Indicate, LaggedStart, Line, MathTex, Polygon, Rectangle, Scene,
    Transform, TransformFromCopy, TransformMatchingTex, ValueTracker,
    VGroup, VMobject, always_redraw, config, linear,
    UP, DOWN, LEFT, RIGHT, WHITE,
)

PASTA = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA.parents[1]))
sys.path.insert(0, str(PASTA))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text
from modelo_orbital import R_T, MU, conica, integrar, lancamento, periodo, v_circular, validar

AZUL = '#267BFF'
CIANO = PRIMARY_COLOR
BRANCO = TEXT_COLOR
VIOLETA = '#9C8CFF'
SUAVE = '#A9BBD8'
SO = {int(n) for n in os.environ.get('SO', '').split(',') if n.strip()}
config.max_files_cached = 1000


@contextmanager
def pango_largo():
    w, h = config.pixel_width, config.pixel_height
    config.pixel_width = config.pixel_height = 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = w, h


def texto(s, tamanho=28, cor=BRANCO, largura=None):
    with pango_largo():
        obj = screen_text(s, tamanho).set_color(cor)
    if largura and obj.width > largura:
        obj.scale_to_fit_width(largura)
    return obj


def equacao(s, tamanho=42, cor=BRANCO, largura=6.2):
    obj = MathTex(s, font_size=tamanho, color=cor)
    if largura and obj.width > largura:
        obj.scale_to_fit_width(largura)
    return obj


def ponto(p):
    return np.array([p[0], p[1], 0.0])


def projetar(p, centro, escala):
    return np.asarray(centro) + ponto(np.asarray(p) / R_T) * escala


def amostrar(orb, passo=5):
    return np.vstack([orb.r[::passo], orb.r[-1]])


def curva(pontos, centro, escala, cor=AZUL, largura=3.5):
    arr = np.asarray(pontos)
    xyz = np.column_stack([arr[:, :2] / R_T * escala, np.zeros(len(arr))]) + centro
    return VMobject().set_points_as_corners(xyz).set_stroke(cor, largura).set_fill(opacity=0).set_z_index(3)


def planeta(centro, raio):
    """Disco esférico esquemático, inteiramente vetorial, sem assets novos."""
    corpo = Circle(radius=raio, color='#4388C7', stroke_width=2,
                   fill_color='#102645', fill_opacity=1)
    paralelos = VGroup(*[
        Ellipse(width=1.8 * raio, height=h * raio, color='#2D5579', stroke_width=1)
        for h in (.45, 1.1)
    ])
    meridiano = Ellipse(width=.7 * raio, height=1.93 * raio,
                        color='#2D5579', stroke_width=1)
    return VGroup(corpo, paralelos, meridiano).move_to(centro).set_z_index(0)


def seta(inicio, fim, cor=BRANCO, largura=3.4):
    return Arrow(inicio, fim, buff=0, color=cor, stroke_width=largura,
                 max_tip_length_to_length_ratio=.25, tip_length=.15).set_z_index(6)


def satelite(pos, escala=.24):
    cabine = Rectangle(width=.5, height=.38, stroke_width=1.5,
                       color=BRANCO, fill_color='#D8E7FC', fill_opacity=1)
    paineis = VGroup(*[
        Rectangle(width=.68, height=.35, color=AZUL, fill_color='#184D93',
                  fill_opacity=1, stroke_width=1.2).shift(s * .65 * RIGHT)
        for s in (-1, 1)
    ])
    return VGroup(paineis, cabine).scale(escala).move_to(pos).set_z_index(6)


def astronauta(pos, escala=.6):
    cabeca = Circle(radius=.16, color=BRANCO, fill_color='#A9D2E5', fill_opacity=1)
    tronco = Line([0, -.16, 0], [0, -.65, 0], color=BRANCO, stroke_width=5)
    membros = VGroup(*[Line(a, b, color=BRANCO, stroke_width=4) for a, b in [
        ([0, -.3, 0], [-.3, -.48, 0]), ([0, -.3, 0], [.3, -.4, 0]),
        ([0, -.65, 0], [-.22, -.97, 0]), ([0, -.65, 0], [.22, -.97, 0])]])
    return VGroup(cabeca, tronco, membros).scale(escala).move_to(pos).set_z_index(6)


class OrbitaQuedaContinua007(Scene):
    def wait(self, duration=1, **kwargs):
        # Os tempos físicos só avançam em plays explícitos (ou em N10).
        # Pausas de leitura podem repetir o quadro sem recalcular updaters.
        kwargs.setdefault('frozen_frame', True)
        return super().wait(duration, **kwargs)

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.validacao = validar()
        self.tempos = []
        self.marcos = []
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(.45)
        self.wm.move_to([6.25, -3.91, 0]).set_z_index(50)
        for n in range(1, 19):
            if SO and n not in SO:
                continue
            inicio = float(self.time)
            getattr(self, f'n{n:02d}')()
            self.tempos.append(dict(bloco=f'N{n:02d}', inicio=inicio, fim=float(self.time)))
        nome = 'timing_preview.json' if not SO else 'timing_parcial_' + '_'.join(map(str, sorted(SO))) + '.json'
        (PASTA / nome).write_text(json.dumps(dict(blocos=self.tempos, marcos=self.marcos,
            duracao=float(self.time), fps=config.frame_rate), indent=2, ensure_ascii=False), encoding='utf-8')
        (PASTA / 'validacao_fisica.json').write_text(json.dumps(self.validacao,
            indent=2, ensure_ascii=False), encoding='utf-8')

    def abre(self, numero, titulo):
        for mob in self.mobjects:
            mob.clear_updaters(recursive=True)
        antigos = [m for m in self.mobjects if m is not self.wm]
        if antigos:
            self.play(*[FadeOut(m) for m in antigos], run_time=.6)
        self.clear()
        self.add(self.wm)
        self.add(texto('FÍSICA I  /  GRAVITAÇÃO', 18, SUAVE).move_to([-4.94, 3.83, 0]))
        self.add(texto(f'{numero:02d} / 18', 18, SUAVE).move_to([6.55, 3.83, 0]))
        self.cabecalho = texto(titulo, 36, largura=14.1).move_to([0, 3.03, 0])
        self.play(FadeIn(self.cabecalho, shift=.12 * UP), run_time=.6)

    def marco(self, nome):
        self.marcos.append(dict(nome=nome, tempo=float(self.time)))

    def nota(self, s, y=-2.52, cor=SUAVE, tamanho=24):
        return texto(s, tamanho, cor, largura=13.8).move_to([0, y, 0])

    def circular(self, centro=np.array([-3.2, -.25, 0]), escala=1.8, raio=1.06 * R_T):
        orb = lancamento(raio, 1.0)
        tempo = ValueTracker(0)
        pos = lambda: projetar(orb.estado(tempo.get_value())[0], centro, escala)
        vel = lambda: ponto(orb.estado(tempo.get_value())[1] / v_circular(raio))
        terra = planeta(centro, escala)
        trilha = curva(amostrar(orb, 6), centro, escala)
        movel = always_redraw(lambda: Dot(pos(), radius=.075, color=BRANCO).set_z_index(7))
        self.add(terra, trilha, movel)
        return orb, tempo, pos, vel, terra, trilha, movel

    def n01(self):
        self.abre(1, 'E se você lançasse uma pedra cada vez mais rápido?')
        raio = ValueTracker(4.4)
        cy = ValueTracker(-3.4)
        centro = lambda: np.array([-3.0, cy.get_value(), 0])
        terra = always_redraw(lambda: planeta(centro(), raio.get_value()))
        montanha = always_redraw(lambda: Polygon(
            centro() + raio.get_value() * np.array([-.04, .998, 0]),
            centro() + raio.get_value() * np.array([0, 1.06, 0]),
            centro() + raio.get_value() * np.array([.04, .998, 0]),
            color=SUAVE, fill_color='#556B8B', fill_opacity=1, stroke_width=1).set_z_index(2))
        self.add(terra, montanha)
        etiqueta = texto('Montanha idealizada\nSem atmosfera', 24, SUAVE).move_to([3.6, 1.3, 0])
        self.play(FadeIn(etiqueta))
        leitura = texto('Mais velocidade lateral.', 30).move_to([3.6, -.1, 0])
        self.play(FadeIn(leitura))
        for i, (fator, zoom, altura) in enumerate(zip(
                (.55, .80, .985, 1.0), (4.4, 3.0, 2.04, 2.04), (-3.4, -1.8, -.3, -.3))):
            orb = lancamento(1.06 * R_T, fator)
            progresso = ValueTracker(0)
            def desenho(o=orb, p=progresso):
                t = p.get_value()
                k = np.searchsorted(o.t, t)
                ps = np.vstack([o.r[:max(1, k):5], o.estado(t)[0]])
                return curva(ps, centro(), raio.get_value())
            trilha = always_redraw(desenho)
            bola = always_redraw(lambda o=orb, p=progresso: Dot(
                projetar(o.estado(p.get_value())[0], centro(), raio.get_value()),
                radius=.075, color=BRANCO).set_z_index(7))
            ordem = texto(f'Lançamento {i + 1}', 24, CIANO).move_to([3.6, -.9, 0])
            self.play(raio.animate.set_value(zoom), cy.animate.set_value(altura), FadeIn(ordem), run_time=1.5)
            self.add(trilha, bola)
            self.play(progresso.animate.set_value(orb.t[-1]), run_time=5.5 if i < 2 else 7, rate_func=linear)
            self.wait(.6)
            self.marco(f'N01_lancamento_{i+1}')
            self.play(FadeOut(bola), FadeOut(ordem), run_time=.4)
            trilha.clear_updaters()
            # Trilha anterior acompanha a abertura da câmera sem mudar o modelo SI.
            trilha.add_updater(lambda m, o=orb: m.become(curva(np.vstack([o.r[::5], o.r[-1]]),
                centro(), raio.get_value()).set_stroke(opacity=.35)))
        self.play(Transform(leitura, texto('Agora, ela não alcança o chão.', 29,
                       largura=6.0).move_to([3.6, -.1, 0])), run_time=.8)
        self.wait(3)

    def n02(self):
        self.abre(2, 'Ele continua caindo')
        orb, t, pos, vel, terra, trilha, bola = self.circular()
        grav = always_redraw(lambda: seta(pos(), pos() + .85 * (np.array([-3.2, -.25, 0]) - pos()) /
                                         np.linalg.norm(np.array([-3.2, -.25, 0]) - pos()), CIANO))
        self.add(grav)
        self.play(t.animate.set_value(.72 * orb.t[-1]), run_time=9, rate_func=linear)
        frase = texto('Ele nunca parou\nde cair.', 40).move_to([3.3, .55, 0])
        self.play(FadeIn(frase))
        self.play(FadeIn(texto('A gravidade aponta para o centro.', 25, CIANO,
                        largura=6.5).move_to([3.3, -1.1, 0])))
        self.marco('N02_gravidade_unica')
        self.wait(4)

    def n03(self):
        self.abre(3, 'O que aconteceria sem gravidade?')
        c = np.array([-3.7, -.65, 0])
        orb, t, pos, vel, terra, trilha, bola = self.circular(c, 1.65)
        origem = pos().copy()
        tangente = DashedLine(origem, origem + 8.5 * RIGHT, color=VIOLETA, dash_length=.13)
        fantasma = Dot(origem, radius=.085, color=VIOLETA).set_z_index(8)
        self.play(Create(tangente), FadeIn(fantasma))
        duracao_fisica = .55 * orb.t[-1]
        deslocamento_livre = v_circular(1.06 * R_T) * duracao_fisica / R_T * 1.65
        self.play(t.animate.set_value(duracao_fisica), fantasma.animate.shift(deslocamento_livre * RIGHT),
                  run_time=7, rate_func=linear)
        sem = texto('Sem força → linha reta', 28, VIOLETA).move_to([3.45, .25, 0])
        com = texto('Gravidade → a velocidade muda de direção', 27, CIANO,
                    largura=6.9).move_to([3.45, -1.05, 0])
        self.play(FadeIn(sem), FadeIn(com))
        self.wait(4)

    def n04(self):
        self.abre(4, 'A gravidade gira a velocidade')
        c = np.array([-3.8, -.4, 0])
        orb, t, pos, vel, terra, trilha, bola = self.circular(c, 1.65)
        legenda = equacao(r'\Delta\vec v\approx\vec a\,\Delta t', 46, largura=6.1).move_to([3.65, -1.7, 0])
        for j, fracao in enumerate((.06, .30, .56)):
            t.set_value(fracao * orb.t[-1])
            p0, v0 = orb.estado(t.get_value())
            p1, v1 = orb.estado(t.get_value() + .032 * orb.t[-1])
            v0, v1 = ponto(v0 / v_circular(1.06 * R_T)), ponto(v1 / v_circular(1.06 * R_T))
            a0 = seta(projetar(p0, c, 1.65), projetar(p0, c, 1.65) + 1.35 * v0)
            a1 = seta(projetar(p1, c, 1.65), projetar(p1, c, 1.65) + 1.35 * v1, SUAVE)
            l0 = equacao(r'\vec v(t)', 30).next_to(a0, UP, buff=.13)
            l1 = equacao(r'\vec v(t+\Delta t)', 29).next_to(a1, DOWN, buff=.13)
            self.play(Create(a0), FadeIn(l0), run_time=.6)
            self.play(t.animate.increment_value(.032 * orb.t[-1]), Create(a1), FadeIn(l1), run_time=1.0)
            o = np.array([3.65, .3, 0])
            b0, b1 = seta(o, o + 1.6 * v0), seta(o, o + 1.6 * v1, SUAVE)
            dv = seta(o + 1.6 * v0, o + 1.6 * v1, CIANO)
            self.play(TransformFromCopy(a0, b0), TransformFromCopy(a1, b1), run_time=1.2)
            self.play(Create(dv), run_time=.6)
            rot = texto('Mudança radial\nno limite de um intervalo pequeno', 24, CIANO,
                         largura=6.2).move_to([3.55, 1.8, 0])
            self.play(FadeIn(rot), *([FadeIn(legenda)] if j == 0 else []), run_time=.6)
            self.marco(f'N04_origem_comum_{j+1}')
            self.wait(2)
            self.play(*[FadeOut(m) for m in (a0, a1, l0, l1, b0, b1, dv, rot)], run_time=.5)
        diferencial = equacao(r'd\vec v=\vec a\,dt', 42).move_to([3.6, .3, 0])
        self.play(FadeIn(diferencial))
        self.wait(3)

    def n05(self):
        self.abre(5, 'Duas descrições da mesma aceleração')
        c = np.array([-3.3, -.3, 0])
        orb, t, pos, vel, terra, trilha, bola = self.circular(c, 1.75)
        t.set_value(.10 * orb.t[-1])
        av = always_redraw(lambda: seta(pos(), pos() + 1.0 * vel()))
        ag = always_redraw(lambda: seta(pos(), pos() + .85 * (c - pos()) / np.linalg.norm(c - pos()), CIANO))
        self.add(av, ag)
        self.play(FadeIn(texto('Para descrever o círculo', 26, SUAVE).move_to([3.5, 1.7, 0])))
        self.play(FadeIn(equacao(r'a_c=\frac{v^2}{r}', 48).move_to([3.5, .8, 0])))
        self.wait(2)
        self.play(FadeIn(texto('A gravidade fornece essa aceleração', 25, CIANO,
                        largura=6.5).move_to([3.5, -.45, 0])))
        self.play(FadeIn(equacao(r'g(r)=\frac{GM}{r^2}', 48, CIANO).move_to([3.5, -1.4, 0])))
        self.play(t.animate.set_value(.82 * orb.t[-1]), run_time=8, rate_func=linear)
        self.wait(2)

    def n06(self):
        self.abre(6, 'A velocidade que faz a queda acompanhar o círculo')
        c = np.array([-3.7, -.35, 0])
        orb, t, pos, vel, terra, trilha, bola = self.circular(c, 1.65)
        t.set_value(.12 * orb.t[-1])
        ag = seta(pos(), pos() + .85 * (c - pos()) / np.linalg.norm(c - pos()), CIANO)
        av = seta(pos(), pos() + 1.0 * vel())
        self.play(Create(ag), Create(av))
        papel = texto('A gravidade faz o papel centrípeto.', 25, CIANO, largura=6.6).move_to([3.5, 1.65, 0])
        self.play(FadeIn(papel))
        e1 = equacao(r'\frac{GM}{r^2}=\frac{v^2}{r}', 50).move_to([3.4, .35, 0])
        e2 = equacao(r'v^2=\frac{GM}{r}', 50).move_to(e1)
        e3 = equacao(r'v_{\mathrm{orb}}=\sqrt{\frac{GM}{r}}', 55, CIANO).move_to(e1)
        self.play(FadeIn(e1))
        self.wait(2.5)
        # Correspondência por símbolos é suficiente; MF-Tools foi considerado,
        # mas aqui não há cancelamento/glyph map que melhore a leitura.
        self.play(TransformMatchingTex(e1, e2), run_time=1.8)
        self.wait(2)
        self.play(TransformMatchingTex(e2, e3), run_time=1.8)
        self.marco('N06_payoff')
        self.play(FadeIn(texto('Uma condição para a órbita circular.', 26, SUAVE,
                        largura=6.4).move_to([3.4, -1.4, 0])))
        self.wait(4)

    def geometria_local(self):
        """Um segundo a 400 km; eixos gráficos têm escalas diferentes e avisadas.

        x representa a distância tangencial SI, y representa a queda SI ampliada.
        O arco é a circunferência exata, não uma parábola desenhada livremente.
        """
        r = R_T + 400e3
        v = v_circular(r)
        estado = ValueTracker(0)
        origem = np.array([-5.85, .6, 0])
        sx, sy = 10.5 / v, 1.4 / (MU / r**2 / 2)
        def coordenada(t):
            ang = v * t / r
            return origem + np.array([r * math.sin(ang) * sx, -r * (1 - math.cos(ang)) * sy, 0])
        ts = np.linspace(0, 1, 150)
        arco = VMobject().set_points_as_corners([coordenada(t) for t in ts]).set_stroke(AZUL, 4)
        tangente = DashedLine(origem, origem + 11.2 * RIGHT, color=VIOLETA, dash_length=.14)
        real = always_redraw(lambda: Dot(coordenada(estado.get_value()), .085, color=BRANCO).set_z_index(7))
        fantasma = always_redraw(lambda: Dot(origem + sx * v * estado.get_value() * RIGHT,
                                             .075, color=VIOLETA).set_z_index(7))
        self.add(tangente, arco, real, fantasma)
        avisos = VGroup(
            texto('aproximação local · t = 1 s', 25, SUAVE),
            texto('curvatura ampliada para visualização', 25, VIOLETA),
        ).arrange(DOWN, buff=.18).move_to([0, 2.08, 0])
        self.add(avisos)
        return estado, origem, coordenada, real, fantasma

    def n07(self):
        self.abre(7, 'Quanto ele cai em um segundo?')
        aviso = texto('Agora: órbita circular a 400 km de altitude', 30, CIANO).move_to([0, .5, 0])
        valores = equacao(r'r=6\,771\,\mathrm{km}\qquad v\approx7{,}67\,\mathrm{km/s}', 40,
                           largura=12).move_to([0, -.5, 0])
        self.play(FadeIn(aviso), FadeIn(valores))
        self.wait(3)
        self.play(FadeOut(aviso), FadeOut(valores))
        t, o, xy, real, fantasma = self.geometria_local()
        self.play(t.animate.set_value(1), run_time=5, rate_func=linear)
        horizontal = DoubleArrow(o + .43 * UP, o + np.array([10.5, .43, 0]),
                                 color=BRANCO, buff=0, stroke_width=2, tip_length=.12)
        dh = texto('7,67 km na direção tangente', 25).next_to(horizontal, UP, buff=.13)
        queda = DoubleArrow(o + 10.5 * RIGHT, xy(1), color=CIANO, buff=0,
                            stroke_width=3, tip_length=.12)
        dq = texto('4,35 m', 28, CIANO).next_to(queda, RIGHT, buff=.2)
        self.play(Create(horizontal), FadeIn(dh), Create(queda), FadeIn(dq))
        f1 = equacao(r'\frac12gt^2\approx4{,}35\,\mathrm m', 38, CIANO).move_to([-3.6, -1.35, 0])
        f2 = equacao(r'\frac{s^2}{2r}\approx4{,}35\,\mathrm m', 38, AZUL).move_to([3.2, -1.35, 0])
        self.play(FadeIn(f1), FadeIn(f2))
        self.wait(3)
        igual = equacao(r'\frac12gt^2=\frac12\left(\frac{v^2}{r}\right)t^2\approx\frac{s^2}{2r}',
                        45, largura=12.5).move_to([0, -2.35, 0])
        self.play(FadeIn(igual), run_time=1.5)
        self.marco('N07_queda_curvatura_avisos')
        self.wait(5)

    def n08(self):
        self.abre(8, 'A queda acompanha a curvatura')
        t, o, xy, real, fantasma = self.geometria_local()
        self.play(t.animate.set_value(1), run_time=4, rate_func=linear)
        frase = self.nota('Ele cai — e a Terra curva para longe.', -1.65, BRANCO, 34)
        self.play(FadeIn(frase))
        self.wait(3)
        objetos = [m for m in self.mobjects if m not in (self.wm, self.cabecalho)]
        for m in objetos:
            m.clear_updaters(recursive=True)
        self.play(*[FadeOut(m) for m in objetos], run_time=1)
        # Volta do referencial local à visão global, mantendo a órbita de 400 km.
        c = np.array([0, -.2, 0])
        orb, tau, pos, vel, terra, trilha, bola = self.circular(c, 1.9, R_T + 400e3)
        grupo = VGroup(terra, trilha)
        self.play(FadeIn(grupo), run_time=1.4)
        self.play(tau.animate.set_value(.7 * orb.t[-1]), run_time=6, rate_func=linear)
        self.wait(1)

    def n09(self):
        self.abre(9, 'Gravidade forte. Peso aparente pequeno.')
        c = np.array([-4.45, -.6, 0])
        self.add(planeta(c, 1.35))
        trilha = Circle(radius=2.05, color=AZUL, stroke_width=2).move_to(c)
        self.play(Create(trilha))
        # Estação e astronauta livres: dois estados próximos no mesmo campo SI.
        r = R_T + 400e3
        nave_traj = integrar([0, r], [v_circular(r), 0], 800)
        pessoa_traj = integrar([5000, r], [v_circular(r), 0], 800)
        tau = ValueTracker(0)
        # Projeção ampliada da altitude e separação explicitamente esquemática.
        def posicao(orb):
            rp = orb.estado(tau.get_value())[0]
            return c + ponto(rp / np.linalg.norm(rp)) * 2.05
        nave = always_redraw(lambda: satelite(posicao(nave_traj), .46))
        pessoa = always_redraw(lambda: astronauta(posicao(pessoa_traj) + .52 * RIGHT, .42))
        def direcao_gravidade(orb):
            rp = orb.estado(tau.get_value())[0]
            return -ponto(rp / np.linalg.norm(rp))
        gn = always_redraw(lambda: seta(nave.get_center(), nave.get_center() +
            .75 * direcao_gravidade(nave_traj), CIANO))
        gp = always_redraw(lambda: seta(pessoa.get_center(), pessoa.get_center() +
            .75 * direcao_gravidade(pessoa_traj), CIANO))
        self.add(nave, pessoa, gn, gp)
        self.play(FadeIn(texto('Estação + astronauta', 26).move_to([-4.1, 2.05, 0])))
        self.play(FadeIn(equacao(r'\frac{g_{\mathrm{orbita}}}{g_{\mathrm{superficie}}}'
                      r'=\left(\frac{R}{R+h}\right)^2\approx0{,}89', 39,
                      largura=6.6).move_to([3.55, 1.5, 0])))
        self.play(tau.animate.set_value(750), run_time=6, rate_func=linear)
        self.play(FadeIn(texto('A gravidade não desaparece.', 29, CIANO,
                               largura=6.5).move_to([3.55, .2, 0])))
        mensagem = texto('Queda livre conjunta:\nquase nenhuma força de apoio.', 27,
                         largura=6.5).move_to([3.55, -.85, 0])
        aviso = self.nota('Órbita a 400 km · altitude e separação ampliadas', -2.82, SUAVE, 22)
        self.play(FadeIn(mensagem), FadeIn(aviso))
        self.marco('N09_queda_conjunta')
        self.wait(4)
        # Comparação breve: apoio impede a queda na superfície.
        mini = astronauta([2.4, -1.7, 0], .55)
        y_chao = mini.get_bottom()[1]
        chao = Line([1.4, y_chao, 0], [3.4, y_chao, 0], color=SUAVE)
        self.play(FadeOut(mensagem), FadeOut(aviso), run_time=.4)
        self.play(FadeIn(mini), Create(chao), Create(seta([2.28, -1.7, 0], [2.28, -.9, 0], BRANCO)),
                  Create(seta([2.52, -1.7, 0], [2.52, -2.5, 0], CIANO)),
                  FadeIn(equacao(r'N', 28).move_to([1.72, -.9, 0])),
                  FadeIn(equacao(r'mg', 28, CIANO).move_to([3.12, -2.35, 0])))
        self.play(FadeIn(texto('Na superfície, o chão sustenta.', 24,
                               largura=6).move_to([3.4, -2.72, 0])))
        self.wait(4)

    def n10(self):
        self.abre(10, 'Órbita mais alta, velocidade menor')
        c = np.array([-3.6, -.25, 0])
        self.add(planeta(c, .85))
        r = ValueTracker(1.18 * R_T)
        fase = ValueTracker(.3)
        fase.add_updater(lambda m, dt: m.increment_value(math.sqrt(MU / r.get_value()**3) * 450 * dt))
        self.add(fase)
        pos = lambda: c + .85 * r.get_value() / R_T * np.array([math.sin(fase.get_value()), math.cos(fase.get_value()), 0])
        tangent = lambda: np.array([math.cos(fase.get_value()), -math.sin(fase.get_value()), 0])
        circulo = always_redraw(lambda: Circle(radius=.85 * r.get_value() / R_T,
                            color=AZUL, stroke_width=3).move_to(c))
        bola = always_redraw(lambda: Dot(pos(), .075, color=BRANCO))
        av = always_redraw(lambda: seta(pos(), pos() + 1.35 * v_circular(r.get_value()) /
                                       v_circular(1.18 * R_T) * tangent()))
        self.add(circulo, bola, av)
        self.play(FadeIn(texto('Comparação de órbitas circulares', 23, SUAVE,
                               largura=6.5).move_to([3.5, 1.85, 0])))
        self.play(FadeIn(equacao(r'v_{\mathrm{orb}}=\sqrt{\frac{GM}{r}}', 50).move_to([3.5, .6, 0])))
        rel = equacao(r'r\uparrow\quad\Longrightarrow\quad v\downarrow', 47, CIANO).move_to([3.5, -.8, 0])
        self.play(FadeIn(rel))
        self.play(r.animate.set_value(2.8 * R_T), run_time=11, rate_func=linear)
        self.marco('N10_raio_velocidade')
        self.wait(3, frozen_frame=False)

    def n11(self):
        self.abre(11, 'Uma volta: distância dividida pela velocidade')
        c = np.array([-3.7, -.3, 0])
        orb, t, pos, vel, terra, trilha, bola = self.circular(c, 1.6)
        self.play(FadeIn(texto('caso circular', 28, CIANO).move_to([3.5, 1.8, 0])))
        e1 = equacao(r'T=\frac{2\pi r}{v}', 50).move_to([3.4, .45, 0])
        e2 = equacao(r'T=2\pi\sqrt{\frac{r^3}{GM}}', 50).move_to(e1)
        e3 = equacao(r'T^2=\frac{4\pi^2}{GM}\,r^3', 50).move_to(e1)
        self.play(FadeIn(e1), t.animate.set_value(orb.t[-1]), run_time=7, rate_func=linear)
        self.wait(2)
        self.play(TransformMatchingTex(e1, e2), run_time=2)
        self.wait(3)
        self.play(TransformMatchingTex(e2, e3), run_time=2)
        self.marco('N11_kepler_circular')
        self.wait(4)

    def n12(self):
        self.abre(12, 'Do círculo à elipse: uma generalização')
        anterior = texto('caso circular', 36, SUAVE).move_to([-3.6, .7, 0])
        seta_conceitual = equacao(r'\longrightarrow', 50).move_to([0, .7, 0])
        novo = texto('generalização:\nórbita elíptica', 34, CIANO).move_to([3.6, .7, 0])
        self.play(FadeIn(anterior), FadeIn(seta_conceitual), FadeIn(novo), run_time=1.5)
        self.marco('N12_transicao_conceitual')
        self.wait(3.5)
        self.play(FadeOut(anterior), FadeOut(seta_conceitual), FadeOut(novo))
        a, b = 2.75, 1.7
        foco = math.sqrt(a*a-b*b)
        centro = np.array([-3.7, -.25, 0])
        terra = planeta(centro + foco * LEFT, .42)
        elipse = Ellipse(width=2*a, height=2*b, color=AZUL, stroke_width=3).move_to(centro)
        eixo = DoubleArrow(centro, centro + a * RIGHT, buff=0, color=CIANO,
                           stroke_width=2, tip_length=.12)
        la = equacao('a', 35, CIANO).next_to(eixo, DOWN, buff=.1)
        self.play(FadeIn(terra), Create(elipse), run_time=2)
        self.play(Create(eixo), FadeIn(la))
        foco_label = texto('corpo central em um foco', 23, SUAVE).move_to([-3.7, -2.45, 0])
        self.play(FadeIn(foco_label))
        troca = equacao(r'r\longrightarrow a', 48, CIANO).move_to([3.5, 1.3, 0])
        e1 = equacao(r'T^2=\frac{4\pi^2}{GM}\,r^3', 47).move_to([3.5, 0, 0])
        e2 = equacao(r'T^2=\frac{4\pi^2}{GM}\,a^3', 47).move_to(e1)
        self.play(FadeIn(troca), FadeIn(e1))
        self.play(TransformMatchingTex(e1, e2), run_time=2)
        self.play(FadeIn(texto('No círculo, a = r.', 28, SUAVE).move_to([3.5, -1.45, 0])))
        self.marco('N12_elipse_foco_a')
        self.wait(5)

    def n13(self):
        self.abre(13, 'Um único parâmetro muda o destino')
        c, escala = np.array([-3.8, .4, 0]), .8
        self.add(planeta(c, escala))
        fator = ValueTracker(.70)
        r0 = 1.5 * R_T
        p0 = projetar([0, r0], c, escala)
        traj = always_redraw(lambda: curva(conica(r0, fator.get_value(), alcance=4 * R_T)[0], c, escala))
        av = always_redraw(lambda: seta(p0, p0 + fator.get_value() * 1.35 * RIGHT))
        self.add(traj, av, Dot(p0, .08, color=BRANCO).set_z_index(7))
        self.add(texto('Mesmo ponto. Direção tangencial.', 24, SUAVE,
                       largura=6.7).move_to([3.65, 1.8, 0]))
        self.add(equacao(r'r_0=1{,}5\,R_{\mathrm T}', 36).move_to([3.65, 1.0, 0]))
        estado = texto('impacto', 43, CIANO).move_to([3.65, -.1, 0])
        # Texto só é reconstruído quando a classificação muda, não a cada frame.
        def atualizar_rotulo(m):
            rotulo = conica(r0, fator.get_value(), amostras=2)[1]['rotulo']
            if rotulo != getattr(m, 'estado_atual', None):
                m.become(texto(rotulo, 43, CIANO).move_to([3.65, -.1, 0]))
                m.estado_atual = rotulo
        estado.add_updater(atualizar_rotulo)
        self.add(estado)
        self.add(texto('Só a velocidade inicial varia.', 26, SUAVE,
                       largura=6.6).move_to([3.65, -1.2, 0]))
        self.wait(3)
        self.marco('N13_impacto_ligado')
        for valor, nome in ((.92, 'ligada'), (1.0, 'circular'), (1.20, 'eliptica'), (1.44, 'aberta')):
            self.play(fator.animate.set_value(valor), run_time=2.6, rate_func=linear)
            self.wait(3.5)
            self.marco(f'N13_{nome}')
        self.play(FadeIn(self.nota('Ligada ou aberta: classificação pela energia específica.', -2.65, SUAVE, 23)))
        self.wait(3)

    def n14(self):
        self.abre(14, 'Uma órbita matemática pode atravessar a Terra')
        c, escala = np.array([-3.55, -.2, 0]), 1.65
        self.add(planeta(c, escala))
        orb = lancamento(1.5 * R_T, .70)
        tempo = ValueTracker(0)
        def parcial():
            k = np.searchsorted(orb.t, tempo.get_value())
            ps = np.vstack([orb.r[:max(1, k):5], orb.estado(tempo.get_value())[0]])
            return curva(ps, c, escala)
        fisica = always_redraw(parcial)
        bola = always_redraw(lambda: Dot(projetar(orb.estado(tempo.get_value())[0], c, escala),
                                         .08, color=BRANCO).set_z_index(7))
        self.add(fisica, bola)
        self.play(FadeIn(texto('trajetória física', 30, AZUL).move_to([3.55, 1.3, 0])))
        self.play(tempo.animate.set_value(orb.t[-1]), run_time=6, rate_func=linear)
        self.marco('N14_primeiro_impacto')
        self.wait(2)
        completa = conica(1.5 * R_T, .70, fisica=False)[0]
        ang_hit = math.atan2(orb.r[-1, 0], orb.r[-1, 1])
        ang = np.linspace(0, 2*math.pi, len(completa))
        resto = completa[ang >= ang_hit]
        matematica = DashedVMobject(curva(resto, c, escala, VIOLETA, 3), num_dashes=65,
                                    dashed_ratio=.52).set_z_index(4)
        self.play(Create(matematica), FadeIn(texto('continuação matemática', 29, VIOLETA,
                    largura=6.6).move_to([3.55, .1, 0])), run_time=2)
        self.play(FadeIn(texto('Energia negativa: ligada.\nMas existe colisão.', 28,
                              largura=6.5).move_to([3.55, -1.35, 0])))
        self.marco('N14_continuacao_tracejada')
        self.wait(5)

    def n15(self):
        self.abre(15, 'O canhão de Newton')
        c, escala = np.array([-3.55, -.25, 0]), 2.04
        self.add(planeta(c, escala))
        self.add(Polygon(c + escala * np.array([-.04, .998, 0]),
                         c + escala * np.array([0, 1.06, 0]),
                         c + escala * np.array([.04, .998, 0]),
                         color=SUAVE, fill_color='#556B8B', fill_opacity=1, stroke_width=1))
        trajetorias = VGroup(*[curva(amostrar(lancamento(1.06 * R_T, f)), c, escala).set_stroke(opacity=op)
                              for f, op in ((.55, .5), (.80, .65), (.985, .8), (1.0, 1))])
        self.play(LaggedStart(*[Create(x) for x in trajetorias], lag_ratio=.5), run_time=6)
        self.play(FadeIn(texto('Experimento mental\nde Newton', 37).move_to([3.55, .6, 0])))
        self.play(FadeIn(texto('A queda e a órbita obedecem à mesma lei.', 26, CIANO,
                               largura=6.7).move_to([3.55, -1.2, 0])))
        self.wait(4)

    def n16(self):
        self.abre(16, 'Da pedra à Lua')
        lei = texto('A mesma lei gravitacional.', 36, CIANO).move_to([0, -2.35, 0])
        self.add(lei)
        chao = Line([-2.2, -1.4, 0], [2.2, -1.4, 0], color=SUAVE, stroke_width=3)
        pedra = Dot([0, 1.4, 0], .11, color=BRANCO)
        nome = texto('pedra', 30).move_to([4, .1, 0])
        self.play(Create(chao), FadeIn(pedra), FadeIn(nome))
        # Queda vertical integrada no campo central, em projeção local ampliada.
        queda = integrar([0, R_T + 25], [0, 0], 4, dt=.01)
        q = ValueTracker(0)
        pedra.add_updater(lambda m: m.move_to([0, -1.4 + (np.linalg.norm(queda.estado(q.get_value())[0]) - R_T) / 25 * 2.8, 0]))
        self.play(q.animate.set_value(queda.t[-1]), run_time=3, rate_func=linear)
        pedra.clear_updaters()
        self.wait(1)
        self.play(FadeOut(chao), FadeOut(pedra), FadeOut(nome))
        c = np.array([0, -.1, 0])
        orb, t, pos, vel, terra, trilha, bola = self.circular(c, 1.25)
        nome = texto('satélite artificial', 30).move_to([4.5, .1, 0])
        self.play(FadeIn(nome))
        self.play(t.animate.set_value(orb.t[-1]), run_time=5, rate_func=linear)
        self.play(FadeOut(nome), FadeOut(terra), FadeOut(trilha), FadeOut(bola))
        # Terra–Lua já em torno de ponto comum; não se mantém Terra fixa aqui.
        fase = ValueTracker(0)
        centro = np.array([-.2, -.1, 0])
        direcao = lambda: np.array([math.cos(fase.get_value()), math.sin(fase.get_value()), 0])
        terra2 = always_redraw(lambda: planeta(centro - (4.67 / (384.4 - 4.67)) * 3.3 * direcao(), .45))
        lua = always_redraw(lambda: Circle(radius=.13, color=SUAVE, fill_color='#8195AB',
                    fill_opacity=1).move_to(centro + 3.3 * direcao()))
        self.add(terra2, lua)
        self.play(FadeIn(texto('Terra–Lua', 30).move_to([4.9, .2, 0])),
                  FadeIn(self.nota('Visão esquemática · tamanhos ampliados', -2.85, SUAVE, 22)))
        self.play(fase.animate.set_value(2.5), run_time=5, rate_func=linear)
        self.wait(2)

    def n17(self):
        self.abre(17, 'Terra e Lua orbitam um ponto comum')
        separacao, rb = 384.4e6, 4.67e6
        c = np.array([-3.8, -.15, 0])
        escala = 2.1 / (separacao - rb)
        fase = ValueTracker(0)
        direcao = lambda: np.array([math.cos(fase.get_value()), math.sin(fase.get_value()), 0])
        terra_pos = lambda: c - rb * escala * direcao()
        lua_pos = lambda: c + (separacao - rb) * escala * direcao()
        # Distâncias físicas preservadas. O marcador lunar é ampliado e avisado;
        # a ampliação terrestre ao lado preserva exatamente rb/R_T.
        terra = always_redraw(lambda: Dot(terra_pos(), radius=R_T * escala, color=AZUL).set_z_index(5))
        lua = always_redraw(lambda: Dot(lua_pos(), radius=.035, color=BRANCO).set_z_index(5))
        orb_lua = Circle(radius=2.1, color=AZUL, stroke_width=2).move_to(c)
        orb_terra = Circle(radius=rb * escala, color=AZUL, stroke_width=1.5).move_to(c)
        bary = Dot(c, .018, color=CIANO).set_z_index(8)
        self.add(orb_lua, orb_terra, terra, lua, bary)
        self.add(texto('Distâncias em escala · Lua ampliada', 23, SUAVE,
                       largura=6.7).move_to([-3.8, 2.2, 0]))
        # Ampliação LOCAL: mesmo fator para raio terrestre e posição do baricentro.
        centro_zoom = np.array([3.1, .25, 0])
        R_zoom = 1.0
        k = R_zoom / R_T
        zoom_terra = always_redraw(lambda: planeta(centro_zoom - rb * k * direcao(), R_zoom))
        zoom_b = Dot(centro_zoom, .065, color=CIANO).set_z_index(8)
        zoom_centro = always_redraw(lambda: Dot(centro_zoom - rb * k * direcao(), .045, color=BRANCO).set_z_index(8))
        raio_b = always_redraw(lambda: Line(centro_zoom - rb * k * direcao(), centro_zoom,
                                           color=CIANO, stroke_width=3).set_z_index(6))
        self.add(zoom_terra, raio_b, zoom_centro, zoom_b)
        self.add(texto('Ampliação da região terrestre', 24, SUAVE).move_to([3.4, 2.2, 0]))
        self.add(texto('baricentro', 26, CIANO).move_to([4.45, .65, 0]))
        self.add(equacao(r'4{,}67\times10^6\,\mathrm m\approx0{,}733R_{\mathrm T}', 33,
                         largura=6.5).move_to([3.65, -1.9, 0]))
        self.play(fase.animate.set_value(1.05), run_time=4, rate_func=linear)
        self.marco('N17_baricentro_dentro_terra')
        self.wait(2)
        self.play(fase.animate.set_value(2*math.pi), run_time=12, rate_func=linear)
        self.play(FadeIn(self.nota('Terra e Lua caem uma em direção à outra\ne orbitam um ponto comum.',
                                  -2.65, BRANCO, 27)))
        self.wait(4)

    def n18(self):
        self.abre(18, 'Uma queda que nunca termina')
        nomes = VGroup(*[texto(s, 29, SUAVE) for s in ('pedra', 'satélite', 'Lua')]).arrange(RIGHT, buff=1.5)
        nomes.move_to([0, 1.6, 0])
        icones = VGroup(Dot(nomes[0].get_center() + .8 * DOWN, .12, color=SUAVE),
                        satelite(nomes[1].get_center() + .8 * DOWN, .38),
                        Circle(radius=.23, color=SUAVE, fill_color='#8195AB', fill_opacity=1)
                        .move_to(nomes[2].get_center() + .8 * DOWN))
        self.play(FadeIn(nomes), FadeIn(icones))
        self.wait(2)
        self.play(FadeOut(nomes), FadeOut(icones), FadeOut(self.cabecalho), run_time=1.2)
        c = np.array([-3.25, -.1, 0])
        orb, t, pos, vel, terra, trilha, bola = self.circular(c, 1.75)
        frase1 = texto('Orbitar não é\nvencer a gravidade.', 37,
                       largura=6.8).move_to([3.4, .5, 0])
        frase2 = texto('É cair…\ne continuar errando o chão.', 37, CIANO,
                       largura=6.8).move_to([3.4, .35, 0])
        self.play(FadeIn(frase1), t.animate.set_value(.35 * orb.t[-1]), run_time=4, rate_func=linear)
        self.wait(3)
        self.play(FadeOut(frase1), run_time=.8)
        self.play(FadeIn(frase2), t.animate.set_value(.8 * orb.t[-1]), run_time=5, rate_func=linear)
        self.marco('N18_fechamento')
        # Retira overlays editoriais gradualmente; ficam marca, Terra e órbita.
        textos_topo = [m for m in self.mobjects if m.get_center()[1] > 3.4 and m is not self.wm]
        if textos_topo:
            self.play(*[FadeOut(m) for m in textos_topo], run_time=1)
        self.wait(5)
