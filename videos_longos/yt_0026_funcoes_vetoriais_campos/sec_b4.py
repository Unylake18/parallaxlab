"""Lote PB4 · PARA O ESPAÇO (B4-1…B4-3), layout A (quadro 13): a folha plana (u, v) sobe e vira a tigela z = u² + v² (3D `c7_paraboloide`, câmera fixa, sem sombra); as famílias âmbar/magenta,
as circunferências de raio 1 e 2 chegam às alturas 1 e 4 (ALTURA 1, ALTURA 4 presos ao 3D); fórmulas na coluna da direita."""
from v7 import *  # noqa: F401,F403

BOX = [150, 200, 900, 820]


class LoteB4(Base):
    def corpo(self):
        seg = {}

        def est(t):
            s = suave((t - seg["sobe"]) / 3.0) if "sobe" in seg else 0.0
            return {"s": s, "box": BOX}

        # ── B4-1 ──
        self.an("B4-1")
        self.secao("PARA O ESPAÇO")
        folha = Fundo3D(self, "c7_paraboloide", est, op=0.0)
        self.add(folha)
        self.play(folha.op.animate.set_value(1.0), run_time=0.8)
        form = TC(r"f(\U,\V) = \S{(}\U,\; \V,\; \U^2+\V^2\S{)}", 1120, 460, 54)
        self.gat("pega cada ponto do plano")
        self.play(caneta(form))

        # ── B4-2 · a folha sobe; as alturas 1 e 4 ──
        self.an("B4-2")
        self.gat("olha o que acontece com a folha")
        seg["sobe"] = self.t
        self.wait(3.0)
        K = 0.55
        pos = lambda r, t: (r * math.cos(t), r * math.sin(t), K * r * r)
        a1 = rotulo3d("ALTURA 1", proj_c7("paraboloide", BOX, pos(1, -0.55)), 26, 14)
        a4 = rotulo3d("ALTURA 4", proj_c7("paraboloide", BOX, pos(2, -0.28)), 26, -14)
        self.gat("sobe para a altura um")
        self.play(FadeIn(a1), run_time=0.5)
        self.gat("a de raio dois sobe")
        self.play(FadeIn(a4), run_time=0.5)

        # ── B4-3 · é o gráfico de z = x² + y² ──
        self.an("B4-3")
        g = TC(r"\S{z = x^2+y^2}", 1120, 580, 54)
        leg = legenda("A FOLHA PLANA VIRA UMA TIGELA", 1124, 690)
        self.gat("essa tigela é exatamente o gráfico")
        self.play(caneta(g), FadeIn(leg))
        self.gat("fabricar uma superfície")
        self.play(pulso(g, 1.05), run_time=1.0)
        self._fecha()
        self.play(FadeOut(VGroup(a1, a4)), FadeOut(form), FadeOut(g), FadeOut(leg), folha.op.animate.set_value(0.0), run_time=0.4)
        folha.clear_updaters()
        self.remove(a1, a4, folha, form, g, leg)
        self.sai_fim()
