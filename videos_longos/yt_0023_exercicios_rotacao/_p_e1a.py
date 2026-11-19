"""v3: planos de câmera do volante (PE1a): mistura wov entre a trilha u (3/4 → frontal) e um plano manual; CORTE; tour de closes; explodido com pílulas."""
import io


def rw(P, fn):
    s = open(P, encoding='utf-8').read()          # newline=None: CRLF vira \n; a escrita devolve o padrão do sistema
    s2 = fn(s)
    open(P, 'w', encoding='utf-8').write(s2)


def rep(s, a, b):
    assert s.count(a) == 1, (s.count(a), a[:90])
    return s.replace(a, b)


def pec(s):
    s = rep(s, '''th2=ValueTracker(0.0), x1=ValueTracker(0.0), alvo_x=ValueTracker(0.0), alvo_z=ValueTracker(0.0))''',
            '''th2=ValueTracker(0.0), x1=ValueTracker(0.0), alvo_x=ValueTracker(0.0), alvo_z=ValueTracker(0.0),
                  wov=ValueTracker(0.0), maz=ValueTracker(-60.0), mel=ValueTracker(15.0), mK=ValueTracker(K0), mxc=ValueTracker(-3.85), myc=ValueTracker(yc0),
                  max=ValueTracker(0.0), maz_=ValueTracker(0.0), corte=ValueTracker(0.0))''')
    s = rep(s, '''        def cam():
            return cam_vol(tr["u"].get_value(), K=tr["K"].get_value(), yc=tr["yc"].get_value(),
                           alvo_x=tr["alvo_x"].get_value(), alvo_z=tr["alvo_z"].get_value())
''', '''        def cam():
            b = cam_vol(tr["u"].get_value(), K=tr["K"].get_value(), yc=tr["yc"].get_value(),
                        alvo_x=tr["alvo_x"].get_value(), alvo_z=tr["alvo_z"].get_value())
            w = tr["wov"].get_value()
            if w <= 1e-6:
                return b
            m = dict(b)
            for k, ch in (("az", "maz"), ("el", "mel"), ("K", "mK"), ("xc", "mxc"), ("yc", "myc")):
                m[k] = round(b[k] + w * (tr[ch].get_value() - b[k]), 4)
            m["alvo"] = [round(b["alvo"][0] + w * (tr["max"].get_value() - b["alvo"][0]), 4), 0.0,
                         round(b["alvo"][2] + w * (tr["maz_"].get_value() - b["alvo"][2]), 4)]
            return m
''')
    s = rep(s, '''"th2": tr["th2"].get_value(), "x1": tr["x1"].get_value(),
                 "zb": ZB,''', '''"th2": tr["th2"].get_value(), "x1": tr["x1"].get_value(), "corte": round(tr["corte"].get_value(), 3),
                 "zb": ZB,''')
    s = rep(s, '''    def vp(self, p):
        """Ponto 3D do volante → tela (câmera corrente)."""''', '''    def plano_v(self, nome, az, el, K, xc, yc, ax=0.0, az_=0.0, rt=1.3, extra=()):
        """Plano de câmera nomeado (v3 §2.1): movimento contínuo (ease in-out) e linha [cam] no log."""
        tr = self.vt
        print(f"[cam] {nome} az={az} el={el} K={K}", flush=True)
        self.play(tr["wov"].animate.set_value(1.0), tr["maz"].animate.set_value(az), tr["mel"].animate.set_value(el), tr["mK"].animate.set_value(K),
                  tr["mxc"].animate.set_value(xc), tr["myc"].animate.set_value(yc), tr["max"].animate.set_value(ax), tr["maz_"].animate.set_value(az_),
                  *extra, run_time=rt, rate_func=smooth)

    def geral_v(self, rt=1.3, extra=()):
        self.vt["wov"].set_value(self.vt["wov"].get_value())
        print("[cam] volta GERAL/frontal", flush=True)
        self.play(self.vt["wov"].animate.set_value(0.0), *extra, run_time=rt, rate_func=smooth)

    def vp(self, p):
        """Ponto 3D do volante → tela (câmera corrente)."""''')
    return s


