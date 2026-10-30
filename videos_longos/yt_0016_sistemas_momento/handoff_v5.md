# yt_0016 — avaliação do preview v4 e HANDOFF v5 (rodada da narração)

Data: 2026-10-29. Base: zip do preview v4 (960×540 / 15 fps, 19:52, 64 âncoras), relatório e logs do Claude Code, e a sugestão de
narração v4 do Claude Code. Método: o vídeo inteiro em quadros a cada 3 s; quadros em tamanho cheio em cada ponto suspeito; logs de
travadas, pausas e alinhamento; a narração conferida linha a linha contra a física congelada do handoff v1 (§3) e contra a tela.

(O Anexo A, a narração final, está salvo palavra por palavra em `narracao_final_v4.md`.)

---

## Parte 1 — Avaliação do v4

**Veredito:** o v4 resolveu o que pesava no v3. O hook tem 25 s e o cavalo aparece só no hook, no A5, no T8 e no resumo. As travadas
sumiram (zero no hook e no resumo). O gelo deixou de ficar parado: o cavalo se mexe o tempo todo. O T9 e o T10 rodam uma vez com um
replay. A luz da coda virou feixe amarelo com fótons, placa que esquenta e espelho que devolve. Sobram **18 sobreposições ou colisões de
texto** (tabela 1.1), quase todas pequenas e fáceis, e dois defeitos de animação: o "morph" embaralhado do T7-3 e a DICA que pisca branca.

### 1.1 Sobreposições e colisões (tempos do v4)

