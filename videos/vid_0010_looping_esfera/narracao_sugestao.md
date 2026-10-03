# vid_0010 — sugestão de narração (rascunho para revisar com o GPT)

EXERCÍCIO RESOLVIDO · EP. 04. Preview silencioso de 168,1 s. Tom e ritmo seguem os vídeos 7, 8 e 9:
frases curtas, conectivos ("agora", "então", "só que", "falta"), uma ideia por frase, grandezas ditas por
extenso, resultados repetidos em palavras. Fecha com "Se curtiu, siga o Parallax Lab."

## Como falar as grandezas (nada de letras soltas)

| Na tela | Na fala |
|---|---|
| R | **raio do looping** (1ª vez: "medido até o centro da partícula") |
| a | **raio da esfera** |
| h | **altura inicial** |
| m, g | **massa**, **gravidade** |
| v, v_top | **velocidade**, **velocidade no topo** |
| ω | **velocidade angular** |
| I_CM | **momento de inércia** |
| N, mg | **força normal**, **peso** |
| ρ | **densidade** |
| x | **distância ao centro** |
| dx, dm, dI | **espessura**, **massa do disco**, **momento de inércia do disco** |
| K, U | **energia cinética**, **energia potencial** |
| 2,5R / 2,7R | **dois e meio vezes o raio** / **dois vírgula sete vezes o raio** |
| 5/2, 7/10, 27/10, 2/5 | **cinco meios**, **sete décimos**, **vinte e sete décimos**, **dois quintos** |

Cuidado: R (do looping) e a (da esfera) são raios diferentes. Dizer sempre "raio do looping" e "raio da esfera".

## Narração por bloco

Os tempos são os do preview; a voz vai ajustar a cena por âncoras (como nos vídeos 8 e 9). `[...]` = trecho
cortável se a voz ficar longa demais para o bloco.

**1. Pergunta e caso base (0–6,9 s)**
Tela: pista com `h = ?`; a esfera vira partícula; a partícula repete a descida.
> Qual é a altura mínima para uma esfera completar um looping? Pra descobrir, a gente começa pelo caso clássico: uma partícula.

**2. O topo do looping (6,9–20,3 s)**
Tela: zoom no topo; peso, normal e velocidade; equação; `N ≥ 0`; `N = 0`; velocidade no topo ao quadrado = gravidade vezes raio.
> No topo, o peso e a força normal apontam para o centro e, juntos, valem a massa vezes a velocidade ao quadrado, sobre o raio do looping, medido até o centro da partícula. Como a pista só empurra, a normal não pode ser negativa. No limite, ela é zero, e a velocidade no topo ao quadrado é a gravidade vezes o raio.

**3. Altura mínima da partícula (20,3–42,7 s)**
Tela: conservação de energia; troca da velocidade ao quadrado por gravidade vezes raio; cortes; cinco meios; `2,5R` (só aqui aparece pela primeira vez); a partícula faz a corrida completa (a partir de ~35 s).
> Agora a energia. No início, ela é toda potencial: massa, gravidade e altura. No topo, a partícula está a duas vezes o raio de altura e ainda tem energia cinética. Troca a velocidade ao quadrado por gravidade vezes raio, corta massa e gravidade, e junta os termos: dois mais meio dá cinco meios.
> *(corrida)* Ou seja, a altura mínima é dois e meio vezes o raio. Soltando daí, a partícula completa o looping.

**4. Agora, a esfera (42,7–53,5 s)**
Tela: zoom no topo com a esfera; "a condição no topo muda?"; mesma caixa da velocidade no topo.
> Agora, a esfera. Será que a condição no topo muda? Não: o peso e a normal continuam iguais, então a velocidade mínima no topo é a mesma.

**5. O que muda na energia (53,5–60,5 s)**
Tela: energia cinética = translação + rotação; fica em aberto o momento de inércia (`I_CM = ?`).
> O que muda é a energia: a esfera também gira, e isso soma uma energia cinética de rotação, que depende do momento de inércia. Mas quanto ele vale?

