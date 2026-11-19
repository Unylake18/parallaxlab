# yt_0037 · CÁLCULO III · EP. 12 · Coordenadas polares na integral dupla
## HANDOFF v1 para o Claude Code: preview visual do vídeo inteiro, com 3D em Three.js

Data: 2026-11-14. Formato: `longo_horizontal`.

Unidade nova: `videos_longos/yt_0037_coordenadas_polares/`. Antes de criar a pasta:
- confira que o número `yt_0037` está livre em `videos_longos/`;
- o EP. 10 é o `yt_0035`;
- o EP. 11 (jacobiano) deve ser o `yt_0036`.

Se `yt_0037` estiver ocupado, pare e reporte.

**Fase:** só o **preview visual silencioso** do vídeo inteiro, em 960×540 a 15 fps.
- O render não tem limite de tempo: o Kaio liberou render sem economia e 3D onde a câmera ajuda.
- Não gerar voz, SRT, master, 1080p nem entrega.
- Não fazer commit nem push.

Este handoff é autocontido. Tudo o que você precisa está nele e no zip `yt0037_handoff_v1_completo.zip`:
- `calculo3_34t2_quadros_alvo_v2/` traz os **9 quadros-alvo** (1920×1080), a `00_folha_contato_v2.jpg` e os geradores:
  - `c3d34t2.html` (Three.js r128, `?k=<chave>`) gera as **cenas 3D de referência** `sino` e `gauss`. Ele tem a geometria, as câmeras, as cores e a função `proj()`, que dá os pontos de tela em px. Ao lado estão os `r3d_<chave>.png` e os pontos em `r3d_pts.json`. A chave `esfera` também está lá, mas **não entra neste vídeo**. **Porte as duas cenas para a unidade** (§2.2): elas são o modelo exato.
  - `sb34t2.html` (Canvas + KaTeX, `?k=<chave>`) gera os quadros completos. Abra-o com as fontes, `logo_crop.png`, `katex/`, `three.min.js` e `r3d_pts.js` do lado.
    - Chaves deste vídeo, na ordem dos alvos 01 a 09: `h0 b1 b2 b2j b3 h1 b6 b7 s2`.
    - As chaves `b4` e `b5` do arquivo são de exemplos que saíram do vídeo: ignore.
  - `r3d.js` e `shot.js` são os scripts Playwright que geraram os PNGs. Servem só de referência.
- `yt_0037_narracao_v2.md` é a **narração aprovada**: 2.724 palavras ≈ 15:17, organizada por âncora, com a **Tela** e os **Gatilhos** de cada âncora e a tabela de leitura dos símbolos (Anexo B). É ela que dá os tempos e as frases de disparo.
- `verificacao/verifica_calc3_34t2_sympy.py` e a saída dele somam **50 checagens, todas `True`**. O script chama o raio de `R`; o vídeo usa `a`.
  - Este vídeo usa só estas checagens: H1, B1, B2, B3, B6 (só a área), B7 e S2.
  - As do meio disco com seno, da esfera, da distância média, da elipse e do cano são de exemplos que saíram.

A matemática, o roteiro, a narração e os textos estão aprovados pelo Kaio. Não rediscuta. Se encontrar uma inconsistência objetiva, reporte antes de mudar.

**Regras da série (Kaio):**
- **Figura:** toda definição ou enunciado formal aparece com a sua figura.
- **Origem:** todo símbolo nasce do desenho (`TransformFromCopy` do objeto para a fórmula) ou pela caneta. Nada aparece pronto.
- **CONTA INTEIRA** (regra permanente de 2026-11-14):
  - primitiva com colchete → F(b) − F(a) com os valores substituídos → número;
  - substituição com a linha `u = …, du = …` **e** a linha dos limites novos;
  - nenhum degrau pulado;
  - a voz lê cada degrau, e a tela escreve cada degrau no gatilho da voz.
- **"Sensacional" quer dizer clareza.** Nada de partícula, brilho, sombra, névoa, contorno em seta, luz que lava a cor ou câmera girando sem motivo.

**Lições dos EP. 06 a 10, já incorporadas aqui** (não as repita):
- MF-Tools de verdade, sem mapa de glifos próprio com `FadeIn`;
- nenhum bloco abrindo vazio;
- palco parado medido só no palco;
- R5 testado também durante as animações;
- frase portuguesa sempre em Space Grotesk, nunca dentro de `MathTex`;
- `\dfrac` sempre;
- cartão do próximo vídeo por ≥ 8 s;
- no 3D, a peça nunca se separa: o lado de fora do corte vira traço.

**A imagem-mãe deste vídeo:** **a célula polar lima**, o pedacinho entre dois círculos e dois raios. Ela aparece:
- no hook, com "?";
- nos dois painéis rθ ↔ xy;
- nos setores;
- no determinante;
- no teorema.

E a imagem que volta duas vezes é **a parede da casca** no sino 3D (H1 e B4-2).

---

## 0. O que entregar

1. A unidade nova, com:
   - `ficha.md` (§1);
   - `cena.py` e uma `sec_*.py` por bloco (H, A, B1 … B7, S);
   - `threejs/`, com as cenas 3D, o renderizador por quadro e os pedidos (§2.2).
2. O preview do vídeo inteiro, `renders/v1/yt_0037_preview_v1_540p15.mp4`, com a duração da narração (§6). Junto, `duracoes_estimadas.json`.
3. A prancha **render × alvo** `renders/v1/qa/comparacao_v1.jpg`, com uma linha por quadro-alvo: o still do render no gatilho ao lado do alvo, para os 9 alvos.
4. Os relatórios de QA em `renders/v1/qa/` (§8):
   - `sobreposicoes_v1.txt`
   - `alinhamento3d_v1.txt`
   - `flash_por_quadro_v1.txt`
   - `palco_parado_v1.txt`
   - `texto_em_mathtex_v1.txt`
   - `glyph_maps_v1.txt`
   - `origens_v1.txt`
   - `conta_inteira_v1.txt`
   - `tempos_render_v1.txt`
5. O relatório de entrega do AGENTS.md: arquivos, renders, QA e pendências.

## 1. Ficha