| # | Tempo | Bloco | O que acontece | Correção |
|---|---|---|---|---|
| V1 | 1:12–1:35 | A5 | O rótulo `−T⃗` e a ponta da seta ficam em cima da linha tracejada da fronteira `CAVALO` | Fronteira começa 0,3 à esquerda do balancim; a seta sai de dentro da caixa e o rótulo fica acima da seta, fora da linha, `buff ≥ 0,15` |
| V2 | 2:39 | T7-2 | `F⃗₂₍₁₎` encostado na linha tracejada da fronteira `SISTEMA: 1 + 2` | Rótulo abaixo da linha ou fronteira 0,2 mais alta |
| V3 | 2:56–2:58 | T7-3 | Transição embaralhada: `d(p⃗₁+p⃗₂)/dt` vira um borrão de glifos e `F⃗^ext` salta por cima do `+` | `TransformByGlyphMap` com mapa explícito (glifo por glifo) ou `FadeTransform`; antes, riscar `F⃗₁₍₂₎ + F⃗₂₍₁₎` e só então trocar a linha |
| V4 | 4:00–4:08 | T7-6 | `Σᵢ Σⱼ F⃗ᵢ₍ⱼ₎ = 0` encosta na última linha da matriz | Descer a soma 0,3 abaixo da matriz |
| V5 | 4:18 e 10:48 | T7-7 e T9-7 | O painel da DICA fica **branco** por ~1 s ao entrar ou sair, com o texto ilegível | Animar a opacidade do grupo inteiro (fundo, borda e texto juntos); nunca o preenchimento partindo do branco |
| V6 | 4:55–5:01 | T7-9 | `MOMENTO DAS PARTÍCULAS + MOMENTO DO CAMPO = CONSTANTE` começa no PALCO e termina na borda da CONTA | Ícone e legenda inteiros na CONTA, em duas linhas |
| V7 | 7:57–8:13 | T8-8 | `PÉ EMPURRA O CHÃO` e `ATRITO DO CHÃO` grudados ("CHÃOATRITO") | Cada rótulo na ponta livre da sua seta: o do pé à esquerda da seta para trás, o do atrito à direita da seta para a frente, folga ≥ 0,25 |
| V8 | 8:15–8:33 | T9-1 | `m⃗g` em cima da superfície da Terra e do círculo tracejado da bola | Rótulo à esquerda da seta, acima da superfície |
| V9 | 8:51–9:02 | T9-2 | `≈ 2,3 × 10⁻²⁴ m/s` encosta na borda direita do quadro | Quebrar depois do `=` (duas linhas) ou reduzir; margem ≥ 0,3 da borda |
| V10 | 9:58–10:30 | T9-5 | `CHÃO COM ATRITO` colado na seta de atrito do bloco leve | Legenda à direita, abaixo da linha do chão, longe das setas |
| V11 | 12:54–13:15 | E6-4 | A DICA encosta nos rótulos `AGARRAR / REBATER` das barras | Descer a DICA ou subir as barras; folga ≥ 0,25 |
| V12 | 13:18–13:45 | E7-1/3 | `LAGO CONGELADO · SEM ATRITO` e o chip `CÂMERA LENTA` grudados ("SEM ATRITOCÂMERA LENTA") | Chip no canto superior direito do PALCO (onde fica o REPLAY); legenda do lago à esquerda |
| V13 | 13:45–14:12 | E7-3/4 | Nos pés, `N⃗`, `(EXTERNA, IMPULSIVA)` e `V⃗` amontoados; a seta do recuo encosta no texto | `N⃗` e a legenda à esquerda da seta da normal; `V⃗` acima da seta do recuo; folga ≥ 0,25 entre os três |
| V14 | 14:00–14:12 | E7-4 | O "X" fica na **ponta de p⃗_bala**, em cima do rótulo; parece que o momento da bala inteiro foi riscado | O X vai no meio da componente vertical `p_y` (tracejada). `p⃗_bala` à esquerda da seta, `p_y` à direita da componente, `p_x` abaixo da componente horizontal |
| V15 | 14:30–14:40 | E7-5 | `≈ 99,994% NA BALA` encosta no topo do painel de barras; a DICA encosta no painel | Subir o texto 0,2 (ou descer o painel); DICA com folga ≥ 0,25 |
| V16 | 15:30–15:44 | E8-3/4 | `Σp = 0` colado no início da seta de `p_gases` | `Σp⃗ = 0` abaixo do diagrama, centralizado, folga ≥ 0,25 |
| V17 | 17:50–18:10 | C-1 | Painel de cima: a seta `p⃗` (magenta) e o rótulo `F⃗` empilhados na placa. Painel de baixo: o rótulo do fóton em movimento atravessa a conta `Δp⃗_placa = p⃗ − (−p⃗) = 2p⃗` | A conta `Δp⃗_placa` vai para a CONTA (abaixo de `p = E/c`). O `p⃗` do fóton destacado fica acima do feixe e some ao chegar na placa; `F⃗` à direita da placa, abaixo do fio |
| V18 | 18:12–18:40 | C-2 | Os riscos amarelos dos fótons passam por cima do texto da CONTA (`1.361 W/m²`) | Partículas só no PALCO (x ≤ 0,6) ou fade nelas a partir de x = 0,2 |

**Cosmético (fazer se for barato):** o chão 3D do T7 e do resumo termina numa borda vertical visível no x ≈ 0,6 (2:03, 19:15). Alargue o degradê
para 0,4–1,2. A placa de gelo do T8-6 parece um tapete retangular. Arredonde as bordas e use um fade nas pontas.

### 1.2 Travadas, pausas e alinhamento (logs do v4)
- Travadas: zero no hook, no T8 (os três saltos são os cortes de câmera previstos: 6:00, 6:20, 7:06) e no resumo. No E7 há **dois
  quadros quase repetidos** (13:43,7 e 14:15,5), nos começos do tiro em câmera lenta e do replay. Conferir que não é o ciclo emendado.
- Pausas ≥ 4 s: zero.
- Alinhamento 3D × Manim: tudo ≤ 2 px, **menos as mãos × bola no E6 (3,39 px)**. Corrigir.

