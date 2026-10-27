# Narração sugerida — vid_0023 · Qual o melhor ângulo para puxar uma caixa?

Base: preview V5 (154,5 s), tempos medidos na cena. Ritmo-alvo ≈ 2,7 palavras/s. Variáveis sempre por extenso (força, ângulo, normal, peso, coeficiente de atrito), nunca "F", "N" ou "θ". Números escritos como serão falados.
Série: **EXERCÍCIO RESOLVIDO · EP. 7** (aplicar na tag no render final). Fechamento: "siga o Parallax Lab" + cartão final com **@labparallax** pequeno, em degradê padrão (a fazer antes do render final).

| Tempo (s) | Fase | Fala |
|---|---|---|
| 0,0 – 5,0 | Pergunta | Imagine que você precisa arrastar uma caixa pesada, com uma corda. Qual é o melhor ângulo para puxar? |
| 5,0 – 11,8 | Corda e ângulo | A corda puxa a caixa com uma força, formando um ângulo com o chão. Horizontal? Inclinado? Vamos descobrir. |
| 11,8 – 22,7 | Componentes | Primeiro, vamos separar essa força em duas partes: a horizontal, que puxa a caixa para a frente, e a vertical, que puxa a caixa para cima. Mudando o ângulo, muda a divisão. |
| 22,7 – 39,5 | Equilíbrio vertical | Agora, olha a vertical. O peso da caixa não muda, e ele é equilibrado pela normal, que é o empurrão do chão, mais a parte vertical da força. Ou seja: a normal é o peso menos a parte vertical. Quanto mais inclinamos a corda, menor fica a normal. |
| 39,5 – 50,3 | Limite do atrito estático | E o atrito? O atrito estático máximo é o coeficiente de atrito vezes a normal. Então, se a normal diminui, o limite do atrito estático também diminui. Mas precisamos considerar também a parte horizontal da força. |
| 50,3 – 61,1 | Limiar | No limiar de deslizamento, a parte horizontal da força é igual ao atrito estático máximo. É o momento em que a caixa está prestes a escorregar. |
| 61,1 – 64,6 | Álgebra 1 | Então, trocamos o atrito máximo pelo coeficiente de atrito vezes a normal. |
| 64,6 – 68,5 | Álgebra 2 | Lembrando: a normal é o peso menos a parte vertical. |
| 68,5 – 71,9 | Álgebra 3 | Agora, distribuímos o coeficiente nos dois termos. |
| 71,9 – 75,5 | Álgebra 4 | Depois, passamos o termo que tem a força para o lado esquerdo… |
| 75,5 – 79,1 | Álgebra 5 | …e colocamos a força em evidência. |
| 79,1 – 81,3 | Álgebra 6 | Por fim, dividimos pelo que ficou entre parênteses… |
| 81,3 – 88,1 | Resultado | …e chegamos à força necessária para cada ângulo. |
| 88,1 – 93,9 | Gráfico | Para enxergar isso, vamos ao gráfico: o ângulo na horizontal, a força necessária na vertical. |
| 93,9 – 101,7 ⏱ | Ângulo zero | Na horizontal, o ângulo é zero: cosseno um, seno zero. Com vinte quilos e coeficiente zero vírgula cinco, dá noventa e oito newtons. |
| 101,7 – 114,3 ⏱ | Curva | Agora, aumentamos o ângulo. No começo, a força necessária cai. Ao inclinar a corda, acontecem duas coisas ao mesmo tempo: a normal diminui, reduzindo o limite do atrito estático, mas uma fração menor da força fica na direção horizontal. O melhor ângulo equilibra esses dois efeitos. Por isso, puxar cada vez mais para cima não é sempre melhor: a força volta a subir. |
| 114,3 – 120,1 | Ângulo ideal | Então existe um ponto mais baixo: o ângulo ideal, de cerca de vinte e seis vírgula seis graus. |
| 120,1 – 125,5 ⏱ | Otimização 1 | Para achar esse ponto, olhamos a fórmula: o numerador permanece constante, porque massa, gravidade e coeficiente de atrito não mudam. Então, quanto maior o denominador, menor a força necessária. Por isso procuramos o máximo do denominador, para encontrar o mínimo da força. |
| 125,5 – 128,9 | Otimização 2 | No máximo do denominador, sua derivada é zero. Isso dá: seno igual a coeficiente vezes cosseno. |
| 128,9 – 131,9 | Otimização 3 | Dividindo por cosseno, aparece a tangente. |
| 131,9 – 135,7 | Otimização 4 | A tangente do ângulo ideal é igual ao coeficiente de atrito. |
| 135,7 – 139,3 | Otimização 5 | Com coeficiente zero vírgula cinco: vinte e seis vírgula seis graus. |
| 139,3 – 143,4 | Conferência (checagem interna, sem fala) | — |
| 143,5 – 146,3 | Comparação 1 | Puxando na horizontal: noventa e oito newtons. |
| 146,3 – 149,1 | Comparação 2 | No ângulo ideal: oitenta e sete vírgula sessenta e cinco newtons. |
| 149,1 – ~158 ⏱ | Conclusão | Uma redução de cerca de dez vírgula cinquenta e seis por cento na força necessária. Inclinar a corda ajuda — mas só até esse ponto. |
| ~158 – ~163 ⏱ | Cartão final | Gostou? Siga o Parallax Lab. |

