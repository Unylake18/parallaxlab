# Sugestão de narração para Produção — VID 20 · EP. 07

**POR TRÁS DA FÓRMULA — O que essa fórmula está somando?**

Rascunho para revisão editorial. Base: V6 silenciosa de `IntegralDuplaVolume020`,
**167,597005 segundos (2min47,6s)**, 540×960 / 15 fps. Tempos conferidos
nos frames e nos marcos do MP4 efetivo. O vídeo e sua cena não foram alterados nesta rodada.

## Proposta de ritmo

- **411 palavras**, contadas no texto por extenso que seria lido.
- Densidade sobre o vídeo inteiro: **2,45 palavras/s**,
  cerca de **147 palavras/minuto**, incluindo os respiros previstos.
- Hipótese para o orçamento de fala: **2,8–2,9 palavras/s**, com entonação conversada.
- Texto falado estimado: **141,7–146,8 s**.
- Tempo restante para pausas e leitura visual: **20,8–25,9 s**.
- Não ocupar todo o intervalo com fala. Distribuir os respiros nas trocas de ideia,
  na montagem da base, no limite e na avaliação dos resultados.

Esses tempos de fala são estimativas de texto, não uma gravação medida. A voz real
pode redistribuir as pausas. Na tabela, “pal/s da janela” divide as palavras pelo
intervalo completo; “fala estimada” usa 2,9 palavras/s; “respiro disponível” é a diferença.

## Referências locais de ritmo

Conferência do texto efetivamente usado e da duração do WAV final:

| Unidade | Palavras | Áudio medido | Palavras/s, com pausas | Situação registrada |
| --- | ---: | ---: | ---: | --- |
| VID 10 — looping | 501 | 168,236 s | 2,98 | Concluído tecnicamente; aprovação humana final pendente |
| VID 11 — adiabática | 450 | 158,160 s | 2,85 | Mesma família; concluído tecnicamente; aprovação humana final pendente |
| VID 12 — esfera não uniforme | 475 | 164,240 s | 2,89 | Vídeo final aprovado em 02/10/2026 |

O VID 12 é a referência com aprovação final explícita neste checkout. O VID 11
ajuda no tom da mesma série: a voz explica o significado e a animação mostra a conta.
As taxas históricas já incluem as pausas dos arquivos; não medem a velocidade
das palavras isoladamente. A hipótese de 2,8–2,9 para esta sugestão é um orçamento
conservador por trecho. O resultado global proposto é mais espaçado que as referências.

Fontes: `texto_narracao.txt`, `audio/narracao_final.wav` e `ficha.md` das três unidades.

## Direção de linguagem

Tom próximo, claro e paciente. Uma ideia por frase. Explicar o que a animação
está fazendo, sem ler todos os símbolos que já aparecem na tela.

| Na tela | Na fala |
| --- | --- |
| f(x,y), f(xᵢ,yⱼ) | a função; a altura da superfície naquele ponto |
| (xᵢ,yⱼ) | o ponto de referência no centro da célula |
| ΔA | a área da célula; a área da base |
| ΔxΔy | comprimento vezes largura |
| ΔV | o volume da coluna; uma pequena contribuição de volume |
| x fixo na integral interna | a posição do corte fica constante |
| y, dy na integral interna | a coordenada ao longo do corte; percorrer o corte |
| A(x) | a área da seção, que depende da posição do corte |
| dx na integral externa | uma pequena espessura; avançar na segunda direção |
| Σ | somar os volumes das colunas |
| integral dupla | o limite dessas somas sobre toda a área |

Usar “área da base”, em vez de “fração de área” sozinha, para evitar que a medida
seja confundida com uma razão numérica. “Uma pequena parte da área total” faz essa
ponte no texto. Usar “coordenada” apenas na conta, onde ela identifica uma posição,
sem pronunciar nomes de letras.

A função e os limites do quadrado permanecem escritos na tela. A voz não precisa
ditar sua fórmula: explica que a função fornece a altura em cada ponto. Não dizer
que uma malha finita já é o volume exato, nem chamar a medida de área da integral
de “quadradinho infinitamente pequeno”. A coluna tem volume exatamente igual à
área da base vezes a altura; ela aproxima a contribuição sob a superfície curva.

## Orçamento por trecho

