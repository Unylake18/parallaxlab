# vid_0011 — sugestão de narração (rascunho para revisar com o GPT)

POR TRÁS DA FÓRMULA · EP. 04 — de onde vem `PV^γ = constante`. Preview V3 silencioso de 169,5 s.
Versão 2, com os ajustes do GPT. Tom e ritmo seguem os vídeos 7, 8, 9 e 10: frases curtas, conectivos ("agora", "então", "só que", "por isso",
"falta"), uma ideia por frase, grandezas ditas por extenso, resultados repetidos em palavras.
Princípio do episódio: **a voz explica o porquê; o Manim mostra o como.** A voz não lê a lousa.

## Como falar as grandezas (nada de letras soltas)

| Na tela | Na fala |
|---|---|
| P, V, T | **pressão**, **volume**, **temperatura** |
| U, dU | **energia interna**, **variação da energia interna** |
| δQ, δW | **calor**, **trabalho** |
| n | **número de mols** |
| C_V | **calor específico molar a volume constante** (depois: "o calor específico a volume constante") |
| C_P | **calor específico molar a pressão constante** (depois: "a pressão constante") |
| R | **constante universal dos gases** (depois: "a constante dos gases") |
| γ | **gama**, sempre definido como a **razão entre os dois calores específicos** na 1ª vez |
| C_P − C_V = R | **relação de Máier** (grafia de fala; a tela mostra Mayer) |
| TV^(γ−1) = cte | **temperatura vezes volume elevado a gama menos um é constante** |
| PV^γ = cte | **pressão vezes volume elevado a gama é constante** |
| P_ad < P_iso | **a pressão da adiabática fica menor que a da isotérmica** |
| dU, dT, dV | "uma pequena variação de…" (nunca "dê u", "dê tê") |

Evitar: ler símbolos ou índices; dizer "lentamente" como se isso bastasse para a expansão ser reversível
(o texto diz "aos poucos" e "quase estática, sem dissipação"); atribuir a relação de Mayer à hipótese de
gama constante (ela vale para o gás ideal; o gama constante só entra na integração).

## Narração por bloco

Tempos do preview V3; a voz vai ajustar a cena por âncoras (como nos vídeos 8, 9 e 10). `[...]` = trecho
cortável se a voz ficar longa demais. As contagens de palavras estão no fim.

**1. Problema físico (0–15 s)**
Tela: cilindro isolado, pistão sem atrito, pesos pequenos saindo; `δQ = 0`; pergunta.
> Imagine um gás ideal num cilindro isolado, com um pistão sem atrito e pequenos pesos em cima. Vamos tirando os pesos aos poucos, e o gás se expande sem receber calor. Então, de onde vem a energia para empurrar o pistão?

**2. Primeira lei (15–35 s)**
Tela: `dU = δQ − δW`; o calor sai da equação; `δW` vira `P dV`; caixa `dU = −P dV`; volume sobe, energia interna e temperatura descem.
> Pela primeira lei da termodinâmica, a variação da energia interna é o calor recebido menos o trabalho realizado. Como não há troca de calor, e a expansão é quase estática e sem dissipação, sobra o trabalho: a pressão vezes a variação do volume. Na expansão, o gás realiza trabalho à custa da própria energia interna. Por isso, ele esfria.

**3. Energia interna e temperatura (35–55 s)**
Tela: `U = U(T)` (gás ideal); "como U muda quando T muda?"; definição de `C_V` (a derivada parcial vira derivada total); `dU = nC_V dT`; as duas equações se juntam; `PV = nRT` → `P = nRT/V`.
> Agora, o gás ideal: a energia interna depende só da temperatura. Então, quanto ela muda quando a temperatura muda? Essa taxa, por mol, define o calor específico a volume constante. Assim, uma pequena variação da energia interna é o número de mols, vezes esse calor específico, vezes a variação da temperatura. [E isso vale mesmo quando o volume muda.]

