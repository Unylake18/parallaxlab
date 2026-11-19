"""yt_0031 · S · síntese e próximo vídeo (alvos 30 e 31) + CTA padrão do canal (copiado do logo_cta do v28.py do yt_0028)."""
from v31 import *


def curva_pts(v, dy=0.0, n=120):
    return [v.px(a, float(g_solda(a)) + dy) for a in np.linspace(0, 2, n + 1)]


class PS(B31):
    ANTES = "SÍNTESE"          # v2 (G2): a linha 2 do canto já está na tela no 1º quadro do bloco

    def logo_cta(self, rt_fim=3.0):
        CL = P3(0, 0.9)
        logo = self.logo(5.6).move_to(CL)
        aneis = VGroup(*[DashedVMobject(Circle(radius=r).move_to(CL), num_dashes=48).set_stroke(GEO, 2.6, opacity=o) for r, o in ((2.1, 0.85), (2.45, 0.6))])
        sem_ctn(aneis)
        ins = VGroup(T("INSCREVA-SE PARA ACOMPANHAR", 960, 0, 66, "center", caneta=False), T("OS PRÓXIMOS VÍDEOS", 960, 0, 66, "center", caneta=False)).arrange(DOWN, buff=0.12).move_to(P3(0, -2.6))
        s4 = self.snap()
        self.play(*[FadeOut(m_) for m_ in s4], FadeOut(self.wm), FadeIn(logo, scale=0.96), FadeIn(aneis), FadeIn(ins, shift=0.1 * UP), run_time=0.6)
        self.remove(*s4, self.wm)
        rt = self.resta() + rt_fim
        self.play(Rotate(aneis[0], 0.3 * rt, rate_func=linear), Rotate(aneis[1], -0.24 * rt, rate_func=linear), run_time=rt)

    def corpo(self):
        # ── S1 · síntese (alvo 30) ──────────────────────────────────────────────────────────────────
        self.an("S1")
        pal = Palco3D("b21", self, CAM_BAIXO, n=16, s=1.0, cresce=1.0, muro=1.0)
        pal.fundo.scale(0.9, about_point=PX(0, 0)).shift(PX(-80, 40) - PX(0, 0))
        pal.fundo.op.set_value(0.0)
        self.add(pal.fundo)
        self.play(pal.fundo.op.animate.set_value(1.0), run_time=0.8)
        itens = [("TAMPAS", "S(P) − s(P) TENDE A ZERO", CORAL, "a soma por baixo e"),
                 ("CONTINUIDADE UNIFORME", "ONDE f É CONTÍNUA", CI, "onde a função é contínua"),
                 ("CONTEÚDO NULO", "ONDE f SALTA", MEN, "onde ela é descontínua")]
        pos = {"TAMPAS": 260, "CONTEÚDO NULO": 410, "CONTINUIDADE UNIFORME": 560}
        caixas = {}
        acendeu = False
        for t, s_, c, fr in itens:
            self.gat(fr)
            Y = pos[t]
            bx = caixa_px(1120, Y - 50, 700, 110, GEO, 2, .45, 12)
            tt = T(t, 1150, Y, 34, cor=c)
            ss = leg(s_, 1150, Y + 42, GEO, "left", 24)
            caixas[t] = (bx, tt, ss)
            self.play(Create(bx), run_time=0.4)
            if t == "TAMPAS":
                self.pena(tt, ss, lag=0.5)
                self.gat("é o volume das tampas")
                pal.acende3d(1.4)                           # v2: o muro acende
                continue
            if t == "CONTEÚDO NULO":
                self.pena(ss)
                self.gat("as tampas podem ser")
                pal.acende3d(1.4)                           # v2: o muro acende de novo
                self.gat("num conjunto de conteúdo")
                self.pena(tt)
                self.gat("gastando tão pouca")
                self.sublinha(tt, 1.2)
            else:
                self.pena(tt, ss, lag=0.5)
        self.gat("juntando as duas ideias")
        dn = TC(r"\Downarrow", 1470, 720, 44, "c")
        ot = T("O TEOREMA", 1470, 800, 44, "center")
        self.pena(dn)
        self.pena(ot)
        self.gat("o importante é controlar")
        self.sublinha(caixas["TAMPAS"][2], 1.4)
        self.marca("30")

        # ── S2 · o próximo vídeo e CTA (alvo 31) ────────────────────────────────────────────────────
        self.an("S2")
        sai = [m for m in self.snap() if m is not pal.fundo]
        anims = [FadeOut(m) for m in sai] + [pal.fundo.op.animate.set_value(0.0), FadeOut(self.h1)]
        if self.h2 is not None:
            anims.append(FadeOut(self.h2))
        v = Vw(330, 870, 230)
        leve = poly_px([v.px(0, 0), v.px(2, 0)] + curva_pts(v)[::-1], LEVE, z=1)
        pes = poly_px([v.px(0, 2), v.px(2, 2)] + curva_pts(v)[::-1], PESADO, z=1)
        sold = solda_px(v, BR, 4)
        self.play(*anims, FadeIn(leve), FadeIn(pes), Create(sold), run_time=0.8)        # v2 (G2): a chapa entra na troca
        pal.fundo.clear_updaters()
        self.remove(*sai, pal.fundo, self.h1, *([self.h2] if self.h2 else []))
        self.h2 = None
        fm = TC(r"\textstyle\iint_R\rr\,dA\ \overset{?}{=}\ \iint_{\text{leve}}\rr\,dA+\iint_{\text{pesado}}\rr\,dA", 1000, 520, 40)
        self.gat("então a massa total")
        self.pena(fm)
        self.gat("só que os dois pedaços")
        self.acende([sold], cor=CORAL, rt=1.0)
        self.gat("ela entra duas vezes")
        self.sublinha(fm, 1.2)
        self.gat("e no nosso modelo")
        sp = T("A SOLDA PESA ALGUMA COISA?", 1000, 700, 44, cor=MEN)
        self.pena(sp)
        self.gat("no próximo vídeo as")
        np1 = leg("NO PRÓXIMO VÍDEO", 960, 200, GEO, "center", 34)
        np2 = T("PROPRIEDADES DA INTEGRAL DUPLA", 960, 290, 66, "center")
        self.pena(np1)
        self.pena(np2)
        self.gat("dividir a região em")
        self.play(leve.animate.shift(DOWN * 37 / 120), pes.animate.shift(UP * 37 / 120), run_time=1.2)   # v2: os pedaços se separam aqui
        self.gat("mudar a função num")
        self.acende([sold], cor=MEN, rt=1.2)
        self.marca("31", agora=True)
        self.gat("se essa aula te ajudou")
        self.logo_cta(rt_fim=0.0)