| # | Janela no vídeo | Duração | Bloco | Palavras | Pal/s da janela | Fala estimada | Respiro disponível |
| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: |
| 1 | 0,00–5,60 s | 5,60 s | Gancho | 12 | 2,14 | 4,14 s | 1,46 s |
| 2 | 5,60–9,00 s | 3,40 s | Partição | 7 | 2,06 | 2,41 s | 0,99 s |
| 3 | 9,00–18,20 s | 9,20 s | Área da base | 22 | 2,39 | 7,59 s | 1,61 s |
| 4 | 18,20–25,20 s | 7,00 s | Ponto e altura | 18 | 2,57 | 6,21 s | 0,79 s |
| 5 | 25,20–34,13 s | 8,93 s | Volume da coluna | 22 | 2,46 | 7,59 s | 1,35 s |
| 6 | 34,13–46,20 s | 12,07 s | Soma de colunas | 29 | 2,40 | 10,00 s | 2,07 s |
| 7 | 46,20–56,93 s | 10,73 s | Refinamento e limite | 25 | 2,33 | 8,62 s | 2,11 s |
| 8 | 56,93–69,00 s | 12,07 s | Área da seção | 30 | 2,49 | 10,34 s | 1,72 s |
| 9 | 69,00–81,40 s | 12,40 s | Da seção ao volume | 31 | 2,50 | 10,69 s | 1,71 s |
| 10 | 81,40–91,40 s | 10,00 s | Duas integrações | 27 | 2,70 | 9,31 s | 0,69 s |
| 11 | 91,40–100,80 s | 9,40 s | Separação e regra de potência | 24 | 2,55 | 8,28 s | 1,12 s |
| 12 | 100,80–113,93 s | 13,13 s | Limites do corte | 32 | 2,44 | 11,03 s | 2,10 s |
| 13 | 113,93–120,93 s | 7,00 s | Simplificação da área | 16 | 2,29 | 5,52 s | 1,48 s |
| 14 | 120,93–125,73 s | 4,80 s | Interpretação da área | 11 | 2,29 | 3,79 s | 1,01 s |
| 15 | 125,73–133,13 s | 7,40 s | Substituição na integral externa | 19 | 2,57 | 6,55 s | 0,85 s |
| 16 | 133,13–141,26 s | 8,13 s | Segunda regra de potência | 19 | 2,34 | 6,55 s | 1,58 s |
| 17 | 141,26–148,60 s | 7,33 s | Limites na segunda direção | 19 | 2,59 | 6,55 s | 0,78 s |
| 18 | 148,60–154,06 s | 5,47 s | Valores nos limites | 14 | 2,56 | 4,83 s | 0,64 s |
| 19 | 154,06–160,93 s | 6,87 s | Resultado do volume | 18 | 2,62 | 6,21 s | 0,66 s |
| 20 | 160,93–167,60 s | 6,67 s | Fechamento | 16 | 2,40 | 5,52 s | 1,15 s |

## Texto sugerido, com a janela de cada bloco

**01. Gancho — 0,00–5,60 s**

O que essa fórmula está somando? Pequenos volumes, sob esta superfície curva.

**02. Partição — 5,60–9,00 s**

Dividimos a base quadrada em pequenas células.

**03. Área da base — 9,00–18,20 s**

Cada célula ocupa uma pequena parte da área total. Multiplicando seu comprimento pela largura, encontramos a área da base de uma coluna.

**04. Ponto e altura — 18,20–25,20 s**

Escolhemos o centro da célula como ponto de referência. A função informa a altura da superfície naquele ponto.

**05. Volume da coluna — 25,20–34,13 s**

A coluna sobe até essa altura. Área da base vezes altura dá seu volume: uma aproximação para a contribuição sob a superfície.

**06. Soma de colunas — 34,13–46,20 s**

Repetimos isso em todas as células. Cada coluna acompanha a altura da superfície. Os topos são planos, mas a superfície é curva. Somando os volumes, aproximamos o volume inteiro.

**07. Refinamento e limite — 46,20–56,93 s**

Refinamos a divisão. As bases diminuem, e os topos acompanham melhor a superfície. No limite, essa soma se torna a integral dupla: o volume exato.

**08. Área da seção — 56,93–69,00 s**

Para calcular, começamos com um corte vertical. Mantemos sua posição fixa e percorremos o corte entre as duas bordas. Integrando as alturas nesse percurso, encontramos a área da seção destacada.

**09. Da seção ao volume — 69,00–81,40 s**

Depois, deslocamos o corte pela base. Sua área muda a cada posição. Área vezes uma pequena espessura dá um volume. A integral externa acumula essas contribuições e encontra o volume total.

**10. Duas integrações — 81,40–91,40 s**

A conta segue essas duas etapas. Primeiro, calculamos a área do corte. Sua posição fica constante durante essa primeira integração; só a coordenada ao longo dele varia.

