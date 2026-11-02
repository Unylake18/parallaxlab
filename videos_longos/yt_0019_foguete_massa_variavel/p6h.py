from ptch6 import patch
patch("sec_t3.py", [
 # §4.2: o dv dos dois insets voa para a vaga do ∫ (a soma de todos os dv)
 (r'''        self.play(FadeOut(ins), run_time=0.4)
        C, ic = M(r"\int_{v_0}^{v_f}dv", "=", "-", r"v_{ex}", r"\int_{m_0}^{m_f}\frac{dm}{m}", size=46, cores={0: VEL, 3: VEX_C})
        self.pilha.poe(C)
        self.gat("então integra")''',
  r'''        C, ic = M(r"\int_{v_0}^{v_f}dv", "=", "-", r"v_{ex}", r"\int_{m_0}^{m_f}\frac{dm}{m}", size=46, cores={0: VEL, 3: VEX_C})
        self.pilha.poe(C)
        alvo_i = mp(C, ic, [0]).get_left() + 0.25 * RIGHT                          # v6 §4.2: onde nasce o ∫
        resto_ins = VGroup(*[ins[k][i_] for k in (0, 1) for i_ in (0, 1, 2, 4, 5)])
        self.play(*[ins[k][3].animate.move_to(alvo_i).scale(0.35).set_opacity(0.0) for k in (0, 1)], FadeOut(resto_ins), run_time=0.8)
        self.remove(ins)
        self.gat("então integra")'''),
 # §4.2: a linha do sinal antes do resultado
 (r'''        E, ie = M(r"\Delta v", "=", r"v_{ex}", r"\ln\frac{m_0}{m_f}", size=50, cores={0: VEL, 2: VEX_C})
        self.pilha.poe(E)
        self.gat("e o sinal de menos inverte")''',
  r'''        E, ie = M(r"\Delta v", "=", r"v_{ex}", r"\ln\frac{m_0}{m_f}", size=50, cores={0: VEL, 2: VEX_C})
        Sg, isg = M("-", r"\ln\frac{m_f}{m_0}", "=", r"\ln\frac{m_0}{m_f}", size=40)
        self.pilha.poe(Sg, dx=1.2)
        self.pilha.poe(E)
        self.gat("e o sinal de menos inverte")
        self.play(FadeIn(Sg), run_time=0.5)'''),
])
