"""Lote PB1 · UM PEDACINHO DE FLUIDO (handoff v2 quadro 03; v3 §3.1–3.2: B1-1 com o campo em contexto e a seta laranja da velocidade; DEFORMA ganha NO FIM DA AULA). B1-1: palco (layout A) com (−y, 2x); UM ponto laranja anda pela trajetória exata com a sua
seta (real × 0,4) e deixa o rastro tracejado; o selo na coluna (três linhas). B1-2: o palco aproxima em volta de P0 (×2, ×4, ×8; setas refeitas com o
mesmo espaçamento na tela, crossfade 0,4 s), diferença entre vizinhas em coral, ΔF/h → ∂F/∂x. B1-3: três cartões (layout C), o quadrado faz o
movimento UMA vez, com o original tracejado.
v4: B1-1a novo (§3.1, alvo 14): a seta em (0,5; 1,3) se decompõe em P e Q; coluna Ω ⊂ ℝ² aberto, F(x, y) = (P, Q), P = −y, Q = 2x; o campo (contexto) é
o mesmo do B1-1 e não pisca. N1: ponto, seta v e rótulo andam juntos (um só objeto animado; a seta parada saiu). N2: cada cartão entra inteiro (painel,
campo e pedacinho) na sua frase. §4: o pedacinho é a chapa com malha 4×4 levada pelo fluxo exato, com clareira na posição final."""
from v27 import *  # noqa: F401,F403

V = Vista(600, 540, 120)
P0 = (0.8, 0.6)          # final §2.2: lupa ×8 em (0,8; 0,6)
X0 = (1.6, 0.0)          # partida do ponto do B1-1


def campo_zoom(Z, ctx=False):
    """Setas na grade do palco (passo 0,5 na tela) mostrando F em P0 + (posição na tela)/Z: com Z grande, todas quase iguais."""
    g = Campo7()
    for i in range(-6, 7):
        for j in range(-6, 7):
            X, Y = 0.5 * i, 0.5 * j
            if math.hypot(X, Y) > 3.05 or math.hypot(X, Y) < 1e-9 and Z == 1:
                continue
            q = (X, Y) if Z == 1 else (P0[0] + X / Z, P0[1] + Y / Z)
            s = seta_campo(V, X, Y, F_Y2X(*q), 0.42, 6.0, ctx)
            if s is not None:
                s._q = q
                g.add(s)
    return g.set_z_index(3)


