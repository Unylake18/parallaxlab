"""Lote PD2 · D2 DESENHAR SEM MIL SETAS · v3 (alvos 07 v1 e v3_d2b). "sem calcular mil setas": a grade de pontinhos onde iriam as setas (cor de
contexto). "procurar onde o campo não muda": as cinco retas x − y = c tracejadas. f⃗ = (1, x − y) → x − y = c ⇒ f⃗ = (1, c) por glyph map; leitura
do ⇒ (sublinhado). Reta por reta: a seta-semente (1, c) e o rótulo em placa EM CIMA da própria reta, em alturas diferentes e longe da borda.
"é só copiar": as setas enchem reta por reta. "o campo inteiro": os pontinhos viram a rede na cor de contexto."""
from alg30 import *  # noqa: F401,F403

CS = [0, 1, 2, -1, -2]
LABX = {-2: -2.5, -1: -.5, 0: 1.5, 1: -1.5, 2: .5}            # abscissa do rótulo de cada reta (alvo v3_d2b)


def reta_c(c):
    """Reta y = x − c (tracejada, recortada), as setas (1, c) nas abscissas inteiras (longe do rótulo) e o rótulo na reta."""
    ln = linha_rec(VA, [(-4.5, -4.5 - c), (4.5, 4.5 - c)], LA, GEO, 2, .65, dash=(10, 9))
    X0 = LABX[c]
    lab = L([("p1", r"(1,\,"), ("c", "%d" % c), ("pf", ")")], *canto_xy(VA, X0, X0 - c), 30, "c")
    lab = VGroup(placa7(lab), lab)
    lab.f = lab[1]
    lab._xy = (X0, X0 - c)
    ss = []
    for X in range(-4, 5):
        Y = X - c
        if abs(Y) > 2.8 or math.hypot(X - X0, Y - (X0 - c)) < .75:
            continue
        s = seta_campo(VA, X, Y, (1, c), .75, 4)
        if s is not None:
            ss.append(s.set_z_index(6))
    return ln, ss, lab


class LoteD2(Base):
    ANTES = "MESMA FÓRMULA, DOIS FILMES"

    def corpo(self):
        # ── D2-1 · enunciado: palco com a grade de pontinhos onde iriam as setas ──
        self.an("D2-1")
        self.secao("DESENHAR SEM MIL SETAS")
        zera_chapas()
        chA = chapa_px(*LA, nome="D2 palco A", v=VA)
        R = {c: reta_c(c) for c in CS}
        lab_xy = [R[c][2]._xy for c in CS]
        pts = {}
        for i in range(15):
            for j in range(11):
                X, Y = -3.5 + .5 * i, -2.5 + .5 * j
                d = Dot(VA.c2p(X, Y), radius=3 / 120, color=CTX).set_z_index(2)
                d._sem_contorno = True
                d._xy = (X, Y)
                pts[(X, Y)] = d
        pontos = VGroup(*pts.values())
        fF = L([("ff", r"\ff=(1,\ "), ("xy", r"\X-\Y"), ("pf", ")")], 1120, 330, 50)
        troca(self, "D1 → D2 (palco)")
        self.play(FadeIn(chA), run_time=0.6)
        self.gat("sem calcular mil setas")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in sorted(pontos, key=lambda d: (d._xy[0], -d._xy[1]))], lag_ratio=0.004), run_time=1.0)
        self.gat("o campo é este")
        escreve(self, fF, 0.4)
        self.gat("pausa o vídeo e tenta")
        self.pausa()
        self.ate(1.0)

        # ── D2-2 · o truque: as retas; x − y = c ⇒ f = (1, c); leitura do ⇒ ──
        self.an("D2-2")
        self.gat("o truque é procurar onde o campo não muda")
        self.play(*[Create(R[c][0]) for c in CS], run_time=0.9)
        f2 = L([("xy", r"\X-\Y"), ("ec", r"=c\ \Rightarrow\ "), ("ff2", r"\ff="), ("p1", r"(1,\,"), ("xy", "c"), ("pf", ")")], 1120, 440, 42)
        self.gat("a vertical só depende da diferença")
        gm(self, fF, f2, rt=1.0, copia=True)
        f2.ks = ["xy", "ec", "ff2", "p1", "c", "pf"]
        nr = legenda("NA RETA, A SETA NÃO MUDA", 1124, 530, GEO)
        self.gat("a seta é a mesma em todo ponto")
        self.play(FadeIn(nr, shift=0.05 * UP), run_time=0.4)
        self.gat("a seta dupla da tela")                          # leitura 3 (Anexo B): ⇒
        le(self, f2.p("ec")[2], 3, "a seta dupla da tela lê-se implica", ate="e essas retas são as paralelas")
        self.ate(1.0)

        # ── D2-3 · reta por reta: a semente e o rótulo em cima da reta ──
        self.an("D2-3")
        sem = {}
        for cs, fr in (((0,), "na própria diagonal"), ((1,), "uma reta abaixo"), ((2,), "mais uma abaixo"), ((-1, -2), "e acima da diagonal")):
            self.gat(fr)
            for c in cs:
                ln, ss, lab = R[c]
                k0 = min(range(len(ss)), key=lambda i: abs(ss[i]._xy[0] - (c / 2 + (1 if abs(ss[i]._xy[0] - LABX[c]) < 1 else 0))))
                sem[c] = ss[k0]
                sob = [d for d in pontos if math.hypot(d._xy[0] - lab._xy[0], d._xy[1] - lab._xy[1]) < .75
                       or math.hypot(d._xy[0] - sem[c]._xy[0], d._xy[1] - sem[c]._xy[1]) < .2]
                self.play(GrowArrow(sem[c]), *[FadeOut(d) for d in sob], run_time=0.5)
                self.remove(*sob)
                gm(self, f2, lab.f, rt=0.7, copia=True, extra=[FadeIn(lab[0])])
                print(f"[D2] reta c = {c}: semente em {sem[c]._xy}, rótulo em {lab._xy}")
        self.ate(1.0)

        # ── D2-4 · é só copiar: as setas enchem reta por reta; depois o campo inteiro ──
        self.an("D2-4")
        self.gat("agora é só copiar")
        for c in CS:
            ln, ss, lab = R[c]
            outras = [s for s in ss if s is not sem[c]]
            sob = [d for d in pontos if d in self.mobjects and any(math.hypot(d._xy[0] - s._xy[0], d._xy[1] - s._xy[1]) < .2 for s in outras)]
            self.play(*[TransformFromCopy(sem[c], s) for s in outras], *[FadeOut(d) for d in sob], run_time=0.5)
            self.remove(*sob)
            print(f"[D2] reta c = {c}: {len(ss)} setas (1, {c})")
        skip = ou(lambda X, Y: any(abs(Y - (X - c)) < .3 for c in CS), lambda X, Y: any(math.hypot(X - a, Y - b) < .75 for a, b in lab_xy))
        rede = campo30(VA, F2, passo=.5, rmin=0, mmax=4, ctx=True, skip=skip, nome="D2 rede (contexto)")
        for s in rede:
            s.set_z_index(2)
        resto = [d for d in pontos if d in self.mobjects]
        self.gat("e o campo inteiro está desenhado")
        self.play(*[FadeOut(d) for d in resto], cresce_campo(rede, 1.0), run_time=1.0)
        self.remove(*resto)
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
