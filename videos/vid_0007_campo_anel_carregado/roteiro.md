# vid_0007 — Roteiro visual e narração sincronizada

Narração ElevenLabs (`audio/narracao_final.wav`, 148,0 s, intacta); vídeo de 148,3 s.
Os tempos abaixo são segundos do WAV e correspondem aos `self.until(...)` da cena; os
pontos de sincronia foram obtidos alinhando as frases às pausas medidas no áudio.

Arco: mistério (E = 0 no centro) → modelo → um dq → simetria → dE_z → integral → testes →
gráfico → derivada → R/√2.
Cores: ciano = dq / 1ª contribuição / curva · magenta = dq oposto · violeta = s, θ,
transformações do denominador, máximo · branco = resultante / equações · azul = anel / eixo.

| Bloco | Tempo (s) | Visual | Texto na tela |
|---|---|---|---|
| C1. Gancho | 0–11,9 | Anel centrado, eixo, P no centro com E = 0 (pisca em 5,9); P sobe (7,1–10,0) e a seta cresce, passa pelo pico e diminui, sempre por e(u). | ONDE O CAMPO ELÉTRICO / É MAIS FORTE? · E = 0 |
| C2. Modelo | 11,9–20,1 | P congela em u = 1,2; cota R (13,5), Q > 0 (15,2), P destacado (17,1) e cota z separada do eixo e da seta. | ANEL FINO · CARGA UNIFORME |
| C3. Um dq | 20,1–36,8 | dq ciano (20,9); corte lateral (21,65) com diâmetro auxiliar tracejado e seção do fio em −R; s (22,75) → R (26,34) → z (27,64); s² = R² + z² (28,94); segunda distância s até o elemento oposto (33,37). | “Um elemento de carga” · CORTE LATERAL · s² = R² + z² |
| C4. Simetria | 36,8–52,5 | dq magenta oposto (39,3); dE₁ e dE₂ (41,07); decomposição ponta–cauda (42,1); laterais com marcas de igualdade (43,2) e cancelamento (44,52); axiais separadas (45,95), soma ponta–cauda (48,2) e resultante branca (49,45); par girando pelo anel (50,1). | “Simetria” · LATERAIS SE CANCELAM · MESMO MÓDULO · SENTIDOS OPOSTOS · AXIAIS SE SOMAM · MESMO SENTIDO · SÓ SOBRA A COMPONENTE NO EIXO |
| C5. Campo de um elemento | 52,5–87,9 | Corte com dE, θ e projeção; uma relação principal por estado: dE = k dq/s² (55,3; destaques 56,0/58,0/59,6) → dE_z = dE cos θ (61,0) → cos θ = z/s (65,19; cateto 66,4, hipotenusa 67,7, segundo θ 68,9) → k dq/s² · z/s (71,3–72,05) → kz dq/(s²·s) (73,7) → s³ com contorno violeta (75,4) → s = √(R² + z²) (77,3–78,3) → [√(R² + z²)]³ (81,1) → (R² + z²)^{3/2} (83,6) → dE_z final em caixa (84,9). | “Campo de um elemento” · CORTE LATERAL · s²·s = s³ |
| C6. Somar o anel | 87,9–97,9 | Volta ao pseudo-3D; E(z) = ∫dE_z (89,2) → fator constante em caixa violeta, “R e z fixos” (90,5–91,6); dq percorre o anel com ∫dq piscando (93,5); ∫dq = Q abaixo do ∫dq (94,95); E(z) final em caixa (95,9). | “Somar o anel” · R e z fixos · ∫dq = Q |
| C7. Dois testes | 97,9–108,6 | P ao centro: z = 0 ⇒ E = 0 (99,2–100,4); P volta e o anel é visto de longe (103,1), sem mudar R; E ≈ kQ/z² e rótulo Q (105,2). | “Dois testes” · VISTO DE MUITO LONGE · z ≫ R · E ≈ kQ/z² |
| C8. Ver a função | 108,6–115,4 | Anel centrado acima do gráfico; P, seta e marcador pelo mesmo `self.u`, desacelerando perto do pico (111,5–115,2). | “O campo ao longo do eixo” · E(z) · z |
| C9. Encontrar o máximo | 115,4–133,1 | E(z) = kQz(R² + z²)^{−3/2} (116,3) → dE/dz (117,6); denominador esmaecido + “> 0” (118,6); numerador violeta (120,4); R² − 2z² = 0 com o marcador indo ao pico (122,55); 2z² = R² (125,25); z = R/√2 (126,5, marcador já no pico); sinais + / 0 / − na curva (128,3); destaque do máximo (131,03). | “Encontrar o máximo” |
| C10. Resultado | 133,1–140,3 | Anel à esquerda; cota violeta O → P = R/√2, guia no pico do gráfico (134,4); z_max = R/√2 (135,3) e ≈ 0,71R (136,5). | “Onde o campo é máximo” · z_max = R/√2 · R/√2 ≈ 0,71R |
| C11. Fechamento | 140,3–148,3 | Composição limpa mantida; síntese em três passos (140,26 / 142,09 / 144,2); @labparallax discreto (145,91). | SIMETRIA → INTEGRAÇÃO → MÁXIMO · @labparallax |

## Narração (texto usado no ElevenLabs)

Texto completo e inícios medidos por bloco em `ficha.md`.

Faixa inferior (y < −4,6 na área lógica) livre para legendas.
