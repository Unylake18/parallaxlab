# yt_0034 · CÁLCULO III · EP. 09 · Regiões gerais e troca de ordem
## HANDOFF v1 (para o Claude Code): preview visual do vídeo inteiro, com 3D em Three.js

Data: 2026-11-13. Formato: `longo_horizontal`. Unidade nova: `videos_longos/yt_0034_regioes_gerais_troca_ordem/`. Antes de criar a pasta, confira que o número `yt_0034` está livre em `videos_longos/`. Se não estiver, pare e reporte.

**Fase:** só o **preview visual silencioso** do vídeo inteiro, em 960×540 a 15 fps (padrão do AGENTS.md para iterar). O render não tem limite de tempo: o Kaio liberou render sem economia e 3D onde a câmera ajuda. Não gerar voz, SRT, master, 1080p nem entrega. Não fazer commit nem push.

Este handoff é autocontido. Tudo o que você precisa está nele e no zip `yt0034_handoff_v1_completo.zip`:
- `yt_0034_quadros_alvo_v1/` traz os **26 quadros-alvo** (1920×1080), a `00_folha_contato_v1.jpg` e os geradores:
  - `c3d34.html` (Three.js r128, `?k=<chave>`) gera os **4 quadros 3D de referência** (`b31`, `b32`, `b42p`, `b42`). Ele tem a geometria, as câmeras, as cores e a função `proj()`, que dá os pontos de tela em px. Ao lado estão as imagens `r3d_<chave>.png` e os pontos em `r3d_pts.json`. **Porte essas cenas para a unidade** (§2.2): elas são o modelo exato, não uma inspiração.
  - `sb34.html` (Canvas + KaTeX, `?k=<chave>`) gera os quadros completos. Abra-o com as fontes, `logo_crop.png`, `katex/`, `three.min.js` e `r3d_pts.js` do lado. Chaves: `h1 h2 a1 b11 b12 b13 b21 b22 b31 b31L b32 b32L b41 b42p b42 b42L b43 b51 b52 b61 b71 b71m b72 b8 s1 s2`.
  - `r3d.js` e `shot.js` são os scripts Playwright que geraram os PNGs. Servem só de referência.
- `narracao_v2.md` é a **narração aprovada** (3.027 palavras ≈ 16:59), por âncora, com a **Tela** e os **Gatilhos** de cada âncora, mais a tabela de leitura dos símbolos (Anexo B). É ela que dá os tempos e as frases de disparo. A mesma narração está no Anexo A deste handoff.
- `verificacao/verifica_calc3_33t2_sympy.py` e a saída dele somam **34 checagens, todas `True`**. Todos os números da tela saem dali.

A matemática, o roteiro, a narração e os textos estão aprovados pelo Kaio. Não rediscuta. Se encontrar uma inconsistência objetiva, reporte antes de mudar.

**Regras da série (Kaio):**
- **Figura:** toda definição ou enunciado formal aparece com a sua figura.
- **Origem:** todo símbolo nasce do desenho, por `TransformFromCopy` do objeto para a fórmula ou pela caneta. Nada aparece pronto.
- **Álgebra passo a passo:**
  - a fórmula-mãe vem antes do número;
  - cada valor voa da fonte;
  - cada passo é um `TransformByGlyphMap` com mapa explícito;
  - não há linha órfã começando por "=".
- **"Sensacional" quer dizer clareza.** Nada de partícula, brilho, sombra, névoa, contorno em seta, luz que lava a cor ou câmera girando sem motivo.

**Lições dos EP. 06 a 08, já incorporadas aqui** (não as repita):
- MF-Tools de verdade, sem `mapa_glifos` próprio com `FadeIn`;
- nenhum bloco abrindo vazio;
- palco parado medido só no palco;
- R5 testado também durante as animações;
- frase portuguesa sempre em Space Grotesk, nunca em serifa dentro de `MathTex`;
- `\dfrac` sempre;
- cartão do próximo vídeo por ≥ 8 s.

Tudo isso está nas regras do §3.2 e no QA do §8.

**A imagem-mãe deste vídeo:** a fatia que **entra** por uma curva (azul-claro) e **sai** por outra (coral). Ela aparece em todos os blocos, sempre com o ponto de entrada azul-claro e o de saída coral. E a imagem que volta três vezes: **a fatia deitada que vira retângulo** (cunha, sino, seno de x³).

---

## 0. O que entregar

1. A unidade nova, com:
   - `ficha.md` (§1);
   - `cena.py` e uma seção `sec_*.py` por bloco (H, A, B1 … B8, S);
   - `threejs/`, com as cenas 3D, o renderizador por quadro e os pedidos (§2.2).
2. O preview do vídeo inteiro, `renders/v1/yt_0034_preview_v1_540p15.mp4`, com a duração da narração (§6). Junto, `duracoes_estimadas.json`.
3. A prancha **render × alvo** `renders/v1/qa/comparacao_v1.jpg`. Ela tem uma linha por quadro-alvo, com o still do render no gatilho ao lado do alvo, para os 26 alvos.
4. Os relatórios de QA em `renders/v1/qa/` (§8):
   - `sobreposicoes_v1.txt`
   - `alinhamento3d_v1.txt`
   - `flash_por_quadro_v1.txt`
   - `palco_parado_v1.txt`
   - `texto_em_mathtex_v1.txt`
   - `glyph_maps_v1.txt`
   - `origens_v1.txt`
   - `tempos_render_v1.txt`
5. O relatório de entrega do AGENTS.md: arquivos, renders, QA e pendências.

## 1. Ficha

```
formato: longo_horizontal
tipo: teoria_visual
serie_publica: CÁLCULO III · EP. 09
titulo: Regiões gerais e troca de ordem
disciplina: Cálculo III
modulo: 3.3 Cálculo de integrais duplas (o docs/mapa_curricular.md do repositório ainda usa a numeração antiga)
bloco: 3.3-T2
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §3.1, Exemplos 4 a 14 e Corolários 1 e 2 (só na descrição do YouTube; nada de livro na tela nem na fala)
unidades: x e y em metros; densidade em kg/m²; massa em kg; áreas em m²
solido_3d: nenhum do arsenal Blender (a cunha z = y sobre o quarto de disco e o sino z = e^(−y²) sobre o triângulo, feitos direto em Three.js, como nos EP. 05 a 08)
3d_threejs: cena1 = cunha z = y sobre o quarto de disco de raio 2 (b31 faca em pé em x = 1 + pouso lateral = triângulo; b32 faca deitada em y = 1 + pouso lateral = retângulo); cena2 = sino z = e^(−y²) sobre o triângulo 0 ≤ x ≤ y ≤ 1 (b42p faca em pé em x = 0,4, teto curvo, sem pouso; b42 faca deitada em y = 0,6 + pouso lateral = retângulo)
duracao_alvo: ≈ 17 min (narração v2: 3.027 palavras ≈ 16:59)
```

## 2. Base de código

### 2.1 Manim

- **Antes de começar:**
  - leia `docs/estado_atual.md`;
  - rode `verificacao/verifica_calc3_33t2_sympy.py` com o Python da `.venv` (as 34 linhas devem dar `True`). Se faltar sympy ou scipy, não instale nada: diga no relatório e siga.
- **Copie, não importe.** Copie o kit da unidade mais recente da série de Cálculo III que estiver no seu checkout, nesta ordem de preferência: `yt_0033_*`, `yt_0032_*`, `yt_0031_*`, `yt_0029_*`. Do kit vêm:
  - `kit.py` e `render.sh`;
  - o canto de duas linhas e `placa_min`;
  - a caneta (`TC`/`TX`), `painel`, `mixl` e o sublinhado de leitura;
  - a chapa x² + y² (mapa ciano), a chapa de dois metais com a solda `g(x)` e o quarto de disco (EP. 05 a 08).

  Se essas unidades não estiverem no seu checkout, use a mais recente que houver. Este handoff não depende delas. Não altere as outras unidades.
- **Fundo:**
  - Gráficos: violeta liso `#18143A → #0F0C26` na câmera, mais a grade `papel(ax)` de `assets/calculo/papel.py`, que nasce dos eixos de cada palco ou painel (quadradinho de 0,25 da unidade do gráfico, sem linhas grossas). Nos alvos, a grade só existe dentro do palco; fora dele o fundo é liso.
  - Cenas 3D: só o violeta liso, sem grade.
  - Cartões sem gráfico (A1, B7-2, B8, S1 lado esquerdo): só o violeta liso.
- Render por bloco (`render.sh <Classe>`), depois concatene.
- **Sem economia artificial**, mas sem updater à toa:
  - a fatia que desliza no B1-1 (x de 0 a quase 2) é um `ValueTracker` só, ligado à tira, aos dois pontos e à placa;
  - a reta-sonda do B2-2 e a tira deitada do S2 são um `ValueTracker` cada;
  - o mapa ciano da chapa (B5) é uma imagem estática ou uma grade de quadradinhos sem contorno, com a cor calculada uma vez.
- Limpe da cena o que saiu da tela. Não deixe nada invisível acumulando.

### 2.2 Three.js (o pipeline da série)

- **Copie o pipeline** da unidade de Cálculo mais recente que tiver `threejs/` (yt_0033, se estiver no checkout; senão yt_0026, `videos_longos/yt_0026_funcoes_vetoriais_campos/threejs/`). Vêm `r3d.js`, `package.json` (playwright-core), `cena3d/three.min.js` (r128) e o esquema de pedidos:
  1. A passagem seca do Manim grava `pedidos3d/<LOTE>.json` com `{cena: [[quadro, estado], …]}`.
  2. `r3d.js` abre `cena3d/<cena>.html`, chama `window.setEstado(estado)` quadro a quadro e grava os PNGs com alfa e o `pontos.json`.
  3. O Manim cola os PNGs como `ImageMobject` em tela cheia e prende os rótulos nos pontos.
