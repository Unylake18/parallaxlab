"""yt_0037 · B1 · coordenadas polares — v2 (G1 tipografia, G4 escrita em ordem, E03–E05). B1-1 (layout A): o ponto (2, π/3), o segmento r, o arco θ,
o triângulo com x = r cos θ e y = r sen θ; coluna: x² + y² = r² (a soma dos catetos vira o r²), o exemplo com os voos glifo a glifo (os rótulos
r = 2 e θ = π/3 do desenho e as projeções 1 e √3 nos eixos), r ≥ 0, 0 ≤ θ ≤ 2π. B1-2 (alvo 02): o retângulo rθ se desenha no gatilho, a vertical vira
círculo, a horizontal vira raio, a grade deforma para o disco (um ValueTracker), r = 0 à esquerda do eixo θ, a borda cai na origem (rótulo fora do
disco com linha-guia) e as bordas θ = 0 e 2π no mesmo segmento. A miniatura do triângulo saiu (E04)."""
from v2kit import *

S3 = math.sqrt(3)
V1 = Vw(250, 985, 365)            # B1-1: palco do ponto
VR = Vw(250, 930, 290)            # B1-2: plano rθ (θ/π em unidades: 2π ocupa 2 u)
VX = Vw(1330, 580, 290)           # B1-2: plano xy
FR = mixh(BG_, GEO, .13)
CEL = (.5, .75, math.pi / 3, math.pi / 2)
X1 = 1100


def amostras_borda():
    ths = np.linspace(0, TAU_, 97)
    rs = np.linspace(0, 1, 13)
    return [(r, 0.0) for r in rs] + [(1.0, t) for t in ths] + [(r, TAU_) for r in rs[::-1]] + [(0.0, t) for t in ths[::-1]]


class Folha:
    """Peças do retângulo rθ guardadas como amostras (r, θ); `poe(s)` desenha a mistura linear entre o painel rθ (s = 0) e o disco xy (s = 1)."""

    def __init__(self):
        self.ps = []

    def P(self, r, t, s):
        a = np.array(VR.px(r, t / math.pi))
        b = np.array(VX.px(r * math.cos(t), r * math.sin(t)))
        return PX(*((1 - s) * a + s * b))

    def curva(self, amostras, cor, wpx, alpha=1.0, z=4):
        m = VMobject().set_stroke(cor, W(wpx), alpha).set_fill(opacity=0)
        m._am, m._fecha = amostras, False
        self.ps.append(sem_ctn(m).set_z_index(z))
        return m

    def chapa(self, amostras, fill, z=1):
        m = VMobject().set_fill(fill, 1).set_stroke(width=0)
        m._am, m._fecha = amostras, True
        self.ps.append(sem_ctn(m).set_z_index(z))
        return m

    def poe(self, s):
        for m in self.ps:
            pts = [self.P(r, t, s) for r, t in m._am]
            if m._fecha:
                pts.append(pts[0])
            m.set_points_as_corners(pts)
        return self


def folha_rtheta():
    f = Folha()
    ths = np.linspace(0, TAU_, 97)
    rs = np.linspace(0, 1, 13)
    g = {}
    g["fundo"] = f.chapa(amostras_borda(), FR, z=1)
    g["lr"] = [f.curva([(i / 4, t) for t in ths], RR, 2, .55, z=3) for i in range(1, 4)]
    g["lt"] = [f.curva([(r, TAU_ * k / 12) for r in rs], TH, 2, .45, z=3) for k in range(1, 12)]
    r1, r2, t1, t2 = CEL
    cel = [(r1, t) for t in np.linspace(t1, t2, 17)] + [(r2, t) for t in np.linspace(t2, t1, 17)]
    g["cel"] = f.chapa(cel, mixh(BG_, LI, .75), z=2)
    g["borda"] = f.curva(amostras_borda(), GEO, 3, 1.0, z=5)
    f.poe(0.0)
    g["todos"] = VGroup(*f.ps)
    return f, g


def _fonte_de(alvo, fonte):
    alvo._fonte = fonte
    return alvo


