# vid_0025 — relatório da rodada r4b (andamento, teto de 2:59)

Acréscimo de 25/10/2026 sobre o r4 abaixo. Pedido: o vídeo precisa ficar abaixo de 3 min (máximo 2:59).

- Mudança única: fator de andamento global `PACE = 0,82` na classe (`play`/`wait` escalam todo `run_time` e `wait`, com piso de 1/15 s). Nenhum estado, passo ou texto foi removido; as proporções entre cenas se mantêm.
- Preview r4b: `media/videos/cena/960p15/ArcoIris025.mp4` (cópia em `renders/preview_r4b_ArcoIris025.mp4`), 540×960, 15 fps, sem áudio, **172,99 s (2:52,99)**, 2.595 quadros. Margem de 6 s sob o teto.
- Marcas (s): C01 0 · C02 10,0 · C03 16,7 · C04 25,7 · C05 39,4 · C06 62,2 · C07 78,8 · C08 93,4 · C09 126,0 · C10 138,6 · C11 158,5 · fim 166,0.
- Pranchas: `renders/preview_r4b_prancha_01..08.png`; zip para o GPT: `renders/preview_r4b_para_gpt.zip` (2.595 quadros + MP4 + cena.py; temporário).
- Estado final de C10 conferido no quadro de 165,9 s: Sol a 47°, topo do arco = −5°, arco inteiro abaixo do horizonte.
- Consequência a revisar: os estados de C05 e C08 agora duram ~18% menos (C05 23,2 s, C08 32,6 s). A leitura da álgebra a 360×640 deve ser reavaliada; se ficar corrida, o ajuste fino é por cena (PACE maior em C05/C08 e menor em C02/C09/C10), mantendo o total sob 2:59.
- O primeiro render do r4b falhou por falta de memória (outros renders de manim em paralelo na máquina); repetido sem alteração de código.
- A duração-alvo de 180–190 s do handoff foi substituída pelo teto de 2:59 pedido pelo usuário; a voz terá de caber nessa duração (a narração congelada tem ~180–190 s).

---

# vid_0025 — relatório da rodada r4 (clareza visual e construção matemática)

Data: 24/10/2026. Fase: preview silencioso. Sem voz, SRT, master, capa, publicação, commit ou push.

## Preview r4

- Arquivo: `videos/vid_0025_arco_iris/media/videos/cena/960p15/ArcoIris025.mp4` (cópia em `renders/preview_r4_ArcoIris025.mp4`).
- 540×960, 15 fps, sem áudio, **211,3 s** (3.169 quadros). Classe `ArcoIris025`.
- Marcas de estado (s): C01 0 · C02 12,5 · C03 20,9 · C04 32,2 · C05 49,1 · C06 77,7 · C07 98,2 · C08 116,4 · C09 158,2 · C10 174,3 · C11 199,1 · fim 208,6 (+ espera final).
- Duração acima do alvo de 180–190 s. Onde foi o tempo: C05 (28,6 s; orçamento 23) e C08 (41,8 s; orçamento 35) ganharam os estados pedidos (três viradas, agrupamento, distribuição de sinal; cadeia de derivação sem salto); C10 (24,9 s) carrega a geratriz percorrendo o cone, o giro e os dois estados do Sol. Esperas já foram enxugadas (nenhuma acima de 1,2 s). Reduzir mais exigiria cortar estados de C05/C08 — decisão devolvida à edição.
- Pranchas de comprovação: `renders/preview_r4_prancha_01..07.png`. Zip para avaliação: `renders/preview_r4_para_gpt.zip` (todos os quadros + MP4 + cena.py; temporário).

## Arquivos

- `cena.py` — classe reescrita (helpers ópticos preservados; `.absolute()` mantido). Novos helpers: `morph` (correspondência explícita de termos), `travel` (marcador de propagação qualitativo), `tick_mark`, `sky_geometry` (esquema lateral coerente).
- `ficha.md` — registro factual do preview r4.
- `relatorio_r4.md` — este arquivo.

## O que mudou, por cena

