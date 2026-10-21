"""Geometria 2.5D do 5.3 (mixin da cena). Convenção: tau < 0 = vista de CIMA (projeção destra; depth() = proximidade).

Laço orientado: o sentido de percurso segue a mão direita em torno da normal (fisica.basis).
"""
import math

import numpy as np
from manim import VGroup, VMobject, Polygon, ParametricFunction, Line, DashedLine, Dot, DashedVMobject

from base import *  # noqa: F401,F403
from fisica import basis, TAU


class Geo:
    def view_to(self, x, y, s, rt=1.4, **more):
        """Move a vista (origem, escala e, opcionalmente, beta/tau)."""
        anims = [self.ox.animate.set_value(x), self.oy.animate.set_value(y), self.gs.animate.set_value(s)]
        anims += [getattr(self, k).animate.set_value(v) for k, v in more.items()]
        self.play(*anims, run_time=rt)

    # ── primitivas ───────────────────────────────────────────────────────────────────────────────────────────
    def circ_pts(self, c, rho, n, N=64, t0=0.0, t1=TAU):
        u, v = basis(n)
        c = np.asarray(c, dtype=float)
        return [c + rho * (math.cos(t) * u + math.sin(t) * v) for t in np.linspace(t0, t1, N)]

    def curve(self, pts, color=WHITE, width=3, op=1.0, z=5, dashed=False):
        m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=op).set_points_smoothly([self.W(p) for p in pts])
        if dashed:
            m = DashedVMobject(m, num_dashes=max(8, int(len(pts) / 2)), dashed_ratio=0.55)
        return m.set_z_index(z)

    def poly(self, pts, color=VIOLET, op=0.25, z=1, stroke=0):
        return Polygon(*[self.W(p) for p in pts], stroke_width=stroke, stroke_color=color).set_fill(color, op).set_z_index(z)

    def tips(self, pts_fn, ts, color, size=0.2, width=4, z=6, sign=1):
        """Pontas de seta ao longo de uma curva paramétrica (sentido de percurso)."""
        g = VGroup()
        for t in ts:
            a, b = self.W(pts_fn(t - 0.03 * sign)), self.W(pts_fn(t + 0.03 * sign))
            g.add(arrow(a, b, color, width, z=z, tip=size))
        return g

    def path3d(self, P, t0, t1, c, color=WHITE, width=4, op=1.0, z=6, N=97, dashed=False):
        """Curva P(t) com a parte de trás (depth < depth(c)) mais apagada e abaixo; poucas VMobjects por curva."""
        ts = np.linspace(t0, t1, N)
        c = np.asarray(c, dtype=float)
        g, run, flag = VGroup(), [], None

        def close(run, back):
            if len(run) > 1:
                m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=op * (0.42 if back else 1.0))
                m.set_points_as_corners([self.W(p) for p in run])
                if dashed:
                    m = DashedVMobject(m, num_dashes=max(2, len(run) // 3), dashed_ratio=0.55)
                g.add(m.set_z_index(z - 3 if back else z))
        for t in ts:
            p = P(t)
            back = self.depth(p - c) < -1e-9
            if flag is None or back == flag:
                run.append(p)
            else:
                run.append(p)
                close(run, flag)
                run = [p]
            flag = back
        close(run, flag)
        return g

    def arrowhead(self, p, d, size=0.3, color=MAG, z=8, op=1.0):
        """Ponta de seta triangular de tamanho FIXO na tela (p, d em coordenadas de tela). As pontas via Arrow ficavam
        limitadas a 35% de um segmento minúsculo e sumiam (V1)."""
        d = np.asarray(d, dtype=float)
        nd = np.linalg.norm(d[:2])
        if nd < 1e-9:
            return VMobject()
        d = d / nd
        nrm = np.array([-d[1], d[0], 0.0])
        p = np.asarray(p, dtype=float)
        tri = Polygon(p + 0.55 * size * d, p - 0.45 * size * d + 0.42 * size * nrm, p - 0.45 * size * d - 0.42 * size * nrm, stroke_width=0)
        return tri.set_fill(color, op).set_z_index(z)

    def loop3d(self, c, rho, n, color=WHITE, width=4, fill=0.0, fill_color=None, arrows=3, dashed=False, tip=0.2, z=6, op=1.0, t0=None,
               heads=False):
        """Laço orientado (mão direita em torno de n). Metade de trás mais apagada.
        t0: parâmetro da primeira ponta (t=0 é o ponto c + rho·u; para n=+y, u=ẑ = frente). heads=True usa pontas triangulares."""
        u, v = basis(n)
        c = np.asarray(c, dtype=float)
        P = lambda t: c + rho * (math.cos(t) * u + math.sin(t) * v)
        g = VGroup()
        if fill > 0:
            g.add(self.poly([P(t) for t in np.linspace(0, TAU, 72)], fill_color or color, fill, z=z - 4))
        g.add(self.path3d(P, 0, TAU, c, color, width, op, z, dashed=dashed))
        if arrows:
            ts = [(t0 if t0 is not None else TAU * 0.25 / arrows) + TAU * k / arrows for k in range(arrows)]
            if heads:
                for t in ts:
                    a, b = self.W(P(t - 0.02)), self.W(P(t + 0.02))
                    back = self.depth(P(t) - c) < -1e-9
                    g.add(self.arrowhead(self.W(P(t)), b - a, tip, color, z=(z - 2 if back else z + 2), op=op * (0.5 if back else 1.0)))
            else:
                g.add(self.tips(P, ts, color, tip, width, z + 1).set_opacity(op))
        return g

    def disk3d(self, c, rho, n, color=VIOLET, op=0.22, inner=0.0, N=72, z=1):
        """Disco (ou coroa, inner>0) no plano ⟂ n: superfície que pode nascer da borda (inner: rho → 0)."""
        out = self.circ_pts(c, rho, n, N)
        if inner <= 1e-4:
            return self.poly(out, color, op, z)
        inn = self.circ_pts(c, inner, n, N)[::-1]
        return self.poly(out + inn, color, op, z)

    def ring_y(self, r, h=0.0, color=MAG, width=3.2, op=0.9, arrows=2, cx=0.0, cz=0.0, sign=1, tip=0.28):
        """Linha de B em torno do eixo y (fio): círculo horizontal, sentido +φ (mão direita em torno de +y).
        Pontas triangulares na frente e atrás (onde a tangente é horizontal na tela, sem encurtamento)."""
        return self.loop3d([cx, h, cz], r, [0, sign, 0], color, width, arrows=arrows, tip=tip, z=5, op=op, t0=0.75, heads=True)

    def wire_y(self, y0=-2.2, y1=2.2, x=0.0, z=0.0, color=STEEL, width=LW_WIRE):
        return self.tube(self.W([x, y0, z]), self.W([x, y1, z]), color, width)

    def flow_y(self, y0=-2.2, y1=2.2, x=0.0, z=0.0, count=7, sign=1):
        return self.flow([lambda u: self.W([x, y0 + (y1 - y0) * u, z])], count=count, direction=sign)

    def b_arrows_fio(self, radii, h=0.0, k=0.9, angs=(-90,), color=MAG, width=5, I=1.0):
        """Vetores B = I/(2π s) φ̂ em pontos do plano y=h; comprimento ∝ 1/s (escala k)."""
        g = VGroup()
        for r in radii:
            for a in angs:
                t = math.radians(a)
                p = np.array([r * math.cos(t), h, r * math.sin(t)])
                ph = np.array([math.sin(t), 0.0, -math.cos(t)])      # φ̂ = ŷ × ŝ
                g.add(self.vec(p, ph, color, scale=k * I / (TAU * r) * TAU / 2.6, width=width, tip=0.2))
        return g

    def normal(self, c, n, L=0.9, color=WHITE, width=4):
        n = np.asarray(n, dtype=float)
        return self.vec(np.asarray(c, dtype=float), n / np.linalg.norm(n), color, scale=L, width=width, tip=0.2)

    def box3d(self, c, h, color=WHITE, op=0.12, width=2.2):
        """Cubo de lado 2h (aresta + faces translúcidas)."""
        c = np.asarray(c, dtype=float)
        V = [c + h * np.array([sx, sy, sz]) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
        faces = [(0, 1, 3, 2), (4, 5, 7, 6), (0, 1, 5, 4), (2, 3, 7, 6), (0, 2, 6, 4), (1, 3, 7, 5)]
        g = VGroup(*[self.poly([V[i] for i in f], color, op, z=2) for f in faces])
        for i in range(8):
            for j in range(i + 1, 8):
                if bin(i ^ j).count("1") == 1:
                    g.add(Line(self.W(V[i]), self.W(V[j]), color=color, stroke_width=width).set_z_index(6))
        return g

    def pin(self, mob, fn):
        """Rótulo/objeto preso a um ponto de tela que muda com a vista."""
        mob.add_updater(lambda m: m.move_to(fn()))
        mob.update(0)
        return mob

    # ── estratégia de Ampère (N16–N20): barra de passos que acende ───────────────────────────────────────────
    def strategy_bar(self, y=2.72):
        items = [("simetria", None), ("direção de", r"\mathbf B"), ("caminho", None), (None, r"\mathbf B\cdot d\boldsymbol\ell"),
                 (None, r"I_{\rm env}")]
        steps = VGroup()
        for t, m in items:
            g = VGroup()
            if t:
                g.add(txt(t, 22))
            if m:
                g.add(E(m, m, size=28))
            g.arrange(RIGHT, buff=0.12)
            steps.add(g)
        row = VGroup()
        for i, s in enumerate(steps):
            row.add(s)
            if i < len(steps) - 1:
                row.add(E(r"\rightarrow", size=26).set_opacity(0.6))
        row.arrange(RIGHT, buff=0.22).move_to([0, y, 0])
        for s in steps:
            s.set_opacity(0.35)
        row.steps = steps
        return row

    def light(self, bar, i, rt=0.5):
        anims = []
        for k, s in enumerate(bar.steps):
            anims.append(s.animate.set_opacity(1.0 if k == i else (0.75 if k < i else 0.35)))
        self.play(*anims, run_time=rt)
