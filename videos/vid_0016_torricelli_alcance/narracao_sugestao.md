# vid_0016 — Narração candidata congelada (aguardando voz)

NARRAÇÃO CANDIDATA, SEM VOZ GERADA. Base: preview silencioso aprovado, 175,3 s, 540×960 / 15 fps. Versão anterior (509 palavras, mais algébrica): `narracao_sugestao_v1.md`.

Contagem por espaços, apenas do texto falado: **534 palavras**; a 2,75 palavras/s, cerca de **194 s** de fala contínua. Palavras/s não mede duração de fala: sílabas, articulação e pausas precisam ser conferidas no áudio real.

## Princípios

- A voz explica por que a passagem faz sentido; o Manim mostra como a conta acontece. Não recitar cancelamentos, “dois y igual a H” nem “um meio vezes um meio”.
- Grandezas pelo significado físico: altura total (da água), altura do furo, profundidade do furo, velocidade de saída, tempo de voo, alcance. Nada de “agá”, “ípsilon”, “ponto A/B”.
- “Na fórmula do alcance deste modelo ideal” é ressalva obrigatória: a gravidade cancela apenas aí, sem afirmar que não importa.
- Pausa curta depois de “mesmo alcance”. CTA falado: “Segue o Parallax Lab.”; `@labparallax` só na tela.
- Fluxo: gerar a voz, medir as pausas reais, só então ajustar a cena à voz e produzir o SRT. Não cravar timestamps de legenda a partir deste roteiro.

## Janelas de planejamento (preview atual) × fala estimada

