"""Lote PS · RESUMO (handoff v2 quadro 24; handoff v3 §3.5, §3.6, alvos 10 e 11). S1: dois cartões (x = 280 e 1160, 480 de largura): a rodinha girando
com o rot embaixo; a caixa com as setas saindo e o div embaixo. S2: layout B, vórtice magenta com o fio de corrente e falsa fonte com o fio carregado (campos
em contexto, já no começo); o laço e a cerca acendem com as setas de circulação e de fluxo; laços longe tracejados com 0 (clareira, S19); as duas linhas.
S3 (v3): os painéis encolhem para 620 × 500 (x = 250 e 1050); DO LOCAL AO GLOBAL no alto; STOKES e GAUSS embaixo de cada painel, GREEN no pé (S18).
S4 (v3): A TERCEIRA COISA — F = (x, −y), o quadradinho coral deformado pelo fluxo exato (x eᵗ, y e⁻ᵗ) até t = 0,55; rot = 0, div = 0; desafio; CTA padrão."""
from v27 import *  # noqa: F401,F403
from sec_ha import VD, VE

L0 = (2.5, 1.75)                                       # centro do laço longe (tracejado com 0)


class LoteS(Base):
    ANTES = "LAPLACIANO"

    def corpo(self):
        # ── S1 ──
        self.an("S1")
        self.secao("RESUMO")
        p1, p2 = painel(280, 250, 480, 460), painel(1160, 250, 480, 460)
        va, vb = Vista(520, 480, 100), Vista(1400, 480, 100)
        rd = Roda(va, 1.25).pose((0, 0), 0)
        arc = giro_seta(va, (0, 0), 1.55, -0.4, 1.1)
        cx = VGroup(preenche(vb, [(-0.8, -0.8), (0.8, -0.8), (0.8, 0.8), (-0.8, 0.8)], CHAPA, 0.55, 4), vlinha(vb, [(-0.8, -0.8), (0.8, -0.8), (0.8, 0.8), (-0.8, 0.8), (-0.8, -0.8)], GEO, 3))
        sai = VGroup(*[seta7(vb.c2p(0.8 * d[0], 0.8 * d[1]), vb.c2p(1.6 * d[0], 1.6 * d[1]), CAMPO2, 6, 22) for d in ((1, 0), (0, 1), (-1, 0), (0, -1))]).set_z_index(10)
        self.grade(papel(va, area_px(va, 280, 250, 480, 460)), papel(vb, area_px(vb, 1160, 250, 480, 460)))   # final: grade de cada cartão
        self.play(Create(p1), Create(p2), FadeIn(rd, scale=0.7), FadeIn(cx), run_time=0.8)
        mr = Motor(self, 1.0, "S1 rodinha").liga()
        rd.add_updater(lambda m_: m_.pose((0, 0), 1.0 * mr.tau()))
        self.play(Create(arc), LaggedStart(*[GrowArrow(s_) for s_ in sai], lag_ratio=0.15), run_time=0.9)
        fR = TC(r"\rot \F = \left(\dfrac{\partial \Qq}{\dx} - \dfrac{\partial \Pp}{\dy}\right)\kk = 2\,\w\,\kk", 520, 800, 40, "c")
        fD = TC(r"\dv \F = \dfrac{\partial \Pp}{\dx} + \dfrac{\partial \Qq}{\dy}", 1400, 800, 40, "c")
        self.gat("o rotacional mede isso com duas derivadas")
        self.play(caneta(fR))
        self.gat("o divergente mede com outras duas")
        self.play(caneta(fD))
        self.ate(0.97)

        # ── S2 (os campos entram enquanto o S1 sai: sem painel vazio) ──
        self.an("S2")
        rd.clear_updaters()
        pE, pD = painel(130, 260, 700, 560), painel(1090, 260, 700, 560)
        cv = campo7(VE, F_VORT, -3.5, 3.5, -2.8, 2.8, 0.6, rmin=0.8, rmax=2.8, mmax=1.3, ctx=True, cor=MAG, nome="S2 vórtice (contexto)")
        cf_ = campo7(VD, F_FONTE, -3.5, 3.5, -2.8, 2.8, 0.6, rmin=0.8, rmax=2.8, mmax=1.3, ctx=True, nome="S2 falsa fonte (contexto)")
        fv, ff = furo7(VE, 0.55, CORR, r"\odot", 40), furo7(VD, 0.55, CARGA, "+", 40)
        s1 = self.snap()
        grE, grD = papel(VE, area_px(VE, 130, 260, 700, 560)), papel(VD, area_px(VD, 1090, 260, 700, 560))
        self.grade(grE, grD)                                                  # final: grade de cada painel (encolhe junto no S3)
        self.play(*self.sai_entra(s1, [Create(pE), Create(pD), FadeIn(fv), FadeIn(ff), cresce_campo(cv, 0.9), cresce_campo(cf_, 0.9)]), run_time=1.0)   # final (R6)
        self.remove(*s1)
        laco = vcirc(VE, 1.7, SAIF, 4)
        circ_s = [seta7(VE.c2p(1.7 * math.cos(a), 1.7 * math.sin(a)), VE.c2p(1.7 * math.cos(a + 0.32), 1.7 * math.sin(a + 0.32)), SAIF, 5, 18).set_z_index(10)
                  for a in [2 * PI * i / 6 + 0.3 for i in range(6)]]
        self.gat("se você der uma volta em torno do furo")
        self.play(Create(laco), run_time=0.8)
        self.play(LaggedStart(*[GrowArrow(s_) for s_ in circ_s], lag_ratio=0.25), run_time=1.2)
        cerca = vcirc(VD, 1.7, SAIF, 4)
        out_s = [seta7(VD.c2p(1.5 * math.cos(a), 1.5 * math.sin(a)), VD.c2p(2.05 * math.cos(a), 2.05 * math.sin(a)), SAIF, 5, 18).set_z_index(10)
                 for a in [2 * PI * i / 8 + 0.2 for i in range(8)]]
        self.gat("se você cercar o furo")
        self.play(Create(cerca), run_time=0.8)
        self.play(LaggedStart(*[GrowArrow(s_) for s_ in out_s], lag_ratio=0.12), run_time=1.0)
        longe = VGroup()
        for v in (VE, VD):
            x, y = canto_xy(v, *L0)
            longe.add(vcirc(v, 0.45, GEO, 3, c=L0, dash=(7, 6)), TC("0", x, y, 34, "c", caneta=False))
        cl0 = VGroup(*esconde(cv, clar([], [L0], 0.7)), *esconde(cf_, clar([], [L0], 0.7)))          # S19: clareira no círculo do 0
        self.gat("longe do furo qualquer volta")
        self.play(some(cl0), FadeIn(longe), run_time=0.7)
        t1 = T("EM CADA PONTO: NADA", 960, 900, 34, "center", GEO)
        t2 = T("EM VOLTA DO FIO: ALGUMA COISA", 960, 960, 34, "center", SAIF)
        self.gat("em cada ponto nada")
        self.play(FadeIn(t1, shift=0.1 * UP), run_time=0.5)
        self.gat("em volta do fio alguma coisa")
        self.play(FadeIn(t2, shift=0.1 * UP), run_time=0.5)
        self.ate(0.97)

        # ── S3 · do local ao global (alvo 10) ──
        self.an("S3")
        k = 84 / 96
        gE = VGroup(grE, pE, cv, fv, laco, *circ_s)
        gD = VGroup(grD, pD, cf_, ff, cerca, *out_s)
        tit = T("DO LOCAL AO GLOBAL", 960, 205, 56, "center")
        self.play(FadeOut(t1), FadeOut(t2), FadeOut(longe), volta(cl0),
                  gE.animate.scale(k, about_point=PX(480, 540)).shift(RIGHT * 80 / 120),
                  gD.animate.scale(k, about_point=PX(1440, 540)).shift(LEFT * 80 / 120), run_time=1.0)
        self.remove(t1, t2, longe)
        self.play(FadeIn(tit, shift=0.1 * DOWN), run_time=0.6)
        nS = VGroup(T("STOKES", 560, 870, 46, "center"), legenda("A VOLTA EM TORNO DO FIO", 560, 920, SAIF, "center"))
        nG = VGroup(T("GAUSS", 1360, 870, 46, "center"), legenda("A CERCA EM TORNO DO FIO", 1360, 920, SAIF, "center"))
        nR = T("NO PLANO, OS DOIS VIRAM UM SÓ: GREEN", 960, 995, 32, "center", GEO, bold=False)
        for m_, fr in ((nS, "stokes"), (nG, "gauss"), (nR, "green")):
            self.gat(fr)
            self.play(FadeIn(m_, shift=0.1 * UP), run_time=0.5)
        self.ate(0.97)

        # ── S4 · a terceira coisa (alvo 11) ──
        self.an("S4")
        self.secao("A TERCEIRA COISA")
        vS = Vista(600, 560, 110)
        CLQ = [(-1.45, -0.75, 1.45, 0.75)]
        cd = campo7(vS, F_SELA, -3.3, 3.3, -3.3, 3.3, 0.6, rmin=0.0, rmax=3.3, mmax=3.3, skip=clar(CLQ), nome="S4 deformação (x, −y)")
        orig = contorno_ini(vS, [(-0.6, -0.6), (0.6, -0.6), (0.6, 0.6), (-0.6, 0.6)])
        q = Pedaco(vS, uv_quad((0, 0), 1.2), fl_sela)                           # v4 §4: as células esticam e achatam
        s3 = self.snap()
        self.grade(papel(vS))                                                 # final: a grade nasce dos eixos do (x, −y)
        self.play(*self.sai_entra(s3, [FadeIn(q), cresce_campo(cd, 0.9)]), run_time=1.0)    # o campo entra depois que o S3 sai (final, R6)
        self.remove(*s3)
        fF = TC(r"\F = (\X,\ -\Y)", 1120, 330, 52)
        self.gat("olha este campo")                                            # final: F começa em "olha este campo"
        self.play(caneta(fF))
        fr_ = TC(r"\rot\F = \vec 0", 1120, 450, 48)
        fd_ = TC(r"\dv\F = 0", 1500, 450, 48)
        self.gat("faz a conta")                                                 # final: rot F = 0 começa em "faz a conta"
        self.play(caneta(fr_))
        self.gat("o divergente também")
        self.play(caneta(fd_))
        self.gat("nenhuma rodinha gira")
        self.play(FadeIn(legenda("NENHUMA RODINHA GIRA", 1124, 560, VEL)), run_time=0.5)
        self.gat("nenhum pedacinho muda de área")
        self.play(FadeIn(legenda("NENHUM PEDACINHO MUDA DE ÁREA", 1124, 610, SAI)), run_time=0.5)
        self.gat("estica")
        self.add(orig)
        a0 = area_poly(q.XY) if hasattr(q, "XY") else area_poly(ret_pts((0, 0), 1.2))
        self.play(*corre(self, [q], 0.55, 2.5, rate=smooth))
        print(f"[deforma] S4: fluxo exato (x eᵗ, y e⁻ᵗ) até t = 0,55: área {a0:.5f} → {area_poly(q.XY):.5f}; "
              f"lados {1.2 * math.exp(0.55):.3f} × {1.2 * math.exp(-0.55):.3f}")
        self.gat("isso é a deformação")
        self.play(FadeIn(T("MAS O QUADRADINHO DEFORMA", 1120, 720, 40, "left", CORAL)), run_time=0.5)
        self.gat("desafio para os comentários")
        self.play(FadeIn(legenda("DESAFIO: ACHE OUTRO CAMPO ASSIM (NÃO CONSTANTE)", 1124, 840, GEO)), run_time=0.5)

        # ── final §2.9 (alvo 21, sb27 `prox5`): prévia do próximo vídeo; tudo da terceira coisa sai ──
        tP = T("NO PRÓXIMO VÍDEO", 960, 215, 56, "center")
        sP = legenda("LIMITE, CONTINUIDADE E DERIVADAS PARCIAIS", 960, 280, SAIF, "center", 34)
        pnE, pnD = painel(170, 350, 700, 560), painel(1050, 350, 700, 560)
        vP = Vista(520, 630, 80)
        cP = campo7(vP, F_SELA, -3.2, 3.2, -3.2, 3.2, 0.8, rmin=1.6, rmax=3.0, mmax=3.2, ctx=True,
                    skip=lambda X, Y: Y < -2.4 and abs(X) < 1.5, nome="S4 prévia (x, −y)")
        oP = contorno_ini(vP, [(-0.8, -0.8), (0.8, -0.8), (0.8, 0.8), (-0.8, 0.8)])
        qP = Pedaco(vP, uv_quad((0, 0), 1.6), fl_sela)
        lD = legenda("A DEFORMAÇÃO", 520, 870, CORAL, "center")
        mJ = TC(r"\begin{pmatrix} \dfrac{\partial \Pp}{\dx} & \dfrac{\partial \Pp}{\dy} \\[12pt] \dfrac{\partial \Qq}{\dx} & \dfrac{\partial \Qq}{\dy} \end{pmatrix}",
                1400, 610, 60, "c")
        lT = legenda("TODAS AS DERIVADAS PARCIAIS", 1400, 870, SAIF, "center")
        self.gat("no próximo vídeo")
        self.grade(papel(vP, area_px(vP, 170, 350, 700, 560)), papel(None, area_px(Vista(960, 540, 120), 1050, 350, 700, 560)))
        s4 = self.snap()
        sai_c = [m_ for m_ in (self.h2,) if m_ is not None]
        self.play(*self.sai_entra(s4 + sai_c, [FadeIn(tP, shift=0.1 * DOWN), FadeIn(sP), FadeIn(pnE), FadeIn(pnD)]), run_time=0.8)
        self.remove(*s4, *sai_c)
        self.h2 = None
        self.play(cresce_campo(cP, 0.8), FadeIn(qP), FadeIn(oP), run_time=0.8)
        self.play(*corre(self, [qP], 0.55, 2.0, rate=smooth))
        self.play(FadeIn(lD, shift=0.1 * UP), run_time=0.4)
        self.gat("juntando todas as derivadas parciais")
        self.play(caneta(mJ))
        self.play(FadeIn(lT, shift=0.1 * UP), run_time=0.4)

        # ── CTA padrão (yt_0026): tudo sai; logo com os dois anéis; INSCREVA-SE até o fim da fala + 3 s ──
        self.gat("se essa aula te ajudou")
        self.grade(self.grade0)
        CL = P3(0, 0.9)
        logo = self.logo(5.6).move_to(CL)
        aneis = VGroup(*[DashedVMobject(Circle(radius=r).move_to(CL), num_dashes=48).set_stroke(GEO, 2.6, opacity=o) for r, o in ((2.1, 0.85), (2.45, 0.6))])
        for m_ in aneis.get_family():
            m_._sem_contorno = True
        ins = VGroup(T("INSCREVA-SE PARA ACOMPANHAR", 960, 0, 66, "center"), T("OS PRÓXIMOS VÍDEOS", 960, 0, 66, "center")).arrange(DOWN, buff=0.12).move_to(P3(0, -2.6))
        s4 = self.snap()
        sai_c = [m_ for m_ in (self.h2,) if m_ is not None]
        self.play(*self.sai_entra(s4 + sai_c, [FadeIn(logo, scale=0.96), FadeIn(aneis), FadeIn(ins, shift=0.1 * UP)]), run_time=0.8)
        self.remove(*s4, *sai_c)
        self.h2 = None
        rt = self.resta() + 3.0
        self.play(Rotate(aneis[0], 0.3 * rt, rate_func=linear), Rotate(aneis[1], -0.24 * rt, rate_func=linear), run_time=rt)
