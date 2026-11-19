# yt_0032 · CÁLCULO III · EP. 07 · Propriedades da integral dupla
## HANDOFF v1 (para o Claude Code): preview visual do vídeo inteiro, com 3D em Three.js

Data: 2026-11-12. Formato: `longo_horizontal`. Unidade nova: `videos_longos/yt_0032_propriedades_integral_dupla/`.

**Fase:** só o **preview visual silencioso** do vídeo inteiro, em 960×540 a 15 fps (padrão do AGENTS.md para iterar). O render não tem limite de tempo: o Kaio liberou render sem economia e 3D onde a câmera ajuda. Não gerar voz, SRT, master, 1080p nem entrega. Não fazer commit nem push.

Este handoff é autocontido. Tudo o que você precisa está nele e no zip `yt0032_handoff_v1_completo.zip`:
- `yt_0032_quadros_alvo_v1/`: os **26 quadros-alvo** (1920×1080), a `00_folha_contato_v1.jpg` e os geradores:
  - `c3d32.html` (Three.js r128, `?k=<chave>`) gera as **7 cenas 3D de referência** (`b12`, `b14`, `b21`, `b22`, `b31`, `b32`, `b61`), com a geometria, as câmeras, as cores e a função `proj()` que dá os pontos de tela em px. As imagens `r3d_<chave>.png` e os pontos `r3d_pts.json` estão ao lado. **Porte essas cenas para a unidade** (§2.2): elas são o modelo exato, não uma inspiração.
  - `sb32.html` (Canvas + KaTeX, `?k=<chave>`) gera os quadros completos. Abra com as fontes, `logo_crop.png`, `katex/`, `three.min.js` e `r3d_pts.js` do lado.
- `narracao_v3.md` (= `yt_0032_narracao_v3_enxuta.md`): a **narração fechada** (3.160 palavras ≈ 17:46), por âncora, com a tela de cada âncora. É ela que dá os gatilhos e os tempos.
- `verificacao/verifica_calc3_32t3_sympy.py` e a saída dele: **19 checagens, todas `True`**. Todos os números da tela saem dali.

A matemática, o roteiro, a narração e os textos estão aprovados pelo Kaio. Não rediscuta. Se encontrar uma inconsistência objetiva, reporte antes de mudar.

**Regras da série (Kaio):**
- Toda definição ou enunciado formal aparece com a sua figura, e **todo símbolo nasce do desenho**: `TransformFromCopy` do objeto para a fórmula, ou caneta. Nada aparece pronto.
- Álgebra passo a passo: a fórmula-mãe vem antes do número, cada valor voa da fonte, cada passo é um `TransformByGlyphMap` com mapa explícito, e não pode haver linha órfã começando por "=".
- "Sensacional" quer dizer clareza. Nada de partícula, brilho, sombra, névoa, contorno em seta, luz que lava a cor ou câmera girando sem motivo.

---

## 0. O que entregar

1. A unidade nova, com:
   - `ficha.md` (§1);
   - `cena.py` e uma seção `sec_*.py` por bloco (H, A, B1 … B7, S);
   - `threejs/` com as cenas 3D, o renderizador por quadro e os pedidos (§2.2).
2. O preview do vídeo inteiro, `renders/v1/yt_0032_preview_v1_540p15.mp4`. A duração segue a narração (§6).
3. A prancha **render × alvo** `renders/v1/qa/comparacao_v1.jpg`, com uma linha por quadro-alvo: o still do render no gatilho ao lado do alvo, para os 26 alvos.
4. Os relatórios de QA em `renders/v1/qa/`:
   - `sobreposicoes_v1.txt` (R5, zero esperado);
   - `alinhamento3d_v1.txt` (rótulos do Manim × pontos do Three.js, ≤ 2 px);
   - `flash_por_quadro_v1.txt` (zero eventos);
   - `tempos_render_v1.txt` (tempo por bloco, só para registro).
5. O relatório de entrega do AGENTS.md: arquivos, renders, QA e pendências.

## 1. Ficha

```
formato: longo_horizontal
tipo: teoria_visual
serie_publica: CÁLCULO III · EP. 07
titulo: Propriedades da integral dupla
disciplina: Cálculo III
modulo: 3.2 Integrais duplas (o docs/mapa_curricular.md do repositório ainda usa a numeração antiga)
bloco: 3.2-T3
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §2.5 (só na descrição do YouTube; nada de livro na tela nem na fala)
unidades: x e y em metros; densidade em kg/m²; massa em kg
solido_3d: nenhum do arsenal Blender (caixas, muro e superfície feitos direto em Three.js, como nos EP. 05 e 06)
3d_threejs: b12 (rampas x² + y² empilhadas), b14 (camadas da chapa de dois metais), b21 (f dentro de g), b22 (chapa entre as lajes 1 e 3), b31 (muro na solda, altura M), b32 (muro de 100, n = 64), b61 (terraplanagem até 8/3)
duracao_alvo: ≈ 18 min (narração v3: 3.160 palavras ≈ 17:46)
```

## 2. Base de código

### 2.1 Manim

- **Antes de começar:**
  - leia `docs/estado_atual.md`;
  - rode `verificacao/verifica_calc3_32t3_sympy.py` com o Python da `.venv`; as 19 linhas devem dar `True`. Se faltar sympy, não instale nada: diga no relatório e siga.
- **Copie, não importe.** Copie o kit da unidade mais recente da série de Cálculo que estiver no seu checkout, nesta ordem de preferência:
  1. `videos_longos/yt_0031_*`;
  2. `videos_longos/yt_0029_*`;
  3. `videos_longos/yt_0028_*`.

  Do kit vêm `kit.py`, `render.sh`, o canto de duas linhas, `placa_min`, a caneta (`TC`/`TX`), `painel` e o sublinhado de leitura no gatilho falado. Não altere as outras unidades.
- **Fundo:** violeta liso `#18143A → #0F0C26` na câmera, mais a grade `papel(ax)` de `assets/calculo/papel.py`, que nasce dos eixos (quadradinho de 0,25 da unidade do gráfico). Nas cenas 3D, só o violeta liso, sem grade. Nos cartões sem gráfico (H2, A1, B5-3, B6-4, B6-5, S), só o violeta liso.
- Render por bloco (`render.sh <Classe>`), depois concatene.
- **Sem economia artificial.** Os mapas de cor (densidade x² + y², x², y², x²/(x² + y²)) são feitos de verdade: uma grade de quadradinhos sem contorno, com a cor da rampa, porque eles se transformam (espelho na diagonal no B1-3 e no B7-2). `ValueTracker` e updaters podem ser usados onde o movimento pede.
- Limpe da cena o que saiu da tela, e não deixe nada invisível acumulando.

### 2.2 Three.js (o pipeline da série)

- **Copie o pipeline do yt_0026** (`videos_longos/yt_0026_funcoes_vetoriais_campos/threejs/`), ou o de uma unidade mais recente da série se houver: `r3d.js`, `package.json` (playwright-core), `cena3d/three.min.js` (r128) e o esquema de pedidos.
  1. A passagem seca do Manim grava `pedidos3d/<LOTE>.json` com `{cena: [[quadro, estado], …]}`.
  2. `r3d.js` abre `cena3d/<cena>.html`, chama `window.setEstado(estado)` quadro a quadro e grava os PNGs com alfa e o `pontos.json`.
  3. O Manim cola os PNGs como `ImageMobject` em tela cheia e prende os rótulos nos pontos.
