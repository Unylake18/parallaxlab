# FEM DE MOVIMENTO E REGRA DO FLUXO MAGNÉTICO

_Pergunta narrativa interna: "Como movimento vira corrente?" (não é o título acadêmico da unidade)._

- **ID:** yt_0010
- **formato:** longo_horizontal
- **natureza:** derivacao_aplicada
- **macroassunto:** eletromagnetismo
- **modulo:** inducao_eletromagnetica
- **solido_3d:** nenhum (o vídeo é implementado primeiro integralmente em Manim puro; o sólido aprovado `barra_trilhos_fem_movimento` pode ser testado numa rodada posterior como ganho visual pontual, mas não é estrutural)
- **Status:** preview visual silencioso em produção (960×540 / 15 fps; sem voz, SRT, capa ou final)
- **Classe:** `FemMovimentoYT010` em `cena.py`

## Pergunta central
Se a força magnética não realiza trabalho, de onde vem a energia da corrente gerada quando movemos um circuito através de um campo magnético?

## Pré-requisitos
Força de Lorentz; corrente e resistência; lei de Ohm; potência elétrica; trabalho e energia; produto vetorial; noções básicas de fluxo.

## Payoff principal
E_diss = K₀ = ½ m u₀². O campo magnético fornece o acoplamento entre o movimento mecânico e o circuito, mas não fornece a energia.

## Aparato único
Dois trilhos horizontais, resistor à esquerda fechando o circuito, barra vertical móvel, campo B uniforme entrando na tela.
Barra puxada com u ≈ constante (N01–N25) → mesma física por fluxo e faixa varrida → retorno ao mesmo aparato sem força externa (Griffiths 7.7).

## Física congelada
- +x̂ direita, +ŷ cima, +ẑ para fora da tela. **B = −B ẑ**, uniforme e estacionário. **u = u x̂**.
- Circuito positivo anti-horário ⇒ n̂ = +ẑ. u × B = +uB ŷ; corrente convencional sobe pela barra.
- I dℓ × B aponta para −x̂ (arrasto); força externa para +x̂ quando u = constante.
- Portadores: carga positiva de prova + corrente convencional (nunca elétrons). u = velocidade da barra (corpo rígido); v_d = deriva relativa ao material; w = u + v_d.
- Φ_B = −B l x; dΦ_B/dt = −B l u; ℰ = B l u = −dΦ_B/dt.
- Faixa varrida: d**a** = (u × dℓ) dt; B·(u × dℓ) = −(u × B)·dℓ ⇒ dΦ_B/dt = −∮(u × B)·dℓ.
- Barra livre: m du/dt = −(B²l²/R) u ⇒ u = u₀ e^{−t/τ}, τ = mR/(B²l²); I = I₀ e^{−t/τ}; P_R = P₀ e^{−2t/τ}; E_diss = ∫P_R dt = ½ m u₀².

## Hipóteses do modelo
- Campo externo uniforme e estacionário.
- Trilhos e barra ideais (resistência desprezível); o resistor desenhado concentra a resistência total efetiva R.
- Autoindutância desprezível ⇒ mesmo na desaceleração ℰ_mov = B l u(t) = R I(t). Não há termo L dI/dt.
- Sem campo elétrico induzido por ∂B/∂t (não aparece ∂B/∂t na tela; só o texto "Campo magnético estacionário; circuito em movimento.").

## Storyboard (N01–N48)
| Bloco | Estados | Conteúdo |
| --- | --- | --- |
| Fenômeno e Lorentz | N01–N07 | aparato, convenções, barra e portadores, u×B, ℰ = Blu, I = Blu/R, P_R = I²R |
| Paradoxo | N08–N10 | w = u + v_d, F_B·w = 0, conflito P_R > 0 × F_B·w = 0 |
| Arrasto e potência | N11–N13 | F_mag = IlB (←), F_ext (→), P_ext = P_R |
| Fluxo | N14–N18 | A = lx, orientação, Φ_B = −Blx, dΦ_B/dt = −Blu, ℰ = −dΦ_B/dt |
| Faixa varrida | N19–N25 | contorno C(t), C(t+dt), elemento d**a**, teste de orientação, tripla, prova |
| Barra livre | N26–N34 | retorno ao aparato, remove F_ext, m du/dt, separação, integração, u(t), τ |
| Sincronizado | N35–N39 | um único t controla barra, u(t), I(t), P_R(t) e brilho do resistor |
| Energia | N40–N44 | área sob P_R, integral, cancelamentos de B, l, R, E_diss = K₀ |
| Síntese | N45–N48 | P_ext = P_R, K₀ = E_diss, acoplamento ≠ fonte de energia |

## Convenção de cores (cena)
u violeta · B magenta · corrente/I/v_d verde · F_mag azul-claro · agente externo/energia mecânica ciano · calor/P_R/E_diss laranja (único tom quente) · aparato em aço.

## QA
Checklist físico de 18 pontos do briefing (sentidos de u, B, F, I, F_ext, orientação, normal, sinais de Φ_B, hipótese de L desprezível, decaimento assintótico, brilho ∝ u², cancelamentos B, l, R).
