"""Lote PH · H gancho (alvo 03 v1 + v2_h2) + A bem-vindos (alvos 01 v1 + v2_ab2). v2: as fórmulas em caneta em "Três fórmulas"; redes e fantasmas em
"três quadradinhos"; o título em três pedaços; traço GEO sob cada fórmula em "só olhando a fórmula"; '?' coral nos fantasmas; A FÓRMULA JÁ SABE. No
"por que o campo magnético", os três cartões saem e entram dois: o fio (α = 1) e a carga; |B| ∝ 1/r, |E| ∝ 1/r²; rot B = 0 e div E = 0. A: cinco
linhas de NESTE VÍDEO, uma por trecho; PAUSE E TENTE; o canto e o logo do canto entram no fim."""
from alg30 import *  # noqa: F401,F403

CARTOES = [(0, F1, r"\F=(\X+\Y,\ \X-\Y)", (0, 0), 1.6, 4), (1, F2, r"\F=(1,\ \X-\Y)", (0, 0), 1.6, 4), (2, F3, r"\F=(\X^2-\Y^2,\ 2\X\Y)", (1, 1), 1.2, 8)]


def cartao_h(i):
    k, Fv, tex, c, s, mm = CARTOES[i]
    X0 = CC[k][0]
    v = VB(CC[k], X0 + 240, 540, 56)
    ch = chapa_px(*CC[k], nome=f"H cartão {k + 1}", v=v)
    cmp = campo30(v, Fv, -3.5, 3.5, -3.5, 3.5, .75, rmin=0, mmax=mm, skip=dq(c, s), nome=f"H cartão {k + 1}")
    fan = fantasma(v, quad_pts(c, s))
    f = TC(tex, X0 + 240, 840, 36, "c")
    q = T("?", *canto_xy(v, *c), 40, "center", CORAL)
    q.move_to(PX(*canto_xy(v, *c)))
    return VGroup(ch, cmp, fan), f, q


def cartao_fio():
    v = Vista(600, 540, 60)
    ch = chapa_px(360, 300, 840, 780, nome="H fio", v=v)
    cmp = campo30(v, VORTA(1), -3.75, 3.75, -3.75, 3.75, .75, rmin=.7, mmax=1.6, nome="H fio α = 1")
    fio = VGroup(preenche(v, circ_pts(.32), "#0F0C26", 1.0, 10), vcirc(v, .32, BR, 3).set_z_index(11), ponto7(v.c2p(0, 0), BR, 5, 12))
    return VGroup(ch, cmp, fio, T("FIO COM CORRENTE", 600, 838, 30, "center"))


def cartao_carga():
    v = Vista(1320, 540, 60)
    ch = chapa_px(1080, 300, 1560, 780, nome="H carga", v=v)
    cmp = campo30(v, F_CARGA, -3.75, 3.75, -3.75, 3.75, .75, rmin=.9, mmax=.9, nome="H carga")
    cg = VGroup(preenche(v, circ_pts(.45), CARGA, 1.0, 10), T("+", 1320, 553, 34, "center").set_z_index(12))
    return VGroup(ch, cmp, cg, T("CARGA", 1320, 838, 30, "center"))


