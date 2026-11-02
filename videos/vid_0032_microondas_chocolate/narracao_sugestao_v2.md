# vid_0032 — narração sugerida v2 (quadro a quadro, sobre o preview v3)

Base: `renders/preview_v3_540x960.mp4` (176,0 s, silencioso). Os estados e tempos são os do preview; a voz estica as cenas depois.
Estilo: `roteiro_voz_elevenlabs_v4.md` (professor de cursinho, variáveis pelo nome, uma tag por trecho, sem `[slowly]`).
Teto: vídeo final com voz **< 180 s**. Voz real: 2,7–3,0 palavras/s. Fala-alvo: ~140–155 s dentro dos 176 s do preview.
Fase: **só a sugestão de fala** (sem voz, SRT, master, capa). As tags `[ ]` entram no `narracao_tags_v2.md`, quando você pedir.

Esta v2 refaz a v1 (`narracao_sugestao.md`, 440 palavras, escrita sem preview): agora cada frase cai sobre o estado da tela.
Mudanças e motivos:

1. **Abertura reescrita para os 28 s do C01 novo:** pergunta → manchas (manchete "ESSAS MANCHAS MEDEM…") → etiqueta (2450 MHz) → porta/prato parado → os 3 passos (chips). A v1 tinha só 4 frases.
2. **Os 3 chips viram a promessa falada:** "primeiro, a onda; segundo, o calor; terceiro, a conta", um por chip (18 / 22,5 / 25,5 s).
3. **Fecho cobre o macro do C07:** "Essas manchas mediram a velocidade da luz" no quadro da manchete no passado (165,3 s).
4. **Enxugado para 418 palavras** (v1: 440): C03 e C04 estavam apertados contra os eventos (a v1 não cabia em 32 s e 40 s). Folga: ~25–40 s abaixo de 3 min.
5. **"c" nunca falado como letra.** λ = "comprimento de onda", d = "distância entre as manchas", f = "frequência", E = "campo elétrico".
6. Fica de fora da fala (regras da ficha): "ressonância da água", "de dentro para fora", porcentagem de erro, instrução de experimento em casa, a resposta do desafio (16,4 cm). O aviso de "comida em anel" fica numa só frase curta, com a ressalva.

Falado × tela: 6,1 cm → "seis vírgula um centímetros"; 12,2 cm → "doze vírgula dois"; 2450 MHz → "dois mil quatrocentos e cinquenta megahertz" (e "quase dois bilhões e meio de oscilações por segundo"); 0,061 m → só aparece, não é lido; 2,99×10⁸ m/s → "praticamente trezentos milhões de metros por segundo"; 915 MHz → "novecentos e quinze megahertz".

## C01 · Abertura (em ~28 s quem chega sabe a pergunta, a pista e os três passos)

| Estado (preview v3) | Na tela | Fala |
|---|---|---|
| **C01** 0,0 s (macro 3D); régua 1,2 s | macro do chocolate com 4 manchas; régua com "6,1 cm" + "medida ilustrativa" | Dá pra medir a velocidade da luz com um micro-ondas e uma barra de chocolate? |
| manchete 1,8 s; saltos 4,0 s | ESSAS MANCHAS MEDEM A VELOCIDADE DA LUZ; a régua salta de par em par | Parece piada, mas essas manchas medem a velocidade da luz. |
| rebobina 7,5 s → recua 8,3 s | a régua some; a câmera recua até o forno | *(respiro)* |
| etiqueta 9,8 s; pulso 11,0 s | etiqueta com contorno pulsando; `2450 MHz` | Na etiqueta, a frequência: dois mil quatrocentos e cinquenta megahertz. |
| porta 13,0 s → entra 14,8 s | a porta fecha; o chocolate entra | Fecha a porta, põe o chocolate no forno... |
| prato parado 16,1 s | PRATO PARADO | ...com o prato parado. |
| chip1 / liga 18,0 s | `1 A ONDA`; o forno liga | Em três passos: primeiro, a onda dentro do forno. |
| chip2 / derrete 22,5 s | `2 O CALOR`; o chocolate derrete | Segundo, o calor, que derrete o chocolate. |
| chip3 25,5 s → topo 27,2 s | `3 A CONTA`; a câmera sobe para a vista de cima | Terceiro, a conta. |

## C02 · A onda bate e volta (28–58 s)