### 1.3 A narração sugerida pelo Claude Code
É boa: segue as 64 âncoras, explica mais onde a tela já mostra mais, tem conectivos, brincadeiras curtas, boas-vindas e encerramento, e
nenhuma letra solta. A física confere em todos os números (T8, T9, T10, E6, E7, E8, E9 e coda recalculados). Fiz nove ajustes:
1. **H1:** "pela terceira lei, puxa o cavalo para trás" estava errado, e a minha primeira correção também. Quem faz a tensão ser
   igual nas duas pontas é a corda ideal (massa desprezível), não a terceira lei: os pares da terceira lei são corda × pedra e corda ×
   cavalo. Ficou: "numa corda ideal, a tensão é a mesma nas duas pontas. Ela puxa a pedra para a frente e puxa o cavalo para trás... com
   forças do mesmo tamanho."
2. **T8-6:** "com uns um vírgula vinte e seis" → "com uma desaceleração de cerca de um vírgula vinte e seis".
3. **T10-3, E7-5 e E7-1:** tirei "levar um tiro é pior do que dar um" e "o recuo não machuca ninguém... e a bala, sim" (piada com tiro
   em gente). No E7-1: "Não me pergunte o que ele caça no meio de um lago congelado; a física só quer saber do recuo." (O "empurrãozinho"
   do T10-3/E7-5 caiu na revisão de física abaixo.)
4. **E7-5:** "mais de noventa e nove vírgula nove por cento" → "uns noventa e nove vírgula nove nove por cento" (a tela mostra 99,994%).
5. **E9-1:** "No século dezessete" → "No fim do século dezessete".
6. **E9-6:** "quase dois séculos" → "mais de um século" (Newton por volta de 1700, Foucault em 1850).
7. **C-2:** 0,9 mN é o peso de ~0,09 g, ou três ou quatro grãos de arroz (não "três grãozinhos").
8. **C-2, laser:** "apontado para uma superfície que absorve" (3,3 nN é absorvido; refletido seria o dobro). O valor aparece na tela em 18:39.
9. Tags conferidas: 20 `[thoughtful]`, 19 `[curious]`, 6 `[thoughtful, emphatic]`, 2 `[excited]`, 1 `[happy]`, 1 `[calm, satisfied]`.

**Revisão de física (segunda leitura, todos os pontos conferidos e aceitos):**
- **T8-4:** fecha com "Numa corda ideal, de massa desprezível, a tensão é a mesma nas duas pontas".
- **T8-6:** no gelo as patas escorregam, então o atrito é **cinético** (μc ≈ 0,1 → 588 N), não estático máximo.
- **T8-7 (Cyrano):** ímã × placa é força interna e não levanta o conjunto; **a gravidade é externa** e continua puxando. Sai "só forças internas".
- **T9-3:** o disparo é tão curto que o **impulso do atrito nesse instante é desprezível**; por isso P = 0 logo depois do disparo.
- **T10-1:** a conservação vale **antes dos batentes** (os batentes são externos). Os momentos são **iguais em módulo e opostos**.
- **T10-3 e E7-5:** energia cinética pequena no caçador **não** quer dizer coice fraco: a força do recuo depende também da duração do
  impulso. Sai o "empurrãozinho"; fica "o caçador recua tão devagar", mais o aviso. A razão das massas (≈ 17.262) continua dita.
- **S2:** "momentos iguais e opostos" só vale para dois corpos que partem do repouso e se separam por forças internas; a terceira ideia vira
  "procure as forças externas e confira quem ficou de fora do sistema" (sai "aumente o sistema").
- **E6-4:** "energia interna, em deformação, aquecimento e um pouco de som". **E8-1:** apoio frouxo = "quase não segura o rifle durante o
  disparo". **E9-2:** "espelho ideal". **C-1:** "com a luz batendo de frente" (a conta 2I/c vale na incidência perpendicular).
- **E9-7 e C-3:** caiu o **modelo corpuscular** clássico, não a ideia do impulso, que estava certa dentro das hipóteses. No C-3 entra também
  "a luz carrega momento mesmo sem ter massa".
- **EN2:** a granada sem resistência do ar ("desprezando a resistência do ar").