class LoteH(Base):
    CANTO = False

    def corpo(self):
        # ── H · gancho ──
        self.an("H-1")
        zera_chapas()
        cs = [cartao_h(i) for i in range(3)]
        for k in range(3):
            cs[k][1]._origem = "a"
            print(f"[origem] a {self.lote} H-1 0.00 {cs[k][1]._tex!r}")
        self.play(*[caneta(cs[k][1], ritmo=0.1, atraso=0.1 * k) for k in range(3)], run_time=0.55)
        self.gat("três quadradinhos de fluido")
        self.play(LaggedStart(*[FadeIn(cs[k][0]) for k in range(3)], lag_ratio=0.45), run_time=1.2)
        ts = [T("QUAL GIRA?", 0, 215, 40), T("QUAL MUDA DE ÁREA?", 0, 215, 40), T("QUAL ENTORTA?", 0, 215, 40)]
        gap = 16 / 120
        tot = sum(t.width for t in ts) + 2 * gap
        x = -tot / 2
        for t in ts:
            t.shift(RIGHT * (x - t.get_left()[0]))
            x += t.width + gap
            t._tex = t.text if hasattr(t, "text") else "título"
        for t, fr in zip(ts, ("um vai girar", "outro vai mudar de área", "e um vai entortar")):
            self.gat(fr)
            self.play(caneta(t, ritmo=0.1))
        tr = []
        for k in range(3):
            f = cs[k][1]
            tr.append(linha7([f.get_corner(DL) + DOWN * 8 / 120, f.get_corner(DR) + DOWN * 8 / 120], GEO, 2))
        self.gat("só olhando a fórmula")
        for t in tr:
            self.play(Create(t), run_time=0.4)
        self.gat("antes de soltar o fluido")
        self.play(*[FadeIn(c[2], scale=0.6) for c in cs], run_time=0.4)
        fs_ = legenda("A FÓRMULA JÁ SABE", 960, 930, GEO, "center", 30)
        self.gat("dá e hoje")
        self.play(caneta(fs_, ritmo=0.2))
        zera_chapas()
        fio, carga = cartao_fio(), cartao_carga()
        t2 = T("POR QUE 1/r? POR QUE 1/r²?", 960, 215, 40, "center", up=False)
        self.gat("por que o campo magnético")
        troca(self, "H três cartões → fio e carga")
        sai = [m for c in cs for m in c] + ts + tr + [fs_]
        self.play(*[FadeOut(m) for m in sai], FadeIn(t2), FadeIn(fio), run_time=0.6)
        self.remove(*sai)
        b1 = TC(r"|\B|\propto\dfrac1r", 600, 905, 36, "c")
        self.gat("com um sobre a distância e")
        escreve(self, b1, 0.3)
        self.gat("e o campo de uma carga")
        self.play(FadeIn(carga), run_time=0.6)
        e1 = TC(r"|\E|\propto\dfrac1{r^2}", 1320, 905, 36, "c")
        self.gat("ao quadrado não")
        escreve(self, e1, 0.3)
        rb, de = TC(r"\V{\rot\B=0}", 600, 990, 34, "c"), TC(r"\D{\dv\E=0}", 1320, 990, 34, "c")
        self.gat("é o rotacional e o divergente")
        escreve(self, rb, 0.25)
        escreve(self, de, 0.25)
        self.ate(1.0)

        # ── A · bem-vindos (alvos 01 v1 e v2_ab2) ──
        self.an("A-1")
        LC = (960, 420)
        logo = self.logo(668 / 120).move_to(PX(*LC))
        aneis = VGroup(*[DashedVMobject(Circle(radius=r / 120).move_to(PX(*LC)), num_dashes=int(2 * PI * r / 20)).set_stroke(GEO, 2 / 1.2, opacity=0.45)
                         for r in (668 * .467, 668 * .434)])
        for m in aneis.get_family():
            m._sem_contorno = True
        bv = T("BEM-VINDOS AO PARALLAX LAB", 960, 850, 46, "center")
        self.limpa_junto()
        troca(self, "H → A (abertura)")
        self.play(FadeIn(logo, scale=0.94), FadeIn(aneis), FadeIn(bv, shift=0.1 * UP), FadeOut(self.wm), run_time=0.8)
        self.remove(self.wm)
        gira = lambda rt: (Rotate(aneis[0], 0.12 * rt, about_point=aneis[0].get_center(), rate_func=linear),
                           Rotate(aneis[1], -0.1 * rt, about_point=aneis[1].get_center(), rate_func=linear))

        def ate_frase(fr):
            rt = self.falta(fr)
            if rt >= 0.2:
                self.play(*gira(rt), run_time=rt)
            self.gat(fr)

        cal = T("CÁLCULO III", 960, 478, 28, "center", GEO, bold=False)
        tit = T("EXERCÍCIOS DO MÓDULO", 960, 566, 54, "center")
        nv = T("NESTE VÍDEO:", 960, 640, 30, "center", CAMPO)

        def duo(a, b, y):
            pa = T(a, 0, y, 32, "left")
            pp = T("·", 0, y, 32, "left", GEO, bold=False)
            pb = T(b, 0, y, 32, "left", CAMPO2, bold=False)
            pp.move_to([pa.get_right()[0] + 11 / 120 + pp.width / 2, pa.get_center()[1], 0])
            pb.shift(RIGHT * (pp.get_right()[0] + 11 / 120 - pb.get_left()[0]))
            g = VGroup(pa, pp, pb)
            return g.shift(RIGHT * (PX(960, 0)[0] - g.get_center()[0]))
        LIN = [("DOIS FILMES", "TRANSFORMAÇÃO E CAMPO", "primeiro ler uma fórmula"), ("REDEMOINHOS", "ROT, DIV E DUAS REGRAS", "depois uma família inteira"),
               ("DE PERTO", "LIMITE, CONTINUIDADE E PARCIAIS", "aí vem um campo"), ("O DESAFIO", "PREVER O QUADRADINHO", "no topo da escada"),
               ("AS APLICAÇÕES", "RIO, PAREDE, MAPAS E FIOS", "na segunda parte")]
        linhas = [duo(a, b, 705 + i * 52) for i, (a, b, _) in enumerate(LIN)]
        ate_frase("esse é o quarto episódio")
        k = 380 / 668
        Lg = Group(logo, aneis)
        self.play(Lg.animate.scale(k).move_to(PX(960, 250)), FadeOut(bv), FadeIn(cal, shift=0.06 * UP), run_time=1.0)
        self.remove(bv)
        ate_frase("o integrador do módulo")
        self.play(FadeIn(tit, shift=0.06 * UP), *gira(0.5), run_time=0.5)
        ate_frase("vai ser uma escada")
        self.play(FadeIn(nv, shift=0.06 * UP), *gira(0.5), run_time=0.5)
        for (a, b, fr), m in zip(LIN, linhas):
            ate_frase(fr)
            self.play(FadeIn(m, shift=0.06 * UP), *gira(0.5), run_time=0.5)
        ate_frase("pausa o vídeo e tenta")
        self.pausa(dur=min(3.0, self.resta() - 0.9))
        self.play(FadeIn(self.h1), FadeIn(self.wm), *gira(0.5), run_time=0.5)     # o canto e o logo do canto entram no fim da abertura (R10)
        rt = self.resta()
        if rt >= 0.2:
            self.play(*gira(rt), run_time=rt)
        self.sai_fim()
