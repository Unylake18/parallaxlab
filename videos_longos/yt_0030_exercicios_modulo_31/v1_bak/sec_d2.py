"""Lote PD2 · D2 DESENHAR SEM MIL SETAS (alvos 07, 08). Palco A vazio com a grade; f⃗ = (1, x − y) e x − y = c ⇒ f⃗ = (1, c) em caneta. Em cada reta
x − y = c (tracejada, recortada na moldura): UMA seta (1, c) nasce num ponto e as cópias deslizam ao longo da reta (0,8 s), com o rótulo (1, c) em placa;
c = 0, 1, 2 (alvo 07) e depois c = −1, −2. "O campo inteiro está desenhado": a rede completa entra na cor de contexto atrás das retas (alvo 08)."""
from lib30 import *  # noqa: F401,F403

LAB = {-2: 2.45, -1: 2.45, 0: 2.45, 1: 2.0, 2: 1.2}


def clar_mob(v, m, marg=0.0):
    """Clareira (R1) em volta da caixa de um rótulo do palco (coordenadas do plano; clar28 soma 0,25 u)."""
    x0, y0 = v.p2c(m.get_corner(DL))
    x1, y1 = v.p2c(m.get_corner(UR))
    return clar28([(x0 - marg, y0 - marg, x1 + marg, y1 + marg)])


def reta_c(c):
    """Reta y = x − c (tracejada, recortada), as setas (1, c) nos pontos de abscissa inteira e o rótulo."""
    ln = linha_rec(VA, [(-4.5, -4.5 - c), (4.5, 4.5 - c)], LA, GEO, 2, .65, dash=(10, 9))
    Yl = LAB[c]
    lab = TP(r"(1,\,%d)" % c, *canto_xy(VA, Yl + c - .23, Yl + .23), 30)
    perto = clar_mob(VA, lab, -0.1)                      # R1: a seta da reta não encosta no rótulo
    ss = []
    for X in range(-4, 5):
        Y = X - c
        if abs(Y) > 2.8 or perto(X, Y):
            continue
        s = seta_campo(VA, X, Y, (1, c), .75, 4)
        if s is not None:
            ss.append(s.set_z_index(6))
    return ln, ss, lab


class LoteD2(Base):
    ANTES = "MESMA FÓRMULA, DOIS FILMES"

    def corpo(self):
        # ── D2-1 · enunciado ──
        self.an("D2-1")
        self.secao("DESENHAR SEM MIL SETAS")
        zera_chapas()
        chA = chapa_px(*LA, nome="D2 palco A", v=VA)
        fF = TC(r"\ff=(1,\ \X-\Y)", 1120, 330, 50)
        troca(self, "D1 → D2 (palco vazio)")
        self.play(FadeIn(chA), run_time=0.6)
        self.gat("o campo é este")
        self.play(caneta(fF, ritmo=0.4))
        self.gat("pausa o vídeo e tenta")
        self.pausa()
        self.ate(1.0)

        # ── D2-2 · o truque ──
        self.an("D2-2")
        f2 = TC(r"\X-\Y=c\ \Rightarrow\ \ff=(1,\,c)", 1120, 440, 42)
        self.gat("em cima de uma reta")
        self.play(caneta(f2, ritmo=0.35))
        nr = legenda("NA RETA, A SETA NÃO MUDA", 1124, 530, GEO)
        self.gat("a seta é a mesma em todo ponto")
        self.play(FadeIn(nr, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D2-3 · reta por reta (alvo 07) ──
        self.an("D2-3")
        retas = {}
        for cs, fr in (((0,), "na própria diagonal"), ((1,), "uma reta abaixo"), ((2,), "mais uma abaixo"), ((-1, -2), "e acima da diagonal")):
            self.gat(fr)
            for c in cs:
                ln, ss, lab = reta_c(c)
                retas[c] = (ln, ss, lab)
                k0 = min(range(len(ss)), key=lambda i: abs(ss[i]._xy[0] - c / 2))   # a semente: no meio do trecho visível da reta
                semente = ss[k0]
                self.play(Create(ln), GrowArrow(semente), run_time=0.6)
                outras = [s for s in ss if s is not semente]
                self.play(*[TransformFromCopy(semente, s) for s in outras], FadeIn(lab), run_time=0.8)
                print(f"[D2] reta c = {c}: {len(ss)} setas (1, {c})")
        self.ate(1.0)

        # ── D2-4 · o campo inteiro (alvo 08) ──
        self.an("D2-4")
        cs = sorted(retas)
        skip = ou(lambda X, Y: any(abs(Y - (X - c)) < .3 for c in cs), *[clar_mob(VA, retas[c][2]) for c in cs])
        rede = campo30(VA, F2, passo=.5, rmin=0, mmax=4, ctx=True, skip=skip, nome="D2 rede (contexto)")
        for s in rede:
            s.set_z_index(2)
        self.gat("e o campo inteiro está desenhado")
        self.play(cresce_campo(rede, 1.0))
        d1, d2 = legenda("DESCENDO DE RETA EM RETA,", 1124, 640, GEO), legenda("A SETA EMPINA", 1124, 685, GEO)
        self.gat("setas que vão empinando")
        self.play(FadeIn(d1, shift=0.05 * UP), run_time=0.4)
        self.play(FadeIn(d2, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D2-5 · é uma derivada ──
        self.an("D2-5")
        dv = legenda("ESSE EMPINAR É UMA DERIVADA", 1124, 760, AMB)
        self.gat("é uma derivada")
        self.play(FadeIn(dv, shift=0.05 * UP), run_time=0.4)
        self.sai_fim()