class LoteB1(Base):
    def corpo(self):
        # ── B1-1a · nomes das peças (v4 §3.1, alvo 14) ──
        self.an("B1-1a")
        self.secao("UM PEDACINHO DE FLUIDO")
        cmp = campo7(V, F_Y2X, mmax=6.0, ctx=True, nome="B1 (−y, 2x) em contexto (B1-1a e B1-1)")
        c0 = legenda("UM CAMPO NO PLANO", 1124, 230, SAIF)
        self.play(cresce_campo(cmp, 1.0), FadeIn(c0))
        p0 = (0.5, 1.3)
        fv = F_Y2X(*p0)
        q = (p0[0] + 0.7 * fv[0], p0[1] + 0.7 * fv[1])
        h = (q[0], p0[1])
        labP, labQ, labF, labX = ((p0[0] + h[0]) / 2, p0[1] - 0.3), (q[0] - 0.32, (p0[1] + q[1]) / 2), (q[0] + 0.34, q[1] + 0.12), (p0[0] + 0.5, p0[1] - 0.22)

        def ds(X, Y, a, b):
            ax, ay = b[0] - a[0], b[1] - a[1]
            u = max(0.0, min(1.0, ((X - a[0]) * ax + (Y - a[1]) * ay) / (ax * ax + ay * ay)))
            return math.hypot(X - a[0] - u * ax, Y - a[1] - u * ay)
        perto = lambda X, Y: (ds(X, Y, p0, q) < 0.34 or ds(X, Y, p0, h) < 0.3 or ds(X, Y, h, q) < 0.3
                              or any(math.hypot(X - l[0], Y - l[1]) < 0.3 for l in (labP, labQ, labF, labX)))
        clA = esconde(cmp, perto)
        sF = seta7(V.c2p(*p0), V.c2p(*q), CAMPO2, 8, 28).set_z_index(11)
        dP, dQ = seta7(V.c2p(*p0), V.c2p(*h), CAMPO, 6, 22).set_z_index(10), seta7(V.c2p(*h), V.c2p(*q), CAMPO, 6, 22).set_z_index(10)
        gd = VGroup(vlinha(V, [(p0[0], q[1]), q], GEO, 2, alpha=0.7, dash=(7, 7)), vlinha(V, [p0, (p0[0], q[1])], GEO, 2, alpha=0.7, dash=(7, 7)))
        pp = ponto7(V.c2p(*p0), BR, 8, 12)
        rP, rQ = TP(r"\Pp", *canto_xy(V, *labP), 44), TP(r"\Qq", *canto_xy(V, *labQ), 44)
        rF, rX = TP(r"\F", *canto_xy(V, *labF), 44), TP(r"(\X,\Y)", *canto_xy(V, *labX), 36)
        c1 = TC(r"\Omega \subset \mathbb{R}^2 \ \text{aberto}, \qquad \F : \Omega \to \mathbb{R}^2", 1120, 315, 44)
        c2 = TC(r"\F(\X,\Y) = \big(\Pp(\X,\Y),\ \Qq(\X,\Y)\big)", 1120, 420, 50)
        lP, lQ = legenda("P: COMPONENTE HORIZONTAL", 1124, 520, CAMPO), legenda("Q: COMPONENTE VERTICAL", 1124, 570, CAMPO)
        lG = legenda("P E Q COM DERIVADAS PARCIAIS CONTÍNUAS EM Ω", 1124, 630, GEO)
        c3, c4 = TC(r"\F = (-\Y,\ 2\X)", 1120, 740, 50), TC(r"\Pp = -\Y, \qquad \Qq = 2\X", 1120, 830, 46)
        print(f"[pecas] B1-1a: F(0,5; 1,3) = ({fv[0]:.2f}, {fv[1]:.2f}): P < 0 (horizontal para a esquerda), Q > 0")
        self.gat("nome às peças")
        self.play(some(clA), GrowArrow(sF), FadeIn(pp, scale=0.5), FadeIn(rF), FadeIn(rX), run_time=0.7)
        self.gat("região aberta")
        self.play(caneta(c1))
        self.gat("duas partes")
        self.play(FadeIn(gd), GrowArrow(dP), run_time=0.45)
        self.play(GrowArrow(dQ), run_time=0.45)
        self.gat("a parte horizontal")
        self.play(FadeIn(rP), FadeIn(lP), run_time=0.5)
        self.gat("e a vertical de q")
        self.play(FadeIn(rQ), FadeIn(lQ), run_time=0.5)
        self.gat("e as duas mudam de ponto para ponto")                  # final: a voz real é mais rápida; F(x, y) = (P(x, y), Q(x, y)) começa na frase anterior
        self.play(caneta(c2))
        self.gat("neste campo")
        self.play(caneta(c3))
        self.play(caneta(c4))
        self.play(FadeIn(lG), run_time=0.5)
        self.ate(0.97)

        # ── B1-1 (a coluna troca; o campo fica) ──
        self.an("B1-1")
        sai_a = [c0, c1, c2, c3, c4, lP, lQ, lG, sF, dP, dQ, gd, pp, rP, rQ, rF, rX]
        self.play(*[FadeOut(m_) for m_ in sai_a], run_time=0.4)
        self.remove(*sai_a)
        self.play(volta(clA), run_time=0.4)                                    # R6: as setas só voltam depois que os rótulos saíram
        # (v3 §3.1) o ponto e a sua seta de velocidade em LARANJA (haste 8 px, ponta 28 px, comprimento 0,3·|F|), pela trajetória exata; órbita tracejada
        T_VOLTA = 2 * PI / math.sqrt(2)
        ts_ = np.linspace(0, T_VOLTA, 240)
        X, Y = fl_y2x(np.full_like(ts_, X0[0]), np.full_like(ts_, X0[1]), ts_)
        orb = vlinha(V, list(zip(X, Y)), GEO, 2.5, alpha=0.75, dash=(8, 8))
        pt = ponto7(V.c2p(*X0), POS, 11, 11)
        sv = seta7(V.c2p(*X0), V.c2p(X0[0] + 0.1, X0[1] + 0.1), POS, 8, 28).set_z_index(11)   # N1: UM objeto só; muda por become()
        lv = TP(r"\Pt{\vec v}", 0, 0, 46)
        estado = {"p": X0, "q": X0}

        def poe(t):
            x, y = fl_y2x(np.array([X0[0]]), np.array([X0[1]]), t)
            x, y = float(x[0]), float(y[0])
            f = F_Y2X(x, y)
            q = (x + 0.3 * f[0], y + 0.3 * f[1])
            pt.move_to(V.c2p(x, y))
            sv.become(seta7(V.c2p(x, y), V.c2p(*q), POS, 8, 28).set_z_index(11))
            lab = (q[0] + 0.32, q[1] - 0.02)
            lv.move_to(V.c2p(*lab))
            estado.update(p=(x, y), q=q, lab=lab)

        def centros():
            p, q = estado["p"], estado["q"]
            l_ = estado["lab"]
            return ([(p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u) for u in np.linspace(0, 1, 6)]
                    + [l_, (l_[0] - 0.2, l_[1]), (l_[0] + 0.2, l_[1]), (l_[0], l_[1] + 0.2), (l_[0], l_[1] - 0.2)])   # R6: a caixa inteira do rótulo v
        poe(0.0)
        self.gat("a gente vai ler o campo como a velocidade")
        self.play(Create(orb), run_time=0.8)
        clareira_viva(cmp, centros, 0.34)
        self.add(cmp)                                  # o grupo entra na cena (as setas já estão nela): sem isso o updater da clareira não roda
        self.play(FadeIn(pt, scale=0.5), FadeIn(sv), FadeIn(lv), run_time=0.5)
        cv_ = T("CAMPO = VELOCIDADE", 1120, 430, 40, "left", SAIF)
        fF = TC(r"\F = (-\Y,\ 2\X)", 1120, 540, 50)
        rt = max(4.0, self.resta() - 0.6 - caneta(fF.copy()).tot)              # final: a volta + a caneta cabem na fala
        print(f"[motor] B1-1: uma volta da elipse (t = {T_VOLTA:.3f}) em {rt:.2f} s (fator {T_VOLTA / rt:.3f})")
        self.play(UpdateFromAlphaFunc(VGroup(pt, sv, lv), lambda m, a: poe(T_VOLTA * a)), FadeIn(cv_, shift=0.1 * UP), run_time=rt, rate_func=linear)
        x_, y_ = fl_y2x(np.array([X0[0]]), np.array([X0[1]]), T_VOLTA)
        print(f"[fluxo] B1-1: o ponto volta a ({float(x_[0]):.4f}, {float(y_[0]):.4f}) depois de uma volta (partiu de {X0})")
        self.play(caneta(fF))
        self.ate(0.97)

        # ── B1-2 · o palco aproxima em volta de P0 (o campo volta à cor normal) ──
        self.an("B1-2")
        cmp.clear_updaters()
        self.play(FadeOut(VGroup(pt, sv, lv, orb, cv_, fF)), UpdateFromAlphaFunc(cmp, lambda m, a: (m.contexto(a < 0.5), [op_seta(s, 1) for s in m] if a > 0.5 else None)), run_time=0.5)
        for s in cmp:
            s._escondida = False
        self.remove(pt, sv, lv, orb, cv_, fF)
        p0 = ponto7(V.c2p(*P0), POS, 10, 10)
        self.gat("pega uma lupa")
        self.play(FadeIn(p0, scale=0.5), run_time=0.5)
        cur = cmp
        zt = None
        for Z, frase in ((2, "chega bem pertinho"), (4, "as setas ficam quase todas iguais")):
            self.gat(frase)
            nz = campo_zoom(Z)
            z2 = legenda(f"×{Z}", 260, 225, GEO, size=34)
            anims = [FadeOut(cur), FadeIn(nz)]
            if zt:
                anims.append(FadeOut(zt, rate_func=lambda a: smooth(min(1.0, 2 * a))))
            self.play(*anims, FadeIn(z2, rate_func=lambda a: smooth(max(0.0, 2 * a - 1))), run_time=0.4)   # R6: o ×N velho sai antes do novo
            self.remove(cur)
            if zt:
                self.remove(zt)
            cur, zt = nz, z2

        # final §2.2 (alvo 18, sb27 `b12v5`): o ×8 dentro da lupa (anel GEO); seta e vizinha; AS DUAS NO MESMO PÉ; ΔF coral; ΔF/h → ∂F/∂x
        L8 = Vista(560, 560, 110)
        ZL, SC, RL = 8, 0.62, 2.75
        FF = lambda X, Y: F_Y2X(P0[0] + X / ZL, P0[1] + Y / ZL)
        A, B = (-0.9, -0.3), (0.9, -0.3)
        hl = lambda X, Y: (math.hypot(X - A[0], Y - A[1]) < 0.45 or math.hypot(X - B[0], Y - B[1]) < 0.45 or (abs(Y + 1.05) < 0.32 and abs(X) < 1.2)
                           or math.hypot(X - A[0] + 0.42, Y - A[1] + 0.32) < 0.4 or math.hypot(X - B[0] - 0.45, Y - B[1] + 0.32) < 0.4 or math.hypot(X, Y + 1.35) < 0.45)
        lupa = Campo7()
        for i in range(11):
            for j in range(11):
                X, Y = -3 + 0.6 * i, -3 + 0.6 * j
                if math.hypot(X, Y) > RL - 0.35:
                    continue
                f_ = FF(X, Y)
                s = seta7(L8.c2p(X - f_[0] * SC / 2, Y - f_[1] * SC / 2), L8.c2p(X + f_[0] * SC / 2, Y + f_[1] * SC / 2), CAMPO, 5, 18)
                s._xy, s._t, s._f, s._L = (X, Y), 0.0, f_, math.hypot(*f_) * SC
                lupa.add(s)
        lupa.set_z_index(3)
        anel = vcirc(L8, RL + 0.12, GEO, 4, alpha=0.8)
        z8 = legenda("×8", *canto_xy(L8, -2.35, 2.45), GEO, size=34)
        self.gat("quase se fossem")
        self.play(FadeOut(cur), FadeOut(p0), FadeIn(lupa), Create(anel), FadeOut(zt, rate_func=lambda a: smooth(min(1.0, 2 * a))),
                  FadeIn(z8, rate_func=lambda a: smooth(max(0.0, 2 * a - 1))), run_time=0.6)
        self.remove(cur, zt, p0)
        fa, fb = FF(*A), FF(*B)
        sA = seta7(L8.c2p(*A), L8.c2p(A[0] + fa[0] * SC, A[1] + fa[1] * SC), CAMPO2, 7, 24).set_z_index(11)
        sB = seta7(L8.c2p(*B), L8.c2p(B[0] + fb[0] * SC, B[1] + fb[1] * SC), CAMPO2, 7, 24).set_z_index(11)
        sA._xy, sB._xy = A, B
        pA, pB = ponto7(L8.c2p(*A), BR, 7, 12), ponto7(L8.c2p(*B), BR, 7, 12)
        rF1, rF2 = TP(r"\F_1", *canto_xy(L8, A[0] - 0.42, A[1] - 0.32), 38), TP(r"\F_2", *canto_xy(L8, B[0] + 0.45, B[1] - 0.32), 38)
        cota = VGroup(vlinha(L8, [(A[0], -1.05), (B[0], -1.05)], AMB, 3), vlinha(L8, [(A[0], -0.95), (A[0], -1.15)], AMB, 3),
                      vlinha(L8, [(B[0], -0.95), (B[0], -1.15)], AMB, 3)).set_z_index(10)
        rh = TP(r"\h", *canto_xy(L8, 0, -1.35), 40)
        tira = [s for s in lupa if hl(*s._xy)]
        self.gat("pega uma seta e a vizinha")
        self.play(*[FadeOut(s) for s in tira], UpdateFromAlphaFunc(lupa, lambda m, a: m.contexto(a > 0.5)), GrowArrow(sA), GrowArrow(sB),
                  FadeIn(pA, scale=0.5), FadeIn(pB, scale=0.5), run_time=0.6)
        lupa.remove(*tira)
        self.remove(*tira)
        self.play(FadeIn(rF1), FadeIn(rF2), run_time=0.4)
        self.gat("que a gente chama de agá")
        self.play(Create(cota), FadeIn(rh), run_time=0.5)
        # painel: as duas no mesmo pé (escala 1,6)
        pn = painel(1010, 200, 840, 400)
        lpn = legenda("AS DUAS NO MESMO PÉ", 1040, 245, SAIF)
        V2 = Vista(1600, 585, 110)
        K2 = 1.6
        ta, tb = (fa[0] * K2, fa[1] * K2), (fb[0] * K2, fb[1] * K2)
        s2A, s2B = seta7(V2.c2p(0, 0), V2.c2p(*ta), CAMPO2, 7, 24).set_z_index(11), seta7(V2.c2p(0, 0), V2.c2p(*tb), CAMPO2, 7, 24).set_z_index(11)
        p2 = ponto7(V2.c2p(0, 0), BR, 7, 12)
        r2A, r2B = TP(r"\F_1", *canto_xy(V2, ta[0] - 0.45, ta[1] - 0.05), 38), TP(r"\F_2", *canto_xy(V2, tb[0] - 0.45, tb[1] + 0.05), 38)
        dF = seta7(V2.c2p(*ta), V2.c2p(*tb), CORAL, 7, 22).set_z_index(12)
        rdF = TP(r"\C{\Delta\vec F}", *canto_xy(V2, ta[0] + 0.7, (ta[1] + tb[1]) / 2), 40)
        print(f"[lupa] B1-2: F1 = ({fa[0]:.3f}, {fa[1]:.3f}), F2 = ({fb[0]:.3f}, {fb[1]:.3f}), ΔF = ({fb[0] - fa[0]:.3f}, {fb[1] - fa[1]:.3f}) (vertical: só o Q muda com x)")
        self.gat("a diferença entre as duas")
        self.play(FadeIn(pn), FadeIn(lpn), run_time=0.4)
        self.play(TransformFromCopy(sA, s2A), TransformFromCopy(sB, s2B), FadeIn(p2), run_time=0.8)
        self.play(FadeIn(r2A), FadeIn(r2B), run_time=0.3)
        self.gat("essa setinha coral")
        self.play(GrowArrow(dF), FadeIn(rdF), run_time=0.6)
        f = TC(r"\dfrac{\C{\Delta\vec F}}{\h} \quad\xrightarrow{\ \h\,\to\,0\ }\quad \dfrac{\partial \F}{\dx}", 1430, 720, 54, "c")
        lDP = legenda("DERIVADA PARCIAL", 1430, 820, SAIF, "center")
        f2 = TC(r"\dfrac{\partial \F}{\dx} = \Big(\dfrac{\partial \Pp}{\dx},\ \dfrac{\partial \Qq}{\dx}\Big)", 1430, 920, 44, "c")
        self.gat("essa diferença dividida")                                    # final: a caneta começa em "essa diferença" (voz real mais rápida)
        self.play(self.caneta_ate(f, "tem nome derivada parcial"))
        self.gat("tem nome derivada parcial")
        self.play(FadeIn(lDP, shift=0.1 * UP, run_time=0.4), caneta(f2))
        self.ate(0.97)
        lupa_tudo = [lupa, anel, z8, sA, sB, pA, pB, rF1, rF2, cota, rh, pn, lpn, s2A, s2B, p2, r2A, r2B, dF, rdF, f, lDP, f2]

        # ── B1-3 · três cartões ──
        self.an("B1-3")
        # §4.1 + final (R6): a lupa sai na 1ª parte do play do 1º cartão; o cartão entra depois (sai_entra)
        C = [(140, "GIRA", "ROTACIONAL", VIO, F_GIRO, fl_giro, 0.6), (720, "MUDA DE ÁREA", "DIVERGENTE", SAI, F_EXPL, fl_expl, math.log(1.45)),
             (1300, "DEFORMA", "NO FIM DA AULA", GEO, F_SELA, fl_sela, math.log(1.5))]
        cards = []
        for x0, rot_, tag, ct, Fv, fl, tf in C:
            v = Vista(x0 + 240, 480, 56)
            pn = painel(x0, 250, 480, 460)
            cm = campo7(v, Fv, -3.5, 3.5, -3.5, 3.5, 0.85, rmin=1.1, rmax=3.9, mmax=3.4, nome=f"B1-3 {rot_}")
            fant = contorno_ini(v, [(-0.6, -0.6), (0.6, -0.6), (0.6, 0.6), (-0.6, 0.6)])
            qd = Pedaco(v, uv_quad((0, 0), 1.2), fl)
            t1 = T(rot_, x0 + 240, 780, 34, "center")
            t2 = T(tag, x0 + 240, 835, 30, "center", ct, bold=False) if tag else None
            cards.append(dict(v=v, pn=pn, cm=cm, fant=fant, qd=qd, t1=t1, t2=t2, tf=tf, gr=papel(v, area_px(v, x0, 250, 480, 460))))
        fr3 = ("pode girar", "pode crescer ou encolher", "e pode se deformar")
        for i_, (c, frase) in enumerate(zip(cards, fr3)):
            self.gat(frase)                                                  # N2: painel, campo e pedacinho entram juntos
            ent = [FadeIn(c["pn"]), FadeIn(c["gr"]), cresce_campo(c["cm"], 0.4), FadeIn(c["qd"]), FadeIn(c["fant"]), FadeIn(c["t1"], shift=0.1 * UP)]
            if i_ == 0:
                self.grade()                                                  # final: a grade padrão sai; cada cartão traz a sua
            self._grades.append(c["gr"])
            if i_ == 0:
                self.play(*self.sai_entra(lupa_tudo, ent, f=0.4), run_time=0.6)
                self.remove(*lupa_tudo)
            else:
                self.play(*ent, run_time=0.4)
            a0 = area_poly(c["qd"].XY)
            rt_ = 1.6 if i_ == 2 else max(0.25, min(1.6, self.falta(fr3[i_ + 1]) - 0.05))   # final: o movimento cabe antes da próxima frase
            self.play(*corre(self, [c["qd"]], c["tf"], rt_, rate=smooth))
            print(f"[malha] B1-3 {c['t1'].text if hasattr(c['t1'], 'text') else ''}: área {a0:.4f} → {area_poly(c['qd'].XY):.4f}")
        for c, frase in zip(cards, ("o giro é medido pelo rotacional", "pelo divergente", "a terceira a deformação")):
            self.gat(frase)
            self.play(FadeIn(c["t2"], shift=0.1 * UP), run_time=0.5)
        self.ate(0.97)
        self.sai_fim()
