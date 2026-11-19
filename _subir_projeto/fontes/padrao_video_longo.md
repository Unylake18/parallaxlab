# Padrão do vídeo longo (horizontal)

Registrado em 2026-10-24 a partir dos longos `yt_0008` (Ampère), `yt_0009` (Quem empurra as cargas?) e, principalmente, `yt_0010` (FEM de movimento),
com as cores herdadas de `yt_0005`/`yt_0006`. Vale para todo `longo_horizontal` novo, salvo decisão diferente no briefing de Produção.
Complementa `docs/formatos.md` (campos da ficha, regras de formato) e `docs/roteiro_voz_elevenlabs_v4.md` (geração da voz).

O briefing de Produção continua soberano sobre física, matemática e storyboard. Este documento fixa **a forma**: o que vai na tela, como
abre, como fecha, quais cores e como a fala é escrita.

## 1. Estrutura do vídeo

| Parte | O que acontece | Referência |
|---|---|---|
| **Hook** (15–40 s) | Fenômeno ou paradoxo na tela, sem fórmula. Uma pergunta que o vídeo vai responder ("Então, de onde vem essa energia?") | yt_0008 N01, yt_0009 N001–N003 |
| **Bem-vindos** | Logo + `BEM-VINDOS AO PARALLAX LAB`. Na fala: "Fala, pessoal! Bem-vindos ao Parallax Lab." | yt_0010 `n00`, yt_0009 N003 |
| **Título** | Título do vídeo + uma linha `NESTE VÍDEO: …` (ou um mapa de 3 nós sem fórmulas, como no yt_0009). Some depois de ~3 s | yt_0010 `n00` |
| **Retomada** | Uma frase do que já vimos na série ("Nos vídeos anteriores…"), quando houver | yt_0008 |
| **Desenvolvimento** | Blocos do storyboard, cada um respondendo a uma sub-pergunta | ficha |
| **Síntese** | A resposta da pergunta do hook, em palavras, e no máximo 2–3 equações-chave | yt_0010 N45–N48 |
| **Encerramento** | Tela limpa, logo + `INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS` + prévia do próximo vídeo | yt_0010 `n49`, yt_0009 N059 |

A ordem padrão é **hook → bem-vindos → título**, como no yt_0008 e no yt_0009. O yt_0010 abriu com o bem-vindos antes do hook; as duas
ordens funcionam, mas a padrão é com o hook primeiro.

### Encerramento (CTA)
1. `FadeOut` de tudo (equações, manchete, legenda de eixos, watermark, tag do canto) e `self.clear()`: nada fica atrás da logo.
2. Logo horizontal (`assets/branding/overlays/parallax_lab_logo_horizontal.png`, largura ~6) com anéis violeta tracejados girando
   devagar em sentidos alternados; uma onda (ripple) no fim.
3. `INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS`.
4. **Prévia do próximo vídeo:** a pergunta-gancho do próximo vídeo (`E SE, EM VEZ DE MOVER O CIRCUITO, FOR O CAMPO QUE MUDA?`) e
   depois `PRÓXIMO VÍDEO: …` + o assunto em ciano. Quando o próximo vídeo já tem aparato pronto, mostrar esse aparato por alguns segundos,
   como o yt_0009 mostrou a barra e os trilhos do yt_0010.
5. Fala: o que ligamos hoje (uma frase) → convite para se inscrever → pergunta do próximo vídeo → "Até a próxima!".

## 2. Tela: pouca escrita

- **Tag do canto superior esquerdo**, presente o vídeo todo: `MÓDULO/SÉRIE · TÍTULO DO VÍDEO` (ex.: `ELETROMAGNETISMO · FEM DE MOVIMENTO
  E REGRA DO FLUXO MAGNÉTICO`), `to_corner(UL, buff≈0.32)`, corpo 24, opacidade 0,78 na abertura. Depois do título, ela encolhe (×0,84)
  e baixa para opacidade ~0,58 para não competir com o conteúdo.
- **Watermark** no canto superior direito: `WATERMARK_PATH`, largura ~1,9, opacidade 0,45.
- **Manchete** (`H(...)`): uma linha no topo (y ≈ 3,4), corpo 30, opacidade 0,9, largura máx. 11,5. Nomeia a etapa
  ("SEGUNDA LEI DE NEWTON", "PUXE A BARRA: O RESISTOR ESQUENTA"). Troca por `FadeOut` + `FadeIn`; nunca duas manchetes juntas.
- **Equações** numa coluna à direita (centro x ≈ 4,3); o aparato ou desenho ocupa a esquerda e a física não invade a coluna da matemática.
  Poucas equações por vez: ao trocar de etapa, a anterior sai (`swap`).