| Janela (s) | Bloco | Palavras | Cena (s) | Fala a 2,75 pal/s (s) | Folga (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| 0.0–3.7 | Gancho | 10 | 3.7 | 3.6 | +0.1 |
| 3.7–10.1 | Pergunta central e geometria | 53 | 6.4 | 19.3 | -12.9 |
| 10.1–42.0 | Bernoulli e Torricelli | 84 | 31.9 | 30.5 | +1.4 |
| 42.0–62.5 | Tempo de voo | 67 | 20.5 | 24.4 | -3.9 |
| 62.5–86.5 | Conflito físico | 50 | 24.0 | 18.2 | +5.8 |
| 86.5–102.2 | Alcance | 57 | 15.7 | 20.7 | -5.0 |
| 102.3–114.5 | Normalização | 33 | 12.2 | 12.0 | +0.2 |
| 114.5–143.0 | Gráfico e retorno ao gancho | 55 | 28.5 | 20.0 | +8.5 |
| 143.0–168.0 | De onde vem o máximo | 93 | 25.0 | 33.8 | -8.8 |
| 168.0–175.3 | Payoff e CTA | 32 | 7.3 | 11.6 | -4.3 |

Folga negativa = a cena precisa de respiro extra (ou o texto, de corte) naquele bloco; folga positiva = a cena pode ser enxugada ou a voz pode respirar.

## Texto falado por bloco

**1 · Gancho · 0.0–3.7 s**

O furo mais baixo faz o jato ir mais longe?

**2 · Pergunta central e geometria · 3.7–10.1 s**

Se eu posso escolher a altura do furo, onde fica o maior alcance? Vamos chamar de altura total a distância entre a superfície da água e o chão, e de altura do furo a distância entre o furo e esse mesmo plano. A profundidade do furo é o que sobra entre as duas.

**3 · Bernoulli e Torricelli · 10.1–42.0 s**

Comecemos pela velocidade de saída. Aplicamos Bernoulli entre a superfície da água e o furo. Nos dois pontos, a pressão é atmosférica. E, como o reservatório é muito mais largo que o orifício, a velocidade da superfície é praticamente zero. Com essas condições, a equação se simplifica e aparece justamente a diferença de altura entre a superfície e o furo. Essa diferença é a profundidade. Isolando a velocidade, chegamos à Lei de Torricelli: quanto maior a profundidade do furo, maior a velocidade de saída.

**4 · Tempo de voo · 42.0–62.5 s**

Só que velocidade não é tudo. O jato sai horizontalmente. Isso significa que, no instante da saída, sua velocidade vertical é zero. A partir daí, na vertical, a água simplesmente entra em queda livre e percorre a altura do furo até o chão. Com essa condição, a equação da queda nos dá o tempo de voo. Quanto menor essa altura, menos tempo a água permanece no ar.

**5 · Conflito físico · 62.5–86.5 s**

Agora aparece o conflito. Se o furo desce, sua profundidade aumenta e a água sai mais rápido. Mas a altura de queda diminui, então ela passa menos tempo no ar. Se o furo sobe, acontece o contrário: a saída fica mais lenta, mas o jato ganha mais tempo de voo.

**6 · Alcance · 86.5–102.2 s**

O alcance depende dos dois efeitos ao mesmo tempo. Como o movimento horizontal é uniforme, o alcance é a velocidade de saída multiplicada pelo tempo de voo. Substituindo as duas expressões, a gravidade cancela na fórmula do alcance deste modelo ideal. O resultado depende do produto entre a altura do furo e sua profundidade abaixo da superfície.

**7 · Normalização · 102.3–114.5 s**

Para comparar tanques de qualquer tamanho, medimos tanto a altura do furo quanto o alcance como frações da altura total da água. Assim, o gráfico deixa de depender do tamanho específico do tanque.

**8 · Gráfico e retorno ao gancho · 114.5–143.0 s**

Agora cada posição do furo gera um ponto no gráfico. Conforme o furo sobe, o alcance cresce, chega a um máximo e depois diminui. E repare num detalhe: um furo a vinte por cento da altura e outro a oitenta por cento chegam exatamente ao mesmo alcance. Então o furo mais baixo não vence automaticamente.

**9 · De onde vem o máximo · 143.0–168.0 s**

Então onde está o máximo? Na fórmula aparece o produto entre a altura do furo e sua profundidade. Esses dois comprimentos sempre somam a altura total: quando um cresce, o outro diminui. Com essa soma fixa, o produto é maior quando os dois têm o mesmo tamanho. Portanto, no máximo, a altura do furo é igual à profundidade. Cada uma vale metade da altura total. Substituindo essa metade na expressão do alcance, o resultado normalizado vale um. Ou seja: o alcance máximo é exatamente igual à altura total da água acima do chão.

**10 · Payoff e CTA · 168.0–175.3 s**

Então a resposta é: nem muito baixo, nem muito alto. O furo que lança mais longe fica exatamente no meio, entre o chão e a superfície da água. Segue o Parallax Lab.

## Texto corrido (para TTS)

O furo mais baixo faz o jato ir mais longe? Se eu posso escolher a altura do furo, onde fica o maior alcance? Vamos chamar de altura total a distância entre a superfície da água e o chão, e de altura do furo a distância entre o furo e esse mesmo plano. A profundidade do furo é o que sobra entre as duas. Comecemos pela velocidade de saída. Aplicamos Bernoulli entre a superfície da água e o furo. Nos dois pontos, a pressão é atmosférica. E, como o reservatório é muito mais largo que o orifício, a velocidade da superfície é praticamente zero. Com essas condições, a equação se simplifica e aparece justamente a diferença de altura entre a superfície e o furo. Essa diferença é a profundidade. Isolando a velocidade, chegamos à Lei de Torricelli: quanto maior a profundidade do furo, maior a velocidade de saída. Só que velocidade não é tudo. O jato sai horizontalmente. Isso significa que, no instante da saída, sua velocidade vertical é zero. A partir daí, na vertical, a água simplesmente entra em queda livre e percorre a altura do furo até o chão. Com essa condição, a equação da queda nos dá o tempo de voo. Quanto menor essa altura, menos tempo a água permanece no ar. Agora aparece o conflito. Se o furo desce, sua profundidade aumenta e a água sai mais rápido. Mas a altura de queda diminui, então ela passa menos tempo no ar. Se o furo sobe, acontece o contrário: a saída fica mais lenta, mas o jato ganha mais tempo de voo. O alcance depende dos dois efeitos ao mesmo tempo. Como o movimento horizontal é uniforme, o alcance é a velocidade de saída multiplicada pelo tempo de voo. Substituindo as duas expressões, a gravidade cancela na fórmula do alcance deste modelo ideal. O resultado depende do produto entre a altura do furo e sua profundidade abaixo da superfície. Para comparar tanques de qualquer tamanho, medimos tanto a altura do furo quanto o alcance como frações da altura total da água. Assim, o gráfico deixa de depender do tamanho específico do tanque. Agora cada posição do furo gera um ponto no gráfico. Conforme o furo sobe, o alcance cresce, chega a um máximo e depois diminui. E repare num detalhe: um furo a vinte por cento da altura e outro a oitenta por cento chegam exatamente ao mesmo alcance. Então o furo mais baixo não vence automaticamente. Então onde está o máximo? Na fórmula aparece o produto entre a altura do furo e sua profundidade. Esses dois comprimentos sempre somam a altura total: quando um cresce, o outro diminui. Com essa soma fixa, o produto é maior quando os dois têm o mesmo tamanho. Portanto, no máximo, a altura do furo é igual à profundidade. Cada uma vale metade da altura total. Substituindo essa metade na expressão do alcance, o resultado normalizado vale um. Ou seja: o alcance máximo é exatamente igual à altura total da água acima do chão. Então a resposta é: nem muito baixo, nem muito alto. O furo que lança mais longe fica exatamente no meio, entre o chão e a superfície da água. Segue o Parallax Lab.

## TEXTO CONGELADO PARA A VOZ (459 palavras, ≈167 s a 2,75 pal/s)

Versão enxugada + microcortes aprovados. A voz explica o porquê; o Manim mostra a conta. Gerar a voz, medir as pausas reais e só então ajustar a cena e produzir o SRT.

| Janela (s) | Bloco | Palavras | Cena (s) | Fala (s) | Folga (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| 0.0–3.7 | Gancho | 10 | 3.7 | 3.6 | +0.1 |
| 3.7–10.1 | Pergunta central e geometria | 22 | 6.4 | 8.0 | -1.6 |
| 10.1–42.0 | Bernoulli e Torricelli | 84 | 31.9 | 30.5 | +1.4 |
| 42.0–62.5 | Tempo de voo | 51 | 20.5 | 18.5 | +2.0 |
| 62.5–86.5 | Conflito físico | 63 | 24.0 | 22.9 | +1.1 |
| 86.5–102.2 | Alcance | 40 | 15.7 | 14.5 | +1.2 |
| 102.3–114.5 | Normalização | 33 | 12.2 | 12.0 | +0.2 |
| 114.5–143.0 | Gráfico e retorno ao gancho | 69 | 28.5 | 25.1 | +3.4 |
| 143.0–168.0 | De onde vem o máximo | 71 | 25.0 | 25.8 | -0.8 |
| 168.0–175.3 | Payoff e CTA | 16 | 7.3 | 5.8 | +1.5 |

**1 · Gancho · 0.0–3.7 s**

O furo mais baixo faz o jato ir mais longe?

**2 · Pergunta central e geometria · 3.7–10.1 s**

Qual altura do furo dá o maior alcance? A altura total vai do chão à superfície; a profundidade, do furo à superfície.

**3 · Bernoulli e Torricelli · 10.1–42.0 s**

Comecemos pela velocidade de saída. Aplicamos Bernoulli entre a superfície da água e o furo. Nos dois pontos, a pressão é atmosférica. E, como o reservatório é muito mais largo que o orifício, a velocidade da superfície é praticamente zero. Com essas condições, a equação se simplifica e aparece justamente a diferença de altura entre a superfície e o furo. Essa diferença é a profundidade. Isolando a velocidade, chegamos à Lei de Torricelli: quanto maior a profundidade do furo, maior a velocidade de saída.

**4 · Tempo de voo · 42.0–62.5 s**

O jato sai horizontalmente, então sua velocidade vertical inicial é zero. Na vertical, a água entra em queda livre, acelerada só pela gravidade, e percorre a altura do furo até o chão. Com essa condição, obtemos o tempo de voo: quanto menor essa altura, menos tempo a água fica no ar.

**5 · Conflito físico · 62.5–86.5 s**

Agora aparece o conflito. Se o furo desce, sua profundidade aumenta e a água sai mais rápido. Mas a altura de queda diminui, então ela passa menos tempo no ar. Se o furo sobe, acontece o contrário: a saída fica mais lenta, mas o jato ganha mais tempo de voo. São dois efeitos opostos, e o alcance depende dos dois ao mesmo tempo.

**6 · Alcance · 86.5–102.2 s**

Na horizontal, o movimento é uniforme: alcance é velocidade de saída vezes tempo de voo. Substituindo as duas expressões, a gravidade cancela na fórmula do alcance deste modelo ideal. Sobra o produto entre a altura do furo e sua profundidade.

**7 · Normalização · 102.3–114.5 s**

Para comparar tanques de qualquer tamanho, medimos tanto a altura do furo quanto o alcance como frações da altura total da água. Assim, o gráfico deixa de depender do tamanho específico do tanque.

**8 · Gráfico e retorno ao gancho · 114.5–143.0 s**

Agora cada posição do furo gera um ponto no gráfico: na horizontal, a altura do furo; na vertical, o alcance, os dois como frações da altura total. Conforme o furo sobe, o alcance cresce, chega a um máximo e depois diminui. Repare: um furo a vinte por cento da altura e outro a oitenta por cento chegam exatamente ao mesmo alcance. Então o furo mais baixo não vence automaticamente.

**9 · De onde vem o máximo · 143.0–168.0 s**

Então onde está o máximo? O alcance depende do produto entre a altura do furo e sua profundidade, e as duas sempre somam a altura total: se uma cresce, a outra diminui. Com soma fixa, o produto é maior quando as duas são iguais, ou seja, quando cada uma vale metade da altura total. Nesse ponto, o alcance normalizado vale um: o alcance máximo é igual à altura total da água.

**10 · Payoff e CTA · 168.0–175.3 s**

Nem muito baixo, nem muito alto: o maior alcance fica no meio. Segue o Parallax Lab.

## Texto corrido enxugado (para TTS)

O furo mais baixo faz o jato ir mais longe? Qual altura do furo dá o maior alcance? A altura total vai do chão à superfície; a profundidade, do furo à superfície. Comecemos pela velocidade de saída. Aplicamos Bernoulli entre a superfície da água e o furo. Nos dois pontos, a pressão é atmosférica. E, como o reservatório é muito mais largo que o orifício, a velocidade da superfície é praticamente zero. Com essas condições, a equação se simplifica e aparece justamente a diferença de altura entre a superfície e o furo. Essa diferença é a profundidade. Isolando a velocidade, chegamos à Lei de Torricelli: quanto maior a profundidade do furo, maior a velocidade de saída. O jato sai horizontalmente, então sua velocidade vertical inicial é zero. Na vertical, a água entra em queda livre, acelerada só pela gravidade, e percorre a altura do furo até o chão. Com essa condição, obtemos o tempo de voo: quanto menor essa altura, menos tempo a água fica no ar. Agora aparece o conflito. Se o furo desce, sua profundidade aumenta e a água sai mais rápido. Mas a altura de queda diminui, então ela passa menos tempo no ar. Se o furo sobe, acontece o contrário: a saída fica mais lenta, mas o jato ganha mais tempo de voo. São dois efeitos opostos, e o alcance depende dos dois ao mesmo tempo. Na horizontal, o movimento é uniforme: alcance é velocidade de saída vezes tempo de voo. Substituindo as duas expressões, a gravidade cancela na fórmula do alcance deste modelo ideal. Sobra o produto entre a altura do furo e sua profundidade. Para comparar tanques de qualquer tamanho, medimos tanto a altura do furo quanto o alcance como frações da altura total da água. Assim, o gráfico deixa de depender do tamanho específico do tanque. Agora cada posição do furo gera um ponto no gráfico: na horizontal, a altura do furo; na vertical, o alcance, os dois como frações da altura total. Conforme o furo sobe, o alcance cresce, chega a um máximo e depois diminui. Repare: um furo a vinte por cento da altura e outro a oitenta por cento chegam exatamente ao mesmo alcance. Então o furo mais baixo não vence automaticamente. Então onde está o máximo? O alcance depende do produto entre a altura do furo e sua profundidade, e as duas sempre somam a altura total: se uma cresce, a outra diminui. Com soma fixa, o produto é maior quando as duas são iguais, ou seja, quando cada uma vale metade da altura total. Nesse ponto, o alcance normalizado vale um: o alcance máximo é igual à altura total da água. Nem muito baixo, nem muito alto: o maior alcance fica no meio. Segue o Parallax Lab.
