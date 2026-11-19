# vid_0026 — sugestão de narração v1 (roteiro limpo, sem tags)

Base: storyboard e física do handoff v1 (congelados) e a cena do preview v4 (146,5 s), analisada quadro a quadro.
Estilo: professor de cursinho, "a gente"/"você", conectivos variados, brincadeiras leves (nunca com vítimas),
variáveis sempre pelo nome inteiro (nunca a letra solta), números por extenso. A cena se estica para a fala
(`ESTICA` por bloco); a álgebra do C02 e do C03 ganha tempo de propósito.
Versão com tags para gravar: `narracao_tags_v1.md`. Nenhum áudio foi gerado.

Cada `###` é um parágrafo da fala, ancorado no passo da cena que ele acompanha.

## C01 · Mistério (hook + bem-vindos)

### C01.1 — o acidente (carros entram, anel de impacto, deslizam desenhando a marca)
Dois carros chegam juntos num cruzamento... e batem. O azul vinha do oeste, o violeta vinha do sul. Grudados, eles ainda
deslizam um bom pedaço até parar.

### C01.2 — chegamos depois (a cena escurece, cotas 8 m, 6 m, 10 m)
Só que a gente chegou depois. A batida já acabou, e sobrou só isto: uma marca no asfalto. Oito metros para leste, seis
para norte... dez metros de marca.

### C01.3 — voltar no tempo (seta curva na régua; entra a pergunta do hook)
Então vamos fazer o caminho de volta no tempo. O que uma marca no asfalto consegue contar sobre uma batida?

### C01.4 — bem-vindos
Fala, pessoal! Bem-vindos ao Parallax Lab! Hoje a gente vira detetive de colisão. E fica tranquilo: aqui os carros são
feitos só de vidro e matemática.

### C01.5 — o que se sabe (coluna de parâmetros, setas fantasma com "= ?")
O que a gente sabe: o carro azul tem dois mil quilos, e o violeta, mil. O coeficiente de atrito cinético entre os pneus e
o asfalto é zero vírgula cinco, e a aceleração da gravidade, dez metros por segundo ao quadrado. A pergunta é: qual era a
velocidade de cada carro imediatamente antes da batida?

### C01.6 — hipóteses (legenda de duas linhas)
Para isso, um modelo simples: o impacto é curtíssimo, o atrito é o mesmo durante todo o deslizamento, e a marca é reta e
começa no ponto do impacto. É um modelo idealizado, não uma perícia de verdade.

## C02 · Começar pelo fim (trabalho e energia)

### C02.1 — massa total na coluna
E por onde um bom detetive começa? Pelo fim! A marca registra o deslizamento, que acontece depois da batida. Grudados, os
dois carros viram um conjunto só, com massa total de três mil quilos: dois mil mais mil.

### C02.2 — replay do deslizamento; velocidade logo depois da batida = ?
O conjunto sai do ponto do impacto com uma velocidade que a gente ainda não conhece, a velocidade logo depois da batida,
e vai freando até parar no fim da marca.

### C02.3 — forças na vista lateral: peso, normal
Olha as forças, vistas de lado. O peso puxa o conjunto para baixo, e o chão empurra de volta com a força normal, do mesmo
tamanho. Então a normal é a massa total vezes a aceleração da gravidade.

### C02.4 — atrito cinético
E o atrito cinético aponta contra o movimento. Ele vale o coeficiente de atrito vezes a normal... ou seja, coeficiente
de atrito vezes massa total vezes gravidade.

### C02.5 — trabalho do atrito (laranja)
Ao longo dos dez metros da marca, esse atrito realiza um trabalho negativo: menos a força de atrito vezes o comprimento da
marca. É a energia que o atrito transforma em calor, no asfalto e nos pneus.

### C02.6 — variação da energia cinética = trabalho do atrito
E aqui entra o teorema do trabalho e energia: a variação da energia cinética é igual ao trabalho do atrito. No começo do
deslizamento, a energia cinética é meio vezes a massa total vezes a velocidade logo depois da batida, ao quadrado. No fim,
o conjunto parou: energia cinética zero. Então fica: zero, menos meio da massa total vezes a velocidade ao quadrado, igual
a menos o coeficiente de atrito vezes a massa total vezes a gravidade vezes o comprimento da marca.

### C02.7 — passo 1: os sinais de menos cancelam
Agora a álgebra, com calma. Primeiro, os dois lados têm um sinal de menos. Multiplicando tudo por menos um, eles somem, e o
zero também sai de cena.

### C02.8 — passo 2: a massa total corta
Repara numa coisa bonita: a massa total aparece dos dois lados, multiplicando. Então dá para cortar! A massa total
cancela. Ou seja, carro leve ou caminhão, a mesma marca daria a mesma velocidade.

### C02.9 — passo 3: o meio atravessa e vira dois
Depois, o meio, que está multiplicando do lado esquerdo, passa para o outro lado como dois. Fica: a velocidade ao
quadrado é igual a duas vezes o coeficiente de atrito vezes a gravidade vezes o comprimento da marca.

### C02.10 — passo 4: raiz
E tirando a raiz quadrada dos dois lados, chegamos à velocidade logo depois da batida.

### C02.11 — substituição (os números voam da coluna e da cota)
Agora é só trocar pelos números: duas vezes zero vírgula cinco, vezes dez, vezes dez. Isso dá cem... e a raiz de cem é
dez. Dez metros por segundo, logo depois da batida.