- **Rótulos curtos** junto ao objeto (`u = u x̂`, `I`, `F_mag`), em MathTex, aparecendo só quando a fala chega neles.
- **Legenda de eixos** (x̂, ŷ, ẑ) pequena, cinza (`DIM`), no canto inferior esquerdo, só quando a convenção importa.
- **O que não vai para a tela:** frases inteiras da narração, parágrafos, listas. Se a fala explica, a tela mostra o objeto e a equação.
  A legenda `.srt` é separada (não há legendado embutido nos longos).
- **Um aparato só** que atravessa o vídeo (no yt_0010: trilhos + resistor + barra + B), controlado por `ValueTracker`s e redesenhado a
  cada quadro. Trocar de cenário só quando a física exige.

## 3. Tipografia

- **Todo texto de tela fora do MathTex: Space Grotesk em MAIÚSCULAS** (`screen_text` de `template/fonts.py`, com `.upper()` dentro do
  helper `txt()`). Vale para tag, manchete, título, bem-vindos, rótulos de etapa, CTA e prévia. (O yt_0010 ainda deixava em caixa normal
  os textos com corpo > 28; o padrão daqui em diante é maiúscula em tudo, como no yt_0009 com `CAPS=1`.)
- **Exceção, minúsculas:** a definição de variável no formato símbolo + significado (`m: massa da barra`, `t = 0 · soltura`). Ela
  fica em MathTex com `\text{...}` e pode ficar em minúsculas.
- **MathTex fica como está:** nunca forçar maiúsculas em símbolos (`u` ≠ `U`, `r` ≠ `R`).
- **Nunca** pôr `∥ ⊥ ρ λ σ ω ⊗ ⊙` (ou outro símbolo matemático) dentro de `txt()`: a Space Grotesk não tem o glifo e aparece um
  quadrado. Símbolo vai em MathTex.
- Corpos de referência (960×540 → 1080p escala junto): manchete/corpo 30 · nota 26 · legenda 22–24 · título 42–52 · bem-vindos 30–38.
  Math: 54 / 46–48 / 38–40 / 30–32 (XL, L, M, S).

## 4. Cores das grandezas

Base: `template/config_horizontal.py` (fundo `#050816`, texto `#F5F7FF`, `PRIMARY_COLOR` = ciano `#35D9FF`). Na MathTex, cada grandeza
leva a sua cor por token (dicionário `TOK`/`TOKCOL` + `M(*partes)`); operadores e números ficam brancos.

### Definidas (usadas em yt_0005–yt_0010)

| Grandeza | Cor | Hex | Constante |
|---|---|---|---|
| Campo magnético **B**, fluxo **Φ_B**, dΦ_B/dt | magenta | `#EA63FF` | `MAGENTA`/`MAG` |
| Corrente **I, J, K**, dℓ da corrente, velocidade de deriva **v_d**, ∇·J | verde | `#3FE08B` | `GREEN` (nunca ciano) |
| Campo elétrico **E**, potencial **V**, ΔV, fem **ℰ** | ciano | `#35D9FF` | `CYAN` |
| Energia, trabalho e potência fornecidos (agente externo, F_ext, P_ext, energia cinética K) | ciano | `#35D9FF` | `CYAN` |
| Força (**F**, F_B, F_E, F_mag, **f**, f_s) | azul-claro | `#5AA2FF` | `FC` |
| Carga (q, dq, Q, ρ, λ, σ, carga de prova) | azul / azul-claro | `#267BFF` / `#7FB2FF` | `BLUE` / `BLUE_L` |
| Velocidade (v, u, v∥, v⊥), ω, período, τ: **o violeta é só disso** | violeta | `#9C8CFF` | `VIOLET` |
| Geometria (comprimentos l, x, R, s, áreas, superfícies, caminhos de integração, amperianos, da, dτ) | cinza-claro | `#B8C4DA` | `GEO` |
| Calor, energia dissipada, P_R, E_diss (**único tom quente**) | laranja | `#FF7A3D` | `HEAT` |
| Matéria condutora (fio, trilho, lâmina, barra) | cinza-aço | `#7A8696` | `STEEL` |
| Texto secundário, eixos, legenda de convenção | cinza-azulado | `#8FA3C4` | `DIM` |
| Painel/cartão de destaque (no lugar de caixa branca) | azul-escuro translúcido, borda `BLUE_L` | `#0E2A52` | `PANEL` |

Decisão do usuário (2026-10-24): geometria em cinza `GEO`, violeta exclusivo da velocidade. O yt_0006, o yt_0008 e o yt_0009 usaram
violeta na geometria; eles não são refeitos por isso. dℓ **da corrente** continua verde; dℓ de um caminho geométrico é `GEO`.
Os anéis violeta do encerramento são marca, não grandeza.

Regras que vieram junto: **carga ≠ corrente ≠ matéria** (azul, verde, aço); portadores desenhados como **cargas positivas de prova**
e corrente convencional, nunca elétrons, salvo quando o briefing pedir; amarelo não entra na paleta.

