"""Lote PH · v3. H gancho em JOGO DE PARES (alvos v3_h1 e v3_h2) + A bem-vindos em ESCADA (alvo v3_ab).
H: três palcos nascem com o campo em cor de contexto e o quadradinho tracejado; cada filme roda UMA vez na sua frase (fl1, fl2, fl3); as três
fórmulas, fora de ordem (③, ①, ②), em caixas com a MESMA largura e posição dos palcos (pedido do Kaio); '?' âmbar; o título. Na segunda metade,
o fio e a carga: círculos r e 2r, a seta copiada desliza até 2r encolhendo (÷2 no fio, ÷4 na carga); as duas leis embaixo.
A: o logo pequeno à esquerda e o título juntos; cada item da fala desenha um degrau; as quatro caixas da Parte 2 a 45 %; o degrau DOIS FILMES
cresce até virar o palco do D1."""
from escada30 import *  # noqa: F401,F403

PALCOS = [(120, 260, 660, 710), (690, 260, 1230, 710), (1260, 260, 1800, 710)]     # lados múltiplos do quadradinho da grade
FORM = [r"\F=(\X^2-\Y^2,\ 2\X\Y)", r"\F=(\X+\Y,\ \X-\Y)", r"\F=(1,\ \X-\Y)"]          # fora de ordem: ③, ①, ②
LEG = ["SÓ ENTORTA", "GIRA, ENCOLHE E ENTORTA", "UM GIRA · OUTRO CRESCE"]


def palco_h(k):
    box = PALCOS[k]
    if k < 2:
        v = VB(box, (box[0] + box[2]) / 2, 470, 56)
        Fv, flx, c, s, T_ = (F1, fl1, [(0.0, 0.0)], 1.6, .32) if k == 0 else (F2, fl2, [(-1.2, -.4)], 1.4, .75)
        cmp = campo30(v, Fv, -4, 4, -3, 3, .75, rmin=0, mmax=5, ctx=True, skip=ou(*[dq(p, s) for p in c]), nome=f"H palco {k + 1}")
    else:
        v = VB(box, 1440, 650, 120)
        Fv, flx, c, s, T_ = F3, fl3, [(1.0, 0.0), (0.0, 1.0)], .34, .12
        cmp = campo30(v, Fv, -1, 2.25, -.25, 2.5, .25, rmin=0, mmax=6, ctx=True, skip=ou(*[dq(p, s, .1) for p in c]), nome="H palco 3")
    ch = chapa_px(*box, nome=f"H palco {k + 1}", v=v)
    fans = [fantasma(v, quad_pts(p, s)) for p in c]
    peds = [quad30(v, p, s) for p in c]
    return dict(v=v, ch=ch, cmp=cmp, fans=fans, peds=peds, fl=flx, c=c, s=s, T=T_)


