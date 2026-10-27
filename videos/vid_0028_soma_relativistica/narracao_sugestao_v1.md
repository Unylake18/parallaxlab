# vid_0028 — sugestão de narração v1 (quadro a quadro, sobre o preview v6)

Base: `renders/preview_v6_540x960.mp4` (152,0 s, silencioso). Tempos = estados do preview (a voz estica a cena depois).
Estilo: `docs/roteiro_voz_elevenlabs_v4.md` (professor de cursinho, variáveis pelo nome, sem ler fórmula letra a letra).
Teto: vídeo final com voz < 180 s. Orçamento: ~2,7 palavras/s ⇒ no máximo ~440 palavras faladas.
Física congelada (handoff): sempre "medido por" (nunca "visto por"); o 1,6c é sempre "na Terra" e não é velocidade de
corpo nem o que A mede de B; não nomear simultaneidade, dilatação, contração nem diagramas de espaço-tempo; o
denominador nunca é "relógio mais lento". γ é apresentado uma vez como "a letra grega gama".

Falado × tela: 0,8c → "oitenta por cento da luz"; 1,6c → "um vírgula seis vezes a luz"; 0,976c → "noventa e sete
vírgula seis por cento da luz"; dx → "deslocamento"; dt → "intervalo de tempo"; v_B′ → "a velocidade de B medida por A".

## Abertura (o que importa: em ~20 s quem chega entende o que vai assistir)

Ordem fixa: cena → pergunta → palpite errado → "não é" → promessa com os três passos que ficam no topo da tela.

| Estado (preview v6) | Na tela | Fala |
|---|---|---|
| **C01** 0,0 s | cold open: dois foguetes, um na direção do outro | Dois foguetes, um na direção do outro... |
| setas 3,6 s / setup 4,7 s | `+0,8c` / `−0,8c`; CADA UM A 0,8c EM RELAÇÃO À TERRA | ...cada um a oitenta por cento da luz, medido na Terra. |
| pergunta 7,0 s / slot 8,6 s | QUE VELOCIDADE O FOGUETE A MEDE PARA O FOGUETE B?; `v_B′ = ?` | Que velocidade o foguete A mede para o B? |
| palpite 10,2 s | PALPITE `0,8c + 0,8c = ?` | Somando, daria cento e sessenta por cento da luz... |
| nao_e_16 12,0 s | A RESPOSTA NÃO É 1,6c | ...mas a resposta NÃO é essa. |
| promessa 13,6 s | NESTE VÍDEO: DE ONDE VEM A REGRA QUE COMPÕE VELOCIDADES PERTO DA LUZ | Neste vídeo, você vai ver de onde vem a regra que junta velocidades perto da luz... |
| chips 15,2 s | ① REFERENCIAL ② FÓRMULA ③ RESULTADO | ...em três passos: referencial, fórmula e resultado. |

## Desenvolvimento

