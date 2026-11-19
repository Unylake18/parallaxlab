"""Lote PS · v3. S RESUMO (alvo v3_s): a escada da abertura volta inteira e cada frase troca o rótulo de um degrau, do tema para a lição
(FadeTransform do texto, com o contorno acendendo); depois as quatro da Parte 2. NO PRÓXIMO VÍDEO (alvo v3_gan), montado frase a frase: o título;
a chapa nasce com a cor partindo do canto (0, 0); ρ = x² + y² e os quatro cantos (0, 4, 4, 8); o 2 do centro voa para "centro: 2 · 4 m² = 8 kg" e o
8 para a régua; os quatro cantos voam para a linha dos cantos e o 16 para a régua; O DOBRO!; QUAL ESTÁ CERTA?; a grade 8 × 8 (traço). Depois o CTA
padrão. Sem número de episódio, sem Atlas, sem a resposta."""
from escada30 import *  # noqa: F401,F403

FRASES = ["a mesma fórmula conta dois filmes", "um campo se desenha pelas curvas", "o sentido da volta não é o sentido do giro",
          "um gradiente nunca gira", "ter derivadas parciais não basta", "e com a tabela você prevê"]
FRASES2 = ["um rio que gira nas margens", "uma parede onde a água deforma", "mapas conformes", "e leis de distância"]      # final: frases da v3.3
X0, Y0, S, N = 240, 380, 460, 46


def cel_chapa():
    cs = []
    for i in range(N):
        for j in range(N):
            xx, yy = (i + .5) / N * 2, (j + .5) / N * 2
            c = mix("#0E3A40", "#8CFFD2", (xx * xx + yy * yy) / 8)
            q = Rectangle(width=(S / N + .6) / 120, height=(S / N + .6) / 120).move_to(PX(X0 + (i + .5) * S / N, Y0 + S - (j + .5) * S / N))
            q.set_fill(c, 1).set_stroke(width=0)
            q._sem_contorno = True
            q._d = xx + yy
            cs.append(q)
    return cs


def P_(a, b):
    """Plano da chapa (metros, origem no canto de baixo à esquerda) → px."""
    return X0 + a / 2 * S, Y0 + S - b / 2 * S


