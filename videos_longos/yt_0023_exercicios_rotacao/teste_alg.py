"""Teste mínimo das ferramentas de álgebra v2 (linha, gm com voos/riscos, lei, pilha.so/limpa): imprime o que sobra em cena."""
from pecas23 import *  # noqa: F401,F403


def textos(cena):
    out = []
    for m in cena.mobjects:
        tx = [x for x in m.get_family() if isinstance(x, MathTex)]
        vis = [g for g in m.family_members_with_points() if isinstance(g, VMobject) and max(g.get_fill_opacity(), g.get_stroke_opacity()) > 0.05]
        if vis:
            out.append((type(m).__name__, tx[0].get_tex_string()[:25] if tx else "", len(vis), [round(float(c), 1) for c in m.get_center()[:2]]))
    return out


class TesteAlg(Lote23):
    def corpo(self):
        self.an("E1-3")
        mae, imae, maeb = self.linha(("I", "=", r"\sum", "I_i"), rt=0.8)
        rot = lbl("M=15", MAS, 40).move_to(P3(-4, 0))
        self.add(rot)
        A, ia, _ = self.linha(("a", "=", "b", "+", "c"), voos={0: rot}, rt=0.8)
        B, ib, _ = self.gm(A, ia, ("a", "-", "c", "=", "b"), rt=0.8)
        C, ic, cb = self.gm(B, ib, ("x", "=", "b"), riscar=[0], sai=[1, 2], voos={0: rot}, caixa_cor=MAS, rt=0.8)
        print("[teste] apos gm:", textos(self))
        self.pilha.so(maeb, cb)
        print("[teste] apos so:", textos(self))
        L0, il0, _ = self.lei("newton_rot", (r"\sum", r"\tau", "=", "I", r"\alpha"), rt=0.8)
        e2, ie2, g2 = self.gm(L0, il0, ("T", "r", "=", "I", r"\alpha"), sai=[0, 1], voos={0: rot}, tag="VOLANTE", rt=1.0)
        print("[teste] apos lei+gm:", textos(self))
        self.pilha.so(maeb, cb)
        self.play(Indicate(mae, color=MAS, scale_factor=1.05), run_time=0.6)
        S1, is1, _ = self.gm(mae, imae, ("I", "=", "I_{a}", "+", "I_{b}"), mapas=[([2, 3], [2, 4])], rt=0.8)
        S2, is2, s2b = self.gm(S1, is1, ("I", "=", "2"), caixa_cor=MAS, rt=0.8)
        print("[teste] apos gm mae:", textos(self))
        self.pilha.so(s2b, rt=0.4)
        print("[teste] apos so s2b:", textos(self))
        self.pilha.limpa()
        self.card_sai()
        print("[teste] apos limpa:", textos(self))
        self.ate(0.99)