```
formato: longo_horizontal
tipo: teoria_visual
serie_publica: CÁLCULO III · EP. 12
titulo: Coordenadas polares na integral dupla
disciplina: Cálculo III
modulo: 3.4 Mudança de variáveis na integral dupla (o docs/mapa_curricular.md do repositório ainda usa a numeração antiga)
bloco: 3.4-T2
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §4.1 (polares) e §4.2 (teorema de mudança de variáveis; Ex. 5, integral de Gauss pelo confronto); Stewart §15.3 (setores, disco x² + y² ≤ 2x). Só na descrição do YouTube: nada de livro na tela nem na fala
unidades: x, y, r e a em metros; θ em radianos; áreas em m²
solido_3d: nenhum do arsenal Blender (o sino z = e^(−(x²+y²)) sobre o disco e sobre o quadrado, feito direto em Three.js como nos EP. 05 a 10)
3d_threejs: sino = z = e^(−(x²+y²)) sobre o disco unitário, com a casca em r = 0,55 (H1 só o sino; B4-1/B4-2 com a casca); gauss = o mesmo sino sobre o quadrado [−a, a]² com o disco inscrito e o circunscrito no chão (B6), com a câmera subindo até a vista de cima e a troca para o 2D
duracao_alvo: ≈ 15:17 (narração v2: 2.724 palavras)
```

## 2. Base de código

### 2.1 Manim

- **Antes de começar:**
  - leia `docs/estado_atual.md`;
  - rode `verificacao/verifica_calc3_34t2_sympy.py` com o Python da `.venv`. As 50 linhas devem dar `True`. Se faltar sympy ou scipy, não instale nada: diga no relatório e siga.
- **Copie, não importe.** Copie o kit da unidade mais recente da série de Cálculo III que estiver no seu checkout, nesta ordem: `yt_0036_*`, `yt_0035_*`, `yt_0034_*`, `yt_0033_*`. Do kit vêm:
  - `kit.py` e `render.sh`;
  - o canto de duas linhas e `placa_min`;
  - a caneta (`TC`/`TX`), `painel`, `mixl` e o sublinhado de leitura;
  - a reta-sonda com os pontos de entrada e saída (EP. 09).

  Não altere as outras unidades.
- **Fundo:**
  - Gráficos: violeta liso `#18143A → #0F0C26` na câmera, mais a grade `papel(ax)` de `assets/calculo/papel.py`, que nasce dos eixos de cada palco ou painel (quadradinho de 0,25 da unidade, sem linhas grossas).
    - **Nos palcos polares** (alvos 01, 03, 04, 05 e 07), a grade de quadradinhos fica **só fora do disco**, ou bem apagada, como nos alvos. A grade polar (círculos e raios GEO a ≈ 42 %) é desenhada por cima, dentro do disco.
    - Nos alvos 01 e 05 os discos estão sem `papel`: siga o alvo.
  - Cenas 3D: só o violeta liso, sem grade. O chão do 3D tem a grade polar da cena.
  - Cartões sem gráfico (A1, S1 à esquerda): só o violeta liso.
- Render por bloco (`render.sh <Classe>`), depois concatene.
- **Sem economia artificial**, mas sem updater à toa. Cada um destes é um `ValueTracker` só:
  - a célula que escorrega para fora no H1;
  - a deformação da grade no B1-2 (um `ApplyPointwiseFunction` com o parâmetro de interpolação);
  - o raio que gira no B3-2 e no B5;
  - o raio que varre o quadrado no B7;
  - o a que cresce na tabela do B6-2.
- Limpe da cena o que saiu da tela. Não deixe nada invisível acumulando.

### 2.2 Three.js (o pipeline da série)

- **Copie o pipeline** da unidade de Cálculo mais recente que tiver `threejs/` (yt_0035 ou yt_0034, se estiverem no checkout; senão `videos_longos/yt_0026_funcoes_vetoriais_campos/threejs/`). Vêm `r3d.js`, `package.json` (playwright-core), `cena3d/three.min.js` (r128) e o esquema de pedidos:
  1. a passagem seca do Manim grava `pedidos3d/<LOTE>.json`;
  2. `r3d.js` chama `window.setEstado(estado)` quadro a quadro e grava os PNGs com alfa e o `pontos.json`;
  3. o Manim cola os PNGs em tela cheia e prende os rótulos nos pontos.
- **Porte as cenas de `c3d34t2.html`** para `threejs/cena3d/`. Vêm de lá:
  - `sup(F, a0, a1, b0, b1, na, nb, cor)`: a superfície parametrizada, com a cor por altura (rampa escura → ciano) ou a cor forçada;
  - `tubo`, `anel`, `chaoDisco`, `gradePolar` e `eixos`;
  - `W3(X, Y, v)` (mundo = `SC` · metros; altura = `SC · ZS` · valor) e a câmera `ver(pos, alvo, cx, cy)` com `setViewOffset`.

  Valores:
  - `sino`: `SC = 2`, `ZS = 0,95`, `VMAX = 1`, casca em `r0 = 0,55`, câmera `ver([7.3, −6.6, 4.9], [0, .05, .55], 620, 600)`;
  - `gauss`: `SC = 1,15`, `ZS = 1,3`, quadrado de meia-aresta 1,25, disco inscrito de raio 1,25 (azul-claro `#7FB2FF`), circunscrito de raio 1,25·√2 (coral `#FF7A8A`), câmera `ver([7.9, −7.4, 5.2], [0, .1, .35], 620, 590)`.

  **Atenção:**
  - `c3d34t2.html` desenha só o estado final de cada chave. A animação entre os estados é sua.
  - Nos alvos 06 e 08, o PNG 3D foi colado em escala e com deslocamento: `sino` com `esc = 0,8` e `(dx, dy) = (−20, +150)`; `gauss` com `esc = 0,95` e `(dx, dy) = (−120, −10)`.
  - Reproduza o enquadramento do alvo ajustando `setViewOffset`/zoom, não redimensionando o PNG.
