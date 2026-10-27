# Narração sugerida — VID 0029 · POR TRÁS DA FÓRMULA · EP. 09

Base visual: preview v3 (`renders/preview_v3_540x960.mp4`, 195 s). Alvo do vídeo final: **~3 min (180 s)**.
Gerado por `narracao_blocos.py` (que escreve também `narracao_sugestao.json` e `texto_narracao_sugestao.txt`).
A voz ainda não foi gerada; os números abaixo são orçamento textual, não duração medida.

## Orçamento

- **453 palavras** faladas (tags e títulos fora da contagem).
- A **2,7 palavras/s** (briefing): **167,8 s** de fala e **12,2 s** de respiro em 180 s.
- A **2,5 palavras/s** (ritmo medido no vid_0021): **181 s** de fala; nesse ritmo o vídeo fecha em ~3:03. Se a voz sair lenta, o primeiro corte é a frase "No modelo ideal, as espiras são bem apertadinhas" (B02, 8 palavras).
- O vídeo de 195 s encolhe para ~180 s **na sincronização**, só pelo `timeline.json`: cada beat ganha a janela da voz medida.

| Beat | Janela proposta (s) | Atual v3 (s) | Palavras | Fala a 2,7/s | Respiro |
|---|---|---|---:|---:|---:|
| B01 Gancho | 0–11 | 0–12 | 29 | 10,7 | 0,3 |
| B02 Objeto | 11–25 | 12–26 | 35 | 13,0 | 1,0 |
| B03 Simetria | 25–46 | 26–52 | 57 | 21,1 | −0,1 |
| B04 Ampère | 46–71 | 52–78 | 61 | 22,6 | 2,4 |
| B05 Buraco | 71–82 | 78–92 | 24 | 8,9 | 2,1 |
| B06 Dentro | 82–112 | 92–122 | 83 | 30,7 | −0,7 |
| B07 Fora | 112–129 | 122–145 | 41 | 15,2 | 1,8 |
| B08 Gráfico | 129–151 | 145–173 | 52 | 19,3 | 2,7 |
| B09 Conferência | 151–165 | 173–185 | 37 | 13,7 | 0,3 |
| B10 Fechamento + CTA | 165–180 | 185–195 | 34 | 12,6 | 2,4 |

Onde a animação encolhe (para a sincronização): B03 (−5 s: o giro rígido das setas fica mais curto), B04 (−1 s),
B05 (−3 s), B06 (0 s), B07 (−6 s: menos espera depois do `B = 0`), B08 (−6 s: varredura de 10 s → ~8 s e elos mais
colados), B09 (+2 s) e B10 (+5 s: o CTA falado cai sobre o end card).

## Regras seguidas

