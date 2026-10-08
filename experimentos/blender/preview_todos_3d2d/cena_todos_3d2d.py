"""Os casos de Gauss no padrão 3D + corte 2D ampliado (sandbox, fora do yt_0002): 3D do Blender permanente, texto da região e corte 2D sincronizados.

Mesma estrutura do coaxial 3D+2D aprovado. O quadro k (30 fps) mostra a imagem do Blender para p(k) (traj_gen.py); o texto e o corte 2D usam o MESMO p(k).
Corte 2D: radial (cilindros e esferas: seção transversal) ou lateral (casos planares: vista de lado), com a fonte, o campo existente (setas discretas e fixas),
a gaussiana animada e, onde E ≠ 0, as setas do campo avaliado na gaussiana (comprimento ∝ |E|, regras em campo_aval.py, as mesmas do Blender). Sem gráfico.

    uv run python -m manim -r 960,540 --fps 30 --media_dir media/preview_todos_3d2d/<caso> experimentos/blender/preview_todos_3d2d/cena_todos_3d2d.py <Classe>
Classes: Linha3D2D CascaCil3D2D MacicoCil3D2D Folha3D2D Placa3D2D Duas3D2D Face3D2D CascaEsf3D2D MacicoEsf3D2D CapEsf3D2D
"""

import sys
from collections import OrderedDict
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, Annulus, Arrow, Circle, DashedLine, DashedVMobject, FadeIn, FadeOut, ImageMobject, Line, Rectangle, Scene, VGroup, always_redraw, config,
)
from PIL import Image

HERE = Path(__file__).resolve().parent
RAIZ = HERE.parents[2]
for extra in (HERE, HERE.parent / "preview_todos_limpo", HERE.parent / "teste_gauss_coaxial"):
    sys.path.insert(0, str(extra))
import campo_aval as CA  # noqa: E402
from cena_manim import BACKGROUND_COLOR, BLUE_L, CYAN, VIOLET, WHITE, P, eq, text  # noqa: E402  (helpers da v1 do coaxial; ela não é alterada)
from cena_todos import RL, UI, XMAX, encaixa, linha  # noqa: E402  (texto por caso do preview limpo)
from traj_gen import CASOS, FPS, Traj  # noqa: E402

MAG = "#EA63FF"
PASTA = RAIZ / "renders" / "preview_todos_3d2d"
C = P(5.2, -2.65)                                       # centro do corte
U = lambda g: P(np.cos(np.radians(g)), np.sin(np.radians(g)))      # noqa: E731

# fontes e marcas do corte radial: ("ponto") | ("disco", R, [símbolo +]) | ("anel", R) | ("casca", R) (− na face interna)
CORTE = {
    "linha": dict(t="rad", fontes=[("ponto",)], est=(0.55, 0.45), marcas=[]),
    "casca_cil": dict(t="rad", fontes=[("anel", 1.0)], est=(1.15, 0.42), marcas=[("R", 1.0, 140, BLUE_L)]),
    "macico_cil": dict(t="rad", fontes=[("disco", 1.0)], est=(1.15, 0.42), marcas=[("R", 1.0, 140, BLUE_L)]),
    "casca_esf": dict(t="rad", fontes=[("anel", 1.0)], est=(1.15, 0.42), marcas=[("R", 1.0, 140, BLUE_L)]),
    "macico_esf": dict(t="rad", fontes=[("disco", 1.0)], est=(1.15, 0.42), marcas=[("R", 1.0, 140, BLUE_L)]),
    "cap_esf": dict(t="rad", fontes=[("disco", 0.8), ("casca", 1.6)], est=(0.92, 0.36), marcas=[("a", 0.8, 90, BLUE_L), ("b", 1.6, 140, MAG)]),
    # planares: barras = (x, meia-largura, cor, sinal) ; pillbox(p) → (xl, xr) ; est = [(x0, direção, comprimento)] dos dois lados (campo existente)
    "folha": dict(t="lat", barras=[(0.0, 0.03, BLUE_L, "+")], pill=lambda p: (-p, p), caps="ambas", est=[(0.3, 1, 1.0), (-0.3, -1, 1.0)], rot=[(0.0, "+\\sigma", BLUE_L)]),
    "placa": dict(t="lat", barras=[(0.0, 0.7, BLUE_L, "+")], pill=lambda p: (-p, p), caps="ambas", est=[(0.82, 1, 0.9), (-0.82, -1, 0.9)], rot=[(0.7, "a", BLUE_L), (-0.7, "-a", BLUE_L)]),
    "duas": dict(t="lat", barras=[(-1.1, 0.03, BLUE_L, "+"), (1.1, 0.03, MAG, "-")], pill=lambda p: (-1.9, max(p, -1.72)), caps="direita", est=[(-0.8, 1, 1.5)],
                 rot=[(-1.1, "+\\sigma", BLUE_L), (1.1, "-\\sigma", MAG)]),
    "face": dict(t="lat", barras=[(-0.85, 0.85, "#26345A", None), (0.0, 0.03, BLUE_L, "+")], pill=lambda p: (-0.75, p), caps="direita", est=[(0.25, 1, 0.9)], rot=[]),
}


