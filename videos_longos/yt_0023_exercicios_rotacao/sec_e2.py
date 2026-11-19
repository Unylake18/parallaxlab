"""Lote PE2 (v2): E2-1 a E2-11 — a haste que cai presa fora do centro, agora em Three.js (barra de aço com seção visível, furo com pino
a d/4 da ponta, garfo e mancal). E2-1 em 3/4; dolly até a frontal no E2-2; o resto na frontal com as setas do Manim por cima.
Queda com a equação exata α(θ) = (12/7)(g/d) cos θ (d = 1,0 m de cena). Escala fixa das forças: Mg = 1,2 u. ⊕ em degradê ciano→magenta.
Álgebra do zero (v2 §2): Steiner do cartão → frações por glyph map; Στ = Iα → α(θ) com M e d cancelando; energia → ω²(θ);
ΣF = Ma_cm projetada → F_r e F_⊥ com Mg sen θ / Mg cos θ atravessando a igualdade."""
from pecas23 import *  # noqa: F401,F403
from pecas23b import haste25, lupa_pivo

O = P3(-4.4, 1.0)             # eixo (v7: +0,35 u: a haste e a lupa não passam da margem esquerda)
LH = 5.8                      # comprimento d na tela (haste ≥ 70% da coluna do esquema)
KF = 1.2                      # Mg (e g) na tela
LENTA = 4.0                   # câmera lenta da queda


def cam_haste(u):
    """u = 0: 3/4 (az −62°, el 16°); u = 1: frontal pura (eixo apontando para a câmera, plano da queda = plano da tela)."""
    s = smooth(clamp(u, 0, 1))
    if s >= 0.9999:
        return cam_obl(-90.0, 0.0, [0.0, 0.0, 0.0], K=LH, xc=float(O[0]), yc=float(O[1]), fov=FOV3)
    return cam_obl(-62.0 - 28.0 * s, 16.0 * (1 - s), [0.0, 0.0, 0.0], K=LH, xc=float(O[0]), yc=float(O[1]), fov=FOV3)


def ponta_lbl(o, v, m, buff=0.32):
    """Rótulo na ponta da seta o→o+v, do lado de fora (v2 §5 #17)."""
    m.move_to(o + v + vet_unit(v) * buff + 0.0 * UP)
    if m.get_center()[1] > 3.0:                    # v7: rótulo que subiria até o título vai para o lado da ponta
        m.move_to(o + v + 0.5 * RIGHT + 0.0 * UP)
        m.set_y(min(float(m.get_center()[1]), 3.0))
    return m


