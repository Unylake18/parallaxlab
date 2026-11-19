"""yt_0037 · H · a integral que não colabora (alvo 01) — v2 (handoff v2, E01). H1: o sino 3D (sem casca) sobe; a integral a caneta; corte para o
2D sem coluna (palco de 0 a 1880 px): discos de raio 300, a faca em pé e a deitada com TRAVA na ponta, fora do disco; e^(−y²) ? SEM PRIMITIVA
ELEMENTAR em 40/30 px; a grade se curva em círculos e raios; a célula lima escorrega para fora e cresce. H2: a célula quadrada escorrega da
origem para a borda sem mudar de tamanho, e a polar escorrega e cresce (4 s, ida e volta); o cartão √π ? no canto. O hook não mostra resposta."""
from v2kit import *

VE = Vw(490, 600, 300)            # disco da grade de quadradinhos
VD = Vw(1430, 600, 300)           # disco da grade de círculos e raios
CAM_H = cam_esc((7.3, -6.6, 4.9), (0, .05, .55), 620, 600, .72, 480 - .72 * 620, 640 - .72 * 600)
FILL_D = mixh(BG_, CI, .10)
T1, T2 = math.pi / 8, math.pi / 4


def disco_quad(v):
    f = disco(v, 1, FILL_D, 1.0, z=1)
    ls = VGroup()
    for k in range(-3, 4):
        a = k / 4
        h = math.sqrt(1 - a * a)
        ls.add(lin_px([v.px(a, -h), v.px(a, h)], GEO, 1.6, alpha=.35, z=3))
        ls.add(lin_px([v.px(-h, a), v.px(h, a)], GEO, 1.6, alpha=.35, z=3))
    c = circulo(v, 1, GEO, 3, z=5)
    return VGroup(f, ls, c)


def disco_pol(v):
    f = disco(v, 1, FILL_D, 1.0, z=1)
    g = gpolar(v, 1, 4, 16, cor=GEO, alpha=.45, wpx=1.8, z=3)
    c = circulo(v, 1, GEO, 3, z=5)
    return VGroup(f, g, c)


def celula(v, r1, r2=None, cor=LI):
    r2 = r1 + .25 if r2 is None else r2
    return setor(v, r1, r2, T1, T2, fill=mixh(BG_, cor, .8), stroke=cor, wpx=2, z=6)


def quad(v, x0, y0, s=.25, cor=LI):
    return VGroup(ret_v(v, x0, x0 + s, y0, y0 + s, mixh(BG_, cor, .8), z=6), borda_v(v, x0, x0 + s, y0, y0 + s, cor, 2, z=7))


