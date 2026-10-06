# yt_0002 — Como a energia potencial permite prever o movimento?

## Estado

Pauta aprovada para desenvolvimento editorial.

Física, matemática, roteiro e storyboard **ainda não estão congelados para implementação**.

Não criar `cena.py` antes do briefing fechado de Produção/Master.

## Classificação

- formato: `longo_horizontal`
- curso/eixo: Física I
- macroassunto: Mecânica
- modulo: Energia potencial e conservação
- natureza: `teoria_visual`
- destino principal: YouTube
- duracao_alvo: 8–10 min (inicial)
- proporção: 16:9
- preview: 960×540 / 15 fps
- final planejado: 1920×1080 / 30 fps

## Título de trabalho

**Como a energia potencial permite prever o movimento?**

Título provisório, não título final de publicação.

## Pergunta central

Como podemos prever qualitativamente o movimento de uma partícula conhecendo o gráfico de sua
energia potencial, sem precisar resolver explicitamente `x(t)`?

## Ideias centrais planejadas

Construir visualmente as relações:

- `F(x) = -dU/dx`
- `E = K + U`
- `K = E - U`
- `K >= 0`

portanto:

- `U(x) <= E`

A partir disso, mostrar como identificar:

- regiões permitidas e proibidas;
- pontos de retorno;
- sentido qualitativo da força;
- mínimos e máximos do potencial;
- equilíbrio;
- estabilidade;
- barreiras de potencial;
- movimento confinado e travessia de barreiras.

## Direção didática

Este vídeo deve funcionar como vídeo-âncora do módulo.

Não é uma versão estendida do `vid_0013`.

Usar diferentes potenciais simples para construir o conceito geral. O poço duplo pode aparecer
como exemplo ou consequência, mas não deve dominar o vídeo nem transformar o longo numa repetição
do `vid_0013`.

A ideia central é: **o formato de `U(x)` permite prever uma classe inteira de movimentos sem
resolver `x(t)`.**

## Linguagem visual

Manim-first. Explorar especialmente:

- partícula em um eixo;
- gráfico `U(x)` sincronizado ao movimento;
- linha horizontal de energia total;
- `K = E - U` mudando visualmente;
- regiões permitidas aparecendo no gráfico;
- pontos de retorno;
- setas de força coerentes com `-dU/dx`;
- mínimo estável;
- máximo instável;
- comparação entre diferentes formatos de potencial;
- transformações visuais entre equação, gráfico e fenômeno.

Aplicar a regra: `equação ↔ gráfico ↔ fenômeno`.

Preferir uma representação dominante ou duas sincronizadas. Não criar dashboard permanente com
muitos painéis.

## Pré-requisitos

Planejados:

- energia cinética;
- ideia básica de conservação de energia;
- derivada como inclinação.

Não assumir conhecimento prévio de análise de potenciais.

## Payoff principal

Ao final, o espectador deve conseguir olhar para um gráfico `U(x)` e responder, qualitativamente:

- onde a partícula pode estar;
- onde ela para e retorna;
- para que lado tende a acelerar;
- quais equilíbrios são estáveis;
- se consegue atravessar uma barreira;
- se o movimento fica preso em uma região.

## Posição na biblioteca

`Física I → Mecânica → Energia potencial e conservação → teoria_visual`
(`docs/mapa_curricular.md`, seção 4.8).

Este é um vídeo-âncora do módulo.

Vídeos futuros relacionados podem incluir:

- construção de `U(x)` a partir de `F(x)`;
- conservação de energia;
- poço duplo;
- pequenas oscilações perto de um mínimo;
- exercícios de barreira e pontos de retorno.

Esses vídeos futuros são contexto editorial, não backlog obrigatório desta unidade.

## Pendência antes da implementação

Master/Produção ainda deve:

1. definir exatamente a sequência conceitual;
2. escolher os potenciais usados como exemplos;
3. resolver/verificar toda a física;
4. definir hipóteses;
5. checar sinais e unidades;
6. definir limites e casos especiais;
7. fechar roteiro;
8. fechar storyboard;
9. congelar QA.

Até isso acontecer: não implementar a cena.
