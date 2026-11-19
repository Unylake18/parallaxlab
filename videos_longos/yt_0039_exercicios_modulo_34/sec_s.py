"""yt_0039 · S · síntese e próximo vídeo (alvo 15). S1: cartão com os cinco erros (✗ ALERTA → correção menta), um por gatilho; no fim a miniatura
da meia arruela com os dois ⊕ (0,990 e 1,023). S2: a chapa [0, 2]² com o mapa ciano GANHA ALTURA e vira o cubo de lado 2 (três faces em perspectiva
fixa desenhadas no Manim; arestas escondidas não aparecem); ρ = x² + y² + z², MAIS PESADO LONGE DO CANTO, QUANTO PESA ESTE CUBO?, a caixinha
lima com Δx Δy Δz; o cartão NO PRÓXIMO VÍDEO / INTEGRAL TRIPLA por ≥ 8 s, sem o CTA por cima; o CTA (liso) com o desafio."""
from k39 import *

O0, U0 = (330, 820), 230
DXv, DYv, DZv = (1, 0), (.55, -.42), (0, -1)


def Pp(a, b, c):
    return (O0[0] + U0 * (a * DXv[0] + b * DYv[0] + c * DZv[0]), O0[1] + U0 * (a * DXv[1] + b * DYv[1] + c * DZv[1]))


def face_img(f, fm, h, n=40, z=2):
    """Uma face do cubo (mapa de x² + y² + z², cor calculada uma vez), em quadradinhos sem contorno; h = altura atual do cubo."""
    g = VGroup()
    for i in range(n):
        for j in range(n):
            s0, s1, t0, t1 = 2 * i / n, 2 * (i + 1) / n, 2 * j / n, 2 * (j + 1) / n
            q = [Pp(*f(s0, t0, h)), Pp(*f(s1, t0, h)), Pp(*f(s1, t1, h)), Pp(*f(s0, t1, h))]
            m = fm((s0 + s1) / 2, (t0 + t1) / 2, h)
            c = mixh("#10243A", CI, min(1.0, (m[0] ** 2 + m[1] ** 2 + m[2] ** 2) / 12) ** .85)
            p = Polygon(*[PX(*x) for x in q]).set_fill(c, 1).set_stroke(c, .6)
            g.add(p)
    return sem_ctn(g).set_z_index(z)


def cubo(h, n=28):
    fF = (lambda s, t, h: (s, 0, t * h / 2), lambda s, t, h: (s, 0, t * h / 2))
    fT = (lambda s, t, h: (s, t, h), lambda s, t, h: (s, t, h))
    fR = (lambda s, t, h: (2, s, t * h / 2), lambda s, t, h: (2, s, t * h / 2))
    faces = VGroup(face_img(*fF, h, n), face_img(*fT, h, n), face_img(*fR, h, n))
    ed = [((0, 0, 0), (2, 0, 0)), ((2, 0, 0), (2, 2, 0)), ((2, 0, 0), (2, 0, h)), ((0, 0, 0), (0, 0, h)), ((0, 0, h), (2, 0, h)), ((2, 0, h), (2, 2, h)),
          ((0, 0, h), (0, 2, h)), ((0, 2, h), (2, 2, h)), ((2, 2, 0), (2, 2, h))]
    arestas = VGroup(*[lin_px([Pp(*a), Pp(*b)], GEO, 2.5, z=5) for a, b in ed])
    return VGroup(faces, arestas)


