"""Reaponta os gatilhos (gat) de T5-2 em diante para a palavra que NOMEIA cada evento (a imagem não pode antecipar nem atrasar a fala)."""
from pathlib import Path

U = Path(__file__).resolve().parent


def sub(arq, a, b):
    p = U / arq
    s = p.read_text(encoding="utf-8")
    if a not in s:
        print("NÃO ACHEI em", arq, ":", a[:90].replace("\n", "⏎"))
        return
    p.write_text(s.replace(a, b, 1), encoding="utf-8")


# ── T5-2: B2 em "deixa de depender do ângulo"; B3 em "sai meio I ômega final" ──
sub("sec_t5.py", 'self.gat("em relação ao ângulo")', 'self.gat("integral deixa de depender do ângulo")')
sub("sec_t5.py", 'self.gat("energia cinética de rotação")', 'self.gat("sai meio i ômega final")')

# ── T5-3: motor só em "imagina um motor" (depois da fórmula P = τω) ──
sub("sec_t5.py", "        self.play(FadeIn(mv), FadeIn(lbl_mot), run_time=0.7)\n\n        C1, ic1", "        C1, ic1")
sub("sec_t5.py", '        self.gat("quatro mil rotações por minuto")\n        C2, ic2', '        self.gat("imagina um motor")\n        self.play(FadeIn(mv), FadeIn(lbl_mot), run_time=0.7)\n        self.gat("quatro mil rotações por minuto")\n        C2, ic2')
sub("sec_t5.py", 'self.gat("quarenta e dois quilowatts")', 'self.gat("multiplica quase quarenta e dois")')

# ── T5-4: fórmula em "reduz a rotação três vezes"; selo em "primeira marcha" ──
sub("sec_t5.py", "        self.pilha.poe(D1b)\n        self.play(ev.op.animate.set_value(1.0), FadeIn(lbl_e1), FadeIn(lbl_e2), run_time=0.8)\n        self.cx(D1b[0])\n        self.monta(D1, id1, {}, rt=1.1)\n        self.gat(\"multiplica o torque três vezes\")",
    "        self.pilha.poe(D1b)\n        self.play(ev.op.animate.set_value(1.0), FadeIn(lbl_e1), FadeIn(lbl_e2), run_time=0.8)\n        self.gat(\"reduz a rotação três vezes\")\n        self.cx(D1b[0])\n        self.monta(D1, id1, {}, rt=1.1)\n        self.gat(\"multiplica o torque três vezes\")")
sub("sec_t5.py", '        self.selo("CAIXA DE MARCHAS"', '        self.gat("primeira marcha arranca o carro")\n        self.selo("CAIXA DE MARCHAS"')

# ── T6-1 ──
sub("sec_t6.py", "        self.play(FadeIn(v_df), FadeIn(a_om), FadeIn(l_om), FadeIn(tag_mesa), run_time=0.8)\n        self.monta(A1, ia1, {0: l_om[1]}, rt=1.0)\n        self.gat(\"soma dos torques ao longo do eixo é zero\")",
    "        self.gat(\"pensa num disco deitado\")\n        self.play(FadeIn(v_df), FadeIn(a_om), FadeIn(tag_mesa), run_time=0.8)\n        self.gat(\"com velocidade angular constante\")\n        self.play(FadeIn(l_om), run_time=0.5)\n        self.gat(\"a aceleração angular é zero\")\n        self.monta(A1, ia1, {0: l_om[1]}, rt=1.0)")
sub("sec_t6.py", 'self.gat("andando em círculo")', 'self.gat("ele tem aceleração centrípeta")')
sub("sec_t6.py", 'self.gat("mancal puxando para o eixo")', 'self.gat("então girar com velocidade angular constante")')

# ── T6-2: Δr × ΣF em "aparece um termo extra" ──
sub("sec_t6.py", "        self.pilha.poe(B2)\n        self.monta(B2, ib2, {4: l_dr}, rt=1.1)", "        self.pilha.poe(B2)\n        self.gat(\"aparece um termo extra\")\n        self.monta(B2, ib2, {4: l_dr}, rt=1.1)")

