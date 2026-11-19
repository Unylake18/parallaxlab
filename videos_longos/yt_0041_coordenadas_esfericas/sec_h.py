"""yt_0041 · H · a bola pesada na casca (H1, alvo 01) e a grade nova (H2, alvo 02).
H1: a bola com o degradê gira ~40° e para; a cunha de 90° abre; só então a caneta escreve a coluna (DENSIDADE, MASSA, a integral cartesiana limite a
limite de fora para dentro, a primitiva de dentro, COM k², TRAVA). H2: a bola perde o degradê (a mesma geometria em traço), entram a casca, o cone e a
página uma por vez, saem, ficam as duas células lima com "?"; o canto troca para QUAL É O VOLUME DE CADA PEDAÇO?."""
from k41 import *


class PH(B41):
    ANTES = "A BOLA PESADA NA CASCA"

    def corpo(self):
        # ── H1 ────────────────────────────────────────────────────────────────────────────────────────────
        self.an("H1")
        self.papel_on(rt=0)                                                     # G1: o papel fica também atrás do 3D
        cb = cam_alvo("h1")
        bola = self.palco("bola", cb, giro=-40.0, cunha=0.0, casca084=0.0)
        rx = self.rot3(bola, "ex", r"\X", dx=18, dy=14, size=38)
        ry = self.rot3(bola, "ey", r"\Y", dx=18, dy=-6, size=38)
        rz = self.rot3(bola, "ez", r"\Z", dx=28, dy=-6, size=38)            # o z sai de cima (margem de 48 px), ao lado da ponta da seta
        self.add(bola.fundo)                                                    # a bola já está no 1º quadro (nenhum bloco abre vazio)
        self.gat("pensa numa bola")
        self.pena(rx, ry, rz, lag=0.15)
        self.play(bola.tr["giro"].animate(rate_func=smooth).set_value(0.0), run_time=2.6)     # ~40° e para no quadro do alvo
        self.play(bola.tr["cunha"].animate(rate_func=smooth).set_value(1.0), run_time=1.2)    # a cunha abre: o degradê por dentro
        self.gat("mais densa que a de dentro")
        sq1, t1_ = legq("#5FA8C8", "LEVE NO CENTRO: ρ = 0", 120, 1020)
        sq2, t2_ = legq(CI, "PESADA NA CASCA: ρ = 1", 540, 1020)
        lv, ps = VGroup(sq1, t1_), VGroup(sq2, t2_)
        lv._txt, ps._txt = "LEVE NO CENTRO", "PESADA NA CASCA"
        self.pena(t1_, extra=[Create(sq1)])
        self.pena(t2_, extra=[Create(sq2)], lag=0.3)
        self.degrau("H1", "bola em octante com degradê; legenda LEVE NO CENTRO / PESADA NA CASCA")

        self.gat("que aqui a gente chama de rô")
        den = mixl([("t", "DENSIDADE", CI), ("L", [("rho", r"\de"), ("eq", "="), ("f", r"\sqrt{\X^2+\Y^2+\Z^2}")])], 1020, 180, 52)
        self.pena(den)
        self.col("H1", den)
        self.degrau("H1", "DENSIDADE ρ = √(x²+y²+z²)")

        self.gat("quanto pesa")
        ms = mixl([("t", "MASSA", BR), ("L", [("eq", "="), ("int", r"\iiint_B"), ("f", r"\Ci{\sqrt{\X^2+\Y^2+\Z^2}}"), ("dv", r"\;dV")])], 1020, 300, 52)
        self.pena(ms.p[0])
        self.escreve(ms.p[1], voos=[(gl(den.p[1], "f"), "f")], nota="H1: o integrando da massa voa da densidade")
        self.col("H1", ms)
        self.degrau("H1", "MASSA = ∭_B √(x²+y²+z²) dV")

        self.gat("então vamos tentar do jeito")
        car = L([("eq", "="), ("i1", r"\int_{-1}^{1}"), ("i2", r"\int_{-\sqrt{1-\X^2}}^{\sqrt{1-\X^2}}"),
                 ("i3", r"\int_{-\sqrt{1-\X^2-\Y^2}}^{\sqrt{1-\X^2-\Y^2}}"), ("f", r"\Ci{\sqrt{\X^2+\Y^2+\Z^2}}"), ("dz", r"\;\dZ"), ("dy", r"\,\dY"),
                 ("dx", r"\,\dX")], 1020, 480, 36)
        poe_parte(self, car)
        self.voos([(gl(ms.p[1], "f"), parte(car, sel(car, "f"), "integrando"))], rt=0.9, nota="H1: o integrando desce da massa")
        self.pena(parte(car, sel(car, "eq"), "="))
        self.gat("o x vai de menos um a um")
        self.pena(parte(car, sel(car, ["i1", "dx"]), "x"))
        self.degrau("H1", "limite de fora: x de −1 a 1")
        self.gat("mas o y já depende")
        self.pena(parte(car, sel(car, ["i2", "dy"]), "y"))
        self.degrau("H1", "limite do meio: y entre ∓√(1−x²)")
        self.gat("e o z depende dos dois")
        self.pena(parte(car, sel(car, ["i3", "dz"]), "z"))
        self.degrau("H1", "limite de dentro: z entre ∓√(1−x²−y²)")
        self.col("H1", car)

        self.gat("a integral de dentro")
        pr = L([("i", r"\int"), ("f", r"\Ci{\sqrt{k^2+\Z^2}}"), ("dz", r"\,\dZ"), ("eq", "="), ("m", r"\dfrac12"), ("a", r"\Big["),
                ("t1", r"\Z\sqrt{k^2+\Z^2}"), ("mais", "+"), ("t2", r"k^2\ln\!\big(\Z+\sqrt{k^2+\Z^2}\big)"), ("b", r"\Big]")], 1020, 660, 36)
        poe_parte(self, pr)
        self.pena(parte(pr, sel(pr, ["i", "f", "dz", "eq"]), "lado esquerdo"))
        self.gat("chama x ao quadrado")
        com = mixl([("t", "COM", GEO), ("m", r"k^2=\X^2+\Y^2")], 1020, 780, 36)
        self.pena(com)
        self.gat("essa primitiva você até acha")
        self.pena(parte(pr, sel(pr, ["m", "a"]), "1/2 ["))
        self.gat("numa tabela")
        self.pena(parte(pr, sel(pr, ["t1"]), "z√"))
        self.gat("mas olha o tamanho dela")
        self.pena(parte(pr, sel(pr, ["mais", "t2", "b"]), "k² ln"))
        self.col("H1", pr, com)
        self.degrau("H1", "primitiva de dentro: ½[z√(k²+z²) + k² ln(z + √(k²+z²))] com k² = x²+y²")

        self.gat("tem raiz tem logaritmo")
        lg_ = leg("RAIZ E LOGARITMO JÁ NA DE DENTRO", 1190, 900, AL, "left", 30)
        self.pena(lg_)
        self.gat("trava")
        mol, tt = selo("TRAVA", 1020, 900, AL, 32)
        self.pena(tt, extra=[Create(mol)])
        self.col("H1", lg_, tt)
        self.marca("01_H1")

        # ── H2 ────────────────────────────────────────────────────────────────────────────────────────────
        self.an("H2")
        coluna = VGroup(den, ms, car, pr, com, lg_, tt, mol)
        cg = cam_alvo("h2")
        grade = self.palco("grade", cg, casca=0.0, cone=0.0, pagina=0.0, celulas=0.0)
        rz2 = pronto(self.rot3(grade, "ez", r"\Z", dx=14, size=32))
        self.gat("a bola é redonda")
        grade.fundo.op.set_value(0.0)
        self.add(grade.fundo)
        self.play(bola.fundo.op.animate.set_value(0.0), grade.fundo.op.animate.set_value(1.0), FadeOut(lv), FadeOut(ps), FadeOut(rx), FadeOut(ry),
                  ReplacementTransform(rz, rz2), coluna.animate.shift(UP * 1.2).set_opacity(0), run_time=1.2)
        for m in (bola.fundo, lv, ps, rx, ry, coluna):
            m.clear_updaters()
        self.remove(bola.fundo, lv, ps, rx, ry, coluna)
        self.col_zera("H1")

        self.gat("então troca a grade")
        pn = painel41(1020, 300, 840, 500, alpha=.35, fop=1.0)
        tg = T("A GRADE NOVA", 1080, 370, 30, "left", GEO)
        l1 = mixl([("t", "CASCAS", RO), ("m", r"\R=\text{cte}")], 1080, 460, 40)
        l2 = mixl([("t", "CONES", FI), ("m", r"\F=\text{cte}")], 1080, 540, 40)
        l3 = mixl([("t", "PÁGINAS", TH), ("m", r"\T=\text{cte}")], 1080, 620, 40)
        for (fr, ln, k) in (("cascas uma dentro da outra", l1, "casca"), ("cones saindo", l2, "cone"), ("e páginas", l3, "pagina")):
            self.gat(fr)
            if k == "casca":                                  # D9: o painel só aparece com a primeira linha
                self.play(Create(pn), run_time=0.4)
                self.pena(tg)
                self.dentro((1020, 300, 1860, 800), tg)
            self.pena(ln, extra=[grade.tr[k].animate(run_time=0.7, rate_func=linear).set_value(1.0)])
            self.dentro((1020, 300, 1860, 800), ln)
            self.degrau("H2", f"família {k} + linha")
        self.gat("repara nestes dois pedaços")
        self.play(*grade.anim(rt=0.5, rate=linear, casca=0.0, cone=0.0, pagina=0.0), run_time=0.5)      # as famílias saem antes das células
        self.play(*grade.anim(rt=0.6, rate=linear, celulas=1.0), run_time=0.6)
        a, b = grade.pt("celPolo"), grade.pt("celEq")
        sqp, lp = legq(LI, "PERTO DO POLO", 120, 1020)                    # D9: legenda colorida no papel (G4), não solta no 3D
        sqe, le = legq(LI, "NO EQUADOR", 540, 1020)
        lpg, leg_ = VGroup(sqp, lp), VGroup(sqe, le)
        lpg._txt, leg_._txt = "PERTO DO POLO", "NO EQUADOR"
        self.pena(lp, extra=[Create(sqp)])
        self.pena(le, extra=[Create(sqe)], lag=0.2)
        self.gat("os dois têm o mesmo delta")
        l4 = mixl([("t", "MESMO", GEO), ("m", r"\DR,\;\DF,\;\DT")], 1080, 700, 40)
        self.pena(l4)
        self.dentro((1020, 300, 1860, 800), l4)
        self.gat("qual é o volume")
        q1 = T("?", a[0] - 40, a[1] - 18, 64, "left", LI)
        q2 = T("?", b[0] - 150, b[1] + 20, 64, "left", LI)
        self.titulo("QUAL É O VOLUME DE CADA PEDAÇO?")
        self.pena(q1, q2, lag=0.2)
        self.marca("02_H2")
        self.sai_fim()