| Estado (preview v6) | Na tela | Fala |
|---|---|---|
| **C02** 19,0 s → troca_A 21,5 s | tag TERRA → FOGUETE A; a Terra ganha a seta −0,8c | Passo um: o referencial. Dentro do foguete A, ele está parado... |
| nota 23,9 s | A EM REPOUSO / A TERRA SE MOVE PARA TRÁS; `v_B′ = ?` em B | ...e é a Terra que anda para trás. A velocidade de B medida por A é o número que falta. |
| **C03** 29,0 s → vet2 33,6 s | volta à Terra; régua; 0,8c + 0,8c em fila | Na Terra, as duas setas em fila dão um vírgula seis vezes a luz. |
| fecha / na_terra 34,8 s | colchete; NA TERRA A SEPARAÇÃO FECHA A 1,6c | É o ritmo com que a distância entre eles diminui, medido na Terra. |
| nao_e 37,4 s | MAS ISSO NÃO É O QUE A MEDE DE B | Não é a velocidade de nenhum foguete, nem o que A mede de B. |
| **C04** 42,2 s | DE ONDE VEM A FÓRMULA? | Passo dois: a fórmula. |
| anda 44,2 s → vb_def 48,3 s | cronômetro dt; seta dx; `v_B = dx/dt` (NA TERRA) | Na Terra, B anda um deslocamento num intervalo de tempo: a velocidade de B é um dividido pelo outro. |
| a_anda 50,2 s | A anda `v_A·dt` | No mesmo tempo, A anda a velocidade dele vezes o tempo. |
| rel_gal 52,2 s / mistura 54,4 s | `dx − v_A dt`; ISSO É GALILEU. PERTO DE c, ESPAÇO E TEMPO SE MISTURAM | Para A, B anda a diferença. Isso é Galileu. Só que, perto da luz, espaço e tempo se misturam. |
| defs 56,8 s | NA TERRA `v_B = dx/dt` · MEDIDO POR A `v_B′ = dx′/dt′` | Para A, a velocidade de B é o deslocamento que ele mede sobre o tempo que ele mede. |
| galileu_eq 58,6 s → lorentz 61,2 s | Galileu vira Lorentz; γ e o termo novo destacados | Lorentz corrige Galileu: entra um fator, a letra grega gama... |
| gama_def 63,4 s | `γ = …`; o tempo de A também depende de onde B está | ...e o tempo de A passa a depender de onde B está. |
| razao / monta 65,4 s | PASSO 1 · MONTAR A RAZÃO | Monta a razão... |
| gama → gama_cancela 69,2 s | γ em cima e embaixo, riscado | ...gama aparece em cima e embaixo, e cancela. |
| dt_hint → distribui 73,2 s | ÷ dt; dt/dt = 1 | Divide tudo pelo intervalo de tempo: tempo sobre tempo dá um... |
| vb 78,6 s | dx/dt = v_B (NA TERRA) | ...e deslocamento sobre tempo é a velocidade de B. |
| formula / caixa 80,0 s | a fórmula em caixa | Chegamos na regra: a velocidade de B menos a de A, sobre um menos o produto das duas dividido pela luz ao quadrado. |
| **C05** 83,0 s → viajam 86,0 s | os valores voam dos foguetes | Passo três: os números. |
| numerador 88,2 s | `−1,6c` | Em cima, menos um vírgula seis: o próprio palpite. |
| sinais → um64 89,6 s | (+)·(−) = (−); c² cancela; `1,64` | Embaixo, mais vezes menos dá menos; menos com menos dá mais: um vírgula sessenta e quatro. |
| fracao → q4041 97,4 s | `−40/41 c ≈ −0,976c`; ponteiro encolhe | Dividindo... quarenta sobre quarenta e um: noventa e sete vírgula seis por cento da luz. |
| sentido → lupa 100,6 s | o sinal só indica o sentido; módulo ao topo; lupa | O sinal só diz o sentido: B vem na direção de A. |
| **C07** 107,0 s → galileu 113,0 s | carros a ±30 m/s; termo ~10⁻¹⁴; `v_B′ ≈ v_B − v_A` | No dia a dia, com carros a trinta metros por segundo, esse produto é minúsculo, o denominador vira um, e sobra a soma de sempre. Galileu é o limite das velocidades baixas. |
| **C08** 115,5 s → h1 119,4 s | 0,5c cada: 1c × 0,8c | Com cinquenta por cento da luz cada, a soma simples daria a luz; medido por A, oitenta por cento. |
| acelera → menor_c 121,0 s | 0,99c cada: 1,98c × 0,99995c | Com noventa e nove por cento cada, quase o dobro da luz... medido por A, noventa e nove vírgula nove nove cinco por cento. |
| **C09** 128,0 s → fecha9 129,0 s | Terra: colchete fecha a 1,6c | Resumindo: na Terra, a distância fecha a um vírgula seis vezes a luz. |
| troca9A → cada 130,4 s | A mede B a 0,976c; B mede A a 0,976c | Mas cada foguete mede o outro a noventa e sete vírgula seis por cento. |
| fecho1 / fecho2 137,4 s | CORPOS COM MASSA: v < c; NÃO SE SOMAM… | Perto da luz, velocidades não se somam: se acumulam sem chegar lá. |
| **C10** 143,0 s | logo + SEGUE O PARALLAX LAB + @labparallax | Se essa conexão entre equação e fenômeno te ajudou, segue o Parallax Lab. |