**Duração (decisão do Kaio: versão enxuta):** a sugestão tinha ~4.650 palavras (~27 min). A versão do Anexo A foi enxugada para
**~4.110 palavras** (com a revisão de física), contra 3.210 da v3: **~23 a 25 min de voz**, contra os 19:52 do v4. Saíram repetições e frases que só descreviam a
tela; nenhum passo da física, número ou conta saiu. Os blocos que mais crescem continuam sendo T7-2/3, T8-6, T9-5/7, T10, E7-4 e C-1. A
cena se estica para acompanhar a voz, e com +28% de fala o risco de tempo morto volta: a §3 trata disso.

---

## Parte 2 — HANDOFF v5 (rodada da narração)

### 0. Rodada
- Unidade `videos_longos/yt_0016_sistemas_momento/` (preview v4). Rode `git status --short`. Copie a unidade para `_v4/` (código, ficha e âncoras; sem renders).
- Salve este handoff na unidade como `handoff_v5.md` e a narração do Anexo A como `narracao_final_v4.md`.
- **Objetivo:** (1) corrigir a tela (§1); (2) gerar a voz com o ElevenLabs v4 a partir do Anexo A (§2); (3) sincronizar a cena com a voz e
  entregar um **preview com voz** 960×540 / 15 fps, completo (§3).
- Sem SRT, master, legendado, `entregar.py`, commit ou push. Não alterar `template/`, `docs/`, `assets/`, `experimentos/threejs/` nem o yt_0015.

### 1. Correções de tela
- As 18 da tabela 1.1 (V1–V18) e o alinhamento mãos × bola do E6 (≤ 2 px). Os cosméticos, se forem baratos.
- **Mudanças de tela da revisão de física** (o texto exato está nas linhas `tela:` do Anexo A):
  - **T8-6:** selo `COEFICIENTE CINÉTICO ≈ 0,1 (AS PATAS ESCORREGAM)` e `f_chão = 0,1 · 600 · 9,8 = 588 N` (sai "estático" e "f_máx").
  - **T8-7:** `ÍMÃ E PLACA: FORÇA INTERNA · NÃO LEVANTA O CONJUNTO; O PESO (EXTERNO) CONTINUA`, com a seta do peso do conjunto, para baixo,
    durante o selo. Sai "CORDA E ÍMÃ: SÓ FORÇAS INTERNAS".
  - **T10-1:** as barras MOMENTO (iguais em módulo, setas opostas) e ENERGIA são medidas **antes dos batentes** e ficam congeladas com o
    selo `ANTES DOS BATENTES` quando os blocos param; a CONTA ganha `(ANTES DOS BATENTES)` ao lado de `P⃗ = 0`.
  - **T10-3:** `MOMENTOS IGUAIS EM MÓDULO; ENERGIAS, NÃO` (sai "MOMENTO SE DIVIDE IGUAL").
  - **E7-5:** nada na tela associa energia pequena a recuo fraco; se houver espaço, um chip `ENERGIA PEQUENA ≠ COICE FRACO`.
  - **E6-4:** `ENERGIA INTERNA: DEFORMAÇÃO, CALOR, SOM` no lugar de "CALOR E DEFORMAÇÃO".
  - **C-1:** a luz incide perpendicular às placas (se o desenho do v4 tiver incidência oblíqua, endireitar).
  - **C-3:** `O MODELO CORPUSCULAR DO NEWTON CAIU.`
  - **S2:** `MOMENTOS IGUAIS E OPOSTOS; ENERGIA, NÃO; NÃO CONSERVA? QUEM FICOU DE FORA?`
- Regras que continuam valendo: nada escrito sobre corpo 3D; rótulos pela ponta livre da seta com `buff ≥ 0,15` e folga ≥ 0,25 de qualquer
  outro texto; viradas de cena em sequência; nenhum texto a menos de 0,3 da borda do quadro.

