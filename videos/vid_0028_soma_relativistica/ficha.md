# Soma relativística de velocidades

- ID: `vid_0028`
- Série pública: **DA EQUAÇÃO AO FENÔMENO · EP. 08** (EP. 07 = vid_0025)
- formato: `curto_vertical`
- solido_3d: nenhum — o problema é de referencial, setas, régua e transformação algébrica; `relogio_de_luz` trata de contração do comprimento e `cone_de_luz` indica que Lorentz e diagramas 1+1 ficam melhores em 2D (decisão do briefing).
- Headline: `0,8c + 0,8c = ?` / “QUANTO A MEDE DE B?”
- Fase: preview visual silencioso, 540×960 / 15 fps. Sem voz, SRT, legenda, master, legendado, entrega ou capa.
- Física, arquitetura e hook: handoff de Produção vid_0028 (C01–C10, sem C06, que foi incorporada à C05), congelados pelo Kaio em 26/10/2026.
- Duração: animação-base com orçamento de ~124 s; com voz, o vídeo final precisa ficar abaixo de 180 s (meta 140–170 s).
- End card silencioso: somente `@labparallax` (padrão aprovado do vid_0024/0027).

## Física (congelada)

Eixo x para a direita. Na Terra: v_A = +0,8c, v_B = −0,8c. O referencial de A se move a +0,8c em relação à Terra.

- dx′ = γ(dx − v_A dt), dt′ = γ(dt − v_A dx/c²); v_B′ = dx′/dt′; γ cancela; dividir por dt; v_B = dx/dt.
- v_B′ = (v_B − v_A)/(1 − v_A v_B/c²) = −1,6c/1,64 = −(40/41)c ≈ −0,976c; |v_B′| ≈ 0,976c (B mede A a +0,976c).
- Na Terra, a separação fecha a 1,6c: não é velocidade de corpo nem de sinal, nem o que A mede de B.
- Limite clássico: |v_A v_B|/c² ~ 10⁻¹⁴ a 30 m/s ⇒ v_B′ ≈ v_B − v_A.
- 0,5c cada: 1c (soma simples) · 0,8c; 0,99c cada: 1,98c · 0,99995c.

## Implementação

Palco no terço superior (foguetes, estação, chão e estrelas que pertencem à Terra), régua de módulos 0 → c → 2c
no meio (marca de c em x = 0 em C03, C05, C08 e C09), equação embaixo e faixa inferior livre. O cenário anda
por integração quadro a quadro das velocidades do referencial atual: mudar de referencial congela, troca as
velocidades e a seta do corpo que fica parado passa para o mundo (a Terra ganha −0,8c). C04 usa
`TransformByGlyphMap` em `MathTex` de string única (índices conferidos antes, nenhum debug no vídeo).

Preview v1 (25/10/2026): `media/videos/cena/960p15/SomaRelativistica028.mp4` — 540×960 / 15 fps, 139,1 s,
2.087 quadros, sem áudio. Pranchas em `renders/prancha_v1_*.png`; zip local para o GPT em `renders/v1_para_gpt.zip`.

## Preview v2 — Three.js + Manim (26/10/2026)

Handoff v2: cold open 3D, promessa + mapa ①②③, troca de referencial com o mundo deslizando (v_ref no timeline),
barras de espaço e tempo na C04, CTA no fim. Pipeline de `experimentos/threejs/` (trazido da branch
`claude/project-thread-pzio5l`, sem commit) montado nesta unidade: `cena3d/` (objetos e câmera), `render3d.js`,
`compor.py`, `qa/alinhamento.js`, `timeline.json` (fonte única de tempos) e `movimento.py` (tabela de trajetórias que
o 3D e o Manim leem igual). `cena.py` agora é a camada Manim com fundo transparente; o v1 só-Manim está em `cena_v1.py`.
Cores dos objetos 3D com a paleta do canal (ciano, azul elétrico; magenta só nos pontos de sinalização), a pedido
do Kaio; violeta fica só nas velocidades do Manim.

Preview v2: `renders/preview_v2_540x960.mp4` (540×960 / 15 fps, 140,0 s, 2.100 quadros, sem áudio);
3D sozinho em `renders/parte3d_v2_540x960.mp4`; pranchas em `renders/prancha_v2_*.png`.

## Preview v3 — entendimento, sincronia, sem sobreposição (26/10/2026)

Handoff v3: setup "CADA UM A 0,8c EM RELAÇÃO À TERRA" → pergunta "QUE VELOCIDADE O FOGUETE A MEDE PARA O FOGUETE B?"
→ `0,8c + 0,8c = ?` como PALPITE → "A RESPOSTA NÃO É 1,6c" → promessa, um texto por vez; slot `v_B′ = ?` fixo no
topo até a C05 (o resultado voa até ele) e atualizado na C09. **Tabela de velocidades por referencial aplicada**
(`movimento.py`): na tela cada objeto anda com a velocidade que o referencial atual mede (Terra: ±0,8; A: B a −40/41,
Terra a −0,8; B: A a +40/41, Terra a +0,8), média suave nas trocas; o colchete fecha a 1,6·k na Terra e a 0,976·k em
A. Foguetes a 0,7×, em pistas (nunca se cruzam nem saem do quadro), recolhidos durante a C04; C04 em três atos; rótulo
da Terra e ponteiros contam junto com o movimento; sem magenta nos objetos; nariz e carros em `#2F6BFF`.
v2 preservado em `v2_snapshot/`.