class PH(B37):
    ANTES = "A INTEGRAL QUE NÃO COLABORA"
    SUB = "QUAL É A ÁREA DE CADA PEDAÇO?"

    def corpo(self):
        # ── H1 · o sino 3D (sem casca) ──
        self.an("H1")
        pal = Palco37(self, "sino", CAM_H, cresce=0.0, casca=0.0, parede=0.0)
        self.add(pal.fundo)
        lx = ok3d(pal.prende(TP(r"\X", 0, 0, 40, "c"), "ex", 18, 6))
        self.pena(lx)
        self.play(*pal.anim(2.0, cresce=1.0), run_time=2.0)
        self.gat("do disco de raio um")
        aro = lin_px(anel_proj(pal, 2.0), GEO, 5, z=8)
        self.play(Create(aro), run_time=0.8)
        self.play(FadeOut(aro), run_time=0.5)
        self.remove(aro)
        self.gat("vídeo passado")
        I0 = TC(r"\iint_{\X^2+\Y^2\le 1} \Ci{e^{-(\X^2+\Y^2)}}\,dA", 1290, 300, 52, "c")
        self.pena(I0)
        self.wait(0.4)
        # corte para o 2D (o sino ficou ~6 s depois de subir); a integral sobe para o centro, no alto
        dq = disco_quad(VE)
        gq = leg("GRADE DE QUADRADINHOS", 490, 990, GEO, "center", 30)
        self.grade = papel(passo=0.5).set_z_index(-10)                 # K2: tela sem gráfico = quadradinhos de 60 px, entram no pouso
        corte3d(self, pal, entram=[FadeIn(self.grade), FadeIn(dq[0]), Create(dq[1]), Create(dq[2]), I0.animate.move_to(PX(960, 208))], rt=0.7)
        self.pena(gq)
        # facas
        self.gat("fatiando em pé")
        h1 = math.sqrt(1 - .35 ** 2)
        fv = lin_px([VE.px(.35, -h1), VE.px(.35, h1)], AZC, 5, z=7)
        self.play(Create(fv), run_time=0.6)
        tr1 = TPt("TRAVA", VE.px(.35, -h1)[0] + 50, VE.px(.35, -h1)[1] + 64, 30, AL, "left")
        self.pena(tr1)
        self.gat("não é elementar")
        ey = TC(r"\Ci{e^{-\Y^2}}\ ?", VE.px(.35, 0)[0], 268, 40, "c")
        sp = leg("SEM PRIMITIVA ELEMENTAR", pxof(ey.get_left())[0] - 24, 280, AL, "right", 30)
        self.pena(ey)
        self.pena(sp, passo=0.03)
        self.gat("deitado trava igual")
        h2 = math.sqrt(1 - .55 ** 2)
        fh = lin_px([VE.px(-h2, -.55), VE.px(h2, -.55)], CORAL, 5, z=7)
        self.play(Create(fh), run_time=0.6)
        tr2 = TPt("TRAVA", VE.px(-h2, -.55)[0] - 40, VE.px(-h2, -.55)[1] + 11, 30, AL, "right")
        self.pena(tr2)
        self.gat("só depende de uma coisa")
        sd = T("SÓ DEPENDE DA DISTÂNCIA ATÉ A ORIGEM", 960, 1036, 32, "center", BR)
        self.pena(sd, passo=0.03)
        self.gat("então troca a grade")
        sa = seta_px((830, 600), (1090, 600), GEO, 4, 20, z=6)
        dp = disco_pol(VD)
        self.play(GrowFromPoint(sa, PX(830, 600)), run_time=0.5)
        self.play(TransformFromCopy(dq, dp), run_time=1.6)          # caminho reto: a trilha da cópia fica entre y = 300 e 900 (os rótulos estão fora dela)
        self.gat("esta célula aqui perto")
        c1 = celula(VD, .25)
        self.play(FadeIn(c1[0]), Create(c1[1]), run_time=0.6)
        self.gat("e esta lá longe")
        r0 = ValueTracker(.25)
        mov = always_redraw(lambda: celula(VD, r0.get_value()))
        self.add(r0, mov)
        self.play(r0.animate(rate_func=smooth).set_value(.75), run_time=1.8)
        mov.clear_updaters()
        self.remove(r0)
        self.gat("o mesmo delta erre")
        mr = leg("MESMO Δr, MESMO Δθ", 1430, 990, LI, "center", 30)
        self.pena(mr, passo=0.03)
        self.gat("bem maior")
        q1 = dentro(cel_txt("?", *[a + b for a, b in zip(VD.px(.375 * math.cos(.59), .375 * math.sin(.59)), (0, 11))], 30))
        q2 = dentro(cel_txt("?", *[a + b for a, b in zip(VD.px(.875 * math.cos(.59), .875 * math.sin(.59)), (0, 14))], 40))
        self.pena(q1, q2, lag=0.2)
        self.marca("01")
        # ── H2 · a pergunta: as duas células escorregam (4 s, ida e volta) ──
        self.an("H2")
        self.gat("quanto vale a área")
        acende(self, (self.st, BR), rt=0.6)
        qq = quad(VE, 0, 0)
        self.play(FadeIn(qq), FadeOut(q1), FadeOut(q2), run_time=0.4)          # os "?" saem: as células vão escorregar por baixo deles
        self.remove(q1, q2)
        u = ValueTracker(0.0)
        qd = always_redraw(lambda: quad(VE, .5 * u.get_value(), .25 * u.get_value()))
        cp = always_redraw(lambda: celula(VD, .25 + .5 * u.get_value()))
        self.remove(qq)
        self.add(u, qd, cp)
        self.play(u.animate(rate_func=there_and_back).set_value(1.0), run_time=4.0)
        qd.clear_updaters()
        cp.clear_updaters()
        self.remove(u, qd, cp)
        # K3: a promessa com imagem. Os discos saem; o sino 2D (a área sombreada) nasce com ÁREA = ?; a integral sobe para (960, 240)
        self.gat("da curva do sino")
        sai = saindo([m for m in self.snap() if m is not I0 and m is not self.grade])
        VS_ = Vw(960, 880, 250, 425)
        xs = np.linspace(-3.2, 3.2, 321)
        cur = [VS_.px(x, math.exp(-x * x)) for x in xs]
        cv = lin_px(cur, CI, 5, z=6)
        sh = poly_px([VS_.px(-3.2, 0)] + cur + [VS_.px(3.2, 0)], mixh(BG_, CI, .25), 1.0, z=2)
        ax_ = seta_px(VS_.px(-3.4, 0), VS_.px(3.5, 0), E1, 3, 16, z=6)
        lxs = TC(r"\X", VS_.px(3.5, 0)[0] + 14, 880, 40, "l")
        self.play(*[FadeOut(m) for m in sai], I0.animate.move_to(PX(960, 240)), GrowFromPoint(ax_, VS_.P(-3.4, 0)), run_time=0.3)
        self.remove(*sai)
        self.play(Create(cv), FadeIn(sh), run_time=1.0)
        ar = T("ÁREA = ?", 960, 800, 44, "center", BR)
        cs = leg("A CURVA DO SINO: DE −∞ A +∞", 960, 960, GEO, "center", 30)
        self.pena(ar, lxs, lag=0.15)
        self.pena(cs, passo=0.03)
        self.marca("v3_01")
        self.gat("estatística")
        self.cart = cartao_raiz()
        src_q = glifos(ar)[-1]
        poe_com_moldura(self, self.cart.f, self.cart.mol, voos_=[(src_q, [len(self.cart.f[0]) - 1])], rt_voo=0.9)
        self.sai_fim()