| Estado (preview v3) | Na tela | Fala |
|---|---|---|
| **C02** 28,0 s → viaja 28,4 s | A ONDA BATE E VOLTA; a onda anda para a parede | O forno solta micro-ondas, da mesma família da luz. Elas batem na parede de metal e voltam. |
| estacionária 34,5 s | a onda de ida e a de volta se somam | Somando a que vai com a que volta, sai uma onda que não anda. |
| parada 39,0 s | ONDA PARADA | Ela só sobe e desce no lugar: é a onda estacionária. |
| nós 43,0 s | pontos "nó" | Nos nós, o campo elétrico fica sempre zero. |
| ventres 47,0 s | setas "ventre" | Nos ventres, ele oscila com toda a força. |
| ~51 s (hold) | setas oscilando | Repara: ele sobe, desce e troca de sentido o tempo todo. |

## C03 · O calor vai com E² (58–90 s)

| Estado (preview v3) | Na tela | Fala |
|---|---|---|
| **C03** 58,0 s → seta 58,8 s | O CALOR VAI COM `E²`; vetor E no ventre | Agora vem o pulo do gato: o que esquenta é o campo elétrico ao quadrado. |
| medidor 60,6 s → mf2 63,5 s | medidor de calor; `(+E)² → E²`, `(−E)² → E²` | Aponta pra cima, depois pra baixo... e esquenta igual, porque o quadrado não liga pro sinal. |
| instantânea 70,0 s → média 71,0 s | `E²` instantâneo; curva da média | Esse aquecimento pulsa rápido; o que importa é a média do quadrado. |
| medidor_pico 79,0 s | `⟨E²⟩` vira um morro por ventre | Resultado: um pico de calor em cada ventre. |
| chaves 82,0 s | chaves `λ` e `λ/2` | De um ventre ao próximo não cabe uma onda inteira, cabe meia. |
| manchas 86,0 s | UMA MANCHA A CADA `λ/2`; guias nos picos | Uma mancha a cada meio comprimento de onda. |

## C04 · A conta (90–130 s)

| Estado (preview v3) | Na tela | Fala |
|---|---|---|
| **C04** 90,0 s → régua 90,8 s | A CONTA; régua `d = 6,1 cm`, "medida ilustrativa" | Agora a conta. Digamos que a régua marque seis vírgula um centímetros entre duas manchas. |
| d_lambda 95,0 s | `d = λ/2` → `λ = 2d` → `= 12,2 cm` | Isso é meio comprimento de onda, então a onda inteira tem o dobro: doze vírgula dois. |
| etiqueta 101,0 s | etiqueta "frequência" `2450 MHz` → `f = 2,45×10⁹ Hz` | A etiqueta dá a frequência: dois mil quatrocentos e cinquenta megahertz. |
| ~105,6 s | `f = 2,45×10⁹ Hz` | São quase dois bilhões e meio de oscilações por segundo. |
| viajante 107,0 s (T0 108,2 s) | a onda viaja; "1 oscilação", "2 oscilações"; chaves `λ` | A cada oscilação, a onda anda um comprimento de onda. |
| ~113,6 s | volta `d`, `λ`, `f` | Então a velocidade é o comprimento de onda vezes a frequência. |
| c_lambda_f 117,0 s | `c = λf` → `c = 2df` | Como o comprimento de onda é o dobro da distância: duas vezes a distância vezes a frequência. |
| números 122,0 s | `c = 2 (0,061 m)(2,45×10⁹ Hz)` | Colocando os números... |
| resultado 126,0 s | `c ≈ 2,99×10⁸ m/s` em caixa; "a velocidade da luz" | *(pausa curta)* Praticamente trezentos milhões de metros por segundo. |
| pulso 128,6 s | a caixa pulsa | A velocidade da luz! |

## C05 · O forno é uma caixa (130–148 s)

| Estado (preview v3) | Na tela | Fala |
|---|---|---|
| **C05** 130,0 s | O FORNO É UMA CAIXA; chip `c ≈ 3×10⁸ m/s` ESTIMATIVA; forno aberto por cima | Só que tem um detalhe: o forno de verdade não é uma linha, é uma caixa. |
| fitas 133–137 s → relevo 137,0 s | fitas de onda em várias direções; mapa de calor | *(a tela mostra)* |
| texto 139,0 s | VÁRIOS PADRÕES SE MISTURAM | Vários padrões de onda se misturam lá dentro, e o mapa de manchas fica irregular. |
| assenta / derrete 142,0 s | o relevo assenta no chocolate | Por isso é uma estimativa, não uma medida de laboratório. Mesmo assim, chega pertinho. |

## C06 · Por que o prato gira (148–165 s)

