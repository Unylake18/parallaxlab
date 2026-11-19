"""yt_0042 · B3 · o teorema e a receita. B3-1 (alvo 10): caixa + lata em cima (3D liso numa faixa), o painel do enunciado embaixo; glyph map 5
(teorema geral → fórmula das cilíndricas, o s lima voa do chip dV). B3-2 (sem alvo): o 3D `deslocadoSonda` parado à esquerda; selos ①②③ e as três linhas
da receita."""
from k42 import *
from sec_b1 import depois


class PB3(B42):
    ANTES = "O TEOREMA"

    def corpo(self):
        # ── B3-1 ──────────────────────────────────────────────────────────────────────────────────────────
        self.an("B3-1")
        self.papel_on(rt=0)
        cx = self.palco("caixa", cam_alvo("b31a"), celula=0.0, eixo=0.0, costura=0.0, meia=0.0, sep=0.0)
        lg = self.palco("latagrade", cam_alvo("b31b"), celula=0.0, eixo=0.0, costura=0.0)
        self.add(cx.fundo, lg.fundo)
        st = seta_px((470, 330), (640, 330), GEO, 4, 18)
        tt = TC(r"T", 555, 292, 40, "c")
        self.play(Create(st), run_time=0.4)
        self.pena(tt)
        self.gat("agora o enunciado")
        pn = painel2d41(60, 600, 1800, 432)
        self.play(Create(pn), run_time=0.5)
        teo = L([("t", r"\iiint_B f(\X,\Y,\Z)\,\dX\,\dY\,\dZ=\iiint_{B_{uvw}} f\big(T(u,v,w)\big)\Big|\dfrac{\partial(\X,\Y,\Z)}{\partial(u,v,w)}\Big|\,du\,dv\,dw")],
                100, 680, 40)
        self.pena(teo)
        self.degrau("C5", "teorema geral de mudança de variáveis")
        self.gat("as exigências são no interior")
        ni = leg("NO INTERIOR: T DE CLASSE C¹, INJETORA, JACOBIANO ≠ 0", 100, 775, GEO, "left", 28)
        self.pena(ni)
        self.gat("onde isso falha")
        self.play(cx.tr["eixo"].animate(rate_func=linear).set_value(1.0), lg.tr["eixo"].animate(rate_func=linear).set_value(1.0),
                  cx.tr["costura"].animate(rate_func=linear).set_value(1.0), lg.tr["costura"].animate(rate_func=linear).set_value(1.0), run_time=0.8)
        nl = mixl([("t", "NA LATA:", GEO), ("m", r"\S=0"), ("t", "→ JACOBIANO 0 ·", GEO), ("m", r"\T=0,\ 2\pi"), ("t", "→ NÃO INJETORA", GEO)], 100, 835, 30)
        self.pena(nl)
        self.degrau("C5", "s = 0 → jacobiano 0; θ = 0, 2π → não injetora")
        self.gat("a lata entra em duas metades")
        self.play(cx.tr["meia"].animate(rate_func=linear).set_value(1.0), cx.tr["sep"].animate(rate_func=smooth).set_value(0.15), run_time=0.8)
        mt = L([("m", r"\T\in[0,\pi]\ +\ \T\in[\pi,2\pi]")], 1240, 440, 40)
        self.pena(mt)
        self.degrau("C5", "θ∈[0,π] + θ∈[π,2π]")
        self.play(cx.tr["sep"].animate(rate_func=smooth).set_value(0.0), run_time=0.8)
        self.gat("trocando o jacobiano por s")
        fo = L([("f", r"\iiint_B f(\X,\Y,\Z)\,\dX\,\dY\,\dZ=\iiint_{B_{\S\T\Z}} f(\S\cos\T,\ \S\sen\T,\ \Z)\,\Js\,\dS\,\dT\,\dZ")], 100, 945, 44)
        self.gm(5, teo, fo, [], copia=False, nota="teorema geral → fórmula das cilíndricas (o s lima)")
        self.degrau("C5", "fórmula das cilíndricas com o s lima")
        self.col("B3-1", teo, ni, nl, mt, fo, chips=1)
        self.marca("10_B3-1")

        # ── B3-2 ──────────────────────────────────────────────────────────────────────────────────────────
        self.an("B3-2")
        self.titulo("A RECEITA: SOMBRA E SONDA", rt=0.3)
        saem = [m for m in self.mobjects if m not in self.fixos() and not isinstance(m, ValueTracker) and m is not self.clk and m is not self.grade]
        self.play(*[FadeOut(m) for m in saem], run_time=0.5)
        self.remove(*saem)
        self.col_zera("B3-1")
        ds = self.palco("deslocadoSonda", cam_alvo("b41"), sombra=0.0, sonda=0.0, eixoNovo=1.0)
        ds.fundo.op.set_value(0.0)
        self.add(ds.fundo)
        self.play(ds.fundo.op.animate.set_value(1.0), run_time=0.6)
        self.gat("primeiro, a sombra")
        s1m, s1t = selo("①", 1010, 330, GEO, 30)
        self.play(ds.tr["sombra"].animate(rate_func=linear).set_value(1.0), Create(s1m), run_time=0.7)
        t1a = leg("A SOMBRA NO CHÃO, EM POLARES", 1090, 320, BR, "left", 28)
        f1 = L([("f", r"\alpha\le\T\le\beta,\ s_1(\T)\le\S\le s_2(\T)")], 1090, 375, 40)
        self.pena(s1t, t1a, f1, lag=0.15)
        self.degrau("C5b", "① a sombra no chão em polares")
        self.gat("segundo, a sonda em pé")
        s2m, s2t = selo("②", 1010, 470, GEO, 30)
        self.play(ds.tr["sonda"].animate(rate_func=linear).set_value(1.0), Create(s2m), run_time=0.9)
        t2a = leg("A SONDA EM PÉ: PISO → TETO", 1090, 460, BR, "left", 28)
        f2 = L([("f", r"g_1(\S,\T)\le\Z\le g_2(\S,\T)")], 1090, 515, 40)
        self.pena(s2t, t2a, f2, lag=0.15)
        self.degrau("C5b", "② a sonda em pé")
        self.gat("terceiro, monta")
        s3m, s3t = selo("③", 1010, 610, GEO, 30)
        self.play(Create(s3m), run_time=0.5)
        f3 = L([("i", r"\int_{\alpha}^{\beta}\!\int_{s_1}^{s_2}\!\int_{g_1}^{g_2} f\cdot\Js\,\dZ\,\dS\,\dT")], 1090, 600, 40)
        self.pena(s3t)
        self.pena(parte(f3, sel(f3, ["i"]), "③ monta: ∫∫∫ f·s dz ds dθ"))
        self.degrau("C5b", "③ monta a integral")
        self.col("B3-2", t1a, f1, t2a, f2, f3)
        self.sai_fim()