### C02.12 — componentes (10·8/10 e 10·6/10)
E a direção? Está na própria marca: o conjunto deslizou em linha reta, então a velocidade aponta ao longo dela. A parte
para leste é dez vezes oito sobre dez: oito metros por segundo. A parte para norte é dez vezes seis sobre dez: seis
metros por segundo. O mesmo triângulo da marca, agora em velocidade.

## C03 · Voltar ao impacto (momento)

### C03.1 — antes do choque; setas com "= ?"
Agora a gente volta mais um pouquinho no tempo: para o instante antes do impacto. E aqui a lei muda.

### C03.2 — selos: impacto curtíssimo × vários metros
No deslizamento, o atrito agiu por vários metros, então não dava para ignorar. Mas o impacto dura uma fração de segundo:
nesse tempinho, o impulso das forças externas é desprezível perto do empurrão enorme que um carro dá no outro. Por isso,
no impacto, quem se conserva é o momento.

### C03.3 — momento de cada carro
Lembrando: o momento de um carro é a massa vezes a velocidade, e aponta para onde o carro vai. O do carro azul aponta
para leste; o do violeta, para norte.

### C03.4 — momento total antes e depois; igualdade
Somando os dois, temos o momento total antes. Logo depois da batida, o momento total é a massa total vezes a velocidade
comum, apontando ao longo da marca. E a conservação diz: momento total antes igual a momento total depois.

### C03.5 — projeções: uma igualdade por direção
Como essa é uma igualdade entre vetores, ela vale em cada direção separadamente. Na direção leste: a massa do carro azul
vezes a velocidade dele é igual à massa total vezes a parte leste da velocidade depois da batida. Na direção norte: a
massa do carro violeta vezes a velocidade dele é igual à massa total vezes a parte norte.

### C03.6 — isolar (a massa de cada carro passa dividindo)
Para isolar a velocidade de cada carro, a massa dele, que está multiplicando, passa para o outro lado dividindo. Fica a
massa total sobre a massa do carro, vezes a parte da velocidade naquela direção.

### C03.7 — substituir e calcular
No carro azul: três mil sobre dois mil, vezes oito... doze metros por segundo. No violeta: três mil sobre mil, vezes
seis... dezoito metros por segundo.

### C03.8 — km/h (o laço fecha nas setas)
Em quilômetros por hora: o azul vinha a quarenta e três vírgula dois, e o violeta a sessenta e quatro vírgula oito. Bem
mais rápido!

## C04 · O triângulo e a pegadinha

### C04.1 — três triângulos (marca → velocidade → momento)
E agora vem a pegadinha. Olha o mesmo triângulo três vezes: a marca, em metros; a velocidade, em metros por segundo; e o
momento, que é a velocidade vezes três mil quilos. Vinte e quatro mil para leste, dezoito mil para norte, trinta mil no
total. A mesma direção atravessa todas as etapas.

### C04.2 — tangente do ângulo
A tangente do ângulo da marca é a parte norte do momento sobre a parte leste: dezoito mil sobre vinte e quatro mil... três
quartos. Repara: é a razão dos momentos, não das velocidades.

### C04.3 — contraste (barras)
Se você dividisse as velocidades, daria dezoito sobre doze, e a conta não fecha. O carro violeta era o mais rápido... mas o
azul, com o dobro da massa, tinha mais momento. Por isso os destroços foram mais para leste do que para norte. Quem manda
na direção não é o mais rápido: é quem tem mais momento.

## C05 · Conferência de ida e volta

### C05.1 — replay para frente
Vamos conferir fazendo o caminho de ida. Carro azul a doze, violeta a dezoito. O momento total fica vinte e quatro mil para
leste e dezoito mil para norte. Dividindo pela massa total, a velocidade depois da batida é oito e seis... e com esse
atrito, o conjunto desliza exatamente dez metros.

### C05.2 — ✓ na marca
Parou em cima da marca! A conta de ida bate com a de volta.

## C06 · E a energia?

### C06.1 — pergunta
O momento se conservou. E a energia cinética?

### C06.2 — energia cinética antes
Antes da batida: meio vezes dois mil vezes doze ao quadrado, mais meio vezes mil vezes dezoito ao quadrado. Dá cento e
quarenta e quatro mais cento e sessenta e dois: trezentos e seis quilojoules.

### C06.3 — energia cinética depois
Logo depois: meio vezes três mil vezes dez ao quadrado. Cento e cinquenta quilojoules.

### C06.4 — o que foi convertido (laranja)
Faltam cento e cinquenta e seis quilojoules: pouco mais da metade. E essa energia não sumiu: virou deformação da lataria,
calor, som e vibração. Momento se conserva; energia cinética, não.

## C07 · Fechamento

### C07.1 — cada intervalo, sua lei
Então, a lição do dia: cada intervalo tem a sua lei. No impacto, conservação do momento. No deslizamento, trabalho e
energia.

### C07.2 — ponte
Aqui os dois carros ficaram juntos. Mas e se a colisão fosse elástica, com a energia cinética também conservada? Aí a
geometria dos momentos começa a dizer até quais ângulos de saída são possíveis. Mas isso já é assunto para outro vídeo.

### C07.3 — resposta ao hook
Respondendo à pergunta do começo: a marca no asfalto conta a velocidade e a direção logo depois da batida, e o momento leva
a gente de volta até a velocidade de cada carro.

## Cartão final

### CTA
Se você curtiu virar detetive de colisão, segue o Parallax Lab. Até a próxima!
