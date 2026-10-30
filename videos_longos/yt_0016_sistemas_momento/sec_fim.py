"""Lote PS (v3): síntese e encerramento. S1: o cavalo 3D com a fronteira e as forças (corda no arreio e na pedra, cinza; chão abaixo
da linha do chão). S2 em PALCO + CONTA: o cavalo grande andando com a fronteira no PALCO; na CONTA as três ideias, uma por vez, cada uma
com o seu ícone (esferas · blocos · blocos + Terra); na terceira a fronteira cresce até incluir o chão (+ TERRA). EN1 inscreva-se;
EN2 granada → centro de massa."""
import json

from kit import *  # noqa: F401,F403
from sec_cavalo import Cavalo3D



# ── v7 (final): a granada 3D do yt_0017 (threejs/cena3d/gra17: campo.js + cm3d.js, cena 'gra', copiados do main) ──────────────
# Campo de provas em vácuo: (30; 40) m/s, explode no topo em três cacos do próprio corpo (2, 1 e 1,5 kg; 90°, 210°, 330°; momento
# relativo 30 kg·m/s). A física e o estado são os do Granada3D do yt_0017 (pecas3d.py), reduzidos ao que o EN2 usa.
MED17 = json.loads((AQUI / "threejs" / "cena3d" / "gra17" / "granada_medidas.json").read_text(encoding="utf-8"))
MS17 = (2.0, 1.0, 1.5)
MT17 = sum(MS17)
DIRS17 = [np.array([math.cos(math.radians(a)), math.sin(math.radians(a))]) for a in (90, 210, 330)]
OMEGA17 = [2 * PI * w for w in (0.9, 1.7, 1.3)]