### 2. Voz
- Crie `narracao_tags.md` a partir do Anexo A com a seção `## Texto corrido (para gravação)`. Ela leva só a fala com as tags, em
  parágrafos (um por âncora), sem as linhas `tela:`, sem IDs e sem a tabela de números. Guarde também a lista âncora → primeira frase
  (para a sincronia).
- `--seco` primeiro (confere os blocos de até 4.500 caracteres, nos finais de frase). A chave fica **só** na variável
  `ELEVENLABS_API_KEY` da sessão do PowerShell do Kaio; nunca em arquivo, log, relatório ou commit. Se a variável não existir, pare e peça.
- Gerar: voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`, `mp3_44100_192` → WAV mono 16 bits 44,1 kHz, em `audio/narracao_v4.wav`
  (não sobrescrever nada que já exista). **Uma tomada.** Não gerar de novo sem ouvir: regenerar só o bloco com problema.
- Ouvir (ou transcrever com o ASR) e conferir a pronúncia de: "cosseno", "micropascais", "milinewton", "nanonewtons",
  "dez elevado a menos vinte e quatro", "Foucault", "Cyrano de Bergerac", "Snell", "Parallax Lab". Também conferir se alguma tag foi lida em
  voz alta. Se algo falhar, trocar a tag pela vizinha ou reescrever a palavra e regenerar só aquele bloco.

### 3. Sincronia e preview com voz
- Tempos das âncoras pela voz real: ASR com timestamps por palavra e cada âncora começando **~0,15 s antes** da primeira palavra da sua
  fala (`gerar_ancoras.py` → `ancoras.json`, como nos longos anteriores). A cena se estica ou encolhe para caber; nenhuma fala é cortada.
- **Sincronia fina dentro de cada âncora:** todo número falado aparece na tela no instante em que é dito (±0,3 s), e todo objeto citado na
  fala ("repara na caixa tracejada", "olha as barras", "essa que acendeu", "aquela interrogação ali no canto") acende quando é citado.
- **Tempo morto com a fala mais longa:** a voz cresce ~28%. Encha cada trecho esticado com o que a fala está dizendo, não com espera:
  - realce do termo citado no desenho e na conta, ao mesmo tempo;
  - a conta montada termo a termo no ritmo da fala, em vez de entrar inteira;
  - o "palco vivo" continua (cavalo andando, esferas vibrando, corpúsculos, fótons, vela girando);
  - os eventos (T9, T10, E6, E7) continuam com **no máximo um replay**. Não encher com loop.
  - Meta: nenhum trecho ≥ 4 s sem mudança visível, exceto o cartão final.
- Render: preview completo 960×540 / 15 fps **com a voz**, mais `capitulos_v5.txt` com os tempos novos dos 11 capítulos.

### 4. QA
- Sobreposição: auditoria completa, conferindo um por um V1–V18. Em cada virada de cena, nenhum quadro com elementos das duas cenas.
- Pausas ≥ 4 s; travadas (lista, como no v4, incluindo os dois quadros do E7); alinhamento 3D × Manim ≤ 2 px (incluindo mãos × bola do E6).
- **Sincronia:** para cada âncora, o atraso entre a primeira palavra e o evento visual (meta ≤ 0,3 s); para cada número da tabela de
  conferência, o tempo falado e o tempo em que aparece na tela.
- Áudio: pico ≤ −1 dBFS, sem clique nas emendas dos blocos da voz.

### 5. Parada e relatório
Pare com o preview com voz. Relatório (AGENTS.md): arquivos alterados; correções V1–V18 (feito / não feito e por quê); geração da voz
(modelo, voz, versão do texto, nº de blocos, blocos regenerados, caracteres gastos); duração final; mapa de âncoras e capítulos novos;
resultados do QA; pronúncias problemáticas; pendências. Zip para avaliação como no v4 (preview com voz, `ancoras.json`,
`capitulos_v5.txt`, logs, stills das correções V3, V7, V12–V14, V17). Sem SRT, master, commit nem push.

---

## Anexo A — narração final v4

Ver `narracao_final_v4.md` (salvo palavra por palavra).
