"""Lote PH (handoff v3 do lote 1, visual novo): hook H1–H3 (campo de provas em vácuo: a granada de fragmentação sobe do marco com a câmera
presa a ela, eixos, fotos fantasma e o vetor de lançamento → as emendas acendem → câmera lenta na fratura em três cacos do próprio corpo →
recuo até o gráfico inteiro → tracejado → ⊕ em degradê → pergunta, congelada antes do toque) e abertura A1–A4 (logo limpo; título com a
fratura de novo, pequena e a 25%; o cavalo e a pedra do vídeo anterior → dP/dt = F_ext saindo do desenho; a granada volta no gráfico
inteiro: ONDE?). Trocas de cena em crossfade (G5)."""
from camadas import *  # noqa: F401,F403
from sec_cavalo import Cavalo3D


class LoteHook(Camadas):
    def construct(self):
        self.setup_base()
        g = self.granada_hook(ancoras=True)
        self.abertura(g)
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def abertura(self, g):
        # A1 — só o logo (nada da granada atrás)
        self.an("A1")
        logo = self.logo(5.6).move_to(P3(0, 0.9))
        bv = txt("BEM-VINDOS AO PARALLAX LAB", 30, op=0.95).move_to(P3(0, -0.5))
        sai = [self.pergunta, self.cam_gra, self.g_par]
        self.play(*[FadeOut(m) for m in sai], g.f3d.op.animate.set_value(0.0), FadeIn(logo, scale=0.94), FadeIn(bv, shift=0.1 * UP), run_time=1.0)
        for m in sai:
            m.clear_updaters()
        self.remove(*sai)
        self.ate(0.97)
        # A2 — título; embaixo dele, pequena e a 25%, a fratura de novo (a mesma granada e os mesmos cacos do H2, câmera presa a ela)
        self.an("A2")
        tt = txt("CENTRO DE MASSA", 54, bold=True).move_to(P3(0, 1.9))
        sub = txt("O PONTO QUE UMA EXPLOSÃO NÃO CONSEGUE DESVIAR", 28, color=DIM).next_to(tt, DOWN, buff=0.35)
        g.seg.set_value(1.0); g.xseg.set_value(0.0); g.yseg.set_value(-1.55); g.K.set_value(1.25); g.w.set_value(0.0); g.fant.set_value(0.0)
        g.tau.set_value(g.TE - 0.45); g.onda.set_value(-1.0); g.brilho.set_value(0.0)
        self.play(FadeOut(logo), FadeOut(bv), FadeIn(tt, shift=0.1 * UP), FadeIn(sub), g.f3d.op.animate.set_value(0.25),
                  g.tau.animate(rate_func=linear).set_value(g.TE - 0.3), run_time=0.8)
        self.play(g.tau.animate(rate_func=linear).set_value(g.TE - 0.05), g.onda.animate(rate_func=linear).set_value(1.25), g.brilho.animate.set_value(2.2),
                  run_time=0.8)
        self.play(g.tau.animate(rate_func=linear).set_value(g.TE + 0.85), run_time=max(1.0, self.resta() - 0.2))
        # A3 — o vídeo anterior: cavalo e pedra, fronteira, corda interna, forças do chão → dP/dt = F_ext (cada símbolo sai do desenho)
        self.an("A3")
        velhos = [tt, sub, g.f3d]
        cv = self.cv = Cavalo3D(self, v=lambda t: 0.42, K=0.72, xt=-1.35, yc=-2.45, op=0.0)
        self.add(cv.f3d)
        self.troca(velhos, cv.f3d.op.animate.set_value(1.0), rt=0.6)
        tens, ext = ValueTracker(0.0), ValueTracker(0.0)
        self.add(tens, ext)

        def front():
            p = cv.pts()
            xl, xr = p["pedra_tras"][0] - 0.3, p["cabeca"][0] + 0.35
            y0, y1 = p["cascos"][1] - 0.15, p["topo"][1] + 0.22
            r = RoundedRectangle(corner_radius=0.3, width=xr - xl, height=y1 - y0).move_to(P3((xl + xr) / 2, (y0 + y1) / 2))
            r.set_stroke(WHITE_, 2.2, opacity=0.62)
            return VGroup(DashedVMobject(r, num_dashes=int((xr - xl + y1 - y0) * 5), dashed_ratio=0.55).set_z_index(1),
                          mtxt("SISTEMA", 24, op=0.85).next_to(r.get_corner(UL), UP, buff=0.1).align_to(r, LEFT).shift(0.25 * RIGHT))

        def forcas():
            p = cv.pts()
            k = cv.K.get_value()
            g_ = VGroup()
            if tens.get_value() > 0.01:
                o = tens.get_value()
                g_.add(seta(p["corda_pedra"] + P3(0.05, -0.14), p["corda_pedra"] + P3(1.1, -0.14), INT, 6, tip=0.2, op=o, z=12),
                       seta(p["peito"] + P3(0.55 * k + 1.05, 0), p["peito"] + P3(0.55 * k, 0), INT, 6, tip=0.2, op=o, z=12),
                       )
                q_ = p["corda_pedra"] + 0.38 * (p["peito"] - p["corda_pedra"])             # trecho da corda entre a seta da pedra e as patas
                lab_ = mtxt("INTERNA", 24, color=INT, op=o).move_to(P3(q_[0], -3.8))              # abaixo dos rótulos do chão
                g_.add(lab_, Line(lab_.get_top() + 0.05 * UP, q_ + 0.08 * DOWN).set_stroke(INT, 1.6, opacity=0.8 * o))
            if ext.get_value() > 0.01:
                o = ext.get_value()
                yb = p["cascos"][1] - 0.34
                g_.add(seta(P3(p["cascos"][0] - 0.2, yb), P3(p["cascos"][0] + 1.25, yb), FC, 7, tip=0.22, op=o, z=12),
                       seta(P3(p["pedra_base"][0] + 0.2, yb), P3(p["pedra_base"][0] - 0.85, yb), FC, 7, tip=0.22, op=o, z=12),
                       mtxt("CHÃO NAS PATAS", 24, color=FC, op=o).move_to(P3(p["cascos"][0] + 0.55, yb - 0.36)),
                       mtxt("CHÃO NA PEDRA", 24, color=FC, op=o).move_to(P3(p["pedra_base"][0] - 0.35, yb - 0.36)))
            return g_
        fr, fz = vivo(front), vivo(forcas)
        self.add(fz)
        self.ate(0.08)
        self.play(FadeIn(fr), run_time=0.8)
        self.ate(0.22)
        self.play(tens.animate.set_value(1.0), run_time=0.6)
        self.ate(0.42)
        self.play(ext.animate.set_value(1.0), run_time=0.6)
        self.ate(0.5)
        eq = Mc((r"\frac{d\vec P}{dt}", MAG), "=", (r"\vec F^{\,ext}", FC), size=64)
        na_conta(eq, 1.0)
        ff = fz.submobjects[0].copy()
        self.play(TransformFromCopy(VGroup(*ff.submobjects[4:6]), eq[2]), run_time=1.0)           # as setas do chão → F_ext
        self.play(TransformFromCopy(fr.submobjects[0][0].copy(), eq[0]), FadeIn(eq[1]), run_time=1.0)   # a fronteira → dP/dt
        nt = cartao("SÓ A FORÇA EXTERNA", "MUDA O MOMENTO TOTAL")
        na_conta(nt, -0.55)
        self.ate(0.75)
        self.play(FadeIn(nt), run_time=0.6)
        self.ate(0.97)
        # A4 — a granada volta grande (o enquadramento final do hook); a equação vai para o canto e pergunta ONDE?
        self.an("A4")
        velhos = [fr, fz, nt, cv.f3d, tens, ext]
        g = self.nova_granada(op=0.0, tau=g.TE - 0.6)                   # o enquadramento final do hook: o gráfico inteiro, com eixos
        g.fant.set_value(1.0)
        self.g_eix.set_value(1.0); self.g_ras.set_value(1.0)
        self.remove(self.cam_gra)                                       # as camadas entram com a granada, depois da troca (G13)
        self.troca(velhos, g.f3d.op.animate.set_value(1.0), OpVivo(self.cam_gra), eq.animate.scale(46 / 64).move_to(P3(5.45, 2.95)), seq=True)
        par = self.parabola(g)
        self.play(Create(par), run_time=0.6)
        q = mtex("?", WHITE_, 56)
        onde = VGroup(txt("ONDE", 32, bold=True), q).arrange(RIGHT, buff=0.08).next_to(eq, LEFT, buff=0.45)   # à esquerda: os pedaços passam por baixo
        self.play(g.tau.animate(rate_func=linear).set_value(g.TE + 0.2), run_time=1.0)
        self.play(FadeIn(onde, shift=0.1 * UP), g.tau.animate(rate_func=linear).set_value(g.TE + 0.35), run_time=0.7)
        self.play(q.animate(rate_func=there_and_back).scale(1.35), g.tau.animate(rate_func=linear).set_value(g.TE + 0.5), run_time=0.6)
        self.ate_mov(0.55, g.tau, g.TE + 0.9)
        self.play(self.g_cm.animate.set_value(1.0), self.g_pul.animate(rate_func=there_and_back).set_value(1.0),
                  g.tau.animate(rate_func=linear).set_value(g.TE + 1.1), run_time=0.8)
        self.ate_mov(0.82, g.tau, g.TE + 1.9)
        self.play(self.g_pul.animate(rate_func=there_and_back).set_value(1.0), g.tau.animate(rate_func=linear).set_value(g.TE + 2.15), run_time=0.8)
        self.play(g.tau.animate(rate_func=linear).set_value(g.ttoque[1] - 0.08), run_time=max(0.6, self.resta() - 0.2))   # até quase o toque