- **Porte as cenas de `c3d32.html`** para `threejs/cena3d/`. Vêm de lá `caixas()` (geometria única com cor por vértice), `arame()`, `tubo()`, `seta()`, `eixos()`, `base()`, `faixa()`, a solda `g(x)` e as câmeras (`CAM_PREDIO`, `CAM_BAIXO` e a câmera baixa do `b12`/`b21`). Cada cena ganha `setEstado(e)` com os parâmetros do §5 e devolve os pontos de `proj()`. **Atenção:** `c3d32.html` desenha só o estado final de cada chave (o do quadro-alvo); os estados intermediários (`cresceA`, `pousoB`, `k`, `n`, `nivela` etc.) são nomes sugeridos, e a animação entre eles é sua.
- **Estilo 3D da série:** opaco e sem luz (`MeshBasicMaterial`); topo na cor, faces x a 70 % e faces y a 48 % sobre o fundo; contorno escuro fino até n = 16 e sem contorno de n = 32 em diante; sem sombra, névoa, brilho ou transparência; `outputEncoding` linear; antialias ligado. **Quando algo precisa "aparecer através"** (a função g no B2-1, as lajes no B2-2), use só as arestas (`arame()`), nunca transparência.
- **Rótulos são do Manim**, presos aos pontos do `pontos.json` do mesmo quadro. Quando a câmera se move, o rótulo anda junto. Alinhamento ≤ 2 px.
- **Câmera:** movimentos lentos com começo e fim suaves; no máximo um movimento por ideia; **a câmera nunca se mexe enquanto uma fórmula está sendo escrita**; nada de órbita só para "dar movimento".

## 3. Sistema visual

### 3.1 Layouts e escala

| layout | geometria a 1080p | blocos |
|---|---|---|
| **A · palco + fórmulas** | Coluna de fórmulas alinhada à esquerda em **x = 1120**. Chapa R = [0, 2]² com **1 m = 240 px e o canto (0, 0) em (360, 780) px**. | B1-1, B3-3, B4-1, B5-2, B6-2, B7-1 |
| **A' · dois palcos menores + fórmulas** | Duas chapas de 2 m = 400 px (ou 360 px) lado a lado à esquerda; coluna em x ≈ 1240. | B1-3, B4-2, B6-3, B7-2 |
| **3D · palco + fórmulas** | O 3D ocupa a esquerda (objeto centrado perto de x = 600 px por `setViewOffset`); a coluna continua em x = 1120 e nada do 3D passa de x = 1090. | B1-2, B1-4, B2-1, B2-2, B3-1, B3-2, B6-1 |
| **Balança** | Dois pratos com os pedaços da chapa (pedaço leve à esquerda, pesado à direita), 1 m = 110 px, fiel e pratos em traço GEO fino. Um objeto só, reaproveitado no S1 e em miniatura no H2. | H1, H2, S1 |
| **C · cartões** | 3 cartões de 480–540 × 500–560 ou 4 de 410 × 430, só a moldura (`#B8C4DA` a 35 %, raio 14). | B5-3, B6-4, B6-5 |

Conversão para o Manim: x_m = (x_px − 960)/135; y_m = (540 − y_px)/135.

### 3.2 Regras (as da série)

- **R1 · Clareira:** nenhum rótulo sobre ponto, aresta, linha da grade ou número; o rótulo sai para o lado.
- **R2 · Placa:** todo rótulo solto sobre o desenho ou sobre o 3D usa `placa_min`.
- **R3:** fórmula nova nunca nasce sobre fórmula velha; a coluna limpa antes.
- **R4:** rótulo junto do objeto que ele nomeia.
- **R5:** QA automático de sobreposição em cada gatilho (§8).
- **R6:** nada sai da moldura do seu painel ou cartão; nada do 3D invade a coluna (x ≥ 1090).
- **R-texto:** legenda com no máximo 6 palavras e pelo menos 26 px a 1080p (as legendas de apoio dos alvos, em 22–24 px, sobem para 26 px).
- **Sublinhado de leitura:** quando a voz lê um símbolo ("lê-se…", "tais que", "implica", "interseção"), um sublinhado fino aparece sob ele no gatilho falado e sai. Não é pulso nem brilho.
- **Um movimento por ideia, uma vez.** Grade nova nasce da velha (`ReplacementTransform`), nunca pisca.
- Parado no máximo 3 s. Se a fala continua e a cena acabou, o próximo passo entra mais cedo.

### 3.3 Cores

| Papel | Cor |
|---|---|
| f, ρ, densidade, prédio de f, superfície x² + y², valores e massas, nível da média | ciano `#35D9FF` |
| **g** (segunda função nas fórmulas; arestas de g no B2-1) | **lilás claro `#C9A7FF`** (novo, aprovado) |
| x, a rampa x², o mapa de x²/(x² + y²) | âmbar `#FFC24D` |
| y, a rampa y², o mapa de y²/(x² + y²) | magenta `#EA63FF` |
| Metal leve / metal pesado | `#1E5072` / `#30BBE0` |
| Solda, B ∩ B₁, fronteira, furo | branco `#F5F7FF` |
| Cobertura menta, "o que falta abaixo do nível" (B6-1), ✓ | menta `#8CFFD2` |
| Muro na solda, "acima do nível" (B6-1), cota | coral `#FF7A8A` |
| Laje de 1 (B2-2), mínimo (B6-3) | azul-claro `#7FB2FF` |
| Caminho da prova, ponto (r, s), arco onde f = média | laranja `#E08A3C` |
| Área α, grade, molduras, balança | GEO `#B8C4DA` |
| Faixa contada duas vezes (B5-2), ✗, "13 kg? ERRO" | ALERTA `#FF5D5D` |

Operadores (∬, Σ, ∪, ∩, ⇒, ≤, ≠, ∈, { | }, ∃) em branco; a cor vai na grandeza.

### 3.4 Álgebra

- **Caneta** em toda fórmula nova: traço finíssimo (~0,7), glifo a glifo, da esquerda para a direita, preenchendo na cor da grandeza, sem flash e sem preview do destino.
- Termo que nasce no desenho **voa** para a fórmula (`TransformFromCopy`, arco). No 3D, ele voa a partir do ponto projetado.
- **Glyph maps obrigatórios** (MF-Tools `TransformByGlyphMap`, `MathTex` de string única nos dois lados):
  1. B1-2: `Σ(f + g)ΔA` → `Σ f ΔA + Σ g ΔA` (o parêntese se abre; cada parcela sai da sua caixa).
  2. B1-3: `32/3` → `16/3 + 16/3`.
  3. B1-4: `1·4 + 2·1,53` → `4 + 3,06` → `≈ 7,06`.
  4. B2-1: `g − f ≥ 0` → `∬(g − f) ≥ 0` → `∬g − ∬f ≥ 0` → `∬f ≤ ∬g`.
  5. B4-2: `∬(f − g) = 0` → `∬f − ∬g = 0` → `∬f = ∬g`.
  6. B5-2: `∬_B + ∬_{B₁} − ∬_{B∩B₁}` → o último termo vira `0` e sai junto com o sinal (o par acende e some junto).
  7. B6-3: `m·α ≤ ∬f ≤ M·α` → divide por α → `m ≤ média ≤ M`.
  8. B7-2: `∬ x²/r² + ∬ y²/r² = π` → `2·∬ x²/r² = π` → `∬ x²/r² = π/2`.
- Tamanhos: fórmula principal de 44–52 px no alvo e secundária de 36–42 px. Nada menor que 26 px.
- Números com vírgula decimal (`{,}` no LaTeX). Números da balança **com três casas**: `2,472 kg + 4,584 kg ≈ 7,06 kg`. Nunca `2,47 + 4,58 = 7,06` na tela.