- **Estados por cena:**

  | cena | estados | o que anima |
  |---|---|---|
  | `sino` | `cresce` 0→1 · `casca` 0→1 · `parede` (acende a face) | **H1:** o disco no chão, o sino sobe (≈ 2 s), fica ~6 s e sai por corte para o 2D. Sem casca no H1. **B4-1:** o sino volta inteiro ao lado da coluna. **B4-2:** em "cada anel fino", entra o corte cilíndrico em r = 0,55. O miolo (r ≤ 0,55) fica opaco, com a cor por altura; o lado de fora vira **traço** `#6C7698` (anéis do teto em r = 0,7, 0,85 e 1, meridianos e geratrizes, como no alvo); a parede acende em laranja escurecido com as bordas laranja vivas. **A peça nunca se separa** |
  | `gauss` | `cresce` 0→1 · `discos` 0→1 · `sobe` 0→1 (câmera) | **B6-1:** o quadrado no chão; o sino sobe sobre ele. **B6-2:** em "entre dois discos", o inscrito (azul-claro) e o circunscrito (coral) se desenham no chão (traço, `discos` 0→1). Em "região maior", a câmera **sobe até a vista de cima** (≈ 2,5 s, começo e fim suaves). No fim, a projeção é ortográfica e o 2D do palco de cima (quadrado + dois discos) entra por cima no mesmo quadro, com alinhamento ≤ 2 px. A partir daí, a tabela e o a crescendo são 2D |

- **Parede da casca:** a cor é `mix(BG, #FF9440, 0,36 + 0,16·max(0, cos(θ + 0,75)))`, com as bordas de cima e de baixo em `#FF9440` vivo.
  - Motivo: o Kaio não quer áreas grandes de laranja ou âmbar vivo ao lado do ciano.
  - Não troque a cor do x (âmbar `#FFC24D`), que é da série.
- **Estilo 3D da série:**
  - opaco e sem luz (`MeshBasicMaterial`);
  - topo na cor por altura;
  - sem sombra, névoa, brilho ou transparência;
  - `outputEncoding` linear e antialias ligado.
- **Rótulos são do Manim**, presos aos pontos do `pontos.json` do mesmo quadro (≤ 2 px). Pontos já exportados:
  - `sino`: `parede`, `topoParede`, `peParede`, `centro`, `pico`, `borda`, `rRaio`, `ex`, `ey`, `ez`;
  - `gauss`: `pico`, `cin`, `ccirc`, `quina`, `ex`, `ey`, `ez`.
- **Câmera:**
  - no máximo um movimento por ideia;
  - **a câmera nunca se mexe enquanto uma fórmula está sendo escrita**;
  - nada de órbita;
  - nada do 3D passa da borda esquerda da coluna menos 30 px.

## 3. Sistema visual

### 3.1 Layouts e escala (px a 1080p; origem = onde fica (0, 0) do palco, u = px por unidade)

| alvo / bloco | geometria |
|---|---|
| 01 · H1 | Dois discos de raio 1: o esquerdo (grade quadrada) com origem em (520, 610) e o direito (grade polar 4 × 16) com origem em (1380, 610), u = 250. Seta entre eles de x = 830 a 1060. A integral no centro, em y ≈ 250 |
| 02 · B1-2 | Painel rθ com origem em (250, 930), r com u = 290, **θ = 2π ocupa 2 u** (θ/π em unidades). Painel xy com origem em (1330, 580), u = 290. Seta `φ(r, θ)` no meio. Miniatura do triângulo do B1-1 em (1690, 980), u = 120 |
| 03 · B2-1 | Quarto de plano com origem em (170, 980), u = 320. Coluna em x = 1100 |
| 04 · B2-2/B2-3 | Disco com origem em (470, 600), u = 250. Coluna em x = 1080 |
| 05 · B3-1 | Painel rθ com origem em (230, 700), u = 215, **θ = π ocupa 1 u**. Disco com origem em (1080, 480), u = 230. Legenda `CONTEÚDO NULO` em x = 1450. Enunciado embaixo, centrado em x = 960 (y ≈ 805–985) |
| 06 · B4-1 | 3D `sino` à esquerda. Coluna em x = 1030 |
| 07 · B5 | Disco deslocado com origem em (150, 650), u = 285. Coluna em x = 1000 |
| 08 · B6 | 3D `gauss` à esquerda; depois o palco de cima (2D). Coluna em x = 1000 |
| 09 · S2 | Meio disco com origem em (560, 700), u = 330. Cartão `NO PRÓXIMO VÍDEO` com moldura em (1120, 360), 680 × 260 |

Conversão para o Manim: x_m = (x_px − 960)/135; y_m = (540 − y_px)/135.

### 3.2 Regras (as da série)

- **R1 · Clareira:** nenhum rótulo sobre ponto, aresta, linha da grade ou número; o rótulo sai para o lado.
- **R2 · Placa:** todo rótulo solto sobre o desenho ou o 3D usa `placa_min`.
- **R3:** fórmula nova nunca nasce sobre fórmula velha; a coluna limpa antes.
- **R4:** rótulo junto do objeto que ele nomeia; o rótulo sai junto com o seu objeto.
- **R5:** QA automático de sobreposição, amostrado a cada 0,5 s, **inclusive durante as animações** (§8).
- **R6:** nada sai da moldura do seu painel ou cartão; o 3D não invade a coluna.
- **R-texto:**
  - **Palavra é Space Grotesk** (`Text`, maiúsculas); matemática é `MathTex`. Nenhuma frase portuguesa dentro de `MathTex`.
  - `ÁREA`, `CONFERE`, `TRAVA`, `SEM PRIMITIVA ELEMENTAR`, `CONTEÚDO NULO`, `METADE DE CIMA`, `NO INTERIOR: …` e `O MESMO NÚMERO DO SINO` são `Text`.
  - Linhas mistas são `Text` + `MathTex` lado a lado, com respiro ≥ 0,15 (`mixl()`).
  - Cada legenda tem no máximo 6 palavras e ≥ 26 px. As legendas de 20–24 px dos alvos sobem para 26 px. As exceções são a legenda longa do teorema (`NO INTERIOR: φ(INTERIOR) = INTERIOR · φ INJETORA · r ≠ 0`, que fica numa linha só, a 26 px) e `DISCO INTEIRO = METADE DE CIMA + METADE DE BAIXO`.
- **Fração:** sempre `\dfrac`, com o glifo ≥ 26 px. Os `\tfrac` dos alvos (`π/2`, `π/3` nos rótulos de ângulo) viram `\dfrac` ou a forma `\pi/2` em linha. `grep -n tfrac` = 0. Nenhum rótulo girado.
- **Glifos:**
  - zero em legenda vai por extenso (`ZERO`);
  - zero como valor é `MathTex`;
  - nos decimais, use `{,}`.
