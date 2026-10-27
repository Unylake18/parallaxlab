# Base de voz V2 — VID21 · Exercício Resolvido · EP. 07

**Base textual congelada: versão de 355 palavras fornecida pelo usuário.**
Substitui a sugestão V1 de 397 palavras. O texto foi preservado integralmente,
inclusive a leitura de símbolos e o CTA “Siga o Parallax Lab para entender a física”.
A gravação e a sincronização final ainda não foram executadas.

## Ritmo: média global e velocidade efetiva

- **355 palavras**, contadas no texto que será lido; títulos e notas ficam fora.
- **150 palavras por minuto durante a fala** = 2,5 palavras/s.
- Orçamento de fala: **142 segundos**.
- Em um vídeo de 165 segundos, restam **23 segundos** para pausas e leitura visual.
- Média sobre o vídeo inteiro, já incluindo esses respiros: **129,09 palavras/minuto**.

A V1 tinha 144,36 palavras/minuto sobre os 165 segundos completos. A hipótese de
2,8–2,9 palavras/s durante a fala correspondia a **168–174 palavras/minuto**;
portanto, não representava uma locução efetiva a 144 palavras/minuto. Essa distinção
fica explícita nesta versão. Os números são um orçamento textual, não a duração
medida de uma voz. A pronúncia, a entonação e as pausas precisam ser medidas no áudio.

## Ajustes de conteúdo incorporados

- A primeira lei vem acompanhada da convenção: trabalho positivo quando realizado
  pelo gás. A expressão falada é “Q igual a delta U mais W”.
- O trabalho é associado à área sob o caminho no diagrama de pressão por volume;
  a expansão explica o sinal positivo. Na compressão, o trabalho realizado pelo
  gás é negativo. Em geral, a integral tem sinal; não tomar uma área geométrica
  positiva como o trabalho de qualquer percurso.
- Foram retiradas repetições sobre a expansão e a temperatura. O pistão, as barras
  e as fórmulas carregam parte da explicação.
- O retorno só estabelece os sinais: variação da energia interna, trabalho e calor
  negativos. Não foi acrescentado cálculo numérico do calor cedido.
- O calor total absorvido soma os dois trechos positivos; é diferente do calor líquido.
- O módulo do trabalho líquido vem da área interna. O percurso anti-horário fixa o
  sinal negativo. A variação total da energia interna é zero ao fechar o ciclo.

## Orçamento frente ao preview atual

Base visual: `media/videos/cena/960p15/CicloTermodinamico021.mp4`, **164,996 s**,
540×960, 15 fps nominal. Os intervalos abaixo são os blocos do preview aprovado;
**não são uma sincronização final da voz V2**.

A fala estimada usa 150 palavras/minuto. Um saldo negativo indica tempo que falta
na janela atual, antes mesmo de reservar uma pausa. Um saldo positivo é tempo
potencial para pausas ou redistribuição, não uma duração de silêncio já fixada.

| Bloco | Janela visual atual | Palavras | Fala estimada | Saldo da janela |
| --- | --- | ---: | ---: | ---: |
| Introdução e construção do ciclo | 0–25 s | 44 | 17,60 s | +7,40 s |
| Ferramentas e convenção de sinal | 25–40 s | 47 | 18,80 s | -3,80 s |
| A → B: expansão | 40–75 s | 52 | 20,80 s | +14,20 s |
| B → C: volume constante | 75–100 s | 47 | 18,80 s | +6,20 s |
| C → A: compressão e calor cedido | 100–120 s | 54 | 21,60 s | -1,60 s |
| Calor total absorvido | 120–135 s | 21 | 8,40 s | +6,60 s |
| Área, sentido e trabalho líquido | 135–153 s | 45 | 18,00 s | 0,00 s |
| Fechamento e CTA | 153–165 s | 45 | 18,00 s | -6,00 s |

Há **11,40 s de déficit local** nas ferramentas, no retorno e no fechamento.
Os demais blocos têm **34,40 s de margem somada**, deixando o saldo global de
23 segundos. Assim, a contagem total cabe no orçamento, mas a distribuição atual
dos tempos precisa mudar. A área/trabalho líquido ocupa sua janela inteira na
estimativa e também precisa receber uma pausa de leitura.