## 4. Números (todos conferidos no script)

- **Chapa de dois metais:** R = [0, 2]²; solda y = g(x) = 1 + 0,42·sen(1,7x − 0,4); ρ = 1 kg/m² para y ≤ g(x) e 3 kg/m² acima.
  - Área leve 2,4721 m² → massa **2,472 kg**; área pesada 1,5279 m² → massa **4,584 kg**; total **7,0557 ≈ 7,06 kg**.
  - Camadas (B1-4): 1·4 = 4 kg + 2·1,53 ≈ 3,06 kg → 7,06 kg.
  - Faixa (B2-2): 4 ≤ massa ≤ 12. Média 7,06/4 ≈ **1,76 kg/m²** (B6-4).
  - Comprimento da solda ≈ **2,25 m**; cordão de 1 cm a 6 kg/m² ≈ **135 g**; de 1 mm ≈ **13 g** (B3-3).
  - Sobreposição numa faixa de 0,2 m de altura em volta da solda: 4 + 0,4 = **4,4 m²** (B5-2).
- **Muro de 100 kg/m² na solda** (B3-2): cota = 100 × área das células que a solda cruza.

  | n | células | área (m²) | cota (kg) |
  |---|---|---|---|
  | 64 | 95 | 0,093 | 9,3 |
  | 128 | 188 | 0,046 | 4,6 |
  | 256 | 376 | 0,023 | 2,3 |
  | 512 | 753 | 0,011 | 1,2 |
  | 1024 | 1 508 | 0,006 | 0,6 |

  Na cena 3D, o muro fica com altura desenhada fixa (escala vertical reduzida, com a legenda `ESCALA VERTICAL REDUZIDA`); só a largura muda.
- **Chapa x² + y²** (EP. 05): massa 32/3 kg. ∬x² = ∬y² = **16/3** (B1-3). Soma de Riemann com os mesmos pontos: n = 4 → 5,25 + 5,25 = 10,50.
  - Média = 8/3 ≈ **2,67**; arco x² + y² = 8/3, raio **1,63**, inteiro dentro da chapa.
  - Terraplanagem: volume acima do nível = volume que falta abaixo = **8π/9 ≈ 2,79**.
  - Prova (B6-3): mínimo 0 em (0, 0); máximo 8 em (2, 2).
- **Dois quadrados separados** (B6-4): densidade 1 e 3, média 2.
- **Exemplo 1** (B7): ∬_{disco de raio 1} x²/(x² + y²) = **π/2**; 0 ≤ f ≤ 1; na origem 0/0, valor 1 no eixo x e 0 no eixo y.

## 5. Cena a cena

- **Gatilho** é a frase da narração (`narracao_v3.md`) em que a ação começa.
- **Alvo** é o quadro em `yt_0032_quadros_alvo_v1/`, reproduzido com tolerância de ±20 px na posição e ±5 % no tamanho. Onde o alvo e este texto divergirem, vale o texto.
- **Canto:** a linha 1 é `CÁLCULO III · INTEGRAL DUPLA`, e a linha 2 é o título da cena que está no alvo.

### H · a balança · alvos 01 e 02
- **H1 (alvo 01).** Abre na chapa de dois metais inteira, com `7,06 kg` sob ela (papel + eixos).
  - "cortar essa chapa exatamente na linha da solda": a chapa se parte na solda, os pedaços se afastam e descem cada um num prato.
  - "O pedaço leve tem…" / "O pesado…": `2,472 kg` e `4,584 kg` aparecem sobre os pratos (caneta).
  - "Usando os valores sem arredondar": os dois números voam para `2,472 + 4,584 ≈ 7,06 kg`.
  - "contou a solda duas vezes?": a solda acende em branco **nos dois pedaços**; `CONTOU DUAS VEZES?` na coluna.
  - "cem quilos por metro quadrado": `E SE ρ = 100 NA SOLDA?`.
  - "densidade média…": `MÉDIA ≈ 1,76 kg/m²` e `ALGUM PONTO TEM A MÉDIA?`.
- **H2 (alvo 02).** A balança encolhe para o canto superior esquerdo. "a integral nasce de uma soma": `O QUE VALE NA SOMA` / `VALE NA INTEGRAL` (caneta). "conjunto de conteúdo nulo": `CONTEÚDO NULO NÃO PESA` em menta.

### A · apresentação · alvo 03
Padrão do canal. `INTEGRAIS DUPLAS · VÍDEO 3`, título `PROPRIEDADES DA INTEGRAL DUPLA` e as quatro etiquetas `1 · SOMAR`, `2 · COMPARAR`, `3 · DIVIDIR`, `4 · MÉDIA`, uma por palavra falada.

### B1 · somar e multiplicar · alvos 04 a 07
- **B1-1 (alvo 04), 2D.** Chapa com o mapa de densidade e a grade 4 × 4; `B` na região. Coluna: `f, g integráveis em B`, `k constante` e `UM NÚMERO FIXO`. "Lê-se": `∬_B f(x, y) dx dy` a caneta, com sublinhado de leitura em ∬, em B e em dx dy, um de cada vez. Legendas `B: A REGIÃO`, `dx dy: ÁREA DE CADA RETANGUINHO`.
- **B1-2 (alvo 05), 3D `b12`.** "levantamos as caixinhas da rampa horizontal": as 16 caixas âmbar (x² no centro de cada célula) crescem do chão (estado `cresceA` 0→1). "colocamos em cima delas": as 16 caixas magenta (y²) **descem e pousam** em cima (estado `pousoB` 0→1). Rótulos `x²` e `y²` presos nos pontos `xq` e `yq`.
  - Coluna: `MESMA GRADE, MESMOS PONTOS`; glyph map 1; "passando ao limite": `⇓ limite`; `∬_B(f + g) = ∬_B f + ∬_B g`; "também é integrável": `E f + g É INTEGRÁVEL`.
- **B1-3 (alvo 06), 2D.** Dois palcos: o mapa de x² (âmbar) com a diagonal tracejada. "espelha": o mapa se reflete na diagonal (`Transform` do mapa, uma vez, 1,2 s) e uma cópia vira o mapa de y² (magenta) no segundo palco. Coluna: `∬x² = ∬y²`; `32/3` voa da régua da massa (canto) e glyph map 2. `NENHUMA SOMA NOVA`.
- **B1-4 (alvo 07), 3D `b14`.** Começa nas 16 caixas do b12 esticando ×2 na vertical ("Se cá vale dois") e voltando (estado `k`: 1 → 2 → 0,5 → 1). Coluna: `∬_B k f = k ∬_B f` com sublinhado no gatilho "Lê-se".
  - "Agora junta com a regra da soma": troca para a chapa de dois metais em camadas: a camada de 1 kg/m² cresce na chapa toda; depois o reforço de 2 kg/m² cresce só no pedaço de cima. Rótulos `1 kg/m²` e `+2 kg/m²`.
  - Coluna: `CAMADA…` `1·4 = 4`, `REFORÇO…` `2·1,53 ≈ 3,06`, glyph map 3 → `≈ 7,06 kg`.

### B2 · sinal e comparação · alvos 08 e 09
- **B2-1 (alvo 08), 3D `b21`.** As caixas de f (ciano) no chão; uma reta dos números curta abaixo da coluna com 3 somas de Riemann (pontos laranja) caindo **à direita do zero**. "Essa é a propriedade dois": `II) f ≥ 0 em B ⇒ ∬_B f ≥ 0`, sublinhado no ⇒ em "implica".
  - "Daí vem a propriedade três": as arestas lilás de g crescem por cima das caixas de f. `III) f ≤ g em B ⇒ ∬_B f ≤ ∬_B g`.
  - "a diferença gê menos éfe": `g − f ≥ 0` nasce da folga entre as tampas (a folga de uma caixa acende em lilás e voa para a coluna); glyph map 4.