- **Sublinhado de leitura:** quando a voz lê um símbolo (Anexo B da narração), um sublinhado fino aparece sob ele no gatilho e sai. Não é pulso nem brilho.
- **Um movimento por ideia, uma vez.** Uma figura nova nasce da velha (`ReplacementTransform`) e nunca pisca.
- **Nenhum bloco abre vazio:**
  - a linha 2 do canto está na tela desde o primeiro quadro;
  - palco vazio por mais de 0,5 s: zero.
- **Palco parado:** menos de 40 px do palco mudando mais de 8 níveis em 3 s (a 960×540, sem a coluna e sem o canto).
  - Limite de 3 s.
  - De 3 a 5 s, só se a voz estiver lendo o que está no palco, com o motivo no relatório.
  - Acima de 5 s: zero.
- **Pontos só os do alvo:** entrada azul-claro, saída coral, a origem em ALERTA no alvo 05 e o ponto do exemplo (2, π/3) no B1-1. Nenhum ponto de debug.

### 3.3 Cores

| Papel | Cor |
|---|---|
| f, a superfície (cor por altura), valores de f, `e^(−…)`, `sen`, `√(x² + y²)` como função | ciano `#35D9FF` |
| x, `dx` | âmbar `#FFC24D` |
| y, `dy` | magenta `#EA63FF` |
| **r** (variável, círculos da grade, raio, `dr`, o r dentro da função) | laranja `#FF9440` |
| **θ** (variável, raios da grade, arcos de ângulo, `dθ`) | verde-água `#2EE6A6` |
| **o r do jacobiano**, a célula polar, `r̄` | lima `#C6F26B` |
| u da substituição, `du` | laranja escuro `#E08A3C` |
| Entrada / saída da reta-sonda; disco inscrito / circunscrito; metade de cima / de baixo (tons a 26–30 %) | azul-claro `#7FB2FF` / coral `#FF7A8A` |
| Resultado final, ✓, `√π`, `π(1 − 1/e)` | menta `#8CFFD2` |
| Erro clássico, `TRAVA`, `SEM PRIMITIVA ELEMENTAR`, bordas ruins, `CONTEÚDO NULO` | ALERTA `#FF5D5D` |
| Grade, réguas, molduras, legendas secundárias, região | GEO `#B8C4DA` |
| Traço do lado de fora do corte (3D) | `#6C7698` |

- Operadores (∫, ∬, ≤, ⇔, ⇒, [ ], ( )) ficam em branco, e a cor vai na grandeza.
- **Dois r diferentes na mesma linha:**
  - o r da função é laranja; quando ele é o **valor** de f, fica em ciano (`√(x² + y²) = r` como função);
  - o r que vem do jacobiano é **sempre lima**.

  Em `e^(−r²) · r dr dθ`, o `r²` do expoente é laranja e o `r` solto é lima.
- **Limite de dentro:** o limite inteiro na cor da curva (coral se é a saída: `2 cos θ` em coral), e só a variável dentro dele na cor dela (o θ em verde-água).

### 3.4 Álgebra

- **Caneta** em toda fórmula nova: traço finíssimo (~0,7), glifo a glifo, da esquerda para a direita, preenchendo na cor da grandeza, sem flash e sem preview do destino.
- **Voos obrigatórios** (`TransformFromCopy` em arco). No 3D, o voo parte do ponto projetado:
  - **H1:** nenhum voo (o hook só pergunta).
  - **B1-1:** o `2` voa do segmento r e o `π/3` voa do arco θ para o exemplo; o `1` e o `√3` voam das projeções nos eixos para o resultado.
  - **B2-1:** `r̄` do meio da célula, `Δr` da espessura e `Δθ` do arco da célula para a coluna; `3/4`, `1/2` e `π/6` da célula de dentro para a conta `π/16` (e o mesmo com `7/4` para `7π/48`).
  - **B2-2:** o `rΔθ` voa da chave do arco para `ÁREA ≈ r Δr Δθ`; cada entrada da matriz é escrita no gatilho da derivada falada.
  - **B3-1:** os limites `0`, `π`, `2π` voam do painel rθ para a linha `∫₀^π … + ∫_π^{2π} … = ∫₀^{2π} …`.
  - **B4-1:** o `1` e o `2π` voam do retângulo rθ (miniatura) para os limites; o `r` lima voa da célula da grade para o fator `· r`; o `(1 − 1/e)/2` final voa para a linha `∫₀^{2π} … dθ`.
  - **B4-2:** o `2πr` voa do anel (chave de comprimento no 3D) para a legenda.
  - **B5:** o `2 cos θ` voa da circunferência coral para o limite de cima de dentro; o `π/3 ⇒ r = 1` sai do ponto de saída da sonda.
  - **B6-2:** o `a` e o `a√2` voam dos dois discos (com a chave `MEIA DIAGONAL = a√2` no quadrado) para os dois lados da desigualdade.
  - **S1:** os três resultados voam das suas fontes (o chip `dA`, a coluna do B4, o `√π` do B6).
- **MF-Tools de verdade:**
  - `from MF_Tools import TransformByGlyphMap` (1.4.9), com `MathTex` de string única nos dois lados e mapa explícito;
  - o glifo que sai usa `auto_fade`;
  - o glifo que **entra** nunca usa `FadeIn`: fica fora do mapa e é escrito com a caneta, ou voa da fonte;
  - `show_indices` só no desenvolvimento.
