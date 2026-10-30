# CENTRO DE MASSA — O PONTO QUE UMA EXPLOSÃO NÃO CONSEGUE DESVIAR

- **ID:** yt_0017 (provisório; 3º vídeo do 4.9). Série do 4.9: yt_0015 uma partícula → yt_0016 sistemas → **yt_0017 centro de massa** → vídeo de
  exercícios de centro de massa → foguete (IDs provisórios). O EN2 do yt_0016 prometeu a granada.
- **formato:** longo_horizontal
- **natureza:** teoria_visual (com dois exercícios ilustrativos; os difíceis vão para o vídeo seguinte)
- **disciplina:** Física I · **bloco:** Momento e colisões · **modulo:** 4.9 Momento linear e impulso
- **referencia:** Sears 8.5 · Moysés cap. 8 · Feynman I, cap. 19 (só na ficha e na descrição). Os números dos exemplos são construção do Parallax Lab.
- **duração esperada:** ~19–20 min com a voz (narração v3: 3.114 palavras; nominal 19,2 min a 2,7 palavras/s; lote 1 ≈ 9:18)
- **solido_3d:** nenhum do arsenal Blender (3D em Three.js na unidade: `threejs/cena3d/campo.js` e `cm3d.js`).
- **3d_threejs (handoff v3 do lote 1, §1.5):** campo de provas em vácuo + granada de fragmentação que se estilhaça em três cacos do próprio corpo
  (hook, A2, A4, T2-7, T2-8, S1); a mesma granada no espaço, céu sem piso (T2-6, T3-1/2/3/5); bandeja com pino (T1-7). Em 2D: haltere (T1-1/2,
  T2-1/2), molas (T2-4), gelo (T2-9) e, no lote 2/3, colisão, barra, placa e canoa. Pipeline por estado do yt_0016 (`threejs/r3d.js` +
  `render3d.sh`); o Manim prende ⊕, setas, eixos e rótulos pelas coordenadas projetadas (`projeta3d`, conferido com `pontos.json`).
  Volumes e centroides dos cacos: `threejs/cena3d/granada_medidas.json` (exportado do Three.js; lido por `pecas3d.py`).
- **Status:** preview silencioso 960×540 / 15 fps do vídeo inteiro (handoff v4 de 2026-10-29, narração v3.1: hook, abertura, T1–T4, E1, E2,
  síntese, encerramento; 18:58): `renders/preview_yt0017_completo_960x540.mp4`, QA em `renders/qa.txt` (sem voz, SRT, master nem entrega).
- **Tag do canto:** `MECÂNICA · CENTRO DE MASSA`
- **Pergunta narrativa:** "Se a granada explode no meio do voo, o que continua na mesma parábola?"
- **Pergunta central:** existe um ponto do sistema que só obedece às forças externas? Onde ele está e como se calcula?
- **Quatro perguntas dos blocos de teoria:** onde está? · como se move? · que energia é do movimento relativo? · como achar num corpo inteiro?
- **Pré-requisitos:** yt_0015 (p⃗ = m v⃗, F⃗ = dp⃗/dt), yt_0016 (internas se cancelam, dP⃗/dt = F⃗_ext, K = p²/2m), derivada e integral simples.
- **Payoff:** R⃗_cm = Σ mᵢ r⃗ᵢ / M (também por partes); P⃗ = M V⃗_cm e M A⃗_cm = F⃗_ext; K = ½ M V²_cm + K_rel.
- **Fontes da especificação:** handoff v3 do lote 1 de 2026-10-29 (sistema visual §1, regras de tela §2, lote 1 §3–§5) e `narracao_sugestao.md`
  (narração v3 = Anexo A do handoff).

## Estrutura
hook H1–H3 (granada) · abertura A1–A4 · T1 onde está (com T1-8 por partes) · T2 como se move · T3 que energia é do movimento relativo · T4 corpo
inteiro · E1 placa com entalhe · E2 remador e estaca · síntese S1–S2 · encerramento EN1–EN2 (próximo vídeo: exercícios; depois, o foguete).
Lotes: (1) hook, abertura, T1, T2 · (2) T3, T4 · (3) E1, E2, síntese, encerramento.

## Cabeçalho e capítulos
Linha 1: `MECÂNICA · CENTRO DE MASSA`; linha 2 = capítulo: T1 `ONDE ESTÁ O CENTRO DE MASSA?` · T2 `COMO ELE SE MOVE?` ·
T3 `QUE ENERGIA É DO MOVIMENTO RELATIVO?` · T4 `COMO ACHAR O CENTRO DE MASSA DE UM CORPO INTEIRO?` · E1 `EXERCÍCIO 1 · PLACA COM ENTALHE` ·
E2 `EXERCÍCIO 2 · REMADOR E ESTACA` · síntese `RESUMO`.

## Marcador do centro de massa e cores (v3)
⊕ em degradê ciano `#35D9FF` → magenta `#EA63FF` (anel em degradê angular, cruz branca fina, halo e glow em degradê), com rastro em degradê ao
longo do comprimento; exclusivo do CM: nenhuma outra coisa usa degradê (G15). `marcador_cm()`, `rastro_cm()` e `CM_A`/`CM_B` no `kit.py`.
Nas contas: R⃗_cm, X, Y, X_cm, R⃗₀ ciano-claro `CMC #8BE9FF`; posições `GEO`; velocidade violeta; momento magenta; força `FC`; impulso `JC`;
rastros finos dos corpos `RAST #9FB4D6`; corpos em aço com a luz B (também em 2D: `esfera2d`, `silhueta`). Amarelo e verde não entram.
