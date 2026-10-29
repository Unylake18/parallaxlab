# HANDOFF v2 — yt_0015 "Momento linear e impulso" (preview silencioso v2, Parte 1 de 2)

Documento autocontido para o Claude Code. Matemática, números, textos de tela e storyboard são **especificação de implementação**
(AGENTS.md): não redesenhar. Se achar inconsistência objetiva, reporte antes de ampliar o escopo.
A narração congelada v3 (Anexo A do handoff original) está salva em `narracao_sugestao.md`; a v2 ficou em `narracao_sugestao_v2.md`.

## 0. Contexto e mudança de escopo
- A unidade já existe no worktree `.claude/worktrees/lucid-ritchie-cd87ad/videos_longos/yt_0015_momento_impulso/` (preview v1, 18:51).
  Trabalhe **nesse worktree**. Rode `git status --short` primeiro e preserve tudo.
- O Kaio avaliou o v1: **pouca teoria, exercício demais, raso; a pessoa parece um stick figure feio.** A Produção reescreveu o conteúdo
  com teoria do Moysés, do Sears e do Feynman, e **dividiu o vídeo em dois**:
  - **yt_0015 (esta rodada): uma partícula.** Hook dos joelhos, T1–T6 (teoria), E1–E5, síntese, CTA.
  - **yt_0016 (próxima rodada, não fazer agora): sistemas.** Os blocos C09–C13 do v1 (conservação em sistemas, gelo, caçador, gases do
    rifle, Newton e a luz) vão para lá. **Não apague esse código:** mova-o para `videos_longos/yt_0015_momento_impulso/_reservado_yt0016/`
    (inclusive o T2 do Three.js, o tanque de água) e tire-o do preview.
- Duração esperada do yt_0015: ~15–16 min.

## 1. Rodada
**Objetivo:** preview silencioso **v2** 960×540 / 15 fps, do hook ao CTA, seguindo o Anexo A. Sem voz, SRT, master, entrega, commit
ou push. Não alterar `template/`, `docs/`, `assets/` nem `experimentos/threejs/`.
**Reaproveitar do v1:** helpers (`kit.py`), header de duas linhas, cores, o trilho de ar em Three.js (vira o T2), os blocos dos exercícios
E1–E5 (antigos C04–C08), o pipeline 16:9 em `threejs/`.
**Atualizar:** `ficha.md` (status v2; `modulo: 4.9`; `referencia: Moysés 4.5 e 9.2 · Sears 8.1 · Feynman I, 10-1 a 10-5`;
`3d_threejs: hook/E4 (manequim), T2 (trilho de ar)`), `ancoras.json` regenerado da narração v3, `cena.py` e as seções.

## 2. Física congelada (só o que é novo; o resto segue o v1)
- **T1 (Moysés §4.5):** três experiências com discos iguais (massa m) num colchão de ar:
  (1) vᵢ = (+v, −v) → v_f = (−v, +v), trocam; (2) (+v, 0) → (0, +v); (3) com chiclete, (+v, 0) → os dois juntos com +v/2.
  Em todas, m·v₁ + m·v₂ antes = depois (tabela com totais em magenta).
- **T3:** Δp⃗₁ = −Δp⃗₂ → ÷Δt → Δt → 0 → dp⃗₁/dt = −dp⃗₂/dt → **F⃗₁₍₂₎ = −F⃗₂₍₁₎**. Bloco na mesa: P e N **no bloco**; a reação do peso
  desenhada **na Terra** (seta para cima, aplicada no centro da Terra). Esquema das cargas: só qualitativo, com o rótulo
  `MOMENTO DAS PARTÍCULAS + MOMENTO DO CAMPO = CONSTANTE`; não desenhar forças com valores.