class PB1(B37):
    ANTES = "COORDENADAS POLARES"
    SUB = "O ENDEREÇO DE UM PONTO"
    CARTAO = True

    def corpo(self):
        v = V1
        t3 = math.pi / 3
        # ── B1-1 · o ponto em polares ──
        self.an("B1-1")
        g = papel_v(v, (-.15, 1.6, -.15, 2.05))
        self.grade = g
        sx, sy, lx, ly = eixos_xy(v, -.15, 1.6, -.15, 2.05, size=40)
        P = ponto_px(*v.px(1, S3), BR, 10)
        self.play(FadeIn(g), GrowFromPoint(sx, v.P(0, 0)), GrowFromPoint(sy, v.P(0, 0)), FadeIn(P, scale=0.5), run_time=0.5)
        self.pena(lx, ly, lag=0.05)
        hip = lin_px([v.px(0, 0), v.px(1, S3)], RR, 5, z=7)
        cx_ = lin_px([v.px(0, 0), v.px(1, 0)], E1, 6, z=6)
        cy_ = lin_px([v.px(1, 0), v.px(1, S3)], E2, 6, z=6)
        arc_ = arco(v, .32, 0, t3, TH, 4, z=7)
        ponta = seta_px(v.px(.32 * math.cos(t3 - .14), .32 * math.sin(t3 - .14)), v.px(.32 * math.cos(t3), .32 * math.sin(t3)), TH, 4, 14, z=7)
        mh = v.px(.5, S3 / 2)
        lr = L([("r", r"\R"), ("eq", r"=2")], mh[0] + 22, mh[1] + 14, 40)      # K4: dentro do triângulo, colado à hipotenusa
        plr = placa_min(lr, 8, 5)
        self.gat("que se chama erre")
        self.play(Create(hip), run_time=0.7)
        self.pena(parte(lr, sel(lr, "r"), "r"), extra=[FadeIn(plr)])
        self.gat("medido a partir do lado")
        self.play(Create(arc_), run_time=0.9)
        self.play(FadeIn(ponta), run_time=0.2)
        lt = L([("t", r"\T"), ("eq", r"=\pi/3")], v.px(.4, 0)[0] + 6, v.px(0, .17)[1], 40)
        plt = placa_min(lt, 8, 5)
        self.gat("que se chama téta")
        self.pena(parte(lt, sel(lt, "t"), "θ"), extra=[FadeIn(plt)])
        self.gat("erre é a hipotenusa")
        realca(self, hip, rt=0.6)
        self.gat("o cateto de baixo")
        self.play(Create(cx_), run_time=0.6)
        fx = TP(r"\X=\R\cos\T", v.px(.5, 0)[0], v.px(0, 0)[1] + 33, 40, "c")      # K4: a margem de baixo (≥ 40 px) com o palco maior
        self.pena(fx)
        self.gat("o cateto em pé")
        self.play(Create(cy_), run_time=0.6)
        fy = TP(r"\Y=\R\sen\T", v.px(1, 0)[0] + 24, v.px(0, S3 / 2)[1] + 70, 40, "l")
        self.pena(fy)
        # coluna
        self.gat("por pitágoras")
        A1 = col(L([("x2", r"\X^2"), ("p", "+"), ("y2", r"\Y^2")], X1, 300, 46))
        escreve_seq(self, A1, [(fx.f[0][0:1], sel(A1, "x2")[0:1], 1.6), (fy.f[0][0:1], sel(A1, "y2")[0:1])])      # o x contorna por fora o rótulo de y
        self.gat("é igual a erre ao quadrado")
        B1 = col(L([("x2", r"\X^2"), ("p", "+"), ("y2", r"\Y^2"), ("eq", "="), ("r2", r"\R^2")], X1, 300, 46))
        passo(self, A1, B1, [("x2", "x2"), ("p", "p"), ("y2", "y2"), (["x2", "p", "y2"], "r2")], rt=1.2, nota="x²+y² vira r²")
        self.gat("erre igual a dois")
        self.pena(parte(lr, sel(lr, "eq"), "= 2"))
        L2 = col(L([("a", r"(\R,\T)=("), ("dois", "2"), ("v", ","), ("pi3", r"\dfrac{\pi}{3}"), ("f", ")")], X1, 415, 46))
        self.pena(parte(L2, sel(L2, "a"), "(r, θ) = ("))
        voos(self, [(lr[0][sel(lr, "eq")[-1]:sel(lr, "eq")[-1] + 1].copy(), _fonte_de(parte(L2, sel(L2, "dois"), "2"), lr))], rt=0.8)
        origem(self, "r = 2", "rótulo r = 2 do segmento (voo)")
        self.gat("pi sobre três dão")
        self.pena(parte(lt, sel(lt, "eq"), "= π/3"))
        self.pena(parte(L2, sel(L2, "v"), ","))
        voos(self, [(lt[0][sel(lt, "eq")[1]:sel(lt, "eq")[-1] + 1].copy(), _fonte_de(parte(L2, sel(L2, "pi3"), "π/3"), lt))], rt=0.8)
        self.pena(parte(L2, sel(L2, "f"), ")"))
        origem(self, "θ = π/3", "rótulo θ = π/3 do arco (voo)")
        # projeções nos eixos e os resultados
        self.gat("dão xis igual")
        pj = lin_px([v.px(1, S3), v.px(0, S3)], E2, 2.5, dash=(8, 6), z=5)
        t1 = TC("1", *[a + b for a, b in zip(v.px(1, 0), (26, 32))], 40, "c")
        t3l = TC(r"\sqrt{3}", *[a + b for a, b in zip(v.px(0, S3), (-46, 0))], 40, "c")
        self.play(Create(pj), run_time=0.3)
        self.pena(t1, t3l, lag=0.1)
        L3 = col(L([("a", r"\X=2\cdot\dfrac{1}{2}="), ("um", "1")], X1, 530, 46))
        self.gat("que é um")
        escreve_seq(self, L3, [(t1, "um")], rt_voo=0.6)
        origem(self, "x = 1", "projeção no eixo x (voo)")
        self.gat("e ípsilon igual a dois")
        L4 = col(L([("a", r"\Y=2\cdot\dfrac{\sqrt{3}}{2}="), ("r3", r"\sqrt{3}")], X1, 650, 46))
        self.pena(parte(L4, sel(L4, "a"), "y = 2·√3/2 ="))
        self.gat("que é raiz de três")
        voos(self, [(t3l.copy(), _fonte_de(parte(L4, sel(L4, "r3"), "√3"), t3l))], rt=0.8)
        origem(self, "y = √3", "projeção no eixo y (voo)")
        self.gat("a gente usa erre")
        L5 = col(TC(r"\R\ge 0,\qquad 0\le\T\le 2\pi", X1, 768, 46, "l"))
        self.pena(L5)
        # ── B1-2 · a grade que vira círculos ──
        self.an("B1-2")
        sai = saindo(self.snap())
        self.subt("A GRADE DO PLANO rθ VIRA CÍRCULOS E RAIOS")
        gR = papel_v(VR, None)                              # K2: tela inteira até o 2º plano chegar; aí cada plano fica com a sua metade
        aR = seta_px(VR.px(-.05, 0), VR.px(1.32, 0), RR, 3, 16, z=6)
        aT = seta_px(VR.px(0, -.05), VR.px(0, 2.22), TH, 3, 16, z=6)
        f0, G0 = folha_rtheta()
        self.play(*[FadeOut(m) for m in sai + [self.grade]], FadeIn(gR), GrowFromPoint(aR, VR.P(0, 0)), GrowFromPoint(aT, VR.P(0, 0)),
                  FadeIn(G0["fundo"]), Create(G0["borda"]), run_time=0.8)
        self.remove(*sai, self.grade)
        self.grade = gR
        lR = TC(r"\R", *VR.px(1.4, 0), 40, "l")
        lT = TC(r"\T", *VR.px(0, 2.34), 40, "c")
        tks = [TC("1", *VR.px(1, -.12), 40, "c"), TC(r"2\pi", *VR.px(-.17, 2), 40, "c"), TC(r"\pi", *VR.px(-.13, 1), 40, "c"),
               TC("0", *VR.px(-.1, -.1), 40, "c")]
        mk = VGroup(lin_px([VR.px(1, -.025), VR.px(1, .025)], GEO, 2, z=6), *[lin_px([VR.px(-.025, b), VR.px(.025, b)], GEO, 2, z=6) for b in (1, 2)])
        pR = leg("PLANO rθ", 395, 1022, GEO, "center", 30)
        self.gat("de um lado o plano")
        self.play(*[Create(m) for m in G0["lr"] + G0["lt"]], Create(mk), run_time=0.8)
        self.pena(lR, lT, *tks, pR, lag=0.05)
        self.gat("do outro o plano")
        gX = papel_meia(VX, 810, 1920)
        ex = eixos_xy(VX, -1.2, 1.3, -1.2, 1.25, size=40)
        pX = leg("PLANO xy", 1330, 985, GEO, "center", 30)
        gRh = papel_meia(VR, 0, 810)
        self.play(FadeOut(gR), FadeIn(gRh), FadeIn(gX), GrowFromPoint(ex[0], VX.P(0, 0)), GrowFromPoint(ex[1], VX.P(0, 0)), run_time=0.6)
        self.remove(gR)
        self.grade = VGroup(gRh, gX)
        self.pena(ex[2], ex[3], pX, lag=0.05)
        self.gat("a transformação fi leva")
        sf = seta_px((700, 300), (920, 300), GEO, 4, 20, z=6)
        fi = TC(r"\varphi(\R,\T)=(\R\cos\T,\ \R\sen\T)", 800, 250, 40, "c")      # acima da faixa que a grade varre ao deformar
        self.play(GrowFromPoint(sf, PX(700, 300)), run_time=0.4)
        self.pena(fi)
        # a vertical vira círculo, a horizontal vira raio
        self.gat("uma reta vertical")
        vr = lin_px([VR.px(.5, 0), VR.px(.5, 2)], RR, 5, z=7)
        self.play(Create(vr), run_time=0.6)
        self.gat("vira um círculo")
        cr = circulo(VX, .5, RR, 5, z=7)
        risca_voando(self, [(vr, cr)], rt=0.6)
        l1 = leg("r CONSTANTE → CÍRCULO", 1490, 990, RR, "left", 30)
        self.pena(l1, passo=0.03)
        self.gat("uma reta horizontal")
        hr = lin_px([VR.px(0, 1 / 3), VR.px(1, 1 / 3)], TH, 5, z=7)
        self.play(Create(hr), run_time=0.4)
        self.gat("vira um raio")
        rr = lin_px([VX.px(0, 0), VX.px(math.cos(math.pi / 3), math.sin(math.pi / 3))], TH, 5, z=7)
        risca_voando(self, [(hr, rr)], rt=0.9)
        l2 = leg("θ CONSTANTE → RAIO", 1490, 1032, TH, "left", 30)
        self.pena(l2, passo=0.03)
        # o retângulo inteiro deforma para o disco (um ValueTracker)
        self.gat("e o retângulo de erre")
        self.play(FadeIn(G0["cel"]), FadeOut(vr), FadeOut(hr), run_time=1.0)
        self.remove(vr, hr)
        self.gat("vira o disco inteiro")
        f1, G1 = folha_rtheta()
        for x in G1["todos"].get_family():
            x._voando = True
        s = ValueTracker(0.0)
        self.add(s, G1["todos"])
        G1["todos"].add_updater(lambda m: f1.poe(s.get_value()))
        self.play(s.animate(rate_func=smooth).set_value(1.0), FadeOut(cr), FadeOut(rr), run_time=2.4)
        G1["todos"].clear_updaters()
        f1.poe(1.0)
        for x in G1["todos"].get_family():
            x._voando = False
        self.remove(s, cr, rr)
        # as bordas
        self.gat("o lado erre igual a zero")
        b0 = lin_px([VR.px(0, 0), VR.px(0, 2)], CORAL, 7, z=8)
        lb0 = leg("r = 0", 222, 506, CORAL, "right", 30)
        self.play(Create(b0), run_time=0.6)
        self.pena(lb0)
        self.gat("cai todo num ponto")
        o = ponto_px(*VX.px(0, 0), CORAL, 10, z=9)
        self.play(TransformFromCopy(b0, o, path_arc=-0.4), run_time=1.2)
        lo = leg("r = 0 → ORIGEM", 1000, 905, CORAL, "left", 30)
        gu = guia_px((1130, 878), [a + b for a, b in zip(VX.px(0, 0), (-10, 12))], CORAL, lo, 2.5, 14)
        self.pena(lo, extra=[Create(gu)])
        self.gat("e os lados téta igual")
        bb = VGroup(lin_px([VR.px(0, 0), VR.px(1, 0)], TH, 7, z=8), lin_px([VR.px(0, 2), VR.px(1, 2)], TH, 7, z=8))
        self.play(Create(bb), run_time=0.7)
        self.gat("no mesmo segmento")
        sg = lin_px([VX.px(0, 0), VX.px(1, 0)], TH, 7, z=8)
        self.play(*[TransformFromCopy(a_, b_, path_arc=0.5) for a_, b_ in ((bb[0], sg), (bb[1], sg.copy()))], run_time=1.2)   # sobem, longe do rótulo r
        self.marca("02")
        self.sai_fim()
