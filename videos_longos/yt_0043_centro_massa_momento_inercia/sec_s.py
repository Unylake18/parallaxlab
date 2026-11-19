"""yt_0043 · Lote PS: S1 (síntese) e S2 (o eixo na parede, cartão ≥ 8s e CTA liso, alvo 21)."""
from k43 import *  # noqa: F401,F403

COL = 1020


class PS(B43):
    ANTES = "MESMA FORMA, MASSA EM OUTRO LUGAR"

    def corpo(self):
        # ── S1 · síntese ──────────────────────────────────────────────────────────────────────────────────
        self.an("S1")

        P1 = [("t", "CENTRO DE MASSA:", GEO), ("m", r"\xb=\dfrac{\Myz}{M},\ \ \yb=\dfrac{\Mxz}{M},\ \ \zb=\dfrac{\Mxy}{M}")]
        P2 = [("t", "MOMENTO DE INÉRCIA:", GEO), ("m", r"I_{\Z}=\iiint\S^2\,\de\,dV")]
        f_top1 = mixl(P1, 120, 180, 42)                   # tamanho do topo (destino)
        f_top2 = mixl(P2, 1140, 180, 42)

        def _centrada(partes, Y, S):
            w0 = mixl(partes, 0, Y, S)
            larg = pxof(w0.get_right())[0] - pxof(w0.get_left())[0]
            return mixl(partes, (1920 - larg) / 2, Y, S)
        # R13: as duas fórmulas-resumo entram grandes e centradas (uma por linha) e só sobem para o topo em "a taça"
        fb1 = _centrada(P1, 420, 52)
        fb2 = _centrada(P2, 560, 52)
        # R14: o título troca junto da escrita da 1ª fórmula (o palco não fica só de papel na emenda B4-6 → S1)
        _novo = self._canto(txt("SÍNTESE", 21.6, color="#F5F7FF", bold=True, up=False), CANTO_Y2, topo_min=self._y1_fim_px() + 10)
        _novo._canto2 = "SÍNTESE"
        _velho = self.h2
        self.pena(fb1, extra=[FadeOut(_velho), FadeIn(_novo)])
        self.remove(_velho)
        self.h2 = _novo
        self.pena(fb2)

        # Coluna 1: A Taça
        self.gat("a taça")
        pronto(f_top1)
        pronto(f_top2)
        self.play(ReplacementTransform(fb1, f_top1), run_time=0.35)      # sobem para o topo, uma por vez (Transform simples)
        self.play(ReplacementTransform(fb2, f_top2), run_time=0.35)
        pronto(f_top1)
        pronto(f_top2)
        c1 = cartao(60, 270, 860, 330)
        ck1 = check_px(104, 324, MEN, 0.9)
        t_c1 = T("A TAÇA", 140, 335, 34, "left", GEO)
        f_c1a = TC(r"\X^2+\Y^2\le\Z\le1", 330, 465, 44, "c")
        f_c1b = TC(r"\zb=\dfrac23", 670, 465, 58, "c")
        m_c1b = caixa_men(f_c1b)
        l_c1 = leg("ACIMA DO MEIO", 490, 565, GEO, "center", 28)
        self.dentro(c1._painel, t_c1, f_c1a, f_c1b, l_c1)
        self.pena(t_c1, f_c1a, extra=[FadeIn(c1), Create(ck1)])           # o cartão nasce junto do texto (R14)
        self.pena(f_c1b, extra=[Create(m_c1b)])
        self.pena(l_c1)

        # Coluna 2: Cilindro e Bola
        self.gat("o cilindro e a bola")
        c2 = cartao(1000, 270, 860, 330)
        ck2 = check_px(1044, 324, MEN, 0.9)
        t_c2 = T("CILINDRO E BOLA", 1080, 335, 34, "left", GEO)
        f_c2a = mixl([("t", "CILINDRO:", GEO), ("m", r"I_{\Z}=\dfrac12\,MR^2")], 1040, 415, 42)
        f_c2b = mixl([("t", "BOLA:", GEO), ("m", r"I_{\Z}=\dfrac25\,MR^2")], 1040, 500, 42)
        l_c2 = leg("MAIS PERTO DO EIXO = GIRA MAIS FÁCIL", 1430, 580, GEO, "center", 26)
        self.dentro(c2._painel, t_c2, f_c2a, f_c2b, l_c2)
        self.pena(t_c2, f_c2a, f_c2b, l_c2, extra=[FadeIn(c2), Create(ck2)])

        # Coluna 3: A Lata Pesada
        self.gat("e a lata pesada")
        c3 = cartao(60, 640, 1800, 330)
        ck3 = check_px(104, 694, MEN, 0.9)
        t_c3 = T("A LATA PESADA", 140, 705, 34, "left", CI)
        f_c3a = TC(r"\de=\Ci{\sqrt{\S^2+\Z^2}}", 430, 835, 46, "c")
        f_c3b = TC(r"\zb\approx0{,}555", 960, 835, 56, "c")
        f_c3c = TC(r"I_{\Z}\approx1{,}539", 1440, 835, 56, "c")
        self.dentro(c3._painel, t_c3, f_c3a, f_c3b, f_c3c)
        self.pena(t_c3, f_c3a, f_c3b, f_c3c, extra=[FadeIn(c3), Create(ck3)])

        self._fecha(antes=0.7)
        self.sai(f_top1, f_top2, c1, ck1, t_c1, f_c1a, f_c1b, m_c1b, l_c1,
                 c2, ck2, t_c2, f_c2a, f_c2b, l_c2,
                 c3, ck3, t_c3, f_c3a, f_c3b, f_c3c, rt=0.35)
        pal = self.palco("lataParede", cam_alvo("s2"), eixo=0.0, seta=0.0)
        self.add(pal.fundo)
        self.titulo("E SE O EIXO ESTIVER NA PAREDE?", rt=0.3)

        # ── S2 · o eixo na parede e o próximo vídeo (alvo 21) ──────────────────────────────────────────────
        self.an("S2")

        self.gat("girar a lata em volta de uma reta")
        r_eixo = self.rot3(pal, "reta", "EIXO", dx=16, dy=10, size=28, ancora="l", txtp=True, cor=E1)
        t1 = T("E SE O EIXO NÃO PASSAR", COL, 200, 44)
        t2 = T("PELO CENTRO?", COL, 260, 44)
        self.play(*pal.anim(rt=0.65, eixo=1.0, seta=1.0), FadeIn(r_eixo[0]))
        self.pena(r_eixo.f, t1, t2)

        self.gat("encostada na parede")
        lg1 = leg("GIRAR A LATA EM VOLTA DE UMA RETA DA PAREDE", COL, 350, AL, "left", 30)
        self.pena(lg1)

        self.gat("No próximo vídeo")
        ct_p = cartao(1060, 500, 760, 330)
        p1 = leg("NO PRÓXIMO VÍDEO", 1440, 580, GEO, "center", 30)
        p2 = T("EXERCÍCIOS", 1440, 665, 48, "center", BR)
        p3 = T("DO MÓDULO", 1440, 735, 48, "center", SOMB)
        p4 = leg("INTEGRAL TRIPLA", 1440, 800, GEO, "center", 28)
        self.dentro(ct_p._painel, p1, p2, p3, p4)
        self.pena(p1, p2, p3, p4, extra=[FadeIn(ct_p)])         # o cartão nasce junto do texto
        self.marca("21_S2", agora=True)

        # Critério 20 (§8 PS e §9.1): cartão permanece visível por ≥ 8 segundos antes do CTA entrar
        self.wait(8.2)
        cta43(self)