- **T4:** F⃗_res = dp⃗/dt; com m constante, = m a⃗; selo `REFERENCIAL INERCIAL`.
- **T5:** J⃗ = F⃗Δt (força constante) → Riemann Σ F⃗ₖΔtₖ com 4 → 8 → 32 retângulos → ∫F⃗ dt; depois ∫F⃗_res dt = ∫(dp⃗/dt)dt = ∫dp⃗ = Δp⃗,
  com o `dt` se cancelando por `TransformByGlyphMap` (LaTeX estabilizado, `MathTex` de string única). Duas curvas de formas diferentes e
  **área numericamente igual** (reportar).
- **T6 (Sears §8.1):** dois painéis com a mesma seta de força: `× Δt → IMPULSO → Δp` e `× d → TRABALHO → ΔK`. K = p²/(2m) por substituição.
  Bolas: 0,50 kg a 4,0 m/s e 0,10 kg a 20 m/s → p = 2,0 kg·m/s nas duas; K = 4 J e 20 J; a mão recua 1× e 5× (mesma força média).
  Barcos no gelo, m e 2m, mesma força e mesma distância → mesma K; momento do pesado = √2 × o do leve.
- **E4 pelos dois caminhos:** impulso: Δt = 0,01 s e Δt = 1/7 s (escrever `≈ 0,143 s`) → F_res,méd = 56.000 N e 3.920 N.
  Trabalho: ΔK = ½·80·7,0² = 1.960 J; d = 0,5 m → 3.920 N; d = v·Δt/2 = 3,5 cm → 56.000 N. Depois N = F_res + m g (784 N) → ≈ 72 e ≈ 6 pesos.
  As curvas são **F_res(t)** com mesma área 560 N·s; não desenhar N com área igual.
- E1, E2, E3 e E5: números do v1, sem mudança.

## 3. Tela
- **Header (igual ao v1 e às colisões):** linha 1 `MECÂNICA · MOMENTO LINEAR E IMPULSO`; linha 2 = capítulo. Capítulos novos:

| Bloco | Linha 2 (= capítulo do YouTube) |
|---|---|
| Hook / abertura | — |
| T1 | `O FATO EXPERIMENTAL` |
| T2 | `POR QUE MASSA VEZES VELOCIDADE?` |
| T3 | `DA CONSERVAÇÃO À TERCEIRA LEI` |
| T4 | `A SEGUNDA LEI COM MOMENTO` |
| T5 | `IMPULSO` |
| E1 | `EXERCÍCIO 1 · BOLA NA PAREDE` |
| E2 | `EXERCÍCIO 2 · CHUTE EM 2D` |
| E3 | `EXERCÍCIO 3 · FORÇA QUE CRESCE COM O TEMPO` |
| T6 | `MOMENTO OU ENERGIA?` |
| E4 | `EXERCÍCIO 4 · DE VOLTA AO MURO` |
| E5 | `EXERCÍCIO 5 · A PULGA` |
| Síntese | `RESUMO` |

- **Selo de fonte** abaixo do header nos exercícios e nos blocos de teoria com fonte (`MOYSÉS §4.5`, `SEARS · EX. 8.2`, `FEYNMAN §10-3`),
  ~20, `DIM`, opacidade 0,6.
- **Selo DICA (peça nova):** cartão `PANEL` `#0E2A52` com borda `BLUE_L` `#7FB2FF`, no canto inferior direito, com `DICA` em ciano
  pequeno em cima e uma frase curta em maiúsculas. Entra no fim de cada exercício (e em T5-6, T6-5) e sai antes do bloco seguinte.
  Textos exatos nas âncoras `tela:` do Anexo A. Nada de símbolo matemático dentro de `txt()`: se a dica tiver Δp, use MathTex só para o símbolo.
- **Transições entre capítulos:** fade curto (~0,4 s) em vez de corte seco entre lotes.
- Cores do padrão de Mecânica (sem mudança). Corrigir os pendentes do v1 que continuam no vídeo (nenhum do C11, que saiu).