**4. Ligando temperatura e volume (55–68 s)** — a voz quase não fala: o Manim carrega
Tela: `P` substituído por `nRT/V`; `n` cancela; `T` atravessa a igualdade; `dV` sobe sobre `V`; caixa `C_V dT/T = −R dV/V`.
> Agora é álgebra: a pressão sai da conta, e cada termo vai para o lado certo. No fim, temos uma relação direta entre as mudanças de temperatura e volume. Mas ainda falta entender de onde surge o gama.

**5. Relação de Mayer (68–90 s)**
Tela: dois recipientes (volume constante × pressão constante); calor entra nos dois; temperatura sobe igual; barras de energia (ΔU nos dois, trabalho só no pistão); `δQ_V = nC_V dT` e `δQ_P = nC_P dT`; `P dV → nR dT`; cancelamento; caixa `C_P − C_V = R`.
> Para isso, falta um resultado: a relação de Máier. Compare dois gases que esquentam o mesmo tanto. A volume constante, não há trabalho, e toda a energia vai para a energia interna. A pressão constante, o gás também empurra o pistão, então precisa de mais energia para esquentar igual. Para um gás ideal, essa diferença entre os calores específicos é a constante universal dos gases.

**6. O gama (90–100 s)**
Tela: `γ = C_P/C_V`; `γ − 1 = C_P/C_V − 1 = (C_P − C_V)/C_V`; o `C_P − C_V` vira `R` (copiado da caixa de Mayer); caixa `γ − 1 = R/C_V`.
> Chamamos de gama a razão entre esses dois calores específicos. E, por Máier, a constante dos gases dividida pelo calor específico a volume constante é gama menos um.

**7. Integração (100–125 s)**
Tela: a relação de temperatura e volume volta com `(γ − 1)`; caixa "γ ≈ constante no intervalo"; integrais; `C` constante de integração; `ln(TV^(γ−1)) = C`; caixa `TV^(γ−1) = cte`; `V↑ ⇒ T↓`.
> Voltando à relação entre temperatura e volume, agora com o gama. Se o gama puder ser considerado aproximadamente constante nesse intervalo, a gente integra os dois lados. O resultado é este: a temperatura vezes o volume elevado a gama menos um é constante. Esse já é um resultado importante: quando o gás se expande, a temperatura precisa cair.

**8. Resultado final (125–140 s)**
Tela: `T = PV/nR` substitui o `T` dentro da expressão; `V·V^(γ−1) → V^γ`; `nR` entra na constante; caixa `PV^γ = cte` em destaque.
> Por fim, usamos de novo o gás ideal para eliminar a temperatura. E aí está: pressão vezes volume elevado a gama é constante. Resumindo: sem calor, o trabalho sai da energia interna; o gás ideal liga temperatura e volume; e Máier traz o gama. A fórmula não foi imposta: ela nasceu das condições físicas do processo.

**9. Adiabática × isotérmica (140–160 s)**
Tela: dois pistões expandem juntos do mesmo estado até o mesmo volume final; seta de calor entrando na isotérmica (`δQ > 0`, `T = cte`), nenhum calor na adiabática (`δQ = 0`, `T ↓`); pontos nas curvas; linha tracejada em `V_f`; `P_ad < P_iso`.
> Na isotérmica, entra calor para compensar o trabalho realizado pelo gás e manter a temperatura constante. Na adiabática, não. O trabalho reduz a energia interna do próprio gás. Por isso ele esfria, e a pressão cai mais. No mesmo volume final, a pressão da adiabática é menor.

**10. Fechamento (160–170 s)**
Tela: pistão, gráfico e caixa `PV^γ = constante` convergem; "gás ideal · adiabático reversível · γ aproximadamente constante".
> E isso aparece no mundo real. Num motor a diesel, comprimir o ar o esquenta o bastante para acender o combustível. [E o gama corrigiu o cálculo de Newton para a velocidade do som.] A fórmula não é o começo da história. É a consequência dela. Vale para um gás ideal, num processo adiabático reversível, com gama aproximadamente constante. [Se curtiu, siga o Parallax Lab.]

