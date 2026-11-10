"""Lote PB7 · NO ESPAÇO (B7-1, B7-2). F⃗(X) = −X/‖X‖³, ‖F⃗‖ = 1/r².
Cena 3D `campo_espaco` (fundo liso): cascas de raio 1,25 / 1,75 / 2,25 com 14 / 22 / 30 direções de Fibonacci, setas sólidas para a origem com 0,92/r²
(1,1/r²: 0,70 → 0,22, sem teto; a opacidade de cada seta cai a 0 por quadro perto da linha de visada, rampa 35° → 25°), um anel por casca sempre de frente para a câmera, anel vazado no furo; câmera fora dos eixos (elevação 22°, azimute de 35° a 155° em 12 s). B7-2 sem zoom: o anel pulsa duas
vezes e as cascas de fora escurecem (sem transparência). Domínio A = ℝ³ − {0} (A em GEO)."""
from kit import *  # noqa: F401,F403

XC, YC = -2.6, -0.3


class LoteB7(Base):
    def corpo(self):
        seg = {}

        def est(t):
            u = min(1.0, t / 12.0)
            az = 35 + 120 * u + 10 * max(0.0, t - 12.0) / 20.0
            d = t - seg["dom"] if "dom" in seg else -1.0
            pulso = math.sin(PI * d / 0.8) ** 2 if 0.0 <= d <= 1.6 else 0.0          # duas pulsações do anel
            longe = 1.0 - 0.65 * suave(d / 1.0) if d >= 0 else 1.0
            return {"longe": longe, "pulso": pulso, "cam": cam_obl(az, 22, (0, 0, 0), K=1.35, xc=XC, yc=YC)}

        # ── B7-1 ──
        self.an("B7-1")
        self.secao("NO ESPAÇO")
        cmp = Fundo3D(self, "campo_espaco", est, op=0.0)
        self.add(cmp)
        self.papel(True, rt=0.5)
        self.play(cmp.op.animate.set_value(1.0), run_time=0.8)
        print("[campo] B7 campo_espaco: 1,1/r² nas cascas 1,25 / 1,75 / 2,25 → 0,704 / 0,359 / 0,217, sem teto; 66 setas, nenhuma descartada (a opacidade cai por quadro perto da visada: ver log_3d_PB7)")
        f1 = Fs(r"\vec F(X) = -\dfrac{X}{\|X\|^3}", {CAMPO: [0, 1], POS: [3, 7, 10]}, size=M_L).move_to(P3(3.9, 2.0))
        f2 = Fs(r"\|\vec F\| = \dfrac{1}{r^2}", {CAMPO: [1, 2], POS: [7]}, size=M_L).move_to(P3(3.9, 0.3))
        self.gat("em cada ponto do espaço")
        self.play(caneta(f1))
        self.gat("com tamanho igual a um dividido")
        self.play(caneta(f2))

        # ── B7-2 · o domínio ──
        self.an("B7-2")
        self.gat("bem na origem")
        seg["dom"] = self.t
        dom = F(("A", GEO), "=", r"\mathbb{R}^3", "-", r"\{0\}", size=M_L).move_to(P3(3.9, -1.5))
        self.gat("menos um ponto")
        self.play(caneta(dom))
        self.gat("o domínio faz parte da função")
        self.play(pulso(dom, 1.05), run_time=1.0)
        self._fecha()
        self.play(FadeOut(VGroup(f1, f2, dom)), cmp.op.animate.set_value(0.0), run_time=0.4)
        cmp.clear_updaters()
        self.remove(cmp, f1, f2, dom)
        self.papel(False, rt=0.4)
        self.sai_fim()
