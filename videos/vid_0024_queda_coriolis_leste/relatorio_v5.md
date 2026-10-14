# V5 — reconstrução causal de Coriolis

Escopo: preview silencioso da unidade 0024, EP. 06. Sem mudança de template ou dependências.

## Decisões e lifecycle

| Transição | Permanece / transforma | Sai |
|---|---|---|
| Torre → Terra | Bola vira o ponto do laboratório no equador | Torre, chão, vertical e pergunta |
| Terra → corte equatorial | Equador vira superfície; ponto vira marca no chão | Meridianos, paralelos, eixo, polos e selo |
| Corte → queda vista do espaço | Superfície, raio, torre, bola e ponto do chão | Construção dos arcos e velocidades tangenciais |
| Espaço → Terra | Mesma dinâmica; ângulo da Terra subtraído da projeção de todos os objetos | Momento angular e vetor de gravidade |
| Corte → haste | Direção radial vira haste; ponto vira pivô | Círculo terrestre, rastro, torre simplificada e textos conceituais |
| Haste → torre local | Haste vira estrutura; fórmula vetorial sobe | Conta, eixos do espaço, vetores e demonstração escalar |
| Queda → integrações | Torre, trajetória, ponto de impacto e eixos locais | Vetores dinâmicos e labels da queda |
| Resultado → escala real | Mesmo tempo físico e mesma curva; fator visual S → 1 | Equações numéricas e selo de exagero |
| Inset → fechamento | Torre e trajetória em baixa opacidade | Ampliação e callout |

## Mudanças conceituais e visuais

- A motivação antecede a haste: mesma rotação, arcos e velocidades lineares diferentes; repouso relativo; queda com conservação aproximada de momento angular; câmera passa a acompanhar a Terra.
- O corte equatorial usa `r² phi_dot = constante` para a bola e o mesmo ângulo de câmera para chão, torre, bola e história da trajetória. A altura nesse corte é exagerada e identificada.
- Coriolis e seus ingredientes são apresentados antes da derivação, sem antecipar a fórmula.
- A haste isola duas contribuições: mudança do módulo tangencial e da direção da velocidade relativa.
- O produto vetorial vem da perpendicularidade; a mudança de referencial precede a inversão da aceleração e a origem visual do sinal negativo.
- Um único tempo governa a queda local, com setas limitadas a 0,62 e 0,56 unidades de cena. A seta vertical também é limitada pela distância restante ao chão; os vetores deixam de aparecer no impacto.
- Altura e gravidade entram em slots isolados do radical. As três substituições numéricas são sequenciais, sem duas animações concorrentes sobre o mesmo destino.
- A primeira integral mostra o cancelamento dos dois fatores 2. A escala real e o inset permanecem ligados ao mesmo impacto.

## MF-Tools

`TransformByGlyphMap` é usado somente na fusão `omega u + omega u → 2 omega u`. As demais transformações algébricas usam `TransformMatchingTex`; substituições físicas usam cópias congeladas das fontes. O cancelamento na integral usa traços sobre os dois fatores antes da simplificação.

## Validação e render

- `py_compile`: aprovado.
- Construção completa com `manim -s`: aprovada após corrigir o acento em `v_chão` e o isolamento de `50` no radical.
- Comando de render: `uv run --no-sync python -m manim -r 540,960 --fps 15 videos/vid_0024_queda_coriolis_leste/cena.py QuedaCoriolis024`.
- Ambiente: `UV_CACHE_DIR` local em `.uv-cache`; MiKTeX existente, sem instalação ou atualização.
- Prévia: `media_v5/videos/cena/960p15/QuedaCoriolis024.mp4`.
- QA e duração efetiva: preencher após inspeção do MP4.

## Precisão e limites do modelo

Dinâmica local em primeira ordem na rotação terrestre, gravidade uniforme, Equador, sem arrasto. O corte inicial é uma visualização de motivação com h/R exagerado; o cálculo final usa 50 m.

O payoff `0,77 cm` foi preservado conforme o briefing. O resultado interno é aproximadamente `0,776 cm`; `0,77` corresponde a truncamento, enquanto o arredondamento a duas casas seria `0,78 cm`. A expressão numérica mostra `3,19…` para indicar que o cálculo utiliza o tempo de queda sem arredondamento intermediário.

Teste do arsenal: nenhum sólido Blender, conforme handoff; a geometria desta unidade é vetorial Manim 2D/2.5D.

## Arquivos

- `cena.py`: V5.
- `cena_v4_preservada.py`: snapshot integral da implementação anterior.
- `ficha.md`: fase e cadeia conceitual atualizadas.
- `revisar_v5.py`: extração de checkpoints, amostras intermediárias e 19 frames.
- `relatorio_v5.md`: este relatório.
- Artefatos de render e QA em `media_v5/`, `qa_v5/`, `qa_v5_timestamps.json` e logs locais.