## Contagem (versão 2 do texto; a v3 está em `texto_narracao.txt`)

| Bloco | Janela | Palavras | Palavras/s |
|---|---|---|---|
| 1 | 0–15 s (15 s) | 41 | 2.73 |
| 2 | 15–35 s (20 s) | 59 | 2.95 |
| 3 | 35–55 s (20 s) | 51 | 2.55 |
| 4 | 55–68 s (13 s) | 33 | 2.54 |
| 5 | 68–90 s (22 s) | 65 | 2.95 |
| 6 | 90–100 s (10 s) | 28 | 2.80 |
| 7 | 100–125 s (25 s) | 59 | 2.36 |
| 8 | 125–140 s (15 s) | 36 | 2.40 |
| 9 | 140–160 s (20 s) | 47 | 2.35 |
| 10 | 160–170 s (10 s) | 31 | 3.10 |
| **Total** | 170 s | **450** | 2.65 |

## Notas de gravação

- **Ordem de trabalho:** gerar a voz nesta versão, sem time-stretch nem aceleração; medir a duração real de cada bloco; encaixar as quatro pausas; só então decidir cortes adicionais. Alvo: 2:47–2:54 (2:55–2:58 se resolve com cortes pequenos; acima de 3:00, mexer no texto).
- **Meta de palavras:** 455–470, não ocupar os 170 s com fala; este episódio pede tempo de contemplação das equações.
- **Pausas reais (sem fala) depois dos quatro payoffs:** `dU = −P dV`, `C_P − C_V = R`, `TV^(γ−1) = cte` (0,4–0,8 s cada) e `PV^γ = cte` (perto de 1 s). Não pedir ao TTS que corra de ponta a ponta.
- **Velocidade natural:** se a primeira voz der 2:53–2:56, não acelerar; ainda há texto para cortar. Perto de 2:45–2:50 está ótimo.
- **O que a voz não duplica:** o `nR` sendo absorvido pela constante (bloco 8) e a junção das duas equações (bloco 3) ficam só na tela.
- **Bloco 7:** "Esse já é um resultado importante" dá peso a `TV^(γ−1)` sem comentar a estrutura da aula.
- **Bloco 9:** a frase de abertura ("compare com uma expansão isotérmica, do mesmo estado ao mesmo volume final") foi cortada; os dois pistões partindo juntos e o `V_f` tracejado já orientam a comparação.
- **Bloco 10:** se a pausa de ~1 s depois de `PV^γ = cte` não couber nos 10 s, cortar o CTA falado (o fechamento conceitual vale mais); ele pode entrar só visualmente.
- **Terminologia a testar no TTS:** "calor específico a volume constante" (com "por mol" no bloco 3) versus "calor específico molar a volume constante"; decidir uma forma e usar nas duas citações.
- **CTA** mantido por consistência com o vid_0010.

## Versão 3 (depois da primeira voz: 2:38)

- A voz de 450 palavras deu 2:38 (≈ 2,85 palavras/s, já com as pausas naturais). Faltava didática, uma síntese da álgebra e o "e daí?".
- **Base (`texto_narracao.txt`, ≈ 489 palavras, ≈ 2:52):** bloco 4 diz o que a álgebra faz; bloco 8 ganha a síntese ("sem calor, o trabalho sai da energia interna; o gás ideal liga temperatura e volume; Máier traz o gama"); bloco 10 ganha a aplicação do motor a diesel.
- **Opcionais, entre colchetes (+~9 s se todos):** "E isso vale mesmo quando o volume muda" (+8 palavras), Newton e a velocidade do som (+12), CTA falado (+6). Com só Newton: ≈ 501 palavras, ≈ 2:56.
- Teto absoluto de 3:00; as quatro pausas de payoff (+~3 s) precisam caber.
- **A cena precisa de novos beats**: um cartão de síntese após o payoff do bloco 8 (os quatro resultados em sequência) e imagens leves para diesel (e Newton, se entrar). Ainda não implementados.