## 4. A pessoa: manequim articulado em Three.js (hook H1–H3 e fundo do E4-1)
Trocar o stick figure por um **manequim de desenho** (boneco articulado de artista), em aço `#7A8696` com juntas `#B8C4DA`:
- Proporção ~7,5 cabeças; cabeça oval, pescoço, tronco em dois segmentos (tórax e pelve), braços e pernas em cápsulas com esferas nas
  juntas (ombro, cotovelo, punho, quadril, joelho, tornozelo), pés em bloco arredondado. Material com `envMapIntensity` baixo e sombra
  de contato suave no chão.
- Muro de concreto (2,5 m, com cota `GEO` do Manim por cima), chão plano escuro com leve reflexo, fundo `#050816`.
- **Cinemática** (tudo função do quadro, curvas suaves 3u² − 2u³ ou mola amortecida):
  - Queda livre real: h = 2,5 m, ~0,71 s; corpo levemente inclinado para a frente, braços abrindo.
  - **Pernas duras:** contato → parada em ~0,01 s (2 quadros a 30 fps), tremor curto do corpo, sem flexão de joelho.
  - **Joelhos:** contato → o quadril desce 0,5 m em ~0,14 s com desaceleração constante, joelhos até ~90°, tronco inclina, braços à frente.
    Use cinemática inversa simples de 2 segmentos (coxa e canela) com o pé fixo no chão.
- H3: as duas aterrissagens lado a lado (dois manequins, câmera abrindo). No E4-1, o mesmo cenário recuado (`realce_3d`) enquanto o
  Manim põe os números.
- Câmera 3/4 baixa, fov ~30°. Alinhamento com o Manim só onde houver rótulo preso ao corpo (cota do muro): conferir com `qa/alinhamento.js`.
- **Plano B** se o manequim travar: silhueta 2D **preenchida**, com cápsulas arredondadas para tronco, coxa, canela e braços, mais cabeça e
  mãos, e a mesma cinemática. Nunca linhas. Reporte se usar o plano B.

**A pulga (E5):** ícone 2D preenchido em aço, de perfil, com o par de patas traseiras articulado (as patas esticam 1 mm no zoom). Mesmo cuidado.

## 5. Álgebra animada (pedido do Kaio: mais álgebra visível)
- T1: tabela antes/depois montada linha a linha, total em magenta piscando quando bate.
- T3: cadeia Δp⃗₁ = −Δp⃗₂ → ÷Δt → limite → força, por `TransformMatchingTex`; o Δt atravessando com `TransformByGlyphMap`.
- T5: Riemann (4 → 8 → 32) + Σ → ∫ + cancelamento do dt.
- T6: K = ½mv² e p = mv → K = p²/(2m) por substituição (v = p/m entrando no lugar de v).
- E3: retângulos de Riemann antes da primitiva.
- E4 e E5: os dois caminhos lado a lado, com as duas contas chegando ao mesmo número (o número final pisca nos dois painéis ao mesmo tempo).
- Sem índices de debug do MF-Tools no render.

## 6. Render mínimo e QA
- Preview 960×540 / 15 fps por lotes; o completo só no fim. Three.js primeiro em quadros soltos (manequim: contato, meio do agachamento,
  fim), depois o trecho inteiro.
- Stills 1920×1080: H3 (os dois manequins), T1-4 (tabela), T5-4 (Riemann → integral), T6-1 (dois painéis), E4-4 (dois caminhos).
- QA: áreas iguais (T5-5, E4-2) medidas e reportadas; números da §2 conferidos no código; capítulos exatamente como na §3; nenhuma sobreposição
  (rodar a auditoria do v1); header legível sobre o 3D; alinhamento 3D × Manim ≤ 2 px; mesmo número de quadros nas camadas.

## 7. Parada e relatório
Pare com o preview v2 completo. Relatório (AGENTS.md): arquivos alterados e criados, o que foi para `_reservado_yt0016/`, renders e
caminhos, áreas medidas, alinhamento e tempo do Three.js, manequim (3D ou plano B), Teste do arsenal, pendências e diferenças desta
especificação. Sem commit nem push.