- **Glyph maps obrigatórios (14):**
  1. B2-1: `½ r₂²Δθ − ½ r₁²Δθ` → `½(r₂² − r₁²)Δθ` (o ½ e o Δθ saem em evidência).
  2. B2-1: `½(r₂² − r₁²)Δθ` → `½(r₂ + r₁)(r₂ − r₁)Δθ` → `[(r₁ + r₂)/2] · (r₂ − r₁) · Δθ` → `r̄ Δr Δθ` (a metade da soma vira r̄ e a diferença vira Δr, cada uma com a chave no desenho).
  3. B2-2: `cos θ · r cos θ − (−r sen θ) · sen θ` → `r cos²θ + r sen²θ` → `r(cos²θ + sen²θ)` → `r` (o `cos²θ + sen²θ` acende e vira `1`, que some).
  4. B2-3 (errado): `∫₀^{2π}∫₀^a dr dθ` → `∫₀^{2π} a dθ` → `2πa` (✗ e `METRO`).
  5. B2-3 (certo): `∫₀^{2π}∫₀^a r dr dθ` → `∫₀^{2π}[r²/2]₀^a dθ` → `∫₀^{2π} a²/2 dθ` → `πa²` (✓ e `METRO²`).
  6. B4-1: `∬_D e^(−(x²+y²)) dA` → `∫₀^{2π}∫₀¹ e^(−r²) · r dr dθ` (o `x² + y²` vira `r²` e o `dA` vira `r dr dθ`, cada um vindo do chip `x² + y² = r²   dA = r dr dθ`).
  7. B4-1: `∫₀¹ e^(−r²) r dr` → `∫₀¹ e^(−u) du/2` (o `r²` vira `u` e o `r dr` vira `du/2`) → `[−e^(−u)/2]₀¹` → `−e^(−1)/2 − (−1/2)` → `(1 − 1/e)/2`.
  8. B4-1: `∫₀^{2π} (1 − 1/e)/2 dθ` → `2π · (1 − 1/e)/2` → `π(1 − 1/e)` (o 2 cancela: o `2` e o `/2` acendem juntos e saem).
  9. B5: `x² + y² ≤ 2x` → `x² − 2x + 1 + y² ≤ 1` (o `2x` **atravessa** e troca de sinal; o `+1` entra a caneta dos dois lados) → `(x − 1)² + y² ≤ 1`.
  10. B5: `r² ≤ 2r cos θ` → `r ≤ 2 cos θ` (um `r` de cada lado acende e sai, com a placa `(r > 0)`).
  11. B5: `∫∫ r dr dθ` → `∫[r²/2]₀^{2cos θ} dθ` → `∫ 2cos²θ dθ` → (com `2cos²θ = 1 + cos 2θ`) `[θ + sen 2θ/2]_{−π/2}^{π/2}` → `(π/2 + 0) − (−π/2 + 0)` → `π`.
  12. B6-1: `I(a) · I(a)` → `∫_{−a}^{a} e^(−y²)[∫_{−a}^{a} e^(−x²) dx] dy` → `∬_{Q_a} e^(−x²) e^(−y²) dA` → `∬_{Q_a} e^(−(x²+y²)) dA`. O colchete acende como `I(a)` antes de virar a integral dupla.
  13. B6-2: `2π[−e^(−r²)/2]₀^b` → `2π(−e^(−b²)/2 + 1/2)` → `π(1 − e^(−b²))`.
  14. B6-3: `∫ e^(−x²/2) dx` → `√2 ∫ e^(−u²) du` → `√2 · √π` → `√(2π)`.
- **Linhas de substituição e de limites** (CONTA INTEIRA): no B4-1 e no B6-3, as duas linhas `u = r² ⇒ du = 2r dr ⇒ r dr = du/2` e `r = 0 → u = 0,  r = 1 → u = 1` (ou `x = √2 u ⇒ dx = √2 du;  x: −∞ → ∞ ⇒ u: −∞ → ∞`) são escritas a caneta **antes** do glyph map que as usa, cada uma no seu gatilho.
- **Tamanhos:**
  - fórmula principal: 40–48 px;
  - secundária: 32–38 px;
  - índice ≥ 22 px;
  - nada menor que 26 px fora dos índices.
- **Arredondamento:** o exato vem antes do decimal, e o decimal sempre com `≈`: `(1 − 1/e)/2 ≈ 0,316`, `π(1 − 1/e) ≈ 1,986`, `π ≈ 3,1416`.
- **Coluna longa no B6:** a coluna se renova em duas telas:
  - tela 1: `I(a)` e `I(a)²` (glyph map 12);
  - tela 2: as inclusões, `∬_{D_b}`, a desigualdade, a tabela e o limite.

  A tela 1 sai (as linhas sobem e somem, sem `FadeOut` de tudo de uma vez) quando a câmera do `gauss` começa a subir.

## 4. Números (todos conferidos no script)

- **Exemplo do ponto:** (r, θ) = (2, π/3) ↦ (x, y) = (2 · ½, 2 · √3/2) = (1, √3).
- **Células** (Δr = ½, Δθ = π/6):
  - de dentro, r̄ = 3/4: `3/4 · 1/2 · π/6 = π/16 ≈ 0,196`;
  - de fora, r̄ = 7/4: `7π/48 ≈ 0,458`;
  - razão 7/3.

  Nos alvos 03 a célula de dentro fica entre r = 0,5 e 1 e a de fora entre 1,5 e 2.
- **Jacobiano:** `det = r`. **Erro:** sem o r sai `2πa`; com o r sai `πa²`.
- **Disco do começo:** `∫₀¹ e^(−r²) r dr = (1 − 1/e)/2 ≈ 0,316` (o mesmo número do sino do EP. 09); `∬ = π(1 − 1/e) ≈ 1,986`. É o volume debaixo do sino sobre o disco.
- **Disco deslocado:** `x² + y² ≤ 2x ⇔ (x − 1)² + y² ≤ 1 ⇔ r ≤ 2 cos θ`, com θ ∈ [−π/2, π/2]; em θ = π/3, r = 1; área `π`.
- **Gauss:**
  - `∬_{D_b} e^(−(x²+y²)) dA = π(1 − e^(−b²))`;
  - `π(1 − e^(−a²)) ≤ I(a)² ≤ π(1 − e^(−2a²))`;
  - tabela: a = 1 → `1,986 | 2,231 | 2,716`; a = 2 → `3,084 | 3,112 | 3,140`; a = 3 → `3,1412 | 3,1415 | 3,1416`;
  - resultado: `∫_{−∞}^{∞} e^(−x²) dx = √π`; normal: `√(2π)`.
- **Gancho:** o meio disco de raio a, com densidade proporcional à distância ao centro. **Nenhum número na tela**: a massa e o centro são do EP. 13.

## 5. Cena a cena

- **Gatilho** é a frase da narração (`yt_0037_narracao_v2.md`) em que a ação começa. Cada âncora tem a sua lista **Gatilhos**. Siga-a inteira; abaixo só vai o que ela não diz ou o que precisa de cuidado.
- **Alvo** é o quadro em `calculo3_34t2_quadros_alvo_v2/`, reproduzido com tolerância de ±20 px na posição e ±5 % no tamanho. Onde o alvo e este texto divergirem, vale o texto.
- **Canto:** a linha 1 é `CÁLCULO III · INTEGRAL DUPLA`, e a linha 2 é o título da cena que está no alvo.