- **C01** — pergunta e 42° entram em 0–1 s. Geometria lateral corrigida: `A = E + L·a` (sombra da cabeça no solo), `T = A + L·tan θmáx·u`; abertura medida pelos vetores do desenho = **42,078107°**; elevação da linha de visão = 22,078° (θmáx − h, h = 20°). Luz gota → olho (seta) distinta da linha de visão (tracejada). Arco colorido só numa vista de frente identificada, à parte do esquema lateral. Observador maior, rótulos maiores. Saída: anel na gota escolhida, linha de visão mantida parte da aproximação, zoom da mesma gota (rotação +h nivela a incidência; saída da gota apontando exatamente para o olho, desvio 0,0000°).
- **C02** — b como distância perpendicular do eixo (com pulso), R como raio (vertical, para comparar), `b/R = 0,86` nasce de cópias de b e R; nota curta de hipóteses no subtítulo; R e medidas recuam antes de C03.
- **C03** — marcador percorre o raio até o ponto; normal → i → refração (corda) → r; Snell nasce dos dois rótulos (cópias sequenciais), símbolos maiores (52 pt); a equação recolhe para posição secundária.
- **C04** — triângulo com os dois lados R marcados (ticks + R, R); r copiado da entrada para a reflexão; ângulo refletido; saída com r interno e i recuperado por cópia; construções antigas recuam a 22 %.
- **C05** — três eventos: direção anterior prolongada (tracejada, ancorada na interface real), arco de virada com seta, rótulo; cópia sequencial para `D = (i−r) + (180°−2r) + (i−r)`. Estados `D = 180° + (i+i) − (r+2r+r)` → `D = 180° + 2i − 4r` com transporte de termos. Paralela ao raio incidente, D e θ suplementares; `θ = 180° − D` → substituição → `θ = 180° − 180° − 2i + 4r` (sinal distribuído, nota) → cancelamento riscado → `θ = 4r − 2i`.
- **C06** — gota existente transformada (escala/posição) em vez de apagada; raio central separado; eixo b/R ligado à razão de C02; varredura com guia móvel de b + valor; três momentos (cresce / achata / cai) com desaceleração perto do máximo; 25 raios em sucessão, ponto aparece quando o raio chega à saída.
- **C07** — gráfico recua ao canto; cinco amostras selecionadas em sequência com seus pontos; halo só nas saídas; detalhe das direções de saída com origem comum, ângulos ampliados ×10 (declarado), janela [θmáx−1°, θmáx] sombreada; contagem por 1° de saída em marcas contáveis (bins ancorados em θmáx; janela destacada: 5); "5 de 25" → "≈ um em cada cinco" + "raios no modelo geométrico"; teto `θ ≤ 42,1°` identificado como "para n = 1,333".
- **C08** — ponte `sen i = b/R`; `θ = 4r − 2i` → `dθ/di = 4 dr/di − 2 = 0` → `dr/di = 1/2`; Snell → `cos i = n cos r · dr/di` → o 1/2 é copiado para o fator → `cos i = (n/2) cos r`; `4cos²i = n²cos²r` → `n²(1 − sen²r)` → `n² − n²sen²r` → `n² − sen²i` (cancelamento do n² indicado) → `n² − 1 + cos²i` → `3cos²i = n² − 1` → `cos²i = (n²−1)/3`. Números: `cos²i = (1,333²−1)/3 = 0,259` → `i = 59,4°` → Snell → `r = 40,2°` → valores copiados em `θ = 4r − 2i` → `θ = 42,1°` (calculado com os valores internos: 42,078°, não 4×40,2 − 2×59,4 = 42,0). Marcador 0,861 separado de b/R.
- **C09** — transição vinculada (o θ = 42,1° vira o rótulo do ângulo de saída na gota); componentes uma de cada vez; detalhe ×10 das duas direções; gráfico com recorte de exibição em 36° (intervalos de b/R calculados por bissecção; nenhum valor achatado); máximos marcados com ponto e rótulo grande; mini-arco (vermelho fora, violeta dentro) preservado na entrada de C10.
- **C10** — gota representativa, luz gota → olho vs. linha de visão; meia-abertura 42° medida na vista lateral; geratriz percorre o cone deixando rastro; anel; giro com textos curtos ("vista lateral" → "girando" → "vista ao longo do eixo") por fades, sem deformar frases; eixo/vértice visíveis durante o giro; ponto antissolar rotulado; Sol retirado do céu e posto num indicador de altura à esquerda (0–60°, marca em 42°); horizonte fixo; Sol 20° → 34° (arco menor) → 47° (abaixo), limiar interno θmáx exato; leitura "42° − altura do Sol".
- **C11** — recuperação curta da altura (1,2 s); cadeia gota (raios amontoados) → máximo → círculo; raio angular 42° identificado como distância angular no céu; CTA maior.

## Verificação direcionada

1. Gancho: abertura pelos vetores do desenho = 42,078107° (= θmáx); direção luz gota → olho = direção T→E (0,0000° de desvio). ✔
2. Núcleo óptico preservado (helpers idênticos ao r3; verificação do r3 vale: Snell, centro, rasante, reflexão, pontos na circunferência). ✔
3. Janela [θmáx−1°, θmáx] = [41,078°, 42,078°]: amostras 17–21, exatamente 5; N = 25 com peso em área (b_k/R = √((k−½)/25)); o detalhe ×10 só transporta direções, não altera a contagem. Contagem por 1° a partir de θmáx: [5, 3, 1, 2, 0, 1, 1, 1, 1, 1, 0, 1, 0, 2, 0, 1] + 5 abaixo de 26° = 25. ✔
4. Máximos: vermelho 42,3698° (tela 42,4°), violeta 40,6459° (tela 40,6°); bandas vermelho fora / violeta dentro em C09, C10 e C11; curvas recortadas por intervalo de b/R, sem trechos horizontais falsos. ✔
5. Limiar: arco acima do horizonte ⇔ tan h < tan θmáx (h = 42,000° ainda acima; 42,078° some); sinal de θmáx − h correto nos estados 20° (+22°), 34° (+8°), 47° (−5°). ✔

Conferência visual (pranchas r4): 42° correto no gancho e pergunta cedo; continuidade da gota no zoom; três viradas e soma sequencial; sinal distribuído visível; cinco saídas agrupadas na janela ampliada; contagem legível; Snell derivado com dr/di; quadrado → fator 3 sem salto; dois picos de cor; cone com eixo/vértice; textos sem deformação; vista frontal com indicador solar separado; faixa inferior livre (nada abaixo de −5,5); sem debug.

## Pendências reais

- **Duração 211 s** vs. alvo 180–190 s (ver acima). Cortes adicionais implicam remover estados de C05/C08 ou acelerar operações; decisão editorial.
- **C07, ~104–107 s**: o detalhe ×10 cabe, mas a cunha de 1° (10° ampliados) ainda é estreita a 360×640; se precisar, ampliar para ×20 declarado.
- **C05, ~52 s**: o rótulo "i − r" da primeira virada fica próximo do "i" recuado; legível, mas apertado.
- **C09, ~166 s**: os dois trajetos quase coincidem na gota (diferença real de 1,7°); a comparação depende do detalhe ×10 e do zoom do gráfico, como previsto.
- Marcas "ESTADO" são impressas no log de render; não há texto de debug na tela.

Teste do arsenal: não se aplica (solido_3d: nenhum).