Preview v3: `renders/preview_v3_540x960.mp4` (540×960 / 15 fps, 139,0 s, 2.085 quadros, sem áudio); 3D sozinho em
`renders/parte3d_v3_540x960.mp4`; pranchas em `renders/prancha_v3_*.png`. Alinhamento 3D × Manim: pior 1,27 px.

## Preview v4 — layout em tela cheia e legibilidade (27/10/2026)

Handoff v4 (só layout, tamanho e contraste): zonas fixas em 540×960 — marca 0–48 px, contexto 56–176 (tag, slot e
passos em linhas próprias), palco 3D 190–470 (só setas, rótulos e colchete do Manim), bloco principal 490–740,
legenda 760–840 livre. Palco mais alto (pistas em y 3,45/3,7, chão em 1,05, estação e cidade 1,35×, foguetes 0,8×).
C04 em tela própria: o 3D sai por inteiro (véu), barras largas uma de cada vez (o pedaço violeta se desprende para
baixo, o resultado fica numa linha própria) e viram resumos de uma linha; as equações do ato 2 saem quando alimentam
o quociente. Tamanhos medidos: dígito das equações principais 32,6 px (MathTex 76), rótulos de régua e ponteiros
22 px, texto do hook 28 px, secundário ≥ 15 px, rótulos dos foguetes 17 px; LaTeX com traço engrossado; nenhum
estado "apagado" abaixo de 0,75. Dois rótulos da barra C04 dizem `dx − v_A dt` / `dt − v_A dx/c²` (sem o γ, que
entra na equação do ato 2). C04 +4 s; v3 preservado em `v3_snapshot/`.

Preview v4: `renders/preview_v4_540x960.mp4` (540×960 / 15 fps, 143,0 s, 2.145 quadros, sem áudio); 3D sozinho em
`renders/parte3d_v4_540x960.mp4`; pranchas `renders/prancha_v4_*.png`. Alinhamento 3D × Manim: pior 1,15 px.

## Preview v5 — origem da álgebra e cores por foguete (27/10/2026, pedido do Kaio)

Kaio: "pulou muita álgebra", "outra cor para v_B", "a partir de 0:49 mostre de onde está vindo tudo". Mudanças:
v_A violeta, v_B e v_B′ em ciano `#35D9FF` (paleta do canal), Terra e soma simples em GEO. A C04 deixa as barras
abstratas e começa na cena (Terra): marcas nos narizes, cronômetro dt, B anda dx → `v_B = dx/dt` (o dx e o dt
voam para a fração); no mesmo dt A anda `v_A·dt` → para A, B se desloca `dx − v_A dt` (Galileu, visível). Depois,
em tela própria: definições lado a lado (NA TERRA `v_B = dx/dt`; MEDIDO POR A `v_B′ = dx′/dt′`), "se fosse só
Galileu" (`dx′ = dx − v_A dt`, `dt′ = dt`) → Lorentz (γ e o termo novo do tempo destacados, γ definido) → quociente
em passos legendados (montar a razão; γ em cima e embaixo e cancela; ÷ dt; dt/dt = 1; dx/dt = v_B). C04 +9 s;
v4 preservado em `v4_snapshot/`.

Preview v5: `renders/preview_v5_540x960.mp4` (540×960 / 15 fps, 152,0 s, 2.280 quadros, sem áudio); 3D sozinho em
`renders/parte3d_v5_540x960.mp4`; pranchas `renders/prancha_v5_*.png`. Alinhamento 3D × Manim: pior 1,15 px.

## Preview v6 — álgebra num tamanho só e derivação em coluna (27/10/2026, pedido do Kaio)

Kaio: "álgebras com tamanhos irregulares e grandes demais", "conta achatada com um termo maior que o outro", "quero
padrão e mais MF-Tools". Toda a álgebra do vídeo (C04 a C09) em MathTex 54 (dígito 23 px a 540×960, 46 px no 1080p),
sem reescala para caber (o `tex()` acusa largura > 8,4 em vez de encolher); frações internas em `\dfrac`, então
nenhum termo encolhe dentro da fração. Só o palpite `0,8c + 0,8c = ?` do hook segue grande (manchete). A C04 virou
uma derivação em coluna: as linhas ficam com o `=` alinhado e cada uma nasce de uma cópia da anterior
(`TransformByGlyphMap(from_copy=True)`); a coluna rola para cima quando falta espaço e o γ riscado fica na linha
dele. Na C08 o caso 0,99c nasce do caso 0,5c por `TransformByGlyphMap`. Tempos do timeline sem mudança; v5
preservado em `v5_snapshot/`.