### H · a integral que não colabora · alvo 01
- **H1:**
  - **"Lembra":** a cena `sino` (só o sino, sem casca) sobe sobre o disco unitário. Fica ~6 s e sai por corte.
  - **"O disco de raio um":** o palco do alvo 01. Primeiro só o disco esquerdo, com a grade de quadradinhos. A integral é escrita a caneta no centro, no alto.
  - **"Fatiando em pé":** a faca em pé (azul-claro) em x = 0,35, com a placa `TRAVA`; `e^(−y²) ?` + `SEM PRIMITIVA ELEMENTAR` (ALERTA, `Text`) no gatilho "não é elementar".
  - **"Deitado":** a faca deitada (coral) em y = −0,55 com `TRAVA`.
  - **"só depende de uma coisa":** `SÓ DEPENDE DA DISTÂNCIA ATÉ A ORIGEM` embaixo.
  - **"troca a grade":** a seta, e o disco direito nasce do esquerdo: a grade quadrada se curva em círculos e raios (um movimento).
  - **"Repara num detalhe":** uma célula lima perto da origem (entre r = 0,25 e 0,5, θ de π/8 a π/4) escorrega para fora (`ValueTracker`) e deixa a cópia; para entre r = 0,75 e 1, maior. `MESMO Δr, MESMO Δθ`.
- **H2:**
  - **"quanto vale":** os dois `?` nas células e a linha 2 do canto `QUAL É A ÁREA DE CADA PEDAÇO?` acende (sublinhado).
  - **"a área inteira debaixo da curva do sino":** o cartão pequeno `√π ?` entra no canto superior direito, abaixo do logo, e **fica** até o B6-2.
  - **O hook não mostra nenhuma resposta:** nem `r dr dθ` nem `π(1 − 1/e)`.

### A · bem-vindos
Padrão do canal:
- logo;
- `CÁLCULO DE INTEGRAL DUPLA · MUDANÇA DE VARIÁVEIS` (ciano, pequeno);
- título `COORDENADAS POLARES NA INTEGRAL DUPLA`;
- `NESTE VÍDEO`, com as cinco etiquetas `1 · A GRADE`, `2 · O FATOR r`, `3 · O TEOREMA`, `4 · DOIS DISCOS` e `5 · O SINO`, uma por palavra falada (26 px).

### B1 · coordenadas polares · alvo 02
- **B1-1** (não há alvo; layout A com o palco centrado, u ≈ 290):
  - o ponto P;
  - o segmento até a origem em laranja (`r`);
  - o arco verde-água (`θ`) a partir do semieixo x positivo, com a seta anti-horária;
  - o triângulo: cateto âmbar `x = r cos θ` e cateto magenta `y = r sen θ`;
  - na coluna: `x² + y² = r²` (glyph map pequeno: a soma dos quadrados dos catetos vira o `r²` da hipotenusa) e o exemplo (2, π/3) → (1, √3) com os voos do §3.4;
  - fecha com `r ≥ 0,   0 ≤ θ ≤ 2π`.

  O triângulo encolhe e vai para a miniatura do canto (1690, 980), onde fica no B1-2.
- **B1-2 (alvo 02):**
  - os dois painéis, com a seta `φ(r, θ) = (r cos θ, r sen θ)`;
  - **"Uma reta vertical":** uma vertical laranja do painel rθ vira círculo no xy (voo + transformação);
  - **"Uma reta horizontal":** uma horizontal verde-água vira raio;
  - **"o disco inteiro":** a grade inteira do retângulo deforma para o disco (`ApplyPointwiseFunction`, um movimento), e a célula lima é a mesma nos dois;
  - **"cai todo num ponto só":** a borda r = 0 (coral, grossa) encolhe até a origem;
  - **"no mesmo segmento":** as bordas θ = 0 e θ = 2π acendem juntas no eixo x.

### B2 · de onde vem o r · alvos 03 e 04
- **B2-1 (alvo 03):**
  - o quarto de plano com a grade polar (círculos em 0,5, 1, 1,5 e 2; raios a cada π/6);
  - **"Começa pelo setor":** o setor inteiro (r ≤ r₂) acende em lima a ≈ 18 %;
  - **"setor grande menos o setor pequeno":** o setor pequeno some dele (um movimento) e sobra a célula;
  - coluna C1 com os glyph maps 1 e 2;
  - **"pi sobre dezesseis":** a célula de dentro; **"sete pi sobre quarenta e oito":** a de fora; legenda `SETE TERÇOS` (26 px).
- **B2-2 (alvo 04, coluna de cima):**
  - a célula de fora ampliada (zoom do palco, um movimento): lado `Δr` laranja e arco `rΔθ` com chave;
  - `ÁREA ≈ r Δr Δθ`;
  - depois o determinante, com o glyph map 3;
  - o chip `dA = r dr dθ` (o r em lima);
  - a legenda `TRÊS CAMINHOS, O MESMO r`.
- **B2-3 (alvo 04, embaixo):** o disco de raio a; os glyph maps 4 (✗, `METRO: É O PERÍMETRO`, e o contorno do disco acende) e 5 (✓, `METRO²: É A ÁREA`, e o disco se pinta).

### B3 · o teorema e a receita · alvo 05
- **B3-1 (alvo 05):**
  - os dois painéis, agora com o retângulo [0, 1] × [0, 2π] **inteiro**;
  - o enunciado é escrito a caneta embaixo: primeiro `φ(r, θ) = …` (cê um), depois a legenda `NO INTERIOR: φ(INTERIOR) = INTERIOR · φ INJETORA · r ≠ 0`, cada item no seu gatilho ("três coisas"), e por fim a fórmula;
  - **"a primeira exigência falha":** a origem (ponto ALERTA) e o segmento da costura (θ = 0, tracejado ALERTA) acendem no disco;
  - **"cortar o disco em duas metades":** a linha θ = π (tracejada ALERTA) corta o retângulo rθ, e as duas metades se pintam (azul-claro a 30 % embaixo = `METADE DE CIMA`; coral a 26 % em cima = `METADE DE BAIXO`); o disco se pinta igual (`CIMA` / `BAIXO`);
  - **"conteúdo nulo":** `O CORTE E A ORIGEM: / CONTEÚDO NULO / NÃO SOMAM ÁREA`;
  - **"a soma":** `DISCO INTEIRO = METADE DE CIMA + METADE DE BAIXO` e a linha `∫₀^π … + ∫_π^{2π} … = ∫₀^{2π} …` (voos do §3.4).