## Texto corrido (proposta com tags, para gravação depois da aprovação)

[curious] Dois foguetes, um na direção do outro... cada um a oitenta por cento da luz, medido na Terra. Que velocidade o foguete A mede para o B?

[thoughtful] Somando, daria cento e sessenta por cento da luz... [thoughtful, emphatic] mas a resposta NÃO é essa.

[curious] Neste vídeo, você vai ver de onde vem a regra que junta velocidades perto da luz... em três passos: referencial, fórmula e resultado.

[thoughtful] Passo um: o referencial. Dentro do foguete A, ele está parado... e é a Terra que anda para trás. A velocidade de B medida por A é o número que falta.

[thoughtful] Na Terra, as duas setas em fila dão um vírgula seis vezes a luz. É o ritmo com que a distância entre eles diminui, medido na Terra. Não é a velocidade de nenhum foguete, nem o que A mede de B.

[curious] Passo dois: a fórmula.

[thoughtful] Na Terra, B anda um deslocamento num intervalo de tempo: a velocidade de B é um dividido pelo outro. No mesmo tempo, A anda a velocidade dele vezes o tempo. Para A, B anda a diferença. Isso é Galileu. Só que, perto da luz, espaço e tempo se misturam.

[thoughtful] Para A, a velocidade de B é o deslocamento que ele mede sobre o tempo que ele mede. Lorentz corrige Galileu: entra um fator, a letra grega gama... e o tempo de A passa a depender de onde B está.

[thoughtful] Monta a razão... gama aparece em cima e embaixo, e cancela. Divide tudo pelo intervalo de tempo: tempo sobre tempo dá um... e deslocamento sobre tempo é a velocidade de B.

[excited] Chegamos na regra: a velocidade de B menos a de A, sobre um menos o produto das duas dividido pela luz ao quadrado.

[curious] Passo três: os números. Em cima, menos um vírgula seis: o próprio palpite. Embaixo, mais vezes menos dá menos; menos com menos dá mais: um vírgula sessenta e quatro.

[short pause] Dividindo... quarenta sobre quarenta e um: noventa e sete vírgula seis por cento da luz. [thoughtful] O sinal só diz o sentido: B vem na direção de A.

[curious] No dia a dia, com carros a trinta metros por segundo, esse produto é minúsculo, o denominador vira um, e sobra a soma de sempre. Galileu é o limite das velocidades baixas.

[thoughtful] Com cinquenta por cento da luz cada, a soma simples daria a luz; medido por A, oitenta por cento. Com noventa e nove por cento cada, quase o dobro da luz... medido por A, noventa e nove vírgula nove nove cinco por cento.

[calm, satisfied] Resumindo: na Terra, a distância fecha a um vírgula seis vezes a luz. Mas cada foguete mede o outro a noventa e sete vírgula seis por cento. [thoughtful, emphatic] Perto da luz, velocidades não se somam: se acumulam sem chegar lá.

[calm, satisfied] Se essa conexão entre equação e fenômeno te ajudou, segue o Parallax Lab.

Se a primeira tomada passar de ~170 s, cortar nesta ordem: (1) "No mesmo tempo, A anda a velocidade dele vezes o
tempo." vira "A também anda."; (2) a frase do caso de cinquenta por cento (C08 fica só com o de noventa e nove);
(3) "Não é a velocidade de nenhum foguete, nem" vira "Não é". Nunca cortar o hook (foguetes → pergunta → palpite →
"não é" → promessa com os três passos), "medido na Terra" do 1,6c nem o cancelamento do gama.