⏱ = trechos que pedem ajuste de duração da cena na sincronização: "Ângulo zero" precisa de ~+1,5 s; a conclusão precisa de ~+4 s de permanência no quadro final; o cartão final (logo + @labparallax) acrescenta ~5 s. Acréscimo de aprofundamento (curva: disputa entre aliviar o apoio e perder parte horizontal; otimização: por que maximizar o denominador minimiza a força): ≈ +55 palavras na curva e ≈ +30 na otimização, que pedem ~+8 s e ~+9 s de permanência (varredura do gráfico mais lenta / pausa no mínimo e na fórmula). Soma provisória sem esse acréscimo: 154,5 + 1,5 + 4 + 5 ≈ 165 s. Os tempos acima são provisórios: a voz gravada decide os ajustes locais (preservando as operações visuais), como nos vídeos anteriores. A tela mantém 26,565° e 87,654 N; a fala usa precisão simplificada (26,6° e 87,65 N). A conferência de normal e atrito fica só na tela.

## Texto corrido (para gravação)

Imagine que você precisa arrastar uma caixa pesada, com uma corda. Qual é o melhor ângulo para puxar? A corda puxa a caixa com uma força, formando um ângulo com o chão. Horizontal? Inclinado? Vamos descobrir.

Primeiro, vamos separar essa força em duas partes: a horizontal, que puxa a caixa para a frente, e a vertical, que puxa a caixa para cima. Mudando o ângulo, muda a divisão.

Agora, olha a vertical. O peso da caixa não muda, e ele é equilibrado pela normal, que é o empurrão do chão, mais a parte vertical da força. Ou seja: a normal é o peso menos a parte vertical. Quanto mais inclinamos a corda, menor fica a normal.

E o atrito? O atrito estático máximo é o coeficiente de atrito vezes a normal. Então, se a normal diminui, o limite do atrito estático também diminui. Mas precisamos considerar também a parte horizontal da força.

No limiar de deslizamento, a parte horizontal da força é igual ao atrito estático máximo. É o momento em que a caixa está prestes a escorregar.

Então, trocamos o atrito máximo pelo coeficiente de atrito vezes a normal. Lembrando: a normal é o peso menos a parte vertical. Agora, distribuímos o coeficiente nos dois termos. Depois, passamos o termo que tem a força para o lado esquerdo… e colocamos a força em evidência. Por fim, dividimos pelo que ficou entre parênteses… e chegamos à força necessária para cada ângulo.

Para enxergar isso, vamos ao gráfico: o ângulo na horizontal, a força necessária na vertical. Na horizontal, o ângulo é zero: cosseno um, seno zero. Com vinte quilos e coeficiente zero vírgula cinco, dá noventa e oito newtons.

Agora, aumentamos o ângulo. No começo, a força necessária cai. Ao inclinar a corda, acontecem duas coisas ao mesmo tempo: a normal diminui, reduzindo o limite do atrito estático, mas uma fração menor da força fica na direção horizontal. O melhor ângulo equilibra esses dois efeitos. Por isso, puxar cada vez mais para cima não é sempre melhor: a força volta a subir. Então existe um ponto mais baixo: o ângulo ideal, de cerca de vinte e seis vírgula seis graus.

Para achar esse ponto, olhamos a fórmula: o numerador permanece constante, porque massa, gravidade e coeficiente de atrito não mudam. Então, quanto maior o denominador, menor a força necessária. Por isso procuramos o máximo do denominador, para encontrar o mínimo da força. No máximo do denominador, sua derivada é zero. Isso dá: seno igual a coeficiente vezes cosseno. Dividindo por cosseno, aparece a tangente. A tangente do ângulo ideal é igual ao coeficiente de atrito. Com coeficiente zero vírgula cinco: vinte e seis vírgula seis graus.

Puxando na horizontal: noventa e oito newtons. No ângulo ideal: oitenta e sete vírgula sessenta e cinco newtons. Uma redução de cerca de dez vírgula cinquenta e seis por cento na força necessária. Inclinar a corda ajuda — mas só até esse ponto.

Gostou? Siga o Parallax Lab.
