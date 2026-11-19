"""yt_0039 · teste localizado (não entra no vídeo): a sequência do ȳ do E4-3 (cad, cad, cancela, cad desce), com o estado da cena a cada passo."""
from k39 import *


def visivel(sc, m):
    ids = {id(x) for t in sc.mobjects for x in t.get_family()}
    g = [x for x in m[0]]
    return sum(1 for x in g if id(x) in ids), len(g)


class PT(B39x):
    ANTES = "TESTE"

    def corpo(self):
        self.an("E4-3")
        self.colX, self.colY = 1130, 300
        Y1 = linha(self, [("y", r"\yb"), ("e", "="), ("f", r"\dfrac{\Mx}{\mm}")], 32)
        Y1 = cad(self, Y1, [("e", "="), ("f", r"\dfrac{\kk\pi/64}{\kk/6}")], [], n=19)
        print("[teste] 1", visivel(self, Y1))
        Y1 = cad(self, Y1, [("e", "="), ("a", r"\dfrac{\kk\pi}{64}"), ("c", r"\cdot"), ("b", r"\dfrac{6}{\kk}")], [("^f", "a"), ("^f", "b")], n=19)
        print("[teste] 2", visivel(self, Y1))
        na, ba, da = frac_ix(Y1, "a")
        nb, bb_, db = frac_ix(Y1, "b")
        cancela(self, G(Y1, na[:1]), G(Y1, db))
        print("[teste] 3", visivel(self, Y1), [type(m).__name__ for m in self.mobjects][-6:])
        import traceback
        alvo = {id(x) for x in Y1[0]}
        orig_rm = Scene.remove

        def rm(sc_, *ms):
            for m in ms:
                f = {id(x) for x in m.get_family()}
                if f & alvo:
                    print("[teste] remove", type(m).__name__, len(f & alvo), "".join(traceback.format_stack(limit=6)[:-1]).replace("\n", " | ")[-900:])
            return orig_rm(sc_, *ms)
        Scene.remove = rm
        Y2 = cad(self, Y1, [("e", "="), ("r", r"\dfrac{6\pi}{64}")], [(na[1:], "r"), (da, "r"), (nb, "r")], n=19, desce=True)
        Scene.remove = orig_rm
        print("[teste] 4", visivel(self, Y1), visivel(self, Y2))
        self.wait(1)