def lado_h2(X0, cx, fio):
    v = VB((X0, 270, X0 + 540, 810), cx, 540, 60)
    ch = chapa_px(X0, 270, X0 + 540, 810, nome="H2 " + ("fio" if fio else "carga"), v=v)
    cmp = campo30(v, VORTA(1) if fio else F_CARGA, -4, 4, -4, 4, .75, rmin=.8, mmax=1.6, ctx=True,
                  skip=lambda X, Y: math.hypot(X, Y) < 1.6, nome="H2 campo " + ("fio" if fio else "carga"))
    c1 = vlinha(v, circ_pts(1), GEO, 2, alpha=.8, dash=(9, 8)).set_z_index(5)
    c2 = vlinha(v, circ_pts(2), GEO, 2, alpha=.8, dash=(9, 8)).set_z_index(5)
    if fio:
        fonte = VGroup(preenche(v, circ_pts(.3), "#0F0C26", 1.0, 10), vcirc(v, .3, BR, 3).set_z_index(11), ponto7(v.c2p(0, 0), BR, 5, 12))
        L1 = 1.3
        s1 = seta7(v.c2p(1, -L1 / 2), v.c2p(1, L1 / 2), CAMPO2, 6, 22).set_z_index(13)
        s2 = seta7(v.c2p(2, -L1 / 4), v.c2p(2, L1 / 4), CAMPO2, 6, 18).set_z_index(13)
        k_ = TXP30("÷2", *canto_xy(v, 2.55, .9), 30, "center", CAMPO2, bold=True)
    else:
        fonte = VGroup(preenche(v, circ_pts(.35), CARGA, 1.0, 10), T("+", cx, 553, 34, "center").set_z_index(12))
        L1 = 1.6
        s1 = seta7(v.c2p(.45, 0), v.c2p(.45 + L1, 0), CAMPO2, 6, 22).set_z_index(13)
        s2 = seta7(v.c2p(2, 0), v.c2p(2 + L1 / 4, 0), CAMPO2, 6, 14).set_z_index(13)
        k_ = TXP30("÷4", *canto_xy(v, 2.55, .55), 30, "center", CAMPO2, bold=True)
    r1 = TXP30("r", *canto_xy(v, -.75, .95), 30, "center", GEO, bold=True, up=False)
    r2 = TXP30("2r", *canto_xy(v, -1.45, 1.75), 30, "center", GEO, bold=True, up=False)
    sob = lambda lab: [s for s in cmp if hasattr(s, "_xy") and np.all(np.abs(np.array(v.c2p(*s._xy))[:2] - lab.get_center()[:2]) < np.array(
        [lab.width / 2 + .32, lab.height / 2 + .32]))]
    return dict(v=v, ch=ch, cmp=cmp, c1=c1, c2=c2, fonte=fonte, s1=s1, s2=s2, k=k_, r1=r1, r2=r2, sob=sob)