def e1a(s):
    # E1-1: tour de closes, cada peça acesa em rosa
    s = rep(s, '''        for fr, nome, *vals, alvo in dados:
            self.gat(fr)
            pcs =''', '''        planos = {"ANEL": (-40.0, 10.0, 5.8, -3.85, 0.95, 0.0, 0.0), "CUBO": (-50.0, 8.0, 11.0, -3.85, 0.95, 0.0, 0.0),
                  "DISCOS": (-35.0, 8.0, 6.8, -3.85, 0.95, 0.0, 0.0), "TAMBOR": (-55.0, 10.0, 9.0, -3.85, 0.95, 0.0, -0.05), "BLOCO": (-60.0, 12.0, 5.2, -3.85, 0.95, 0.0, -0.45)}
        for fr, nome, *vals, alvo in dados:
            self.gat(fr)
            self.v_flags["foco"] = nome.lower() if nome != "BLOCO" else ""
            pl = planos[nome]
            self.plano_v(f"E1-1 CLOSE {nome}", pl[0], pl[1], pl[2], pl[3], pl[4], pl[5], pl[6], rt=1.2)
            pcs =''')
    s = rep(s, '''            ch = VGroup(Dot(p, radius=0.05, color=GEO), Line(p, linha_.get_left() + 0.12 * LEFT).set_stroke(GEO, 1.6)).set_z_index(9)''',
            '''            ch = VGroup(Dot(p, radius=0.06, color=GEO_CL), linha_halo(p, linha_.get_left() + 0.12 * LEFT, cor=GEO_CL, w=2.0)).set_z_index(9)''')
    s = rep(s, '''        self.gat("o bloco é solto do repouso")
        tr = self.trilha''', '''        self.gat("o bloco é solto do repouso")
        self.v_flags["foco"] = ""
        self.geral_v(rt=1.2)
        tr = self.trilha''')
    # E1-3: CORTE ao meio
    s = rep(s, '''        self.v_flags["foco"] = "anel"
        self.play(vt["ex"].animate.set_value(1.0), vt["th"].animate.set_value(0.25), run_time=1.0)
        self.gat("um disco cheio de quarenta centímetros")''', '''        self.v_flags["foco"] = "anel"
        self.v_flags["cord"] = False
        self.plano_v("E1-3 CORTE", -18.0, 8.0, 5.4, -3.85, 0.95, rt=1.4, extra=(vt["th"].animate.set_value(0.0), vt["corte"].animate.set_value(1.0)))
        self.gat("um disco cheio de quarenta centímetros")''')
    s = rep(s, '''        th_ = vt["th"].get_value()
        rot_ = lambda x, y, z: self.vp((x * math.cos(th_) + z * math.sin(th_), y, -x * math.sin(th_) + z * math.cos(th_)))
        r_lbl = VGroup(chamada(rot_(0.0, -0.04, 0.30), lbl(r"R_1=0{,}30\\ \\mathrm{m}", GEO, 40), LEFT + 0.05 * DOWN, 2.6),
                       chamada(rot_(0.0, -0.04, 0.40), lbl(r"R_2=0{,}40\\ \\mathrm{m}", GEO, 40), RIGHT + 0.05 * DOWN, 2.3),
                       chamada(rot_(-0.35, 0.05, 0.0), lbl(r"M=15\\ \\mathrm{kg}", MAS, 42), DOWN + 0.3 * LEFT, 2.2))''', '''        rot_ = lambda x, y, z: self.vp((x, y, z))                  # th = 0 no corte: a face cortada fica no plano x = 0
        o_c = rot_(0.0, 0.0, 0.0)
        r_lbl = VGroup(cota23(o_c, rot_(0.0, 0.0, -0.30), lbl(r"R_1=0{,}30\\ \\mathrm{m}", GEO, 40), lado=LEFT, d=2.4),
                       cota23(o_c, rot_(0.0, 0.0, 0.40), lbl(r"R_2=0{,}40\\ \\mathrm{m}", GEO, 40), lado=RIGHT, d=2.4),
                       chamada(rot_(0.0, 0.0, -0.35), lbl(r"M=15\\ \\mathrm{kg}", MAS, 42), DOWN + 0.4 * LEFT, 2.0, cor=MAS))''')
    s = rep(s, "voos={2: r_lbl[2][2]}, size=46, rt=1.2)", "voos={2: r_lbl[2][2]}, size=46, rt=1.2)")
    # E1-4: cubo e discos em closes
    s = rep(s, '''        self.v_flags["foco"] = "cubo"
        self.play(vt["th"].animate.set_value(0.0), run_time=0.6)''', '''        self.v_flags["foco"] = "cubo"
        self.v_flags["cord"] = True
        self.plano_v("E1-4 CLOSE cubo", -50.0, 8.0, 11.0, -3.85, 0.95, rt=1.2, extra=(vt["corte"].animate.set_value(0.0), vt["th"].animate.set_value(0.0)))''')
    s = rep(s, '''        self.v_flags["foco"] = "discos"
        pc = self.vp((0.25, -0.03, 0.0))''', '''        self.v_flags["foco"] = "discos"
        self.plano_v("E1-4 CLOSE disco", -35.0, 8.0, 6.8, -3.85, 0.95, 0.0, 0.0, rt=1.2)
        pc = self.vp((0.25, -0.03, 0.0))''')
    s = rep(s, '''        cota = VGroup(Line(o_, pc).set_stroke(GEO, 3), chamada(pc + 0.0 * UP, lbl(r"D=0{,}25\\ \\mathrm{m}", GEO, 40), UP + 0.35 * RIGHT, 2.0)).set_z_index(14)''',
            '''        cota = cota23(o_, pc, lbl(r"D=0{,}25\\ \\mathrm{m}", GEO, 40), lado=UP, d=1.1)''')
    s = rep(s, "self.play(Create(cota[0]), FadeIn(cota[1]), FadeIn(dk_), run_time=0.7)", "self.play(FadeIn(cota), FadeIn(dk_), run_time=0.7)")
    s = rep(s, "10: cota[1][2]}", "10: cota[2]}")
    # E1-5: explodido com as pílulas de I
    s = rep(s, '''        self.pilha.so(maeb, fb, gb, kb, anims=[FadeOut(cota), FadeOut(dk_), vt["ex"].animate.set_value(0.0)])
        self.play(Indicate(mae, color=MAS, scale_factor=1.05), run_time=0.6)''', '''        self.v_flags["foco"] = ""
        self.pilha.so(maeb, fb, gb, kb, anims=[FadeOut(cota), FadeOut(dk_)])
        self.plano_v("E1-5 EXPLODIDO", -32.0, 12.0, 4.2, -3.5, 0.9, 0.0, 0.0, rt=1.3, extra=(vt["ex"].animate.set_value(1.0),))
        ce = self.vcam()
        pi_an = chamada(self.vp((0.0, 0.10 * 1.0 - 0.034, 0.40)), lbl(r"1{,}875", MAS, 40), UP + 0.2 * RIGHT, 1.1, cor=MAS)
        pi_cu = chamada(self.vp((0.0, -0.16, 0.08)), lbl(r"0{,}015", MAS, 40), LEFT + 0.6 * DOWN, 2.2, cor=MAS)
        pi_di = chamada(self.vp((0.25, -0.30 - 0.005, 0.0)), lbl(r"0{,}1275", MAS, 40), RIGHT + 0.5 * DOWN, 2.0, cor=MAS)
        self.play(FadeIn(pi_an), FadeIn(pi_cu), FadeIn(pi_di), Indicate(mae, color=MAS, scale_factor=1.05), run_time=0.8)''')
    s = rep(s, "voos={2: mp(F_, if_, [2]), 4: mp(G_, ig, [2]), 6: mp(K_, ik, [3])}", "voos={2: pi_an[2], 4: pi_cu[2], 6: pi_di[2]}")
    s = rep(s, '''        self.pilha.so(sb, rt=0.4)
        x0, w = 1.0, 5.4''', '''        self.pilha.so(sb, rt=0.4)
        self.v_flags["foco"] = ""
        self.geral_v(rt=1.3, extra=(vt["ex"].animate.set_value(0.0), FadeOut(pi_an), FadeOut(pi_cu), FadeOut(pi_di)))
        x0, w = 1.0, 5.4''')
    return s


rw('pecas23.py', pec)
rw('sec_e1a.py', e1a)
print('ok')