- **B3-2** (sem alvo; layout A):
  - os selos `PASSO 1 · DESENHAR` … `PASSO 4 · CALCULAR` (menta);
  - uma região redonda genérica (um setor de anel), com o raio branco tracejado girando a partir da origem e os pontos azul-claro (entra) e coral (sai);
  - o cartão `θ FORA: NÚMEROS` / `r DENTRO: DA SONDA`;
  - a lista da troca `x → r cos θ · y → r sen θ · x² + y² → r² · dA → r dr dθ`, item por gatilho.

### B4 · o disco do começo · alvo 06
- **B4-1 (alvo 06):**
  - a cena `sino` volta sem casca, com o canto `O DISCO DO COMEÇO` / `PASSO 4 · CALCULAR`;
  - a miniatura do retângulo rθ [0, 1] × [0, 2π] entra no canto inferior esquerdo em "é um retângulo";
  - a coluna C4 inteira, linha a linha, com os glyph maps 6, 7 e 8 e as duas linhas de substituição;
  - **"o mesmo número do sino":** a legenda `O MESMO NÚMERO DO SINO` (`Text`, 26 px);
  - o resultado `π(1 − 1/e) ≈ 1,986` em menta.
- **B4-2:**
  - **"esse número tem cara":** a legenda `VOLUME ≈ 1,99` perto do `pico`;
  - **"cada anel fino":** entra o corte da casca (§2.2), a parede acende;
  - `PAREDE DA CASCA` e `2π r · e^(−r²)` presos em `parede`: o comprimento `2π r` (com o r em lima) voa do anel e a altura `e^(−r²)` (ciano) voa do `topoParede`.

### B5 · um disco fora do centro · alvo 07
- O disco de centro (1, 0) (coral), a origem azul-claro, `ENTRA NA ORIGEM`.
- A coluna C5: glyph maps 9 e 10, a linha `cos θ ≥ 0 ⇒ −π/2 ≤ θ ≤ π/2`.
- **"A reta-sonda":** o raio laranja sai da origem e gira de −π/2 a π/2 (`ValueTracker`), com o ponto de saída coral andando na circunferência. Para em θ = π/3, com a placa `θ = π/3 ⇒ r = 1`.
- **"não vira retângulo":** `A GRADE CERTA SIMPLIFICA A REGIÃO` (menta, `Text`) embaixo do palco, por ≥ 4 s.
- **"Confere com a área":** `ÁREA` (`Text`) e o glyph map 11, com o chip `CONFERE: π · 1²` ✓.

### B6 · a área inteira debaixo do sino · alvo 08
- **B6-1:**
  - a curva `e^(−x²)` em 2D, com a área de −a a a sombreada (ciano a 25 %) e a chave `I(a)`;
  - **"a primitiva existe, mas não é elementar":** `SEM PRIMITIVA ELEMENTAR` (ALERTA);
  - coluna tela 1 (§3.4) com o glyph map 12;
  - **"o sino girado":** corte para a cena `gauss`, e o sino sobe sobre o quadrado.
- **B6-2 (alvo 08):**
  - **"entre dois discos":** os discos se desenham no chão (azul-claro `D_a`, coral `D_{a√2}`, rótulos presos em `cin` e `ccirc`);
  - **"meia diagonal":** a chave `MEIA DIAGONAL = a√2` na diagonal do quadrado;
  - **"região maior":** a câmera sobe até a vista de cima e troca para o 2D (§2.2); a coluna tela 2;
  - glyph map 13 e a desigualdade com os voos de `a` e `a√2`;
  - a tabela: a cada "á igual a um / dois / três", o a cresce (`ValueTracker`, os dois discos e o quadrado crescem juntos no palco 2D, que reescala) e a linha da tabela é escrita;
  - o limite e `√π` com moldura menta;
  - o cartão `√π ?` do canto ganha ✓ e sai.
- **B6-3:**
  - a curva `e^(−x²/2)` (2D, a mesma moldura da B6-1);
  - as linhas de substituição e o glyph map 14;
  - `1/√(2π)` na frente da fórmula da normal;
  - a área vira `1 = 100 %`.

### B7 · quando usar polares
- O quadrado [0, 1]² (layout A); o raio branco varre de 0 a π/2 (`ValueTracker`), com o ponto de saída coral.
- Até π/4 a saída fica no lado x = 1, com o rótulo `r = sec θ`; depois de π/4 passa para o lado y = 1, com o rótulo `r = cossec θ`. A troca de rótulo é um movimento só, e a linha θ = π/4 fica tracejada ALERTA.
- A placa `DUAS INTEGRAIS` (ALERTA).
- **"Polar vale a pena":** o cartão `POLARES: REGIÃO REDONDA · x² + y²` (mista).
- Não escrever a conta de ∬xy (ela não está na narração).

### S · síntese e próximo · alvo 09
- **S1:**
  - os dois painéis em miniatura à direita;
  - os três ✓ à esquerda, cada um num gatilho: `dA = r dr dθ` · `DISCO: π(1 − 1/e)` · `SINO INTEIRO: √π`, com os voos do §3.4;
  - em "a grade certa simplifica a região", o retângulo rθ da miniatura acende (sublinhado, não brilho).
- **S2 (alvo 09):**
  - o meio disco de raio a com o tom crescendo para a borda;
  - `MAIS PESADO NA BORDA`, o lápis embaixo, o `?` e `ONDE ELE EQUILIBRA?`;
  - **"no próximo vídeo":** o cartão `NO PRÓXIMO VÍDEO: / MASSA E / CENTRO DE MASSA` **fica ≥ 8 s** e não é atropelado;
  - o CTA padrão entra só em "deixa o like".

## 6. Narração (para o tempo do preview)

O preview é silencioso, mas cada âncora dura o tempo estimado da fala: 3 palavras/s, mais 0,15 s antes e 0,35 s depois de cada âncora. O total é ≈ **15:17**.

