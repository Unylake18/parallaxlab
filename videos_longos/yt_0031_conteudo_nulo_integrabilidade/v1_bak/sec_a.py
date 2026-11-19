"""yt_0031 · A · bem-vindos (alvo 03). Padrão do canal (copiado do A1 do yt_0028): a logo clássica com os anéis e BEM-VINDOS; depois o cartão
`INTEGRAIS DUPLAS · VÍDEO 2`, o título e as três etiquetas, que acendem uma por vez com a voz. Sem canto (a linha 1 entra no começo do B1)."""
from v31 import *


class PA(B31):
    CANTO = False

    def corpo(self):
        self.an("A1")
        CL = P3(0, 0.6)
        logo = self.logo(5.6).move_to(CL)
        aneis = VGroup(*[DashedVMobject(Circle(radius=r).move_to(CL), num_dashes=48).set_stroke(GEO, 2.2, opacity=o) for r, o in ((2.1, 0.45), (2.45, 0.25))])
        sem_ctn(aneis)
        bv = T("BEM-VINDOS AO PARALLAX LAB", 960, 880, 46, "center")
        gira = lambda rt: (Rotate(aneis[0], 0.12 * rt, about_point=aneis[0].get_center(), rate_func=linear),
                           Rotate(aneis[1], -0.1 * rt, about_point=aneis[1].get_center(), rate_func=linear))
        self.gat("fala pessoal")
        self.play(FadeIn(logo, scale=0.94), FadeIn(aneis), FadeOut(self.wm), run_time=0.8)
        self.remove(self.wm)
        self.pena(bv, extra=gira(1.4), rt=1.4)
        rt = self.falta("este é o segundo vídeo")
        if rt >= 0.2:
            self.play(*gira(rt), run_time=rt)
        self.gat("este é o segundo vídeo")
        sup = leg("INTEGRAIS DUPLAS · VÍDEO 2", 960, 400, CI, "center", 30)
        tit = T("CONTEÚDO NULO E INTEGRABILIDADE", 960, 500, 70, "center")
        self.play(FadeOut(Group(logo, aneis), scale=0.9), FadeOut(bv), run_time=0.5)
        self.remove(logo, aneis, bv)
        self.play(FadeIn(self.wm), run_time=0.3)
        self.pena(sup)
        self.gat("no vídeo passado")
        self.pena(tit)
        nv = leg("NESTE VÍDEO", 960, 615, GEO, "center", 24)
        it = ["1 · TAMPAS", "2 · CONTEÚDO NULO", "3 · TEOREMA"]
        ws = [txt(s, ts(34), bold=True, up=False).width * 120 + 56 for s in it]
        tot = sum(ws) + 2 * 28
        X = 960 - tot / 2
        caixas, textos = [], []
        for i, s in enumerate(it):
            caixas.append(caixa_px(X, 650, ws[i], 70, GEO, 2, 0.45, 12))
            textos.append(T(s, X + ws[i] / 2, 698, 34, "center", CI if i == 2 else BR))
            X += ws[i] + 28
        self.gat("hoje a pergunta")
        self.pena(nv, extra=[Create(c) for c in caixas], rt=1.0)
        for fr, t in zip(("medir a diferença", "entender o que é conteúdo", "e juntar tudo"), textos):
            self.gat(fr)
            self.pena(t)
        self.marca("03")
        self.sai_fim()