class PS(B39x):
    ANTES = "SÍNTESE"

    def corpo(self):
        # ═══ S1 · os cinco erros ═══
        self.an("S1")
        self.secao("OS CINCO ERROS")
        self.grade = papel_cartao()
        self.play(FadeIn(self.grade), run_time=0.4)
        erros = [("ESQUECER O JACOBIANO", [("m", r"dA=\R\,\dr\,\dth")], "esquecer o jacobiano"),
                 ("JACOBIANO SEM MÓDULO, OU O DA IDA", [("m", r"|J|"), ("t", "INVERTA O DA IDA", MEN)], "sem módulo"),
                 ("LIMITES SEM DESENHAR", [("t", "BORDA POR BORDA", MEN)], "sem desenhar"),
                 ("DIVIDIR PELA ÁREA COM ρ VARIÁVEL", [("m", r"\yb=\dfrac{\Mx}{\mm}")], "dividir pela área"),
                 ("PAPPUS COM CHAPA NÃO HOMOGÊNEA", [("t", "SÓ COM O CENTROIDE", MEN)], "usar pappus com chapa")]
        self.gat("resumindo")
        Y0, DY = 300, 125
        # C13: as cinco cruzes nascem já na primeira palavra (a tela nunca fica só com o título); cada linha nasce no seu gatilho
        cxs = [cruz_px(150, Y0 + i_ * DY, AL, .9) for i_ in range(5)]
        for c_ in cxs:
            self.play(Create(c_), run_time=0.25)
        for i, (e, cor_, fr) in enumerate(erros):
            self.gat(fr)
            Y = Y0 + i * DY
            cx = cxs[i]
            te = T(e, 200, Y + 11, 30, "left", BR)
            sa = seta_px((860, Y), (930, Y), GEO, 3, 14, z=6)
            cc = mixl(cor_, 960, Y, 38)
            self.pena(te)
            self.play(Create(sa), run_time=0.3)
            self.pena(*cc.p, lag=0.05)
            ok = check_px(pxof(cc.get_right())[0] + 36, Y, MEN, .9)
            self.play(Create(ok), run_time=0.3)
        self.gat("E a meia arruela")
        v = Vw(1580, 960, 75)
        ar = arruela(v, z=2)
        bd = lin_px([v.px(*p) for p in arcoP(2)], GEO, 2.5, z=4)
        bi = lin_px([v.px(*p) for p in arcoP(1)], AL, 2.5, z=4)
        self.play(FadeIn(ar), Create(bd), Create(bi), run_time=0.6)
        pv = cm(*v.px(0, 28 / (9 * math.pi)), 9, vaz=True)
        self.play(FadeIn(pv), run_time=0.3)
        n1 = TC(r"0{,}990", *v.px(-2.25, .7), 26, "r")
        self.pena(n1)
        self.gat("volta para a chapa em")
        pk = cm(*v.px(0, 45 / (14 * math.pi)), 10)
        n2 = TC(r"\Ci{1{,}023}", *v.px(2.2, 1.4), 26, "l")
        self.play(FadeIn(pk), run_time=0.3)
        self.pena(n2)
        self._fecha(antes=0.4)
        self.limpa_tudo(rt=0.4)

        # ═══ S2 · o próximo vídeo (alvo 15) e CTA ═══
        self.an("S2")
        self.secao("O PRÓXIMO PASSO")
        self.grade = papel_cartao()
        self.play(FadeIn(self.grade), run_time=0.3)
        self.gat("toda massa foi de chapa")
        hT = ValueTracker(0.02)
        ch = cubo(0.02, 24)
        self.play(FadeIn(ch), run_time=0.8)
        self.gat("dentro de um sólido ponto")
        ch2 = cubo(2.0, 24)
        self.play(Transform(ch, ch2), run_time=2.2)
        p0 = Pp(0, 0, 0)
        dot = ponto_px(*p0, BR, 8, z=9)
        lc = mixl([("t", "CANTO", GEO), ("m", r"(0,0,0)")], p0[0] - 20, p0[1] + 44, 30)
        self.play(FadeIn(dot), run_time=0.3)
        self.pena(*lc.p, lag=0.05)
        self.gat("mais pesado longe de um canto")
        rh = TC(r"\rr=\X^2+\Y^2+z^2", 1180, 760, 38, "l")
        lm = leg("MAIS PESADO LONGE DO CANTO", 1180, 830, CI, "left", 28)
        self.pena(rh, lm, lag=0.1)
        self.gat("quanto pesa esse cubo")
        qp = T("QUANTO PESA ESTE CUBO?", 330, 1010, 36, "left", BR)
        self.pena(qp)
        self.gat("uma soma de caixinhas")
        bx, h = (1.2, .9, 1.1), .28
        cb = [Pp(bx[0] + a, bx[1] + b, bx[2] + c) for a, b, c in ((0, 0, 0), (h, 0, 0), (h, 0, h), (0, 0, h))]
        caixa = poly_px(cb, LIMA, 1.0, z=8)
        lcx = TP(r"\Delta x\,\Delta y\,\Delta z", 300, (cb[1][1] + cb[2][1]) / 2, 28, "r")
        fio_c = lin_px([(308, (cb[1][1] + cb[2][1]) / 2), (cb[0][0] - 8, (cb[1][1] + cb[2][1]) / 2)], GEO, 1.3, z=8)
        fio_c.set_stroke(opacity=.8)
        self.play(FadeIn(caixa), Create(fio_c), run_time=0.4)
        self.pena(lcx)
        self.gat("no próximo vídeo")
        pn = painel(1180, 330, 600, 330)
        t1 = T("NO PRÓXIMO VÍDEO", 1480, 440, 32, "center", GEO)
        t2 = T("INTEGRAL TRIPLA", 1480, 530, 52, "center", BR)
        f3 = TC(r"\iiint_E \rho\enspace dV", 1480, 610, 40, "c")
        self.pena(t1, t2, f3, lag=0.08, extra=[Create(pn)])
        t_card = self.t
        self.marca("15_S2", agora=True)
        self.gat("deixa o like")
        if self.t - t_card < 8.2:
            self.wait(8.2 - (self.t - t_card))
        print(f"[cartao] próximo vídeo na tela por {self.t - t_card:.2f} s antes do CTA")
        # CTA padrão do canal, liso (sem grade), com o desafio
        CL = P3(0, 1.1)
        logo = self.logo(5.6).move_to(CL)
        aneis = VGroup(*[DashedVMobject(Circle(radius=r).move_to(CL), num_dashes=48).set_stroke(GEO, 2.6, opacity=o) for r, o in ((2.1, 0.85), (2.45, 0.6))])
        ins = VGroup(T("INSCREVA-SE PARA ACOMPANHAR", 960, 0, 60, "center", caneta=False), T("OS PRÓXIMOS VÍDEOS", 960, 0, 60, "center", caneta=False)
                     ).arrange(DOWN, buff=0.12).move_to(P3(0, -2.2))
        s4 = self.snap() + [self.grade]
        sai_c = [m_ for m_ in (self.h2, self.h1) if m_ is not None and m_ in self.mobjects]
        self.play(*[FadeOut(m_) for m_ in s4 + sai_c], FadeIn(logo, scale=0.96), FadeIn(aneis), run_time=0.6)
        self.remove(*s4, *sai_c)
        self.wait(0.3)                                   # v2 A8: o texto só entra depois que o cubo saiu e o logo terminou de montar
        self.play(FadeIn(ins, shift=0.1 * UP), run_time=0.5)
        self.grade, self.h2 = None, None
        self.gat("a partir de que tamanho")
        dz = T("A PARTIR DE QUE BURACO O CENTRO CAI NELE?", 960, 1010, 36, "center", MEN)
        self.pena(dz, passo=0.03)
        rt = self.resta() + 3.0
        self.play(Rotate(aneis[0], 0.3 * rt, rate_func=linear), Rotate(aneis[1], -0.24 * rt, rate_func=linear), run_time=rt)
