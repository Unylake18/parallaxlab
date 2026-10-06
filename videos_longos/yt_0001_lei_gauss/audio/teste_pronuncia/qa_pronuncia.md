# yt_0001 — teste de pronúncia (ElevenLabs)

Fase: só pronúncia. Não mexer em cena, ficha (seção 12), tempos ou Git; não gerar os 16 minutos.

## Como gerar

- **Mesma voz e configuração** dos vídeos curtos (ElevenLabs Studio).
- Texto: `texto_teste.txt` desta pasta. São 10 frases, uma por parágrafo; a linha em branco entre elas dá a pausa curta.
- Exportar como `teste_pronuncia_v1.wav` (ou `.mp3`) **nesta pasta**. Se precisar refazer, gerar `_v2`, `_v3` sem
  apagar as anteriores.

## O que ouvir

| # | Frase | Termo-alvo | Critério | Soou como | OK? |
|---|---|---|---|---|---|
| 1 | O d ômega mede a abertura angular. | d ômega | "ômega" em português, sem "omega" inglês | | |
| 2 | Agora entra o d ômega orientado. | d ômega orientado | "orientado" colado naturalmente em "d ômega" | | |
| 3 | Todas as direções somam quatro pi esterradianos. | esterradianos | sem separar nem engolir sílabas (es-ter-ra-di-a-nos) | | |
| 4 | O elemento tem lado r linha seno de teta d fi. | r linha, teta, fi | "r linha" nítido; "teta" e "fi" em português | | |
| 5 | Aqui aparece rô de r. | rô | "rô", nunca "rho" inglês | | |
| 6 | Dividido por épsilon zero. | épsilon | tônica em "É" (É-psi-lon) | | |
| 7 | A direção é dada por n chapéu. | n chapéu | "ene chapéu" compreensível | | |
| 8 | A área projetada é d A perpendicular. | d A perpendicular | "dê á perpendicular", sem leitura estranha de símbolo | | |
| 9 | R maiúsculo é o raio da esfera física; r é o raio da gaussiana; e r linha é a variável da integral. | R × r × r linha | os três claramente distintos na frase corrida | | |
| 10 | r chapéu ponto n chapéu determina o sinal. | r chapéu ponto n chapéu | compreensível em velocidade normal | | |

## Se algum termo falhar

Não mexer na matemática da tela. Trocar **só a grafia enviada ao TTS** (a ficha e a tela ficam como estão) e regerar
apenas as frases que falharam. Variantes para tentar, na ordem:

| Termo | 1ª variante | 2ª variante |
|---|---|---|
| d ômega | dê ômega | dê-ômega |
| esterradianos | esterradiânos | estéreo-radianos |
| r / r linha | erre / erre linha | érre linha |
| R maiúsculo | erre maiúsculo | erre grande *(muda a fala; só se nada mais resolver)* |
| teta | téta | |
| fi | fí | |
| rô | rô (com acento explícito) | rhô → evitar; usar "rô" isolado entre vírgulas |
| épsilon | épsilon (com acento explícito) | é-psilon |
| n chapéu | ene chapéu | |
| d A perpendicular | dê á perpendicular | dê-á perpendicular |
| r chapéu ponto n chapéu | erre chapéu ponto ene chapéu | erre chapéu escalar ene chapéu |

Em teste anterior (vid_0011), a solução que funcionou foi a mesma: grafia de fala no texto do TTS ("Máier") com a forma
correta mantida na tela.

## Registro (preencher)

| Frase | Como a voz pronunciou | Variante que resolveu |
|---|---|---|
| | | |

## Entrega

1. áudio do teste nesta pasta;
2. termos aprovados;
3. termos que precisaram de ajuste;
4. grafia final recomendada para o TTS (vira a tabela "Como falar as grandezas" da `narracao_sugestao.md` e o texto
   enviado ao ElevenLabs; a seção 12 da ficha mantém a grafia normal).

Depois: seção 12 da ficha → remapeamento (inclui afastar `dΩ_or = +dΩ` da borda tracejada e remover o resíduo visual
de Poisson/condutores) → voz por blocos → sincronia fina.
