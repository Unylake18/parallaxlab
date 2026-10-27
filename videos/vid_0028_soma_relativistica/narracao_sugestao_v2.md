# vid_0028 — narração sugerida v2 (quadro a quadro, sobre o preview v6)

Base: `renders/preview_v6_540x960.mp4` (152,0 s, silencioso). Os estados e tempos são os do preview; a voz estica as cenas depois.
Estilo: `roteiro_voz_elevenlabs_v4.md` (professor de cursinho, variáveis pelo nome, uma tag por trecho, sem `[slowly]`).
Teto: vídeo final com voz **< 180 s**. Voz real: 2,7–3,0 palavras/s.

Esta v2 revisa a v1 (467 palavras, 156–173 s, sem folga). Mudanças e motivos:

1. **"Lorentz corrige Galileu" saiu.** Contraria a regra congelada ("a fórmula não corrige Galileu"; Galileu é o limite de baixas velocidades). Agora: "entra um fator, a letra grega gama".
2. **Conta do denominador reescrita.** "Mais vezes menos dá menos; menos com menos dá mais" soava embaralhado. Agora: "o produto é negativo, então o menos vira mais: um vírgula sessenta e quatro".
3. **Fórmula falada mais clara:** "o produto das duas velocidades dividido pela luz ao quadrado".
4. **Fecho cobre o que a tela diz:** entra "um corpo com massa fica sempre abaixo da luz" (a tela mostra `CORPOS COM MASSA: v < c`).
5. **"não é o que A mede de B"** no C03 (sem "nenhum foguete"): uma ideia só, mais curta.
6. **Enxugado para 439 palavras** (28 a menos que a v1): 146–163 s de fala a 2,7–3,0 palavras/s; com pausas e reticências ~155–172 s. Folga de ~8–25 s abaixo de 3 min. Se a primeira tomada passar de ~165 s, ver a ordem de cortes no fim.
7. "a luz" só depois de dizer "velocidade da luz" uma vez (a primeira vez no hook).

Falado × tela: 0,8c → "oitenta por cento da velocidade da luz" (depois "da luz"); 1,6c → "um vírgula seis vezes a velocidade da luz"; 0,976c → "noventa e sete vírgula seis por cento da luz"; dx → "deslocamento"; dt → "intervalo de tempo"; v_B′ → "a velocidade de B medida por A". Nunca "c" solto, nunca "dx"/"dt" soletrados. γ: "a letra grega gama" (uma vez).

## Abertura (o que importa: em ~22 s quem chega entende o que vai assistir)

Ordem fixa: cena → pergunta → palpite → "não é" → promessa com os três passos que ficam no topo.

| Estado (preview v6) | Na tela | Fala |
|---|---|---|
| **C01** 0,0 s | cold open: dois foguetes, um na direção do outro | Dois foguetes vêm um contra o outro... |
| setas 3,6 s / setup 4,7 s | `+0,8c` / `−0,8c`; CADA UM A 0,8c EM RELAÇÃO À TERRA | ...Para a Terra, cada um vai a oitenta por cento da velocidade da luz. |
| pergunta 7,0 s / slot 8,6 s | QUE VELOCIDADE O FOGUETE A MEDE PARA O FOGUETE B?; `v_B′ = ?` | Que velocidade o foguete A mede para o foguete B? |
| palpite 10,2 s | PALPITE `0,8c + 0,8c = ?` | O palpite é somar: cento e sessenta por cento da luz... |
| nao_e_16 12,0 s | A RESPOSTA NÃO É 1,6c | ...mas a resposta não é essa. |
| promessa 13,6 s | NESTE VÍDEO: DE ONDE VEM A REGRA QUE COMPÕE VELOCIDADES PERTO DA LUZ | Neste vídeo você vai ver de onde vem a regra que compõe velocidades perto da luz... |
| chips 15,2 s | ① REFERENCIAL ② FÓRMULA ③ RESULTADO | ...em três passos: referencial, fórmula e resultado. |

## Desenvolvimento

