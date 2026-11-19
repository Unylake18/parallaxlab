"""Lote PA2 · A2 ÁGUA BATENDO NA PAREDE (alvo 24). Origem (600, 840): parede em y = 0 (GEO 6 px, hachura embaixo), rede de (x, −y) só em y ≥ 0,5,
hipérboles xy = c tracejadas (c = 0,5; 1; 2; 3,5), tudo recortado na moldura. A gota de tinta é o quadradinho em (0, 3), solto até t = 0,9. A
conferência u·y + x·v = xy − xy = 0 em caneta; depois φ, ∇²φ e EQUAÇÃO DE LAPLACE."""
from lib30 import *  # noqa: F401,F403

VP = VB(LA, 600, 840, 120)
CG, SG_, TG = (0.0, 3.0), 1.0, .9


def parede():
    g = VGroup(linha_rec(VP, [(-4, 0), (4, 0)], LA, GEO, 6))
    X = -3.9
    while X < 4:
        g.add(linha_rec(VP, [(X, 0), (X - .25, -.25)], LA, GEO, 2, .6))
        X += .35
    return g.set_z_index(6)


def hiperboles():
    g = VGroup()
    for k in (.5, 1, 2, 3.5):
        for sg in (1, -1):
            pts = [(sg * X, k / X) for X in np.arange(.12, 4.0001, .04) if k / X <= 5.5]
            g.add(linha_rec(VP, pts, LA, GEO, 2, .55, dash=(8, 8)))
    return g.set_z_index(4)


class LoteA2(Base):
    ANTES = "APLICAÇÃO · O RIO"

    def corpo(self):
        # ── A2-1 · o jato e a parede ──
        self.an("A2-1")
        self.secao("APLICAÇÃO · ÁGUA BATENDO NA PAREDE")
        zera_chapas()
        chA = chapa_px(*LA, nome="A2 palco (600, 840)", v=VP)
        pw = parede()
        ped = quad30(VP, CG, SG_)
        fan = fantasma(VP, quad_pts(CG, SG_))
        st = {"q": False}
        cmp = campo30(VP, F_SELA, -3.5, 3.5, .5, 5.5, .5, rmin=0, mmax=4, nome="A2 (x, −y), y ≥ 0,5")
        troca(self, "A1 → A2 (palco com a origem em (600, 840))")
        self.play(FadeIn(chA), run_time=0.6)
        self.gat("batendo numa parede")
        self.play(Create(pw), run_time=0.6)
        vv = TC(r"\vv=(\X,\ -\Y),\ \ \Y\ge0", 1120, 280, 42)
        mi = legenda("MODELO IDEAL PERTO DO PONTO DE CHOQUE", 1124, 350, GEO, "left", 26)
        self.gat("num modelo ideal")
        self.play(FadeIn(mi, shift=0.05 * UP), run_time=0.4)
        self.gat("a velocidade tem a coordenada horizontal")
        self.play(cresce_campo(cmp, 0.8), caneta(vv, ritmo=0.35), run_time=1.6)
        clareira(cmp, lambda: ou(clar_ped(ped), dq(CG, SG_)) if st["q"] else NADA)
        self.ate(1.0)

        # ── A2-2 · desliza; só deforma; as hipérboles ──
        self.an("A2-2")
        rd = TC(r"\rot\vv=\V0,\quad \dv\vv=\D0,\quad d_1=\Lm2", 1120, 440, 38)
        self.gat("rotacional zero divergente zero")
        self.play(caneta(rd, ritmo=0.3))
        self.gat("uma gota de tinta")
        st["q"] = True
        self.play(FadeIn(ped), FadeIn(fan), run_time=0.4)
        a0 = ped.area()
        self.play(anda(ped, fl_sela, TG, 2.0, rate=linear, nome="A2 gota"))
        print(f"[A2] gota: área {a0:.4f} → {ped.area():.4f}")
        hp = hiperboles()
        lc = leg_mix(["LINHAS DE CORRENTE: xy = CONSTANTE"], 1124, 815, GEO, "left", 26)
        self.gat("as linhas de corrente são hipérboles")
        self.play(Create(hp), FadeIn(lc, shift=0.05 * UP), run_time=0.8)
        cf = TC(r"\Uu\,\Y+\X\,\Vv=\X\Y-\X\Y=0", 1120, 540, 38)
        self.gat("confere andando com a água")
        self.play(caneta(cf, ritmo=0.35))
        self.ate(1.0)

        # ── A2-3 · o potencial; o laplaciano ──
        self.an("A2-3")
        ph = TC(r"\varphi=\tfrac12(\X^2-\Y^2),\quad \nabla\varphi=\vv", 1120, 540, 38)
        self.gat("esse campo é o gradiente")
        self.play(FadeOut(cf), caneta(ph, ritmo=0.3), run_time=1.4)
        self.remove(cf)
        lp = TC(r"\nabla^2\varphi=\dv\,\nabla\varphi=1-1=0", 1120, 640, 42)
        self.gat("e o laplaciano dela")
        self.play(caneta(lp, ritmo=0.35))
        self.ate(1.0)

        # ── A2-4 · a equação de Laplace ──
        self.an("A2-4")
        eq = T("EQUAÇÃO DE LAPLACE", 1120, 750, 40)
        self.gat("a equação de laplace")
        self.play(FadeIn(eq, shift=0.05 * UP), run_time=0.4)
        cmp.clear_updaters()
        self.sai_fim()