**11. Separação e regra de potência — 91,40–100,80 s**

A parte constante sai da integral. No termo ao quadrado, usamos a regra de potência: aumentamos o expoente para três e dividimos por três.

**12. Limites do corte — 100,80–113,93 s**

Montamos a primitiva, cuja derivada devolve a expressão inicial. Aplicamos os limites: substituímos a coordenada por um e por menos um. Subtraímos o valor do limite inferior do valor do limite superior.

**13. Simplificação da área — 113,93–120,93 s**

Subtraímos o resultado inteiro, com atenção aos sinais. Agrupamos os termos constantes e simplificamos a expressão.

**14. Interpretação da área — 120,93–125,73 s**

Encontramos a área da seção. Ela depende da posição do corte.

**15. Substituição na integral externa — 125,73–133,13 s**

Agora, integramos as áreas para obter o volume. Substituímos a área encontrada na integral externa e separamos os termos.

**16. Segunda regra de potência — 133,13–141,26 s**

A constante é multiplicada pela coordenada. O fator dois permanece; a potência aumenta para três e dividimos por três.

**17. Limites na segunda direção — 141,26–148,60 s**

Aplicamos os limites também na segunda direção. Substituímos primeiro por um e depois por menos um, como no corte.

**18. Valores nos limites — 148,60–154,06 s**

Os resultados são vinte terços e menos vinte terços. Subtraímos o segundo do primeiro.

**19. Resultado do volume — 154,06–160,93 s**

Subtrair o negativo vira soma. O volume é quarenta terços, aproximadamente treze vírgula trinta e três unidades cúbicas.

**20. Fechamento — 160,93–167,60 s**

A integral dupla soma pequenas contribuições de volume sobre toda a área. Assim, recuperamos o sólido.

## Pontos de encaixe para a revisão de Produção

- **0–5,60 s:** perguntar e responder, com um breve respiro após a pergunta.
- **16,13 s:** a área da base já está montada; deixar a multiplicação dos lados ser vista.
- **25,20–34,13 s:** ligar explicitamente a base à altura e ao volume. Não antecipar
  a soma de todas as colunas enquanto a coluna isolada ainda está sendo explicada.
- **46,20–56,93 s:** não narrar cada resolução. “No limite” deve acompanhar a passagem
  para áreas tendendo a zero, a partir de 53,33 s; “integral dupla” acompanha 55,73 s.
- **56,93–69,00 s:** posição do corte fixa; a primeira integral produz uma área.
- **69,00–81,40 s:** área vezes espessura produz uma contribuição de volume;
  a segunda integral acumula essas contribuições. Não dizer que somar áreas,
  sem considerar a espessura, já produz volume.
- **88,60 s:** a posição do corte fica constante na primeira integração.
- **97,86 s:** a regra de potência está montada; não ler as letras dos exemplos.
- **105,86 e 108,26 s:** acompanhar a substituição pelos dois valores dos limites.
  A subtração fica montada em 113,93 s. Distribuir a pausa desse bloco entre esses eventos.
- **120,93–125,73 s:** interpretar o resultado como área da seção, sem ler a expressão toda.
- **127,93–130,53 s:** a área entra na integral externa. Explicar a substituição.
- **146,26 e 148,60 s:** segunda avaliação nos limites; os dois valores simplificados
  estão completos em 151,66 s. Usar a pausa para não anunciar o segundo cedo demais.
- **158,26–160,93 s:** quarenta terços e sua aproximação. Este é um dos trechos mais
  sensíveis a palavras compridas; conferir a duração real antes da tomada completa.
- **160,93–167,60 s:** fechar com a mesma ideia da abertura. Encerrar a frase antes
  do último frame e deixar um pequeno respiro final. Não acrescentar CTA nesta sugestão.

As janelas são contínuas, mas não significam que cada frase deva começar no primeiro
frame da janela. As pausas servem também para a fala acompanhar o aparecimento dos termos.
Não aplicar uma velocidade única sem conferir esses encaixes.

Se alguma frase ficar longa na voz real, primeiro reduzir uma repetição ou redistribuir
uma pausa dentro do bloco. Os trechos finais de limites e resultado precisam de teste
de leitura. Preservar a explicação central de base × altura, o limite e área × espessura.

## Entrega desta rodada

Somente sugestão textual, orçamento de tempo e orientação para revisão. Nenhuma voz,
legenda, render ou alteração da cena foi produzida. O texto limpo, sem horários nem
instruções, está em `texto_narracao_sugestao_v6.txt`; ainda é um rascunho para Produção.
