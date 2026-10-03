# vid_0012 — narração e notas de gravação

EXERCÍCIO RESOLVIDO · EP. 05. Texto para o TTS em `texto_narracao.txt`: 14 parágrafos, um por bloco da tabela abaixo (variáveis por extenso: E → "o campo", r → "a distância (ao centro)", R → "o raio", ρ0 → "a densidade central", dA → "área"; só "épsilon zero" e "pi" ficam com o nome). As janelas são as do preview silencioso final (170,9 s), medidas pelas trocas de título no render; a voz real manda no tempo final. Pal/s é só pré-QA: fórmulas faladas e pausas do TTS não seguem esse ritmo.

## Notas de gravação

- Uma tomada única com os 14 parágrafos, mesma voz/configuração dos vídeos 0010 e 0011 (prosódia contínua). Não acelerar a voz para caber.
- Antes da tomada completa, teste curto com quatro frases: "a distância sobre duas vezes o raio", "a distância vale dois terços do raio", "quatro pi vezes a densidade central", "sobre épsilon zero". A tela mantém r, R, E; a voz usa os nomes.
- Pausas perceptíveis (≈ 0,6–0,8 s) depois do gancho, de "É uma parábola côncava para baixo", e de "…a carga encerrada passa a crescer devagar demais… Então o campo cai". Depois de "r vale dois terços de R" e do payoff, respiro maior (≈ 1–1,5 s): a cena segura 1,5 s no quadro de r = 2R/3.
- Não narrar os cancelamentos de 4π e r² nem as primitivas: ficam na animação.
- Interpretação: o argumento é o crescimento relativo da carga encerrada frente a r², não "entra pouca carga" (em termos absolutos, a casca perto da borda carrega mais carga que a do centro; ver divergência na `ficha.md`).
- Se a voz extrapolar: primeiro ganhar 0,5–1 s no vídeo (Cascas, Integral, Campo interno são os mais apertados); só cortar texto se o desvio for maior (primeiro as checagens).

## Blocos (janelas medidas) e âncoras previstas

| Janela | Bloco | Palavras | Pal/s | Na tela |
| --- | --- | --- | --- | --- |
| 0,0–10,5 | Gancho | 30 | 2,86 | esfera uniforme, campo crescendo, pergunta |
| 10,5–20,5 | Setup | 22 | 2,20 | ρ(r) = ρ0(1 − r/R), simetria |
| 20,5–48,0 | Gauss | 81 | 2,95 | gaussiana, n̂, d⃗A, E∥dA, E·4πr² = Q_enc/ε0 |
| 48,0–60,0 | Cascas | 36 | 3,00 | casca r' e dr', dV, dQ |
| 60,0–69,7 | Integral | 28 | 2,89 | Q_enc(r) |
| 69,7–81,4 | Campo interno | 32 | 2,74 | E_in(r) e o gráfico nasce |
| 81,4–95,1 | Externo | 38 | 2,77 | r = R, Q total, E_out |
| 95,1–103,5 | Virada | 25 | 2,98 | função por partes, "o exercício ainda não acabou" |
| 103,5–125,8 | Derivada | 62 | 2,78 | dE/dr termo a termo, tangente, r = 2R/3 |
| 125,8–133,3 | Payoff | 21 | 2,80 | esfera/gaussiana/ponto em 2/3 (inclui 1,5 s de respiro) |
| 133,3–151,5 | Interpretação | 52 | 2,86 | centro × borda por Δr |
| 151,5–158,0 | Checagens | 18 | 2,77 | E(0)=0, E(R⁻)=E(R⁺), E→0 |
| 158,0–166,6 | Recap | 24 | 2,79 | Gauss → Q_enc → E(r) → dE/dr = 0 → r_max = 2R/3 + frase final |
| 166,6–170,9 | CTA | 6 | 1,40 | logo + @labparallax |

Âncoras por palavra para a sincronização (depois do áudio real): "vetor normal" → n̂; "vetor de área" → d⃗A; "paralelos" → E⃗∥d⃗A; "quatro pi r ao quadrado" → E·4πr²; "cascas finas" → casca; "parábola côncava para baixo" → gráfico interno visível; "termo a termo" → início da derivação; "a derivada vale zero" → tangente horizontal; "dois terços do raio" → payoff 2R/3; "no começo" e "perto da borda" → respectivas animações; "Gauss deu" → início do recap; "arroba labparallax" → handle visível.