- **B2-2 (alvo 09), 3D `b22`.** A chapa de dois metais em colunas (1 e 3). "duas chapas uniformes": a laje de 1 (azul-claro) e a de 3 (coral) aparecem como contornos; `1·4 = 4 kg` e `3·4 = 12 kg` presos em `l1` e `l3`.
  - Coluna: régua da massa com a faixa [4, 12] acendendo e o ponto `7,06`; `m·α ≤ ∬_B f ≤ M·α` com `α: ÁREA DE B`. "treze quilos": carimbo `13 kg? ERRO` em ALERTA, levemente inclinado.

### B3 · a solda não pesa · alvos 10 a 12
- **B3-1 (alvo 10), 3D `b31`.** Só a solda, sobre o chão dos dois metais. "cobri-la com retângulos": a cobertura menta (do EP. 06) aparece em 2D antes de passar ao 3D, ou como tampas baixas; depois o muro coral de altura M cresce nas células que a solda cruza (n = 16). Marca `M` no eixo.
  - Coluna: `B tem conteúdo nulo ⇒ ∬_B f = 0`, `|f| ≤ M` `LIMITADA`, `∬ ≤ M · área da cobertura`, `ALTO, MAS CADA VEZ MAIS FINO`.
- **B3-2 (alvo 11), 3D `b32`.** "cem quilos": o muro sobe até a altura desenhada fixa (`ESCALA VERTICAL REDUZIDA`). A grade refina 64 → 128 → 256 → 512 → 1024, uma linha da tabela `COTA SUPERIOR` por passo falado (n · área · cota). Ao lado do muro, `COTA, NÃO MASSA`. Fecha com `→ 0`. A altura nunca muda; só a largura.
- **B3-3 (alvo 12), 2D.** A chapa de dois metais lisa com uma moldura tracejada sobre um trecho da solda; o painel de zoom mostra o **cordão** com largura (cor `#C9CFE0`), com a curva tracejada no meio. `L ≈ 2,25 m`, `6 kg/m², LARGURA 1 cm → 1 mm`; "Com um centímetro": `≈ 135 g`; "Com um milímetro": o cordão afina e `135 g → 13 g → 0`; no fim, o cordão vira a curva branca. "densidade linear": `kg/m (MASSA NUMA LINHA) → INTEGRAL DE LINHA` em menta.

### B4 · mudar f sem mudar a integral · alvos 13 e 14
- **B4-1 (alvo 13), 2D.** Chapa de dois metais; a solda engrossa em coral. A cada valor falado (um, três, dois, cem), a solda troca de cor e a etiqueta `ρ = …` correspondente acende embaixo (corte simples, sem pulso). O contador `MASSA ≈ 7,06 kg` fica **parado**; `TANTO FAZ`.
  - Coluna: `{(x, y) ∈ B | f ≠ g}` a caneta, sublinhado no `|` em "tais que"; `tem conteúdo nulo ⇒ ∬_B f = ∬_B g`.
- **B4-2 (alvo 14), 2D.** Palco 1: `f − g` vale zero fora da solda; só as células que a solda cruza acendem em coral, e a grade refina (16 → 32 → 64) com as células afinando. Glyph map 5. Palco 2: "um furo na origem": um disco com um furo tracejado no centro; o furo é preenchido por valores diferentes (três cores em sequência) e a integral ao lado não muda. `PREENCHE E A INTEGRAL NÃO MUDA`.

### B5 · dividir a região · alvos 15 a 17
- **B5-1 (alvo 15), 2D.** Os dois pedaços se afastam um pouco (a solda fica nas duas bordas, duas linhas brancas) e voltam a se encostar. Rótulos `B` e `B₁`.
  - Coluna: `B ∩ B₁ tem conteúdo nulo ⇒`, `∬_{B∪B₁} f = ∬_B f + ∬_{B₁} f`, com sublinhados em ∪ e ∩ nos gatilhos "união" e "interseção". `2,472 + 4,584 ≈ 7,06 kg` (os números voam da balança no canto).
- **B5-2 (alvo 16), 2D.** "A conta correta": `∬_{B∪B₁} = ∬_B + ∬_{B₁} − ∬_{B∩B₁}`; a solda acende duas vezes; glyph map 6. "faixa de vinte centímetros": a faixa ALERTA hachurada aparece em volta da solda; `4 + 0,4 = 4,4 m² numa chapa de 4`, `SOBREPOSIÇÃO COM ÁREA: DESCONTAR`.
- **B5-3 (alvo 17), cartões.** Três cartões entrando um por frase: peças montadas (encostam numa face), região em L (dois retângulos), dois metais (corte onde ρ muda). `VÁRIAS INTEGRAIS SIMPLES`.

### B6 · valor médio · alvos 18 a 22
- **B6-1 (alvo 18), 3D `b61`.** Começa com o prédio de x² + y² inteiro em ciano (n = 16). "nivelarmos tudo": aparece o contorno ciano do nível 8/3. "Olha a terraplanagem": a parte acima do nível acende em coral e **desce em camadas** para os buracos, que se enchem em menta (um movimento só, estado `nivela` 0→1; o volume se conserva). No fim, o arco laranja onde f = 8/3 acende.
  - Coluna: `média = (32/3)/4 = 8/3 ≈ 2,67`; `acima = abaixo = 8π/9 ≈ 2,79`; `x² + y² = 8/3` e `ARCO DE RAIO 1,63`.
- **B6-2 (alvo 19), 2D.** Chapa com o mapa de densidade e o arco laranja; um ponto `(r, s)` no arco. Três ícones: disco fechado ✓, disco com borda tracejada ✗, faixa ilimitada ✗ (no gatilho "Fechada quer dizer…" / "limitada…"). O enunciado a caneta em duas linhas de hipóteses e uma de tese; sublinhado em ∃ ("existe") e em α ("sendo alfa a área").
- **B6-3 (alvo 20), 2D.** Mínimo (azul-claro) em (0, 0) e máximo (coral) em (2, 2). Glyph map 7. "escolhe um caminho": um caminho laranja curvo é desenhado do mínimo ao máximo; ao lado, o gráfico de f **ao longo do caminho** é traçado junto (mesma velocidade), de 0 a 8, e cruza a linha tracejada 8/3; o ponto de cruzamento acende e volta para a chapa, caindo no arco. `ÁREA 0: QUALQUER PONTO SERVE` no fim.
- **B6-4 (alvo 21), cartões.** Três cartões:
  1. "a função salta": perfil em degrau (1 e 3) com a linha da média 1,76 passando entre os degraus; ✗.
  2. "dois quadrados separados": dois quadrados 1 e 3 com um vão entre eles; ✗.
  3. "colocar um vírgula setenta e seis exatamente sobre a solda": a solda acende em menta e um ponto laranja pousa nela; ✓ `MÉDIA ATINGIDA`.
  - Embaixo: `SUFICIENTE, NÃO NECESSÁRIA` e `SEM AS HIPÓTESES, O TEOREMA NÃO GARANTE`.
- **B6-5 (alvo 22), cartões.** Quatro cartões entrando um por exemplo falado; embaixo, `média = ∬_B f / α`.

