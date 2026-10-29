"""Lote X1: refaz o teste das cenas 3D com as correções da avaliação (2026-10-28 §2) e a granada em Three.js (§2-D).
D — granada: H1 (subida), H2 (explosão em câmera lenta), H3 (parábola tracejada → ⊕ → pergunta, congela 2 s antes do toque), T2-8 (toque).
A — haltere: giro oblíquo → para horizontal na frontal → apoio → balança e equilibra → régua e cotas (sem troca para 2D).
B — explosão: T2-6 (chão: P → três mᵢv⃗ᵢ somados ponta com ponta), T3-1 (velocidades do chão), T3-2 (acompanha o CM: sai a parte comum),
    T3-3 (momentos relativos iguais → triângulo).
C — semiesfera: fatia translúcida, cotas z, dz, √(R² − z²) e 3R/8."""
from camadas import *  # noqa: F401,F403


class LoteTeste3D(Camadas):
    def construct(self):
        self.setup_base(cap="TESTE 3D")
        self.teste_granada()
        self.clear()
        self.teste_haltere()
        self.clear()
        self.teste_explosao()
        self.clear()
        self.teste_semiesfera()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def teste_granada(self):
        g = self.granada_hook(dur_h1=8.0, dur_h2=6.0, dur_h3=10.0)
        self.granada_toque(g, dur=12.0)

    def teste_haltere(self):
        h = self.haltere_giro(giro=3.0)
        h.parar(2.6)
        self.play(FadeOut(self.selo_cam), run_time=0.4)
        h.apoiar()
        self.haltere_regua(h)
        self.wait(1.5)

    def teste_explosao(self):
        e = self.explosao_chao_momento(dur=10.0)
        self.explosao_chao_velocidades(e, dur=5.0)
        self.explosao_segue_cm(e, dur=4.0)
        self.explosao_relativos(e, dur=5.0)

    def teste_semiesfera(self):
        self.semiesfera_cotas(dur=7.0)