class LoteS(Base):
    ANTES = "APLICAÇÃO · POR QUE UM SOBRE A DISTÂNCIA AO QUADRADO"

    def corpo(self):
        # ── S-1 · a escada inteira; cada frase troca o rótulo de um degrau (alvo v3_s) ──
        self.an("S-1")
        self.secao("RESUMO")
        D = [Degrau(i, 1, "ab") for i in range(6)]
        Ap = [Degrau(i, 2, "ab", .45) for i in range(4)]
        e1, e2 = titulos_escada()
        troca(self, "A3 → S (a escada volta)")
        self.play(*[FadeIn(d) for d in D], *[FadeIn(a) for a in Ap], FadeIn(e1), FadeIn(e2), run_time=0.7)

        def troca_rotulo(d, novo_txt):
            novo = T(novo_txt, d.rot.get_left()[0] * 120 + 960, 0, 26, cor=BR, up=False)
            novo.shift(UP * (d.rot.get_center()[1] - novo.get_center()[1]))
            self.play(FadeTransform(d.rot, novo), d.caixa.animate.set_stroke(BR), run_time=0.5)
            self.play(d.caixa.animate.set_stroke(d.cor), run_time=0.5)
            d.remove(d.rot)
            d.rot = novo
            d.add(novo)
        for i, fr in enumerate(FRASES):
            self.gat(fr)
            troca_rotulo(D[i], ESC[i][2])
        self.gat("e nas aplicações")
        self.play(*[UpdateFromAlphaFunc(a, lambda m, x: m.opacidade(.45 + .55 * x)) for a in Ap], run_time=0.5)
        for i, fr in enumerate(FRASES2):
            self.gat(fr)
            troca_rotulo(Ap[i], APL[i][2])
        self.ate(1.0)

        # ── S-2 · no próximo vídeo, frase a frase (alvo v3_gan) ──
        self.an("S-2")
        g1 = T("NO PRÓXIMO VÍDEO", 960, 170, 32, "center", GEO, bold=False)
        g2 = T("SOMA DE RIEMANN E INTEGRAL DUPLA", 960, 250, 58, "center")
        sai = self.snap() + [m for m in (self.h1, self.h2, self.wm) if m is not None]
        self.gat("no próximo vídeo")
        troca(self, "S → cartão do próximo vídeo (sem canto e sem logo)")
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        self.h2 = None
        self.play(FadeIn(g1, shift=0.05 * UP), caneta(g2, ritmo=0.08), run_time=0.9)
        cs = cel_chapa()
        bd = Rectangle(width=S / 120, height=S / 120).move_to(PX(X0 + S / 2, Y0 + S / 2)).set_fill(opacity=0).set_stroke(GEO, 3 / 1.2, 1)
        bd._sem_contorno = True
        l1 = T("2 m", X0 + S / 2, Y0 + S + 44, 28, "center", GEO, bold=False, up=False)
        l2 = T("2 m", X0 - 20, Y0 + S / 2, 28, "right", GEO, bold=False, up=False)
        self.gat("agora é hora de somar pedacinhos")              # a cor parte do canto (0, 0) e se espalha
        self.play(Create(bd), FadeIn(l1), FadeIn(l2), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(q) for q in sorted(cs, key=lambda q: q._d)], lag_ratio=0.0006), run_time=1.6)
        rho = L([("r", r"\rho="), ("f", r"\X^2+\Y^2"), ("u", r"\ \ \text{kg/m}^2")], 870, 420, 38)
        cantos = [(0, 0, "0"), (2, 0, "4"), (0, 2, "4"), (2, 2, "8")]
        pts, labs = [], []
        for a, b, v in cantos:
            pts.append(ponto7(PX(*P_(a, b)), E2, 9, 12))
            labs.append(TXP30(v, *P_(a + (-.14 if a else .14), b + (-.17 if b else .1)), 30, "center", E2, bold=True))
        self.gat("leve num canto e cada vez mais densa")
        escreve(self, rho, 0.25)
        self.play(*[FadeIn(p, scale=0.6) for p in pts], *[FadeIn(l) for l in labs], run_time=0.5)
        pc = ponto7(PX(*P_(1, 1)), E1, 10, 12)
        lc = TXP30("2", *P_(1, 1.14), 30, "center", E1, bold=True)
        Lc = L([("c", r"\text{centro:}\ \ "), ("v", r"\Am{2}"), ("x", r"\cdot 4\ \text{m}^2="), ("r", r"\Am{8\ \text{kg}}")], 870, 530, 38)
        rx, ry, rw = 900, 900, 760
        regua = VGroup(linha7([PX(rx, ry), PX(rx + rw, ry)], GEO, 3))
        for k in range(0, 21, 4):
            X = rx + k / 20 * rw
            regua.add(linha7([PX(X, ry - 10), PX(X, ry + 10)], GEO, 3), T(str(k), X, ry + 42, 24, "center", GEO, bold=False))
        regua.add(T("MASSA (kg)", rx + rw / 2, ry + 84, 26, "center", GEO, bold=False, up=False))

        def palpite(k, cor):
            X = rx + k / 20 * rw
            tri = Polygon(PX(X, ry - 14), PX(X - 12, ry - 38), PX(X + 12, ry - 38)).set_fill(cor, 1).set_stroke(width=0)
            tri._sem_contorno = True
            return VGroup(tri, T(f"{k} kg?", X, ry - 52, 32, "center", cor, up=False))
        self.gat("pelo valor do centro")
        self.play(FadeIn(pc, scale=0.6), FadeIn(lc), FadeIn(regua), run_time=0.5)
        escreve_p(self, Lc, ["c"], 0.15)
        voa(self, lc.f, Lc.p("v"), rt=0.5)
        escreve_p(self, Lc, ["x", "r"], 0.15)
        junta(self, Lc, "b")
        p8 = palpite(8, E1)
        self.play(TransformFromCopy(Lc.p("r"), p8[1]), FadeIn(p8[0]), run_time=0.6)
        Lk = L([("c", r"\text{cantos:}\ \ "), ("fa", r"\dfrac{", 0), ("n", r"\Mg{0+4+4+8}"), ("fb", "}{", 1), ("d", "4"), ("fc", "}", 0),
                ("x", r"\cdot 4\ \text{m}^2="), ("r", r"\Mg{16\ \text{kg}}")], 870, 640, 38)
        nn = Lk.p("n")
        self.gat("pela média dos quatro cantos")
        escreve_p(self, Lk, ["c"], 0.15)
        Lk._origem = "b"
        print(f"[origem] b {self.lote} S-2 {self.t:.2f} {Lk._tex!r} ← os quatro cantos")
        self.play(*[TransformFromCopy(l.f, nn[k]) for l, k in zip(labs, (0, 2, 4, 6))], caneta(VGroup(nn[1], nn[3], nn[5]), ritmo=0.2), run_time=0.7)
        escreve_p(self, Lk, ["fb", "d", "x", "r"], 0.15)
        junta(self, Lk, "b")
        p16 = palpite(16, E2)
        self.play(TransformFromCopy(Lk.p("r"), p16[1]), FadeIn(p16[0]), run_time=0.6)
        dob = T("O DOBRO!", 1640, 600, 44, "center", BR)
        self.gat("o dobro")
        self.play(FadeIn(dob, scale=0.9), run_time=0.4)
        qc = T("QUAL ESTÁ CERTA?", 1280, 755, 36, "center", CAMPO2, bold=False)
        self.gat("qual das duas está certa")
        self.play(caneta(qc, ritmo=0.12), run_time=0.6)
        g8 = VGroup(*[linha7([PX(X0 + k * S / 8, Y0), PX(X0 + k * S / 8, Y0 + S)], BR, 1.5, .7) for k in range(1, 8)],
                    *[linha7([PX(X0, Y0 + k * S / 8), PX(X0 + S, Y0 + k * S / 8)], BR, 1.5, .7) for k in range(1, 8)]).set_z_index(30)
        self.gat("a resposta exata vem de somar")
        self.play(Create(g8), run_time=1.2)
        self.ate(1.0)

        # ── S-3 · CTA padrão ──
        self.an("S-3")
        self.gat("se essa aula te ajudou")
        troca(self, "cartão → CTA")
        sai = self.snap()
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)        # v3: o cartão sai antes de o CTA entrar
        self.remove(*sai)
        logo_cta(self, rt_fim=0.0)                                 # final §7.3: o vídeo termina no fim da última âncora (WAV + 1,0 s)