### B7 · integral sem integrar · alvos 23 e 24
- **B7-1 (alvo 23), 2D.** Disco de raio 1 (centro da chapa) com o mapa de x²/(x² + y²) em âmbar e o furo tracejado na origem. "Pelo eixo horizontal…": `1` no eixo x e `0` no eixo y. Coluna: a função, `(0,0): 0/0`, `UM PONTO TEM CONTEÚDO NULO`, `0 ≤ f ≤ 1`, `PREENCHE O FURO: INTEGRÁVEL`.
- **B7-2 (alvo 24), 2D.** O mapa de x²/r² e o de y²/r² lado a lado, `+`, `=` e o disco inteiro em `1` ("o numerador fica igual ao denominador"). `= área = π`. "espelhando o disco pela diagonal": o mapa âmbar se reflete e coincide com o magenta. Glyph map 8 até `π/2`. `SOMA · CONTEÚDO NULO · SIMETRIA`.

### S · síntese e próximo · alvos 25 e 26
- **S1 (alvo 25).** A balança volta; três caixas com ✓, uma por resposta falada: `SOLDA: 0 kg`, `DENSIDADE NA SOLDA: TANTO FAZ`, `MÉDIA: CONTINUIDADE + CAMINHO`. Embaixo, a lista curta das sete propriedades (26 px).
- **S2 (alvo 26).** Cartão `NO PRÓXIMO VÍDEO` · `TEOREMA DE FUBINI`; a chapa de dois metais se fatia em tiras verticais que se separam um pouco ("A ideia é fatiar a região"). `7,06 = 12 − 2·área leve`, `COMO CALCULAR O 7,06 EXATO?`, `FATIAR: DUAS INTEGRAIS SIMPLES`. Depois o CTA padrão (logo, anéis, INSCREVA-SE).

## 6. Narração (para o tempo do preview)

O preview é silencioso, mas cada âncora dura o tempo estimado da fala de `narracao_v3.md` (tabela "Tempo por âncora", 3 palavras/s): total ≈ **17:46**.
- Gere um `duracoes_estimadas.json` por âncora, como nas unidades anteriores, para a voz encaixar depois.
- Os gatilhos do §5 são frases dessa narração; marque o instante estimado de cada um a partir da contagem de palavras.
- **Não gerar voz.**

## 7. O que NÃO fazer

- Nada de `ThreeDScene`, `Surface` ou `Prism` do Manim: todo 3D é Three.js.
- Nenhuma partícula, brilho, sombra, névoa, contorno em seta, pulso automático ou transparência no 3D.
- Câmera nunca se mexe durante a escrita de uma fórmula.
- Não escrever `2,47 + 4,58 = 7,06` na tela.
- Não mexer em `template/`, `assets/`, `docs/`, `AGENTS.md` nem nas outras unidades.
- Não citar livro nem o Atlas na tela. Não dizer "peso": é massa.
- Não gerar voz, SRT, master, 1080p nem entrega. Não fazer commit nem push.

## 8. QA do preview (obrigatório antes de entregar)

1. **Render × alvo:** um still em cada um dos 26 gatilhos, tirado quando o estado do alvo está completo, comparado na mesma resolução (alvo reduzido a 960×540, tolerância de 10 px nessa escala). Prancha `comparacao_v1.jpg`; toda diferença que sobrar vai listada com o motivo.
2. **Alinhamento 3D × Manim:** para cada quadro 3D, os rótulos contra os pontos do `pontos.json` do mesmo quadro (≤ 2 px). Relatório `alinhamento3d_v1.txt`.
3. **R5 · sobreposição:** em cada gatilho, caixas de texto e `MathTex` não se cruzam entre si nem com pontos, arestas ou linhas. Relatório `sobreposicoes_v1.txt`.
4. **R6:** nada sai do painel ou cartão; o 3D não invade a coluna.
5. **Flash por quadro = 0:** nenhuma fórmula aparece inteira antes da caneta (nada de `FadeIn`, `TransformFromCopy` ou `Write` dentro de `Succession(Wait…)`/`AnimationGroup` que ponha o destino na cena no instante 0). Relatório `flash_por_quadro_v1.txt`.
6. **Glyph maps:** os 8 do §3.4 existem e nenhuma linha começa órfã com "=".
7. **Parado ≤ 3 s.**
8. **Números:** confira na tela os valores do §4 (em especial a balança com três casas e a tabela de cotas).
9. **Tempo de render por bloco** em `tempos_render_v1.txt`, só para registro.

## 9. Parada

Entregue o preview, a prancha, os relatórios e o relatório de entrega. Pare. Não inicie voz nem 1080p.

---

## Anexo A · narração v3 por âncora (cópia de `narracao_v3.md`, para os gatilhos)


Tags permitidas: [curious], [thoughtful], [surprised], [happy], [excited], [serious]. Uma por parágrafo (o S2 tem duas, como nos EP. 05 e 06). Sem [slowly] e sem [pause]. Letras escritas como a voz deve ler: éfe, gê, cá, xis, ípsilon, érre, ésse, éle, eme.

### H1 · a balança e as três perguntas
**Tela:** a chapa inteira com `7,06 kg`; ela se parte na solda; os pedaços nos pratos; `2,472 kg + 4,584 kg ≈ 7,06 kg`; a solda acende nos dois pedaços (`CONTOU DUAS VEZES?`); `E SE ρ = 100 NA SOLDA?`; `MÉDIA ≈ 1,76 kg/m²` + `ALGUM PONTO TEM A MÉDIA?`.
> [curious] Lembra da chapa de dois metais? Embaixo da solda, um quilo por metro quadrado; em cima, três. No episódio passado, descobrimos que a massa total existe e vale aproximadamente sete vírgula zero seis quilos. Agora imagina cortar a chapa exatamente na linha da solda e colocar os dois pedaços numa balança. O pedaço leve tem aproximadamente dois vírgula quarenta e sete quilos. O pesado, quatro vírgula cinquenta e oito. Usando os valores sem arredondar, a soma dá os mesmos sete vírgula zero seis. Até aqui, tudo bem. Mas olha a linha branca entre os dois metais: ela é a fronteira dos dois pedaços. Será que a gente contou a solda duas vezes? E quanto ela pesa? Agora piora: e se a densidade exatamente sobre a solda fosse de cem quilos por metro quadrado? A massa mudaria? E uma última pergunta: a densidade média da chapa é aproximadamente um vírgula setenta e seis quilo por metro quadrado. Existe algum ponto onde a densidade tem exatamente esse valor?

### H2 · o que vamos descobrir
**Tela:** a balança encolhe para o canto; `O QUE VALE NA SOMA` / `VALE NA INTEGRAL`; embaixo, `CONTEÚDO NULO NÃO PESA`.
> [serious] Parecem três perguntas diferentes, mas as propriedades da integral dupla respondem todas. E a ideia principal é simples: a integral nasce de uma soma. Então as regras que funcionam nas somas continuam funcionando quando passamos ao limite: somar, multiplicar, comparar e dividir regiões. E tem um ingrediente a mais, que veio do episódio passado: um conjunto de conteúdo nulo pode estar no desenho sem contribuir para a integral de uma função limitada. É isso que vai resolver o mistério da solda.