| Estado (preview v6) | Na tela | Fala |
|---|---|---|
| **C02** 19,0 s → troca_A 21,5 s | tag TERRA → FOGUETE A; a Terra ganha a seta −0,8c | Passo um: o referencial. Para A, ele está parado... |
| nota 23,9 s | A EM REPOUSO / A TERRA SE MOVE PARA TRÁS; `v_B′ = ?` em B | ...e é a Terra que anda para trás. Queremos a velocidade de B medida por A. |
| **C03** 29,0 s → vet2 33,6 s | volta à Terra; régua; 0,8c + 0,8c em fila | Na Terra, as duas setas em fila dão um vírgula seis vezes a velocidade da luz: |
| fecha / na_terra 34,8 s | colchete; NA TERRA A SEPARAÇÃO FECHA A 1,6c | é o ritmo com que a distância entre eles diminui, medido na Terra. |
| nao_e 37,4 s | MAS ISSO NÃO É O QUE A MEDE DE B | Não é o que A mede de B. |
| **C04** 42,2 s | DE ONDE VEM A FÓRMULA? | Passo dois: a fórmula. |
| anda 44,2 s → vb_def 48,3 s | cronômetro dt; seta dx; `v_B = dx/dt` (NA TERRA) | Na Terra, B percorre um deslocamento num intervalo de tempo: a velocidade de B é um sobre o outro. |
| a_anda 50,2 s | A anda `v_A·dt` | A percorre a velocidade dele vezes esse tempo... |
| rel_gal 52,2 s / mistura 54,4 s | `dx − v_A dt`; ISSO É GALILEU. PERTO DE c, ESPAÇO E TEMPO SE MISTURAM | ...então, para A, B anda a diferença. Isso é Galileu. Só que, perto da luz, espaço e tempo se misturam. |
| defs 56,8 s | NA TERRA `v_B = dx/dt` · MEDIDO POR A `v_B′ = dx′/dt′` | Para A, a velocidade de B é o deslocamento que ele mede sobre o tempo que ele mede. |
| galileu_eq 58,6 s → lorentz 61,2 s | Galileu vira Lorentz; γ e o termo novo destacados | Entra um fator, a letra grega gama... |
| gama_def 63,4 s | `γ = …`; o tempo de A também depende de onde B está | ...e o tempo de A passa a depender de onde B está. |
| razao / monta 65,4 s | PASSO 1 · MONTAR A RAZÃO | Monta a razão: |
| gama → gama_cancela 69,2 s | γ em cima e embaixo, riscado | o gama aparece em cima e embaixo, e cancela. |
| dt_hint → distribui 73,2 s | ÷ dt; dt/dt = 1 | Divide pelo intervalo de tempo: |
| vb 78,6 s | dx/dt = v_B (NA TERRA) | sobra deslocamento sobre tempo, a velocidade de B. |
| formula / caixa 80,0 s | a fórmula em caixa | Chegamos à regra: a velocidade de B menos a de A, sobre um menos o produto das duas dividido pela luz ao quadrado. |
| **C05** 83,0 s → viajam 86,0 s | os valores voam dos foguetes | Passo três: os números. |
| numerador 88,2 s | `−1,6c` | Em cima, menos um vírgula seis, o mesmo do palpite. |
| sinais → um64 89,6 s | (+)·(−) = (−); c² cancela; `1,64` | Embaixo, produto negativo: o menos vira mais, um vírgula sessenta e quatro. |
| fracao → q4041 97,4 s | `−40/41 c ≈ −0,976c`; ponteiro encolhe | Dividindo: quarenta sobre quarenta e um, noventa e sete vírgula seis por cento da luz. |
| sentido → lupa 100,6 s | o sinal só indica o sentido; módulo ao topo; lupa | O sinal só diz o sentido. |
| **C07** 107,0 s → galileu 113,0 s | carros a ±30 m/s; termo ~10⁻¹⁴; `v_B′ ≈ v_B − v_A` | Com carros a trinta metros por segundo, esse produto é minúsculo, o denominador vira um, e sobra a soma de sempre: Galileu é o limite das velocidades baixas. |
| **C08** 115,5 s → h1 119,4 s | 0,5c cada: 1c × 0,8c | Com cinquenta por cento da luz cada, a soma simples daria a luz; medido por A, oitenta por cento. |
| acelera → menor_c 121,0 s | 0,99c cada: 1,98c × 0,99995c | Com noventa e nove, quase o dobro; medido por A, noventa e nove vírgula nove nove cinco. |
| **C09** 128,0 s → fecha9 129,0 s | Terra: colchete fecha a 1,6c | Resumindo: na Terra, a distância fecha a um vírgula seis vezes a luz, |
| troca9A → cada 130,4 s | A mede B a 0,976c; B mede A a 0,976c | mas cada foguete mede o outro a noventa e sete vírgula seis por cento. |
| fecho1 / fecho2 137,4 s | CORPOS COM MASSA: v < c; NÃO SE SOMAM… | Perto da luz, velocidades não se somam: se acumulam sem chegar lá. Corpo com massa fica sempre abaixo da luz. |
| **C10** 143,0 s | logo + SEGUE O PARALLAX LAB + @labparallax | Se essa conexão entre equação e fenômeno te ajudou, segue o Parallax Lab. |

## Texto corrido (proposta com tags, para gravação depois da aprovação)

O texto para gravar está em `narracao_tags_v1.md` (mesmo texto, seção `## Texto corrido (para gravação)`).

## Ordem de cortes

Se a primeira tomada passar de ~165 s, cortar nesta ordem: (1) "A percorre a velocidade dele vezes esse tempo..." vira "A também anda..."; (2) a frase de cinquenta por cento (o C08 fica só com o de noventa e nove); (3) "Monta a razão:" vira "Monta:". **Nunca cortar:** o hook (foguetes → pergunta → palpite → "não é" → promessa com os três passos), "medido na Terra" do 1,6c, o cancelamento do gama, nem "corpo com massa fica sempre abaixo da luz".