def _suave(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def _r4(d):
    if isinstance(d, dict):
        return {k: _r4(v) for k, v in d.items()}
    if isinstance(d, (list, tuple)):
        return [_r4(v) for v in d]
    return round(d, 4) if isinstance(d, float) else d


class Granada17:
    S, G, PRE, R_TELA = 20.0, 9.8, 30.0, 0.42          # granada maior que no yt_0017 (aqui ela é o assunto do quadro)
    V0 = np.array([30.0, 40.0])
    TE = 40.0 / 9.8

    def __init__(self, cena, cam):
        self.cena, self.camd = cena, cam
        self.tau = ValueTracker(0.0)
        self.pe = self.V0 * self.TE + np.array([0, -0.5 * self.G * self.TE ** 2])
        self.vf = [np.array([self.V0[0], 0.0]) + d * self.PRE / m for m, d in zip(MS17, DIRS17)]
        self.ttoque = [self._toque(v) for v in self.vf]
        self.f3d = Fundo3D(cena, "gra17/gra", self.estado, op=0.0)

    def _toque(self, v):
        a, b, c = -0.5 * self.G, v[1], self.pe[1]
        return self.TE + (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)

    def ideal(self, tau):
        return self.V0 * tau + np.array([0.0, -0.5 * self.G * tau * tau])

    def frags(self, tau):
        out = []
        for v, tt in zip(self.vf, self.ttoque):
            s = min(tau, tt) - self.TE
            out.append(self.pe + v * s + np.array([0, -0.5 * self.G * s * s]))
        return out

    def cm(self, tau):
        if tau < self.TE:
            return self.ideal(tau)
        return sum(m * q for m, q in zip(MS17, self.frags(tau))) / MT17

    def ang(self, k, tau):
        dx, dp = tau - self.TE, self.ttoque[k] - self.TE
        if dx <= 0:
            return 0.0
        if dx <= dp:
            return OMEGA17[k] * dx
        return OMEGA17[k] * dp + OMEGA17[k] / 5.0 * (1 - math.exp(-5.0 * (dx - dp)))

    def estado(self, t):
        tau = self.tau.get_value()
        dx = tau - self.TE
        esc = self.R_TELA / (self.camd["K"] * MED17["req_corpo"])
        onda = -1.0 if tau < self.TE - 0.2 else min(1.25, -1.0 + 2.25 * (tau - self.TE + 0.2) / 0.2)
        gr = {"esc": esc, "chao": 1, "marco": math.exp(-((tau - 0.3) / 0.15) ** 2), "onda": onda,
              "brilho": 2.2 * (math.exp(-dx / 0.3) if dx > 0 else 1.0)}
        if tau < self.TE:
            q = self.ideal(tau)
            gr.update(cen=[q[0] / self.S, q[1] / self.S], deco=1)
        else:
            gr.update(frags=[[q[0] / self.S, q[1] / self.S, self.ang(k, tau), _suave(dx / 0.25) if dx > 0 else 0.0]
                             for k, q in enumerate(self.frags(tau))],
                      dx=dx, pe=[self.pe[0] / self.S, self.pe[1] / self.S], vpe=[self.V0[0] / self.S, 0.0], calor=math.exp(-dx / 0.35))
        return _r4({"gr": gr, "cam": self.camd, "tau": tau})

    def m(self, q):
        return proj3d(self.camd, (q[0] / self.S, 0.0, q[1] / self.S))


class LoteFim(Base):
    def construct(self):
        self.setup_base(cap="RESUMO")
        self.sintese()
        self.cta()
        self.fim()
        self.relatorio()

    def sintese(self):
        self.an("S1")
        cv = self.cv = Cavalo3D(self, v=lambda t: 0.42, K=0.95, xt=2.1, yc=-2.4, op=0.0)
        self.add(cv.f3d)
        self.play(cv.f3d.op.animate.set_value(1.0), run_time=1.0)
        terra = ValueTracker(0.0)          # 1 = a fronteira inclui o chão

        def front():
            p = cv.pts()
            u = terra.get_value()
            xl, xr = p["pedra_tras"][0] - 0.3, p["cabeca"][0] + 0.35
            y0, y1 = p["cascos"][1] - 0.15, p["topo"][1] + 0.22
            xl, xr, y0 = xl + (PALCO_X[0] + 0.15 - xl) * u, xr + (PALCO_X[1] - 0.15 - xr) * u, y0 + (PALCO_Y[0] + 0.15 - y0) * u
            r = RoundedRectangle(corner_radius=0.3, width=xr - xl, height=y1 - y0).move_to(P3((xl + xr) / 2, (y0 + y1) / 2))
            r.set_stroke(WHITE_, 2.2, opacity=0.62)
            g = VGroup(DashedVMobject(r, num_dashes=int((xr - xl + y1 - y0) * 5), dashed_ratio=0.55).set_z_index(1),
                       mtxt("SISTEMA", 16, op=0.8).next_to(r.get_corner(UL), UP, buff=0.1).align_to(r, LEFT).shift(0.25 * RIGHT))
            if u > 0.01:
                g.add(mtxt("+ TERRA", 18, color=GEO, op=0.9 * u).move_to(P3(xl + 0.9, y0 + 0.3)))
            return g
        fr = always_redraw(front)
        tens = ValueTracker(0.0)
        ext = ValueTracker(0.0)
        rot_t = ValueTracker(0.0)          # v6 (1.2): 0 = T⃗ e −T⃗; 1 = INTERNA

        def forcas():
            p = cv.pts()
            g = VGroup()
            if tens.get_value() > 0.01:
                if rot_t.get_value() < 0.5:
                    ts = cv.setas_corda(mix(INT, 0.45), mix(INT, 0.45), L=1.1, w=7, lab_a=r"-\vec T", lab_b=r"\vec T", size=30, cor_lab=mix(INT, 0.5))
                else:
                    ts = cv.setas_corda(INT, INT, L=1.35, w=6, lab_a=mtxt("INTERNA", 15, color=INT))
                g.add(escala_op(ts, tens.get_value()))
            if ext.get_value() > 0.01:
                yb = p["cascos"][1] - 0.42
                e = VGroup(arrow(P3(p["cascos"][0] - 0.2, yb), P3(p["cascos"][0] + 1.4, yb), color=FC, width=7, tip=0.2, z=12),
                           arrow(P3(p["pedra_base"][0] + 0.2, yb), P3(p["pedra_base"][0] - 0.98, yb), color=FC, width=7, tip=0.2, z=12))
                e.add(mtxt("CHÃO NAS PATAS", 15, color=FC).next_to(e[0], DOWN, buff=0.1),
                      mtxt("CHÃO NA PEDRA", 15, color=FC).next_to(e[1], DOWN, buff=0.1))
                g.add(escala_op(e, ext.get_value()))
            return g
        fz = always_redraw(forcas)
        self.add(fz)
        self.diz("A corda puxa, sim")
        self.play(tens.animate.set_value(1.0), run_time=0.6)
        self.wait(1.6)
        rot_t.set_value(1.0)
        self.diz("no sistema cavalo, corda e pedra")
        self.play(FadeIn(fr), run_time=1.0)
        self.diz("Quem acelera o cavalo")
        self.play(ext.animate.set_value(1.0), run_time=0.6)
        r = txt("QUEM ACELERA O CAVALO E A PEDRA É O CHÃO", 26, bold=True).move_to(P3(0, 2.3))
        self.diz("é o chão")
        self.play(FadeIn(r, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        # S2 — PALCO + CONTA: o cavalo grande vai para o PALCO; as três ideias entram na CONTA, uma por vez, com o ícone à esquerda
        self.an("S2")
        fz.clear_updaters()
        self.play(FadeOut(fz), FadeOut(r), cv.K.animate.set_value(0.85), cv.xt.animate.set_value(-0.75), cv.yc.animate.set_value(-2.3),
                  cv.f3d.conta.animate.set_value(1.0), run_time=1.2)      # v4: o chão 3D não passa atrás da CONTA
        self.remove(fz)
        t0 = self.clk.get_value()
        XI, XT = XC0 + 0.45, XC0 + 1.3        # centro do ícone · começo do texto (folga entre os dois)

        def esferas(c):
            def f():
                a = math.sin(2 * PI * (self.clk.get_value() - t0) / 2.4)
                ps = [c + P3(-0.34 - 0.03 * a, -0.22), c + P3(0.34 + 0.03 * a, -0.22), c + P3(0, 0.3 - 0.04 * a)]
                g = VGroup(*[mola(ps[i], ps[j], n=4, amp=0.05, cor=FC, w=2) for i, j in ((0, 1), (0, 2), (1, 2))])
                g.add(*[bola(0.12, GEO).move_to(q) for q in ps])
                return g
            return always_redraw(f)

        def blocos(c, chao_terra=False):
            def f():
                s = ((self.clk.get_value() - t0) % 3.0) / 3.0
                d = 0.16 * math.sin(PI * s)
                g = VGroup()
                if chao_terra:
                    g.add(Arc(radius=1.0, start_angle=PI * 0.38, angle=PI * 0.24, arc_center=c + P3(0, -1.2)).set_stroke(mix(TERRA, 0.35), 2)
                          .set_fill(TERRA, 1))
                g.add(Square(0.22).set_stroke(width=0).set_fill(GEO, 1).move_to(c + P3(-0.16 - d, 0.0)),
                      Square(0.3).set_stroke(width=0).set_fill(STEEL, 1).move_to(c + P3(0.2 + 0.5 * d, 0.04)))
                return g
            return always_redraw(f)

        i1 = VGroup(linha(tex(r"\frac{d\vec P}{dt}", MAG, 44), mais(40, "="), tex(r"\vec F^{\,ext}", FC, 44), buff=0.22),
                    txt("COMPONENTE POR COMPONENTE", 18, color=DIM)).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        i2 = VGroup(txt("MOMENTOS IGUAIS E OPOSTOS;", 24, bold=True), txt("ENERGIA, NÃO", 24, bold=True, color=KC)) \
            .arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        i3 = VGroup(txt("NÃO CONSERVA?", 24, bold=True), txt("QUEM FICOU DE FORA?", 24, bold=True, color=MAG)) \
            .arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        ys = (1.75, 0.3, -1.15)
        icones = (esferas(P3(XI, ys[0])), blocos(P3(XI, ys[1])), blocos(P3(XI, ys[2] + 0.1), chao_terra=True))
        for m_, y in zip((i1, i2, i3), ys):
            m_.move_to(P3(XT + m_.width / 2, y))
            if m_.get_right()[0] > 6.6:
                m_.scale_to_fit_width(6.6 - XT).move_to(P3(XT + m_.width / 2, y))
        for k, (m_, ic, fr_) in enumerate(zip((i1, i2, i3), icones, ("Primeira", "Segunda", "E terceira"))):   # v5: cada ideia na fala
            self.diz(fr_)
            extra = [terra.animate.set_value(1.0)] if k == 2 else []
            self.play(FadeIn(m_, shift=0.1 * UP), FadeIn(ic), *extra, run_time=0.9 if k < 2 else 1.4)
        self.ate(0.97)
        for ic in icones:
            ic.clear_updaters()

    def cta(self):
        self._pend = []
        self.an("EN1")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.clk], run_time=0.8)
        for m in self.mobjects:
            m.clear_updaters()
        Scene.clear(self)
        self.h2 = self._sl = None
        oc = P3(0, 0.7)
        rings = VGroup(*[DashedVMobject(Circle(radius=r, arc_center=oc), num_dashes=max(12, int(14 * r)), dashed_ratio=0.6)
                         .set_stroke(VEL, 3.5, 0.16) for r in (2.0, 3.0, 4.0)])
        for i, r_ in enumerate(rings):
            r_.add_updater(lambda m, dt, sg=(1 if i % 2 == 0 else -1) * (0.06 - 0.01 * i): m.rotate(sg * dt, about_point=oc))
        logo = self.logo(6.0).move_to(oc + P3(0, 0.4))
        msg = txt("INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS", 28, op=0.9).move_to(oc + P3(0, -1.0))
        self.play(LaggedStart(*[FadeIn(r_, scale=0.85) for r_ in rings], lag_ratio=0.3), FadeIn(logo, scale=0.92), run_time=1.6)
        self.play(FadeIn(msg, shift=0.1 * UP), run_time=0.8)
        self.ate(0.97)
        # EN2 — granada --------------------------------------------------------------------------------------
        self.an("EN2")
        self.play(FadeOut(logo), FadeOut(msg), *[FadeOut(r_) for r_ in rings], run_time=0.6)
        for r_ in rings:
            r_.clear_updaters()
        self.remove(*rings)
        # v7 (final): a granada 3D do yt_0017 no campo de provas; o ⊕ (centro de massa) e o rastro dele ficam no Manim, presos à
        # projeção exata da câmera. O voo vai até pouco antes do primeiro caco tocar o chão (até lá o CM segue a parábola).
        g = Granada17(self, {"modo": "frente", "K": 1.0, "xc": -0.15, "yc": -2.75, "camx": 6.12, "fov": 16, "el": 6, "near": 0.25, "far": 700})
        self.g17 = g
        self.add(g.f3d)
        TF = min(g.ttoque) - 0.05
        SE = 0.42
        tau_de = lambda s: s / SE * g.TE if s <= SE else g.TE + (s - SE) / (1 - SE) * (TF - g.TE)
        s_ = ValueTracker(0.0)
        g.tau.add_updater(lambda m: m.set_value(tau_de(s_.get_value())))
        self.add(g.tau)
        caminho = DashedVMobject(VMobject().set_points_smoothly([g.m(g.ideal(t)) for t in np.linspace(0, 2 * g.TE, 50)])
                                 .set_stroke(DIM, 2, opacity=0.55), num_dashes=70)
        pergunta = txt("SE A GRANADA EXPLODE NO AR, O QUE CONTINUA NA PARÁBOLA?", 30, bold=True).move_to(P3(0, 3.0))

        def cm_():
            tau = g.tau.get_value()
            gq = VGroup()
            if tau > g.TE:
                ts = np.linspace(g.TE, tau, max(2, int(40 * (tau - g.TE) / (TF - g.TE)) + 2))
                gq.add(VMobject().set_points_smoothly([g.m(g.cm(x)) for x in ts]).set_stroke(color=[MAG, CYAN], width=6))   # rastro do CM
                u = (tau - g.TE) / (TF - g.TE)
                gq.add(Dot(g.m(g.cm(tau)), radius=0.11, color=interpolate_color(ManimColor(CYAN), ManimColor(MAG), u)).set_z_index(9))
            return gq
        gr = always_redraw(cm_)
        self.play(g.f3d.op.animate.set_value(1.0), FadeIn(pergunta, shift=0.1 * UP), Create(caminho), run_time=1.4)
        self.add(gr)
        t_exp = self.ate_dizer("explode no meio do voo", -0.2, mover=False)
        self.play(s_.animate.set_value(SE), run_time=max(1.0, t_exp), rate_func=linear)            # sobe até explodir na fala
        self.diz("os pedaços voam")
        t_fim = self.ate_dizer("na mesma parábola", -0.9, mover=False)
        self.play(s_.animate.set_value(1.0), run_time=max(1.5, t_fim), rate_func=linear)          # o CM segue a parábola na fala
        prox1 = txt("PRÓXIMO VÍDEO:", 26, op=0.9)
        prox2 = txt("CENTRO DE MASSA", 30, color=CYAN, bold=True)
        VGroup(prox1, prox2).arrange(RIGHT, buff=0.3).move_to(P3(0, -3.4))
        self.diz("No próximo vídeo")
        self.play(FadeIn(prox1), FadeIn(prox2, shift=0.1 * UP), run_time=0.8)
        self.ate(0.97)
        gr.clear_updaters()