| Estado (preview v3) | Na tela | Fala |
|---|---|---|
| **C06** 148,0 s | POR QUE O PRATO GIRA | E é por isso que o prato gira. |
| prato 150,0–160,0 s | o prato gira; as manchas viram anéis | Ele leva a comida pelas regiões quentes e pelas frias, e as manchas viram anéis. |
| ~157,0 s | anéis | Por isso, comida em anel costuma ajudar, mas depende do forno. |
| centro 160,0–163,0 s | anel do centro; CENTRO PARADO | Só o centro não sai do lugar, então não ganha essa média. |

## C07 · Fecho e desafio (165–176 s)

| Estado (preview v3) | Na tela | Fala |
|---|---|---|
| macro 165,0 s (manchete 165,3 s) | volta o macro do C01; ESSAS MANCHAS MEDIRAM A VELOCIDADE DA LUZ | Essas manchas mediram a velocidade da luz. |
| desafio 167,5 s | DESAFIO; `f = 915 MHz`; `d = ?`; NO MODELO IDEAL | Desafio: com novecentos e quinze megahertz, qual a distância entre as manchas? |
| endcard 172,0 s → 176,0 s | `@labparallax` | Se isso te ajudou, segue o Parallax Lab. |

## Texto corrido (sem tags; tags no `narracao_tags_v2.md`, depois da aprovação)

**C01.** Dá pra medir a velocidade da luz com um micro-ondas e uma barra de chocolate? Parece piada, mas essas manchas medem a velocidade da luz. Na etiqueta, a frequência: dois mil quatrocentos e cinquenta megahertz. Fecha a porta, põe o chocolate no forno com o prato parado. Em três passos: primeiro, a onda dentro do forno. Segundo, o calor, que derrete o chocolate. Terceiro, a conta.

**C02.** O forno solta micro-ondas, da mesma família da luz. Elas batem na parede de metal e voltam. Somando a que vai com a que volta, sai uma onda que não anda. Ela só sobe e desce no lugar: é a onda estacionária. Nos nós, o campo elétrico fica sempre zero. Nos ventres, ele oscila com toda a força. Repara: ele sobe, desce e troca de sentido o tempo todo.

**C03.** Agora vem o pulo do gato: o que esquenta é o campo elétrico ao quadrado. Aponta pra cima, depois pra baixo... e esquenta igual, porque o quadrado não liga pro sinal. Esse aquecimento pulsa rápido; o que importa é a média do quadrado. Resultado: um pico de calor em cada ventre. De um ventre ao próximo não cabe uma onda inteira, cabe meia. Uma mancha a cada meio comprimento de onda.

**C04.** Agora a conta. Digamos que a régua marque seis vírgula um centímetros entre duas manchas. Isso é meio comprimento de onda, então a onda inteira tem o dobro: doze vírgula dois. A etiqueta dá a frequência: dois mil quatrocentos e cinquenta megahertz. São quase dois bilhões e meio de oscilações por segundo. A cada oscilação, a onda anda um comprimento de onda. Então a velocidade é o comprimento de onda vezes a frequência. Como o comprimento de onda é o dobro da distância: duas vezes a distância vezes a frequência. Colocando os números... Praticamente trezentos milhões de metros por segundo. A velocidade da luz!

**C05.** Só que tem um detalhe: o forno de verdade não é uma linha, é uma caixa. Vários padrões de onda se misturam lá dentro, e o mapa de manchas fica irregular. Por isso é uma estimativa, não uma medida de laboratório. Mesmo assim, chega pertinho.

**C06.** E é por isso que o prato gira. Ele leva a comida pelas regiões quentes e pelas frias, e as manchas viram anéis. Por isso, comida em anel costuma ajudar, mas depende do forno. Só o centro não sai do lugar, então não ganha essa média.

**C07.** Essas manchas mediram a velocidade da luz. Desafio: com novecentos e quinze megahertz, qual a distância entre as manchas? Se isso te ajudou, segue o Parallax Lab.

## Ordem de cortes

Se a primeira tomada passar de ~165 s, cortar nesta ordem: (1) "Repara: ele sobe, desce e troca de sentido…" (C02); (2) "Por isso, comida em anel costuma ajudar, mas depende do forno." (C06); (3) "São quase dois bilhões e meio de oscilações por segundo." (C04). **Nunca cortar:** a pergunta de abertura, os três passos, "o quadrado não liga pro sinal", "meio comprimento de onda", o "estimativa, não medida de laboratório" e o desafio.
