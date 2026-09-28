# vid_0006 — Roteiro visual e narração sincronizada

Narração ElevenLabs (`audio/narracao_final.wav`, 104,64 s, intacta); vídeo de 105,5 s.
Os tempos abaixo são segundos do WAV e correspondem aos `self.until(...)` da cena; os
pontos de sincronia foram obtidos alinhando as frases às pausas medidas no áudio.

Arco: curiosidade → superposição → interferência → cancelamento → fone.
Cores: ciano = onda 1 / ruído · magenta = onda 2 / fone · branco = soma / resíduo ·
azul = eixos / fone · violeta = processamento / atraso.

| Bloco | Tempo (s) | Visual | Texto na tela |
|---|---|---|---|
| C1. Gancho | 0–5,6 | Fone de ouvido em corte, ruído ciano chegando; painel perto do ouvido: a contribuição do fone cresce (2,74–5,24) e a branca encolhe. | “O som pode cancelar o próprio som?” · PERTO DO OUVIDO |
| C2. Volta à física | 5,6–9,95 | Fone sai; entram p₁ (ciano) e p₂ (magenta); manchete em 8,19. | “Interferência de ondas” · p₁ = A sin(ωt) · p₂ = A sin(ωt) |
| C3. Superposição | 9,95–18,0 | Eixo da soma (11,3), equação (12,2); varredura ponto a ponto 13,21–16,71 com barras empilhadas, a curva branca nasce da soma. | “Superposição” · PRESSÃO EM UM PONTO · AO LONGO DO TEMPO · p_total = p₁ + p₂ |
| C4. Construtiva | 18,0–24,8 | Linha de crista e barras no pico (18,79); A + A = 2A e colchete (21,56); rótulo (22,96). | “Em fase” · A + A = 2A · CONSTRUTIVA |
| C5. Fase e amplitude | 24,8–35,8 | p₂ → A sin(ωt + φ); p_total = 2A cos(φ/2) sin(ωt + φ/2) (25,8); fator destacado e ligado ao colchete A_res (27,38); A_res = 2A\|cos(φ/2)\| (29,3); φ: 0 → π/2 (√2 A em 33,0, pausa) → π (0 em 35,7). | “Diferença de fase” · AMPLITUDE (0 ≤ φ ≤ π) |
| C6. Destrutiva ideal | 35,8–44,6 | p₂ = A sin(ωt + π) → −A sin(ωt) (37,74) → −p₁ (38,5); p_total = p₁ + p₂ (39,24) → p₁ − p₁ (40,5) → 0 (41,71); curva branca horizontal. | “Fases opostas” · CASO IDEAL · DESTRUTIVA |
| C7. Significado físico | 44,6–56,1 | Gráficos viram o inset p(t) em x₀; fileiras de camadas de ar (46,78), só deslocamento horizontal; congelamento com compressão/rarefação (50,75–51,8); resultante parada. | “O gráfico não é o formato do ar” · “No ar: compressões e rarefações” · ONDA 1 / ONDA 2 / RESULTANTE · AS ONDAS NÃO SE ANIQUILAM → A PRESSÃO RESULTANTE DIMINUI |
| C8–C9. Fone | 56,1–64,5 | Fone de ouvido desenhado; microfones piscam (57,7), pulsos ao processador, processador violeta (59,6), pulso ao alto-falante (60,6), arcos magenta (61,64). | “Cancelamento ativo de ruído” · fone de ouvido · microfones · processamento · alto-falante · ESQUEMA CONCEITUAL |
| C10. Imperfeito | 64,5–71,4 | Região perto do ouvido e painel (64,49); p_ruído + p_fone = p_residual e barras de amplitude (65,9); fone 0 → 0,9A (resíduo 0,179A); pulso no resíduo (69,65). | PERTO DO OUVIDO · p_ruído + p_fone = p_residual |
| C11. Melhor ajuste | 71,4–76,2 | g 0,9 → 0,95 e φ 0,95π → 0,97π (71,5–73,5): resíduo 0,105A; comparação de amplitudes (73,6); pulso “não chega a zero” (74,8). | A_residual ≪ A_ruído |
| C12. Não é perfeito | 76,2–82,1 | Rótulos dos componentes saem; ruído ganha 3ω (76,62–78,42), resíduo com ondulação fina; fatores (79,5). | “Por que não é perfeito?” · FREQUÊNCIAS · ATRASO / POSIÇÃO · ACÚSTICA |
| C13. Onde funciona melhor | 82,1–93,5 | Ícones avião/motor/ar-condicionado; onda de frequência baixa (86,6) e alta (88,2); 1 PERÍODO (89,26); mesmo atraso (90,6); realce na onda longa (91,9). | “Onde costuma funcionar melhor” · FREQUÊNCIA MAIS BAIXA / MAIS ALTA · MESMO ATRASO |
| C14. Fechamento | 93,5–105,5 | Fone e painel com resíduo pequeno; realce magenta (95,4) e branco (97,6); síntese (98,7); @labparallax (101,12). | “O som não desaparece” · SUPERPOSIÇÃO → INTERFERÊNCIA → REDUÇÃO DO RUÍDO · @labparallax |

## Narração (texto usado no ElevenLabs)

| Início (s) | Fala |
|---|---|
| 0,04 | O som pode cancelar o próprio som? É isso que um fone com cancelamento de ruído explora. Pra entender como, vamos voltar à física: interferência de ondas. |
| 9,95 | Este gráfico mostra a pressão num ponto ao longo do tempo. As duas pressões se somam, e a curva branca nasce dessa soma: superposição. |
| 18,02 | Em fase, crista encontra crista e vale encontra vale. As ondas se reforçam: interferência construtiva. |
| 24,82 | Agora deslocamos a fase da onda magenta. O fator destacado determina a amplitude da soma. Repare na curva branca: de zero a meio ciclo, sua amplitude cai até zero. |
| 34,80 | Com meio ciclo de diferença, crista encontra vale. Se as amplitudes são iguais, uma compensa a outra e, nesse caso ideal, a soma é zero: interferência destrutiva. |
| 44,64 | Mas esse gráfico não é o formato do ar. No ar, as camadas oscilam para a frente e para trás, formando compressões e rarefações. As ondas não se aniquilam: o que diminui é a pressão resultante. |
| 56,10 | Agora, de volta ao fone. Os microfones captam o ruído, o processamento calcula uma resposta, e o alto-falante produz outra contribuição sonora. |
| 64,49 | Perto do ouvido, acontece a mesma soma. Como amplitude e fase não batem perfeitamente, sobra um resíduo, em branco. |
| 71,44 | Com um ajuste melhor, o resíduo fica menor. Mas, num fone real, não chega a zero. |
| 76,22 | O ruído real mistura várias frequências, e o sistema ainda lida com atraso, posição e acústica. |
| 82,10 | Por isso, o cancelamento ativo costuma funcionar melhor com ruídos contínuos e frequências mais baixas, como motor e avião. O período é maior, então o mesmo atraso gera uma diferença de fase menor. |
| 93,47 | O som não desaparece. O fone adiciona outra contribuição e reduz a pressão resultante perto do ouvido. |
| 99,91 | Se curtiu, siga o Parallax Lab. |

Faixa inferior (y < −4,6 na área lógica) livre para legendas.