| Âncora | Palavras | Voz (s) | Início |
|---|---:|---:|---:|
| H1 | 120 | 40,0 | 0:00 |
| H2 | 47 | 15,7 | 0:40 |
| A1 | 36 | 12,0 | 0:56 |
| B1-1 | 163 | 54,3 | 1:09 |
| B1-2 | 137 | 45,7 | 2:04 |
| B2-1 | 232 | 77,3 | 2:50 |
| B2-2 | 168 | 56,0 | 4:08 |
| B2-3 | 93 | 31,0 | 5:04 |
| B3-1 | 219 | 73,0 | 5:36 |
| B3-2 | 114 | 38,0 | 6:49 |
| B4-1 | 220 | 73,3 | 7:28 |
| B4-2 | 87 | 29,0 | 8:41 |
| B5 | 286 | 95,3 | 9:11 |
| B6-1 | 175 | 58,3 | 10:47 |
| B6-2 | 232 | 77,3 | 11:46 |
| B6-3 | 88 | 29,3 | 13:03 |
| B7 | 99 | 33,0 | 13:33 |
| S1 | 111 | 37,0 | 14:07 |
| S2 | 97 | 32,3 | 14:44 |
| **Total** | **2724** | | **15:17** |

- Gere o `duracoes_estimadas.json` por âncora, para a voz encaixar depois (WAV contínuo, a cena segue a voz).
- Marque o instante estimado de cada gatilho pela contagem de palavras.
- As tags `[curious]`, `[serious]` etc. não contam palavras.
- **Não gerar voz.**

## 7. O que NÃO fazer

- **3D:**
  - nada de `ThreeDScene`, `Surface` ou `Prism` do Manim: todo 3D é Three.js;
  - nenhuma partícula, brilho, sombra, névoa, pulso automático ou transparência;
  - a peça 3D nunca se separa;
  - a câmera nunca se mexe durante a escrita de uma fórmula.
- **Conteúdo do hook:** não mostrar `r dr dθ` nem o resultado do disco no H1 ou no H2. O hook só pergunta.
- **Frases proibidas:**
  - não escrever `REGIÃO REDONDA VIRA RETÂNGULO`: a frase é `A GRADE CERTA SIMPLIFICA A REGIÃO`;
  - não escrever que e^(−x²) "não tem primitiva": é `SEM PRIMITIVA ELEMENTAR`;
  - não citar erf nem Liouville;
  - não chamar a chapa do gancho de "meia-lua": é **meio disco**.
- **Exemplos que saíram:** não incluir nenhum. Ficam de fora o meio disco com sen(x² + y²), a esfera, a distância média, a elipse e o cano, mesmo que estejam no `sb34t2.html` (chaves `b4`, `b5`) ou no script sympy.
- **Escrita:**
  - não escrever decimal sem `≈`, nem o decimal antes do exato;
  - nada de frase portuguesa dentro de `MathTex`, `\tfrac`, `FadeIn` de linha pronta nem rótulo girado.
- **Referências:** não citar livro, número de episódio nem o Atlas na tela.
- **Arquivos:** não mexer em `template/`, `assets/`, `docs/`, `AGENTS.md` nem nas outras unidades.
- **Fase:** não gerar voz, SRT, master, 1080p nem entrega. Não fazer commit nem push.

## 8. QA do preview (obrigatório antes de entregar)

1. **Render × alvo:** um still em cada um dos 9 gatilhos, comparado na mesma resolução (alvo reduzido a 960×540, tolerância de 10 px). Gere a prancha `comparacao_v1.jpg` e liste toda diferença que sobrar, com o motivo.
2. **Alinhamento 3D × Manim** (`alinhamento3d_v1.txt`):
   - os rótulos contra os pontos do `pontos.json` do mesmo quadro (≤ 2 px);
   - a troca 3D → 2D do `gauss`: os dois discos e o quadrado do 2D contra os do último PNG (≤ 2 px).
3. **R5 · sobreposição** (`sobreposicoes_v1.txt`), amostrada a cada 0,5 s, inclusive durante as animações. Atenção especial a:
   - a célula que escorrega no H1;
   - a grade que deforma no B1-2;
   - o raio que gira no B3-2, no B5 e no B7;
   - a tabela do B6-2.

   Esperado: zero.
4. **R6:** nada sai do painel ou do cartão; o 3D não invade a coluna.
5. **Flash por quadro = 0** (`flash_por_quadro_v1.txt`).
6. **Glyph maps** (`glyph_maps_v1.txt`): os 14 do §3.4, com o mapa, o bloco e o tempo de cada um, e nenhuma linha órfã com "=". `grep -n "from MF_Tools"` ≥ 1.
7. **Conta inteira** (`conta_inteira_v1.txt`): para cada conta (B2-1, B2-2, B2-3, B4-1, B5, B6-2, B6-3), a lista de degraus com o tempo em que cada um é escrito. Nenhum degrau pode faltar em relação ao §3.4 e à narração. Em especial:
   - a linha dos limites novos da substituição no B4-1;
   - o `F(b) − F(a)` com os valores (`−e^(−1)/2 − (−1/2)`, `(π/2 + 0) − (−π/2 + 0)`, `2π(−e^(−b²)/2 + 1/2)`).
8. **Texto em MathTex** (`texto_em_mathtex_v1.txt`): zero `\text{…}` com mais de uma palavra; `grep -n tfrac` = 0.
9. **Palco parado** (`palco_parado_v1.txt`), medido só no palco: nenhum trecho acima de 5 s; de 3 a 5 s, só com o motivo. Inclua palco vazio (zero) e canto sem a linha 2 (zero).
10. **Cores** (`origens_v1.txt`, seção própria):
    - o r do jacobiano é lima em toda linha em que aparece;
    - o r da função (no expoente, dentro do seno ou da raiz) é laranja;
    - a entrada da sonda é azul-claro e a saída coral, no mesmo quadro.
11. **Origens** (`origens_v1.txt`): para cada número e limite da tela do §4, de onde ele voa ou qual mapa o produz. Os voos do §3.4 são obrigatórios.
12. **Cartão do próximo vídeo:** ≥ 8 s na tela, sem o CTA por cima.
13. **Tempo de render por bloco** (`tempos_render_v1.txt`), com o custo por quadro do 3D. Se a subida de câmera do `gauss` atrasar o preview, faça a vista de cima direto em 2D (corte seco), entregue assim e reporte.

## 9. Parada

Entregue o preview, a prancha, os relatórios e o relatório de entrega, incluindo:
- as cenas Three.js e o que foi portado de `c3d34t2.html`;
- a resolução e o custo por quadro;
- o alinhamento medido.

Pare. Não inicie voz nem 1080p.