### A1 · apresentação
**Tela:** logo; `INTEGRAIS DUPLAS`; `NESTE VÍDEO: SOMAR · COMPARAR · DIVIDIR · MÉDIA`.
> [happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Esse é o sétimo episódio da nossa série de Cálculo três e o terceiro do módulo de integrais duplas. A gente já sabe de onde a integral vem e como garantir que ela existe. Agora vamos aprender a trabalhar com ela: sete propriedades para somar, comparar, estimar e dividir integrais sem refazer a conta. E, no final, o teorema do valor médio. Cada propriedade vai sair de um desenho.

### B1-1 · as regras do jogo
**Tela:** D1; `f, g INTEGRÁVEIS EM B` · `k CONSTANTE`; `∬_B f(x, y) dx dy` a caneta, sublinhado em ∬, B e dx dy no gatilho.
> [thoughtful] Primeiro, as regras do jogo. Temos duas funções, éfe e gê, integráveis numa mesma região B, e uma constante cá, que é simplesmente um número fixo. Lembrando: uma função é integrável quando suas somas de Riemann convergem para um único valor à medida que a partição fica fina, independentemente dos pontos escolhidos. Esse valor é escrito com o símbolo de integral dupla. Lê-se: integral dupla sobre B de éfe de xis, ípsilon, dê xis, dê ípsilon. A letra B indica a região onde estamos somando, e o dê xis, dê ípsilon representa o elemento de área.

### B1-2 · somar funções
**Tela:** D2 em Three.js (rampa x² âmbar + rampa y² magenta → prédio ciano); na coluna, `Σ (f + g) ΔA = Σ f ΔA + Σ g ΔA` e depois `∬(f + g) = ∬f + ∬g`.
> [curious] Pega a nossa chapa quadrada de dois metros de lado e duas funções: xis ao quadrado, uma rampa que cresce na direção horizontal, e ípsilon ao quadrado, uma rampa que cresce na direção vertical. Mesma grade para as duas, mesmos pontos em cada célula. Primeiro, levantamos as caixinhas da rampa horizontal. Depois, colocamos em cima delas as caixinhas da outra rampa. Em cada célula, a altura total é a soma das duas alturas. Então a soma de Riemann de éfe mais gê é exatamente a soma de Riemann de éfe mais a de gê. Isso vale antes mesmo de refinar a grade! E, passando ao limite, a igualdade continua valendo. Portanto, a soma de duas funções integráveis também é integrável, e a integral da soma é a soma das integrais.

### B1-3 · uma conta de graça
**Tela:** D3: espelho na diagonal; `32/3` voa da régua da massa e vira `16/3 + 16/3`.
> [excited] E olha o que isso dá de graça! Quando construímos a integral dupla, a chapa com densidade xis ao quadrado mais ípsilon ao quadrado deu trinta e dois terços de quilo. Agora espelha a rampa de xis ao quadrado pela diagonal da chapa: ela se transforma exatamente na rampa de ípsilon ao quadrado. A região continua a mesma, e as caixinhas correspondentes têm os mesmos volumes. Então as duas integrais são iguais. Como somam trinta e dois terços, cada uma vale dezesseis terços. Nenhuma soma nova: só a propriedade que acabamos de ver e a simetria do desenho.

### B1-4 · multiplicar por uma constante
**Tela:** D4: caixas esticam ×2; `∬ k f = k ∬ f`; as duas camadas da chapa de dois metais; `1 · 4 = 4` e `2 · 1,53 ≈ 3,06`; `4 + 3,06 ≈ 7,06`.
> [thoughtful] A segunda parte da primeira propriedade é a constante. Multiplicando a função por cá, todas as caixinhas têm a altura multiplicada por cá. Se cá vale dois, as alturas dobram; se vale meio, caem pela metade; se é negativo, a contribuição troca de sinal. Em todos os casos, cada parcela da soma de Riemann é multiplicada por cá, e a constante sai da soma e, depois, da integral. Lê-se: a integral de cá vezes éfe é cá vezes a integral de éfe. Agora junta com a regra da soma. A chapa de dois metais pode ser vista como uma camada de um quilo por metro quadrado sobre os quatro metros quadrados, mais um reforço de dois quilos por metro quadrado só na região do metal pesado. A camada dá quatro quilos; o reforço, aproximadamente três vírgula zero seis. Total: sete vírgula zero seis quilos, agora montado em camadas.

### B2-1 · uma função acima da outra
**Tela:** D5 (caixas no chão; somas sempre à direita do zero); D6 (prédio de f dentro do de g); `f ≥ 0 em B ⇒ ∬f ≥ 0`; `f ≤ g em B ⇒ ∬f ≤ ∬g`; `g − f ≥ 0` nasce da folga.
> [curious] Agora uma propriedade que parece óbvia no desenho, mas é muito útil nas contas. Se uma função é maior ou igual a zero em toda a região, cada parcela da soma de Riemann também é, e a integral não pode ser negativa. Essa é a propriedade dois, a do sinal. Aquela seta na fórmula se lê "implica". Daí vem a propriedade três: se éfe é menor ou igual a gê em todos os pontos, a integral de éfe é menor ou igual à de gê. Por quê? A diferença gê menos éfe nunca é negativa, então sua integral também não é. E, pela propriedade da soma, essa integral é a integral de gê menos a integral de éfe. Reorganizando, aparece a comparação. Percebe? Uma propriedade ajuda a demonstrar a seguinte.

### B2-2 · estimar sem resolver
**Tela:** D7: as lajes de 1 e 3; régua da massa com a faixa [4, 12] e o 7,06 dentro; `m · α ≤ ∬ f ≤ M · α`; `13 kg? ERRO`.
> [thoughtful] E a comparação permite descobrir se uma resposta é possível antes de calcular a integral. Na chapa de dois metais, a densidade fica entre um e três quilos por metro quadrado. Compara com duas chapas uniformes: com a menor densidade, a massa seria quatro quilos; com a maior, doze. Então a massa verdadeira está entre quatro e doze, e o sete vírgula zero seis passa no teste. Em geral, se uma função fica entre um valor eme minúsculo e um eme maiúsculo, sua integral fica entre esses valores multiplicados pela área da região, que chamamos de alfa. Parece simples, mas é extremamente útil: se um programa calculasse treze quilos para essa chapa, já saberíamos que tem erro, sem resolver a integral inteira.

### B3-1 · uma linha pode ter massa?
**Tela:** D8: só a solda com a cobertura menta; o muro coral (Three.js); `B COM CONTEÚDO NULO ⇒ ∬_B f = 0`; `∬ ≤ M · ÁREA DA COBERTURA`.
> [serious] Agora, a primeira pergunta da abertura: quanto pesa a solda? Começa pela solda matemática: uma curva, sem espessura. No episódio passado, vimos que essa linha tem conteúdo nulo: dá para cobri-la com retângulos de área total tão pequena quanto quisermos. Agora põe sobre ela uma densidade limitada: existe um número eme maior que o módulo de todos os seus valores. A contribuição das células que cobrem a solda fica limitada por eme vezes a área da cobertura. A altura pode ser grande, mas a área vai ficando cada vez menor, e a contribuição tende a zero. Essa é a quarta propriedade: a integral de uma função limitada sobre um conjunto de conteúdo nulo é zero. No desenho, um muro que pode ser alto, mas fica tão fino quanto se queira.

### B3-2 · um muro de cem
**Tela:** D9: o muro de altura 100 afinando; tabela `COTA SUPERIOR` com `n · ÁREA · COTA`: 64 · 0,093 · 9,3 kg → 1024 · 0,006 · 0,6 kg; ao lado do muro, `COTA, NÃO MASSA`.
> [surprised] Vamos exagerar: densidade de cem quilos por metro quadrado exatamente sobre a solda. O muro coral fica altíssimo. Com sessenta e quatro divisões por lado, a cota superior desse muro chega a nove vírgula três quilos. Atenção: é uma cota grosseira, não a massa real da linha. Dobra a resolução: a cota cai para quatro vírgula seis. Depois, dois vírgula três. Depois, um vírgula dois. E, continuando, seis décimos de quilo. A altura continua cem; o que desaparece é a área da cobertura. Repetindo, a contribuição fica menor que qualquer tolerância positiva. Então a solda matemática não acrescenta massa à integral dupla, por maior que seja a densidade, desde que limitada. E contar zero duas vezes não muda nada.

### B3-3 · mas uma solda real pesa
**Tela:** D10: zoom na solda; o cordão de 1 cm com `≈ 135 g`; afina para 1 mm, `≈ 13 g`; vira a curva branca; `kg/m` quando a voz fala de densidade linear.
> [thoughtful] Só que aqui precisamos separar o modelo da realidade. Uma solda de verdade é um cordão de metal: ocupa espaço e acrescenta massa à peça. Vamos representá-lo como uma faixa de largura constante, com seis quilos por metro quadrado. A linha da solda tem uns dois vírgula vinte e cinco metros. Com um centímetro de largura, a faixa teria uns cento e trinta e cinco gramas. Com um milímetro, uns treze gramas. E, conforme a largura tende a zero, a massa desse modelo também tende a zero. E se quisermos uma massa realmente concentrada numa linha? Aí usamos uma densidade linear, em quilos por metro, que leva às integrais de linha. A integral dupla com densidade superficial limitada não representa uma massa concentrada dessa maneira.

### B4-1 · cem, dois ou três?
**Tela:** D11: a solda troca de cor e rótulo (`ρ = 1`, `3`, `2`, `100`), contador parado em `≈ 7,06 kg`; `{(x, y) ∈ B | f ≠ g}` a caneta, sublinhado no "|".
> [curious] Agora, uma consequência surpreendente. Qual densidade devemos colocar exatamente sobre a solda? A do metal leve, um? A do pesado, três? A média, dois? Ou aquele exagero de cem? Para a massa total, tanto faz. Essa é a quinta propriedade: se duas funções integráveis só diferem num conjunto de conteúdo nulo, suas integrais são iguais. Na fórmula, aparece o conjunto dos pontos xis, ípsilon de B tais que éfe é diferente de gê. O tracinho em pé, dentro das chaves, se lê "tais que". Se esse conjunto tem conteúdo nulo, a integral de éfe é igual à de gê. Então podemos mudar a densidade sobre a solda, e o contador continua marcando sete vírgula zero seis quilos.

### B4-2 · o motivo e a função com furo
**Tela:** D12: caixas de f − g (zero fora, muro fino na solda); um furo tracejado preenchido por valores diferentes, a integral parada.
> [thoughtful] E essa propriedade nasce das anteriores. Se duas funções são iguais fora da solda, a diferença entre elas vale zero fora dessa linha. Então, nas somas da diferença, só contam as células que encostam na solda, e a área delas pode ser tornada arbitrariamente pequena. A integral da diferença é zero, e, pela propriedade da soma, as integrais das duas funções são iguais. Isso também resolve uma situação comum: uma função que não está definida em alguns pontos, como um furo na origem ou uma borda onde a fórmula falha. Se esses pontos formam um conjunto de conteúdo nulo, podemos preenchê-los com valores limitados e trabalhar com uma extensão integrável. O valor da integral não depende de como preenchemos o furo.

### B5-1 · a propriedade da balança
**Tela:** D13: os dois pedaços se afastam e voltam; `B ∩ B₁ COM CONTEÚDO NULO ⇒ ∬_{B∪B₁} f = ∬_B f + ∬_{B₁} f`; `2,472 + 4,584 ≈ 7,06`.
> [serious] Agora voltamos à balança, com a propriedade seis. A chapa foi dividida em duas partes: o metal leve, que vamos chamar de B, e o metal pesado, B um. Se a função é integrável nelas e a parte comum tem conteúdo nulo, a integral sobre a união é a soma das duas integrais. O U normal é a união: os dois conjuntos juntos. O U de cabeça para baixo é a interseção: a parte em comum. Lê-se: a integral sobre B união B um é igual à integral sobre B mais a integral sobre B um. A solda está na fronteira dos dois pedaços, então aparece nas duas regiões. Mas ela tem conteúdo nulo, e sua contribuição é zero. Por isso a balança não precisa de correção: sem arredondar, o total é sete vírgula zero seis quilos.

### B5-2 · e se houver sobreposição?
**Tela:** a solda acende duas vezes; `∬_B + ∬_{B₁} − ∬_{B∩B₁}`; o último termo vira `0` e sai; D14: faixa de 0,2 m hachurada duas vezes, `4 + 0,4 = 4,4 m²`.
> [thoughtful] E se a parte comum tiver área positiva? Aí somar as integrais conta essa parte duas vezes. A conta correta é a integral sobre B, mais a integral sobre B um, menos a integral sobre a interseção. É como contar os alunos de duas turmas: quem está nas duas não pode entrar duas vezes no total. Na chapa: faz os dois pedaços se sobreporem numa faixa de vinte centímetros de altura. A chapa tem quatro metros quadrados, mas a soma das áreas dos dois pedaços dá quatro vírgula quatro. Os quatro décimos extras são a faixa contada duas vezes. Quando a interseção tem conteúdo nulo, esse desconto vale zero e desaparece. Com área positiva, precisamos descontá-la.

### B5-3 · por que dividir ajuda?
**Tela:** quatro miniaturas: peças montadas que se tocam numa face; região em L partida em dois retângulos; a chapa partida na solda; "várias integrais simples".
> [curious] E dividir é uma das estratégias mais úteis na prática. A massa de uma peça montada sai das massas de cada componente, sem sobreposições. Uma região em formato de éle vira dois retângulos. Uma chapa de materiais diferentes se divide justamente onde a densidade muda. Em vez de uma integral complicada, várias integrais simples. Quando começarmos a trabalhar com integrais iteradas, essa estratégia vai aparecer o tempo todo.

### B6-1 · a terraplanagem
**Tela:** D16 em Three.js: a superfície x² + y² vira morro; terraplanagem até a altura 8/3; `ACIMA: 8π/9` · `ABAIXO: 8π/9`; o arco de raio 1,63 acende na chapa.
> [curious] Agora, a terceira pergunta: a média. Volta à chapa com densidade xis ao quadrado mais ípsilon ao quadrado. A massa é trinta e dois terços de quilo, e a área é quatro metros quadrados. Dividindo, a densidade média é oito terços, aproximadamente dois vírgula sessenta e sete quilos por metro quadrado. Agora transforma a densidade num relevo, como quando construímos a integral: o gráfico vira um morro. A média é a altura que dá o mesmo volume se nivelarmos tudo. Olha a terraplanagem: o material acima dessa altura vai preencher o espaço que falta abaixo. O volume retirado e o preenchido são iguais: oito pi sobre nove, aproximadamente dois vírgula setenta e nove. E existe algum ponto da chapa que já tem exatamente a altura média? Existe! Todos os pontos deste arco, a um vírgula sessenta e três da origem, têm densidade igual a oito terços.

### B6-2 · o teorema aparece
**Tela:** D15 (ícones fechado/limitado); o enunciado a caneta: `B COMPACTO · FRONTEIRA DE CONTEÚDO NULO`, `CAMINHO DENTRO DE B · f CONTÍNUA`, `⇒ ∃ (r, s) ∈ B : ∬_B f = α f(r, s)`; `α = ÁREA DE B`.
> [serious] Mas isso acontece com qualquer função? Aqui entra a sétima propriedade: o teorema do valor médio para integrais duplas. As hipóteses: a região B é compacta, ou seja, fechada e limitada. Fechada quer dizer que contém seus pontos de fronteira; limitada, que cabe dentro de algum retângulo. A fronteira tem conteúdo nulo. Dois pontos quaisquer da região podem ser ligados por um caminho contínuo que não sai dela. E a função é contínua. Com essas condições, existe pelo menos um ponto érre, ésse da região onde a função vale exatamente a média. Na fórmula, a integral sobre B de éfe é igual a alfa vezes éfe de érre, ésse, sendo alfa a área de B. Em outras palavras: desde que a região tenha área positiva, a função assume em algum lugar o valor médio.

### B6-3 · por que isso é verdade?
**Tela:** D17: mínimo em (0, 0), máximo em (2, 2); `m · α ≤ ∬ f ≤ M · α` volta do B2-2 e se divide por α; o caminho laranja; o gráfico ao longo do caminho cruzando 8/3.
> [thoughtful] E a demonstração é muito bonita, porque junta duas ideias conhecidas. Como B é compacto e a função é contínua, ela atinge um mínimo e um máximo na região. Na nossa chapa, o mínimo é zero, na origem, e o máximo é oito, no canto oposto. Pela comparação, a integral fica entre o mínimo vezes a área e o máximo vezes a área. Dividindo pela área, a média está entre o mínimo e o máximo. Agora escolhe um caminho dentro da região ligando um ponto de mínimo a um ponto de máximo. Ao longo dele, a função muda continuamente. E, pelo teorema do valor intermediário, uma função contínua não passa de um valor abaixo da média para outro acima sem assumir a própria média. Esse é o ponto érre, ésse. E, se a região tiver área zero e não for vazia, a integral é zero, e qualquer ponto satisfaz a igualdade.

### B6-4 · quando a média não aparece
**Tela:** D18: (a) degraus 1 e 3 com a linha da média 1,76 passando entre eles; (b) dois quadrados separados, 1 e 3, média 2; (c) beat novo: a solda acende em `ρ = 1,76`, ponto laranja nela, `MÉDIA ATINGIDA`.
> [curious] Agora a parte interessante: o que acontece sem alguma dessas hipóteses? Volta à chapa de dois metais. A densidade média é aproximadamente um vírgula setenta e seis, mas, no modelo original, a função só assume dois valores: um e três. Nenhum ponto tem densidade um vírgula setenta e seis: a função salta de um valor para o outro, passando por cima da média. Outro exemplo: dois quadrados separados, um com densidade um e o outro com densidade três. A função é contínua na região formada pelos dois, mas não existe caminho dentro dela ligando os quadrados. A média é dois, e a função não vale dois em nenhum ponto. Só que repara no outro lado da moeda: pela quinta propriedade, dá para colocar um vírgula setenta e seis exatamente sobre a solda sem mudar a massa. Aí a média aparece num ponto, mesmo com o salto. Então continuidade e caminho garantem o resultado, mas não são a única forma de ele acontecer. Sem essas hipóteses, a média pode até ser atingida, mas o teorema não assegura.

### B6-5 · onde encontramos essa média?
**Tela:** quatro miniaturas: placa aquecida, bacia de rio com chuva, terraplanagem, imagem; `MÉDIA = ∬ f / α`.
> [happy] E essa média aparece em muito lugar. A temperatura média de uma placa aquecida. A altura média de chuva numa bacia hidrográfica. A altura de uma terraplanagem, que equilibra corte e aterro. O brilho médio de uma região numa imagem digital. A integral dupla dá a média mesmo quando a grandeza varia de ponto para ponto. E o teorema acrescenta: se a função é contínua e a região satisfaz as hipóteses do teorema, algum lugar assume exatamente esse valor médio.

### B7-1 · a função com um furo
**Tela:** D19: mapa de x²/(x² + y²) no disco, origem tracejada; `1` no eixo x, `0` no eixo y; o furo preenchido.
> [curious] Para fechar, um exemplo que junta várias propriedades. No disco de raio um, considera a função xis ao quadrado dividido por xis ao quadrado mais ípsilon ao quadrado. Na origem, a fórmula vira zero dividido por zero: a função não está definida ali. E o limite na origem nem existe: pelo eixo horizontal, o valor é um; pelo vertical, zero. Mas a origem é um único ponto, e um ponto tem conteúdo nulo. Fora dele, a função é contínua e fica entre zero e um. Então podemos preencher o furo com qualquer valor finito: a função fica integrável, e a integral não depende do valor escolhido. É a quinta propriedade funcionando.

### B7-2 · pi sobre dois, sem fazer conta
**Tela:** os dois mapas somados viram o disco todo em `1`; `= ÁREA = π`; espelho na diagonal; `π/2 + π/2`.
> [excited] E agora o valor, sem calcular nenhuma primitiva. Cria uma segunda função, parecida, mas com ípsilon ao quadrado no numerador. Somando as duas, fora da origem, o numerador fica igual ao denominador. Resultado: um! Então a soma das duas funções vale um em todo o disco, exceto talvez naquele ponto que não altera a integral. Pela propriedade da soma, as duas integrais juntas valem a integral de um sobre o disco, que é a área: pi. Agora a simetria: espelhando o disco pela diagonal, a primeira função vira a segunda, e a região continua a mesma. Então as integrais são iguais. Dois números iguais que somam pi: cada um vale pi sobre dois. Soma, conteúdo nulo e simetria. Nenhuma integração complicada.

### S1 · voltando à balança
**Tela:** a balança volta com os três ✓: `SOLDA: 0 kg` · `DENSIDADE NA SOLDA: TANTO FAZ` · `MÉDIA: CONTINUIDADE + CAMINHO`; embaixo, a lista curta das sete.
> [thoughtful] Então olha o que aprendemos. A integral dupla nasce de uma soma, por isso podemos somar funções, multiplicar por constantes e comparar resultados. Um conjunto de conteúdo nulo não contribui para a integral de uma função limitada, e mudar a função só nele não altera o resultado. Dividir a região funciona quando a sobreposição não traz contribuição extra. E o teorema do valor médio garante que uma função contínua, numa região adequada, atinge sua média em algum ponto. As três perguntas da abertura: a solda matemática não acrescenta massa; o valor limitado que pomos nela não altera o total; e, para garantir um ponto com a média, olhamos a continuidade e a geometria da região.

### S2 · o próximo vídeo e CTA
**Tela:** cartão `NO PRÓXIMO VÍDEO: TEOREMA DE FUBINI`; a chapa de dois metais fatiada em tiras verticais; `COMO CALCULAR O 7,06 EXATO?`; depois o CTA padrão.
> [curious] Mas repara numa coisa. Até aqui, as integrais apareceram como limites de somas de Riemann, com grades cada vez mais finas, propriedades e simetrias. Falta uma pergunta bem prática: como calcular uma integral dupla diretamente, com as ferramentas do Cálculo um? Por exemplo: dá para achar a massa exata da chapa de dois metais numa conta no papel, sem refinar milhares de caixinhas? Dá. A ideia é fatiar a região: primeiro, somamos dentro de cada fatia; depois, somamos as fatias. Duas integrais simples trabalhando juntas. É isso que vamos ver no próximo episódio, com o teorema de Fubini. [happy] Se essa aula te ajudou, deixa o like e se inscreve no Parallax Lab para acompanhar a série. E conta nos comentários: qual propriedade te surpreendeu mais? A solda sem massa, mudar a função num conjunto de conteúdo nulo ou o ponto com o valor médio? Até a próxima!
