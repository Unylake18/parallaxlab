# Por que uma carga faz uma hélice?

- ID: `vid_0024`
- Série pública: **DA EQUAÇÃO AO FENÔMENO · EP. 06** (confirmado pelo usuário em 18/10/2026)
- formato: `curto_vertical`
- solido_3d: nenhum — Manim 2.5D aprovado para esta implementação.
- Subtítulo: campo magnético uniforme
- Fase: preview visual completo, sem áudio, 540×960 / 15 fps.
- Física e storyboard: handoff de Produção recebido em 15/10/2026, blocos A–G.
- Sem exemplo numérico. End card silencioso aprovado: somente `@labparallax`.

## Implementação

Geometria em coordenadas 3D, com B no eixo z e projeção linear fixa no
frame (mesma abordagem 2.5D do vid_0020). A vista transversal é uma mudança
didática localizada da projeção, sem câmera orbital. Vetores são projetados
pela mesma transformação linear; o paralelogramo fecha exatamente.

Preview previsto: `media/videos/cena/960p15/CargaHelice024.mp4`, dentro desta unidade.

## Teste do arsenal

Não utilizado: decisão explícita do briefing por Manim 2.5D. Resolução do
preview: 540×960. Sem ativos, caches ou custo de integração do arsenal.

## Refinamento do preview — 15/10/2026

Comparação entre sinais com posição e vetor velocidade iniciais comuns;
reinícios explícitos entre condições; gráficos sincronizados de v_x e F_x
em t/T; cancelamento algébrico visível; orientação de B na vista transversal;
marcação de uma volta, T e p; comparações geométricas seguidas de execuções
no mesmo intervalo físico. Soma vetorial e síntese final corrigidas.

Novo preview: `media_refinado/videos/cena/960p15/CargaHelice024.mp4`.
Preview anterior e pacote temporário de análise preservados.

## Polimento visual/animação — 15/10/2026

Campo em dez vetores com três profundidades e brilho discreto; trajetória luminosa;
transições contínuas; álgebra com TransformByGlyphMap; construção de omega_c e T;
parâmetros retornando ao baseline; inversão visual da força antes da curvatura;
síntese recomposta e end card somente com @labparallax.

Preview desta rodada: `media_polimento/videos/cena/960p15/CargaHelice024.mp4`.
Previews e pacotes anteriores preservados.

## Layout, legibilidade e ritmo — continuidade em 17/10/2026

Preview atual: `media_layout_ritmo/videos/cena/960p15/CargaHelice024.mp4`.
540×960 / 15 fps, 176,6 s, 2.649 quadros, sem áudio.
Código, briefings, MP4 e resultados de QA preparados para continuidade no Git.
Instruções e estado completo: `CONTINUAR_AQUI.md`. Frames e ZIPs ficam somente locais.
