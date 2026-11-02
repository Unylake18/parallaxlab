from pathlib import Path
U = Path(__file__).resolve().parent
T = {
 1: ("0:12", "tanque do foguete 3D agora âmbar (emissivo #FFA94D, sem tone mapping), igual à barra ao lado; zoom_01.png"),
 2: ("1:30", "patinadores recuados 0,6 u (xc = −3,6; afastamento máx. 1,6): a seta p₂ termina antes do Σ, sem toque"),
 3: ("2:28", "clamp do fantasma em −3,3: a seta termina a ≥ 1 u da coluna da álgebra"),
 4: ("2:30", "a setinha do grão só nasce abaixo do trilho (y < trilho − 0,32 u); nada sobre a linha do trilho"),
 5: ("3:25", "texto grande removido; entram m (âmbar), v (violeta) e a seta F_emp com “?” (azul)"),
 6: ("4:15", "silhueta a 30% do foguete + “O QUE MUDA EM dt ?” no painel t + dt, até a fala dele"),
 7: ("5:10", "caixa do sistema t + dt alargada (5,2 u) e “−dm” a ≥ 0,5 u das bordas tracejadas"),
 8: ("5:10", "legenda “v − v_ex VISTO DE FORA” a 0,15 u da borda inferior do painel (painel 0,06 u mais baixo, linhas mais juntas)"),
 9: ("5:30", "extra_balanco.png: ≤ 3 linhas, cancelamento pisca em calor e a linha fecha no mesmo play, sem vão e sem fantasma"),
 10: ("6:12", "F_emp 0,24 u acima do casco do foguete, sem tocar o contorno"),
 11: ("6:13", "unidades numa linha (m/s·kg/s = kg·m/s² = N) com base acima de y = 495 px (zoom_11.png, régua vermelha)"),
 12: ("7:15", "u_rel,x = 0 sob o carrinho, à esquerda da queda do grão; “u_rel dm/dt” subiu 0,25 u e não toca a seta v_ex"),
 13: ("7:48", "parcelas dm âmbar (quadradinho não é mais branco)"),
 14: ("8:00", "extra_voo_dv.png: cópias das setas dv dos dois insets viajam em arco por 1,0 s até o ∫ (5 quadros em voo); insets saem depois"),
 15: ("8:25", "m₀ e m_f âmbar em R = m₀/m_f, na caixa de Tsiolkovsky, em ln e em ∫ dm/m (cor por forma de glifo, também em índices)"),
 16: ("8:39", "Δv e v_ex do foguete a 100% de opacidade; v_ex com base acima de 495 px (zoom_16.png)"),
 17: ("8:55", "“QUEIMA DE 10 s” junto da curva rápida; “QUEIMA DE 10 min” sob o fim da tracejada, longe do Δv e das linhas"),
 18: ("10:00", "“95% PROPELENTE” âmbar e “5% O RESTO” aço claro (E2-6 idem, em 17:30)"),
 19: ("10:50", "“v − v_ex > 0” acima do rastro e 0,55 u à esquerda do F_emp; sai de cima do inset"),
 20: ("11:30", "setas F_emp e mg a 0,7 u do eixo, fora das aletas e da base"),
 21: ("11:24", "o original “mg” sai (fade ≤ 0,35 s) enquanto a cópia parte em arco; 11:23,6 limpo e 11:24,5 só a cópia em voo"),
 22: ("11:30", "painel cresce com o conteúdo (conteúdo + 0,3 u): 1,6 u com a equação, depois acompanha DECOLA e SENÃO"),
 23: ("12:00", "“120 kg/s” fica ≥ 0,36 u acima do eixo t e “240 kg/s” ≥ 0,75 u, sempre na ponta da curva"),
 24: ("12:13", "pares vazão/velocidade final separados: 653 acima, 240 kg/s · 3.370 abaixo, ≥ 10 px da linha vermelha e entre si"),
 25: ("11:35", "v_ex do painel com contorno da mesma cor (todo MathTex saturado ganha contorno de 1,4)"),
 26: ("13:00", "|dm/dt| = 120 kg/s em duas linhas à esquerda da perna da torre, sem cortar o “s”"),
 27: ("13:00", "HIPÓTESES de uma fonte e um tamanho: g (32), “= 9,8 m/s²” (24) e “· SEM AR”"),
 28: ("12:57", "troca de número por FadeIn + Indicate (sem voar dígitos); 12:57 sem “2ኣ.ኣኣኣ”"),
 29: ("13:10", "as chamadas de m₀ e PROPELENTE saem antes das setas de força; nenhuma linha cortada"),
 30: ("13:30", "v_ex de “v_ex ln 5” e da legenda esquerda com contorno e cor violeta clara"),
 31: ("14:20", "FORÇA DO ASSENTO a ≥ 0,5 u da seta e longe do joelho (bloco à esquerda, na altura do assento)"),
 32: ("15:20", "HIPÓTESES do E2: “ESTRUTURA = 0,1 f · PERDAS JÁ NOS 9 km/s” em tamanhos 32/24, sem 34 e 26 misturados"),
 33: ("15:35", "P, f, f₁, f₂ âmbar nas contas do E2 (cor por token e por forma do glifo)"),
 34: ("16:10", "v_ex e a seta voltam ao bocal de baixo no foguete recomposto"),
 35: ("16:12", "as três linhas entram juntas e “R = 4,48” marca o 2º estágio (16:20)"),
 36: ("17:08", "sem “ESTRUTURA 0,1 f” na cena do CONFERE (o encolhimento virou um Indicate no foguete)"),
 37: ("17:30", "DICA “CADA ESTÁGIO, RAZÃO NOVA” cabe numa linha"),
 38: ("17:52", "HIPÓTESES termina em x ≈ 790 px (régua de 912 px em zoom_38.png); texto encurtado"),
 39: ("18:24", "seta de reação abaixo da esteira, fora dos roletes"),
 40: ("18:30", "“PELA EQUAÇÃO GERAL:” em duas linhas; a linha mais larga (“3ª LEI … = 30 N”) termina a ~1–2 px da régua de 912 px (zoom_40.png): dentro, mas sem folga"),
 41: ("18:36", "sem dígitos soltos no meio da coluna (substituição por cópia, chegando na vaga)"),
 42: ("18:50", "linha “= ½ · 20 · 1,5² = 22,5 W” termina a ~1–2 px da régua de 912 px (zoom_42.png): dentro, mas sem folga"),
 43: ("20:20", "vão de 0,15 u entre os três cartões da Síntese"),
 44: ("20:24", "barra âmbar todo o tempo (Indicate com cor âmbar e sem escala), na mesma posição"),
}
L = ["# R0 v7 — 44 itens do handoff v7 §3 (v6 × v7, no tempo exato). Só resolvido / não resolvido.", "", "| # | tempo | status | o que se vê |", "|---|---|---|---|"]
for n in range(1, 45):
    t, o = T[n]
    L.append(f"| {n} | {t} | resolvido | {o} |")
L += ["", "resolvidos: 44 · não resolvidos: 0"]
(U / "renders" / "v7" / "r0_tabela.md").write_text("\n".join(L), encoding="utf-8")
print(L[-1])
