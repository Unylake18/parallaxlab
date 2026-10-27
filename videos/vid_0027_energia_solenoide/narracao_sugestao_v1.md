# vid_0027 — sugestão de narração v1 (quadro a quadro, sobre o preview v3)

Base: `renders/vid_0027_preview_v3_540x960.mp4` (175,1 s). Tempos = estados do preview (a voz estica a cena depois).
Estilo: `docs/roteiro_voz_elevenlabs_v4.md` (professor de cursinho, variáveis pelo nome, sem ler fórmula letra a letra).
Teto: vídeo final com voz < 180 s. Orçamento: ~2,7 palavras/s ⇒ no máximo ~440 palavras faladas.
Cuidados de física: ½LI² é a energia guardada quando a corrente vale I (entrou enquanto ela subia); u_B = B²/2μ₀ é
resultado geral, não deduzido aqui; as duas rotas *conferem*, não é descoberta; "trecho longe das pontas".

| Estado (preview v3) | Na tela | Fala |
|---|---|---|
| **C01** 0,0 s | solenoide, corrente correndo; título | Onde fica a energia de um indutor? |
| C01 4,8 s | apostas `NO FIO?` / `NO ESPAÇO?` | No fio... ou no espaço dentro dele? |
| **C02** 8,0 s | rótulo I + definição | Pensa num solenoide bem longo, com núcleo de ar, e uma corrente passando por ele. |
| C02 ~11 s | raio a | Ele tem um raio... |
| C02 ~14 s | n sobre as espiras | ...e um certo número de espiras em cada metro. |
| C02 ~16 s | chave h + chip | A gente olha só um trecho, longe das pontas. |
| **C03** 18,7 s | `LEI DE AMPÈRE`, ∮B·dℓ = μ₀I_int | Primeiro, o campo. A lei de Ampère: somando o campo ao longo de um caminho fechado, o resultado é mi zero vezes a corrente que atravessa esse caminho. |
| C03 26,1 s | laço + setas de B | Escolhendo este retângulo, só o lado de dentro conta: lá o campo acompanha o caminho. Nos outros lados, ou ele é perpendicular, ou é praticamente zero. |
| C03 27,7 → 29,3 s | integral vira Bℓ | Então a soma vira só campo vezes o comprimento do lado. |
| C03 ~31 s | I_int = (nℓ)I; ⊙ dentro do laço acendem | E a corrente que atravessa o laço? São as espiras dentro dele, cada uma com a corrente. |
| C03 36,0 → 38,7 s | ℓ cancela; B = μ₀nI | O comprimento aparece dos dois lados... e cancela. O campo dentro é uniforme: mi zero vezes as espiras por metro vezes a corrente. |
| **C04** 40,7 s | disco A; Φ = ∫B·dA | Agora, o fluxo: quanto campo atravessa a área de uma espira. |
| C04 48,9 s | B sai da integral | Como o campo é uniforme e perpendicular ao disco, ele sai da integral... |
| C04 52,6 s | Φ = BA | ...e sobra só a área do disco. |
| C04 55,3 → 58,3 s | Φ = μ₀nIπa² | Fluxo por espira: o campo vezes pi vezes o raio ao quadrado. |
| **C05** 60,3 s | disco se replica ao longo de h | Só que o trecho tem muitas espiras... |
| C05 65,6 s | Λ = Φ₁ + Φ₂ + … + Φ_N | ...e o fluxo concatenado soma o fluxo de cada uma. |
| C05 67,8 → 69,3 s | Λ = NΦ | Como todas enxergam o mesmo fluxo, é esse fluxo vezes o número de espiras do trecho. |
| C05 ~71 s | N = nh | E esse número é espiras por metro vezes o comprimento do trecho. |
| C05 74,5 → 78,5 s | NΦ = μ₀n²Iπa²h | O mesmo fluxo, N vezes. |
| **C06** 80,5 s | `INDUTÂNCIA`, L = NΦ/I | Daí sai a indutância: fluxo concatenado dividido pela corrente. A unidade é o henry. |
| C06 86,3 → 92,9 s | substitui; I cancela; L = μ₀n²πa²h | Substituindo... a corrente cancela. A indutância só depende da geometria. |
| C06 ~95 s | os dois n destacados | Repara nas espiras por metro ao quadrado: uma vem do campo, a outra, do número de espiras. |
| **C07** 99,7 s | corrente sobe de zero; ε_L = −L dI/dt | Agora, a energia pelo circuito. Enquanto a corrente sobe, o indutor reage com uma força eletromotriz contra essa variação. |
| C07 ~105 s | P = abs(ε_L)·I = LI dI/dt | Para vencê-la, a fonte entrega uma potência: indutância vezes corrente vezes a taxa com que a corrente sobe. |
| C07 110,3 s | dU_B = P dt = LI dI | Em cada instante, a energia guardada cresce um pouquinho. |
| C07 114,9 s | integral de 0 a I = ½LI² | Somando tudo, de corrente zero até I, chegamos a meio vezes indutância vezes corrente ao quadrado. É a energia guardada quando a corrente vale I. |
| C07 119,9 → 124,5 s | substitui L; resultado fixado no topo | Com a indutância do solenoide, fica esta expressão. Guarda ela aí em cima. |
| **C08** 125,3 s | `DENSIDADE DE ENERGIA`, u_B = dU_B/dV | Agora, pelo campo. Densidade de energia é a energia por unidade de volume. |
| C08 ~129 s | volume acende; u_B = B²/2μ₀ (resultado geral) | E o eletromagnetismo dá o valor geral: campo ao quadrado sobre duas vezes mi zero. |
| C08 ~133 s | U_B = ∫u_B dV | A energia total soma essa densidade em cada pedacinho de volume. |
| C08 137,3 s | ∫ vira u_B V; seção varre h | Aqui ela é igual em todo o interior e zero fora: densidade vezes volume. E o volume é a área do disco ao longo do trecho. |
| C08 143,1 → 147,9 s | troca u_B e B = μ₀nI | Trocando o campo por mi zero vezes espiras por metro vezes corrente... |
| C08 148,7 → 154,9 s | abre o quadrado; μ₀ cancela | ...um mi zero de cima cancela com o de baixo. |
| **C09** 156,9 s | reorganiza: mesma forma do topo | Reorganizando, aparece a mesma expressão da rota do circuito. |
| C09 163,3 s | ½LI² = u_B V | As duas contas conferem. |
| C09 167,9 s | fio apaga, volume fica aceso | E a resposta: o fio só conduz a corrente. A energia está no campo, dentro do solenoide. |
| **C10** 171,1 s | @labparallax | Segue o Parallax Lab! |

Contagem: ~400 palavras ⇒ ~150 s de fala a 2,7 palavras/s; com pausas e transições, o vídeo final deve ficar por volta de
170–178 s. Se a primeira tomada passar de 180 s, cortar na ordem: frase dos dois n (C06); "Guarda ela aí em cima" (C07);
"Ele tem um raio..." (C02).