class LoteE2(Lote23):
    def corpo(self):
        th = ValueTracker(0.0)
        sx = ValueTracker(0.25)       # distância eixo → ⊕ (em d); 1/4 no problema; E2-3 desliza o eixo
        ucam = ValueTracker(0.0)
        self.add(th, sx, ucam)
        h25op = ValueTracker(0.0)
        self.add(h25op)
        fl = dict(h25=False, lupa=False, peso=False, braco=False, F=None, comp=None, acc=False, arco=False, cotav=False, at=True, ac=True, lbl_d=False, rot_F=True, cm=False)
        self.fl = fl

        def est(t):
            e = {"th": round(th.get_value(), 5), "sx": round(sx.get_value(), 4), "cam": cam_haste(ucam.get_value())}
            if not PEDIDOS3D:
                self.reg("haste3d", th=e["th"], eixo=pr(e["cam"], (0, 0, 0)))
            return r4(e)

        f3 = Fundo3D(self, "haste", est, op=0.0)
        self.add(f3)
        self.lbls = {}

        def desenho():
            t, s_ = th.get_value(), sx.get_value()
            u = np.array([math.cos(t), -math.sin(t), 0.0])
            n = np.array([math.sin(t), math.cos(t), 0.0])
            cm = O + s_ * LH * u
            a_, b_ = cm - LH / 2 * u, cm + LH / 2 * u
            g = VGroup()
            if fl["h25"]:                                  # v5 §1.3: a barra em 2.5D frontal (azul-aço escuro, pino e mancal) no lugar do 3D
                h_ = haste25(O, cm, t, LH)
                if h25op.get_value() < 0.999:
                    escala_op(h_, h25op.get_value())
                g.add(h_)
            if fl["cm"]:
                g.add(marcador_cm(cm, r=0.17, z=16))
            if fl["lbl_d"] and t < 0.05:
                c_d = VGroup(Line(a_ + 0.6 * DOWN, b_ + 0.6 * DOWN).set_stroke(C_RAIO, 4.0), lbl("d", C_RAIO, 42).move_to((a_ + b_) / 2 + 0.95 * DOWN))
                c_q = VGroup(Line(a_ + 0.5 * UP, O + 0.5 * UP).set_stroke(C_RAIO, 4.0), lbl(r"\frac{d}{4}", C_RAIO, 40).move_to((a_ + O) / 2 + 1.05 * UP))
                l_M = lbl("M", MAS, 42).move_to(cm + 0.55 * UP + 0.45 * RIGHT)
                self.lbls.update(d=c_d[1], d4=c_q[1], M=l_M)
                g.add(c_d, c_q, l_M)
            if fl["arco"] and t > 0.03:
                g.add(DashedLine(O, O + 1.4 * RIGHT, dash_length=0.07).set_stroke(GEO, 1.8),
                      Arc(radius=0.85, start_angle=-t, angle=t, arc_center=O).set_stroke(ANG, 4),
                      lbl(r"\theta", ANG, 40).move_to(O + 1.2 * np.array([math.cos(t / 2), -math.sin(t / 2), 0]) + 0.1 * RIGHT))
            if fl["peso"]:
                lMg = lbl("Mg", FC, 40).next_to(cm + KF * DOWN, LEFT, buff=0.2)
                self.lbls["Mg"] = lMg
                g.add(seta_s(cm + 0.16 * DOWN, cm + KF * DOWN, FC, 6), lMg)
            if fl["braco"]:
                lb = lbl(r"\tfrac{d}{4}\cos\theta", C_RAIO, 40).move_to(P3((O[0] + cm[0]) / 2, O[1] + 0.66))
                self.lbls["braco"] = lb
                g.add(DashedLine(cm, P3(cm[0], O[1]), dash_length=0.07).set_stroke(GEO, 1.8),
                      Line(O, P3(cm[0], O[1])).set_stroke(GEO, 4), lb)
            if fl["cotav"]:
                lv = lbl(r"\tfrac{d}{4}\operatorname{sen}\theta", C_RAIO, 40).next_to(P3(cm[0] + 0.55, (O[1] + cm[1]) / 2), RIGHT, buff=0.15)
                self.lbls["cotav"] = lv
                g.add(Line(P3(cm[0] + 0.55, O[1]), P3(cm[0] + 0.55, cm[1])).set_stroke(GEO, 3), lv)
            if fl["acc"]:
                f = forca_eixo(t)
                at, ac = f["at"] * KF, f["ac"] * KF
                if fl["at"] and at > 0.08:
                    la = ponta_lbl(cm, -n * at, lbl("a_t", ACC, 40), 0.35)
                    self.lbls["at"] = la
                    g.add(seta_s(cm, cm - n * at, ACC, 6), la)
                if fl["ac"] and ac > 0.08:
                    lc = ponta_lbl(cm, -u * ac, lbl("a_c", ACC, 40), 0.38).shift(0.3 * n)
                    self.lbls["ac"] = lc
                    g.add(seta_s(cm, cm - u * ac, ACC, 6), lc)
            if fl["F"]:
                f = forca_eixo(t)
                F = f["F"] * KF
                self.reg("haste", th=t, F=list(F / KF), seta=[float(F[0]), float(F[1])], modo=fl["F"])
                if fl["F"] == "dash":
                    g.add(DashedLine(O, O + F, dash_length=0.1).set_stroke(FC, 5), ponta_lbl(O, F, lbl(r"\vec F", FC, 42), 0.4))
                else:
                    g.add(seta_s(O, O + F, FC, 7, tip=0.24))
                    if fl["rot_F"]:
                        g.add(ponta_lbl(O, F, lbl(r"\vec F", FC, 42), 0.4))
                if fl["comp"] == "rp":
                    fr, fp = -f["fr"] * KF * u, f["fp"] * KF * n
                    if f["fr"] > 0.05:
                        g.add(DashedLine(O, O + fr, dash_length=0.08).set_stroke(FC, 3.5), ponta_lbl(O, fr, lbl("F_r", FC, 40), 0.42))
                    if f["fp"] > 0.05:
                        g.add(DashedLine(O, O + fp, dash_length=0.08).set_stroke(FC, 3.5), ponta_lbl(O, fp, lbl(r"F_\perp", FC, 40), 0.45))
                elif fl["comp"] == "xy":
                    g.add(DashedLine(O, O + F[0] * RIGHT, dash_length=0.08).set_stroke(FC, 3.5), DashedLine(O + F[0] * RIGHT, O + F, dash_length=0.08).set_stroke(FC, 3.5))
            if fl["lupa"]:                                 # v5 §1.3: lupa do pivô (E2-6 a E2-10)
                f = forca_eixo(t)
                g.add(lupa_pivo(O, t, f["F"] * KF, (-f["fr"] * KF * u) if fl["comp"] == "rp" else None, (f["fp"] * KF * n) if fl["comp"] == "rp" else None))
            return g

        dv = vivo(desenho)

        # ── E2-1: a haste em 3/4 (o eixo atravessando o furo, o garfo) ──
        self.an("E2-1")
        self.secao("EXERCÍCIO 2 · A HASTE E O EIXO")
        self.play(f3.op.animate.set_value(1.0), FadeIn(dv), run_time=0.6)
        tr = self.trilha([("A", T("I", 40)), ("B", T(r"\alpha", 40)), ("C", T(r"\omega", 40)), ("D", txt("FORÇA", 30))])
        self.play(FadeIn(tr), run_time=0.4)
        self.gat("de massa e comprimento conhecidos")
        d1 = VGroup(txt("HASTE UNIFORME:", 30, bold=True, color=GEO), lbl("M", MAS, 44), txt("E", 30), lbl("d", C_RAIO, 44)).arrange(RIGHT, buff=0.18)
        self.pilha.poe(d1)
        self.play(FadeIn(d1, shift=0.08 * UP), run_time=0.5)
        self.gat("a um quarto do comprimento")
        d2 = VGroup(txt("EIXO A", 30, bold=True, color=GEO), lbl(r"\frac{d}{4}", C_RAIO, 44), txt("DE UMA PONTA", 30, bold=True, color=GEO)).arrange(RIGHT, buff=0.18)
        self.pilha.poe(d2)
        self.play(FadeIn(d2, shift=0.08 * UP), run_time=0.6)
        self.gat("solta do repouso na horizontal")
        d3 = txt("SOLTA DO REPOUSO, NA HORIZONTAL", 30, bold=True, color=GEO)
        self.pilha.poe(d3)
        self.play(FadeIn(d3, shift=0.08 * UP), run_time=0.5)
        self.gat("queremos o momento de inércia")
        self.selo("O QUE ESTE PEDE", [["I", "·", lbl(r"\alpha(\theta)", ACC, 38), "·", lbl(r"\omega(\theta)", VEL, 38)], ["FORÇA NO EIXO"]])
        self.gat("principalmente a força do eixo")
        self.play(self.ind_copia(tr[3], CYAN, 1.2, 0.8), run_time=0.8)
        self.ate(0.99)

        # ── E2-2: dolly até a frontal; I pelos eixos paralelos (cartões de Steiner e da haste) ──
        self.an("E2-2")
        self.hip("EIXO SEM ATRITO · SEM RESISTÊNCIA DO AR")
        self.pilha.limpa()
        self.tr_acende(0)
        self.play(ucam.animate.set_value(1.0), run_time=1.4)
        fl["h25"] = True
        self.play(h25op.animate.set_value(1.0), f3.op.animate.set_value(0.0), run_time=0.6)        # match cut 3D → 2.5D (mesma posição e comprimento)
        fl["lbl_d"] = True
        fl["cm"] = True
        self.gat("o centro de massa está no meio")
        self.play(self.ind_copia(marcador_cm(O + 0.25 * LH * RIGHT, r=0.17), WHITE_, 1.6, 0.8), run_time=0.8)
        self.gat("pelos eixos paralelos")
        S0, is0, _ = self.lei("steiner", ("I", "=", r"I_{cm}", "+", "M", "D^2"), rt=0.9)
        HcC, Hci = self.cartao_lei("haste_cm")
        S1, is1, _ = self.gm(S0, is0, ("I", "=", r"\tfrac{1}{12}", "M", "d^2", "+", "M", r"\left(\tfrac{d}{4}\right)^2"), sai=[2, 5],
                             voos={2: mp(HcC, Hci, [2]), 3: mp(HcC, Hci, [3]), 4: mp(HcC, Hci, [4]), 7: self.lbls["d4"]}, rt=1.4)
        self.card_sai()
        self.gat("um doze avos mais um dezesseis avos")
        S2, is2, _ = self.gm(S1, is1, ("I", "=", r"\left(\tfrac{4}{48}+\tfrac{3}{48}\right)", "M", "d^2"),
                             mapas=[([2, 5, 7], [2]), ([3, 6], [3]), ([4], [4])], rt=1.3)
        self.gat("sete quarenta e oito avos")
        S3, is3, cb = self.gm(S2, is2, ("I", "=", r"\tfrac{7}{48}", "M", "d^2"), mapas=[([2], [2])], cores={2: MAS}, size=52, caixa_cor=MAS, rt=1.1)
        self.I_ = (S3, is3)
        self.ate(0.99)

        # ── E2-3: confere — o eixo desliza do centro à ponta; régua 4/48 · 7/48 · 16/48 com nomes em linhas fixas ──
        self.an("E2-3")
        self.selo("CONFERE", "ENTRE OS DOIS")
        self.pilha.so(cb)
        self.card_sai()
        x0, w, yr = 1.2, 5.2, -0.9
        xr = lambda v: x0 + w * (v - 4) / 12
        regua_ = VGroup(Line(P3(x0, yr), P3(x0 + w, yr)).set_stroke(GEO, 3))
        marcas = VGroup()
        for v, rot, cor, dy in ((4, "NO CENTRO", GEO, -0.5), (7, "NOSSO EIXO", MAS, -1.05), (16, "NA PONTA", GEO, -0.5)):
            marcas.add(VGroup(Line(P3(xr(v), yr - 0.15), P3(xr(v), yr + 0.15)).set_stroke(cor, 4), lbl(r"\tfrac{" + str(v) + r"}{48}", cor, 46).move_to(P3(xr(v), yr + 0.6)),
                              txt(rot, 30, bold=True, color=cor).move_to(P3(xr(v), yr + dy))))
        marcas[0][2].shift((x0 - marcas[0][2].get_left()[0] - 0.4) * RIGHT)
        self.play(FadeIn(regua_), run_time=0.4)
        self.gat("com o eixo no centro")
        self.play(sx.animate.set_value(0.0), FadeIn(marcas[0]), run_time=1.0)
        self.gat("na ponta um terço")
        self.play(sx.animate.set_value(0.5), FadeIn(marcas[2]), run_time=1.4)
        self.gat("o nosso eixo está entre os dois")
        self.play(sx.animate.set_value(0.25), FadeIn(marcas[1]), run_time=1.0)
        self.tr_ok(0)
        self.ate(0.99)

        # ── E2-4: Στ = Iα → τ (peso e braço voando do desenho) → α = τ/I → M e d cancelam → α(θ) ──
        self.an("E2-4")
        self.sem_selo()
        self.pilha.so(cb, anims=[FadeOut(regua_), FadeOut(marcas)])
        self.tr_acende(1)
        fl["lbl_d"] = False
        fl["arco"] = True
        self.gat("mede o ângulo a partir da horizontal")
        self.play(th.animate.set_value(math.radians(30)), run_time=1.2)
        self.gat("o único torque é o do peso")
        fl["peso"] = True
        L0, il0, _ = self.lei("newton_rot", (r"\sum", r"\tau", "=", "I", r"\alpha"), rt=0.9)
        self.gat("com braço de um quarto do comprimento")
        fl["braco"] = True
        self.wait(0.3)
        A, ia, ab = self.gm(L0, il0, (r"\tau", "=", "M", "g", r"\tfrac{d}{4}", r"\cos\theta"), sai=[0, 3, 4],
                            voos={2: self.lbls["Mg"][0][0], 3: self.lbls["Mg"][0][1], 4: self.lbls["braco"], 5: self.lbls["braco"]}, rt=1.4)
        self.gat("dividindo pelo momento de inércia")
        self.pilha.so(cb, ab)
        Ab, iab, _ = self.gm(L0, il0, {"pre": (r"\alpha", "="), "num": (r"\tau",), "den": ("I",)}, sai=[0], rt=1.0)
        Ac, iac, _ = self.gm(Ab, iab, {"pre": (r"\alpha", "="), "num": ("M", "g", r"\tfrac{d}{4}", r"\cos\theta"), "den": (r"\tfrac{7}{48}", "M", "d^2")},
                             sai=[2, 4], voos={2: mp(A, ia, [2]), 3: mp(A, ia, [3]), 4: mp(A, ia, [4]), 5: mp(A, ia, [5]),
                                               7: mp(S3, is3, [2]), 8: mp(S3, is3, [3]), 9: mp(S3, is3, [4])}, rt=1.4)
        Ad, iad, adb = self.gm(Ac, iac, (r"\alpha", "=", r"\tfrac{12}{7}", r"\tfrac{g}{d}", r"\cos\theta"), riscar=[2, 8],
                               mapas=[([4, 7], [2]), ([3, 9], [3])], cores={2: ACC}, caixa_cor=ACC, rt=1.4)
        self.gat("ela não é constante")
        mx, my = 1.4, -3.27        # v7: abaixo da caixa do resultado (a barra de α cortava a linha)
        most = vivo(lambda: VGroup(lbl(r"\alpha", ACC, 42).move_to(P3(mx - 0.4, my)),
                                   barra_h(mx, my, 4.6, math.cos(th.get_value()), ACC)).set_z_index(12))
        self.play(FadeIn(most), run_time=0.4)
        self.gat("cai a zero na vertical")
        self.play(th.animate.set_value(math.radians(88)), run_time=2.2)
        self.play(th.animate.set_value(math.radians(30)), run_time=1.0)
        self.tr_ok(1)
        self.ate(0.99)

        # ── E2-5: energia: U_i + K_i = U_f + K_f → Mg(d/4)sen θ = ½Iω² → ω²(θ) ──
        self.an("E2-5")
        self.selo("FERRAMENTA", [[lbl(r"\alpha", ACC, 38), "MUDA"], ["USA A ENERGIA"]])
        self.pilha.so(cb, anims=[FadeOut(most)])
        self.tr_acende(2)
        fl["braco"] = False
        fl["peso"] = False
        self.gat("o centro de massa desce")
        fl["cotav"] = True
        self.play(th.animate.set_value(math.radians(40)), run_time=0.8)
        ex, ey = 1.4, -2.75

        def energia():
            s = math.sin(th.get_value())
            return VGroup(lbl("U", KC, 40).move_to(P3(ex - 0.35, ey + 0.5)), barra_h(ex, ey + 0.5, 4.6, 1 - s, KC),
                          lbl("K", KC, 40).move_to(P3(ex - 0.35, ey - 0.1)), barra_h(ex, ey - 0.1, 4.6, s, KC)).set_z_index(12)

        en = vivo(energia)
        self.pilha.base = -1.95                    # as barras U/K ocupam a faixa de baixo da CONTA
        self.gat("essa energia potencial vira energia cinética")
        C0, ic0, _ = self.linha(("U_i", "+", "K_i", "=", "U_f", "+", "K_f"), rt=1.0, metodo="lei")
        self.play(FadeIn(en), run_time=0.4)
        C1, ic1, _ = self.gm(C0, ic0, ("M", "g", r"\tfrac{d}{4}", r"\operatorname{sen}\theta", "=", r"\tfrac{1}{2}", "I", r"\omega^2"), riscar=[2],
                             mapas=[([0, 4], [0, 1]), ([6], [5, 6, 7])], voos={2: self.lbls["cotav"], 3: self.lbls["cotav"]}, rt=1.5)
        self.play(th.animate.set_value(math.radians(70)), run_time=1.2)
        self.gat("isolando a velocidade angular")
        C2, ic2, _ = self.gm(C1, ic1, {"pre": (r"\omega^2", "="), "num": ("2", "M", "g", r"\tfrac{d}{4}", r"\operatorname{sen}\theta"), "den": ("I",)}, rt=1.3)
        C3, ic3, _ = self.gm(C2, ic2, {"pre": (r"\omega^2", "="), "num": ("2", "M", "g", r"\tfrac{d}{4}", r"\operatorname{sen}\theta"), "den": (r"\tfrac{7}{48}", "M", "d^2")},
                             sai=[8], voos={8: mp(S3, is3, [2]), 9: mp(S3, is3, [3]), 10: mp(S3, is3, [4])}, rt=1.2)
        C4, ic4, cb4 = self.gm(C3, ic3, (r"\omega^2", "=", r"\tfrac{24}{7}", r"\tfrac{g}{d}", r"\operatorname{sen}\theta"), riscar=[3, 9],
                               mapas=[([2, 5, 8], [2]), ([4, 10], [3])], cores={2: VEL}, size=50, caixa_cor=VEL, rt=1.3)
        self.tr_ok(2)
        self.ate(0.99)

        self.pilha.base = -3.25
        # ── E2-6: ΣF = Ma_cm no ⊕; a_t = αD, a_c = ω²D com D = d/4 (setas verdes voando) ──
        self.an("E2-6")
        self.sem_selo()
        self.pilha.so(adb, cb4, anims=[FadeOut(en)])
        fl["cotav"] = False
        self.tr_acende(3)
        self.play(th.animate.set_value(math.radians(35)), run_time=0.8)
        self.gat("a haste só tem duas forças externas")
        fl["peso"] = True
        fl["F"] = "dash"
        fl["lupa"] = True
        self.wait(0.6)
        self.gat("força do eixo mais peso é a massa vezes")
        N0, in0, _ = self.linha((r"\sum", r"\vec F", "=", "M", r"\vec a_{cm}"), rt=0.9, metodo="lei")
        N1, in1, n1b = self.gm(N0, in0, (r"\vec F", "+", "M", r"\vec g", "=", "M", r"\vec a_{cm}"), sai=[0], rt=1.1)
        self.gat("anda num círculo de raio")
        circ = DashedVMobject(Circle(radius=0.25 * LH).move_to(O).set_stroke(GEO, 1.6), num_dashes=40).set_z_index(3)
        self.play(Create(circ), run_time=0.8)
        self.gat("a tangencial")
        fl["acc"] = True
        fl["ac"] = False
        self.wait(0.2)
        self.pilha.so(adb, cb4, n1b)
        T0, it0, _ = self.lei("pontes", ("a_t", "=", r"\alpha", "D", r"\quad", "a_c", "=", r"\omega^2", "D"), rt=1.0)
        T1, it1, t1b = self.gm(T0, it0, ("a_t", "=", r"\tfrac{12}{7}", r"\tfrac{g}{d}", r"\cos\theta", r"\cdot", r"\tfrac{d}{4}", "=", r"\tfrac{3}{7}", "g", r"\cos\theta"),
                               sai=[2, 3, 4, 5, 6, 7, 8], voos={0: self.lbls["at"], 2: mp(Ad, iad, [2]), 3: mp(Ad, iad, [3]), 4: mp(Ad, iad, [4])}, cores={8: ACC}, rt=1.5)
        self.gat("e a centrípeta")
        fl["ac"] = True
        self.wait(0.2)
        T2, it2, t2b = self.gm(T0, it0, ("a_c", "=", r"\tfrac{24}{7}", r"\tfrac{g}{d}", r"\operatorname{sen}\theta", r"\cdot", r"\tfrac{d}{4}", "=", r"\tfrac{6}{7}", "g", r"\operatorname{sen}\theta"),
                               sai=[0, 1, 2, 3, 4, 7, 8], voos={0: self.lbls["ac"], 2: mp(C4, ic4, [2]), 3: mp(C4, ic4, [3]), 4: mp(C4, ic4, [4])}, cores={8: ACC}, rt=1.5)
        self.ate(0.99)

        # ── E2-7: projeções: F_r − Mg sen θ = M a_c → F_r = (13/7)Mg sen θ; Mg cos θ − F_⊥ = M a_t → F_⊥ = (4/7)Mg cos θ ──
        self.an("E2-7")
        self.sem_selo()
        self.card_sai()
        self.pilha.so(n1b, t1b, t2b)
        self.gat("projetando ao longo da haste")
        fl["F"] = "solid"
        fl["comp"] = "rp"
        R0, ir0, _ = self.gm(N1, in1, ("F_r", "-", "M", "g", r"\operatorname{sen}\theta", "=", "M", "a_c"), mapas=[([0], [0]), ([3], [3, 4]), ([6], [7])], rt=1.2)
        R1, ir1, _ = self.gm(R0, ir0, ("F_r", "=", "M", "a_c", "+", "M", "g", r"\operatorname{sen}\theta"), mapas=[([1], [4])], rt=1.2)
        self.gat("o eixo puxa para dentro")
        R2, ir2, r2b = self.gm(R1, ir1, ("F_r", "=", r"\left(\tfrac{6}{7}+1\right)", "M", "g", r"\operatorname{sen}\theta"), mapas=[([3, 4], [2]), ([2, 5], [3])], rt=1.2)
        R3, ir3, r3b = self.gm(R2, ir2, ("F_r", "=", r"\tfrac{13}{7}", "M", "g", r"\operatorname{sen}\theta"), mapas=[([2], [2])], cores={2: FC}, caixa_cor=FC, rt=1.0)
        self.gat("segura com quatro sétimos")
        self.pilha.so(n1b, t1b, r3b)
        P0, ip0, _ = self.gm(N1, in1, ("M", "g", r"\cos\theta", "-", r"F_\perp", "=", "M", "a_t"), mapas=[([2], [0]), ([3], [1, 2]), ([0], [4]), ([6], [7])], rt=1.2)
        P1, ip1, _ = self.gm(P0, ip0, (r"F_\perp", "=", "M", "g", r"\cos\theta", "-", "M", "a_t"), rt=1.2)
        P2, ip2, p2b = self.gm(P1, ip1, (r"F_\perp", "=", r"\tfrac{4}{7}", "M", "g", r"\cos\theta"), riscar=[], mapas=[([5, 6, 7], [2])], cores={2: FC}, caixa_cor=FC, rt=1.2)
        self.gat("o comprimento da haste sumiu")
        self.pilha.so(r3b, p2b)
        nd = VGroup(lbl("d", C_RAIO, 44), txt("SUMIU", 30, bold=True, color=GEO)).arrange(RIGHT, buff=0.14)
        self.pilha.poe(nd)
        self.play(FadeIn(nd, shift=0.08 * UP), run_time=0.5)
        self.play(th.animate.set_value(math.radians(60)), run_time=2.0)
        self.play(th.animate.set_value(math.radians(35)), run_time=1.4)
        self.ate(0.99)

        # ── E2-8: parada em θ = 0 ──
        self.an("E2-8")
        self.selo("CONFERE", [["0 <", lbl(r"\tfrac{4}{7}", FC, 40), "< 1"]])
        self.pilha.limpa(anims=[FadeOut(circ)])
        fl["comp"] = None
        fl["acc"] = False
        self.gat("na largada ângulo zero")
        self.play(th.animate.set_value(0.0), run_time=1.0)
        fl["rot_F"] = False
        F0v = forca_eixo(0)["F"] * KF
        lF0 = lbl(r"\tfrac{4}{7}\,Mg", FC, 42).next_to(O + F0v, LEFT, buff=0.25)
        self.gat("quatro sétimos do peso para cima")
        self.play(FadeIn(lF0), run_time=0.5)
        A, ia, _ = self.linha((r"\theta=0", r":\ ", "F", "=", r"\tfrac{4}{7}", "M", "g", r"\ \uparrow"), voos={4: lF0}, cores={4: FC}, size=48, rt=1.2)
        self.gat("começa descendo com três sétimos")
        B, ib, _ = self.linha(("a_{cm}", "=", r"\tfrac{3}{7}", "g", r"\ \downarrow"), cores={2: ACC}, size=48, rt=1.0)
        x0, w, yr = 1.3, 5.0, -1.7
        rg = VGroup(Line(P3(x0, yr), P3(x0 + w, yr)).set_stroke(GEO, 3))
        for v, s, rot, dy in ((0, "0", "QUEDA LIVRE", -0.5), (4 / 7, r"\tfrac{4}{7}", "NOSSO EIXO", -1.05), (1, "1", "SEGURA TUDO", -0.5)):
            cor = FC if 0 < v < 1 else GEO
            rg.add(Line(P3(x0 + w * v, yr - 0.15), P3(x0 + w * v, yr + 0.15)).set_stroke(cor, 4), lbl(s, cor, 44).move_to(P3(x0 + w * v, yr + 0.6)),
                   txt(rot, 30, bold=True, color=cor).move_to(P3(x0 + w * v, yr + dy)))
        rg[3].shift((x0 - 0.35 - rg[3].get_left()[0]) * RIGHT)
        rg[9].shift((x0 + w + 0.3 - rg[9].get_right()[0]) * RIGHT)
        self.gat("o eixo não segura o peso inteiro")
        self.play(FadeIn(rg), run_time=0.7)
        self.ate(0.99)

        # ── E2-9: parada em θ = 45° ──
        self.an("E2-9")
        self.sem_selo()
        self.pilha.limpa(anims=[FadeOut(rg), FadeOut(lF0)])
        self.gat("a quarenta e cinco graus")
        self.play(th.animate.set_value(math.pi / 4), run_time=1.6)
        fl["comp"] = "xy"
        circ2 = DashedVMobject(Circle(radius=0.25 * LH).move_to(O).set_stroke(GEO, 1.6), num_dashes=40).set_z_index(3)
        F45 = forca_eixo(math.pi / 4)["F"] * KF
        lx = lbl(r"\tfrac{9}{14}\,Mg", FC, 40).move_to(O + 2.2 * LEFT + 0.85 * DOWN)      # v6 #13: fora da barra, do mancal e da lupa
        ly = lbl(r"\tfrac{17}{14}\,Mg", FC, 40).move_to(O + 2.0 * LEFT + 1.25 * UP)
        self.gat("o eixo também empurra de lado")
        self.play(FadeIn(lx), run_time=0.5)
        A, ia, _ = self.linha(("F_x", "=", r"\tfrac{9}{14}", "M", "g", r"\ (\leftarrow)"), voos={2: lx}, cores={2: FC}, size=48, rt=1.1)
        self.gat("e a vertical dezessete")
        self.play(FadeIn(ly), run_time=0.5)
        B, ib, _ = self.linha(("F_y", "=", r"\tfrac{17}{14}", "M", "g", r"\ \uparrow"), voos={2: ly}, cores={2: FC}, size=48, rt=1.1)
        self.gat("no total uma vírgula três sete")
        C_, ic, _ = self.linha((r"|\vec F|", "=", r"1{,}37", "M", "g"), cores={2: FC}, size=50, rt=1.0, caixa_cor=FC)
        self.gat("o centro de massa está fazendo uma curva")
        self.play(Create(circ2), run_time=0.9)
        arco_cm = Arc(radius=0.25 * LH, start_angle=-math.pi / 4 - 0.25, angle=0.5, arc_center=O).set_stroke(ACC, 5).set_z_index(4)
        self.play(Create(arco_cm), run_time=0.6)
        self.ate(0.99)

        # ── E2-10: parada em θ = 90°; depois queda contínua com |F|/Mg ao vivo ──
        self.an("E2-10")
        self.selo("CONFERE", [[lbl(r"\alpha=0", ACC, 38), "·", lbl(r"\omega", VEL, 38), "MÁXIMA"]])
        self.pilha.limpa(anims=[FadeOut(VGroup(lx, ly, circ2, arco_cm))])
        fl["comp"] = None
        self.gat("e na vertical noventa graus")
        self.play(th.animate.set_value(math.pi / 2), run_time=1.6)
        F90 = forca_eixo(math.pi / 2)["F"] * KF
        l90 = lbl(r"\tfrac{13}{7}\,Mg", FC, 42).next_to(O + 0.75 * F90, RIGHT, buff=0.35)
        self.gat("sobram treze sétimos do peso")
        self.play(FadeIn(l90), run_time=0.5)
        A, ia, _ = self.linha((r"\theta=90^\circ", r":\ ", "F", "=", r"\tfrac{13}{7}", "M", "g", r"\ \uparrow"), voos={4: l90}, cores={4: FC}, size=48, rt=1.2, caixa_cor=FC)
        self.gat("aceleração angular zero não é parada")
        B, ib, _ = self.linha((r"\alpha", "=", "0", r",\quad", r"\omega", "=", r"\omega_{\max}"), size=48, rt=1.1)
        gx0, gy0, gw, gh = 1.6, -3.0, 4.4, 1.7
        fmax = 13 / 7
        pg = lambda t_, v: P3(gx0 + gw * t_ / (math.pi / 2), gy0 + gh * v / fmax)
        ax = VGroup(Line(pg(0, 0), pg(math.pi / 2, 0)).set_stroke(GEO, 2), Line(pg(0, 0), pg(0, fmax) + 0.15 * UP).set_stroke(GEO, 2),
                    lbl(r"|\vec F|/Mg", FC, 38).move_to(pg(0, fmax) + 0.45 * UP + 0.75 * RIGHT), lbl(r"\theta", ANG, 40).move_to(pg(math.pi / 2, 0) + 0.35 * RIGHT),
                    lbl(r"\tfrac{4}{7}", FC, 40).move_to(pg(0, 4 / 7) + 0.4 * LEFT), lbl(r"\tfrac{13}{7}", FC, 40).move_to(pg(0, fmax) + 0.42 * LEFT),
                    lbl(r"90^\circ", ANG, 36).move_to(pg(math.pi / 2, 0) + 0.38 * DOWN)).set_z_index(10)
        curva = VMobject().set_points_as_corners([pg(t_, forca_eixo(t_)["mod"]) for t_ in np.linspace(0, math.pi / 2, 90)]).set_stroke(FC, 4).set_z_index(11)
        ponto = vivo(lambda: Dot(pg(th.get_value(), forca_eixo(th.get_value())["mod"]), radius=0.08, color=ANG).set_z_index(13))
        self.gat("numa única queda")
        self.play(FadeOut(l90), th.animate.set_value(0.0), FadeIn(ax), Create(curva), run_time=1.0)
        fl["rot_F"] = False
        self.add(ponto)
        tq = ValueTracker(0.0)
        self.add(tq)
        th.add_updater(lambda m: m.set_value(haste_th(tq.get_value())))
        self.play(tq.animate.set_value(T_HASTE), run_time=T_HASTE * LENTA * 2, rate_func=linear)
        th.clear_updaters()
        self.tr_ok(3)
        self.ate(0.99)

        # ── E2-11: DICA ──
        self.an("E2-11")
        fl["lupa"] = False
        self.selo("DICA", "FORÇA NO EIXO = NEWTON NO ⊕ · AS DUAS ACELERAÇÕES")
        self.pilha.limpa(anims=[FadeOut(VGroup(ax, curva, ponto))])
        fl["rot_F"] = True
        self.play(th.animate.set_value(math.radians(50)), run_time=1.0)
        self.gat("a força no eixo sai")
        A, ia, _ = self.linha((r"\vec F", "=", "M", r"\vec a_{cm}", "-", "M", r"\vec g"), size=50, rt=1.2, caixa_cor=FC, metodo="lei")
        self.gat("esquecer a centrípeta")
        B, ib, _ = self.linha((r"\vec a_{cm}", "=", r"\vec a_t", "+", r"\vec a_c"), size=50, rt=1.1, metodo="lei")
        self.play(self.ind_copia(mp(B, ib, [4]), ACC, 1.2, 0.8), run_time=0.8)
        self.ate(0.99)
