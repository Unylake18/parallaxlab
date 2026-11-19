"""Lote PA1 · P2 transição (PARTE 2 · AS APLICAÇÕES, sem palco) + A1 O RIO (alvo 23). Margens em x = ±3 (GEO 5 px, hachura curta para fora,
recortadas); primeiro o perfil (só a linha de setas de y = −2,5, proporcionais), depois a rede inteira; enunciado curto + PAUSE E TENTE; depois as
contas (v, div, rot, d₁ e d₂), cada uma no seu trecho. Três quadradinhos (lado 0,9) soltos juntos até t = 1,2; ↺ à esquerda, ↻ à direita."""
from lib30 import *  # noqa: F401,F403

CS = [(-2.4, -1.6), (0.0, -1.6), (2.4, -1.6)]
SR, TR = .9, 1.2


def margens():
    g = VGroup()
    for X in (-3, 3):
        g.add(linha_rec(VA, [(X, -3.2), (X, 3.2)], LA, GEO, 5))
        for k in range(16):
            Y = -2.9 + .4 * k
            g.add(linha_rec(VA, [(X, Y), (X + (-.25 if X < 0 else .25), Y - .25)], LA, GEO, 2, .6))
    return g.set_z_index(5)


class LoteA1(Base):
    ANTES = None

    def corpo(self):
        # ── P2 · PARTE 2 ──
        self.an("P2-1")
        p1 = T("PARTE 2", 960, 500, 28, "center", GEO, bold=False)
        p2 = T("AS APLICAÇÕES", 960, 580, 54, "center")
        troca(self, "D5 → P2 (tela de passagem)")
        self.play(FadeIn(p1, shift=0.05 * UP), FadeIn(p2, shift=0.05 * UP), run_time=0.6)
        self.ate(1.0)

        # ── A1-1 · o canal; enunciado ──
        self.an("A1-1")
        self.secao("APLICAÇÃO · O RIO")
        zera_chapas()
        chA = chapa_px(*LA, nome="A1 palco", v=VA)
        mg = margens()
        peds = [quad30(VA, c, SR) for c in CS]
        fans = [fantasma(VA, quad_pts(c, SR)) for c in CS]
        st = {"q": False, "g": []}
        rede = campoP30(VA, RIO, -2.5, 2.5, passo=.5, rmin=0, mref=1, nome="A1 rio")
        perfil = VGroup(*[s for s in rede if abs(s._xy[1] + 2.5) < 1e-6])
        resto = VGroup(*[s for s in rede if abs(s._xy[1] + 2.5) >= 1e-6])
        en = leg_mix(["CANAL DE 6 m · 1 m/s NO MEIO · ZERO NAS MARGENS"], 1124, 330, GEO, "left", 28)
        self.limpa_junto()
        troca(self, "P2 → A1 (palco do rio)")
        self.play(FadeIn(chA), Create(mg), run_time=0.8)
        self.play(FadeIn(en, shift=0.05 * UP), run_time=0.4)
        self.gat("a água corre a um metro")
        self.play(cresce_campo(perfil, 0.6, chave=lambda s: s._xy[0]))
        self.gat("numa parábola")
        self.play(cresce_campo(resto, 0.8, chave=lambda s: s._xy[1]))
        clareira(rede, lambda: ou(*([clar_ped(p) for p in peds] + [dq(c, SR) for c in CS] if st["q"] else []), *st["g"]))
        self.gat("pausa o vídeo e tenta")
        self.pausa()
        self.ate(1.0)

        # ── A1-2 · incompressível ──
        self.an("A1-2")
        vv = TC(r"\vv=\Big(0,\ 1-\dfrac{\X^2}{9}\Big)", 1120, 290, 44)
        self.gat("primeira a velocidade")
        self.play(FadeOut(en), caneta(vv, ritmo=0.35), run_time=1.2)
        self.remove(en)
        dv = TC(r"\dv\vv=\D0", 1120, 400, 42)
        self.gat("divergente zero")
        self.play(caneta(dv, ritmo=0.4))
        self.ate(1.0)

        # ── A1-3 · o rotacional; o galho ──
        self.an("A1-3")
        rt = TC(r"\rot\vv=\V{-\dfrac{2\X}{9}}", 1120, 500, 42)
        self.gat("o rotacional é a derivada")
        self.play(caneta(rt, ritmo=0.35))
        l1 = leg_mix(["MARGEM ESQUERDA: rot = 2/3 ", r"$\circlearrowleft$"], 1124, 720, VIO, "left", 26)
        self.gat("na margem esquerda ele vale")
        self.play(FadeIn(l1, shift=0.05 * UP), run_time=0.4)
        gl = leg_mix(["GALHO: 1/3 rad/s · UMA VOLTA A CADA ", r"$\approx$", " 19 s"], 1124, 868, GEO, "left", 24)
        self.gat("uma volta a cada dezenove")
        self.play(FadeIn(gl, shift=0.05 * UP), run_time=0.4)
        l2 = leg_mix(["MEIO: 0 · MARGEM DIREITA: −2/3 ", r"$\circlearrowright$"], 1124, 760, VIO, "left", 26)
        self.gat("na margem direita")
        self.play(FadeIn(l2, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── A1-4 · os três quadradinhos ──
        self.an("A1-4")
        self.gat("olha os três quadradinhos")
        st["q"] = True
        self.play(*[FadeIn(p) for p in peds], *[FadeIn(f) for f in fans], run_time=0.5)
        a0 = [p.area() for p in peds]
        self.play(*[anda(p, flRio, TR, 2.0, rate=linear, nome=f"A1 quadradinho {CS[i]}") for i, p in enumerate(peds)])
        for i, p in enumerate(peds):
            print(f"[A1] quadradinho {CS[i]}: área {a0[i]:.4f} → {p.area():.4f}")
        gs = []
        for c, ccw in ((CS[0], True), (CS[2], False)):
            Fc = ponto_fl(flRio, c, TR)
            gs.append(giro30(VA, Fc, .78, ccw))
            st["g"].append(clarPoly(circ_pts(.85, Fc, 12), .05))
        self.gat("cada um para um lado")
        self.play(*[Create(g) for g in gs], run_time=0.4)
        self.ate(1.0)

        # ── A1-5 · o atrito ──
        self.an("A1-5")
        dd = TC(r"d_1=\Lm0,\quad d_2=\Lm{-\dfrac{2\X}{9}}", 1120, 610, 40)
        self.gat("aqui a primeira deformação")
        self.play(caneta(dd, ritmo=0.35))
        at = legenda("ATRITO VISCOSO: MÁXIMO NAS MARGENS", 1124, 820, LIMA, "left", 26)
        self.gat("máxima nas margens")
        self.play(FadeIn(at, shift=0.05 * UP), run_time=0.4)
        rede.clear_updaters()
        self.sai_fim()
