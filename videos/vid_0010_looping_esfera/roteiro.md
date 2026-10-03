# vid_0010 — Roteiro e narração (texto definitivo para a voz)

EXERCÍCIO RESOLVIDO · EP. 04. Cena: `cena.py`, classe `LoopingEsfera010`. Texto fechado com a revisão do GPT sobre `narracao_sugestao.md` (rascunho, só histórico).
Voz gerada (ElevenLabs, `audio/narracao_final.wav`, 168,24 s). Os tempos abaixo são os do preview silencioso (janelas); os tempos reais das âncoras estão em `sync.json`.

Arco: pergunta (esfera) → caso clássico (partícula) → condição no topo → dois e meio vezes o raio →
esfera: mesma condição → surge o momento de inércia → calcula → volta à energia → sete décimos →
dois vírgula sete vezes o raio → teste → síntese.

## Como falar as grandezas

| Na tela | Na fala |
|---|---|
| R | **raio do looping** |
| a | **raio da esfera** |
| h | **altura** / **altura inicial** |
| m, g | **massa**, **gravidade** |
| v, v_top | **velocidade**, **velocidade no topo** |
| ω | **velocidade angular** |
| I_CM | **momento de inércia** |
| N, mg | **normal** / **força normal**, **peso** |
| ρ | **densidade** |
| 2,5R · 2,7R | **dois e meio vezes o raio do looping** · **dois vírgula sete vezes o raio do looping** |
| 5/2 · 27/10 · 7/10 · 2/5 | **cinco meios** · **vinte e sete décimos** · **sete décimos** · **dois quintos** |

Sempre "looping" (nunca "loop"). R é o raio do looping; a é o raio da esfera: nunca só "raio" quando houver dúvida.

## Blocos e janelas do preview

| # | Bloco | Janela (s) | Âncoras semânticas (tempos virão da voz) |
|---|---|---|---|
| 1 | Pergunta e caso clássico | 0–6,9 | `pergunta` · `particula` |
| 2 | Topo do looping | 6,9–20,3 | `normal_zero` · `velocidade_topo` |
| 3 | Altura mínima da partícula | 20,3–42,7 | `energia_inicial` · `cinco_meios` · `dois_e_meio` · `corrida_particula` |
| 4 | Agora, a esfera | 42,7–53,5 | `condicao_igual` |
| 5 | O que muda na energia | 53,5–60,5 | `termo_rotacao` · `quanto_vale` |
| 6 | Momento de inércia | 60,5–106,9 | `disco` · `triangulo` · `quadrado` · `soma_discos` · `oito_pi` · `densidade` · `dois_quintos` |
| 7 | De volta à energia | 106,9–120,5 | `substitui_inercia` · `velocidade_angular` · `sete_decimos` |
| 8 | Para onde vai a energia | 120,5–129,2 | `cinco_e_dois` · `desce_sobe` |
| 9 | Altura mínima da esfera | 129,2–147,4 | `mesma_velocidade` · `vinte_e_sete_decimos` · `dois_virgula_sete` |
| 10 | Teste a partir de dois vírgula sete | 147,4–158,1 | `solta` · `completa` |
| 11 | Fechamento | 158,1–168,1 | `por_que` · `siga` |

Se a fala de um bloco passar da janela, a cena segura/alonga o trecho por âncoras (1–2 s no topo, por exemplo),
em vez de comprimir a fala.

## Narração (texto enviado ao ElevenLabs)

Qual é a altura mínima para uma esfera completar um looping? Pra descobrir, começamos pelo caso clássico: uma partícula.

No topo, peso e normal apontam para o centro. Juntos, dão massa vezes velocidade ao quadrado sobre o raio do looping. Como a pista só empurra, a normal não pode ser negativa. No limite ela zera: velocidade no topo ao quadrado igual a gravidade vezes raio.

Agora a energia. No início, ela é toda potencial: massa vezes gravidade vezes altura. No topo, a partícula está a dois raios e ainda tem energia cinética. Troca velocidade ao quadrado por gravidade vezes raio, corta massa e gravidade e junta: dois mais meio dá cinco meios. Logo, a altura mínima é dois e meio vezes o raio do looping. Soltando daí, a partícula completa o looping.

Agora, a esfera. A condição no topo muda? Não. As mesmas forças continuam atuando, então a velocidade mínima no topo é a mesma.

O que muda é a energia. A esfera também gira, então surge um termo de rotação, que depende do momento de inércia. Quanto ele vale?

Divida a esfera homogênea em discos finos. Para um disco a certa distância do centro, o raio da esfera, essa distância e o raio do disco formam um triângulo retângulo. Então o raio do disco ao quadrado é o raio da esfera ao quadrado menos a distância ao quadrado.

A massa do disco é densidade vezes volume, e o volume é área vezes espessura. O momento de inércia desse disco é metade da massa vezes o raio ao quadrado. Substituindo, os dois fatores iguais formam um quadrado.

Agora somamos todos os discos. A integral dá oito pi vezes a densidade vezes o raio da esfera à quinta, sobre quinze. Pela massa total, isolamos a densidade e substituímos. Os pi cancelam, e raio à quinta sobre raio ao cubo vira raio ao quadrado. Sobra: dois quintos da massa vezes o raio da esfera ao quadrado.

De volta à energia. Substituímos o momento de inércia e usamos o rolamento sem deslizamento: a velocidade angular é a velocidade dividida pelo raio da esfera. Os raios se cancelam. Somando rotação e translação, chegamos a sete décimos de massa vezes velocidade ao quadrado.

Desses sete décimos, cinco partes ficam na translação e duas na rotação. Descendo, potencial vira cinética; subindo, acontece o contrário.

Agora a altura mínima da esfera. No topo, a velocidade é a mesma e a altura continua sendo dois raios do looping. A diferença é a energia cinética de sete décimos. Substitui a condição do topo, corta massa e gravidade e soma: vinte e sete décimos do raio, ou dois vírgula sete vezes o raio do looping.

Soltando a esfera dessa altura, ela desce, rola, sobe e completa o looping. A energia total não muda; apenas se redistribui.

Por que a esfera precisa de mais altura? A velocidade mínima no topo é a mesma, mas parte da energia vai para a rotação. Mais energia, mais altura inicial. Se curtiu, siga o Parallax Lab.

Faixa inferior (y < −4,6 na área lógica) livre para legendas.
