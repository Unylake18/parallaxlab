"""yt_0044 · Lote PS: S1 (a receita e os cinco erros, alvo 25) e S2 (a hélice na lata e o próximo vídeo, alvo 26) + CTA."""
from k44 import *  # noqa: F401,F403

COL = 1020


class PS(B44):
    ANTES = "A BOLA ENCOSTADA E O ERRO CLÁSSICO"

    def corpo(self):
        # ── S1 · síntese: a receita e os cinco erros (alvo 25) ────────────────────────────────────────────────
        self.an("S1")
        self.titulo("A RECEITA E OS CINCO ERROS", rt=0.3)
        # os exemplos não estão mais na tela neste lote (as fontes ficaram nos lotes E1–E5): reescritos a caneta (handoff §7, S1)
        R = [("ONDE ESTÁ O CORPO?", [("t", "A SOMBRA DO TETRAEDRO", SOMB)]),
             ("QUAL SISTEMA?", [("m", r"\Js"), ("t", "NO CONE ·", GEO), ("m", r"\Jr"), ("t", "NA MEIA BOLA", GEO)]),
             ("ENTRA E SAI", [("t", "SAI NO PLANO:", GEO), ("m", r"\Co{\Z=1-\X-\Y}")]),
             ("CONFERIR", [("t", "RIEMANN · CENTROIDE · ESFÉRICAS · FATIAS · POLO", MEN)])]
        gats = ["fechar", "o fator s no cone", "a sonda que sai", "uma conferência em todo exercício"]
        S1m = []
        for i, ((a, ex), g) in enumerate(zip(R, gats)):
            self.gat(g)
            ct = cartao(80, 170 + i * 190, 800, 160)
            nn = num(i + 1, 128, 214 + i * 190, 38)
            ta = T(a, 160, 225 + i * 190, 32, "left", BR)
            exm = mixl(ex, 110, 285 + i * 190 - 26 * .27, 30)
            self.dentro(ct._painel, nn, ta, exm)
            self.pena(nn, ta, extra=[FadeIn(ct)])
            if i < 3:
                self.pena(exm)
            self.col("S1a", ta, exm)
            S1m += [ct, nn, ta, exm]

        self.gat("E os cinco erros")
        tE = T("OS CINCO ERROS", 1000, 215, 40, "left", AL)
        self.pena(tE, S1m[-1])                 # o exemplo do cartão ④ termina junto do título dos erros
        ERR = ["ESQUECER O FATOR (s, r² sen φ)", "USAR r (ATÉ A ORIGEM) NO LUGAR DE s", "CHUTE DO CENTRO COM ρ NÃO LINEAR", "STEINER ENTRE EIXOS FORA DO CM",
               "ACHAR QUE TAMPA E COSTURA CONTAM"]
        for i, (t, g) in enumerate(zip(ERR, ["o fator", "a distância errada", "o chute do centro", "o Steiner", "a tampa"])):
            self.gat(g)
            cz = cruz_px(1020, 310 + i * 120, AL, .9)
            le = leg(t, 1060, 320 + i * 120, BR, "left", 30)
            self.play(Create(cz), run_time=0.3)
            self.pena(le)
            self.col("S1b", le)
            S1m += [cz, le]
        self.marca("25_S1")
        pal = self.palco("helice", OL, helice=0.0, conta=0.0, F=0.0)
        rz = self.rot3(pal, "ez", r"\Z", size=38, ancora="c")
        self.sai(*S1m, tE, rt=0.35, extra=self.ent3d(pal))

        # ── S2 · o caminho em volta da lata e o próximo vídeo (alvo 26) ──────────────────────────────────────
        self.an("S2")
        self.titulo("E SE A SOMA FOR AO LONGO DE UM CAMINHO?", rt=0.3)

        self.gat("a massa morava num volume")
        l1 = leg("ATÉ AQUI: A MASSA MORAVA NUM VOLUME", COL, 190, GEO, "left", 30)
        self.pena(rz, l1)
        self.col("S2", l1)

        self.gat("uma hélice enrolada na parede da lata")
        sqH, lqH = legq(HEL, "HÉLICE NA PAREDE DA LATA", 120, 1020, 30)
        self.play(*pal.anim(2.2, helice=1.0), FadeIn(sqH), run_time=2.2)
        self.pena(lqH)
        l2 = mixl([("t", "HÉLICE:", GEO), ("m", r"\S=R,\ \ \T=t,\ \ \Z=c\,t")], COL, 280, 42)
        self.pena(l2)
        self.col("S2", l2)

        self.gat("uma conta de colar")
        rF = self.rot3(pal, "F", r"\vec F", size=32, ancora="l", dx=14, dy=-6)
        MENTA = "#2EE6A0"   # F5: cor do campo F na série
        rF.f.set_color(MENTA)
        sqF, lqF = legq(MENTA,"A FORÇA EMPURRA A CONTA", 560, 1020, 30)
        pal.set(conta=1.0)
        self.play(*pal.anim(0.8, F=1.0), FadeIn(sqF), run_time=0.8)
        self.pena(rF, lqF)

        self.gat("quanto trabalho")
        l3 = T("QUANTO TRABALHO A FORÇA", COL, 380, 40, "left", BR)
        l4 = T("FAZ NESSA VOLTA?", COL, 435, 40, "left", BR)
        self.pena(l3, l4)
        self.col("S2", l3, l4)

        self.gat("No próximo vídeo")
        ct = cartao(1060, 530, 760, 330)
        p1 = leg("NO PRÓXIMO VÍDEO", 1440, 605, GEO, "center", 30)
        p2 = T("INTEGRAIS", 1440, 690, 52, "center", BR)
        p3 = T("DE LINHA", 1440, 760, 52, "center", HEL)
        p4 = leg("O CAMPO AO LONGO DA CURVA", 1440, 820, GEO, "center", 28)
        self.dentro(ct._painel, p1, p2, p3, p4)
        self.pena(p1, p2, p3, p4, extra=[FadeIn(ct)])         # o cartão nasce junto do texto
        self.marca("26_S2", agora=True)
        # critério 20: o cartão fica ≥ 8 s antes do CTA (a fala do desafio e do "deixa nos comentários" corre por cima; nada se escreve na tela)
        self.wait(8.2)
        cta43(self)