## Versão final — voz, sync, legenda e master (27/10/2026)

Narração: texto da sugestão v2 (revisão do GPT) em `narracao_tags_v1.md`, voz `qw7jgPZWOKrl10GsjQ82`, `eleven_v4`,
uma tomada (`audio/narracao_v1.wav`, 141,7 s). Sync (`sync_voz.py`): forced-alignment por palavra
(`alinhar_voz.py`), 61 eventos-âncora LEAD 0,10 s antes da palavra; o timeline inteiro (3D + Manim) é reesticado por
trechos, as animações de cada trecho rodam no fator `sync.ritmo` (mín. 0,68) e, onde nem assim cabe, entra pausa na
voz só em fronteira de frase (14 pausas, 7,8 s; voz final `audio/narracao_final.wav` = `narracao_sync.wav`, 149,4 s).
`conferir_sync.py`: imagem 0,08–0,12 s antes da voz nas 61 âncoras, nenhum atraso do Manim. Mudanças de cena para a
fala: chip ① acende em "Passo um", chip ② em "Passo dois"; fecho na ordem da fala ("não se somam" antes de "corpos
com massa"). `timeline_v6_base.json` guarda o timeline silencioso. Legenda: `gerar_legenda.py` (72 blocos, ≤ 2 linhas
de 30 caracteres) com `cores_legenda.py` (A violeta, B/v_B′ ciano, 1,6c e gama GEO). Master e legendado 1080×1920 /
30 fps, CRF 14, 150,77 s.

## Preview v7 — menos texto, álgebra menor e transições MF-Tools (27/10/2026, pedido do Kaio)

Kaio, sobre o vídeo final: texto na tela repetia a narração; equações grandes e empastadas; tela poluída; quer separação
entre as equações e transições dinâmicas sem fade, só MF-Tools. Mudanças (tempos do timeline e voz sem mudança):
- saiu da tela todo texto que a voz já diz (setup, pergunta, "a resposta não é 1,6c", promessa, notas da C02/C03,
  "de onde vem a fórmula", legendas da cena Galileu, "se fosse só Galileu", "Lorentz", nota do γ, legendas PASSO 1–4,
  "o sinal só indica o sentido", "Galileu = limite...", "cada um mede...", "perto de c...", linha longa do CTA);
  ficaram tag, slot, mapa ①②③, rótulos de velocidade, resultados (1,6c NA TERRA, |v_B′| ≈ 0,976c, v_B′ ≈ v_B − v_A,
  ≈ 0,99995c < c, CORPOS COM MASSA: v < c) e o @labparallax;
- álgebra em MathTex 40 (era 54) com traço proporcional ao tamanho; o render 1080p já era nítido, o "pixelado" vinha
  do tamanho e do traço grosso;
- derivação da C04 em coluna com vão maior e ⇓ entre as linhas; linhas antigas saem por Unwrite, não por fade;
- hook: o palpite vira `0,8c + 0,8c = 1,6c ?` e depois `≠ 1,6c` por TransformByGlyphMap;
- cena → álgebra sem corte: `v_B = dx/dt` e `dx′ = dx − v_A dt` nascem na cena e sobem para a tela da álgebra;
  `v_B′ = dx′/dt′` e `dt′ = dt` nascem de cópias delas (TBGM); na razão, os lados direitos de dx′ e dt′ entram na
  fração e dx′, dt′ voltam para dentro de `v_B′ = dx′/dt′`;
- termos novos de Lorentz sublinhados (não em caixa); notas de sinal, módulo, G2 e slot do resultado por
  TransformFromCopy/TBGM a partir das linhas de cima, sem nada cruzar a conta.

Preview v7: `renders/preview_v7_540x960.mp4` (540×960 / 15 fps, 150,7 s, 2.261 quadros, sem áudio; 3D refeito no
timeline sincronizado); pranchas `renders/prancha_v7_*.png`. Sync conferido (15 fps): 61 âncoras com a imagem
0,02–0,13 s antes da voz, nenhum atraso. Aprovado pelo Kaio ("tá top agora os tamanhos") e fechado no mesmo dia: render final 1080p30 do v7 (sync no render final: 61 âncoras, imagem 0,08–0,12 s antes da voz, nenhum atraso), mesma voz `narracao_sync.wav` e mesma legenda (72 blocos); master e legendado CRF 14, 4.523 quadros, 150,77 s, substituídos em `entregas/`.

## Teste do arsenal

Não utilizado (decisão do briefing); objetos da cena (foguetes, estação, cidade, carros) em Three.js, geometria
nova no `cena3d/cena3d.js`. 3D a 540×960: 0,08 s/quadro (2.100 quadros em ~167 s, Chrome local via CHROMIUM_PATH).