class LoteH(Base):
    CANTO = False

    def corpo(self):
        # ── H · gancho: três filmes em cima, três fórmulas fora de ordem embaixo (alvo v3_h1) ──
        self.an("H-1")
        zera_chapas()
        P = [palco_h(k) for k in range(3)]
        for p in P:
            clareira(p["cmp"], (lambda p=p: ou(*[clar_ped(q, .12 if p["s"] < 1 else .25) for q in p["peds"] if q in self.mobjects]) if any(
                q in self.mobjects for q in p["peds"]) else NADA))
        self.play(*[FadeIn(p["ch"]) for p in P], *[cresce_campo(p["cmp"], 0.8) for p in P], *[FadeIn(f) for p in P for f in p["fans"]], run_time=0.8)
        legs = [legenda(t, (b[0] + b[2]) / 2, 755, GEO, "center", 28) for t, b in zip(LEG, PALCOS)]
        giros = []

        def solta(k, rt, giro_em=None):
            p = P[k]
            self.add(*p["peds"])
            ans = [anda(q, p["fl"], p["T"], rt, rate=smooth, nome=f"H filme {k + 1} {c}") for q, c in zip(p["peds"], p["c"])]
            self.play(*ans, caneta(legs[k], ritmo=0.15), run_time=rt)
            ex = []
            for i in (giro_em or []):
                Fc = ponto_fl(p["fl"], p["c"][i], p["T"])
                g = giro30(p["v"], Fc, 1.0 if k < 2 else .32, True)
                giros.append(g)
                ex.append(Create(g))
            if ex:
                self.play(*ex, run_time=0.4)
        self.gat("um só entorta")
        solta(0, 0.85)
        self.gat("outro gira encolhe e entorta")
        solta(1, 1.8, [0])
        self.gat("e no terceiro campo")
        solta(2, 2.0, [1])
        caixas, fs_ = [], []
        for b, f in zip(PALCOS, FORM):
            caixas.append(caixa30(b[0], 825, b[2] - b[0], 96, GEO, .9))
            fs_.append(TC(f, (b[0] + b[2]) / 2, 873, 34, "c"))
        qs = [T("?", (b[0] + b[2]) / 2, 808, 40, "center", E1) for b in PALCOS]
        self.gat("embaixo três fórmulas fora de ordem")
        self.play(*[Create(cx) for cx in caixas], run_time=0.3)
        for f in fs_[1:]:
            f._origem = "a"
            print(f"[origem] a {self.lote} H-1 {self.t:.2f} {f._tex!r}")
        escreve(self, fs_[0], 0.12, extra=[caneta(fs_[1], ritmo=0.12, atraso=0.35), caneta(fs_[2], ritmo=0.12, atraso=0.7)])
        self.play(*[FadeIn(q, shift=0.06 * DOWN) for q in qs], run_time=0.3)
        tit = T("QUAL FÓRMULA FAZ QUAL FILME?", 960, 215, 42, "center")
        self.gat("a pergunta é")
        self.play(caneta(tit, ritmo=0.2), run_time=1.0)
        self.gat("dá e hoje é você")
        acende(self, qs, CAMPO2, 1.2)
        self.gat("exatamente as mesmas contas")                     # as caixas das contas citadas acendem (só o contorno)
        acende(self, caixas, BR, 1.2)

        # ── segunda metade: r e 2r; a seta cai pela metade (fio) e para um quarto (carga) (alvo v3_h2) ──
        zera_chapas()
        Fi, Ca = lado_h2(150, 420, True), lado_h2(1230, 1500, False)
        t2 = T("POR QUE 1/r? POR QUE 1/r²?", 960, 215, 40, "center", up=False)
        self.gat("por que o campo magnético")
        troca(self, "H filmes → fio e carga")
        sai = [m for p in P for m in (p["ch"], p["cmp"], *p["fans"], *p["peds"])] + giros + legs + caixas + fs_ + qs + [tit]
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        lf = legenda("FIO COM CORRENTE", 420, 855, GEO, "center", 28)
        for s_ in Fi["sob"](Fi["r1"]):
            op_seta(s_, 0)
        self.play(FadeIn(t2), FadeIn(Fi["ch"]), cresce_campo(Fi["cmp"], 0.7), FadeIn(Fi["fonte"]), Create(Fi["c1"]), FadeIn(Fi["r1"]), FadeIn(lf),
                  run_time=0.8)
        self.play(GrowArrow(Fi["s1"]), run_time=0.4)

        def dobra(L, rt=0.8):
            anel = [s for s in L["cmp"] if hasattr(s, "_xy") and math.hypot(*s._xy) < 2.5] + L["sob"](L["r2"])   # v3: abre quando o 2r entra
            self.play(Create(L["c2"]), FadeIn(L["r2"]), *[UpdateFromAlphaFunc(s, lambda m, a: op_seta(m, 1 - a)) for s in anel], run_time=0.5)
            cp = L["s1"].copy()
            self.add(cp)
            self.play(Transform(cp, L["s2"]), run_time=rt)
            self.remove(cp)
            self.add(L["s2"])
            self.play(FadeIn(L["k"], scale=0.8), *[UpdateFromAlphaFunc(s, lambda m, a: op_seta(m, 1 - a)) for s in L["sob"](L["k"])], run_time=0.3)
        self.gat("enfraquece com um sobre a distância")
        dobra(Fi)
        dd = legenda("DOBRA A DISTÂNCIA →", 960, 560, GEO, "center", 28)
        self.play(FadeIn(dd, shift=0.05 * RIGHT), run_time=0.4)
        lc = legenda("CARGA", 1500, 855, GEO, "center", 28)
        self.gat("e o campo de uma carga")
        for s_ in Ca["sob"](Ca["r1"]):
            op_seta(s_, 0)
        self.play(FadeIn(Ca["ch"]), cresce_campo(Ca["cmp"], 0.7), FadeIn(Ca["fonte"]), Create(Ca["c1"]), FadeIn(Ca["r1"]), FadeIn(lc), run_time=0.8)
        self.play(GrowArrow(Ca["s1"]), run_time=0.4)
        self.gat("ao quadrado")
        dobra(Ca)
        b1 = TC(r"|\B|\propto\dfrac1r", 420, 945, 38, "c")
        e1 = TC(r"|\E|\propto\dfrac1{r^2}", 1500, 945, 38, "c")
        self.gat("é o rotacional e o divergente")
        escreve(self, b1, 0.25)
        escreve(self, e1, 0.25)
        self.ate(1.0)

        # ── A · bem-vindos: a escada (alvo v3_ab) ──
        self.an("A-1")
        lg = self.logo(300 / 120).move_to(PX(300, 150))
        ta = T("CÁLCULO III · ", 560, 165, 44)
        tb = T("EXERCÍCIOS DO MÓDULO", ta.get_right()[0] * 120 + 960 + 14, 165, 44)
        self.limpa_junto()
        troca(self, "H → A (escada)")
        self.play(FadeIn(lg, shift=0.05 * RIGHT), FadeOut(self.wm), caneta(ta, ritmo=0.08), caneta(tb, ritmo=0.08), run_time=1.0)
        self.remove(self.wm)
        D = [Degrau(i, 1, "ab") for i in range(6)]
        Ap = [Degrau(i, 2, "ab", .45) for i in range(4)]
        p1, p2 = titulos_escada()
        fant = VGroup(*[d.caixa.copy() for d in D], *[a.caixa.copy() for a in Ap])      # C7: a silhueta da escada, traço fraco, logo depois do título
        for f, d in zip(fant, [*D, *Ap]):
            f.set_fill(opacity=0).set_stroke(d.cor, 3 / 1.2, 0.30)
            f._sem_contorno = True
            f._fantasma = True
        fant.set_z_index(-1)
        self.play(LaggedStart(*[Create(f) for f in fant], lag_ratio=0.08), run_time=1.2)

        def risca(m, fr, ate):
            ln = Line(m.get_corner(DL) + DOWN * 10 / 120, m.get_corner(DR) + DOWN * 10 / 120).set_stroke(GEO, 2 / 1.2, 1)
            ln._sem_contorno = True
            self.gat(fr)
            self.play(Create(ln), run_time=0.3)
            self.gat(ate)
            self.play(FadeOut(ln), run_time=0.3)
            self.remove(ln)
        risca(ta, "quarto episódio da nossa série", "e hoje é dia")
        risca(tb, "o integrador do módulo", "só com exercícios")
        self.gat("vai ser uma escada")
        self.play(Create(D[0].caixa), FadeIn(p1, shift=0.04 * UP), run_time=0.5)
        self.gat("ler uma fórmula de dois jeitos")
        self.play(FadeIn(D[0].ic), FadeIn(D[0].rot, shift=0.04 * UP), run_time=0.45)
        for i, fr in ((1, "desenhar um campo"), (2, "uma família de redemoinhos"), (3, "duas regras"), (4, "um campo que não melhora de perto"),
                      (5, "e no topo o desafio")):
            self.gat(fr)
            degrau_entra(self, [D[i]], 0.8)
        self.gat("depois as aplicações")
        self.play(FadeIn(p2, shift=0.04 * UP), run_time=0.4)
        for i, fr in ((0, "um rio"), (1, "um jato numa parede"), (2, "mapas que não entortam"), (3, "e as leis do um sobre a distância")):
            self.gat(fr)
            self.play(FadeIn(Ap[i], shift=0.04 * LEFT), run_time=0.4)
        self.gat("pausa o vídeo e tenta")
        self.pausa(dur=min(3.0, self.resta() - 2.2))
        # o degrau DOIS FILMES cresce até virar o palco do D1 (painel da esquerda do layout B)
        alvo = RoundedRectangle(width=(BE[2] - BE[0]) / 120, height=(BE[3] - BE[1]) / 120, corner_radius=8 / 120).move_to(PX((BE[0] + BE[2]) / 2,
                                                                                                                              (BE[1] + BE[3]) / 2))
        alvo.set_fill(PLACA_V4, 0.92).set_stroke(GEO, 3 / 1.2, 1)
        resto = [*(d for d in D[1:]), *Ap, p1, p2, lg, ta, tb, D[0].ic, D[0].rot, fant]
        self.play(Transform(D[0].caixa, alvo), *[FadeOut(m) for m in resto], FadeIn(self.h1), FadeIn(self.wm), run_time=1.0)
        self.remove(*resto)
        self.sai_fim()