- **Porte as cenas de `c3d34.html`** para `threejs/cena3d/`. Vêm de lá:
  - `solido(p, h, {nu, nv, off, cor})`: sólido sobre uma região parametrizada `p(u, v) → [x, y]`, com o topo na cor por altura e as quatro paredes de borda (a 70 % e 48 %, conforme a orientação, ou na cor forçada da face cortada);
  - `chao()` (o piso #1C1846 com contorno GEO), `contorno()` (borda escura da face cortada) e `eixos()`;
  - `W3(X, Y, v, off)` (mundo = `SC` · metros; altura = `SC · ZS` · valor) e as câmeras `ver(pos, alvo, cx, cy)` com `setViewOffset`.

  Valores de cada chave: `b31` e `b32` com `SC = 1`, `ZS = 1`, `VMAX = 2`; `b42p` e `b42` com `SC = 2`, `ZS = 1`, `VMAX = 1,15`. Câmera perspectiva, up = +z. **Atenção:** `c3d34.html` desenha só o estado final de cada chave, o do quadro-alvo. Os estados abaixo são nomes sugeridos, e a animação entre eles é sua.
- **Estados por cena:**

  | cena | estados | o que anima |
  |---|---|---|
  | cena1 (cunha z = y) | `cresce` 0→1 · `faca` (`tipo`: em pé em x = 1 ou deitada em y = 1) · `afasta` 0→1 · `pouso` 0→1 | B3-1: o quarto de disco no chão, a cunha sobe, a faca em pé entra em x = 1, a parte x > 1 recua em +x (`D = 0,75`), a face âmbar acende, pouso. B3-2: volta à vista do alvo 11, a faca deitada entra em y = 1, a parte y < 1 desliza para a frente e para o lado (`off = [2,35; −0,9]`), a face magenta acende, pouso |
  | cena2 (sino z = e^(−y²)) | `cresce` · `faca` (em pé em x = 0,4; deitada em y = 0,6) · `afasta` · `pouso` | B4-2: o triângulo no chão, o sino sobe, faca em pé (a parte x > 0,4 recua `D = 0,85`, face âmbar de teto curvo, **sem pouso**), a faca sai e o sólido se fecha; faca deitada (a parte y < 0,6 desliza para `off = [1,75; −0,55]`), face magenta = retângulo, pouso |

- **Pouso lateral (três vezes: B3-1, B3-2 e B4-2).** É a passagem 3D → 2D, a assinatura da série.
  - A câmera vai, num movimento lento com começo e fim suaves (≈ 2,5 s), até a **vista frontal ao plano da fatia**:
    - fatia em pé (x fixo): olhando de +x para −x, com y crescendo para a direita e z para cima;
    - fatia deitada (y fixo): olhando de −y para +y, com x crescendo para a direita e z para cima.
  - No fim do pouso a projeção precisa ser **ortográfica**, porque é ela que vira o painel 2D. Faça o pouso em perspectiva com a câmera se afastando e o fov fechando (dolly-zoom) até a perspectiva ficar desprezível. No último quadro, troque para `OrthographicCamera`; a diferença tem de ficar ≤ 2 px.
  - **O que fica na frente da fatia sai antes**, porque não pode haver transparência. A parte cortada que está entre a câmera e a face desliza para fora do quadro durante a primeira metade do pouso (nos alvos 11 e 15 ela já está deslocada para o lado; no pouso ela termina de sair).
  - **Escala:** no quadro da troca, o 2D precisa coincidir com o 3D.
    - Cena 1 (alvos 10 e 12): painel lateral com origem em (200, 880) px a 1080p e **1 m = 300 px nos dois eixos**. Como a cena 1 tem `ZS = 1`, a altura z = y já sai na mesma escala.
    - Cena 2 (alvo 16): painel com origem em (200, 820), **1 m = 560 px no eixo x e 440 px por unidade de f**. A cena tem `ZS = 1`, então escolha uma das duas saídas e diga no relatório qual usou: (a) ajuste `ZS` sem o espectador ver (`ZS = 440/560 ≈ 0,786`); (b) construa o 2D com a escala vertical do 3D (560 px por unidade).
  - O 2D entra **por cima, no mesmo quadro** em que o PNG 3D sai. Os eixos, o contorno da fatia e a área nascem sobre as arestas projetadas. **Alinhamento ≤ 2 px** entre o contorno 2D e o contorno da fatia no último PNG, medido e registrado.
- **Estilo 3D da série:**
  - opaco e sem luz (`MeshBasicMaterial`);
  - topo na cor por altura (rampa escura → ciano), paredes a 70 % e 48 % sobre o fundo;
  - face cortada em pé âmbar `#FFC24D`, face cortada deitada magenta `#EA63FF`, com contorno escuro fino;
  - sem sombra, névoa, brilho ou transparência;
  - `outputEncoding` linear e antialias ligado.

  **O plano da faca é um retângulo opaco e fino, só a borda** (âmbar para a faca em pé, magenta para a deitada). Nada de transparência.
- **Rótulos são do Manim**, presos aos pontos do `pontos.json` do mesmo quadro. Quando a câmera se move, o rótulo anda junto. Alinhamento ≤ 2 px. Pontos já exportados no alvo:
  - `b31`: `fatia`, `faca`, `base`, `alt`, `x1`, eixos `ex`, `ey`, `ez`;
  - `b32`: `fatia`, `faca`, `base`, `alt`, `y1`, eixos;
  - `b42p`: `fatia`, `teto`, `faca`, `x1`, eixos;
  - `b42`: `fatia`, `teto`, `faca`, `base`, `alt`, `y1`, eixos.

  O eixo y fica escondido atrás do sólido nos quatro ângulos: **não rotule o y no 3D** (ele aparece no painel lateral). O `x` do alvo 11 fica na parte visível do eixo, antes da peça deslocada.
- **Câmera:**
  - movimentos lentos com começo e fim suaves;
  - no máximo um movimento por ideia;
  - **a câmera nunca se mexe enquanto uma fórmula está sendo escrita**;
  - nada de órbita só para "dar movimento";
  - nada do 3D passa de x = 1090 px (a coluna começa em 1120).

## 3. Sistema visual

### 3.1 Layouts e escala

| layout | geometria a 1080p | blocos |
|---|---|---|
| **A · palco + fórmulas** | Coluna de fórmulas alinhada à esquerda em **x = 1120**. Três palcos: **quarto de disco / chapa** R = [0, 2]² com 1 m = 240 px e o canto (0, 0) em (360, 780) px; **triângulo unitário** [0, 1]² com 1 = 560 px e a origem em (260, 860); **telhado** [−1, 1] × [0, 1] com 1 = 420 px e a origem em (560, 800). | H1, H2, B1-1, B1-3, B2, B4-1, B5, B6-1, B7-1 |
| **A-pequeno** | Palco do quarto de disco menor (1 m = 200 px, origem em (300, 640)) com o painel 1D da fatia embaixo (origem em (300, 975), 1 m = 200 px). | B1-2 |
| **L · vista lateral + fórmulas** | Painel lateral da cena 1: eixo horizontal (y magenta no triângulo, x âmbar no retângulo), eixo vertical f (ciano), origem em (200, 880), 1 m = 300 px nos dois eixos. Painel da cena 2: eixo x âmbar, origem em (200, 820), 560 px por metro e 440 px por unidade de f. Coluna em x = 1120. | B3-1, B3-2, B4-2, S1 (miniatura) |
| **3D · palco + fórmulas** | O 3D ocupa a esquerda (objeto centrado perto de x = 580–600 px por `setViewOffset`). A coluna continua em x = 1120. | B3-1, B3-2, B4-2 |
| **E · erro clássico** | Forma errada à esquerda (x = 200) e cartão da forma certa à direita (moldura de 1060 a 1840, com o triângulo pequeno: 1 = 300 px, origem em (1300, 700)). | B4-3 |
| **C · cartões** | 3 cartões de 520 × 700 (x = 100, 700, 1300), só a moldura (`#B8C4DA` a 35 %, raio 14), com um desenho de traço GEO cada. | B8 |

Conversão para o Manim: x_m = (x_px − 960)/135; y_m = (540 − y_px)/135.

### 3.2 Regras (as da série + as lições dos EP. 06 a 08)

- **R1 · Clareira:** nenhum rótulo sobre ponto, aresta, linha da grade ou número; o rótulo sai para o lado.
- **R2 · Placa:** todo rótulo solto sobre o desenho ou sobre o 3D usa `placa_min`.
- **R3:** fórmula nova nunca nasce sobre fórmula velha; a coluna limpa antes.
- **R4:** rótulo junto do objeto que ele nomeia; **o rótulo sai junto com o seu objeto** (nada de legenda órfã depois de uma transição).
- **R5:** QA automático de sobreposição, amostrado a cada 0,5 s **inclusive durante as animações** (§8).
- **R6:** nada sai da moldura do seu painel ou cartão; nada do 3D invade a coluna (x ≥ 1090).
- **R-texto:**
  - **Palavra é Space Grotesk** (`Text`, maiúsculas); matemática é `MathTex`.
  - Uma linha mista é `Text` + `MathTex` lado a lado, com respiro ≥ 0,15 (ver `mixl()` no `sb34.html`, alvos 04, 07 e 13).
  - Nenhuma frase portuguesa dentro de `MathTex`. O `EM B`, o `FORA`, o `CONTÍNUAS EM` e o `SEM PRIMITIVA EM FÓRMULA` são `Text`.
  - Cada legenda tem no máximo 6 palavras e pelo menos 26 px a 1080p. As legendas de apoio dos alvos em 22–24 px (`CAIXINHAS`, `3,25 · 3,17 · 3,15`, `CHEIA / 1 CORTE / 2 CORTES`, `ANA`, `HORÁRIOS UNIFORMES`, `UMA FATIA`, os selos `TIPO I / II`) sobem para 26 px.
- **Fração:** sempre `\dfrac`, com o glifo da fração ≥ 26 px a 1080p. Nenhum rótulo girado. `grep -n tfrac` = 0.
- **Glifos:** zero em legenda vai por extenso (`ZERO`), porque o 0 do Space Grotesk parece O. Zero como **valor** (os `0` fora de B no alvo 04, os `0` do painel da fatia no alvo 05, os limites de integração) é `MathTex`. Nos números com vírgula decimal, use `{,}` no LaTeX.
- **Sublinhado de leitura:** quando a voz lê um símbolo (Anexo B da narração: "dê ípsilon", "cê de xis", "contido", "menor ou igual", "é elevado a", "raiz de"), um sublinhado fino aparece sob ele no gatilho falado e sai. Não é pulso nem brilho.
- **Um movimento por ideia, uma vez.** Uma figura nova nasce da velha (`ReplacementTransform`) e nunca pisca.
- **Nenhum bloco abre vazio:**
  - a linha 2 do canto está na tela desde o primeiro quadro de cada bloco;
  - a figura do bloco anterior fica até a nova nascer dela, ou a nova começa a entrar em ≤ 0,5 s;
  - palco vazio por mais de 0,5 s: zero ocorrências.
- **Palco parado:**
  - Medida: trecho em que menos de 40 px do **palco** (máscara sem a coluna e sem o canto, a 960×540) mudam mais de 8 níveis ao longo de 3 s.
  - Limite de 3 s. De 3 a 5 s só é aceito se a voz estiver lendo o que está no palco, com o motivo no relatório. Acima de 5 s: zero.
  - Se a fala continua e a cena acabou, o próximo passo entra mais cedo.
- **Pontos e marcas só os do alvo:** os únicos pontos são o de entrada (azul-claro) e o de saída (coral) de cada tira, mais os vértices do triângulo no alvo 13. Nenhum ponto de debug.

### 3.3 Cores

| Papel | Cor |
|---|---|
| f, ρ, a superfície (cor por altura), valores de f, o mapa x² + y², e^(−x²) do B8 | ciano `#35D9FF` |
| x, fatia em pé, faca em pé, a, b (limites de fora em x), `dx` | âmbar `#FFC24D` |
| y, fatia deitada, faca deitada, c, d (limites de fora em y), `dy` | magenta `#EA63FF` |
| **Curva de entrada** (limite de baixo de dentro: c(x), a(y)) e o ponto de entrada | azul-claro `#7FB2FF` |
| **Curva de saída** (limite de cima de dentro: d(x), b(y)) e o ponto de saída | coral `#FF7A8A` |
| Região B | GEO `#B8C4DA` a ≈ 18 % sobre o fundo |
| Diagonal y = x da chapa, solda g(x), reta-sonda, retas auxiliares | branco `#F5F7FF` |
| Tese, ✓, `MESMA REGIÃO, OUTRA ORDEM`, `PASSO 1/2/3`, `2,4721 m²` | menta `#8CFFD2` |
| Erro clássico, fronteira do B1-2, `SEM PRIMITIVA EM FÓRMULA`, `DOIS TRECHOS?` | ALERTA `#FF5D5D` |
| Metal leve / metal pesado | `#1E5072` / `#30BBE0` |
| Grade, réguas, molduras, cartões, legendas secundárias | GEO `#B8C4DA` |

- Operadores (∫, ∬, ≤, ⇔, ⇒, { }, :) ficam em branco, e a cor vai na grandeza.
- **Limites de dentro:** o limite inteiro na cor da curva (azul-claro se é por onde a fatia entra, coral se é por onde sai), e só o x ou o y dentro dele na cor da variável (ex.: `√(4 − x²)` em coral, com o x em âmbar).
- **A mesma curva troca de cor quando a ordem troca.** A diagonal y = x é a **entrada** da tira em pé do triângulo do sino (azul-claro) e a **saída** da tira deitada (coral, como `x = y`). A cor sempre diz o papel na fatia que está na tela; quando a tira troca de direção, a curva troca de cor junto, num movimento só.
- Nas iteradas, o `dy` é magenta e o `dx` é âmbar, para a ordem "de dentro para fora" se ver pela cor.

### 3.4 Álgebra

- **Caneta** em toda fórmula nova: traço finíssimo (~0,7), glifo a glifo, da esquerda para a direita, preenchendo na cor da grandeza, sem flash e sem preview do destino.
- Um termo que nasce no desenho **voa** para a fórmula (`TransformFromCopy`, em arco). No 3D, ele voa a partir do ponto projetado. Os voos obrigatórios deste vídeo:
  - **B1-1:** o `√3` voa do ponto de saída da tira para o limite de cima da integral.
  - **B4-1 (ao contrário):** os quatro limites voam **da fórmula para o desenho**: `0` e `1` para o eixo x, `x` vira a reta `y = x` (azul-claro), `1` vira a reta `y = 1` (coral).
  - **B4-2:** o `y` do comprimento da fatia (a chave `COMPRIMENTO DA FATIA` do painel lateral) voa para dentro de `∫₀¹ y e^(−y²) dy`.
  - **B5-1:** o `x` voa da diagonal para o limite de cima; **B5-2:** o `y` voa da diagonal para o limite de baixo.
  - **B6-1:** o `x²` voa da parábola para o limite de cima e, depois, para o fator `x²` de `x² sen(x³)`.
- **MF-Tools de verdade:**
  - `from MF_Tools import TransformByGlyphMap` (1.4.9), com `MathTex` de string única nos dois lados e mapa explícito.
  - O glifo que sai usa `auto_fade` (ou entra no mapa com destino vazio).
  - O glifo que **entra** nunca usa `FadeIn`: fica fora do mapa e é escrito com a caneta logo depois, ou voa da fonte.
  - Não use função própria de mapa de glifos.
  - `show_indices` só no desenvolvimento.
- **Glyph maps obrigatórios** (12):
  1. H1: `∫₀¹ ∫ₓ¹ e^(−y²) dy dx` → `∫₀¹ ∫₀^y e^(−y²) dx dy` (o `dy dx` troca de lugar; os limites que mudam, `x`/`1` → `0`/`y`, acendem juntos e se transformam; o resto fica parado).
  2. B1-1: `1² + y² = 4` → `y² = 3` → `y = √3`.
  3. B1-3: `∫₀² ∫₀^{√(4−x²)} 1 dy dx` → `= ∫₀² √(4 − x²) dx` (a integral de dentro vira o comprimento da fatia; o `1 dy` sai) → `= π · 2²/4 = π`.
  4. B3-1: `∫₀^{√(4−x²)} y dy` → `= y²/2 |₀^{√(4−x²)}` → `= (4 − x²)/2` (o quadrado come a raiz).
  5. B3-1: `∫₀² (4 − x²)/2 dx` → `= (8 − 8/3)/2` → `= 8/3`.
  6. B3-2: `y = √(4 − x²)` → `y² = 4 − x²` → `x² = 4 − y²` (o `x²` e o `y²` **atravessam a igualdade**, cada um trocando de sinal) → `x = √(4 − y²)`, com a placa `x ≥ 0` (MathTex).
  7. B3-2: `∫₀^{√(4−y²)} y dx` → `= y√(4 − y²)` (o y sai da integral como altura fixa) → `∫₀² y√(4 − y²) dy = [−(4 − y²)^{3/2}/3]₀² = 8/3 ✓`.
  8. B4-2: `∫₀¹ ∫₀^y e^(−y²) dx dy` → `= ∫₀¹ y e^(−y²) dy` (a integral de dentro e o `dx` saem; o `y` entra por voo, não por mapa) → `= [−e^(−y²)/2]₀¹` (o `y` e o `−y²` acendem juntos antes: "quase a derivada") → `= (1 − 1/e)/2` → `≈ 0,316` (o exato primeiro, sempre).
  9. B4-3: `∫₀¹ ∫ₓ¹ e^(−y²) dx dy` (a forma errada) → `= (1 − x) · ∫₀¹ e^(−y²) dy` (o `x` do limite e o `dx` acendem juntos em ALERTA antes).
  10. B5-1: `∫₀ˣ (x² + y²) dy` → `= x² · x + x³/3` → `= 4x³/3` → `∫₀² (4/3) x³ dx = (4/3) · 2⁴/4 = 16/3`.
  11. B5-2: `∫_y² (x² + y²) dx` → `= 8/3 + 2y² − 4y³/3` → `∫₀² (…) dy = 16/3 + 16/3 − 16/3` → `= 16/3 ✓`.
  12. B6-1: `x = √y` → `y = x²` (o quadrado atravessa) e `∫₀¹ ∫₀^{x²} sen(x³) dy dx` → `= ∫₀¹ x² sen(x³) dx` → `= (1 − cos 1)/3` → `≈ 0,153`.
- **Tamanhos:** fórmula principal de 44–52 px no alvo; secundária de 34–42 px; índice ≥ 22 px; nada menor que 26 px fora dos índices.
- **Arredondamento na tela:** o exato vem antes do decimal e o decimal sempre com `≈`: `(1 − 1/e)/2 ≈ 0,316`, `(1 − cos 1)/3 ≈ 0,153`, `π ≈ 3,1416`, `7/16 ≈ 44 %`. A área do metal leve leva `≈ 2,4721 m²` (no alvo 22 está com `=`: **use `≈`**).

## 4. Números (todos conferidos no script)

- **Quarto de disco** B = {x² + y² ≤ 4, x ≥ 0, y ≥ 0} dentro de R = [0, 2]²:
  - em x = 1 a fatia sai em y = √3 ≈ 1,732; ∫₀² F(1, y) dy = ∫₀^√3 f(1, y) dy (o zero não soma);
  - área ∫₀² √(4 − x²) dx = **π**; caixinhas do EP. 05: **3,25 · 3,17 · 3,15** (sem dizer o número do vídeo).
- **Cunha z = y** no quarto de disco: em pé ∫₀^{√(4−x²)} y dy = (4 − x²)/2 (triângulo de base e altura √(4 − x²)), ∫₀² = **8/3**; deitado ∫₀^{√(4−y²)} y dx = y√(4 − y²), ∫₀² = [−(4 − y²)^{3/2}/3]₀² = **8/3**.
- **Sino** (Guidorizzi Ex. 8): triângulo 0 ≤ x ≤ y ≤ 1 (vértices (0, 0), (0, 1), (1, 1), área 1/2); ∫₀¹ y e^(−y²) dy = **(1 − 1/e)/2 ≈ 0,316**. A forma errada deixa (1 − x) · ∫₀¹ e^(−y²) dy, função de x.
- **Chapa x² + y²** (massa 32/3 kg) cortada na diagonal: em pé β(x) = 4x³/3, ∫₀² = **16/3**; deitado α(y) = 8/3 + 2y² − 4y³/3, ∫₀² = 16/3 + 16/3 − 16/3 = **16/3**; espelho 16/3 + 16/3 = **32/3**.
- **Seno de x³** (Ex. 9): 0 ≤ y ≤ 1, √y ≤ x ≤ 1 ⇔ 0 ≤ x ≤ 1, 0 ≤ y ≤ x²; ∫₀¹ x² sen(x³) dx = **(1 − cos 1)/3 ≈ 0,153**.
- **Telhado** (−1, 0), (0, 1), (1, 0): em pé 1/2 + 1/2 (duas contas, saídas `y = 1 + x` e `y = 1 − x`); deitado ∫₀¹ ∫_{y−1}^{1−y} dx dy = **1** (uma conta).
- **Metal leve** (solda g(x) = 1 + 0,42 sen(1,7x − 0,4)): g(0) = 0,836, g(2) = 1,059, máximo 1,42 em x ≈ 1,16; em pé ∫₀² g ≈ **2,4721 m²**; deitado 1,6729 (cheia até 0,836) + 0,4097 (1 corte até 1,059) + 0,3895 (2 cortes até 1,42) = 2,4721. Faixas no alvo: tira cheia em y = 0,42; 1 corte em y = 0,95 (de x ≈ 0,27 a 2); 2 cortes em y = 1,24 (de x ≈ 0,61 a 1,71).
- **Encontro:** |x − y| ≤ 1/4 no quadrado [0, 1]², área = 1 − (3/4)² = **7/16 ≈ 43,75 %** (tela: `≈ 44 %`).
- **Gancho** (Ex. 12): y = x e y = 4x − x², 0 ≤ x ≤ 3; y = 4x − x² ⇔ x = 2 ∓ √(4 − y); deitado: entra no ramo esquerdo `x = 2 − √(4 − y)`, sai na reta `x = y` até y = 3 e no ramo direito `x = 2 + √(4 − y)` de 3 a 4. Área 9/2 (não aparece na tela).

## 5. Cena a cena

- **Gatilho** é a frase da narração (Anexo A) em que a ação começa. Cada âncora do Anexo A tem a sua lista **Gatilhos: "frase" → ação**. Siga-a inteira; abaixo só vai o que o Anexo não diz ou o que precisa de cuidado.
- **Alvo** é o quadro em `yt_0034_quadros_alvo_v1/`, reproduzido com tolerância de ±20 px na posição e ±5 % no tamanho. Onde o alvo e este texto divergirem, vale o texto.
- **Canto:** a linha 1 é `CÁLCULO III · INTEGRAL DUPLA`, e a linha 2 é o título da cena que está no alvo.

### H · uma integral que trava · alvos 01 e 02
- **H1 (alvo 01, estado final).** A ordem segue a voz (gatilhos do Anexo A).
  - "Olha esta integral": `∫₀¹ ∫ₓ¹ e^(−y²) dy dx` a caneta **no centro da tela** (52 px), com o sublinhado de leitura no gatilho de cada parte (Anexo B).
  - "E aí trava": um `?` a caneta ao lado do `e^(−y²)` e a placa `SEM PRIMITIVA EM FÓRMULA` (ALERTA, `Text`).
  - "com a ordem trocada": a integral sobe para a coluna (x = 1120) e o glyph map 1 dá `∫₀¹ ∫₀^y e^(−y²) dx dy`.
  - "zero vírgula três um seis": `= (1 − 1/e)/2 ≈ 0,316` (o exato primeiro).
  - "os limites mudaram": o `x`/`1` da primeira e o `0`/`y` da segunda acendem juntos na coluna (sublinhado, sem pulso).
  - "um triângulo": o triângulo nasce no palco atrás da coluna, com a tira em pé (pontos `x` azul-claro e `1` coral) e a tira deitada (`0` azul-claro e `y` coral): os quatro limites acendem no desenho. `MESMA REGIÃO, OUTRA ORDEM` em menta. Este é o estado do alvo.
  - "não é um retângulo": corte seco para o alvo 02.
  - **Nota:** o texto de Tela da proposta v2 pedia o triângulo antes da conta, mas a narração aprovada diz o resultado antes de "os limites mudaram". Vale a voz: o triângulo entra depois da conta, como acima.
- **H2 (alvo 02).** O quarto de disco de raio 2 com a tira em pé em x = 1, o ponto de entrada em `y = 0` (azul-claro) e o de saída no arco (coral, `y = √(4 − x²)`). Coluna: a iterada com os limites coloridos, `LIMITES DE FORA: NÚMEROS` (âmbar), `LIMITES DE DENTRO: CURVAS` (coral) e, embaixo, `TROCAR A ORDEM = RELER A REGIÃO` (menta).

### A · bem-vindos · alvo 03
Padrão do canal: logo; `CÁLCULO DE INTEGRAL DUPLA · VÍDEO 2` (ciano, pequeno); título `REGIÕES GERAIS E TROCA DE ORDEM`; `NESTE VÍDEO`. As cinco etiquetas `1 · A FATIA NA CURVA`, `2 · O TEOREMA`, `3 · DUAS ORDENS`, `4 · A TROCA` e `5 · QUANDO VALE` entram uma por palavra falada. A quarta tem o texto em menta. Etiquetas em 26 px (no alvo estão em 24).

### B1 · a fatia na curva · alvos 04 a 06
- **B1-1 (alvo 04).**
  - O quarto de disco do H2 fica; entra o retângulo R = [0, 2]² tracejado em volta (`B ⊂ R`, com o sublinhado em `⊂`), e os `0` (MathTex GEO apagado) aparecem fora de B, dentro de R.
  - Coluna: `F = f EM B · F = 0 FORA` (linha mista).
  - "xis congelado em um": a reta tracejada âmbar em x = 1; em "só soma zeros", a tira acende de y = 0 a y = √3 e fica tracejada, apagada, de √3 a 2.
  - `∫₀² F(1, y) dy = ∫₀^√3 f(1, y) dy`, com o `√3` voando do ponto de saída em "raiz de três"; depois glyph map 2 (`1² + y² = 4 ⇒ y = √3`).
  - "deixa o xis andar": um `ValueTracker` leva x de 0 a 1,9 e volta a 1. A tira, os dois pontos e a placa da saída andam juntos. Em "raiz de quatro menos xis ao quadrado" o arco ganha o rótulo coral `y = √(4 − x²)`, e em "ípsilon igual a zero" o eixo ganha o azul-claro `y = 0`.
  - `A FATIA TERMINA NA CURVA` em coral.
- **B1-2 (alvo 05), layout A-pequeno.**
  - Duas caixas vazias na coluna ("duas coisas").
  - "fronteira de B": o arco e os dois segmentos acendem finos em ALERTA, com `CONTEÚDO NULO`; a primeira caixa ganha o ✓ e `F INTEGRÁVEL EM R`.
  - "zero, depois f, depois zero": o painel 1D embaixo nasce com o eixo y magenta e o vertical f ciano: `0` | `f` | `0`, com os dois saltos tracejados em ALERTA e `DOIS SALTOS`. **Correção ao texto da proposta:** no quarto de disco a fatia em x = 1 tem um salto só (em y = √3), então o painel mostra **uma fatia qualquer** de uma região entre duas curvas (legenda `UMA FATIA`), como no alvo.
  - A segunda caixa ganha o ✓ e `FATIA INTEGRÁVEL`.
  - "garante": `TEOREMA DE FUBINI` (GEO) e `⇒ ∬_B f dA = ∫_a^b ∫_{c(x)}^{d(x)} f dy dx` a caneta.
  - "nada de especial do disco": o disco se transforma (`ReplacementTransform`) na região genérica do alvo 07, e isso já é o B2.
- **B1-3 (alvo 06).**
  - "f igual a um": a coluna começa; "comprimento da fatia": um segmento âmbar acende; "dá a área": as fatias âmbar varrem o disco da esquerda para a direita (10 traços, um `LaggedStart`).
  - Glyph map 3 na coluna.
  - "três vírgula vinte e cinco" … "três vírgula quinze": a régua com os pontos `3,25`, `3,17`, `3,15` (GEO) e o ponto menta `π ≈ 3,1416`. Rótulos a 26 px, sem tocar uns nos outros (o `3,15` e o `3,17` estão apertados no alvo: desça um deles para baixo da régua se precisar).

### B2 · o teorema · alvos 07 e 08
- **B2-1 (alvo 07).**
  - A região genérica entre `y = c(x)` (azul-claro) e `y = d(x)` (coral), de `x = a` a `x = b` (tracejados âmbar). A tira em pé com os pontos de entrada e saída.
  - Enunciado a caneta, linha por linha, cada uma no seu gatilho:
    - `c, d CONTÍNUAS EM [a, b], c(x) ≤ d(x)` (linha mista);
    - `B = {(x, y) : a ≤ x ≤ b, c(x) ≤ y ≤ d(x)}`;
    - `f CONTÍNUA EM B`;
    - `⇒ ∬_B f dx dy = ∫_a^b [∫_{c(x)}^{d(x)} f(x, y) dy] dx`.
  - Sublinhado de leitura nos `≤` ("menor ou igual"), nas chaves `{ }` ("As chaves") e no `:` ("tais que"), cada um no seu gatilho.
  - Selo pequeno `REGIÃO EM PÉ (TIPO I)` em GEO.
- **B2-2 (alvo 08).**
  - "Trocando os papéis": a região genérica dá lugar à deitada (`ReplacementTransform`, um movimento): `x = a(y)` à esquerda (azul-claro), `x = b(y)` à direita (coral), entre `y = c` e `y = d` (tracejados magenta).
  - Coluna: `B = {(x, y) : c ≤ y ≤ d, a(y) ≤ x ≤ b(y)}`, `∬_B f = ∫_c^d [∫_{a(y)}^{b(y)} f dx] dy` e o selo `REGIÃO DEITADA (TIPO II)`.
  - O cartão `FORA: NÚMEROS` / `DENTRO: SÓ A VARIÁVEL DE FORA`.
  - "atravessa a região": a reta-sonda branca tracejada atravessa a região (um `ValueTracker` de baixo para cima, parando em y ≈ 1,05). Ponto azul-claro `COMEÇA` e ponto coral `TERMINA`.
  - "dois pedaços separados": a miniatura da região em U, embaixo da coluna, com a reta cruzando dois trechos e a placa `DOIS TRECHOS?` em ALERTA.

### B3 · a cunha · alvos 09 a 12
- **B3-1 (alvos 09 → 10), cena1 3D → 2D.**
  - O quarto de disco no chão; "uma cunha": a cunha z = y sobe. Coluna: `f(x, y) = y` e `ALTURA = DENSIDADE (kg/m²)`.
  - "em xis igual a um": o plano âmbar (só borda) entra em x = 1; o corte abre e a face âmbar (triângulo) acende, com a placa `FATIA EM PÉ` e a placa `x = 1` no ponto `faca`. Coluna: `CORTE EM x = 1` e `A FATIA EM PÉ É UM TRIÂNGULO`.
  - "é um triângulo": pouso lateral (§2.2) e troca para o painel do alvo 10. Cotas `BASE` e `ALTURA`, cada uma com `√(4 − x²)` em coral; placa `x = 1` no canto do painel.
  - Coluna: `BASE · ALTURA / 2` (âmbar), glyph maps 4 e 5.
- **B3-2 (alvos 11 → 12).**
  - O painel lateral sai; volta a vista de cima do quarto de disco (2D, layout A) com a tira deitada magenta em y = 1. A coluna recebe o glyph map 6 ("ler a curva pelo outro eixo").
  - "olha a fatia": corte para a cena1 no ângulo do alvo 11; a faca deitada (borda magenta) entra em y = 1, a parte y < 1 desliza para a frente e para o lado, e a face magenta (retângulo) acende, com a placa `y = 1`. `A FATIA DEITADA É UM RETÂNGULO`.
  - "um retângulo": pouso lateral e troca para o painel do alvo 12: retângulo magenta de altura `y` e comprimento `√(4 − y²)`.
  - "Guarda essa diferença": o cartão `EM PÉ: ALTURA MUDA · TRIÂNGULO` (âmbar) / `DEITADA: ALTURA FIXA · RETÂNGULO` (magenta).
  - Glyph map 7 ("quase a derivada": o `4 − y²` e o `y` acendem juntos), com o ✓ menta em "oito terços de novo". No alvo o cartão usa `·`; se o Space Grotesk tiver a seta `→`, ela pode voltar (como no texto da proposta).

### B4 · a troca · alvos 13 a 17
- **B4-1 (alvo 13).**
  - A integral do hook volta a caneta na coluna. `PASSO 1: DESENHAR A REGIÃO` em menta.
  - Os limites voam da fórmula para o palco (§3.4): `0` e `1` para o eixo x, a reta `y = x` (azul-claro), a reta `y = 1` (coral). Os vértices `(0, 1)` e `(1, 1)` com pontos GEO pequenos.
  - "pintam um triângulo": as tiras em pé, uma a uma (5 tiras, `LaggedStart`), pintam o triângulo.
  - `∬ SÓ CONHECE REGIÃO E FUNÇÃO` (linha mista, o ∬ em MathTex).
- **B4-2 (alvos 14 → 15 → 16), cena2 3D → 2D.**
  - "reler o triângulo deitado": `PASSO 2: RELER DEITADO` e `0 ≤ y ≤ 1, 0 ≤ x ≤ y` na coluna; em "sai na diagonal", o limite `y` voa da diagonal do palco 2D (ainda o do alvo 13, agora com a tira deitada).
  - Corte para a cena2: o triângulo no chão; o sino z = e^(−y²) sobe. Coluna: `f(x, y) = e^(−y²)`.
  - "Em pé": a faca âmbar entra em x = 0,4, o corte abre, a face âmbar de teto curvo acende. "travava": a placa `SEM PRIMITIVA EM FÓRMULA` acima do sólido (alvo 14). Coluna: `FATIA EM PÉ: TETO CURVO` e `∫ₓ¹ e^(−y²) dy = ?` (o `?` em ALERTA).
  - "Deitada": a faca em pé sai e o sólido se fecha; a faca deitada magenta entra em y = 0,6, a parte da frente desliza, a face magenta (retângulo) acende (alvo 15; a coluna do alvo 15 repete o passo 2).
  - "um retângulo": pouso lateral e troca para o painel do alvo 16: retângulo de altura `e^(−y²)` (rótulo ciano no canto) e comprimento `y` (chave magenta embaixo, com `COMPRIMENTO DA FATIA`).
  - `PASSO 3: CALCULAR` e glyph map 8. Em "o comprimento da fatia", o `y` **voa da chave** para a integral; o sublinhado magenta fica sob ele por 2 s. "quase a derivada do expoente": o `y` e o `−y²` acendem juntos. "menos meio": a terceira linha. "Zero vírgula três um seis": o resultado.
- **B4-3 (alvo 17), layout E.**
  - A forma errada `∫₀¹ ∫ₓ¹ e^(−y²) dx dy` a caneta à esquerda; o `x` do limite e o `dx` acendem juntos em ALERTA. `SÓ TROCOU dx COM dy` (as letras `dx`/`dy` dessa legenda em MathTex, linha mista).
  - Glyph map 9; a placa `RESULTADO COM x?` com o ✗ em ALERTA.
  - "começa pela região": o cartão da direita com `∫₀¹ ∫₀^y e^(−y²) dx dy` e o ✓, o triângulo pequeno com a tira deitada, e `A REGIÃO ESCOLHE OS LIMITES` em menta.

### B5 · a chapa cortada na diagonal · alvos 18 e 19
- **B5-1 (alvo 18).**
  - A chapa x² + y² com o mapa ciano e `CHAPA INTEIRA: 32/3 kg` na coluna.
  - "na diagonal": a diagonal branca `y = x`; o triângulo de cima apaga (fica a 22 %).
  - A tira em pé em x = 1,2: entra em `y = 0` (azul-claro), sai na diagonal (`y = x`, coral). O `x` voa da diagonal para o limite de cima.
  - Glyph map 10.
- **B5-2 (alvo 19).**
  - A tira gira e vira a deitada (um movimento) em y = 0,8: entra na diagonal (`x = y`, agora **azul-claro**: a diagonal troca de cor junto com a tira) e sai em `x = 2` (coral). O `y` voa da diagonal para o limite de baixo.
  - Glyph map 11, com o ✓.
  - "um espelho": o triângulo de cima volta (tracejado) e se dobra sobre o de baixo pela diagonal (seta branca, um movimento). `f(x, y) = f(y, x)`, `ESPELHO NA DIAGONAL` e `16/3 + 16/3 = 32/3 kg`.

### B6 · seno de x³ · alvo 20
- **B6-1 (alvo 20).**
  - Coluna: `∫₀¹ ∫_{√y}¹ sen(x³) dx dy` a caneta; linha mista `sen(x³)` + `SEM PRIMITIVA EM FÓRMULA` (ALERTA).
  - Palco (triângulo unitário): primeiro a leitura deitada, pelos limites: `0` e `1` no eixo y (magenta), a curva `x = √y` (azul-claro, entrada) e a reta `x = 1` (coral, saída), com uma tira deitada.
  - Glyph map 12 (primeira parte): `x = √y ⇔ y = x²`. A curva troca de rótulo e de cor (vira a saída coral `y = x²` da tira em pé).
  - A tira deitada sai e a tira em pé entra em x = 0,72: entra em `y = 0` (azul-claro), sai em `y = x²` (coral).
  - "não depende de ípsilon": um painel lateral pequeno (não está no alvo; mesmo estilo do alvo 16, ≈ 40 % do tamanho, no canto inferior direito do palco) com o retângulo de altura `sen(x³)` e comprimento `x²`. Em "No sino", a miniatura do retângulo do sino (alvo 16, pequena) aparece ao lado por 2–3 s e sai. Em "trouxe xis ao quadrado", o `x²` voa desse comprimento para o fator `x²` da conta, e o `x²` e o `x³` acendem juntos.
  - Glyph map 12 (resto), com `(1 − cos 1)/3 ≈ 0,153`.

### B7 · quando a região se divide e quando trocar · alvos 21 a 23
- **B7-1a (alvo 21).**
  - O telhado (−1, 0), (0, 1), (1, 0), com as arestas coral.
  - "este telhado": o palco. "muda de fórmula no meio": a tira em pé desliza de x = −1 a 1 (um `ValueTracker`). À esquerda, o rótulo de saída é `y = 1 + x`; ao passar por x = 0, ele troca para `y = 1 − x`. Em "se divide em duas", a linha branca tracejada em x = 0 racha a região em `B₁` e `B₂` (os dois rótulos ficam).
  - Coluna: `EM PÉ: DUAS CONTAS` e a soma das duas iteradas `= 1/2 + 1/2`.
  - "Fatiando deitado": a tira deitada em y = 0,74: entra em `x = y − 1` (azul-claro), sai em `x = 1 − y` (coral). `DEITADO: UMA CONTA` (menta) e `∫₀¹ ∫_{y−1}^{1−y} dx dy = 1`.
- **B7-1b (alvo 22).**
  - Corte para a chapa de dois metais (a do EP. 08) com o metal leve aceso e o pesado apagado; a solda branca.
  - "zero, uma ou duas vezes": a reta deitada sobe (um `ValueTracker`), e as três faixas aparecem por gatilho: `CHEIA`, `1 CORTE`, `2 CORTES` (26 px), com as marcas `0,836`, `1,059` e `1,42` no eixo y e as tracejadas finas.
  - Coluna: `EM PÉ: UMA CONTA` com `∫₀² ∫₀^{g(x)} dy dx`; `DEITADO: TRÊS PEDAÇOS` com `1,6729 + 0,4097 + 0,3895`; `≈ 2,4721 m²` (menta) e `NAS DUAS ORDENS`.
  - Nada de arco-seno na tela.
- **B7-2 (alvo 23).** Cartão de três linhas a caneta, cada uma com a sua miniatura (o retângulo do sino, o telhado rachado, o triângulo da diagonal): `A DE DENTRO SEM PRIMITIVA` · `UMA ORDEM DIVIDE A REGIÃO` · `LIMITES MAIS SIMPLES`. Embaixo, `MESMA REGIÃO, MESMO VALOR` em menta.

### B8 · regiões gerais no mundo · alvo 24
- **B8 (alvo 24).** Três cartões, um por gatilho, em traço GEO, sem foto e sem efeito:
  - **ENCONTRO:** o quadrado dos horários, `ANA` no eixo x (âmbar) e `BIA` no eixo y (magenta, na horizontal, à esquerda do quadrado), a faixa em volta da diagonal pintada ("a faixa em volta da diagonal"); em "três pedaços", a faixa racha em três por duas verticais tracejadas finas (x = 1/4 e x = 3/4) e volta inteira; `7/16 ≈ 44 %`; `HORÁRIOS UNIFORMES` / `E INDEPENDENTES`.
  - **CURVA NORMAL:** o sino `e^(−x²)` em ciano.
  - **PEÇA RECORTADA:** chapa com a borda de cima curva (coral), `MASSA = ∬_B ρ dA` (linha mista).
  - As legendas dos cartões sobem para 26 px.

### S · síntese e próximo · alvos 25 e 26
- **S1 (alvo 25).**
  - A fórmula-tese `∬_B f = ∫_a^b ∫_{c(x)}^{d(x)} f dy dx = ∫_c^d ∫_{a(y)}^{b(y)} f dx dy` a caneta.
  - Os três ✓ entram nos gatilhos: `QUARTO DE DISCO: ÁREA π` (o π em MathTex logo depois do texto, sem o vão do alvo), `TRAVADA → (1 − 1/e)/2` e `TROCAR = RELER A REGIÃO`.
  - Miniaturas por gatilho, uma de cada vez no lado direito: "estende a função por zero" → o retângulo tracejado com o quarto de disco; "no máximo dois saltos" → o painel da fatia 0 | f | 0; "virar um retângulo" → o retângulo do sino (a do alvo, que fica).
- **S2 (alvo 26).**
  - "um desafio": a região entre a reta `y = x` e a parábola `y = 4x − x²` (0 ≤ x ≤ 3).
  - "Em pé, é uma conta só": uma tira em pé passa (entra na reta, sai na parábola) e sai. Não está no alvo.
  - "vira duas curvas": a tira deitada sobe (um `ValueTracker`); até y = 3 ela sai na reta (`x = y`, coral); ao passar de y = 3 (tracejado magenta), a saída troca para o ramo direito. Rótulos `x = 2 − √(4 − y)` (azul-claro) e `x = 2 + √(4 − y)` (coral). O alvo mostra as duas tiras, uma de cada faixa.
  - "no próximo vídeo": o cartão `NO PRÓXIMO VÍDEO:` / `EXERCÍCIOS DO MÓDULO` / `A PARÁBOLA VIRA DUAS CURVAS?` **fica ≥ 8 s** e não é atropelado.
  - O CTA padrão entra só em "deixa o like".

## 6. Narração (para o tempo do preview)

O preview é silencioso, mas cada âncora dura o tempo estimado da fala do Anexo A: 3 palavras/s, mais 0,15 s antes e 0,35 s depois de cada âncora. O total é ≈ **16:59**.

| Âncora | Palavras | Voz (s) | Início |
|---|---:|---:|---:|
| H1 | 212 | 71,2 | 0:00 |
| H2 | 67 | 22,8 | 1:11 |
| A1 | 61 | 20,8 | 1:34 |
| B1-1 | 182 | 61,2 | 1:54 |
| B1-2 | 173 | 58,2 | 2:56 |
| B1-3 | 125 | 42,2 | 3:54 |
| B2-1 | 158 | 53,2 | 4:36 |
| B2-2 | 158 | 53,2 | 5:29 |
| B3-1 | 141 | 47,5 | 6:22 |
| B3-2 | 168 | 56,5 | 7:10 |
| B4-1 | 115 | 38,8 | 8:06 |
| B4-2 | 173 | 58,2 | 8:45 |
| B4-3 | 134 | 45,2 | 9:43 |
| B5-1 | 127 | 42,8 | 10:29 |
| B5-2 | 129 | 43,5 | 11:11 |
| B6-1 | 188 | 63,2 | 11:55 |
| B7-1 | 182 | 61,2 | 12:58 |
| B7-2 | 127 | 42,8 | 13:59 |
| B8 | 162 | 54,5 | 14:42 |
| S1 | 125 | 42,2 | 15:37 |
| S2 | 120 | 40,5 | 16:19 |
| **Total** | **3027** | | **16:59** |

- Gere o `duracoes_estimadas.json` por âncora, como nas unidades anteriores, para a voz encaixar depois (WAV contínuo, cena segue a voz).
- Os gatilhos do §5 e do Anexo A são frases dessa narração. Marque o instante estimado de cada um pela contagem de palavras.
- As tags `[curious]`, `[serious]` etc. não contam palavras.
- **Não gerar voz.**

## 7. O que NÃO fazer

- Nada de `ThreeDScene`, `Surface` ou `Prism` do Manim: todo 3D é Three.js.
- Nenhuma partícula, brilho, sombra, névoa, contorno em seta, pulso automático ou transparência no 3D. O plano da faca é só borda.
- A câmera nunca se mexe durante a escrita de uma fórmula.
- Não escrever decimal sem `≈`, nem o decimal antes do exato.
- Não escrever que e^(−y²) ou sen(x³) "não têm primitiva": é `SEM PRIMITIVA EM FÓRMULA` (a primitiva existe; não é escrita com as funções do Cálculo I). Não citar Liouville nem erf na tela.
- Não mostrar a forma errada do B4-3 com um valor numérico: ela não tem valor, deixa um x solto.
- Não calcular o quarto de disco em coordenadas polares, nem escrever arco-seno no B7-1b.
- Não pôr frase portuguesa dentro de `MathTex`, nem `\tfrac`, nem `FadeIn` de linha pronta. Nenhum rótulo girado.
- Não citar livro, número de episódio nem o Atlas na tela. Não dizer "peso": é massa.
- Não mexer em `template/`, `assets/`, `docs/`, `AGENTS.md` nem nas outras unidades.
- Não gerar voz, SRT, master, 1080p nem entrega. Não fazer commit nem push.

## 8. QA do preview (obrigatório antes de entregar)

1. **Render × alvo:** um still em cada um dos 26 gatilhos, tirado quando o estado do alvo está completo e comparado na mesma resolução (alvo reduzido a 960×540, tolerância de 10 px nessa escala). Prancha `comparacao_v1.jpg`. Toda diferença que sobrar vai listada com o motivo.
2. **Alinhamento 3D × Manim** (`alinhamento3d_v1.txt`):
   - para cada quadro 3D, os rótulos contra os pontos do `pontos.json` do mesmo quadro (≤ 2 px);
   - para os três pousos (triângulo da cunha, retângulo da cunha, retângulo do sino), o contorno 2D contra o contorno da fatia no último PNG (≤ 2 px), dizendo qual saída de escala foi usada na cena 2 (§2.2).
3. **R5 · sobreposição** (`sobreposicoes_v1.txt`): caixas de `Text` e `MathTex` contra outros textos, linhas, arestas, setas, bordas de painel e chapa, rótulos dos eixos e arestas do 3D, amostradas **a cada 0,5 s, inclusive durante as animações** (em especial a tira que desliza no B1-1, a reta-sonda do B2-2 e a tira deitada do S2, que carregam placas). Esperado: zero.
4. **R6:** nada sai do painel ou do cartão; o 3D não invade a coluna.
5. **Flash por quadro = 0** (`flash_por_quadro_v1.txt`): nenhuma fórmula aparece inteira antes da caneta. Nada de `FadeIn`, `TransformFromCopy` ou `Write` dentro de `Succession(Wait…)`/`AnimationGroup` que ponha o destino na cena no instante 0.
6. **Glyph maps** (`glyph_maps_v1.txt`): os 12 do §3.4, com mapa → bloco → tempo, e nenhuma linha órfã com "=". `grep -n "from MF_Tools"` ≥ 1 e nenhuma função própria de mapa de glifos.
7. **Texto em MathTex** (`texto_em_mathtex_v1.txt`): liste todo `\text{…}` com mais de uma palavra. Esperado: zero. Inclua também `grep -n tfrac` = 0.
8. **Palco parado** (`palco_parado_v1.txt`): medido só no palco (§3.2). Nenhum trecho acima de 5 s; de 3 a 5 s, só com o motivo. Inclua o palco vazio (> 0,5 s: zero; o H1 abre com a integral no centro, e isso conta como palco ocupado) e o canto sem a linha 2 (zero).
9. **Cores de entrada e saída** (`origens_v1.txt`, seção própria): para cada tira de cada bloco, a curva por onde ela entra está em azul-claro e a por onde sai em coral, no mesmo quadro, inclusive depois das trocas (diagonal do B5-2, curva do B6-1, rótulo do telhado no B7-1a).
10. **Origens** (`origens_v1.txt`): para cada número e limite da tela do §4, de onde ele voa (objeto-fonte) ou qual mapa o produz. Os voos do §3.4 são obrigatórios.
11. **Cartão do próximo vídeo:** ≥ 8 s na tela, sem o CTA por cima.
12. **Tempo de render por bloco** em `tempos_render_v1.txt`, só para registro, com o custo por quadro do 3D. Se o pouso de alguma cena 3D atrasar o preview, a cena funciona em 2D (vista de cima + painel lateral): entregue assim e reporte.

## 9. Parada

Entregue o preview, a prancha, os relatórios e o relatório de entrega, incluindo as cenas Three.js, o que foi portado de `c3d34.html`, a resolução, o custo por quadro e o alinhamento medido. Pare. Não inicie voz nem 1080p.

---

## Anexo A · narração v2 por âncora (cópia de `narracao_v2.md`, com a Tela e os Gatilhos)

### H1 · uma integral que trava
**Tela:** `∫₀¹ ∫ₓ¹ e^(−y²) dy dx` a caneta no centro, com sublinhado de leitura; a primitiva tenta sair e para (`SEM PRIMITIVA EM FÓRMULA`); glyph map para `∫₀¹ ∫₀^y e^(−y²) dx dy`, com os limites que mudaram acendendo (`x` e `1` → `0` e `y`); a conta cai em `= (1 − 1/e)/2 ≈ 0,316` (o exato primeiro); em "os limites mudaram", os limites que mudaram acendem na fórmula; em "um triângulo", o triângulo aparece atrás da fórmula e os quatro limites acendem no desenho (`x` e `1` na tira em pé, `0` e `y` na deitada), na ordem da voz; corte para o quarto de disco com a tira em pé terminando na curva.
**Gatilhos:** "Olha esta integral"→caneta · "E aí trava"→placa · "com a ordem trocada"→glyph map · "zero vírgula três um seis"→resultado · "os limites mudaram"→limites acendem no desenho · "um triângulo"→o triângulo aparece atrás da fórmula · "não é um retângulo"→corte para o quarto de disco · "os limites novos"→a tira deitada no triângulo
> [curious] Olha esta integral: integral de zero a um, da integral de xis até um, de é elevado a menos ípsilon ao quadrado, dê ípsilon, dê xis. O é, aqui, é o número de Euler: dois vírgula setenta e um e pouco. Pela regra do vídeo passado, a gente começa por dentro: precisa de uma primitiva de é elevado a menos ípsilon ao quadrado. E aí trava. Essa primitiva existe, mas não se escreve com nenhuma combinação das funções do Cálculo um: nada de polinômio, seno, logaritmo, nada. A conta de dentro não sai, e a de fora nem começa. Agora, a mesma integral, com a ordem trocada: integral de zero a um, da integral de zero até ípsilon, dê xis, dê ípsilon. Em duas linhas, sai metade de um menos um sobre é: mais ou menos zero vírgula três um seis. E repara: os limites mudaram. O xis até um virou zero até ípsilon. A gente não trocou só o dê xis com o dê ípsilon: mudou o jeito de percorrer a região. Porque essa integral não mora num retângulo. Ela mora num triângulo. E aí entram duas perguntas: como fica o teorema de Fubini quando a região não é um retângulo? E como achar os limites novos sem mudar o valor?

### H2 · a ideia do vídeo
**Tela:** a tira em pé no quarto de disco, entrada azul-claro e saída coral; `LIMITES DE FORA: NÚMEROS` / `LIMITES DE DENTRO: CURVAS`; embaixo, `TROCAR A ORDEM = RELER A REGIÃO`.
**Gatilhos:** "no desenho"→a tira no quarto de disco · "começa numa curva"→ponto azul-claro · "termina em outra"→ponto coral · "números"→linha 1 · "passam a ser curvas"→linha 2 · "reler a mesma região"→linha 3
> [serious] A resposta está no desenho. Quando a região se deixa fatiar inteira, cada fatia começa numa curva e termina em outra. Então os limites de fora continuam sendo números, mas os de dentro passam a ser curvas, que dependem da variável de fora. E trocar a ordem não é só trocar o dê xis com o dê ípsilon: é reler a mesma região, fatiando no outro sentido.

### A1 · bem-vindos
**Tela:** logo; `REGIÕES GERAIS E TROCA DE ORDEM`; `NESTE VÍDEO: A FATIA NA CURVA · O TEOREMA · DUAS ORDENS · A TROCA · QUANDO VALE`.
**Gatilhos:** "Bem-vindos"→logo · "sai do retângulo"→título · "a fatia que termina numa curva"…"quando vale a pena trocar"→os cinco itens acendem um a um
> [happy] Fala, pessoal! Bem-vindos ao Parallax Lab! No vídeo passado, o teorema de Fubini transformou a integral dupla num retângulo em duas integrais do Cálculo um. Hoje ele sai do retângulo. A gente vai ver a fatia que termina numa curva, o teorema para regiões gerais, as duas ordens de fatiar, como trocar uma pela outra e quando vale a pena trocar.

### B1-1 · a fatia que termina na curva
**Tela:** D1. Palco: R = [0, 2]² tracejado, o quarto de disco B dentro (`B ⊂ R`), `0` apagado fora; faca em pé âmbar em x = 1; a fatia acende de y = 0 a y = √3 e fica apagada de √3 a 2, com `0`; coluna: `∫₀² F(1, y) dy = ∫₀^√3 f(1, y) dy`; a circunferência `x² + y² = 4` com `x = 1` dá `y = √3`; x desliza de 0 a quase 2; a saída ganha o rótulo coral `y = √(4 − x²)` e a entrada o azul-claro `y = 0`.
**Gatilhos:** "quarto de disco"→palco · "contido"→`B ⊂ R` · "valer zero fora"→`0` · "xis congelado em um"→faca · "só soma zeros"→trecho apagado · "raiz de três"→`y = √3` · "deixa o xis andar"→x desliza · "raiz de quatro menos xis ao quadrado"→rótulo coral · "ípsilon igual a zero"→rótulo azul-claro
> [thoughtful] Volta no quarto de disco de raio dois. Quando a gente construiu a integral dupla, apareceu um truque para regiões que não são retângulos: coloca a região B dentro de um retângulo R, lê-se B contido em R, e faz a função valer zero fora de B. Agora fatia em pé, com o xis congelado em um. A fatia atravessa o retângulo inteiro, de ípsilon zero até ípsilon dois. Só que, depois que sai do disco, ela só soma zeros. Então a integral da fatia é a mesma de zero até onde ela sai do disco. E onde ela sai? Na circunferência, xis ao quadrado mais ípsilon ao quadrado igual a quatro. Com xis igual a um, ípsilon é raiz de três. Agora deixa o xis andar. Em xis igual a zero, a fatia vai até dois; perto de xis igual a dois, ela quase some. O fim da fatia é a curva ípsilon igual a raiz de quatro menos xis ao quadrado, e o começo é a reta ípsilon igual a zero. A fatia começa numa curva e termina em outra.

### B1-2 · por que o Fubini ainda vale
**Tela:** D2. O retângulo com F; a fronteira de B acende fina em ALERTA (arco + dois segmentos) e ganha `CONTEÚDO NULO`; selo `F INTEGRÁVEL EM R`; painel pequeno embaixo: a fatia em x = 1 como gráfico de uma variável, `0`, `f`, `0`, com os dois saltos marcados; selo `FATIA INTEGRÁVEL`; a miniatura do enunciado do EP. 08 com `⇒`; a fórmula `∬_B f = ∫_a^b ∫_{c(x)}^{d(x)} f dy dx`; no fim, o disco dá lugar a uma região genérica entre duas curvas (a ponte para o B2).
**Gatilhos:** "duas coisas"→duas caixas vazias · "fechado e limitado"→borda de B · "fronteira de B"→fronteira acende · "conteúdo nulo"→rótulo · "integrável no retângulo"→selo 1 · "zero, depois f, depois zero"→painel da fatia · "dois saltos"→saltos marcados · "As duas hipóteses valem"→selo 2 · "garante"→miniatura e fórmula · "nada de especial do disco"→região genérica
> [serious] Mas será que o teorema do vídeo passado ainda vale aqui? Ele pedia duas coisas: a função integrável no retângulo e cada fatia com integral. Primeira: f é contínua em B, que é fechado e limitado, então f é limitada. E a função estendida, com zero fora, só pode ser descontínua na fronteira de B: o arco e os dois segmentos. Quando a gente estudou conteúdo nulo, viu que essas linhas têm conteúdo nulo. Então a estendida é integrável no retângulo. Segunda: cada fatia vale zero, depois f, depois zero de novo. São no máximo dois saltos, e uma função de uma variável com dois saltos tem integral, lá do Cálculo um. As duas hipóteses valem. Então o teorema de Fubini garante: a integral dupla em B é a integral de fora, da integral de dentro, com os limites de dentro nas curvas. E repara: esse argumento não usou nada de especial do disco. Vale para toda região entre os gráficos de duas funções contínuas, e é esse o enunciado que vem agora.

### B1-3 · a área pi
**Tela:** D3. f = 1: as fatias viram segmentos âmbar varrendo o disco (revelação da esquerda para a direita); coluna a caneta: `∬_B 1 dA = ∫₀² ∫₀^{√(4−x²)} 1 dy dx` → `= ∫₀² √(4 − x²) dx` (glyph map: a de dentro vira o comprimento) → `= π · 2²/4 = π`; a régua do EP. 05 com `3,25 · 3,17 · 3,15` e o ponto `π ≈ 3,1416`.
**Gatilhos:** "f igual a um"→coluna · "comprimento da fatia"→segmento acende · "dá a área"→varredura · "substituição trigonométrica"→segunda linha · "pi erre ao quadrado"→`π · 2²/4` · "três vírgula vinte e cinco"…"três vírgula quinze"→marcas na régua · "o valor exato"→ponto π
> [happy] Agora o caso mais simples: f igual a um. A integral de dentro, de zero até raiz de quatro menos xis ao quadrado, de um, dê ípsilon, é só o comprimento da fatia. E somar os comprimentos de todas as fatias dá a área. Fica a integral de zero a dois de raiz de quatro menos xis ao quadrado, dê xis: uma integral do Cálculo um, que a substituição trigonométrica resolve e que a geometria já conhece. Um quarto de pi erre ao quadrado, com raio dois, dá pi. Lembra das caixinhas? Com quatro divisões, três vírgula vinte e cinco; com dezesseis, três vírgula dezessete; com trinta e duas, três vírgula quinze. Elas estavam chegando em pi, três vírgula catorze. Fatiando, sai o valor exato.

### B2-1 · o enunciado: a região em pé
**Tela:** D4. Região genérica entre `y = c(x)` (azul-claro) e `y = d(x)` (coral), de `x = a` a `x = b` (âmbar); tira em pé com ponto de entrada e de saída; coluna a caneta, sublinhado no gatilho: `c, d CONTÍNUAS EM [a, b], c(x) ≤ d(x)` · `B = {(x, y) : a ≤ x ≤ b, c(x) ≤ y ≤ d(x)}` · `f CONTÍNUA EM B` · `⇒ ∬_B f dx dy = ∫_a^b [∫_{c(x)}^{d(x)} f(x, y) dy] dx`; selo pequeno `REGIÃO EM PÉ (TIPO I)`.
**Gatilhos:** "cê e dê"→curvas · "menor ou igual"→sublinhado em ≤ · "As chaves"→sublinhado em { } · "tais que"→sublinhado em `:` · "f é contínua em B"→linha 3 · "então"→⇒ · "entra na região"→ponto azul-claro · "sai pela curva de cima"→ponto coral · "tipo um"→selo
> [serious] Agora o enunciado, com o rigor do livro. Sejam cê e dê duas funções contínuas no intervalo fechado de á até bê, com cê de xis menor ou igual a dê de xis. A região B é o conjunto dos pontos xis, ípsilon tais que xis está entre á e bê, e ípsilon está entre cê de xis e dê de xis. As chaves se leem "o conjunto dos pontos", e os dois-pontos, "tais que". Se f é contínua em B, então a integral dupla de f sobre B é igual à integral de á até bê, da integral de cê de xis até dê de xis, de f de xis, ípsilon, dê ípsilon, dê xis. Na figura: a fatia em pé entra na região pela curva de baixo, cê de xis, e sai pela curva de cima, dê de xis. Essa é uma região que se fatia em pé; alguns livros chamam de região do tipo um.

### B2-2 · a região deitada e a regra dos limites
**Tela:** D5. A região genérica é trocada por uma deitada: `x = a(y)` (azul-claro, à esquerda), `x = b(y)` (coral, à direita), entre `y = c` e `y = d` (magenta); tira deitada; coluna: `B = {(x, y) : c ≤ y ≤ d, a(y) ≤ x ≤ b(y)}` · `∬_B f = ∫_c^d [∫_{a(y)}^{b(y)} f dx] dy`; selo `REGIÃO DEITADA (TIPO II)`; cartão `FORA: NÚMEROS` / `DENTRO: SÓ A VARIÁVEL DE FORA`; a reta-sonda atravessa a região: ponto azul-claro `COMEÇA`, ponto coral `TERMINA`; por último, num canto, uma região em forma de U com a reta cruzando dois trechos e a placa `DOIS TRECHOS?`.
**Gatilhos:** "Trocando os papéis"→região deitada · "da curva da esquerda até a da direita"→tira · "sempre números"→cartão linha 1 · "só da variável de fora"→linha 2 · "atravessa a região"→reta-sonda · "onde ela entra"→ponto azul-claro · "onde ela sai"→ponto coral · "dois pedaços separados"→região em U
> [thoughtful] Trocando os papéis, vem a região que se fatia deitada: ípsilon entre cê e dê, e xis entre á de ípsilon e bê de ípsilon. Aí a integral de dentro é em xis, da curva da esquerda até a da direita, e a de fora é em ípsilon. E daqui sai a regra que você vai usar em todo exercício. Os limites de fora são sempre números: eles dizem até onde as fatias vão. Os limites de dentro podem depender, mas só da variável de fora, porque é ela que está congelada na fatia. Para achar os limites de dentro, pega uma reta na direção da fatia e atravessa a região: onde ela entra, começa a integral; onde ela sai, termina. Na fatia em pé, de baixo para cima; na deitada, da esquerda para a direita. E, se essa reta encontrar dois pedaços separados da região, uma integral só não basta. Isso a gente resolve mais à frente.

### B3-1 · a cunha: a fatia em pé é um triângulo
**Tela:** D6. Three.js cena 1: quarto de disco no chão; a cunha z = y sobe (legenda `ALTURA = DENSIDADE (kg/m²)`); faca em pé âmbar em x = 1: a fatia triangular acende; pouso na vista lateral → 2D: triângulo âmbar com base e altura `√(4 − x²)`, `BASE · ALTURA / 2`; coluna: `∫₀^{√(4−x²)} y dy = y²/2 |₀^{√(4−x²)} = (4 − x²)/2` → `∫₀² (4 − x²)/2 dx = (8 − 8/3)/2 = 8/3`.
**Gatilhos:** "ípsilon quilos por metro quadrado"→legenda · "uma cunha"→a cunha sobe · "em xis igual a um"→faca · "é um triângulo"→pouso lateral · "ípsilon ao quadrado sobre dois"→linha 1 · "base vezes altura sobre dois"→rótulo · "oito terços de quilo"→resultado
> [curious] Agora uma chapa em forma de quarto de disco, mas com densidade que cresce com a altura: ípsilon quilos por metro quadrado. Desenhando a densidade como altura, aparece uma cunha. Fatia em pé, em xis igual a um. A fatia vai de zero até raiz de quatro menos xis ao quadrado, e a altura dela em cada ponto é o próprio ípsilon: ela é um triângulo. A integral de dentro, de zero até raiz de quatro menos xis ao quadrado, de ípsilon, dê ípsilon, dá ípsilon ao quadrado sobre dois, ou seja, quatro menos xis ao quadrado, sobre dois. E é exatamente a área do triângulo: base vezes altura sobre dois, com base e altura iguais a raiz de quatro menos xis ao quadrado. Somando as fatias, de zero a dois: oito menos oito terços, sobre dois. Oito terços de quilo.

### B3-2 · a fatia deitada é um retângulo
**Tela:** D7. Vista de cima (2D): tira deitada magenta em y = 1; coluna: `y = √(4 − x²)` → `y² = 4 − x²` → `x² = 4 − y²` → `x = √(4 − y²)` (glyph maps; placa `x ≥ 0`); a mesma cena Three.js com a faca deitada: a fatia é um **retângulo** de altura y e comprimento √(4 − y²); pouso lateral → 2D: `ALTURA × COMPRIMENTO`; coluna: `∫₀^{√(4−y²)} y dx = y√(4 − y²)` → `∫₀² y√(4 − y²) dy = [−(4 − y²)^{3/2}/3]₀² = 8/3 ✓`.
**Gatilhos:** "lida pelo outro eixo"→coluna · "Eleva ao quadrado"→glyph map 1 · "isola o xis"→glyph map 2 · "raiz positiva"→placa · "olha a fatia"→faca deitada · "um retângulo"→pouso · "altura vezes comprimento"→rótulo · "quase a derivada"→`4 − y²` e `y` acendem juntos · "oito terços de novo"→✓ · "Guarda essa diferença"→cartão `EM PÉ: ALTURA MUDA → TRIÂNGULO` / `DEITADA: ALTURA FIXA → RETÂNGULO` · "o fator que falta"→o comprimento acende
> [thoughtful] Agora deitado. Primeiro, um passo que vai aparecer em toda troca de ordem: a curva tem que ser lida pelo outro eixo. Ípsilon igual a raiz de quatro menos xis ao quadrado. Eleva ao quadrado, isola o xis e fica com a raiz positiva, porque aqui o xis é positivo: xis igual a raiz de quatro menos ípsilon ao quadrado. É a mesma circunferência, agora dizendo onde a fatia deitada sai. E olha a fatia: a altura é ípsilon em todo ponto dela, então ela é um retângulo. A integral de dentro, em xis, é altura vezes comprimento: ípsilon vezes raiz de quatro menos ípsilon ao quadrado. Essa tem primitiva fácil, porque o ípsilon que multiplica é quase a derivada do que está dentro da raiz. Resultado: oito terços de novo. Guarda essa diferença. Quando a fatia vai na direção em que a função não muda, a integral de dentro vira altura vezes comprimento. E esse comprimento pode ser exatamente o fator que falta na conta de fora.

### B4-1 · desenhar a região pelos limites
**Tela:** D8. A integral do hook volta à coluna; os limites voam para o palco: `0` e `1` no eixo x (âmbar), a reta `y = x` (azul-claro, entrada), a reta `y = 1` (coral, saída); tiras em pé, uma a uma, pintam o triângulo (0, 0), (0, 1), (1, 1); `PASSO 1: DESENHAR A REGIÃO`; legenda `∬ SÓ CONHECE REGIÃO E FUNÇÃO`.
**Gatilhos:** "a integral do começo"→fórmula · "desenhar a região"→passo 1 · "xis vai de zero a um"→`0` e `1` voam · "de xis até um"→as duas retas · "pintam um triângulo"→tiras · "zero zero, zero um e um um"→vértices · "não sabe nada de ordem"→legenda
> [serious] Agora sim, a integral do começo. Trocar a ordem tem um método, e o primeiro passo é desenhar a região a partir dos limites. Os limites de fora dizem: xis vai de zero a um. Os de dentro dizem: para cada xis, ípsilon vai de xis até um. Então a fatia em pé entra na reta ípsilon igual a xis, a diagonal, e sai na reta ípsilon igual a um. Com o xis andando de zero a um, essas fatias pintam um triângulo, com vértices em zero zero, zero um e um um. Esse triângulo é a região. E a integral dupla não sabe nada de ordem: ela só conhece a região e a função.

### B4-2 · reler deitado: o sino vira retângulo
**Tela:** D9. Three.js cena 2: o sino z = e^(−y²) sobre o triângulo; faca em pé âmbar: a fatia tem o teto curvo, placa `SEM PRIMITIVA EM FÓRMULA`; faca deitada magenta: a fatia é um **retângulo** de altura e^(−y²) e comprimento y; pouso lateral → 2D; `PASSO 2: RELER DEITADO`: `0 ≤ y ≤ 1, 0 ≤ x ≤ y`; `PASSO 3: CALCULAR`: `∫₀¹ ∫₀^y e^(−y²) dx dy` → `= ∫₀¹ y e^(−y²) dy`, com o `y` **voando do comprimento da fatia** no painel lateral para a integral e a chave `COMPRIMENTO DA FATIA` embaixo dele; depois o `y` e o `−y²` acendem juntos → `= [−e^(−y²)/2]₀¹` → `= (1 − 1/e)/2` (exato primeiro) → `≈ 0,316`.
**Gatilhos:** "reler o triângulo deitado"→passo 2 · "sai na diagonal"→limite `y` voa · "Em pé"→faca em pé · "travava"→placa · "Deitada"→faca deitada · "um retângulo"→pouso · "o comprimento da fatia"→`y` voa · "quase a derivada do expoente"→`y` e `−y²` acendem · "menos meio"→linha 3 · "Zero vírgula três um seis"→resultado
> [excited] Segundo passo: reler o triângulo deitado. Agora o ípsilon vai de zero a um, e, para cada ípsilon, a fatia entra no eixo, em xis igual a zero, e sai na diagonal, em xis igual a ípsilon. E olha a fatia na figura. Em pé, o teto dela é um pedaço do sino, curvo, e é por isso que a conta travava. Deitada, o é elevado a menos ípsilon ao quadrado não muda ao longo da fatia: o teto é reto, e a fatia é um retângulo. A integral de dentro é altura vezes comprimento: é elevado a menos ípsilon ao quadrado, vezes ípsilon, o comprimento da fatia. E esse ípsilon, que veio do desenho, é quase a derivada do expoente. Terceiro passo: a primitiva é menos meio de é elevado a menos ípsilon ao quadrado. De zero a um, dá metade de um menos um sobre é. Zero vírgula três um seis. A integral que travava virou uma conta de duas linhas, porque a gente mudou o jeito de percorrer a região.

### B4-3 · o erro clássico
**Tela:** D10. Coluna: a forma errada `∫₀¹ ∫ₓ¹ e^(−y²) dx dy` em ALERTA (só os diferenciais trocados); o `x` do limite e o `dx` acendem juntos; a conta formal deixa `(1 − x) · ∫₀¹ e^(−y²) dy` com o `x` em ALERTA; carimbo `RESULTADO COM x?`; volta a forma certa `∫₀¹ ∫₀^y e^(−y²) dx dy` com ✓ e o triângulo pequeno ao lado.
**Gatilhos:** "trocar só o dê ípsilon com o dê xis"→forma errada · "ao mesmo tempo"→`x` e `dx` acendem · "sobra um xis solto"→resultado com x · "não pode depender de xis"→carimbo · "só da variável de fora"→regra no rodapé · "começa pela região"→forma certa ✓ com o triângulo
> [serious] Cuidado com o erro mais comum nessa troca: trocar só o dê ípsilon com o dê xis e deixar os limites como estavam. Olha o que acontece. A integral de dentro passa a ser em xis, de xis até um. O xis seria, ao mesmo tempo, a variável que anda e o limite dela. Isso não tem sentido. E, se você fizer a conta mesmo assim, sobra um xis solto no resultado. Só que a integral dupla é um número: não pode depender de xis. É o mesmo aviso da regra: limite de dentro só pode depender da variável de fora. Por isso a troca certa começa pela região: primeiro redesenha o conjunto de pontos, depois acha os limites novos, e só então escreve a integral. A região manda; os limites só a descrevem.

### B5-1 · a chapa cortada na diagonal
**Tela:** D11. A chapa x² + y² (mapa ciano) com a régua `32/3 kg`; a diagonal branca `y = x`; o triângulo de cima apaga; tira em pé: entra em `y = 0`, sai na diagonal; o `x` voa da diagonal para o limite de cima; coluna: `∫₀ˣ (x² + y²) dy` → `= x² · x + x³/3` → `= 4x³/3` (glyph maps) → `∫₀² (4/3) x³ dx = (4/3) · 2⁴/4 = 16/3`.
**Gatilhos:** "trinta e dois terços"→régua · "na diagonal"→diagonal · "triângulo de baixo"→o de cima apaga · "Fatia em pé"→tira · "sai na diagonal"→`x` voa · "constante na fatia"→`x² · x` · "xis ao cubo sobre três"→`x³/3` · "quatro terços"→`4x³/3` · "dezesseis terços"→resultado
> [curious] Agora, para fixar o método, uma conta completa com a chapa de densidade xis ao quadrado mais ípsilon ao quadrado, aquela de trinta e dois terços de quilo. Corta a chapa na diagonal, ípsilon igual a xis, e fica com o triângulo de baixo. Quanto ele pesa? Fatia em pé: ela entra em ípsilon igual a zero e sai na diagonal, em ípsilon igual a xis. A integral de dentro vai de zero até xis, de xis ao quadrado mais ípsilon ao quadrado, dê ípsilon. O xis ao quadrado é constante na fatia e dá xis ao cubo; o ípsilon ao quadrado dá xis ao cubo sobre três. Somando, quatro terços de xis ao cubo. A de fora, de zero a dois, dá dezesseis terços de quilo.

### B5-2 · a outra ordem e o espelho
**Tela:** D12. Tira deitada magenta: entra na diagonal `x = y` (azul-claro), sai em `x = 2` (coral); o `y` voa da diagonal para o limite de baixo; coluna: `∫_y² (x² + y²) dx = 8/3 + 2y² − 4y³/3` → `∫₀² = 16/3 + 16/3 − 16/3 = 16/3 ✓`; depois o espelho: o triângulo de cima volta e se dobra sobre o de baixo pela diagonal, `f(x, y) = f(y, x)`, `16/3 + 16/3 = 32/3`.
**Gatilhos:** "congela o ípsilon"→tira deitada · "entra na diagonal"→`y` voa · "o limite de baixo mudou"→limite acende · "oito terços"→linha 1 · "dezesseis terços"→cada parcela · "Sobra dezesseis terços"→✓ · "um espelho"→a dobra · "trinta e dois terços"→soma
> [thoughtful] E deitado? Congela o ípsilon. Agora a fatia entra na diagonal, em xis igual a ípsilon, e sai na borda, em xis igual a dois. Repara que o limite de baixo mudou: antes era o zero, agora é a diagonal. A conta de dentro dá oito terços, mais dois ípsilon ao quadrado, menos quatro terços de ípsilon ao cubo. Integrando de zero a dois, cada parcela vale dezesseis terços, e uma delas entra com sinal de menos. Sobra dezesseis terços. Mesmo valor, como o teorema garante. E tem uma conferência que nem precisa de conta: se você trocar xis com ípsilon, a densidade não muda, e a diagonal funciona como um espelho. Os dois triângulos pesam igual. Dezesseis terços mais dezesseis terços: trinta e dois terços, a chapa inteira.

### B6-1 · seno de xis ao cubo
**Tela:** D13. Coluna: `∫₀¹ ∫_{√y}¹ sen(x³) dx dy`; placa `sen(x³): SEM PRIMITIVA EM FÓRMULA`; palco: `0` e `1` no eixo y (magenta), a curva `x = √y` (azul-claro, entrada) e a reta `x = 1` (coral, saída); glyph map `x = √y` → `y = x²`; a região embaixo da parábola; tira em pé: entra em `y = 0` (azul-claro), sai em `y = x²` (coral); painel lateral: retângulo de altura sen(x³) e comprimento x²; coluna: `∫₀¹ ∫₀^{x²} sen(x³) dy dx = ∫₀¹ x² sen(x³) dx = (1 − cos 1)/3 ≈ 0,153`.
**Gatilhos:** "raiz de ípsilon até um"→fórmula · "também não se escreve"→placa · "Desenha"→limites voam · "pelo outro eixo"→glyph map · "embaixo da parábola"→região · "fatia em pé"→tira · "não depende de ípsilon"→retângulo · "No sino"→miniatura do retângulo do sino · "trouxe xis ao quadrado"→`x²` voa do comprimento; `x²` e `x³` acendem · "um menos cosseno de um"→resultado
> [curious] Mais uma, agora com curva: integral de zero a um, da integral de raiz de ípsilon até um, de seno de xis ao cubo, dê xis, dê ípsilon. A primitiva de seno de xis ao cubo também não se escreve com as funções do Cálculo um. Então, o método. Desenha: ípsilon de zero a um, e cada fatia deitada entra na curva xis igual a raiz de ípsilon e sai em xis igual a um. Lendo essa curva pelo outro eixo, xis igual a raiz de ípsilon é a parábola ípsilon igual a xis ao quadrado. A região é o pedaço embaixo da parábola. Agora fatia em pé: ípsilon de zero até xis ao quadrado. Como seno de xis ao cubo não depende de ípsilon, a fatia é um retângulo, e a de dentro dá xis ao quadrado vezes seno de xis ao cubo. No sino, o comprimento da fatia trouxe o fator ípsilon; aqui, trouxe xis ao quadrado, que é quase a derivada de xis ao cubo. Mesmo raciocínio, outra curva. Resultado: um menos cosseno de um, sobre três. Mais ou menos zero vírgula um cinco três.

### B7-1 · quando a região se divide
**Tela:** D14. O telhado (−1, 0), (0, 1), (1, 0); tira em pé desliza: à esquerda sai em `y = 1 + x`, à direita em `y = 1 − x` (os dois rótulos em coral); em x = 0 a região racha em `B₁` e `B₂`; coluna: `∫_{−1}^0 ∫₀^{1+x} dy dx + ∫₀¹ ∫₀^{1−x} dy dx = 1/2 + 1/2`; tira deitada: entra em `x = y − 1`, sai em `x = 1 − y`; `∫₀¹ ∫_{y−1}^{1−y} dx dy = 1` (uma conta); corte para a chapa de dois metais com o metal leve: a reta deitada sobe, faixas `CHEIA · 1 CORTE · 2 CORTES`, marcas 0,836 · 1,059 · 1,42; `EM PÉ: UMA CONTA` / `DEITADO: TRÊS PEDAÇOS`; `2,4721 m²` nas duas.
**Gatilhos:** "este telhado"→palco · "muda de fórmula no meio"→os dois rótulos · "se divide em duas"→B₁ e B₂ · "meio mais meio"→coluna · "Fatiando deitado"→tira deitada · "Uma conta só"→fórmula única · "onde a mudança acontece"→x = 0 acende no telhado · "chapa de dois metais"→corte · "zero, uma ou duas vezes"→faixas · "dois vírgula quatro sete dois um"→área nas duas
> [thoughtful] Mas às vezes uma ordem obriga a dividir a região. Olha este telhado: o triângulo de vértices menos um zero, zero um e um zero. Fatiando em pé, a fatia sai pelo telhado, só que o telhado muda de fórmula no meio: à esquerda é ípsilon igual a um mais xis; à direita, um menos xis. Uma fórmula só não descreve a saída, então a região se divide em duas, bê um e bê dois, e a integral vira duas integrais somadas: meio mais meio, área um. Fatiando deitado, toda fatia entra pela esquerda, em xis igual a ípsilon menos um, e sai pela direita, em xis igual a um menos ípsilon. Uma conta só. A regra prática: se a fatia muda de comportamento no caminho, descobre onde a mudança acontece. É ali que a integral se divide. Na chapa de dois metais foi igual: o metal leve, fatiado em pé, era uma conta só. Deitado, a reta cortava a solda zero, uma ou duas vezes: três pedaços, com arco-seno, para a mesma área, dois vírgula quatro sete dois um metros quadrados.

### B7-2 · quando vale trocar
**Tela:** D15. Cartão de três linhas a caneta, cada uma com miniatura: `A DE DENTRO SEM PRIMITIVA` (sino) · `UMA ORDEM DIVIDE A REGIÃO` (telhado) · `LIMITES MAIS SIMPLES` (diagonal); embaixo, `MESMA REGIÃO, MESMO VALOR`.
**Gatilhos:** "Primeiro"→linha 1 · "não é garantia"→miniatura do retângulo · "Segundo"→linha 2 · "Terceiro"→linha 3 · "o valor não muda"→rodapé
> [serious] Então, quando vale a pena trocar a ordem? Primeiro, quando a integral de dentro não tem primitiva em fórmula, como o sino e o seno de xis ao cubo. Se a função depende de uma variável só, a fatia no sentido da outra vira um retângulo, e o comprimento dela entra como fator. Não é garantia de que a conta vai sair, mas é a primeira coisa a tentar. Segundo, quando uma ordem divide a região em pedaços e a outra não. Terceiro, quando os limites ficam mais simples. Em todos os casos, o valor não muda: a região é a mesma, a função é a mesma, e o teorema garante as duas ordens quando a função é contínua e a região se lê dos dois jeitos.

### B8 · regiões gerais no mundo
**Tela:** D16. Três cartões de traço GEO: (1) o quadrado dos horários, `HORÁRIO DE ANA` no eixo x e `HORÁRIO DE BIA` no eixo y (nomes genéricos), a faixa em volta da diagonal pintada, `HORÁRIOS UNIFORMES E INDEPENDENTES`, `7/16 ≈ 44%`; (2) o sino `e^(−x²)` com `CURVA NORMAL`; (3) uma peça de chapa recortada com borda curva e `MASSA = ∬_B ρ dA`.
**Gatilhos:** "probabilidade"→cartão 1 · "sem um depender do outro"→legenda · "a faixa em volta da diagonal"→faixa · "três pedaços"→faixa racha em três · "sete dezesseis avos"→`7/16` · "a curva normal"→cartão 2 · "peça recortada"→cartão 3
> [excited] E onde isso aparece? Na probabilidade, o tempo todo. Dois amigos combinam de se encontrar entre meio-dia e uma hora; cada um chega num horário sorteado por igual dentro dessa hora, sem um depender do outro, e espera só quinze minutos. Qual a chance de eles se encontrarem? Coloca o horário de um no eixo xis e o do outro no eixo ípsilon. "Eles se encontram" é a faixa em volta da diagonal, de um quarto de hora para cada lado. Fatiando em pé, a fatia entra e sai em retas que dependem do xis, e a faixa se divide em três pedaços. A área dá sete dezesseis avos: quase quarenta e quatro por cento. E aquele sino, é elevado a menos xis ao quadrado, tem o formato da curva normal da estatística: a curva mais usada da probabilidade não tem primitiva em fórmula. Na engenharia, a massa de uma peça recortada, com borda curva, é exatamente uma integral numa região geral.

### S1 · síntese
**Tela:** a fórmula-tese `∬_B f = ∫_a^b ∫_{c(x)}^{d(x)} f dy dx = ∫_c^d ∫_{a(y)}^{b(y)} f dx dy`; os três ✓: `QUARTO DE DISCO: ÁREA π` · `TRAVADA → (1 − 1/e)/2` · `TROCAR = RELER A REGIÃO`; miniatura do retângulo do sino.
**Gatilhos:** "estende a função por zero"→retângulo tracejado · "no máximo dois saltos"→miniatura da fatia · "entra numa curva e sai em outra"→fórmula-tese · "virar um retângulo"→miniatura do retângulo do sino · "deu pi"→✓ 1 · "um menos um sobre é"→✓ 2 · "reler a mesma região"→✓ 3
> [thoughtful] Então, juntando tudo. Nas regiões que se deixam fatiar entre duas curvas, o truque é o mesmo de sempre: estende a função por zero até um retângulo, e o teorema de Fubini continua valendo, porque a fronteira dessas regiões tem conteúdo nulo e cada fatia tem no máximo dois saltos. Na prática, a fatia entra numa curva e sai em outra. Os limites de fora são números; os de dentro dependem só da variável de fora. E, quando a ordem muda, uma fatia curva pode virar um retângulo e trazer exatamente o fator que faltava. Foi assim que o quarto de disco deu pi, e a integral que travava virou metade de um menos um sobre é. Trocar a ordem é reler a mesma região.

### S2 · o próximo vídeo e CTA
**Tela:** a região entre a reta `y = x` e a parábola `y = 4x − x²` (0 ≤ x ≤ 3); a tira em pé (uma conta); a tira deitada sobe e, ao passar de y = 3, a saída troca da reta para o ramo direito da parábola: rótulos `x = 2 − √(4 − y)` (azul-claro) e `x = 2 + √(4 − y)` (coral); cartão `NO PRÓXIMO VÍDEO: EXERCÍCIOS DO MÓDULO` e `A PARÁBOLA VIRA DUAS CURVAS?` (≥ 8 s); depois o CTA padrão.
**Gatilhos:** "um desafio"→região · "Em pé, é uma conta só"→tira em pé · "vira duas curvas"→os dois rótulos · "no próximo vídeo"→cartão · "deixa o like"→CTA
> [curious] E fica um desafio. Olha a região entre a reta ípsilon igual a xis e a parábola ípsilon igual a quatro xis menos xis ao quadrado. Em pé, é uma conta só. Mas, para fatiar deitado, a parábola tem que ser lida pelo eixo ípsilon, e aí ela vira duas curvas, uma de cada lado do topo. Como fica a troca? Isso, junto com volumes, massas e as duas ordens, é o que a gente resolve no próximo vídeo: os exercícios do módulo de cálculo de integrais duplas. [happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual integral você já viu travar numa ordem e sair na outra? Até a próxima!

---

## Anexo B · Como cada símbolo é lido na fala

| Símbolo | Como se lê | Âncora |
|---|---|---|
| ∫₀¹ ∫ₓ¹ e^(−y²) dy dx | "integral de zero a um, da integral de xis até um, de é elevado a menos ípsilon ao quadrado, dê ípsilon, dê xis" | H1 |
| e | "o número de Euler: dois vírgula setenta e um e pouco" (depois só "é") | H1 |
| (1 − 1/e)/2 | "metade de um menos um sobre é" | H1, B4-2 |
| B ⊂ R | "B contido em R" | B1-1 |
| √(4 − x²) | "raiz de quatro menos xis ao quadrado" | B1-1 |
| ∂B (sem símbolo na tela; só `FRONTEIRA`) | "a fronteira de B" | B1-2 |
| [a, b] | "o intervalo fechado de á até bê" | B2-1 |
| c(x) ≤ d(x) | "cê de xis menor ou igual a dê de xis" | B2-1 |
| { (x, y) : … } | "o conjunto dos pontos xis, ípsilon tais que…" (chaves = "o conjunto", dois-pontos = "tais que") | B2-1 |
| ∫_a^b ∫_{c(x)}^{d(x)} f dy dx | "integral de á até bê, da integral de cê de xis até dê de xis, de f de xis, ípsilon, dê ípsilon, dê xis" | B2-1 |
| ⇒ | "então" | B2-1 |
| a(y), b(y) | "á de ípsilon", "bê de ípsilon" | B2-2 |
| 4x³/3 | "quatro terços de xis ao cubo" | B5-1 |
| y√(4 − y²) | "ípsilon vezes raiz de quatro menos ípsilon ao quadrado" | B3-2 |
| sen(x³) | "seno de xis ao cubo" | B6-1 |
| (1 − cos 1)/3 | "um menos cosseno de um, sobre três" | B6-1 |
| B₁, B₂ | "bê um", "bê dois" | B7-1 |
| 7/16 | "sete dezesseis avos" | B8 |
| x = 2 ∓ √(4 − y) | (não lido; só os rótulos na tela) | S2 |
