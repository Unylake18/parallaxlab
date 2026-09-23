# Storyboard — Integral002 sincronizado

| Tempo | Conteúdo visual |
| --- | --- |
| 0–5 s | ∫ 2x cos(x²) dx. Destacar x² em ciano e 2x em magenta. |
| 5–11,2 s | x² → 2x com d/dx sobre a seta e caixas nas duas peças. |
| 11,2–15,8 s | u = x², depois du = 2x dx. Chave sob 2x dx: uma única peça. |
| 15,8–22,5 s | Chaves fixas; ∫ cos( ) preparado antes da troca; cópias curtas de u e du chegam diretamente aos seus espaços. |
| 22,5–30,9 s | ∫ cos(u) du = sin(u) + C; leitura confortável da igualdade. |
| 30,9–35,8 s | sin(u) + C → sin(x²) + C; caixa no resultado. |
| 35,8–44,4 s | Regra da cadeia no caso: d/dx sin(x²) = cos(x²) · d/dx(x²), depois d/dx(x²) = 2x e cos(x²) · 2x. As duas últimas linhas permanecem durante a entrada da verificação. |
| 42,2–50 s | Derivada de sin(x²) + C; a igualdade cos(x²) · 2x assume a explicação por volta de 44,4 s; depois 2x cos(x²). Última linha permanece na pausa da voz. |
| 50–52,7 s | Síntese: sin(x²) → 2x cos(x²) por derivada; 2x cos(x²) → sin(x²) + C por integral. |
| 52,7–69,33 s | Coda: F e F′ visíveis até 53 s; máximo perto de 63 s, descida após 63,8 s. CTA sobre o último estado. |

A narração final efetiva abre com “Essa integral parece complicada, mas tem uma
pista.” O SRT em `legenda.srt` acompanha `audio/narracao_montagem.wav`.
Os previews de QA usados na produção foram substituídos pelos dois MP4 finais.

A seta principal foi disposta verticalmente para preservar o tamanho das
fórmulas no celular. Na transformação central, apenas os rótulos são copiados
e deslocados, sem morph de glifos. As chaves permanecem fixas. A estrutura
branca do destino aparece antes, com os espaços para u e du reservados.
`TransformFromCopy` permanece somente no retorno u → x².

A coda usa apenas curvas, eixos sem ticks, duas fórmulas e uma nota curta de
sinal. Não há área, preenchimento, valores especiais nem aula paralela.
O conteúdo termina acima de y = −4,5; a faixa inferior permanece livre.

A coda sustenta a fala sobre os gráficos e o CTA final. A preparação do áudio
e a validação estão descritas em `revisao.md`.