**6. Qual é o momento de inércia da esfera (60,5–106,9 s)** — o bloco mais apertado
Tela: esfera cortada em discos; um disco; triângulo (raio da esfera, distância, raio do disco); massa do disco; momento de inércia do disco; quadrado; soma de todos os discos; integral; massa da esfera isolando a densidade; cancelamentos; resultado.
> Vamos descobrir. Corta a esfera, homogênea, em discos finos e olha um deles, a certa distância do centro. O raio da esfera, essa distância e o raio do disco formam um triângulo retângulo, então o raio do disco ao quadrado é o raio da esfera ao quadrado menos a distância ao quadrado.
> A massa do disco é a densidade vezes o volume, área vezes espessura, e o momento de inércia dele é metade da massa vezes o raio ao quadrado. Juntando tudo, os dois fatores iguais viram um quadrado.
> Agora soma todos os discos, de menos o raio da esfera até o raio da esfera. [A constante sai da integral, o quadrado se expande,] e o resultado é oito pi vezes a densidade vezes o raio da esfera à quinta, sobre quinze.
> Falta tirar a densidade: ela é a massa da esfera dividida pelo volume. Substitui, cancela os pi, e o raio à quinta sobre o raio ao cubo vira raio ao quadrado. Sobra: o momento de inércia é dois quintos da massa vezes o raio da esfera ao quadrado.

**7. De volta à energia (106,9–120,5 s)**
Tela: a mesma equação em aberto recebe o momento de inércia por cópia e depois a velocidade angular; cancelamentos; soma dos coeficientes; sete décimos.
> De volta à energia. Troca o momento de inércia pelo valor que achamos e a velocidade angular pela velocidade dividida pelo raio da esfera, porque ela rola sem deslizar. Os raios se cancelam, e meio mais um quinto dá sete décimos da massa vezes a velocidade ao quadrado.

**8. Para onde vai a energia (120,5–129,2 s)**
Tela: barra empilhada; a esfera desce e sobe; razão cinco para dois.
> Dessa energia cinética, cinco partes vão para a translação e duas para a rotação. Descendo, a potencial vira cinética; subindo, é o contrário.

**9. Altura mínima da esfera (129,2–147,4 s)**
Tela: conservação de energia com sete décimos; troca da velocidade ao quadrado; vinte e sete décimos; `2,7R` (primeira aparição); a linha de altura e a esfera sobem de 2,5 para 2,7.
> Agora, a altura mínima da esfera. Mesma velocidade no topo, mesma altura de dois raios, mas com sete décimos da massa vezes a velocidade ao quadrado. Corta massa e gravidade: dois mais sete décimos dá vinte e sete décimos. A altura mínima é dois vírgula sete vezes o raio, mais alta que os dois e meio da partícula.

**10. Teste a partir de 2,7R (147,4–158,1 s)**
Tela: corrida completa com barra e gráfico de energia; "completa o loop".
> Soltando a esfera dessa altura, ela desce, rola, sobe e completa o looping. A energia total não muda: só se redistribui.

**11. Fechamento (158,1–168,1 s)**
Tela: partícula `2,5R`, esfera `2,7R`; síntese em três linhas.
> Por que a esfera precisa de mais altura? Porque a velocidade mínima no topo é a mesma, mas parte da energia vai para a rotação. Mais energia pedida, mais altura inicial. Se curtiu, siga o Parallax Lab.

## Observações para o GPT

- Palavras de fala no texto acima: 578 (≈ 190 s a 3 palavras/s), contra 168 s do preview. O vídeo 8 tinha 464 palavras em 152 s; o 9 alongou a cena em ~10% pela voz. Aqui há ~20 s a mais do que a cena comporta: o bloco 6 (momento de inércia) e o 7 são os que mais precisam de cortes (marcados com `[...]`), e vale pedir ao GPT uma versão de ~500 palavras.
- Não falar `2,5R`, `2,7R` nem `dois quintos` antes dos blocos 3, 9 e 6, respectivamente (a tela também os esconde até lá).
- Dizer "rola sem deslizar" só uma vez (bloco 7), como hipótese, e "ideal" sem insistir.
- O vídeo mostra, nos blocos 3, 7 e 9, cópias de termos viajando de uma equação para outra: a fala pode acompanhar com "troca", "corta", "junta", "sobra".
