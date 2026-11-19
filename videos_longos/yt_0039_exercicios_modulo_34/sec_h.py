"""yt_0039 · H · a chapa e o buraco (alvo 01) + os cinco passos. H1: a meia arruela nasce do meio disco de raio 2 (o de raio 1 sai, contorno
tracejado); MEIA ARRUELA e HOMOGÊNEA em placas; o eixo y acende (SIMETRIA); o ⊕ com ? anda no eixo (ValueTracker) e para perto da borda do buraco,
sem número; a borda r = 1 em ALERTA e BURACO; o mapa ρ = k r pinta a chapa (MAIS PESADA NA BORDA) e o ⊕ pula; os ícones bola e bola oca com
SEM INTEGRAL. H2: cartão (grade passo 0,5) com os cinco passos a caneta e o painel ȳ = M_x/m."""
from k39 import *

VH = Vw(960, 820, 220)


class PH(B39x):
    ANTES = "A CHAPA E O BURACO"

    def corpo(self):
        v = VH
        self.an("H1")
        P = monta_palco(self, v, -2.55, 2.6, -.05, 2.55, ticks=[("x", -2, r"\Am{-2}"), ("x", -1, r"\Am{-1}"), ("x", 1, r"\Am{1}"), ("x", 2, r"\Am{2}")])
        self.gat("olha esta chapa")
        md = poly_px([v.px(*p) for p in arcoP(2)], FUNDO_R, 1.0, z=1)
        b2 = lin_px([v.px(*p) for p in arcoP(2)], GEO, 3, z=5)
        self.play(FadeIn(md), Create(b2), run_time=1.0)
        self.gat("arrancado do meio")
        furo = poly_px([v.px(*p) for p in arcoP(1)], FUNDO_R, 1.0, z=2)
        tr = lin_px([v.px(*p) for p in arcoP(1)], GEO, 3, dash=(10, 8), z=6)
        self.add(furo)
        self.play(Create(tr), run_time=0.6)
        ar = arruela(v)
        self.add(ar)
        self.remove(md)
        self.play(furo.animate.shift(UP * 0.0).set_opacity(0), run_time=0.8)
        self.remove(furo)
        self.gat("Sobrou uma meia arruela")
        lm = placa_t("MEIA ARRUELA", *v.px(1.35, 1.75), BR, 30)
        self.pena(lm)
        self.gat("e ela é homogênea")
        lh = placa_t("HOMOGÊNEA", *v.px(1.55, 1.5), GEO, 26)
        self.pena(lh)
        self.gat("onde ficaria o ponto")
        tit = T("O CENTRO DE MASSA CAI NO BURACO?", 960, 200, 44, "center")
        self.pena(tit, passo=0.03)
        self.gat("pela simetria")
        sim = lin_px([v.px(0, 0), v.px(0, 2.3)], BR, 2, dash=(8, 8), z=7)
        ls = leg("SIMETRIA", *v.px(.06, 2.28), GEO, "left", 26)
        self.play(Create(sim), run_time=0.6)
        self.pena(ls)
        self.gat("mas em que altura")
        yv = ValueTracker(0.6)
        pc = cm(*v.px(0, .6), 16)
        q = T("?", *v.px(1.15, .6), 44, "center", BR)
        pc.add_updater(lambda m: m.move_to(v.P(0, yv.get_value())))
        q.add_updater(lambda m: m.move_to(v.P(1.15, yv.get_value())))   # C9: o ? vai na chapa, à direita do arco de dentro e abaixo do de fora (≥ 14 px de todo traço)
        self.add(yv)
        self.play(FadeIn(pc, scale=.6), run_time=0.4)
        self.pena(q)
        self.play(yv.animate(rate_func=there_and_back).set_value(1.4), run_time=2.4)
        self.play(yv.animate.set_value(1.0), run_time=1.0)
        self.gat("menos de um")
        borda = lin_px([v.px(*p) for p in arcoP(1)], AL, 3, dash=(10, 8), z=6)
        bur = lin_px([v.px(0, .04), v.px(0, .97)], AL, 7, alpha=.85, z=7)
        self.play(ReplacementTransform(tr, borda), Create(bur), run_time=0.7)
        lb = placa_t("BURACO", *v.px(-.62, .5), AL, 28, "c")
        self.pena(lb)
        self.gat("a borda de fora fosse mais pesada")
        mp = meia_lua_mapa(v, 1, 2, lambda r: r, 2.0, z=2)
        lr = rot_m(v, r"\rr=\kk\,r", (-2.45, 2.25), 0, 0, 30, "l")
        lp = leg("MAIS PESADA NA BORDA", *v.px(-2.45, 2.03), CI, "left", 26)
        self.play(FadeIn(mp), lm.animate.set_opacity(0), lh.animate.set_opacity(0), run_time=1.0)
        self.pena(lr, lp, lag=0.1)
        self.gat("sobe de volta")
        self.play(yv.animate(rate_func=there_and_back).set_value(1.22), run_time=1.2)
        self.gat("hoje a gente responde")
        self.play(FadeOut(mp), FadeOut(lr), FadeOut(lp), lm.animate.set_opacity(1), lh.animate.set_opacity(1), run_time=0.8)
        self.remove(mp, lr, lp)
        self.gat("uma bola e uma bola")
        ib = icone_bola(1600, 940)
        io = icone_bola(1730, 940, oca=True)
        self.play(Create(ib), Create(io), run_time=0.9)
        si = leg("SEM INTEGRAL", 1665, 1018, GEO, "center", 26)
        self.pena(si)
        self.marca("01_H1")
        self._fecha(antes=0.4)
        pc.clear_updaters()
        q.clear_updaters()
        self.limpa_tudo(rt=0.4)

        # ── H2 · cinco passos e uma divisão (cartão) ──
        self.an("H2")
        self.secao("CINCO PASSOS E UMA DIVISÃO")
        self.grade = papel_cartao()
        pn = painel(1220, 330, 600, 400)
        self.play(FadeIn(self.grade), run_time=0.4)
        self.gat("cinco passos e")
        itens = [
            [("t", "ESCOLHER AS VARIÁVEIS NOVAS")],
            [("t", "ESCREVER"), ("m", r"x,\ y"), ("t", "EM FUNÇÃO DELAS")],
            [("t", "JACOBIANO, EM MÓDULO"), ("m", r"\Jl{|J|}")],
            [("t", "DESENHAR A REGIÃO NOVA")],
            [("t", "CALCULAR E CONFERIR")],
        ]
        gats = ["escolher as variáveis", "x e y em função", "calcular o jacobiano", "desenhar a região nova", "calcular e conferir"]
        Y0, DY, XN = 330, 110, 260
        oks = None
        for i, (it, gg) in enumerate(zip(itens, gats)):
            self.gat(gg)
            Y = Y0 + i * DY
            c = circ_px(XN, Y, 26, GEO, 2.5, z=6)
            n_ = T(str(i + 1), XN, Y + 11, 30, "center", E1)
            ln = mixl(it, XN + 50, Y, 36)
            for x_ in c.get_family():
                x_._guia_de = n_
            self.play(Create(c), run_time=0.3)
            self.pena(n_, *ln.p, lag=0.04)
            if i == 4:
                oks = check_px(pxof(ln.get_right())[0] + 34, Y, MEN, 1.0)
                self.play(Create(oks), run_time=0.4)
        self.gat("uma divisão só")
        t1 = T("CENTRO DE MASSA", 1520, 420, 32, "center", GEO, bold=False)
        self.pena(t1, extra=[Create(pn)])
        self.gat("momento sobre massa")
        f = LL([("yb", r"\yb"), ("eq", "="), ("fr", r"\dfrac{\Mx}{\mm}")], 1520, 540, 56, "c")
        self.pena(f)
        t2 = T("MOMENTO ÷ MASSA", 1520, 670, 30, "center", BR, bold=False)
        self.pena(t2)
        self.sai_fim()
