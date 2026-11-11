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
  e baixa para opacidade ~0,58 para não competir com o conteúdo. O primeiro termo é a área do vídeo no `docs/mapa_curricular.md`
  (ELETROMAGNETISMO, MECÂNICA...), não o ID do módulo.
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

- Ficha (`ficha.md`): endereço no mapa (`disciplina:`, `bloco:`, `modulo:` com o ID, `referencia:`, ex.: Eletromagnetismo · Eletrodinâmica ·
  EM 7.2 · Griffiths 7.2.1–7.2.2); título acadêmico (vai na tag do canto) e pergunta narrativa interna; pergunta central; pré-requisitos; payoff;
  aparato; **física congelada** (convenções de eixo, sinais, fórmulas); **hipóteses do modelo**; storyboard em blocos N01–NNN; convenção
  de cores da cena; checklist de QA físico. Campos obrigatórios em `docs/formatos.md`.
- Sincronia: âncoras de evento visual por frase (`an(n, k)`, a imagem começa ~0,15 s antes da frase), sem ASR; a voz é a régua.
- Entrega: master 1080p30, CRF 14, `.srt` separado, `capitulos_youtube.txt`, via `videos/entregar.py` (`docs/entregas.md`). A pasta em
  `entregas/Vídeos Longos/` segue `<Área> - <Bloco> - <Assunto>`, com área e bloco do mapa.
- Duração observada: 12–27 min. A duração sai da explicação, não o contrário.

## 7. Fundo e entrada de fórmulas (regras permanentes, 2026-11-06)

1. **Fundo de estrelas** (exceto Cálculo I–IV: ver a seção "Série Cálculo I–IV (exceção de fundo)" no fim deste documento). Movimento contínuo **para a esquerda**, em velocidade constante por camada (3 camadas, parallax), calculado em **relógio global do
   vídeo** (`t = início do lote na voz + clk do lote`), independente da sincronia (`play`, `plano()`, `LEAD`). Nunca reinicia por lote/cena, nunca para, nunca
   volta, sem balanço vertical. A reciclagem (mod) das estrelas acontece só **fora da tela** (campo ≥ tela + 2 u de folga de cada lado); nenhuma estrela
   surge ou some dentro da área visível. Cena parada resolve-se com movimento do conteúdo, nunca acelerando o fundo nem somando camadas. QA de
   deslocamento por quadro (correlação de fase, `fundo22.py` no yt_0022) no preview e no master, inclusive nas fronteiras de lote.
2. **Fórmulas sem "flash".** Nenhum termo, linha, título ou caixa pode ficar visível (opacidade > 0,15) e depois sumir antes de ser escrito. Cada elemento
   nasce uma vez, na palavra que o nomeia, e só sai por `FadeOut` deliberado depois de lido; visível por < 0,7 s seguido de sumiço é defeito. Causa mais
   comum: `FadeOut` de um objeto que a `Pilha` (`limpa()`/`so()`) já tirou da cena: o Manim o re-mostra com a opacidade original e o apaga de novo. O kit
   deve filtrar `FadeOut` de objeto fora da cena. QA FLASH: log `[fantasma]` na auditoria + detector por vídeo (picos de "tinta" que sobem em ≤ 3 quadros e
   voltam em ≤ 10, `flash22.py`).
3. **Sólidos 3D.** Contraste mínimo entre tampa, raios, anéis e fatias (nunca tom sobre tom); luminância da superfície ≤ ~85% (sem estourar); lateral/espessura
   legível; rótulos e setas **fora** do sólido (≥ 0,3 u de afastamento); um só desenho do sólido para todas as cenas em que ele aparece.

## 8. Escrita da álgebra: caneta (regra permanente, 2026-11-08)

> **Escrita da álgebra: caneta (desde 2026-11-08, Kaio).** Todo termo novo de uma conta é escrito glifo a glifo, da esquerda para a direita, por uma caneta: contorno finíssimo (≈ 2% da altura do glifo, ≈ 1 px a 1280×720, ≈ `stroke_width` 1 no Manim a 1080p), ponta branca de ≈ 3 px, preenchimento na cor do token **sem contorno por cima**, 0,6 s por glifo, um glifo a cada 0,30 s. Termos com origem no desenho (seta, cota, rótulo) **voam** do desenho com `TransformFromCopy`; passos de manipulação usam `TransformByGlyphMap`. Nada de `FadeIn` de linha pronta e nada de preview do destino: antes da sua vez o termo **não está na cena** (ou está com opacidade 0 no fill e no stroke). Cuidado: `FadeIn`, `TransformFromCopy` e `Write` dentro de `Succession(Wait(...), ...)` ou de `AnimationGroup` adicionam o destino à cena em estado final no instante 0 (flash): programar o início de cada termo sem esse padrão. Auditoria `FLASH POR QUADRO` obrigatória no QA (zero eventos). Vale para toda álgebra nova (longos e curtos); vídeos já feitos não são refeitos.