### Em aberto (definir com o tempo)

| Grandeza | Situação |
|---|---|
| Ângulos auxiliares (α, γ, θ) | ciano no yt_0006; sem padrão geral |
| Posição do observador **r** e ∇ (ciano) × fonte **r′** e ∇′ (verde) | só no yt_0008 |
| Potencial vetor **A** | ainda não usado (gancho do yt_0008) |
| Indutância **L**, ℰ_L, energia magnética | em uso no yt_0012 (preview); registrar quando fechar |
| Resistência **R**, capacitância **C** | branco até agora |
| Massa **m** | branco até agora |
| Mecânica (posição, momento linear, energia mecânica, centro de massa) | a definir no yt_0013 (colisões) |
| Temperatura, pressão, calor em termodinâmica | só o laranja do calor está definido |

Ao fixar uma cor nova num vídeo, acrescente a linha na tabela "Definidas" com o vídeo de origem.

## 5. Narração

Geração, voz, modelo e regras gerais das tags: `docs/roteiro_voz_elevenlabs_v4.md`. Para os longos, valem estas regras a mais:

- **Explique tudo, sem se preocupar com o tempo da animação.** A fala manda; a cena se estica para acompanhar (`self.wait`, holds,
  âncoras `an(n, k)` que encaixam cada trecho na voz). Nunca cortar um passo didático para caber num tempo de animação.
- **Nunca a letra solta: sempre o nome completo.** "a distância ao eixo", e não "ésse"; "a velocidade da barra", e não "u";
  "o campo magnético", e não "bê". Se o símbolo é novo, apresentar uma vez ("a velocidade da barra, que na tela aparece como u") e depois só
  o nome. Isso substitui a tabela de "letras faladas" usada no yt_0008.
- **Didático e com intimidade:** professor de cursinho conversando com o aluno. "Fala, pessoal!", "Olha o experimento", "Escolhe uma
  carga positiva", "Repara que…", "Vamos combinar os sentidos". Pode usar "a gente" e "você".
- **Conectivos sempre:** "Primeiro", "Agora", "Então", "Só que", "Ou seja", "Por isso", "Lembrando", "Repara que", "Resumindo". Variar e
  não repetir o mesmo em frases seguidas.
- **Dizer o que o desenho é e o que não é:** "os marcadores são cargas positivas de prova; não são uma afirmação sobre o sinal dos
  portadores reais"; "a velocidade no desenho não é a velocidade real das cargas".
- **Hipóteses ditas em voz alta** uma vez, no começo do bloco em que importam (campo uniforme, resistência só no resistor, atrito
  desprezado).
- **Fechamento na pergunta do hook:** "A pergunta inicial está respondida: …".
- **CTA curto e específico:** "Se essas conexões ajudaram você, se inscreve no Parallax Lab para acompanhar os próximos vídeos." + pergunta
  do próximo vídeo + "Até a próxima!". Opcional: uma pergunta para os comentários (yt_0009).

### Tags do ElevenLabs v4 nos longos

- Uma tag por trecho/parágrafo, em inglês, valendo até a próxima.
- Base: `[thoughtful]` (explicação) e `[curious]` (pergunta, virada). Ênfase de conceito-chave: `[thoughtful, emphatic]`. Descoberta ou
  resultado: `[excited]`, com parcimônia (1–2 por vídeo). Bem-vindos: `[happy]` ou `[curious]`. Fechamento: `[calm, satisfied]`.
- Pausa: `[short pause]` ou reticências antes de um resultado importante.
- **Não usar `[slowly]`, `[slow, measured pace]` nem variações de "devagar"**: deixam a voz arrastada nos longos. Também não usar
  `[pause]` (não está na lista validada: usar `[short pause]`).
- Distribuição de referência (yt_0010, ~20 min): 25 `[thoughtful]`, 18 `[curious]`, 6 `[thoughtful, emphatic]`, 2 `[excited]`,
  1 `[short pause]`, 1 `[calm, satisfied]`.

## 6. Ficha, sincronia e entrega

- Ficha (`ficha.md`): título acadêmico (vai na tag do canto) e pergunta narrativa interna; pergunta central; pré-requisitos; payoff;
  aparato; **física congelada** (convenções de eixo, sinais, fórmulas); **hipóteses do modelo**; storyboard em blocos N01–NNN; convenção
  de cores da cena; checklist de QA físico. Campos obrigatórios em `docs/formatos.md`.
- Sincronia: âncoras de evento visual por frase (`an(n, k)`, a imagem começa ~0,15 s antes da frase), sem ASR; a voz é a régua.
- Entrega: master 1080p30, CRF 14, `.srt` separado, `capitulos_youtube.txt`, via `videos/entregar.py` (`docs/entregas.md`).
- Duração observada: 12–27 min. A duração sai da explicação, não o contrário.