def sinal(txt, cor, pos, s_=0.085):
    """Marcador esquemático de carga (+ ou −): traços sobre um disco do fundo; não é uma contagem de cargas."""
    fundo = Circle(radius=s_ * 1.6).move_to(pos).set_stroke(width=0).set_fill(BACKGROUND_COLOR, 0.9)
    tr = [Line(pos + P(-s_, 0), pos + P(s_, 0)).set_stroke(cor, 4)]
    if txt == "+":
        tr.append(Line(pos + P(0, -s_), pos + P(0, s_)).set_stroke(cor, 4))
    return VGroup(fundo, *tr).set_z_index(8)


def seta(a, b, op=1.0, w=4, tip=0.15):
    return Arrow(a, b, buff=0, stroke_width=w, tip_length=tip, color=CYAN).set_stroke(opacity=op)


class CasoBase3D2D(Scene):
    CID = None

    def construct(self):
        assert config.frame_rate == FPS, f"use --fps {FPS}"
        cid = self.CID
        ui, T, cut = UI[cid], Traj(CASOS[cid]["wps"]), CORTE[cid]
        pmax = max(p for p, _ in CASOS[cid]["wps"])
        pasta = PASTA / cid / "1120x784"
        self.camera.background_color = BACKGROUND_COLOR
        cache, estado = OrderedDict(), {"t0": 0.0, "k": 0}

        def k_atual():
            return min(max(int(round((self.time - estado["t0"]) * FPS)), 0), T.total - 1)

        def p_atual():
            return T.p_em_quadro(k_atual())              # None na introdução (sem gaussiana)

        def ativo():
            p = p_atual()
            return p is not None and CA.ativo(cid, p) and CA.comp(cid, p) >= CA.MIN

        def dim():
            """0 → 1: o campo existente fica discreto na medida em que o avaliado aparece (mesma rampa do Blender)."""
            p = p_atual()
            return 0.0 if p is None or not CA.ativo(cid, p) else CA.fator(cid, p)

        def quadro(k):
            nome = pasta / f"q_{T.chave(k)}.png"
            if nome not in cache:
                cache[nome] = np.array(Image.open(nome).convert("RGBA"))
                while len(cache) > 24:
                    cache.popitem(last=False)
            return cache[nome]

        img = ImageMobject(quadro(0)).set_width(9.0).move_to(P(-3.0, -0.15))
        img.set_opacity(0.0)

        # ── texto por região (o mesmo do preview limpo) ────────────────────
        regs = []
        for reg in ui["regs"]:
            cond, dom, q, e, nota = reg[:5]
            esq = reg[5] if len(reg) > 5 else "E"
            d = eq(dom, size=34, color=VIOLET).move_to(P(0, 1.55)).align_to(P(RL, 0), LEFT)
            qq = eq(q, size=40).move_to(P(0, 1.55)).align_to(P(max(RL + 1.85, d.get_right()[0] + 0.4), 0), LEFT)
            l1 = VGroup(d, qq)
            if l1.get_right()[0] > XMAX:
                l1.scale((XMAX - RL) / (l1.get_right()[0] - RL), about_point=P(RL, 1.55))
            ee = eq(esq, "=0", size=50, colors={0: CYAN}) if e is None else eq(esq, "=", e, size=50, colors={0: CYAN})
            nt = text(nota, 22, WHITE, 0.92)
            regs.append((cond, VGroup(l1, encaixa(ee.move_to(P(0, 0.4)), RL), encaixa(nt.move_to(P(0, -0.55)), RL))))
        titulo = encaixa(linha(ui["titulo"]).move_to(P(0, 2.9)), RL)

        # ── corte 2D ampliado ──────────────────────────────────────────────
        estatico, dinamico, desvanece = VGroup(), [], []
        if cut["t"] == "rad":
            K = 1.7 / pmax
            for f in cut["fontes"]:
                if f[0] == "ponto":
                    estatico.add(Circle(radius=0.09).move_to(C).set_stroke(BLUE_L, 2).set_fill(BLUE_L, 1), sinal("+", BLUE_L, C + 0.0 * U(0)))
                elif f[0] == "disco":
                    estatico.add(Circle(radius=K * f[1]).move_to(C).set_stroke(BLUE_L, 3).set_fill("#1B4DB5", 0.5))
                    nsy = 6 if f[1] >= 0.9 else 8
                    for i in range(nsy):
                        estatico.add(sinal("+", BLUE_L, C + K * f[1] * (0.7 if i % 2 else 0.4) * U(60 * i + (20 if i % 2 else 0))) if f[1] >= 0.9
                                     else sinal("+", BLUE_L, C + K * f[1] * U(45 * i)))
                elif f[0] == "anel":
                    estatico.add(Circle(radius=K * f[1]).move_to(C).set_stroke(BLUE_L, 5))
                    estatico.add(*[sinal("+", BLUE_L, C + (K * f[1] + 0.17) * U(45 * i)) for i in range(8)])
                elif f[0] == "casca":
                    estatico.add(Circle(radius=K * f[1]).move_to(C).set_stroke(BLUE_L, 5))
                    estatico.add(*[sinal("-", MAG, C + (K * f[1] - 0.16) * U(45 * i + 22.5)) for i in range(8)])
            for nome, raio, ang, cor in cut["marcas"]:
                estatico.add(Line(C + K * raio * 0.12 * U(ang), C + K * raio * U(ang)).set_stroke(cor, 2, 0.9),
                             eq(nome, size=30, color=cor).move_to(C + (K * raio + 0.24) * U(ang)))
            r0, ln = cut["est"]
            existente = VGroup(*[seta(C + K * r0 * U(22.5 + 45 * i), C + K * (r0 + ln) * U(22.5 + 45 * i), w=3.5, tip=0.16) for i in range(8)])
            if cid in ("linha", "casca_cil", "macico_cil"):                       # cilindros: com as coroas ativas, só elas (o campo existente de dentro some, como no 3D)
                existente.add_updater(lambda m: m.set_stroke(opacity=0.0 if dim() > 0.02 else 0.95))
            else:
                existente.add_updater(lambda m: m.set_stroke(opacity=0.95 - 0.6 * dim()))
            if cid == "cap_esf":
                vao = Annulus(inner_radius=K * 0.8, outer_radius=K * 1.6).move_to(C).set_stroke(width=0).set_fill(CYAN, 0.0)
                vao.add_updater(lambda m: m.set_fill(CYAN, 0.08 if ativo() else 0.0))
                desvanece.append(vao)
            else:
                vao = None

            def gauss():
                p = p_atual()
                if p is None:
                    return VGroup()
                g = VGroup(Circle(radius=K * p).move_to(C).set_stroke(width=0).set_fill(VIOLET, 0.06),
                           DashedVMobject(Circle(radius=K * p).move_to(C), num_dashes=56, dashed_ratio=0.55).set_stroke(VIOLET, 4, 0.95),
                           DashedLine(C, C + K * p * U(-35), dash_length=0.07).set_stroke(VIOLET, 2.5, 0.95),
                           eq("r", size=32, color=VIOLET).move_to(C + K * p * 0.5 * U(-35) + 0.24 * U(-125)))
                k = CA.comp_vis(cid, p)
                if k > 0:
                    ln = K * k * (1.6 if cid == "cap_esf" else 1.0)                    # no vão estreito do capacitor, setas ampliadas p/ leitura
                    g.add(*[seta(C + K * p * U(30 * i + 15), C + K * p * U(30 * i + 15) + ln * U(30 * i + 15), tip=min(0.15, 0.5 * ln)) for i in range(12)])
                return g.set_z_index(6)
        else:
            ks = 0.85
            P2 = lambda x, y: C + P(x * ks, y)                                  # noqa: E731
            for x, hw, cor, sg in cut["barras"]:
                if hw < 0.1:
                    estatico.add(Line(P2(x, -1.3), P2(x, 1.3)).set_stroke(cor, 5))
                else:
                    estatico.add(Rectangle(width=2 * hw * ks, height=2.6).move_to(P2(x, 0)).set_stroke(BLUE_L, 3).set_fill("#1B4DB5" if cor != "#26345A" else "#26345A", 0.4))
                if sg:
                    lado = 0.0 if hw < 0.1 else hw * 0.6
                    estatico.add(*[sinal(sg, cor, P2(x + (0.0 if hw < 0.1 else lado * (-1) ** i), y), 0.075) for i, y in enumerate((-0.9, -0.45, 0.0, 0.45, 0.9))])
            for x, nome, cor in cut["rot"]:
                estatico.add(eq(nome, size=28, color=cor).move_to(P2(x, 1.55)))
            existente = VGroup(*[seta(P2(x0, y), P2(x0 + d * ln, y), w=3.5, tip=0.16) for x0, d, ln in cut["est"] for y in (-1.05, 1.05)])
            existente.add_updater(lambda m: m.set_stroke(opacity=0.95 - 0.6 * dim()))
            vao = None

            def gauss():
                p = p_atual()
                if p is None:
                    return VGroup()
                xl, xr = cut["pill"](p)
                w = max((xr - xl) * ks, 0.04)
                ret = Rectangle(width=w, height=1.8).move_to(C + P((xl + xr) / 2 * ks, 0))
                g = VGroup(ret.copy().set_stroke(width=0).set_fill(VIOLET, 0.07),
                           DashedVMobject(ret, num_dashes=50, dashed_ratio=0.55).set_stroke(VIOLET, 3.5, 0.95),
                           Line(P2(xr, -0.9), P2(xr, 0.9)).set_stroke(VIOLET, 5, 0.95))
                k = CA.comp_vis(cid, p)
                if k > 0:
                    for y in (-0.4, 0.0, 0.4):
                        g.add(seta(P2(xr, y), P2(xr + k, y), tip=min(0.15, 0.5 * k)))
                        if cut["caps"] == "ambas":
                            g.add(seta(P2(xl, y), P2(xl - k, y), tip=min(0.15, 0.5 * k)))
                return g.set_z_index(6)
        gauss_mob = always_redraw(gauss)

        def atualiza(m, dt=0):
            k = k_atual()
            if k != estado["k"] or m.stroke_opacity < 1:
                estado["k"] = k
                arr = quadro(k)
                m.pixel_array = arr.copy()
                m.orig_alpha_pixel_array = arr[:, :, 3]
                if m.stroke_opacity < 1:
                    m.pixel_array[:, :, 3] = (arr[:, :, 3] * m.stroke_opacity).astype(m.pixel_array.dtype)
            p = p_atual()
            for cond, g in regs:
                g.set_opacity(0.0 if p is None else (1.0 if cond(p) else 0.0))

        img.add_updater(atualiza)
        for _, g in regs:
            g.set_opacity(0.0)
        self.add(img, *desvanece, *[g for _, g in regs])
        self.play(img.animate.set_opacity(1.0), FadeIn(titulo), FadeIn(estatico), FadeIn(existente), run_time=0.8)
        self.add(gauss_mob)
        estado["t0"] = self.time
        self.wait(T.total / FPS)
        img.remove_updater(atualiza)
        for m in (gauss_mob, existente, *desvanece):
            m.clear_updaters()
        self.play(FadeOut(VGroup(titulo, estatico, existente, gauss_mob, *desvanece, *[g for _, g in regs])), img.animate.set_opacity(0.0), run_time=0.6)


class Linha3D2D(CasoBase3D2D):
    CID = "linha"


class CascaCil3D2D(CasoBase3D2D):
    CID = "casca_cil"


class MacicoCil3D2D(CasoBase3D2D):
    CID = "macico_cil"


class Folha3D2D(CasoBase3D2D):
    CID = "folha"


class Placa3D2D(CasoBase3D2D):
    CID = "placa"


class Duas3D2D(CasoBase3D2D):
    CID = "duas"


class Face3D2D(CasoBase3D2D):
    CID = "face"


class CascaEsf3D2D(CasoBase3D2D):
    CID = "casca_esf"


class MacicoEsf3D2D(CasoBase3D2D):
    CID = "macico_esf"


class CapEsf3D2D(CasoBase3D2D):
    CID = "cap_esf"