| Parâmetro | Valor |
|---|---|
| Traço do contorno | finíssimo: ≈ 2% da altura do glifo (≈ 1 px a 1280×720; nunca abaixo de 1 px no preview 960×540) |
| Preenchimento | cor do token, sem contorno por cima (a letra termina com o peso normal) |
| Ponta da caneta | ponto branco de ≈ 3 px com borda na cor do token; some quando o traço fecha |
| Tempo por glifo | 0,6 s de traço + preenchimento; início de um glifo a cada 0,30 s |
| Ordem dos traços | em sequência, como a mão |
| Fração, raiz, parênteses | escrevem como um bloco, 0,4–0,5 s, esquerda para a direita |
| Preview 960×540 | se o QA reprovar a legibilidade, subir só o traço (1,0 px), nunca a ponta |

Portão de QA `FLASH POR QUADRO`: no quadro `t0−1` de cada termo escrito/voado, a tinta no retângulo de destino é igual à do fundo (≤ 2% de pixels claros) e o termo não aparece completo antes de `t0`. FALHA com qualquer evento.


## Série Cálculo I–IV (exceção de fundo)

Padrão aprovado pelo Kaio em 2026-11-09 (thread "Comparar Manim 2.5D e Three.js em Cálculo III"). Vale para todo `longo_horizontal` de Cálculo I, II, III e IV (Guidorizzi). O resto deste documento continua valendo; aqui ficam só as diferenças. Código e imagens: `assets/calculo/` (`papel.py`; `gerar_fundos.py` gerou os PNGs da v1). Fundo e grade em vigor: v2 de 2026-11-11 (seções 1 e 3).

### 1. Fundo: violeta liso, parado (v2, 2026-11-11)
- Degradê vertical violeta liso, #18143A no topo → #0F0C26 na base, sem grade na imagem, parado na câmera (`usar_papel(self)`). O PNG `fundo_calculo_violeta_liso_<W>x<H>.png` é gerado sozinho na primeira chamada (`assets/calculo/papel.py`).
- O milimetrado em PNG (v1, 2026-11-09: `fundo_calculo_milimetrado_*`, `fundo_calculo_liso_*`) saiu do padrão. Os PNGs antigos ficam em `assets/calculo/` para as unidades ainda não migradas.
- **Exceção à regra dos longos de Física:** nos longos de Cálculo não há céu espacial nem estrelas andando (`poeira_estelar`).
- Vale com o quadro 16×9 u do projeto (`template/config_horizontal.py`): 1 u = 120 px em 1080p, 60 px em 540p.

### 2. Fundo fixo = render rápido
- O fundo entra como imagem da câmera (`camera.background_image`, via `usar_papel(self)`), nunca como `ImageMobject`, e nada no fundo se mexe.
- Motivo, medido em 2026-11-09 (cena de álgebra de 8 s, 1080p/30): fundo atual dos longos de Física, com estrelas andando, 10,1 s; fundo parado na câmera, 4,5 s. O updater das estrelas obriga o Manim a redesenhar, em todo quadro, todos os objetos que vêm depois delas na cena. Isso dá ~20–25 min de render a mais num longo de 30 min.

### 3. Grade que nasce dos eixos (v2, 2026-11-11)
- A grade é desenhada pelo Manim **a partir dos eixos de cada cena**: `papel(ax)` usa a mesma origem e a mesma unidade de `ax` (qualquer objeto com `c2p`), então alinha por construção em qualquer escala. Não há mais eixo preso a cruzamento nem unidade arredondada.
- Quadradinhos iguais, sem linha grossa: cor #2B2558, traço 1,2.
- Passo: 0,25 da unidade do gráfico. Se o quadradinho ficar com menos de 20 px em 1080p, passa sozinho para 0,5 (e depois 1). `passo=` força outro valor.
- Cena com um gráfico: `papel(ax)` cobre a tela inteira. Dois painéis com escalas diferentes: `papel(ax1, area=...)` e `papel(ax2, area=...)` (área em unidades de cada gráfico), um por painel, e o resto liso. Cena sem gráfico: `papel()`, na unidade padrão (1 u, origem no centro).
- A grade é um `VGroup` parado (z_index −10 por padrão; a unidade pode baixar para ficar sob chapas e placas): entra e sai com `FadeIn`/`FadeOut`, nunca com updater.
- `eixos_no_papel` continua existindo, mas só cria e posiciona os eixos. `janela`/`janela_local` deixam de ser necessárias (`janela` fica em `papel.py` só por compatibilidade).

### 4. 3D: Three.js onde a câmera trabalha
- Superfície curva, campo vetorial, sólido com corte e câmera orbitando: Three.js, com valores, rótulos e fórmulas no Manim (pipeline de sempre). Não usar `ThreeDScene` do Manim: no teste do fluxo pelo paraboloide, ele levou 242 s contra 22 s do Three.js e ainda errou a ordem de profundidade.
- O fundo das cenas 3D é o mesmo violeta liso (quadros Three.js com fundo transparente sobre a câmera, ou o violeta no próprio Three.js); a grade sai (fade) enquanto o 3D está na tela, para a grade plana não confundir a leitura de profundidade.

### 5. Hábitos de render leve
- Poucos updaters; não usar `always_redraw` que recria `MathTex` a cada quadro.
- Tirar da cena (`remove`/`FadeOut`) o que saiu da tela; opacidade 0 ainda custa.
- Preview em 540p/15 só da seção que mudou; 1080p/30 uma vez, no fechamento.
