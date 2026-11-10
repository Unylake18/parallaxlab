"""Lote PB4 · PARA O ESPAÇO (B4-1…B4-3): f(u, v) = (u, v, u² + v²). Cena 3D `folha_paraboloide` (fundo liso): a câmera começa de cima
(parece um painel 2D), a folha sobe em 3 s para z = u² + v² (tigela sólida; circunferências de raio 1 e 2 nas alturas 1 e 4; chão com sombra e o disco do domínio), depois a câmera
inclina até 35° e orbita 40° em 6 s. ALTURA 1 e ALTURA 4 presos nos pontos (1, 0, 1) e (2, 0, 4) pela mesma câmera do b3d.js."""
from kit import *  # noqa: F401,F403

XC, YC = -2.6, -0.4


class LoteB4(Base):
    def corpo(self):
        seg = {}

        def est(t):
            s = suave((t - seg["sobe"]) / 3.0) if "sobe" in seg else 0.0
            u = suave((t - seg["inc"]) / 6.0) if "inc" in seg else 0.0
            extra = 12.0 * min(1.0, max(0.0, t - seg["inc"] - 6.0) / 25.0) if "inc" in seg else 0.0
            return {"s": s, "cam": cam_obl(-90 + 40 * u + extra, 89.9 - 54.9 * u, (0, 0, 1.7 * u), K=1.15 - 0.3 * u, xc=XC, yc=YC)}

        # ── B4-1 · a folha vista de cima ──
        self.an("B4-1")
        self.secao("PARA O ESPAÇO")
        folha = Fundo3D(self, "folha_paraboloide", est, op=0.0)
        self.add(folha)
        self.papel(True, rt=0.5)
        self.play(folha.op.animate.set_value(1.0), run_time=0.8)
        form = F("f", "(", ("u", E1), ",", ("v", E2), ")", "=", ("(", SAI), ("u", E1), (",", SAI), (r"\ v", E2), (",", SAI), (r"\ u^2", E1), ("+", SAI),
                 ("v^2", E2), (")", SAI), size=M_L).move_to(P3(3.85, 2.2))
        self.gat("pega cada ponto do plano")
        self.play(caneta(form))

        # ── B4-2 · a folha sobe; alturas 1 e 4; a câmera inclina e orbita ──
        self.an("B4-2")
        self.gat("olha o que acontece com a folha")
        seg["sobe"] = self.t
        self.wait(3.0)
        seg["inc"] = self.t

        def rotulo(p_fn, s, folga=0.18):
            g = VGroup(ponto(ORIGIN, SAI_F, 0.08, z=8), placa(s, SAI_F, 20))          # v4: ponto com anel e rótulo em placa escura

            def upd(m):
                p = projeta3d(folha.e["cam"], p_fn(folha.e["s"]))
                m[0].move_to(p)
                m[1].next_to(p, RIGHT, buff=folga)
            g.add_updater(upd)
            upd(g)
            return g
        a1 = rotulo(lambda s: (1, 0, s), "ALTURA 1")
        a4 = rotulo(lambda s: (2, 0, 4 * s), "ALTURA 4", folga=0.43)          # v3 §2.5: +0,25 u para fora da borda
        self.gat("sobe para a altura um")
        self.play(FadeIn(a1), run_time=0.5)
        self.gat("a de raio dois sobe")
        self.play(FadeIn(a4), run_time=0.5)

        # ── B4-3 · é o gráfico de z = x² + y² ──
        self.an("B4-3")
        g = F(("z", SAI), "=", ("x^2", SAI), "+", ("y^2", SAI), size=M_L).move_to(P3(3.85, 0.6))
        self.gat("essa tigela é exatamente o gráfico")
        self.play(caneta(g))
        self.gat("fabricar uma superfície")
        self.play(pulso(g, 1.05), run_time=1.0)
        self._fecha()
        self.play(FadeOut(VGroup(a1, a4)), FadeOut(form), FadeOut(g), folha.op.animate.set_value(0.0), run_time=0.4)
        for m in (a1, a4, folha):
            m.clear_updaters()
        self.remove(a1, a4, folha, form, g)
        self.papel(False, rt=0.4)
        self.sai_fim()
