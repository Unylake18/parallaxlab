# Momento angular do corpo rígido

formato: longo_horizontal
natureza: teoria_visual
disciplina: Física I
bloco: Rotação
modulo: 4.11 Rotação de corpos rígidos (momento angular do corpo rígido)
referencia: Kleppner & Kolenkow, An Introduction to Mechanics, 1ª ed., Ex. 6.2 e 6.6, §7.2 e Ex. 7.4–7.6; Moysés vol. 1, cap. 12; Sears, cap. 10

Série pública: **MECÂNICA · EP. 6 (ROTAÇÃO DE CORPOS RÍGIDOS)** (provisório)

pergunta_narrativa: Como pode existir torque sem aumentar a velocidade angular?
pergunta_central: o que é o momento angular de um corpo rígido em eixo fixo, quando ele não aponta ao longo do eixo e o que é preciso para manter esse eixo no lugar?
pre_requisitos: L = r × p; torque = dL/dt; I = soma m rho²; torque = I alpha; produto vetorial; força centrípeta
payoff_principal: L_z = I_z omega é só a componente axial; torque pode mudar só a direção de L com omega constante; no eixo principal L = I omega vetorial; simetria ajuda a localizar os eixos, sem ser condição necessária
duracao_alvo: ~14 min, teto 15 min; estimativa da fala preservada a 2,7 palavras/s, sem voz nesta fase
3d_threejs: bancada_dupla (H, S1: dois halteres lado a lado); pendulo_conico (A, B1); corpo_voxel (B2, B4-3); haltere_torto (B3, B4-1, B5), com câmeras de topo (TOPO) e axial; roda_balanceamento (B6), com câmeras CLOSE, AXIAL e PERFIL; plataforma_livre (S2, gancho; câmeras TOPO e PERFIL)
solido_3d: nenhum do arsenal Blender; geometria própria em Three.js

## Especificação congelada

Fonte integral: `handoff_v1.md`. Narração integral extraída, sem reescrita: `narracao_v1.md`. A implementação e o QA usam `ancoras.json` e `tab25.json`.
Convenção: z para cima; omega positivo anti-horário visto de cima; roda com eixo horizontal y. Origem do pêndulo no prego; haltere e batata no CM.
L em #F19AFF; posição #D2823A; massa/inércia #FF7EB6; velocidade #9C8CFF; força/torque #5AA2FF; aceleração #3FE08B; ângulo #FFC24D; operadores e unidades neutros.

## Storyboard

H/A: pergunta sobre o torque do peso no pêndulo → B1: L só muda de direção → B2: soma dos pedaços e componente axial → B3: haltere torto, transversais se somam → B4: eixo principal e remontagem da batata → B5: binário dos mancais e conferência centrípeta → B6: roda, balanceamento estático versus dinâmico → S/EN: síntese, corpo deformável e pergunta para comentários.

## Fase aberta

Fechamento (HANDOFF FINAL, 2026-11-09): voz ElevenLabs v4, sincronização por âncoras, `.srt`, render 1080p, master e entrega em `entregas/`. Não iniciar publicação, capa, commit ou push. Critérios completos do portão e artefatos: handoff §7. Estado medido: `renders/qa.txt`, quando gerado.