- **Hook** na primeira frase, antes de qualquer fórmula: o anel prende o próprio campo; fora, nada. Pergunta no fim do B01.
- **Variáveis pelo nome:** a letra aparece só quando o símbolo é apresentado ("o número de espiras é o N", "o raio médio
  do anel é o R", "o raio da seção, o a", "de raio r"). Depois, sempre o nome: "o número de espiras vezes a corrente",
  "dois pi vezes o raio", "um sobre o raio". μ₀ é lido "mi zero".
- **Conectivos de professor:** "Agora", "Repara", "Então", "Primeiro", "E olha", "É por isso", "Resumindo".
- **Física do briefing preservada:** "no toroide ideal" dito uma vez, com a simetria na formulação do Kaio (o campo
  acompanha o círculo, tangente, com o mesmo valor). Nada de "exatamente zero na vida real", nada de "polo", sem número em tela
  falado (o "quase o dobro" é comparação).
- **Tags v4 em inglês, uma por trecho**: `[curious]`, `[thoughtful]`, `[calm, satisfied]` e `[short pause]` pontual.
  Sem `[slowly]` nem `[slow, measured pace]`. Nenhum `[excited]`: o "não é uniforme" ganha ênfase pela pausa e pela frase curta.
- **CTA:** "Siga o Parallax Lab." falado; o end card mostra `@labparallax`.

## Texto, casado com a tela

Cada frase cai no evento indicado em **Na tela**. As âncoras viram chaves do `timeline.json` na sincronização.

### B01 · 0–11 s · `[curious]` · 29 palavras
> Esse anel de fio prende o próprio campo magnético. Liga a corrente... e o campo aparece só dentro do enrolamento.
> E fora do anel? Nada. Como ele consegue isso?

**Na tela:** toroide em órbita · "Liga a corrente" = rastro único percorrendo o fio · "o campo aparece" = anéis magenta
acendendo · "E fora do anel?" = chip `E FORA DO ANEL?`.

### B02 · 11–25 s · `[thoughtful]` · 35 palavras
> Isso é um toroide: um solenoide dobrado até as pontas se encontrarem. No modelo ideal, as espiras são bem apertadinhas.
> O número de espiras é o N, e todas levam a mesma corrente, o I.

**Na tela:** "modelo ideal" = chip `MODELO IDEAL` · "o N" e "o I" = definições `N: número de espiras`, `I: corrente no fio`.

### B03 · 25–46 s · `[thoughtful]` · 57 palavras
> Agora, de cima. O raio médio do anel é o R, e o raio da seção, o a. Desenha um círculo em volta do eixo, de raio r.
> No toroide ideal, a simetria faz o campo acompanhar esse círculo, tangente a ele, com o mesmo valor em todo ponto.
> E o caminho aponta junto com o campo.

**Na tela:** "de cima" = câmera pousando · "o R" / "o a" = seta R, segmento a e definições · "Desenha um círculo… de raio r" =
amperiano + seta de raio · "acompanhar esse círculo… mesmo valor" = 8 setas B iguais girando · "o caminho aponta junto" =
setas dℓ + chip `B ∥ dℓ`, depois `MESMO B NO CÍRCULO TODO`.

### B04 · 46–71 s · `[thoughtful]` · 61 palavras
> A Lei de Ampère diz: a circulação do campo magnético nesse caminho é mi zero vezes a corrente envolvida, a que atravessa
> o disco. Campo e caminho são paralelos, então o produto escalar vira um produto simples. E, com o mesmo valor no círculo
> todo, o campo sai da integral. Sobra o comprimento do círculo. Desenrola... dois pi vezes o raio.

**Na tela:** "Lei de Ampère" = `∮ B·dℓ = μ₀ I_enc` com elos B e dℓ · "a que atravessa o disco" = definição de I_enc + disco ·
"produto simples" = setas piscam + ponto do produto escalar some · "sai da integral" = B atravessa para fora ·
"Desenrola…" = círculo rolando · "dois pi vezes o raio" = rótulo 2πr voando para a equação.

### B05 · 71–82 s · `[curious]` · 24 palavras
> Primeiro, um círculo no buraco do anel. Quantos fios furam esse disco? Nenhum. [short pause] A corrente envolvida é zero...
> então o campo ali é zero.

**Na tela:** "no buraco" = círculo encolhendo · "Nenhum" = disco vazio · "corrente envolvida é zero" = `I_enc = 0` ·
"campo ali é zero" = `B = 0` e as setas encolhendo até sumir.

### B06 · 82–112 s · `[thoughtful]` · 83 palavras
> Agora o círculo passa por dentro do enrolamento. Repara: cada espira fura o disco uma vez, pelo lado de dentro, e todas
> no mesmo sentido. Então a corrente envolvida é o número de espiras vezes a corrente. Passando dois pi vezes o raio para
> o outro lado: o campo é mi zero vezes o número de espiras vezes a corrente, sobre dois pi vezes o raio. E olha o raio ali
> embaixo: o campo não é uniforme. É mais forte perto do buraco.

**Na tela:** "cada espira fura o disco uma vez" = ⊙ acendendo um a um com o contador (frase dita *durante* a contagem) ·
"número de espiras vezes a corrente" = `24 I → N I` e o anel de ⊙ inteiro aceso · "Passando… para o outro lado" = 2πr descendo
para o denominador · "o raio ali embaixo" = elo do r do denominador com a seta de raio · "mais forte perto do buraco" = setas
voltando com tamanho ∝ 1/r + chip `NÃO É UNIFORME`.

### B07 · 112–129 s · `[curious]` · 41 palavras
> E fora do anel? Agora cada espira fura o disco duas vezes: subindo pelo lado de dentro... e descendo pelo lado de fora.
> Uma corrente cancela a outra. [short pause] Corrente envolvida zero, campo zero. É por isso que o campo não escapa.

**Na tela:** "subindo pelo lado de dentro" = flash de dentro + primeiro `N I` ligado ao anel de ⊙ · "descendo pelo lado de fora" =
⊗ um a um + segundo `N I` ligado ao anel de ⊗ · "Uma cancela a outra" = riscos e `0` · "campo zero" = `B = 0` e as setas sumindo.

### B08 · 129–151 s · `[thoughtful]` · 52 palavras
> Aumentando o raio do círculo, a gente desenha o campo. No buraco, zero. Ao entrar no enrolamento, um salto. Lá dentro, ele
> cai com um sobre o raio. E do lado de fora, zero de novo. Na borda de dentro, o campo é quase o dobro do campo na borda de fora.

**Na tela:** "desenha o campo" = eixos e bordas descendo do anel · cada trecho falado acompanha o cursor da varredura (buraco,
salto em R − a, curva com o `∝ 1/r`, zero depois de R + a) · "quase o dobro" = duas setas de comparação + `≈ 1,9×`.

### B09 · 151–165 s · `[thoughtful]` · 37 palavras
> E dá pra conferir. Se o anel for grande perto da seção, o raio quase não muda. Aí, o número de espiras dividido pela volta
> do anel vira espiras por metro... e volta o campo do solenoide.

**Na tela:** close lateral (parece um solenoide reto) · "o raio quase não muda" = `r ≈ R` e `r → R` · "dividido pela volta
do anel" = reagrupamento `μ₀ (N/2πR) I` · "espiras por metro" = colapso em `n` + definição · "campo do solenoide" = chip `SOLENOIDE`.

### B10 · 165–180 s · `[calm, satisfied]` · 34 palavras
> Resumindo: dentro do enrolamento, o campo cai com um sobre o raio. No buraco e fora, zero. É assim que um solenoide fechado
> em anel prende o próprio campo. Siga o arroba lab parallax.

**Na tela:** "dentro… um sobre o raio" = painel, linha `DENTRO` e a coroa do ícone · "No buraco e fora, zero" = linha `FORA` e o
buraco/exterior do ícone · "Siga o arroba lab parallax" = end card `@labparallax`.

## Próximos passos (não iniciados)

1. Aprovação deste texto.
2. Geração da voz (ElevenLabs v4, uma exportação contínua, como no vid_0004).
3. Sincronização: medir o áudio, ajustar só o `timeline.json` (beats, eventos, contagens, chaves do amperiano), re-renderizar 3D
   e Manim e montar. SRT e legenda queimada no estilo `compacto` ficam para a rodada própria.
