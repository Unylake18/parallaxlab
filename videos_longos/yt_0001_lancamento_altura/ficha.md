# yt_0001 — lançamento de projétil a partir de uma altura

## Estado

Pauta aprovada para desenvolvimento editorial.

Conteúdo matemático/físico: **AINDA NÃO CONGELADO PARA IMPLEMENTAÇÃO.**

Não implementar `cena.py` antes de receber briefing fechado de Produção/Master.

## Formato

- formato: `longo_horizontal`
- natureza: `exercicio_resolvido`
- destino principal: YouTube
- proporção: 16:9
- preview: 960×540 / 15 fps
- final planejado: 1920×1080 / 30 fps
- duracao_alvo: 8–10 min (inicial)

## Organização

- macroassunto: Mecânica (`mecanica`)
- modulo: Movimento em duas dimensões (`movimento_2d`)

## Título de trabalho

“Por que o lançamento ótimo de uma altura não é a 45°?”

Título provisório. Não tratar como título final de publicação.

## Pergunta central

Para um projétil lançado com velocidade inicial fixa a partir de uma altura acima do solo:

- qual ângulo maximiza o alcance horizontal?
- por que o resultado deixa de ser 45°?
- existe uma curva que delimita todos os pontos que podem ser atingidos?

## Payoff planejado

trajetória → alcance → otimização → família de trajetórias → região alcançável →
envoltória / parábola de segurança.

O espectador deve ver que a otimização de uma trajetória específica e a geometria da família
inteira de trajetórias são duas perspectivas do mesmo problema.

## Linguagem visual desejada

Manim-first. Muito visual. Explorar especialmente:

- projétil real animado;
- família de parábolas;
- vetor velocidade inicial;
- altura inicial;
- alcance no solo;
- variação contínua do ângulo;
- gráfico/função sincronizado quando útil;
- equações transformando em vez de empilhar estados;
- família de trajetórias aparecendo progressivamente;
- surgimento visual da fronteira da região alcançável;
- tangência como payoff geométrico;
- objeto físico ↔ equação ↔ gráfico/geometria sincronizados.

O horizontal deve aproveitar o espaço lateral. Preferir objeto físico de um lado e construção
matemática do outro, quando isso melhorar a compreensão. Não usar 16:9 para simplesmente
adicionar mais informação.

## Identidade

Identidade Parallax Lab aprovada (`docs/identidade_visual.md`, `docs/formatos.md`):

- fundo `#050816`
- ciano `#35D9FF`
- azul `#267BFF`
- violeta `#745CFF`
- magenta `#EA63FF`
- branco `#F5F7FF`

Texto de animação conforme helpers vigentes (`template/fonts.py`); matemática em MathTex.
Configuração: `template/config_horizontal.py` e, se útil, `template/layout_horizontal.py`.

Estilo: científico, elegante, cósmico sutil, premium, limpo. Evitar: gamer, infantil, escolar
genérico, excesso de brilho, dashboard carregado.

## Regra didática

Não transformar isso numa aula tradicional filmada. Mesmo com 8–10 minutos, deve haver progresso
visual frequente. O vídeo trabalha com transformações e descobertas.

Objetivo: `equação ↔ geometria ↔ fenômeno`.

## Pendência obrigatória antes de Manim

Master/Produção ainda deve:

1. resolver completamente o problema;
2. verificar hipóteses;
3. verificar unidades;
4. verificar sinais;
5. conferir limites;
6. fechar a derivação do ângulo ótimo;
7. fechar a construção da região alcançável;
8. verificar a parábola de segurança/envoltória;
9. definir roteiro;
10. definir storyboard;
11. congelar QA.

Somente depois disso esta ficha vira especificação de implementação.