Não acelerar essas partes para caber nos timestamps antigos. Primeiro medir a voz
real; depois redistribuir os waits e, se necessário, ajustar os pontos de entrada
das animações dentro dos mesmos processos. Não foi alterado nenhum wait nesta rodada.

## Texto de voz congelado

Quanto calor esse gás realmente absorve?

Calor absorvido não é calor líquido. Vamos seguir o ciclo.

Primeiro, o gás se expande a pressão constante até quadruplicar o volume.

Depois, o volume fica fixo enquanto a pressão quadruplica.

Por fim, ele retorna ao estado inicial.

Para um gás ideal monoatômico, a energia interna é três meios de P vezes V.

E, com trabalho positivo quando realizado pelo gás, a primeira lei fica Q igual a delta U mais W.

No diagrama P por V, o trabalho é a área sob o caminho.

Em A para B, a pressão é constante. A área do retângulo dá três P zero V zero.

A energia interna também aumenta: nove meios de P zero V zero.

Somando os dois, o calor recebido é quinze meios de P zero V zero.

Como Q é positivo, calor entra no gás.

De B para C, o pistão fica parado. Sem variação de volume, o trabalho é zero.

Mas a pressão aumenta, então P vezes V aumenta e a energia interna também.

Logo, o calor recebido é dezoito P zero V zero.

Mais uma vez, calor entra no gás.

No retorno, pressão e volume diminuem. Então P vezes V diminui e a energia interna cai.

Além disso, o gás é comprimido, então o trabalho realizado por ele é negativo.

Com delta U negativo e W negativo, Q também é negativo: calor sai do gás.

Esse trecho não entra na soma do calor absorvido.

Então somamos apenas os dois trechos com Q positivo.

O resultado é cinquenta e um meios de P zero V zero.

Agora olhe para o ciclo inteiro.

O módulo do trabalho líquido é a área do triângulo: metade de três V zero vezes três P zero.

Isso dá nove meios de P zero V zero.

Mas o percurso é anti-horário, então o trabalho líquido é negativo.

Como o gás termina no mesmo estado em que começou, a variação total da energia interna é zero.

Assim, calor líquido e trabalho líquido são iguais: no ciclo completo, o gás cede mais calor do que absorve.

Siga o Parallax Lab para entender a física.

## Próxima etapa de sincronização

1. Usar esta base, sem voltar à V1 de 397 palavras.
2. Gerar a voz com leitura conversada e medir o WAV resultante.
3. Conferir as entradas da primeira lei, dos resultados, da compressão, do sentido
   anti-horário e do CTA. Não fixar um alinhamento de palavras apenas pela contagem.
4. Ajustar os waits com base nessa medida, preservando pausas para os resultados
   e respiro antes do CTA. Se a voz pedir mais que 165 segundos, rever o encaixe
   com a duração real antes de acelerar a locução.

Esta rodada fecha somente a base textual e o orçamento. Nenhuma voz, SRT, master,
novo render ou alteração da cena foi produzida.

## Arquivos e conferência

- `texto_narracao_sugestao.txt`: base V2, 355 palavras, em 29 parágrafos.
- `qa_narracao/blocos_sugestao.json`: orçamento V2 em oito blocos, com déficits explícitos.
- `qa_narracao/mapa_por_segundo.csv`: correspondência dos segundos do preview com os oito blocos V2.
- `narracao_sugestao_v1.md`, `texto_narracao_sugestao_v1.txt`,
  `qa_narracao/blocos_sugestao_v1.json` e `qa_narracao/mapa_por_segundo_v1.csv`:
  versões anteriores preservadas para histórico; não usar para gravação.
- `qa_narracao/marcos_cena.json` e os frames de conferência já existentes continuam
  descrevendo o preview aprovado, que não mudou.
- Conferidos: 355 palavras, soma dos oito blocos, cobertura contínua de 0–165 s,
  29 parágrafos e conta correta de velocidade efetiva, fala e pausas.
