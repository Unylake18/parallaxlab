"""yt_0045 · Lote PS: S1 (resumo, alvo 17) e S2 (mais rápido, ao contrário, com quina; alvo 18) + cartão do próximo vídeo + CTA."""
from k45 import *  # noqa: F401,F403

COL = 1020
V = Vista2D(320, 560, 110)
RA = 2.0
fc = lambda t: (RA * math.cos(t), RA * math.sin(t))
fo = lambda t: (2.4 * math.cos(t), 2.4 * math.sin(t))


class PS(B45):
    ANTES = "LENDO A RESPOSTA"

    def corpo(self):
        # ── S1 · síntese (alvo 17) ──────────────────────────────────────────────────────────────────────────
        # as fórmulas de origem não estão mais na tela neste lote (saíram nos lotes PB2, PB6 e PB4): tudo a caneta (handoff §7, S1)
        self.an("S1")
        self.titulo("RESUMO", rt=0.2)
        cw = 580
        cards = []
        for i, (X, t) in enumerate(((60, "DEFINIÇÃO"), (670, "OUTRA NOTAÇÃO"), (1280, "O SINAL"))):
            ct = cartao(X, 200, cw, 440)
            nn = num(i + 1, X + 48, 252, 36)
            tt = T(t, X + 76, 262, 32, "left", GEO)
            cards.append((ct, nn, tt))
        S1m = []

        self.gat("Resumindo a aula")
        ct, nn, tt = cards[0]
        f1 = TC(r"\int_{\g}\Fv\cdot\dg=", 90, 380, 44)
        f2 = TC(r"\int_a^b \Fv(\g(\Tt))\cdot\gp(\Tt)\,\dTt", 110, 490, 40)
        self.dentro(ct._painel, tt, f1, f2)
        self.pena(nn, tt, extra=[FadeIn(ct)])
        self.pena(f1, f2)
        self.col("S1", f1, f2)
        S1m += [ct, nn, tt, f1, f2]

        self.gat("Na outra notação")
        ct, nn, tt = cards[1]
        g1 = TC(r"\int_{\g}P\,\dX+Q\,\dY+R\,\dZ", 700, 430, 44)
        g2 = leg("SEMPRE VOLTANDO PARA O t", 700, 540, GEO, "left", 28)
        self.dentro(ct._painel, tt, g1, g2)
        self.pena(nn, tt, extra=[FadeIn(ct)])
        self.pena(g1, g2)
        self.col("S1", g1, g2)
        S1m += [ct, nn, tt, g1, g2]

        self.gat("O sinal do produto escalar")
        ct, nn, tt = cards[2]
        hs = [mixl([("m", s), ("t", w, c)], 1310, y, 44) for s, w, c, y in ((">0", "AJUDA", LI, 370), ("=0", "DE LADO", GEO, 460), ("<0", "ATRAPALHA", AL, 550))]
        self.dentro(ct._painel, tt, *[p for h in hs for p in h.p])
        self.pena(nn, tt, extra=[FadeIn(ct)])
        for h in hs:
            self.pena(*h.p)
        self.col("S1", *hs)
        S1m += [ct, nn, tt, *[p for h in hs for p in h.p]]

        self.gat("E duas lições dos exemplos")
        cb = cartao(60, 740, 1800, 200)
        i1 = T("REDEMOINHO: DEPENDE DO CAMINHO", 100, 815, 32, "left", CAMPO)
        j1 = mixl([("m", r"2\pi R^2"), ("t", "E", GEO), ("m", "0")], 100, 885, 32)
        i2 = T("F = (x, y): SÓ AS PONTAS", 780, 815, 32, "left", MEN)
        j2 = TC(r"W=0", 780, 885, 32)
        self.dentro(cb._painel, i1, *j1.p, i2, j2)
        self.pena(i1, extra=[FadeIn(cb)])
        self.pena(*j1.p)
        self.pena(i2, j2)
        S1m += [cb, i1, *j1.p, i2, j2]

        self.gat("medir área")
        i3 = T("VOLTA FECHADA: 2 × ÁREA", 1340, 815, 32, "left", LI)
        j3 = TC(r"4\pi=2\cdot2\pi", 1340, 885, 32)
        self.dentro(cb._painel, i3, j3)
        self.pena(i3, j3)
        S1m += [i3, j3]
        self.marca("17_S1")

        # ── S2 · mais rápido, ao contrário, com quina (alvo 18) ────────────────────────────────────────────────
        self.an("S2")
        self.sai(*S1m, rt=0.3)            # a saída do S1 corre já dentro da fala do S2: a caneta da última lição não acelera e a tela não atrasa
        self.titulo("MAIS RÁPIDO, AO CONTRÁRIO, COM QUINA", rt=0.3)
        eix, (rx, ry) = eixos2(V, -2.6, 2.8, -2.6, 2.7)
        self.papel_vista(V, rt=0.4, extra=[Create(eix[0]), Create(eix[1])])
        self.pena(rx, ry)

        self.gat("com t de zero a dois pi")
        self.degrau("C9.1a", "gamma_1(t) = (R cos t, R sen t), 0 <= t <= 2pi")
        cv = curva(V, fc, 0, 2 * PI, HEL, 6)
        sv = sentido(V, fc, PI * .6)
        sqM, lqM = legq(HEL, "MESMA VOLTA", 120, 1020, 28)
        s1 = TC(r"\g_1(\Tt)=(R\cos\Tt,\ R\sen\Tt),\quad 0\le\Tt\le2\pi", COL, 200, 42)
        self.play(Create(cv), run_time=1.2)
        self.play(FadeIn(sv), FadeIn(sqM), run_time=0.3)
        self.pena(lqM, s1)
        self.col("S2", s1)

        self.gat("duas vezes mais rápido")
        self.degrau("C9.1b", "gamma_2(u) = (R cos 2u, R sen 2u), 0 <= u <= pi")
        s2 = TC(r"\g_2(\uu)=(R\cos2\uu,\ R\sen2\uu),\quad 0\le\uu\le\pi", COL, 300, 42)
        s3 = leg("DUAS VEZES MAIS RÁPIDO: W MUDA?", COL, 385, CI, "left", 32)
        self.pena(s2)
        self.pena(s3)
        self.col("S2", s2, s3)

        self.gat("E se a conta der a volta ao contrário")
        ac = lin_px([V.P(*fo(PI * 1.1 + PI * .4 * k / 40)) for k in range(41)], AL, 4, z=6)
        sa = sentido(V, lambda t: fo(-t), -PI * 1.32, AL)
        sqA, lqA = legq(AL, "AO CONTRÁRIO", 420, 1020, 28)
        s4 = T("AO CONTRÁRIO?", COL, 465, 40, "left", BR)
        self.play(Create(ac), FadeIn(sa), FadeIn(sqA), run_time=0.6)
        self.pena(lqA, s4)

        self.gat("E se o caminho tiver quina")
        sq = [(3.3, -1.0), (5.1, -1.0), (5.1, 0.8), (3.3, 0.8), (3.3, -1.0)]
        qd = V.linha(sq, HEL, 6, dash=(14, 10))
        qs = VGroup(*[V.ponto(p, AL, 10) for p in sq[:4]])
        sqQ, lqQ = legq(AL, "QUINAS", 720, 1020, 28)
        s5 = T("COM QUINA?", pxof(s4.get_right())[0] + 14, 465, 40, "left", BR)
        self.play(Create(qd), run_time=0.8)
        self.play(FadeIn(qs), FadeIn(sqQ), run_time=0.3)
        self.pena(lqQ, s5)
        self.col("S2", VGroup(s4, s5))

        self.gat("No próximo vídeo")
        ct = cartao(1060, 560, 760, 330)
        p1 = leg("NO PRÓXIMO VÍDEO", 1440, 635, GEO, "center", 30)
        p2 = T("MUDANÇA DE PARÂMETRO", 1440, 720, 48, "center", BR)
        p3 = T("E CAMINHOS COM QUINA", 1440, 790, 48, "center", HEL)
        p4 = leg("O MESMO TRABALHO?", 1440, 850, GEO, "center", 28)
        self.dentro(ct._painel, p1, p2, p3, p4)
        self.pena(p1, p2, p3, p4, extra=[FadeIn(ct)])         # o cartão nasce junto do texto
        self.marca("18_S2", agora=True)
        # critério 20: o cartão fica ≥ 8 s antes do CTA (o desafio e o "deixa nos comentários" correm por cima; nada novo se escreve)
        self.wait(8.2)
        self.gat("Curte o vídeo")
        cta43(self)
