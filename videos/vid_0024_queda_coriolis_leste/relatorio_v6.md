# V6 — núcleo didático no corte equatorial

## Entrega

Preview silencioso 540×960 / 15 fps. Duração: 178,597 s (2min58,6s).

MP4: `media_v6/videos/cena/960p15/QuedaCoriolis024.mp4`.

Comando: `uv run --no-sync python -m manim -r 540,960 --fps 15 videos/vid_0024_queda_coriolis_leste/cena.py QuedaCoriolis024`.

Usado `UV_CACHE_DIR` local em `.uv-cache` e MiKTeX existente, sem alteração de ambiente.

## Mudanças didáticas

- Haste removida integralmente. O laboratório é o mesmo corte equatorial até o zoom da torre local.
- Arcos em dois raios e no mesmo intervalo produzem `ds = r dtheta`; a expressão passa pela divisão por dt e pela identificação de `dtheta/dt` com omega.
- Vetores tangenciais do topo e do chão mostram a diferença de velocidade, antes da soltura.
- A bola conserva aproximadamente momento angular, enquanto a malha terrestre possui velocidade linear menor em raios menores.
- A contribuição da bola é derivada da regra do produto em `r vphi`; a contribuição da malha vem de `vref = omega r`, usando `rdot = -u`.
- Os resultados são copiados para a diferença relativa; subtrair uma variação negativa produz duas contribuições positivas e o fator 2.
- A câmera passa a acompanhar o planeta. O solo fica fixo, marcas externas mudam de orientação e a curva relativa aponta para leste.
- A fórmula vetorial nasce das duas contribuições, da perpendicularidade e do sentido oposto ao produto vetorial nesta geometria.
- A borda do disco se transforma em chão, o raio em z, a tangente em x e o símbolo do eixo em norte entrando na tela.
- Mantidos cálculo local, integrações, 50 m, tempo de queda, substituições, escala real e ampliação conectada ao impacto.

## Mudanças visuais e lifecycle

| Etapa | Objetos persistentes / transformados | Objetos retirados |
|---|---|---|
| Globo → corte | Equador abre em círculo; vetor axial vira símbolo central; ponto do experimento vira chão | Paralelos, meridianos, polos e eixo projetado |
| Arcos → velocidade | Raio e arco alimentam a equação; ponto superior vira bola | Ghost inicial, arcos auxiliares e rótulos |
| Duas contribuições | Disco, malha, bola, raio e vetores continuam na cena | Cada cadeia algébrica sai depois de alimentar a diferença relativa |
| Espaço → Terra | Mesma posição e história da bola reexpressas na câmera girante | Rótulos de velocidade inercial após a mudança |
| Disco → torre | Superfície → chão; raio → z; tangente → x; eixo → norte; bola e marca do chão persistem | Malha, marcas externas, arco de giro e demonstração escalar |
| Payoff → escala real | Mesma curva; S converge para 1 | Valores numéricos saem antes da caixa do resultado |
| Fechamento | Torre e trajetória em opacidade 0,07 | Inset e callout |

O vetor angular violeta está sobre o eixo; o arco violeta tem rótulo próprio de sentido. As setas da queda mantêm os limites locais de comprimento e não atravessam o chão. O selo de exagero foi reduzido e usa cor secundária.

## MF-Tools e genealogia matemática

`TransformByGlyphMap` funde os dois termos `omega_T u` em `2 omega_T u`, com mapeamento explícito de omega, índice T e u. `TransformMatchingTex` permanece o padrão nas cadeias algébricas. As substituições físicas e numéricas usam cópias das fontes para slots definidos; cada destino é animado uma vez. A primeira integração marca os dois fatores 2 antes da simplificação.

## QA

- `py_compile` aprovado para cena e script de revisão.
- Construção completa com `manim -s` aprovada; pausas redistribuídas para respeitar 3 minutos.
- Render completo executado e repetido após encontrar um termo `r` residual na revisão visual.
- Correção do ghost: remoção explícita dos filhos do antigo grupo após transformar os termos individuais. A equação anterior dos arcos também sai durante a chegada de `vrot = omega r`.
- Corrigida a sobreposição do tempo de queda com o payoff: valores saem antes da caixa.
- Rótulo radial reposicionado para não disputar espaço com bola e vetores.
- Verificações do modelo: `r vphi` constante; velocidade tangencial da bola crescente; velocidade da malha decrescente; excesso relativo para leste.
- Decodificação integral do MP4; timestamps crescentes; 23 checkpoints e 90 amostras temporais de transições; seleção de 19 PNGs em `qa_v6/`.
- Conferência visual após o último render: os 23 checkpoints e as 90 amostras foram inspecionados; o termo residual foi removido e o payoff não se sobrepõe ao tempo de queda. 2.679 frames decodificados sem erro.
- A reprodução contínua pelo player não pôde ser concluída: o controle do VLC retornou `foreground window did not report a process id`, inclusive após recuperação. O navegador de revisão não alcançou o player local e Chrome não estava disponível pelo conector. A inspeção visual foi temporal, por quadros extraídos; não declarar reprodução contínua aprovada.

## Limites

- Equador, gravidade uniforme, sem arrasto, primeira ordem na rotação terrestre. A igualdade aproximada de corotação é a aproximação usada na derivação do fator 2.
- A altura do corte é exagerada e sinalizada; o cálculo local utiliza 50 m.
- Mantido o payoff aprovado `0,77 cm`. O valor interno é cerca de `0,776 cm`; `0,77` é truncamento, enquanto arredondar a duas casas produziria `0,78 cm`. O tempo numérico aparece como `3,19…` para evitar arredondamento intermediário.
- Teste do arsenal: nenhum sólido Blender, conforme briefing; geometria vetorial 2D/2.5D Manim.

## Arquivos alterados e gerados

- `cena.py`: implementação V6.
- `cena_v5_preservada.py`: snapshot integral da V5.
- `ficha.md`: fase e derivação atualizadas.
- `revisar_v6.py`: checkpoints, amostras temporais, 19 frames e auditoria de decodificação.
- `relatorio_v6.md`: este relatório.
- `media_v6/`, `qa_v6/`, `qa_v6_timestamps.json` e logs locais: artefatos do preview e QA.

Sem alteração de arquivos globais, voz, SRT, capa, master, commit ou push.