# ── T6-3: cada elemento na frase que o nomeia ──
sub("sec_t6.py", "        self.pilha.poe(C1)\n        self.play(FadeIn(gan), FadeIn(l_30), FadeIn(l_45), FadeIn(cota_15), FadeIn(cota_10), FadeIn(s_p30), FadeIn(s_p45), run_time=0.8)\n        self.monta(C1, ic1, {0: l_30, 3: cota_15, 5: l_45, 8: cota_10}, rt=1.1)\n\n        self.gat(\"pega o próprio apoio\")\n        self.play(FadeIn(s_N), FadeIn(l_N), run_time=0.6)\n        self.gat(\"trinta vezes um e meio\")\n",
    "        self.pilha.poe(C1)\n        self.gat(\"na gangorra\")\n        self.play(FadeIn(gan), FadeIn(s_p30), FadeIn(s_p45), run_time=0.8)\n        self.gat(\"pega o próprio apoio\")\n        self.play(FadeIn(s_N), FadeIn(l_N), run_time=0.6)\n        self.gat(\"uma massa de trinta quilos\")\n        self.play(FadeIn(l_30), FadeIn(cota_15), run_time=0.6)\n        self.gat(\"quarenta e cinco a um metro\")\n        self.play(FadeIn(l_45), FadeIn(cota_10), run_time=0.6)\n        self.gat(\"porque trinta vezes um e meio\")\n        self.monta(C1, ic1, {0: l_30, 3: cota_15, 5: l_45, 8: cota_10}, rt=1.1)\n")

# ── T6-4: conta de força junto com as frases ──
sub("sec_t6.py", "        self.pilha.poe(D1)\n        self.monta(D1, id1, {0: l_dob_sup, 2: l_ded_sup}, rt=1.0)", "        self.pilha.poe(D1)\n        self.gat(\"o dedo segura metade do peso\")\n        self.monta(D1, id1, {0: l_dob_sup, 2: l_ded_sup}, rt=1.0)")
sub("sec_t6.py", "        g_inf = VGroup(r_inf, s_mg_inf, s_acm_inf, l_acm_inf, s_dob_inf, l_dob_inf)", "        g_inf = VGroup(r_inf, s_mg_inf)\n        g_acm = VGroup(s_acm_inf, l_acm_inf)\n        g_dobinf = VGroup(s_dob_inf, l_dob_inf)")
sub("sec_t6.py", "        self.pilha.poe(D2)\n        self.monta(D2, id2, {6: l_acm_inf}, rt=1.0)", "        self.pilha.poe(D2)\n        self.gat(\"o centro de massa passa a acelerar\")\n        self.play(FadeIn(g_acm), run_time=0.6)\n        self.gat(\"o peso menos a força da dobradiça\")\n        self.monta(D2, id2, {6: l_acm_inf}, rt=1.0)")
sub("sec_t6.py", "        self.cx(D3b[0])\n        self.monta(D3, id3, {0: l_dob_inf}, rt=1.0)", "        self.cx(D3b[0])\n        self.play(FadeIn(g_dobinf), run_time=0.5)\n        self.monta(D3, id3, {0: l_dob_inf}, rt=1.0)")

# ── S2: 3g/2 em "na ponta três meios de g" ──
sub("sec_fim.py", "FadeIn(s_23_s2), FadeIn(s_pt_s2), FadeIn(lbl_pt_s2), run_time=0.9)", "FadeIn(s_23_s2), run_time=0.9)")
sub("sec_fim.py", '        self.gat("os vizinhos puxam a ponta")', '        self.gat("na ponta três meios de g")\n        self.play(FadeIn(s_pt_s2), FadeIn(lbl_pt_s2), run_time=0.6)\n        self.gat("os vizinhos puxam a ponta")')
