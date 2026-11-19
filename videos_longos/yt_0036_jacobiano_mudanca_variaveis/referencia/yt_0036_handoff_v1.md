# yt_0036 · CÁLCULO III · EP. 11 · Jacobiano e mudança de variáveis (3.4-T1)
## HANDOFF v1 (para o Claude Code): preview visual do vídeo inteiro, com uma cena 3D em Three.js

Data: 2026-11-14. Formato: `longo_horizontal`, tipo teoria visual. Unidade nova: `videos_longos/yt_0036_jacobiano_mudanca_variaveis/`. Antes de criar a pasta, confira que o número `yt_0036` está livre em `videos_longos/`. Se não estiver, pare e reporte.

**Fase:** só o **preview visual silencioso** do vídeo inteiro, em 960×540 a 15 fps (padrão do AGENTS.md para iterar). O render não tem limite de tempo: o Kaio liberou render sem economia e 3D onde a câmera ajuda. Não gerar voz, SRT, master, 1080p nem entrega. Não fazer commit nem push.

Este handoff é autocontido. Tudo o que você precisa está nele e no zip `yt0036_handoff_v1_completo.zip`:
- `yt_0036_quadros_alvo_v1/` traz os **16 quadros-alvo** (1920×1080), a `00_folha_contato_v2.jpg` e os geradores:
  - `sb36.html` (Canvas + KaTeX, `?k=<chave>`) gera os quadros completos. Abra-o com as fontes, `logo_crop.png`, `katex/`, `r3d_obl.png` e `r3d_pts.js` do lado. Chaves: `h1 h2 a1 b11 b21 b31 b33 b41 b42 b42_3d b43 b52 b53 b62 b63 s2`. As funções `vista(ox, oy, s)` (origem do gráfico em px e px por unidade), `P(x, y)`, `celula()`, `mapT` (φ do trapézio) e `mapC` (φ curva) dão a geometria exata de cada alvo.
  - `c3d36.html` (Three.js r128, `?k=obl` ou `?k=topo`) é a **cena 3D de referência**: geometria, câmera oblíqua, vista de cima ortográfica, cores e a função `proj()`, que dá os pontos de tela em px. Ao lado estão `r3d_obl.png`, `r3d_topo.png`, os pontos em `r3d_pts.json` e o `three.min.js`. **Porte essa cena para a unidade** (§2.2): ela é o modelo exato, não uma inspiração.
  - `shot.js` e `r3d.js` são os scripts Playwright que geraram os PNGs. Servem só de referência.
- `yt_0036_narracao_v1.md` é a **narração** (3.614 palavras ≈ 20:17 de fala), por âncora, com a **Tela** e os **Gatilhos** de cada âncora, mais a tabela de leitura dos símbolos (Anexo B). É ela que dá os tempos e as frases de disparo. A mesma narração está no Anexo A deste handoff. Todos os gatilhos foram conferidos contra o texto da fala.
- `verificacao/verifica_calc3_34t1_sympy.py` e a saída dele somam **41 checagens, todas `True`**. Todos os números da tela saem dali.
- `calculo3_34t1_jacobiano_mudanca_variaveis_proposta_v2.md` é a proposta aprovada, só para consulta (figuras D1–D19 no §1, a CONTA INTEIRA C1–C17 no §3.1, o papel de cada hipótese no §3.2). Onde ela e este handoff divergirem, vale o handoff.

A matemática, o roteiro, a narração e os textos vêm da proposta v2, que o Kaio aprovou para o handoff. Não rediscuta. Se encontrar uma inconsistência objetiva, reporte antes de mudar.

**Regras da série (Kaio):**
- **Figura:** toda definição ou enunciado formal aparece com a sua figura própria (D1–D19).
- **Origem:** todo símbolo nasce do desenho, por `TransformFromCopy` do objeto para a fórmula ou pela caneta. Nada aparece pronto.
- **CONTA INTEIRA (regra permanente):** a escada completa, do básico ao avançado. Primitiva com colchete `[G]ₐᵇ` → `G(b) − G(a)` com os valores substituídos → número; o comprimento da fatia como `SAÍDA − ENTRADA`; cada derivada parcial escrita antes de entrar na matriz; nada de "dá" nem seta pulando degrau. O texto exato da coluna, linha a linha, está no §3.5 (C1–C17). A narração lê cada degrau.
- **Álgebra passo a passo:** a fórmula-mãe vem antes do número; cada valor voa da fonte; cada passo é um `TransformByGlyphMap` com mapa explícito; não há linha órfã começando por "=".
- **"Sensacional" quer dizer clareza.** Nada de partícula, brilho, sombra, névoa, contorno em seta, luz que lava a cor ou câmera girando sem motivo.

**Lições dos EP. 06 a 10, já incorporadas aqui** (não as repita):
- MF-Tools de verdade, sem `mapa_glifos` próprio com `FadeIn`;
- nenhum bloco abrindo vazio;
- palco parado medido só no palco;
- R5 testado também durante as animações;
- frase portuguesa sempre em Space Grotesk, nunca em serifa dentro de `MathTex` (vários alvos ainda têm `\text{…}` em serifa: o §3.2 diz como trocar);
- `\dfrac` sempre (os alvos usam `\tfrac` em vários lugares: troque todos);
- cartão do próximo vídeo por ≥ 8 s.

**A imagem-mãe deste vídeo:** a **grade de u, v desenhada por cima do papel de x, y**, com uma célula acesa no estilo do quadradinho do EP. 03 (chapa `#663A4C`, malha `#FFB3BC`). A célula é o fio condutor: na régua ela é um segmento que estica (fator 2); no caso linear vira paralelogramo e todas esticam igual (fator 5); no caso curvo cada uma estica de um jeito (4u² + 4v²), mas de perto vira paralelogramo; no trapézio cada uma encolhe pela metade (fator 1/2). A frase de tela que resume tudo: `JACOBIANO = FATOR LOCAL DE ÁREA` e `dx dy = |J| du dv`.

---

## 0. O que entregar

1. A unidade nova, com:
   - `ficha.md` (§1);
   - `cena.py` e uma seção `sec_*.py` por bloco (H, A, B1 … B8, S);
   - `threejs/`, com a cena 3D, o renderizador por quadro e os pedidos (§2.2).
2. O preview do vídeo inteiro, `renders/v1/yt_0036_preview_v1_540p15.mp4`, com a duração da narração (§6). Junto, `duracoes_estimadas.json`.
3. A prancha **render × alvo** `renders/v1/qa/comparacao_v1.jpg`. Ela tem uma linha por quadro-alvo, com o still do render no gatilho ao lado do alvo, para os 16 alvos.
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
serie_publica: CÁLCULO III · EP. 11
titulo: Jacobiano e mudança de variáveis
disciplina: Cálculo III
modulo: 3.4 Mudança de variáveis na integral dupla — o docs/mapa_curricular.md do repositório ainda usa a numeração antiga
bloco: 3.4-T1
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, cap. 4 (§4.1 Preliminares; §4.2 teorema e Exemplo 1); Stewart, seção de mudança de variáveis em integrais múltiplas (só na descrição do YouTube; nada de livro na tela além do "como no livro" da fala)
unidades: sem unidade (matemática pura)
solido_3d: nenhum do arsenal Blender (a única peça 3D, o produto vetorial em pé sobre um paralelogramo, é feita direto em Three.js)
3d_threejs: cena1 = o produto vetorial em pé (B4-2): o paralelogramo das setas ∂φ/∂u Δu e ∂φ/∂v Δv no chão, o vetor (∂φ/∂u Δu) ∧ (∂φ/∂v Δv) subindo em k com altura = área; decolagem da vista de cima (= o 2D do zoom), câmera oblíqua parada, pouso de volta na vista de cima
duracao_alvo: ≈ 21 min (narração v1: 3.614 palavras ≈ 20:17)
```

## 2. Base de código

### 2.1 Manim

- **Antes de começar:**
  - leia `docs/estado_atual.md`;
  - rode `verificacao/verifica_calc3_34t1_sympy.py` com o Python da `.venv` (as 41 linhas devem dar `True`). Se faltar sympy ou scipy, não instale nada: diga no relatório e siga.
- **Copie, não importe.** Copie o kit da unidade mais recente da série de Cálculo III que estiver no seu checkout, nesta ordem de preferência: `yt_0035_*`, `yt_0034_*`, `yt_0033_*`. Do kit vêm:
  - `kit.py` e `render.sh`;
  - o canto de duas linhas e `placa_min`;
  - a caneta (`TC`/`TX`), `painel`, `mixl`, o sublinhado de leitura, `tiraV`/`tiraH` com os pontos de entrada e saída;
  - o quadradinho do EP. 03 (chapa + malha), se o kit tiver; senão, faça a função `celula(F, u0, u1, v0, v1, n=4)` como a do `sb36.html` (a borda da imagem amostrada em 24 pontos por lado, a malha n × n desenhada pela imagem das retas internas).

  Se essas unidades não estiverem no seu checkout, use a mais recente que houver. Este handoff não depende delas. Não altere as outras unidades.
- **Fundo:**
  - Gráficos: violeta liso `#18143A → #0F0C26` na câmera, mais a grade `papel(ax)` de `assets/calculo/papel.py`, que nasce dos eixos de cada palco ou painel (quadradinho de 0,25 da unidade do gráfico, sem linhas grossas). **No layout B cada plano tem o seu `papel(ax, area=…)`**, com a escala própria (§3.1). No zoom do B4-2 o passo é 0,05 (`passo=0.05`), como no alvo 09.
  - Cena 3D: só o violeta liso, sem a grade do Manim (o chão da cena tem a grade dela, ver §2.2).
  - Cartões sem gráfico (H2, A1, S1, o cartão do S2, os dois cartões do B8): só o violeta liso.
- Render por bloco (`render.sh <Classe>`), depois concatene.
- **Transformações de grade:** a grade de u, v que se inclina (B3-1) é um `VGroup` de retas transformado por `ApplyMatrix([[2, 1], [1, 3]])` num movimento só; a malha que curva (B4-1) é um `ApplyPointwiseFunction` com φ(u, v) = (u² − v², 2uv) sobre retas pré-subdivididas (≥ 40 pontos por reta, para a curva sair lisa); a dobra do B5-3 é um `ApplyPointwiseFunction` com φ(u, v) = (u², v) sobre a metade esquerda, num movimento.
- **Sem economia artificial**, mas sem updater à toa: a célula de Δ que encolhe no B4-3 é um `ValueTracker` só, ligado à célula, ao paralelogramo e ao zoom; a tira deitada do B5-4 é estática (uma posição) e só a cor da entrada e da saída acende.
- Limpe da cena o que saiu da tela. Não deixe nada invisível acumulando.

### 2.2 Three.js (o pipeline da série)

- **Copie o pipeline** da unidade de Cálculo mais recente que tiver `threejs/` (yt_0035, se estiver no checkout; senão yt_0034, yt_0033 ou yt_0026). Vêm `r3d.js`, `package.json` (playwright-core), `cena3d/three.min.js` (r128) e o esquema de pedidos:
  1. A passagem seca do Manim grava `pedidos3d/<LOTE>.json` com `{cena: [[quadro, estado], …]}`.
  2. `r3d.js` abre `cena3d/<cena>.html`, chama `window.setEstado(estado)` quadro a quadro e grava os PNGs com alfa e o `pontos.json`.
  3. O Manim cola os PNGs como `ImageMobject` em tela cheia e prende os rótulos nos pontos.
- **Porte a cena de `c3d36.html`** para `threejs/cena3d/cena1.html`. Vêm de lá:
  - **Coordenadas locais do zoom:** origem no canto M = φ(0,75; 0,5) = (0,3125; 0,75), unidade = Δ = 0,1 do plano x, y **nos três eixos**. Nessas coordenadas:
    - `w1 = ∂φ/∂u · Δu = (2u, 2v) · 0,1 = (0,15; 0,10)` → local **(1,5; 1; 0)**, laranja `#FF9440`;
    - `w2 = ∂φ/∂v · Δv = (−2v, 2u) · 0,1 = (−0,10; 0,15)` → local **(−1; 1,5; 0)**, verde-água `#2EE6A6`;
    - `w1 ∧ w2 = (0, 0, 1,5 · 1,5 − (−1) · 1) = (0, 0, 3,25)` → **altura 3,25 = área do paralelogramo (3,25 unidades²)**, lima `#C6F26B`.

    Em unidades de x, y, essa área é 3,25 · 0,1 · 0,1 = 0,0325 = |J(M)| Δu Δv. **As setas e o vetor estão na mesma escala, sem fator de desenho**: é isso que faz a altura ser a área (era o erro do esboço da v1, que usava as derivadas sozinhas e uma altura encolhida).
  - O chão: grade de passo 0,5 local (= 0,05 de x, y), tubos finos `#2B2558`; as linhas de ξ deslocadas 0,125 para cair na grade absoluta de x (x_M = 0,3125 não é múltiplo de 0,05), como no `c3d36.html`. O paralelogramo com o preenchimento `chapa` misturado ao fundo (95 %) e a borda `malha` `#FFB3BC`; as duas setas e o vetor como em `seta()`.
  - **Câmera oblíqua (`k=obl`, alvo 10):** `PerspectiveCamera(22°)`, `up = +z`, posição `(−7,2; −11; 7,4)`, alvo `(0,25; 1,25; 1,45)`, `setViewOffset(W, H, 960 − 640, 540 − 560, W, H)`.
  - **Vista de cima (`k=topo`, = o 2D do alvo 09):** `OrthographicCamera` com M em **(330, 860) px** e **190 px por unidade local** (= 1900 px por unidade de x, y), x para a direita, y para cima. Os pontos exportados batem com o alvo 09: `M (330, 860)`, `w1 (615, 670)`, `w2 (140, 575)`, `C (425, 385)`.
- **Estados da cena 1** (nomes sugeridos; a animação entre eles é sua):

  | estado | o que anima |
  |---|---|
  | `cam` 0→1 | câmera da vista de cima ortográfica (0) para a oblíqua (1). Faça em perspectiva com o fov abrindo a partir de um dolly-zoom (a câmera começa longe com fov pequeno, quase ortográfica, e chega na oblíqua), ≈ 2,5 s, começo e fim suaves. No quadro 0 a diferença para a vista ortográfica tem de ficar ≤ 2 px |
  | `sobe` 0→1 | o vetor lima cresce de altura 0 até 3,25, a partir de M (≈ 1,5 s) |
  | `cam` 1→0 | o pouso: a mesma trajetória de volta, terminando na `OrthographicCamera` exata |

- **Decolagem e pouso (a passagem 2D ↔ 3D, assinatura da série):**
  - **Antes da decolagem**, no 2D: a célula curva `MNPQ` vira o paralelogramo das duas setas (`ReplacementTransform`, um movimento, no gatilho "o paralelogramo dessas duas setas"). Os pontos N, P, Q e os rótulos `ARCO MN ≅ …` e `ARCO MQ ≅ …` saem junto. O que fica no 2D (grade 0,05, paralelogramo cheio, as duas setas, o ponto M) é exatamente o `k=topo`.
  - **No quadro da decolagem** (gatilho "Põe as duas setas"), o PNG do `cam = 0` entra por cima e o 2D sai no mesmo quadro. **Alinhamento ≤ 2 px** entre o contorno do paralelogramo 2D e o do PNG, medido e registrado.
  - **No pouso** (gatilho "vista de cima"), o vetor lima, que aponta para a câmera, vira um ponto sob M; no último quadro (`OrthographicCamera`) o 2D entra por cima no mesmo quadro e o PNG sai. Mesmo alinhamento ≤ 2 px.
  - O B4-2 **tem de funcionar só com o 2D** se o 3D atrasar o preview: nesse caso, o vetor é desenhado em perspectiva cavaleira 2D, com a mesma geometria do alvo 10. Entregue assim e reporte.
- **Estilo 3D da série:** opaco e sem luz (`MeshBasicMaterial`); sem sombra, névoa, brilho ou transparência; `outputEncoding` linear e antialias ligado; fundo transparente (o violeta liso vem do Manim).
- **Rótulos são do Manim**, presos aos pontos do `pontos.json` do mesmo quadro. Quando a câmera se move, o rótulo anda junto. Alinhamento ≤ 2 px. Pontos já exportados: `M`, `w1`, `w2`, `C`, `topo` (a ponta do vetor), `w1_meio`, `w2_meio`.
  - Rótulo de `w1`: `\dfrac{∂φ}{∂u} Δu` (laranja), à direita da ponta; de `w2`: `\dfrac{∂φ}{∂v} Δv` (verde-água), à esquerda da ponta; os dois com `placa_min` (cruzam a grade do chão).
  - Na ponta do vetor: `\vec k` à esquerda e, ligado por um tracejado lima, `(\dfrac{∂φ}{∂u} Δu) ∧ (\dfrac{∂φ}{∂v} Δv)` à direita (alvo 10).
- **Câmera:**
  - parada na oblíqua enquanto o vetor sobe e enquanto as fórmulas são escritas;
  - um movimento por ideia (decolagem, pouso); nada de órbita só para "dar movimento";
  - **a câmera nunca se mexe enquanto uma fórmula está sendo escrita**;
  - nada do 3D passa de x = 1090 px (a coluna começa em 1120 nos quadros 3D: no alvo 10 ela começa em 1180).

## 3. Sistema visual

### 3.1 Layouts e escala

`vista(ox, oy, s)` = a origem do gráfico em (ox, oy) px a 1080p e 1 unidade = s px. Conversão para o Manim: x_m = (x_px − 960)/135; y_m = (540 − y_px)/135.

| layout | geometria a 1080p (dos alvos) | blocos |
|---|---|---|
| **B · dois planos** (novo neste módulo) | Plano u, v à esquerda, plano x, y à direita, cada um com o seu `papel(ax)`; a seta curva `φ` por cima, entre os dois (alvos 01, 05, 06, 07, 08, 13, 14). **H1 e B6-2:** u, v `vista(400, 640, 120)`; x, y `vista(1180, 330, 175)`; a faixa de fórmula embaixo em y ≈ 985. **B2-1:** u, v `vista(160, 790, 540)`; x, y `vista(1300, 820, 265)`; faixa embaixo em y ≈ 1000. **B3-1:** u, v `vista(130, 700, 260)`; x, y `vista(800, 900, 160)`; coluna em x = 1400. **B3-3:** u, v `vista(180, 720, 360)`; x, y `vista(940, 560, 400)`; coluna centrada em x = 1700. **B4-1:** u, v `vista(170, 760, 480)`; x, y `vista(1290, 860, 330)`. **B5-3:** u, v `vista(360, 700, 240)`; x, y `vista(1020, 700, 300)`; coluna em x = 1480 | H1, B2, B3-1, B3-3, B4-1, B5-1, B5-3, B6-1, B6-2 |
| **A · palco + fórmulas** | Coluna de fórmulas alinhada à esquerda em **x = 1120**. Exceções dos alvos: no **B4-3** a cadeia C6 fica à esquerda (x = 80–100) e C5 com a tabela em x = 1120; no **B5-2** o enunciado fica à esquerda (x = 110) e as seis miniaturas à direita (x ≥ 1460); no **B6-3** e no **B7** o plano fica à esquerda e a coluna em **x = 760**. Palcos: **réguas** do B1-1 com t e x em `vista(160, 360, 400)` e `vista(160, 640, 400)`; **zoom** do B4-2 com M em (330, 860) e 1 = 1900 px; **plano u, v** do B6-3 em `vista(330, 700, 150)`; região entre parábolas do B5-4 (use `vista(1290, 860, 330)` do B4-1, deslocada para a esquerda até a coluna caber, origem em ≈ (520, 860)) | B1, B3-2, B4-2, B4-3, B5-2, B5-4, B6-3, B6-4, B7 |
| **3D · palco + fórmulas** | O 3D ocupa a esquerda (alvo 10). A coluna começa em x = 1180 | B4-2 |
| **C · cartões** | H2: a célula inclinada grande em `vista(520, 560, 300)` à esquerda, as duas linhas da tese em x = 1140. A1: padrão do canal. B8: dois cartões de traço GEO lado a lado (≈ 820 × 640 cada, em x = 100 e x = 1000, topo em y = 220). S1: `dx dy = |J| du dv` grande no topo e quatro caixas 2 × 2. S2: o disco em `vista(470, 560, 330)` e o cartão do próximo vídeo à direita (x ≥ 1080) | H2, A1, B8, S1, S2 |

### 3.2 Regras (as da série + as lições dos EP. 06 a 10)

- **R1 · Clareira:** nenhum rótulo sobre ponto, aresta, linha da grade ou número; o rótulo sai para o lado.
- **R2 · Placa:** todo rótulo solto sobre o desenho ou sobre o 3D usa `placa_min`.
- **R3:** fórmula nova nunca nasce sobre fórmula velha; a coluna limpa antes.
- **R4:** rótulo junto do objeto que ele nomeia; **o rótulo sai junto com o seu objeto** (nada de legenda órfã depois de uma transição).
- **R5:** QA automático de sobreposição, amostrado a cada 0,5 s **inclusive durante as animações** (§8).
- **R6:** nada sai da moldura do seu painel ou cartão; no layout B nada de um plano invade o outro; nada do 3D invade a coluna.
- **R-texto:**
  - **Palavra é Space Grotesk** (`Text`, maiúsculas); matemática é `MathTex`.
  - Uma linha mista é `Text` + `MathTex` lado a lado, com respiro ≥ 0,15 (`mixl()`).
  - **Nenhuma frase portuguesa dentro de `MathTex`.** Os alvos ainda têm `\text{…}` em serifa; troque assim:
    - alvo 05: `φ DE CLASSE C¹ NO ABERTO Ω` → `Text("φ DE CLASSE")` + `MathTex("C^1")` + `Text("NO ABERTO")` + `MathTex("\Omega")`; `área de B = ?` → `Text("ÁREA DE")` + `MathTex("B = ?")`;
    - alvo 06: `CAIXA:` e `ÁREA =` são `Text`;
    - alvo 09: `arco MN ≅ …` → `Text("ARCO")` + `MathTex("MN \cong …")`; `área de B ≅ …` → `Text("ÁREA DE")` + `MathTex("B \cong …")`;
    - alvo 11: `área de B ≅ |J| Δu Δv` idem; `JACOBIANO`, `FATOR LOCAL DE ÁREA`, `EXATA`, `RAZÃO` são `Text`;
    - alvo 12: cada hipótese é uma linha mista (ex.: `Text("φ INVERSÍVEL NO INTERIOR DE")` + `MathTex("B_{uv}")`); `TEOREMA (MUDANÇA DE VARIÁVEIS NA INTEGRAL DUPLA)` vira `Text("TEOREMA")` em lima, sem o parêntese; `DETERMINAR` é `Text`;
    - alvo 13: `ÁREA DA IMAGEM = 1` → `Text("ÁREA DA IMAGEM")` + `MathTex("= 1")`;
    - alvo 01: `ÁREA ?` e `ÁREA 3/2` → `Text("ÁREA")` + `MathTex("?")` ou `MathTex("\dfrac{3}{2}")`.
  - Cada legenda tem no máximo 6 palavras e pelo menos 26 px a 1080p. As legendas de apoio dos alvos em 20–24 px (`EM PÉ E DEITADO`, `3 CÉLULAS`, `ANTI-HORÁRIO`, `GRANDE`, `PEQUENA`, `M = φ(0,75; 0,5)`, os títulos das miniaturas do B5-2, `FATOR DE COMPRIMENTO`) sobem para 26 px.
  - Exceções de comprimento (a fala sustenta): `JACOBIANO = FATOR LOCAL DE ÁREA`, `ALTURA = ÁREA DO PARALELOGRAMO`, `O FATOR MUDA DE PONTO PARA PONTO`, `SOBREPOSIÇÃO: CONTOU DUAS VEZES`, `QUAL É O FATOR DA GRADE DE CÍRCULOS?` (duas linhas no cartão).
- **Fração:** sempre `\dfrac`, com o glifo da fração ≥ 26 px a 1080p. Os alvos usam `\tfrac` em muitos lugares (`½` das células, `1/2` do chip, as frações das colunas do B3-3 e do B6, os limites `4/3`): **troque todos por `\dfrac`**. Nenhum rótulo girado (os rótulos inclinados das bordas no alvo 01 ficam horizontais, com placa). `grep -n tfrac` = 0.
- **Glifos:** zero em legenda vai por extenso (`ZERO`), porque o 0 do Space Grotesk parece O. Zero como **valor** (limites, coordenadas, `J(0, 0) = 0`) é `MathTex`. Nos números com vírgula decimal, use `{,}` no LaTeX (`0{,}75`, `3{,}25`, `1{,}44`).
- **Sublinhado de leitura:** quando a voz lê um símbolo (Anexo B: "o jacobiano de xis, ípsilon em relação a u, vê", "produto vetorial", "a derivada parcial de fi em relação a u", "bê u vê", "o módulo de menos um meio", "gê linha de tê"), um sublinhado fino aparece sob ele no gatilho falado e sai. Não é pulso nem brilho.
- **Um movimento por ideia, uma vez.** Uma figura nova nasce da velha (`ReplacementTransform`) e nunca pisca. A única "pulsação" do vídeo é a do H2 ("estica ou encolhe"): a célula cresce e volta, uma vez, sem brilho.
- **Nenhum bloco abre vazio:**
  - a linha 2 do canto está na tela desde o primeiro quadro de cada bloco;
  - a figura do bloco anterior fica até a nova nascer dela, ou a nova começa a entrar em ≤ 0,5 s;
  - palco vazio por mais de 0,5 s: zero ocorrências.
- **Palco parado:**
  - Medida: trecho em que menos de 40 px do **palco** (máscara sem a coluna e sem o canto, a 960×540) mudam mais de 8 níveis ao longo de 3 s.
  - Limite de 3 s. De 3 a 5 s só é aceito se a voz estiver lendo o que está no palco, com o motivo no relatório. Acima de 5 s: zero.
  - Este vídeo tem muita conta na coluna (B4-3, B5-2, B6-3): enquanto a coluna escreve, o palco acompanha (o termo da vez acende no desenho com o sublinhado de leitura, a derivada voa da fórmula de x ou de y, o limite voa do plano u, v). Se a fala continua e a cena acabou, o próximo passo entra mais cedo.
- **Pontos e marcas só os do alvo:** os cantos M, N, P, Q (B2-1, B4-2), os cantos do trapézio com as coordenadas (B6-2), o ponto branco (ūᵢ, v̄ⱼ) e a sua imagem (B5-1), os pontos de entrada (azul-claro) e saída (coral) das tiras. Nenhum ponto de debug.
- **`PAUSE E TENTE`:** selo âmbar ao lado do enunciado do B7, da fala "Pausa o vídeo e tenta" até "Pronto?" (≥ 3 s).
- **Chip do 1/2:** no B3-3, o `1/2` de `ÁREA = |−1/2| = 1/2` ganha a cor lima e voa para o canto superior direito, abaixo do logo, dentro de uma moldura lima fina: `|J| = 1/2` (alvo 15: moldura de 240 × 70 px com o canto em (1560, 150)). Ele fica lá, discreto, do B4 ao B6, e no B6-1 desce e encaixa no `J = −1/2` da coluna. R5 vale para ele.

### 3.3 Cores

| Papel | Cor |
|---|---|
| f, o integrando, `e^{u/v}`, `cos`, `sen` | ciano `#35D9FF` |
| x, `dx`, os números de x nos eixos | âmbar `#FFC24D` |
| y, `dy`, os números de y nos eixos | magenta `#EA63FF` |
| **u**, retas de u constante, ∂φ/∂u, `Δu`, `du`, o lado Δu | **laranja `#FF9440`** |
| **v**, retas de v constante, ∂φ/∂v, `Δv`, `dv`, o lado Δv | **verde-água `#2EE6A6`** |
| **\|J\|**, o fator de área, o vetor ∧, o chip `\|J\| = 1/2`, `JACOBIANO = FATOR LOCAL DE ÁREA`, a moldura da definição | **lima `#C6F26B`** |
| A célula da grade (A, Rᵢⱼ, a célula acesa) | chapa `#663A4C` + malha `#FFB3BC` |
| Células coloridas pelo tamanho (B4-1) | escala GEO escuro → lima (pequenas perto da origem, grandes perto de (0, 2)) |
| Curva de entrada / de saída da fatia e os pontos | azul-claro `#7FB2FF` / coral `#FF7A8A` |
| Região B, caixas, cartões, réguas, a caixa 3 × 4, legendas secundárias | GEO `#B8C4DA` (região a ≈ 18 % sobre o fundo) |
| Dobra, determinante negativo, `TRAVA`, `VIROU DE COSTAS`, `2 ≠ 1`, a hipótese que falha | ALERTA `#FF5D5D` |
| Pontos de amostra (ūᵢ, v̄ⱼ), (x̄ᵢ, ȳⱼ), a curva γ, a seta γ′(t) Δt | branco `#F5F7FF` |
| ✓ | menta `#8CFFD2` |
| Na dobra (B5-3): metade esquerda / direita | laranja-claro (`#FF9440` a 45 %) / verde-água-claro (`#2EE6A6` a 45 %) |

- Operadores (∫, ∬, ∧, ≅, ⇒, det, | |, =) ficam em branco, e a cor vai na grandeza.
- **Derivadas parciais:** o numerador na cor da função (x âmbar, y magenta; φ branco) e o denominador na cor da variável (u laranja, v verde-água). Nas casas da matriz, `x_u` tem o x âmbar e o u laranja.
- **Limites de dentro:** o limite inteiro na cor da curva (azul-claro se é por onde a fatia entra, coral se é por onde sai), e só o u, v, x ou y dentro dele na cor da variável.
- O `1/2` do trapézio é lima desde o H1 (`1/2 ?` na faixa de baixo).

### 3.4 Álgebra

- **Caneta** em toda fórmula nova: traço finíssimo (~0,7), glifo a glifo, da esquerda para a direita, preenchendo na cor da grandeza, sem flash e sem preview do destino.
- Um termo que nasce no desenho **voa** para a fórmula (`TransformFromCopy`, em arco). No 3D, ele voa a partir do ponto projetado. **Os voos obrigatórios deste vídeo:**
  - **H1:** `x + y` e `x − y` do expoente acendem e voam para os rótulos `u` e `v` das duas famílias de retas; o trapézio do papel **voa** para o plano u, v e se endireita (um movimento); o `3` de `3 CÉLULAS` e o `3/2` de `ÁREA 3/2` nascem da contagem das células, não da caneta.
  - **B1-1:** o segmento `Δt` desce pelas linhas finas e vira `Δx`; o comprimento `2` da régua de x voa para `dx = 2 dt`; os limites `0` e `1` voam das pontas da régua de t para a integral.
  - **B1-2:** a seta `γ′(t) Δt` nasce no ponto γ(t) e o `Δs` nasce do arco aceso.
  - **B3-1:** as setas `(2, 1)` e `(1, 3)` voam para as colunas da matriz; cada pedaço da caixa, ao sair, leva a sua área (`2 · 1/2`, `1 · 3/2`, `1 · 1`) para a linha correspondente de C2.
  - **B3-2:** as letras `a, c` e `b, d` das pontas das setas voam para a matriz.
  - **B3-3:** as colunas `(1/2, 1/2)` e `(1/2, −1/2)` voam das pontas das setas do losango; o `1/2` vira o chip lima.
  - **B4-2:** as setas `∂φ/∂u Δu` e `∂φ/∂v Δv` nascem dos lados MN e MQ; no 3D, a altura do vetor voa da ponta (`topo`) para `ALTURA = ÁREA DO PARALELOGRAMO`.
  - **B4-3:** as quatro derivadas voam das fórmulas `x = u² − v²` e `y = 2uv` para as casas da matriz; o `0,75` e o `0,5` voam do ponto M para `4 · 0,5625 + 4 · 0,25`; cada linha da tabela nasce da célula da vez.
  - **B5-1:** `α(Bᵢⱼ)` voa da célula da direita; `Δuᵢ Δvⱼ`, da célula da esquerda; `φ(ūᵢ, v̄ⱼ)` nasce da seta entre o ponto branco e a sua imagem.
  - **B5-3:** o `2` de `∬|J| = 2` e o `1` de `ÁREA DA IMAGEM = 1` ficam lado a lado e viram `2 ≠ 1`.
  - **B5-4:** as duas parábolas voam das bordas para C9 (linhas 1 e 2); `SAÍDA − ENTRADA` nasce das duas pontas da tira.
  - **B6-1:** `x + y` e `x − y` voam do expoente para C10; o `−1/2` encaixa no chip lima, que desce.
  - **B6-2:** cada lado do trapézio acende com a equação e **voa** para o plano u, v, onde vira `u = v` (coral, saída), `v = 2`, `u = −v` (azul-claro, entrada), `v = 1`; os quatro cantos levam as coordenadas.
  - **B6-3:** o `u` e o `v` do expoente voam de C10; o `1/2` voa do chip; os limites `−v`, `v`, `1`, `2` voam do plano u, v.
  - **B6-4:** o `3` voa das 3 células acesas do plano u, v; o `2 · 2/2` e o `1 · 1/2` voam dos dois triângulos do papel.
  - **B7:** as quatro bordas voam do trapézio do livro para C17 linha 3.
- **MF-Tools de verdade:**
  - `from MF_Tools import TransformByGlyphMap` (1.4.9), com `MathTex` de string única nos dois lados e mapa explícito.
  - O glifo que sai usa `auto_fade` (ou entra no mapa com destino vazio).
  - O glifo que **entra** nunca usa `FadeIn`: fica fora do mapa e é escrito com a caneta logo depois, ou voa da fonte.
  - Não use função própria de mapa de glifos.
  - `show_indices` só no desenvolvimento.
- **Glyph maps obrigatórios** (17): um para cada passagem `→` da CONTA INTEIRA do §3.5.
  1. C1 (B1-1): `[x²/2]₀²` → `2²/2 − 0²/2` → `2`; e `∫₀¹ (2t) · 2 dt` → `4 ∫₀¹ t dt` → `4 [t²/2]₀¹` → `4 · (1/2 − 0)` → `2`.
  2. C2 (B3-1): `12 − 2 − 3 − 2` → `5`.
  3. C3 (B3-2): o produto aberto; `ac` e `−ac` acendem juntos e somem; `bd` e `−bd` idem; `bc − 2bc` → `−bc`; `ad − bc` → `det [a b; c d]`.
  4. C4 (B3-3): `(1/2)(−1/2) − (1/2)(1/2)` → `−1/4 − 1/4` → `−1/2`; `|−1/2|` → `1/2`.
  5. C5 (B4-3): `det [2u −2v; 2v 2u]` → `(2u)(2u) − (−2v)(2v)` → `4u² + 4v²`; `4 · 0,5625 + 4 · 0,25` → `2,25 + 1` → `3,25`.
  6. C6 (B4-2/B4-3): o 3 × 3 → `(x_u y_v − x_v y_u) k` (os termos com i e j acendem e somem) → `det [x_u x_v; y_u y_v] k` (transposta: cada linha vira coluna por mapa explícito) → `‖∂φ/∂u ∧ ∂φ/∂v‖ = |∂(x, y)/∂(u, v)|`. E no 3D: `‖(∂φ/∂u Δu) ∧ (∂φ/∂v Δv)‖` → `Δu Δv ‖∂φ/∂u ∧ ∂φ/∂v‖` (os deltas saem dos parênteses e vão para a frente).
  7. C7 (B5-1): ① → ② (o `α(Bᵢⱼ)` vira `|J(ūᵢ, v̄ⱼ)| Δuᵢ Δvⱼ`, e o `(x̄ᵢ, ȳⱼ)` vira `φ(ūᵢ, v̄ⱼ)`) → ③ (cada símbolo da soma vai para o seu lugar na integral: `Σᵢ Σⱼ` → `∬_{B_uv}`, `ūᵢ, v̄ⱼ` → `u, v`, `Δuᵢ Δvⱼ` → `du dv`).
  8. C8 (B5-4): `[4u³/3 + 4v² u]₀¹` → `4/3 + 4v²`; `[4v/3 + 4v³/3]₀¹` → `4/3 + 4/3` → `8/3`.
  9. C9 (B5-4): `x = 1 − v², y = 2v` → `v = y/2` → `x = 1 − y²/4` (e a outra borda); `(1 − y²/4) − (y²/4 − 1)` → `2 − y²/2`; `[2y − y³/6]₀²` → `4 − 8/6` → `4 − 4/3` → `8/3`.
  10. C10 (B6-1): `u + v = 2x` → `x = (u + v)/2`; `u − v = 2y` → `y = (u − v)/2` (o 2 atravessa a igualdade).
  11. C11 (B6-1): `(1/2)(−1/2) − (1/2)(1/2)` → `−1/4 − 1/4` → `−1/2`; a conferência `1 · (−1) − 1 · 1` → `−2` → `(−2) · (−1/2) = 1`.
  12. C12 (B6-2): `y = 0: u = x, v = x` → `u = v` (e as outras três bordas).
  13. C13 → C14 (B6-3): `[v e^{u/v}]_{u=−v}^{u=v}` → `v e^{v/v} − v e^{−v/v}` → `v e − v e^{−1}` → `v (e − 1/e)`.
  14. C15 (B6-3): `(1/2) ∫₁² v (e − 1/e) dv` → `(1/2)(e − 1/e) ∫₁² v dv` (a constante sai); `[v²/2]₁²` → `4/2 − 1/2` → `3/2`; `(1/2)(e − 1/e)(3/2)` → `(3/4)(e − 1/e)` → `≈ 1,763` (o exato primeiro).
  15. C16 (B6-4): `∫₁² (v − (−v)) dv` → `∫₁² 2v dv` → `[v²]₁²` → `4 − 1` → `3`; `3 · 1/2` → `3/2`; `2 · 2/2 − 1 · 1/2` → `2 − 1/2` → `3/2`.
  16. C17 (B7): `(1/2)(1/2) − (1/2)(−1/2)` → `1/4 + 1/4` → `1/2`; `(1/sen v)[sen u]_{−v}^{v}` → `(sen v − sen(−v))/sen v` → `2 sen v / sen v` → `2`; `(1/2) · 2 · (2 − 1)` → `1`.
  17. H1: `∬_B e^{(x+y)/(x−y)} dA` → `= 1/2 ? ∫₁² ∫_{−v}^{v} e^{u/v} du dv` (o `x + y` vira `u`, o `x − y` vira `v`, o `dA` vira `du dv`; o `1/2 ?` é escrito com a caneta depois, em lima com o `?` ALERTA).
- **Tamanhos:** fórmula principal de 40–52 px no alvo; secundária de 32–40 px; índice ≥ 22 px; nada menor que 26 px fora dos índices. Algumas linhas dos alvos estão em 30–32 px para caber (B3-3, B4-3, B6-3): mantenha ≥ 30 px.
- **Arredondamento na tela:** o exato vem antes do decimal e o decimal sempre com `≈`: `(3/4)(e − 1/e) ≈ 1,763`. Os decimais da tabela do B4-3 vêm com `≈` no cabeçalho (`EXATA ≈`), e a razão com duas casas.

### 3.5 CONTA INTEIRA (o texto exato da coluna, linha a linha)

Cada linha entra a caneta ou por glyph map a partir da anterior; nenhum número aparece sem a linha que o produz. Cor: x âmbar, y magenta, u laranja, v verde-água, |J| lima, f ciano, entrada azul-claro, saída coral, operadores brancos.

**C1 · régua (B1-1)**
1. `∫₀² x dx = [x²/2]₀² = 2²/2 − 0²/2 = 2`
2. `x = 2t ⇒ dx = 2 dt` · `x = 0 ⇒ t = 0` · `x = 2 ⇒ t = 1`
3. `∫₀² x dx = ∫₀¹ (2t) · 2 dt = 4 ∫₀¹ t dt = 4 [t²/2]₀¹ = 4 · (1/2 − 0) = 2 ✓`
4. `x = g(t) ⇒ Δx ≅ g′(t) Δt` · legenda `FATOR DE COMPRIMENTO: |g′(t)|`

**C2 · área do paralelogramo pela figura (B3-1)**
1. `CAIXA: (2 + 1)(1 + 3) = 3 · 4 = 12`
2. `− 2 · (2 · 1)/2 = − 2` (dois triângulos de catetos 2 e 1)
3. `− 2 · (1 · 3)/2 = − 3` (dois triângulos de catetos 1 e 3)
4. `− 2 · (1 · 1) = − 2` (dois retangulinhos 1 × 1)
5. `ÁREA = 12 − 2 − 3 − 2 = 5`

**C3 · a mesma conta com letras (B3-2)**
1. `ÁREA = (a + b)(c + d) − 2 · ac/2 − 2 · bd/2 − 2 · bc`
2. `= ac + ad + bc + bd − ac − bd − 2bc`
3. `= ad + bc − 2bc = ad − bc`
4. `= det [a b; c d]` · `2 · 3 − 1 · 1 = 5 ✓`
5. `CÉLULA Δu × Δv ⇒ ÁREA = 5 Δu Δv` (a palavra `CÉLULA` e `ÁREA` são `Text`) · selo `FATOR CONSTANTE`

**C4 · o sinal (B3-3)**
1. `x = (u + v)/2, y = (u − v)/2` → colunas `(1/2, 1/2)` e `(1/2, −1/2)`
2. `det = (1/2)(−1/2) − (1/2)(1/2) = −1/4 − 1/4 = −1/2`
3. `ÁREA = |−1/2| = 1/2`

**C5 · as derivadas e o jacobiano do caso curvo (B4-3)**
1. `x = u² − v², y = 2uv`
2. `∂x/∂u = 2u` · `∂x/∂v = −2v` · `∂y/∂u = 2v` · `∂y/∂v = 2u`
3. `∂(x, y)/∂(u, v) = det [2u −2v; 2v 2u] = (2u)(2u) − (−2v)(2v) = 4u² + 4v²`
4. `M = (0,75; 0,5): 4 · 0,5625 + 4 · 0,25 = 2,25 + 1 = 3,25`
5. `J(0, 0) = 0` · `J(1, 1) = 8`

**C6 · produto vetorial → jacobiano (B4-2/B4-3)**
1. `∂φ/∂u ∧ ∂φ/∂v = det [i j k; x_u y_u 0; x_v y_v 0]`
2. `= (x_u y_v − x_v y_u) k`
3. `= det [x_u x_v; y_u y_v] k`
4. `‖∂φ/∂u ∧ ∂φ/∂v‖ = |∂(x, y)/∂(u, v)|` (moldura lima, `JACOBIANO` ao lado)
5. `ÁREA DE B ≅ |∂(x, y)/∂(u, v)| Δu Δv` · legenda lima `FATOR LOCAL DE ÁREA`

**Tabela do B4-3** (célula de canto M = (0,75; 0,5), lado Δ; "exata" pela fronteira, sem usar J):

| Δ | EXATA ≈ | \|J(M)\| Δ² | RAZÃO |
|---|---|---|---|
| 0,25 | 0,2917 | 0,2031 | 1,44 |
| 0,1 | 0,03777 | 0,03250 | 1,16 |
| 0,05 | 0,008767 | 0,008125 | 1,08 |
| 0,01 | 0,000330 | 0,000325 | 1,02 |

**C7 · soma de Riemann → fórmula (B5-1)**
1. `∬_B f dx dy ≅ Σᵢ Σⱼ f(x̄ᵢ, ȳⱼ) α(Bᵢⱼ)` ①
2. `α(Bᵢⱼ) ≅ |J(ūᵢ, v̄ⱼ)| Δuᵢ Δvⱼ` · `(x̄ᵢ, ȳⱼ) = φ(ūᵢ, v̄ⱼ)`
3. `≅ Σᵢ Σⱼ f(φ(ūᵢ, v̄ⱼ)) |J(ūᵢ, v̄ⱼ)| Δuᵢ Δvⱼ` ②
4. `→ ∬_{B_uv} f(φ(u, v)) |∂(x, y)/∂(u, v)| du dv` ③

**Teorema (B5-2)**, uma hipótese por linha, numeradas 1 a 6 como no alvo 12, e a conclusão:
1. `φ` de classe `C¹` no aberto `Ω`
2. `B_uv ⊂ Ω` compacto, fronteira de conteúdo nulo
3. `B = φ(B_uv)`, `φ(B̊_uv) = B̊`
4. `φ` inversível no interior de `B_uv`
5. `∂(x, y)/∂(u, v) ≠ 0` no interior de `B_uv`
6. `f` integrável em `B`
- `⇒ ∬_B f(x, y) dx dy = ∬_{B_uv} f(φ(u, v)) |∂(x, y)/∂(u, v)| du dv`
- Quadro-receita: `dx dy = |∂(x, y)/∂(u, v)| du dv` · `DETERMINAR B_uv COM B = φ(B_uv)`

**C8 · área 8/3 com jacobiano (B5-4)**
1. `ÁREA = ∬_{[0,1]²} (4u² + 4v²) du dv`
2. `∫₀¹ (4u² + 4v²) du = [4u³/3 + 4v² u]₀¹ = 4/3 + 4v²`
3. `∫₀¹ (4/3 + 4v²) dv = [4v/3 + 4v³/3]₀¹ = 4/3 + 4/3 = 8/3`

**C9 · área 8/3 sem jacobiano, deitado (B5-4)**
1. `u = 1: x = 1 − v², y = 2v ⇒ v = y/2 ⇒ x = 1 − y²/4` (SAÍDA, coral)
2. `v = 1: x = u² − 1, y = 2u ⇒ u = y/2 ⇒ x = y²/4 − 1` (ENTRADA, azul-claro)
3. `COMPRIMENTO = (1 − y²/4) − (y²/4 − 1) = 2 − y²/2`
4. `∫₀² (2 − y²/2) dy = [2y − y³/6]₀² = 4 − 8/6 = 4 − 4/3 = 8/3 ✓`

**C10 · trapézio: variáveis e inversa (B6-1)**
1. `u = x + y` · `v = x − y`
2. `u + v = 2x ⇒ x = (u + v)/2` · `u − v = 2y ⇒ y = (u − v)/2`

**C11 · trapézio: jacobiano (B6-1)**
1. `∂x/∂u = 1/2` · `∂x/∂v = 1/2` · `∂y/∂u = 1/2` · `∂y/∂v = −1/2`
2. `∂(x, y)/∂(u, v) = (1/2)(−1/2) − (1/2)(1/2) = −1/4 − 1/4 = −1/2`
3. `|J| = 1/2` · conferência: `∂(u, v)/∂(x, y) = 1 · (−1) − 1 · 1 = −2` · `(−2) · (−1/2) = 1`

**C12 · trapézio: a região nova (B6-2)**
1. `y = 0: u = x, v = x ⇒ u = v` · `x − y = 2 ⇒ v = 2` · `x = 0: u = y, v = −y ⇒ u = −v` · `x − y = 1 ⇒ v = 1`
2. `(1, 0) → (1, 1)` · `(2, 0) → (2, 2)` · `(0, −2) → (−2, 2)` · `(0, −1) → (−1, 1)`
3. `B_uv: 1 ≤ v ≤ 2, −v ≤ u ≤ v`

**C13 · trapézio: a integral montada (B6-3)**
1. `∬_B e^{(x+y)/(x−y)} dx dy = ∫₁² ∫_{−v}^{v} e^{u/v} · (1/2) du dv`

**C14 · trapézio: a de dentro (B6-3)**
1. `PRIMITIVA EM u: v e^{u/v}` · `CONFERE: d/du (v e^{u/v}) = v · (1/v) e^{u/v} = e^{u/v} ✓`
2. `∫_{−v}^{v} e^{u/v} du = [v e^{u/v}]_{u=−v}^{u=v} = v e^{v/v} − v e^{−v/v}`
3. `= v e − v e^{−1} = v (e − 1/e)`

**C15 · trapézio: a de fora (B6-3)**
1. `(1/2) ∫₁² v (e − 1/e) dv = (1/2)(e − 1/e) ∫₁² v dv`
2. `∫₁² v dv = [v²/2]₁² = 4/2 − 1/2 = 3/2`
3. `= (1/2)(e − 1/e)(3/2) = (3/4)(e − 1/e) ≈ 1,763`

**C16 · trapézio: conferência f = 1 (B6-4)**
1. `PLANO u, v: ∫₁² (v − (−v)) dv = ∫₁² 2v dv = [v²]₁² = 4 − 1 = 3`
2. `× |J| = 3 · 1/2 = 3/2`
3. `PAPEL: 2 · 2/2 − 1 · 1/2 = 2 − 1/2 = 3/2 ✓`
4. `1/2 = O JACOBIANO` (lima)

**C17 · Ex. 1 do livro (B7)**
1. `u = x − y, v = x + y ⇒ x = (u + v)/2, y = (v − u)/2`
2. `J = (1/2)(1/2) − (1/2)(−1/2) = 1/4 + 1/4 = 1/2` · selo `SINAL TROCOU, MÓDULO NÃO`
3. `x + y = 1 ⇒ v = 1` · `x + y = 2 ⇒ v = 2` · `y = 0 ⇒ v = u` · `x = 0 ⇒ v = −u` · `B_uv: 1 ≤ v ≤ 2, −v ≤ u ≤ v`
4. `∫_{−v}^{v} (cos u)/(sen v) du = (1/sen v) [sen u]_{−v}^{v} = (sen v − sen(−v))/sen v = 2 sen v / sen v = 2`
5. `(1/2) ∫₁² 2 dv = (1/2) · 2 · (2 − 1) = 1`

## 4. Números (todos conferidos no script)

- **Régua:** ∫₀² x dx = 2; com x = 2t, ∫₀¹ (2t) · 2 dt = 4 · 1/2 = 2.
- **Linear** φ(u, v) = (2u + v, u + 3v): colunas (2, 1) e (1, 3); caixa 3 × 4 = 12; pedaços 2, 3, 2; área **5** = 2 · 3 − 1 · 1.
- **Sinal:** o quadrado unitário de u, v vai no losango (0, 0), (1/2, 1/2), (1, 0), (1/2, −1/2), percorrido no sentido horário; det **−1/2**, área **1/2**.
- **Curvo** φ(u, v) = (u² − v², 2uv) em [0, 1]²: bordas u = 1 → x = 1 − y²/4, v = 1 → x = y²/4 − 1, u = 0 → x = −v², y = 0 (o eixo x negativo), v = 0 → x = u², y = 0 (o eixo x positivo); J = **4u² + 4v²**; J(0, 0) = 0, J(1, 1) = 8; M = φ(0,75; 0,5) = **(0,3125; 0,75)**, J(M) = **3,25**; área **8/3** pelos dois caminhos.
- **Zoom (B4-2):** Δ = 0,1; ∂φ/∂u Δu = (0,15; 0,10); ∂φ/∂v Δv = (−0,10; 0,15) (perpendiculares); área do paralelogramo 0,0325 = 3,25 · 0,01.
- **Dobra** φ(u, v) = (u², v) em [−1, 1] × [0, 1]: J = 2u; ∬ |J| = **2**; área da imagem [0, 1]² = **1**; J = 0 em u = 0.
- **Trapézio** de vértices (1, 0), (2, 0), (0, −2), (0, −1): u = x + y, v = x − y; J = **−1/2**; B_uv: 1 ≤ v ≤ 2, −v ≤ u ≤ v; cantos → (1, 1), (2, 2), (−2, 2), (−1, 1); ∫_{−v}^{v} e^{u/v} du = v(e − 1/e); ∫₁² v dv = 3/2; resultado **(3/4)(e − 1/e) ≈ 1,763**; área 3 · 1/2 = **3/2** = 2 − 1/2; a grade inclinada tem passo 1 nas duas famílias, célula de lado 1/√2 e área 1/2.
- **Ex. 1 do livro:** u = x − y, v = x + y; J = **+1/2**; resultado **1**.
- **Mercator:** fator de área sec²(latitude); sec²(72°) ≈ 10,47 (na tela só `≈ × 10`).
- **Fluidos:** `ÁREA × (1 + t · div F + …)` (sem O(t²) na tela).
- **S2 · gancho:** o disco x² + y² ≤ 1 com ∬ e^{−(x²+y²)} dA, **trava nas duas ordens**; a célula do anel com `ÁREA ≅ ? · Δr Δθ`. O valor π(1 − 1/e) **não vai para a tela**.

## 5. Cena a cena

- **Gatilho** é a frase da narração (Anexo A) em que a ação começa. Cada âncora do Anexo A tem a sua **Tela** e a sua lista **Gatilhos: "frase" → ação**. Siga-as inteiras; abaixo só vai o que o Anexo não diz ou o que precisa de cuidado.
- **Alvo** é o quadro em `yt_0036_quadros_alvo_v1/`, reproduzido com tolerância de ±20 px na posição e ±5 % no tamanho. Onde o alvo e este texto divergirem, vale o texto.
- **Canto:** a linha 1 é `CÁLCULO III · MUDANÇA DE VARIÁVEIS`, e a linha 2 é o título da cena: o do alvo quando há alvo; nos outros, o trecho da tabela de tempo em maiúsculas (ex.: B1-2 `O FATOR NUMA CURVA`, B5-1 `DA ÁREA PARA A INTEGRAL`, B5-4 `CONFERINDO O TEOREMA`, B6-1 `O TRAPÉZIO: O JACOBIANO`, B6-4 `A CONFERÊNCIA`, B7 `PAUSE E TENTE`, B8 `O JACOBIANO NO MUNDO`, S1 `SÍNTESE`).

### H · o desafio e a tese · alvos 01 e 02
- **H1 (alvo 01).** Layout B direto. Ordem: o trapézio no papel (direita) e `∬_B e^{(x+y)/(x−y)} dA` a caneta na faixa de baixo; a tira em pé âmbar e a placa `TRAVA`; a tira deitada magenta e a segunda placa (a legenda `EM PÉ E DEITADO` embaixo das placas); no expoente, `x + y` acende laranja e `x − y` verde-água; as bordas `x − y = 1` e `x − y = 2` acendem verde-água; nascem as retas `x + y = k` (laranja) e depois `x − y = m` (verde-água), passo 1, uma família por vez; nasce o plano u, v à esquerda e o trapézio **voa** para ele e se endireita (um movimento); o glyph map 17 escreve a integral nova; `1/2 ?` em lima com `?` ALERTA; as células do trapézio de u, v acendem (`1`, `2`, `½ + ½`) e `3 CÉLULAS`; no papel, `ÁREA 3/2`; **por último** uma célula da grade inclinada acende (chapa + malha) com `ÁREA ?`. **Não escrever `1/2` nessa célula**: a resposta só aparece no B3-3.
- **H2 (alvo 02).** A célula inclinada cresce até o centro (vem da célula acesa do H1), com `Δu` e `Δv` nos lados; `JACOBIANO = FATOR LOCAL DE ÁREA` a caneta; `dx dy = |J| du dv` (o `|J|` em lima). A pulsação única da célula é no gatilho "estica ou encolhe".

### A · bem-vindos · alvo 03
Padrão do canal: logo; `CÁLCULO III · MUDANÇA DE VARIÁVEIS` (ciano, pequeno; **troque** o `MUDANÇA DE VARIÁVEIS NA INTEGRAL DUPLA · VÍDEO 1` do alvo, porque nada de número de vídeo na tela); título `JACOBIANO E MUDANÇA DE VARIÁVEIS`; `NESTE VÍDEO`; as cinco etiquetas `1 · A RÉGUA`, `2 · O PARALELOGRAMO`, `3 · O FATOR LOCAL`, `4 · O TEOREMA`, `5 · O TRAPÉZIO` entram uma por gatilho (a última em lima).

### B1 · a régua esticada · alvo 04
- **B1-1 (alvo 04).** As duas réguas (t laranja em cima, 0 a 1; x âmbar embaixo, 0 a 2); o segmento `Δt` (lima) acende e as pontas descem por linhas finas até a régua de x (`Δx = 2 Δt`); a coluna C1 inteira. A frase do sinal ("esse delta xis tem sinal") acende a legenda `FATOR DE COMPRIMENTO: |g′(t)|` com o módulo sublinhado.
- **B1-2 (sem alvo).** Layout A: a curva γ (branca) no palco, o arco de γ(t) a γ(t + Δt) aceso em lima, a seta `γ′(t) Δt` (branca) tangente em γ(t); Δt encolhe (um movimento) e a seta gruda no arco; coluna: `Δs ≅ ‖γ′(t)‖ Δt`.

### B2 · a transformação · alvo 05
- **B2-1 (alvo 05).** Layout B. Ordem do refino (três movimentos curtos): **um ponto** branco do plano u, v voa pela seta φ e cai no ponto do papel; **um lado** (Δu) vira a curva; o lado Δv também; **a célula inteira** vira o quadrilátero curvo com M, N, P, Q. As retas `u₀ CONSTANTE` e `v₀ CONSTANTE` e as curvas correspondentes ficam com o mesmo rótulo (26 px, placa). Faixa de baixo a caneta (linhas mistas, §3.2): `(x, y) = φ(u, v)` · `φ DE CLASSE C¹ NO ABERTO Ω` · `B = φ(A)` · `ÁREA DE B = ?`.

### B3 · o paralelogramo · alvos 06 e 07
- **B3-1 (alvo 06).** A grade inteira de u, v se inclina pelo `ApplyMatrix` (um movimento); o paralelogramo aceso; as setas `(2, 1)` e `(1, 3)` voam para a matriz; a caixa 3 × 4 (traço GEO) nasce em volta; os seis pedaços acendem e saem um por vez, cada um levando a sua área para C2.
- **B3-2 (sem alvo).** A mesma figura com `a`, `b`, `c`, `d` nas pontas das setas; C3 inteira por glyph maps; no fim, a grade inteira com as quatro células mais próximas acesas e `5 Δu Δv` em cada uma (não `5`: a área é multiplicada por cinco) e o selo `FATOR CONSTANTE`.
- **B3-3 (alvo 07).** O quadrado com a seta circular anti-horária, o losango com a horária, `VIROU DE COSTAS` em ALERTA, C4; o `1/2` vira o chip lima (§3.2). Na frase "Falta a outra", o losango e o quadrado saem e a malha 4 × 4 do B4-1 já começa a nascer à esquerda.

### B4 · o fator local · alvos 08 a 11
- **B4-1 (alvo 08).** A malha 4 × 4 do quadrado curva pelo `ApplyPointwiseFunction` (um movimento); as células se colorem pelo tamanho (GEO escuro → lima); `PEQUENA` perto da origem, `GRANDE` perto de (0, 2); os rótulos das bordas (`v = 1: x = y²/4 − 1` e `u = 1: x = 1 − y²/4`, horizontais e com placa); `O FATOR MUDA DE PONTO PARA PONTO`.
- **B4-2 (alvos 09 e 10).** O zoom (um movimento) até a célula de canto M (alvo 09): o quadrilátero curvo, as setas, o paralelogramo tracejado lima, `ARCO MN ≅ …`, `ARCO MQ ≅ …`, `ÁREA DE B ≅ ‖∂φ/∂u ∧ ∂φ/∂v‖ Δu Δv`, legenda `M = φ(0,75; 0,5)`. Depois a sequência do §2.2: a célula curva vira o paralelogramo → decolagem → o vetor sobe → `ALTURA = ÁREA DO PARALELOGRAMO` → a linha `= Δu Δv ‖∂φ/∂u ∧ ∂φ/∂v‖` com os deltas saindo por glyph map (C6, última passagem do mapa 6) → pouso.
- **B4-3 (alvo 11).** Layout A: C6 linhas 1 a 5 à esquerda da coluna (como no alvo), a moldura lima na definição com `JACOBIANO`; C5 à direita; a tabela do Δ com a célula encolhendo no palco (o `ValueTracker` do §2.1); `J(0, 0) = 0 · J(1, 1) = 8` com os dois cantos acendendo no desenho do B4-1 (miniatura). **A frase "usando o jacobiano do canto M para a célula inteira"** acende o canto M na célula da vez.

### B5 · o teorema · alvos 12 e 13
- **B5-1 (sem alvo).** Layout B com a partição de B_uv (use o quadrado [0, 1]² da transformação curva, 4 × 4, depois 8 × 8 no refino) e as imagens Bᵢⱼ; o ponto branco e a sua imagem com a seta φ; a cadeia C7 na faixa de baixo.
- **B5-2 (alvo 12).** O enunciado, uma hipótese por linha, e as seis miniaturas à direita (`1 · DENTRO DE UM ABERTO`, `2 · CONTEÚDO NULO`, `3 · MIOLO NO MIOLO`, `4 · SEM DOBRA`, `5 · A CÉLULA NÃO COLAPSA`, `6 · NA BORDA, PODE`). Cada miniatura acende no gatilho da sua hipótese, **junto com a frase do papel dela** (§3.2 da proposta: "as derivadas são contínuas", "a borda não pesa na soma", "as duas regiões se correspondem", "nenhum pedaço é contado duas vezes", "nenhuma célula de dentro se achata"). Na frase "Essas condições bastam", um selo GEO pequeno `CONDIÇÕES SUFICIENTES` aparece embaixo da lista. O quadro-receita entra em "Na prática".
- **B5-3 (alvo 13).** A dobra (um movimento). A parte sobreposta acende com o selo `SOBREPOSIÇÃO: CONTOU DUAS VEZES` (troca o `CONTOU DUAS VEZES` do alvo); `2 ≠ 1` em ALERTA; a linha u = 0 com `J = 2u = 0` acende em "zera no meio"; por último a borda de um quadrado genérico acende fina com `NA BORDA, PODE`.
- **B5-4 (sem alvo).** Layout A com a região entre parábolas no palco (a mesma do B4-1, sem a malha colorida); C8 inteira; a tira deitada: entrada azul-claro em `x = y²/4 − 1`, saída coral em `x = 1 − y²/4`; C9 inteira; `8/3 = 8/3 ✓`.

### B6 · o trapézio · alvos 14 e 15
- **B6-1 (sem alvo).** Layout B do H (o trapézio com a grade inclinada); coluna C10 e C11; o chip lima desce e encaixa no `J = −1/2`; `|J| = 1/2`; a conferência `∂(u, v)/∂(x, y) = −2`.
- **B6-2 (alvo 14).** Os quatro lados acendem um por um com a equação e voam para o plano u, v; os cantos com as coordenadas; `B_uv: 1 ≤ v ≤ 2, −v ≤ u ≤ v` na faixa de baixo (linha mista: `B_uv:` é `MathTex`).
- **B6-3 (alvo 15).** Layout A: o plano u, v com a tira deitada (v congelado, legenda `v CONGELADO` com placa), entrada azul-claro em u = −v, saída coral em u = v; o chip `|J| = 1/2` no canto da coluna; C13, C14, C15 inteiras.
- **B6-4 (sem alvo).** O plano u, v com as 3 células acesas (`ÁREA 3`); o papel com o triângulo grande (2 · 2/2) menos o pequeno (1 · 1/2); C16; `1/2 = O JACOBIANO` em lima; na frase "A troca não fez mágica", o trapézio do papel e o do plano u, v ficam lado a lado com a seta φ (um movimento, sem texto novo).

### B7 · pause e tente (sem alvo)
Layout A: o trapézio 1 ≤ x + y ≤ 2 no primeiro quadrante (palco como o do B6-3, `vista(330, 700, 150)`, agora com x e y), o enunciado `∬_B cos(x − y)/sen(x + y) dx dy` e o selo `PAUSE E TENTE`; depois C17 inteira, em ritmo mais rápido (cada linha ainda a caneta). O selo `SINAL TROCOU, MÓDULO NÃO` entra no fim (a frase foi para o fim na narração v1).

### B8 · o jacobiano no mundo (sem alvo)
Dois cartões de traço GEO, sem foto e sem efeito: (1) a grade de Mercator (meridianos verticais, paralelos cada vez mais espaçados para o norte), uma célula em 72° acesa com `× sec²(LATITUDE)` e `≈ × 10`, e a célula do equador ao lado para a comparação; legenda `TERRA COMO ESFERA`; (2) o quadradinho do EP. 03 escoando num campo (um movimento curto) com `ÁREA × (1 + t · div F + …)`.

### S · síntese e próximo · alvo 16
- **S1 (sem alvo).** `dx dy = |J| du dv` grande no topo; as quatro caixas com ✓ (`RÉGUA: dx = g′(t) dt` · `LINEAR: ÁREA × |ad − bc|` · `CURVA: ÁREA ≅ |J| ΔuΔv` · `TRAPÉZIO: (3/4)(e − 1/e)`), cada palavra em `Text` e cada fórmula em `MathTex`.
- **S2 (alvo 16).** O disco x² + y² ≤ 1 com `∬_{x²+y²≤1} e^{−(x²+y²)} dA`; as duas placas `TRAVA` (`EM PÉ E DEITADO`); a grade quadrada some e nasce a grade de círculos (laranja) e raios (verde-água), com `r` e `θ`; uma célula do anel acende (chapa + malha) com `ÁREA ≅ ? · Δr Δθ`; o cartão `NO PRÓXIMO VÍDEO: COORDENADAS POLARES` / `QUAL É O FATOR DA GRADE DE CÍRCULOS?` no gatilho falado e por **≥ 8 s**, sem o CTA por cima; depois o CTA padrão.

## 6. Narração (para o tempo do preview)

O preview é silencioso, mas cada âncora dura o tempo estimado da fala do Anexo A: 3 palavras/s, mais 0,15 s antes e 0,35 s depois de cada âncora. O total é ≈ **20:17** de fala (≈ 21 min de vídeo com os respiros e o cartão final).

| Âncora | Palavras | Voz (s) | Início |
|---|---:|---:|---:|
| H1 | 217 | 72,8 | 0:00 |
| H2 | 52 | 17,8 | 1:12 |
| A1 | 60 | 20,5 | 1:30 |
| B1-1 | 194 | 65,2 | 1:51 |
| B1-2 | 105 | 35,5 | 2:56 |
| B2-1 | 148 | 49,8 | 3:31 |
| B3-1 | 152 | 51,2 | 4:21 |
| B3-2 | 132 | 44,5 | 5:12 |
| B3-3 | 134 | 45,2 | 5:57 |
| B4-1 | 98 | 33,2 | 6:42 |
| B4-2 | 177 | 59,5 | 7:15 |
| B4-3 | 298 | 99,8 | 8:15 |
| B5-1 | 163 | 54,8 | 9:55 |
| B5-2 | 215 | 72,2 | 10:49 |
| B5-3 | 130 | 43,8 | 12:02 |
| B5-4 | 174 | 58,5 | 12:45 |
| B6-1 | 201 | 67,5 | 13:44 |
| B6-2 | 145 | 48,8 | 14:51 |
| B6-3 | 173 | 58,2 | 15:40 |
| B6-4 | 102 | 34,5 | 16:38 |
| B7 | 200 | 67,2 | 17:13 |
| B8 | 122 | 41,2 | 18:20 |
| S1 | 92 | 31,2 | 19:01 |
| S2 | 130 | 43,8 | 19:32 |
| **Total** | **3614** | | **20:17** |

- Gere o `duracoes_estimadas.json` por âncora, como nas unidades anteriores, para a voz encaixar depois (WAV contínuo, cena segue a voz).
- Os gatilhos do §5 e do Anexo A são frases dessa narração. Marque o instante estimado de cada um pela contagem de palavras.
- As tags `[curious]`, `[serious]` etc. não contam palavras.
- **Não gerar voz.**

## 7. O que NÃO fazer

- Nada de `ThreeDScene`, `Surface` ou `Prism` do Manim: o único 3D é a cena Three.js do B4-2.
- Nenhuma partícula, brilho, sombra, névoa, contorno em seta, pulso automático ou transparência no 3D.
- A câmera nunca se mexe durante a escrita de uma fórmula.
- Não escrever `1/2` na célula do H1 (é `ÁREA ?`); a resposta só aparece no B3-3.
- Não dizer nem escrever que toda célula do caso linear "tem área 5": é `5 Δu Δv`, a área multiplicada por cinco.
- Não desenhar o vetor ∧ do 3D com as derivadas sozinhas nem com altura "de desenho": são os deslocamentos (com Δu e Δv), na mesma escala das setas, altura 3,25 nas unidades locais.
- Não chamar a cadeia ①②③ de demonstração; não escrever "PROVA".
- Não escrever decimal sem `≈`, nem o decimal antes do exato.
- Não escrever que a primitiva do H1 "não existe" nem citar Ei ou Liouville: é `TRAVA`.
- Não mostrar o valor π(1 − 1/e) do gancho, nem a palavra "polar" antes do cartão do S2, nem o fator `r` (a célula do anel leva `?`).
- Não escrever O(t²) na tela do B8.
- Não usar o laranja `#E08A3C` do EP. 05 para pontos de amostra (briga com o u): pontos são brancos.
- Não pôr frase portuguesa dentro de `MathTex`, nem `\tfrac`, nem `FadeIn` de linha pronta. Nenhum rótulo girado.
- Não citar livro, número de episódio nem o Atlas na tela.
- Não mexer em `template/`, `assets/`, `docs/`, `AGENTS.md` nem nas outras unidades.
- Não gerar voz, SRT, master, 1080p nem entrega. Não fazer commit nem push.

## 8. QA do preview (obrigatório antes de entregar)

1. **Render × alvo:** um still em cada um dos 16 gatilhos, tirado quando o estado do alvo está completo e comparado na mesma resolução (alvo reduzido a 960×540, tolerância de 10 px nessa escala). Prancha `comparacao_v1.jpg`. Toda diferença que sobrar vai listada com o motivo (as trocas pedidas no §3.2 e no §5 contam como diferença esperada; liste-as).
2. **Alinhamento 3D × Manim** (`alinhamento3d_v1.txt`):
   - para cada quadro 3D, os rótulos contra os pontos do `pontos.json` do mesmo quadro (≤ 2 px);
   - na decolagem e no pouso, o contorno do paralelogramo 2D contra o do PNG no quadro da troca (≤ 2 px);
   - a altura do vetor no quadro final de `sobe` igual a 3,25 vezes o comprimento de 1 unidade local na vertical, medido no PNG (registre a conta).
3. **R5 · sobreposição** (`sobreposicoes_v1.txt`): caixas de `Text` e `MathTex` contra outros textos, linhas, arestas, setas, bordas de painel e de região, rótulos dos eixos, o chip lima e as arestas do 3D, amostradas **a cada 0,5 s, inclusive durante as animações** (em especial a grade que se inclina no B3-1, a malha que curva no B4-1, a dobra do B5-3, os lados que voam no B6-2 e a câmera do B4-2). Esperado: zero.
4. **R6:** nada sai do painel ou do cartão; no layout B nada de um plano invade o outro; o 3D não invade a coluna.
5. **Flash por quadro = 0** (`flash_por_quadro_v1.txt`): nenhuma fórmula aparece inteira antes da caneta. Nada de `FadeIn`, `TransformFromCopy` ou `Write` dentro de `Succession(Wait…)`/`AnimationGroup` que ponha o destino na cena no instante 0.
6. **Glyph maps** (`glyph_maps_v1.txt`): os 17 do §3.4, com mapa → bloco → tempo, e nenhuma linha órfã com "=". `grep -n "from MF_Tools"` ≥ 1 e nenhuma função própria de mapa de glifos.
7. **CONTA INTEIRA** (`conta_inteira_v1.txt`): cada linha de C1 a C17 do §3.5, com o tempo em que aparece na tela e o gatilho falado que a lê. Nenhuma linha faltando, nenhuma linha que não esteja no §3.5.
8. **Texto em MathTex** (`texto_em_mathtex_v1.txt`): liste todo `\text{…}` com mais de uma palavra. Esperado: zero. Inclua também `grep -n tfrac` = 0.
9. **Palco parado** (`palco_parado_v1.txt`): medido só no palco (§3.2). Nenhum trecho acima de 5 s; de 3 a 5 s, só com o motivo. Inclua o palco vazio (> 0,5 s: zero) e o canto sem a linha 2 (zero). Atenção ao B4-3 e ao B5-2 (muita coluna): o palco acompanha.
10. **Cores** (`origens_v1.txt`, seção própria): u laranja e v verde-água em toda reta, seta, derivada e diferencial; |J| em lima em toda ocorrência; entrada azul-claro e saída coral nas tiras do B5-4, do B6-3 e do B6-2 (`u = −v` entrada, `u = v` saída).
11. **Origens** (`origens_v1.txt`): para cada número e limite da tela do §4, de onde ele voa (objeto-fonte) ou qual mapa o produz. Os voos do §3.4 são obrigatórios.
12. **Cartão do próximo vídeo:** ≥ 8 s na tela, sem o CTA por cima.
13. **`PAUSE E TENTE`** no B7, ≥ 3 s.
14. **Tempo de render por bloco** em `tempos_render_v1.txt`, só para registro, com o custo por quadro do 3D. Se o 3D atrasar o preview, o B4-2 funciona em 2D (§2.2): entregue assim e reporte.

## 9. Parada

Entregue o preview, a prancha, os relatórios e o relatório de entrega, incluindo a cena Three.js, o que foi portado de `c3d36.html`, a resolução, o custo por quadro e o alinhamento medido. Pare. Não inicie voz nem 1080p.

---

## Anexo A · narração v1 por âncora (cópia de `yt_0036_narracao_v1.md`, com a Tela e os Gatilhos)

É a narração v1 com as mudanças pontuais do refino filtrado (lista no §8 da proposta v2): H1, B1-1, B2-1, B3-2, B3-3, B4-2, B4-3, B5-1, B5-2, B5-3, B6-4, B7 e B8. As outras 11 âncoras não mudaram.

Tags permitidas: [curious], [thoughtful], [surprised], [happy], [excited], [serious]. Uma por parágrafo (o S2 tem duas, como nos EP. 05 a 10). Sem [slowly] e sem [pause]. Números por extenso na fala. Tela e gatilhos por âncora.

### Tempo por âncora

| Âncora | Trecho | Palavras | Voz (s) | Início estimado |
|---|---|---:|---:|---:|
| H1 | o desafio do vídeo passado | 217 | 72.8 | 0:00 |
| H2 | a ideia do vídeo | 52 | 17.8 | 1:12 |
| A1 | bem-vindos | 60 | 20.5 | 1:30 |
| B1-1 | a régua esticada | 194 | 65.2 | 1:51 |
| B1-2 | o fator numa curva | 105 | 35.5 | 2:56 |
| B2-1 | a transformação | 148 | 49.8 | 3:31 |
| B3-1 | o caso reto: o paralelogramo | 152 | 51.2 | 4:21 |
| B3-2 | o determinante | 132 | 44.5 | 5:12 |
| B3-3 | o sinal e o módulo | 134 | 45.2 | 5:57 |
| B4-1 | a grade curva | 98 | 33.2 | 6:42 |
| B4-2 | de perto, um paralelogramo | 177 | 59.5 | 7:15 |
| B4-3 | o jacobiano | 298 | 99.8 | 8:15 |
| B5-1 | da área para a integral | 163 | 54.8 | 9:55 |
| B5-2 | o teorema | 215 | 72.2 | 10:49 |
| B5-3 | por que inversível | 130 | 43.8 | 12:02 |
| B5-4 | conferindo o teorema | 174 | 58.5 | 12:45 |
| B6-1 | o trapézio: as variáveis e o jacobiano | 201 | 67.5 | 13:44 |
| B6-2 | o trapézio: a região nova | 145 | 48.8 | 14:51 |
| B6-3 | o trapézio: a conta | 173 | 58.2 | 15:40 |
| B6-4 | a conferência | 102 | 34.5 | 16:38 |
| B7 | pause e tente | 200 | 67.2 | 17:13 |
| B8 | o jacobiano no mundo | 122 | 41.2 | 18:20 |
| S1 | síntese | 92 | 31.2 | 19:01 |
| S2 | o próximo vídeo e CTA | 130 | 43.8 | 19:32 |
| **Total** | | **3614** | **20:17** | |

### H1 · o desafio do vídeo passado
**Tela:** layout B. À direita, o trapézio de vértices (1, 0), (2, 0), (0, −2), (0, −1) no papel (GEO translúcido), `∬ e^{(x+y)/(x−y)} dA` a caneta na faixa de baixo; tira em pé âmbar com a placa `TRAVA`; tira deitada magenta com a placa `TRAVA`; no expoente, `x + y` acende laranja e `x − y` acende verde-água; as bordas `x − y = 1` e `x − y = 2` acendem verde-água; nascem as retas `x + y = k` (laranja) e depois `x − y = m` (verde-água), passo 1; à esquerda nasce o plano u, v e o trapézio **voa** para ele, endireitando: `1 ≤ v ≤ 2`, `−v ≤ u ≤ v`; `1/2 ·` aparece em lima na frente da integral com `?`; as células do trapézio de u, v acendem (duas inteiras, `1` e `2`, e duas metades, `½ + ½`: `3 CÉLULAS`) e no papel `ÁREA 3/2`; por último uma célula da grade inclinada acende (chapa + malha) com `ÁREA ?` (a resposta, `1/2`, só aparece no B3-3).
**Gatilhos:** "ficou um desafio"→trapézio · "Fatia em pé"→tira âmbar · "Trava"→placa 1 · "deitada"→tira magenta · "trava também"→placa 2 · "a soma"→`x + y` · "a diferença"→`x − y` · "as bordas também"→bordas acendem · "uma grade nova"→retas nascem · "o trapézio fica reto"→voo para o plano u, v · "um meio na frente"→`1/2 ?` · "três quadradinhos"→1, 2, ½ + ½ · "três meios"→`ÁREA 3/2` · "meio quadradinho do papel"→célula acesa com `ÁREA ?`
> [curious] No fim do vídeo passado, ficou um desafio: este trapézio, com cantos em um, zero; dois, zero; zero, menos dois; e zero, menos um, e a integral dupla de é elevado à fração xis mais ípsilon sobre xis menos ípsilon. Fatia em pé: a integral de dentro, em ípsilon, pede uma primitiva que não se escreve com as funções do Cálculo um. Trava. Fatia deitada: trava também. Nenhuma das duas ordens resolve. Agora repara no expoente. Ele só enxerga duas coisas: a soma, xis mais ípsilon, e a diferença, xis menos ípsilon. E as bordas também: duas delas são retas de xis menos ípsilon constante. Então chama a soma de u e a diferença de vê. As retas de u constante e de vê constante formam uma grade nova, inclinada, por cima do papel. E, nessa grade, o trapézio fica reto: vê vai de um a dois, e u vai de menos vê até vê. A conta sai rapidinho. Só que aparece um meio na frente, que ninguém chamou. E repara: o trapézio tem três quadradinhos da grade nova, contando as duas metades das pontas, mas a área dele no papel é três meios. Então cada quadradinho da grade nova vale só meio quadradinho do papel? De onde sai esse meio? É isso que este vídeo responde.

### H2 · a ideia do vídeo
**Tela:** a célula inclinada grande no centro, com `Δu` e `Δv` nos lados; `JACOBIANO = FATOR LOCAL DE ÁREA` a caneta; embaixo, `dx dy = |J| du dv` (o `|J|` em lima).
**Gatilhos:** "a grade muda"→célula · "estica ou encolhe"→a célula pulsa uma vez de tamanho (um movimento, sem brilho) · "jacobiano"→linha 1 · "vira o módulo"→linha 2
> [serious] E esse é o assunto de hoje. Quando você troca as variáveis, a grade muda, e cada pedacinho de área muda de tamanho. O número que diz quanto ele estica ou encolhe se chama jacobiano. E, na integral, dê xis dê ípsilon vira o módulo do jacobiano vezes dê u dê vê.

### A1 · bem-vindos
**Tela:** logo; `JACOBIANO E MUDANÇA DE VARIÁVEIS`; `NESTE VÍDEO: A RÉGUA · O PARALELOGRAMO · O FATOR LOCAL · O TEOREMA · O TRAPÉZIO`.
**Gatilhos:** "Bem-vindos"→logo · "as próprias variáveis"→título · "a régua esticada"…"do começo ao número"→os cinco itens acendem um a um
> [happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Até aqui, a gente calculou integrais duplas fatiando em xis e em ípsilon. Hoje a gente troca as próprias variáveis. Vamos ver a régua esticada do Cálculo um, o paralelogramo das transformações lineares, o fator local de área, o teorema de mudança de variáveis e, no fim, o trapézio inteiro, do começo ao número.

### B1-1 · a régua esticada
**Tela:** D1 + C1. A coluna: `∫₀² x dx = [x²/2]₀² = 2²/2 − 0²/2 = 2`; as duas réguas (t em cima, x embaixo); `x = 2t ⇒ dx = 2 dt` com os limites `t = 0`, `t = 1` voando das pontas da régua; a conta `∫₀¹ (2t) · 2 dt = 4 ∫₀¹ t dt = 4 [t²/2]₀¹ = 4 · 1/2 = 2 ✓`; no fim, `x = g(t) ⇒ Δx ≅ g′(t) Δt`.
**Gatilhos:** "dá dois"→linha 1 · "xis igual a dois tê"→réguas · "zero a um"→limites voam · "dois dê tê"→`dx = 2 dt` · "duas vezes maior"→o segmento desce e dobra · "fator de comprimento"→rótulo `× 2` · "quatro vezes um meio"→conta · "o mesmo valor"→✓ · "gê linha de tê"→última linha
> [thoughtful] Começa onde você já sabe. No Cálculo um, a integral de zero a dois de xis, dê xis, dá dois: a primitiva é xis ao quadrado sobre dois, e fica quatro sobre dois menos zero. Agora troca a variável: xis igual a dois tê. Quando tê vai de zero a um, xis vai de zero a dois. E o dê xis vira dois dê tê. Por quê? Olha as duas réguas. A do tê tem comprimento um; a do xis, dois. Cada pedacinho delta tê vira um pedacinho delta xis duas vezes maior. Esse dois é o fator de comprimento da troca. E a conta confirma: a integral de zero a um de dois tê, vezes dois, dê tê, é quatro vezes a integral de tê, que é um meio. Quatro vezes um meio, dois. O mesmo valor. Quando a troca não é tão simples, xis igual a gê de tê, o fator muda de lugar para lugar: delta xis é mais ou menos gê linha de tê vezes delta tê. E esse delta xis tem sinal; o fator de comprimento é o módulo de gê linha. Guarda esse sinal: ele volta no determinante.

### B1-2 · o fator numa curva
**Tela:** D2. A curva γ (branca) com `γ(t)` e `γ(t + Δt)`; o arco `Δs` em lima; a seta `γ′(t) Δt` tangente; `Δs ≅ ‖γ′(t)‖ Δt`; Δt encolhe (um movimento) e a seta gruda no arco; no fim, `NO PLANO: FATOR DE ÁREA = ?`.
**Gatilhos:** "um ponto andando"→curva · "um arco"→arco lima · "vetor velocidade"→seta · "a norma"→fórmula · "Quanto menor"→Δt encolhe · "qual é o fator de área"→cartão
> [curious] E se o caminho for uma curva? Gama de tê é um ponto andando no plano. Num tempinho delta tê, ele percorre um arco, delta esse. A derivada, gama linha de tê, é o vetor velocidade, tangente à curva. Então gama linha vezes delta tê é uma setinha tangente, e o comprimento dela, a norma de gama linha de tê vezes delta tê, quase cobre o arco. Quanto menor o delta tê, melhor. Numa dimensão, o fator é sempre o tamanho de uma derivada. E aí vem a pergunta do vídeo: no plano, quando um retângulo vira outra figura, qual é o fator de área?

### B2-1 · a transformação
**Tela:** D3. Layout B. À esquerda, o plano u, v com o retângulo A (chapa + malha), lados `Δu` (laranja) e `Δv` (verde-água), canto `(u₀, v₀)`; seta curva `φ`; à direita, B = φ(A), quadrilátero curvo com cantos `M`, `N`, `P`, `Q`; as retas `u₀ CONSTANTE` e `v₀ CONSTANTE` à esquerda e as curvas correspondentes à direita; faixa de baixo a caneta: `(x, y) = φ(u, v)` · `φ DE CLASSE C¹ NO ABERTO Ω` · `B = φ(A)`.
**Gatilhos:** "fi de u, vê"→fórmula · "de classe cê um"→linha 2 · "um retângulo A"→retângulo · "delta u e delta vê"→rótulos · "a imagem dele"→B · "Um ponto vai num ponto"→um ponto branco voa pela seta φ · "vira uma curva"→o lado Δu vira curva, depois o lado Δv · "M, N, P e Q"→cantos · "quanto vale a área de B"→B acende
> [serious] Vamos dar nome às coisas, como no livro. Fi de u, vê igual a xis, ípsilon: uma transformação que leva cada ponto do plano u vê num ponto do plano xis ípsilon. Ela é de classe cê um num aberto ômega: as derivadas parciais existem e são contínuas, como a gente viu quando estudou derivadas parciais. Pega um retângulo A, de lados paralelos aos eixos, contido em ômega, com lados delta u e delta vê. A imagem dele, B igual a fi de A, é o conjunto dos pontos fi de u, vê com u, vê em A. Um ponto vai num ponto. Um lado, delta u, vira uma curva, e o lado delta vê também. E o retângulo inteiro vira um quadrilátero curvo, com cantos M, N, P e Q. A pergunta é: quanto vale a área de B quando delta u e delta vê são pequenos?

### B3-1 · o caso reto: o paralelogramo
**Tela:** D4, D5 + C2. Layout B: a grade de u, v se inclina inteira (um movimento); o quadrado unitário vira o paralelogramo; os lados viram as setas `(2, 1)` laranja e `(1, 3)` verde-água, que voam para a matriz `[2 1; 1 3]` (sem selo: só a fala cita o EP. 03); a caixa 3 × 4 em GEO, e os seis pedaços saem um a um com a área a caneta; `12 − 2 − 3 − 2 = 5`.
**Gatilhos:** "dois u mais vê"→fórmula · "retas viram retas"→grade inclina · "dois, um"→seta laranja · "um, três"→seta verde-água · "as colunas da matriz"→setas voam · "derivadas parciais"→a matriz ganha moldura fina · "caixa de três por quatro"→caixa · "um de área cada"→2 triângulos saem · "um e meio de área cada"→2 triângulos saem · "um por um"→2 retangulinhos saem · "cinco"→`= 5`
> [thoughtful] Antes da curva, o caso reto. Fi de u, vê igual a dois u mais vê, u mais três vê. É uma transformação linear: retas viram retas, e o quadrado de lado um vira um paralelogramo. Para onde vão os lados? O lado do u, de zero, zero até um, zero, vai para dois, um. O lado do vê vai para um, três. Esses dois vetores são as colunas da matriz dois, um; um, três. É a matriz jacobiana que a gente viu nas derivadas parciais: cada coluna diz para onde vai um lado do quadradinho. E a área? Põe o paralelogramo numa caixa de três por quatro: área doze. Tira dois triângulos de catetos dois e um, um de área cada. Tira dois triângulos de catetos um e três, um e meio de área cada. E tira dois retangulinhos de um por um. Doze, menos dois, menos três, menos dois: cinco.

### B3-2 · o determinante
**Tela:** D5 com letras + C3. A mesma figura com `a`, `b`, `c`, `d` nas pontas das setas; a coluna por glyph maps: o produto aberto, `ac` e `−ac` acendem juntos e somem, `bd` e `−bd` idem, `bc − 2bc` vira `−bc`; `= ad − bc = det [a b; c d]`; `2 · 3 − 1 · 1 = 5 ✓`; a grade inteira com todas as células acesas e `5` em cada uma (as quatro mais próximas).
**Gatilhos:** "Com letras"→letras · "A caixa é á mais bê"→linha 1 · "Abrindo o produto"→linha 2 · "cancela"→pares somem · "sobra menos bê cê"→linha 3 · "o determinante"→det · "cinco"→✓ · "toda célula"→células com 5 · "o mesmo em todo lugar"→selo `FATOR CONSTANTE`
> [serious] Agora com letras: as colunas á, cê e bê, dê. A caixa é á mais bê, vezes cê mais dê. Tira duas vezes á cê sobre dois, duas vezes bê dê sobre dois e dois bê cê. Abrindo o produto: á cê, mais á dê, mais bê cê, mais bê dê. O á cê cancela, o bê dê cancela, e bê cê menos dois bê cê sobra menos bê cê. Fica á dê menos bê cê: o determinante da matriz. Dois vezes três, menos um vezes um: cinco. E, como a transformação é linear, toda célula da grade, de lados delta u e delta vê, vira um paralelogramo de área cinco vezes delta u vezes delta vê: a área é multiplicada por cinco. E o fator é o mesmo em todo lugar.

### B3-3 · o sinal e o módulo
**Tela:** D6 + C4. Layout B: o quadrado com a seta circular anti-horária (`u` depois `v`); à direita o losango com a seta horária; selo `VIROU DE COSTAS` em ALERTA; coluna: as colunas `(1/2, 1/2)` e `(1/2, −1/2)`, `det = (1/2)(−1/2) − (1/2)(1/2) = −1/4 − 1/4 = −1/2`, `ÁREA = |−1/2| = 1/2`; o `1/2` ganha a cor lima e voa para o canto, onde fica como chip até o B6.
**Gatilhos:** "de trás para a frente"→fórmulas · "um meio, um meio"→colunas · "menos um meio"→det · "Área negativa?"→ALERTA · "anti-horário"→seta 1 · "sentido horário"→seta 2 · "virou de costas"→selo · "o módulo"→`|−1/2| = 1/2` · "o meio do trapézio"→chip
> [curious] Agora a troca do trapézio, de trás para a frente: xis igual a u mais vê sobre dois, ípsilon igual a u menos vê sobre dois. As colunas são um meio, um meio, e um meio, menos um meio. O determinante: um meio vezes menos um meio, menos um meio vezes um meio. Menos um quarto, menos um quarto: menos um meio. Área negativa? Não. Anda pelo quadrado no sentido anti-horário: primeiro o lado do u, depois o do vê. Na imagem, a volta sai no sentido horário: o quadrado virou de costas. O sinal conta isso, a orientação. A área é o módulo: um meio. É o meio do trapézio, e a primeira parte do desafio está paga. Falta a outra: e quando a transformação não é linear, e a grade sai curva?

### B4-1 · a grade curva
**Tela:** D7. Layout B: a malha 4 × 4 do quadrado [0, 1]² à esquerda; à direita a grade se curva (um movimento); as bordas ganham rótulos `u = 1 → x = 1 − y²/4` e `v = 1 → x = y²/4 − 1`; as células se pintam pelo tamanho (GEO apagado → lima); a célula perto da origem e a perto do topo acendem com `PEQUENA` e `GRANDE`.
**Gatilhos:** "que entorta"→fórmulas · "a parábola"→rótulos · "quadriláteros curvos"→grade curva · "quase somem"→célula pequena · "crescem"→célula grande · "muda de ponto para ponto"→pintura pelo tamanho
> [thoughtful] Agora uma transformação que entorta: xis igual a u ao quadrado menos vê ao quadrado, e ípsilon igual a dois u vê, no quadrado de zero a um. A reta u igual a um vira a parábola xis igual a um menos ípsilon ao quadrado sobre quatro. A reta vê igual a um vira a parábola xis igual a ípsilon ao quadrado sobre quatro menos um. As células viram quadriláteros curvos. E repara no tamanho: perto da origem, elas quase somem; lá em cima, elas crescem. Aqui não existe um fator só: ele muda de ponto para ponto.

### B4-2 · de perto, um paralelogramo
**Tela:** D8 + Three.js. Zoom na célula de canto `M` (alvo 09): o quadrilátero curvo `MNPQ` (chapa + malha); as setas `∂φ/∂u Δu` (laranja) e `∂φ/∂v Δv` (verde-água) saindo de M; o paralelogramo tracejado lima; `ARCO MN ≅ ‖∂φ/∂u‖ Δu` e `ARCO MQ ≅ ‖∂φ/∂v‖ Δv`. A célula curva vira o paralelogramo (um movimento) e a vista de cima **decola** para a cena Three.js (a vista ortográfica de cima é o mesmo quadro do 2D): o paralelogramo no chão, as duas setas dos deslocamentos, o vetor `(∂φ/∂u Δu) ∧ (∂φ/∂v Δv)` sobe em lima até a altura 3,25 (unidade local = Δ), `ALTURA = ÁREA DO PARALELOGRAMO` (alvo 10); a linha `= Δu Δv ‖∂φ/∂u ∧ ∂φ/∂v‖` com os deltas saindo para fora por glyph map; pouso de volta na vista de cima, que vira o 2D no mesmo quadro.
**Gatilhos:** "dá zoom"→zoom · "vê constante"→lado MN acende · "a setinha"→seta laranja · "delta vê"→seta verde-água · "o paralelogramo dessas duas setas"→tracejado e a célula curva vira o paralelogramo · "Põe as duas setas"→decolagem para o 3D · "fica em pé"→vetor sobe · "a altura dele é a área"→rótulo · "saem para fora"→a linha dos deltas · "vista de cima"→pouso
> [serious] Então dá zoom numa célula, com canto M em u igual a zero vírgula setenta e cinco e vê igual a zero vírgula cinco. O lado MN é a curva de vê constante, andando delta u. Como na curva do começo, ele é quase a setinha da derivada parcial de fi em relação a u, vezes delta u. E o lado MQ é quase a derivada parcial de fi em relação a vê, vezes delta vê. Então a célula é quase o paralelogramo dessas duas setas. E a área de um paralelogramo, lá de vetores, é a norma do produto vetorial. Põe as duas setas, já com o delta u e o delta vê, no chão do espaço, com terceira coordenada zero: o produto vetorial delas fica em pé, na direção cá, e a altura dele é a área do paralelogramo. Os deltas são números, então saem para fora: a área é delta u vezes delta vê vezes a norma do produto vetorial das duas derivadas. Agora volta para a vista de cima, e calcula essa norma.

### B4-3 · o jacobiano
**Tela:** D9, D10 + C6, C5. Layout A: a coluna C6 (o det 3 × 3, a coluna dos zeros acende, sobra o 2 × 2 com o k, a transposta por glyph map, a moldura lima na definição `∂(x, y)/∂(u, v) = det [x_u x_v; y_u y_v]`); `ÁREA DE B ≅ |∂(x, y)/∂(u, v)| Δu Δv` · `FATOR LOCAL DE ÁREA`; depois C5: as quatro derivadas voam de `x = u² − v²` e `y = 2uv` para a matriz, `4u² + 4v²`, `3,25` em M; no palco, a célula de M encolhendo (Δ = 0,25 → 0,1 → 0,05 → 0,01) e a tabela `Δ · EXATA · |J| ΔuΔv · RAZÃO` preenchendo (1,44 · 1,16 · 1,08 · 1,02); por fim `J(0, 0) = 0` e `J(1, 1) = 8` nos cantos da grade.
**Gatilhos:** "i, jota e cá"→det 3 × 3 · "têm zero"→coluna acende · "sobra só o cá"→2 × 2 · "trocando linha por coluna"→transposta · "jacobiano de xis, ípsilon"→moldura · "fator de ampliação"→selo · "dois u"…"dois u"→as quatro derivadas voam · "quatro u ao quadrado mais quatro vê ao quadrado"→J · "três vírgula vinte e cinco"→M · "um vírgula quarenta e quatro"…"um vírgula zero dois"→linhas da tabela · "zero na origem"→`J(0, 0) = 0` · "oito"→`J(1, 1) = 8`
> [serious] O produto vetorial é o determinante com i, jota e cá na primeira linha, as derivadas de xis e de ípsilon em relação a u na segunda, e em relação a vê na terceira, com zero no fim das duas. Os termos com i e com jota têm zero, então sobra só o cá, multiplicado por um determinante dois por dois. Trocando linha por coluna, que não muda o determinante, ele vira a matriz jacobiana: derivadas de xis na primeira linha, de ípsilon na segunda. Esse número se chama o jacobiano de xis, ípsilon em relação a u, vê. E a área da célula é mais ou menos o módulo do jacobiano, vezes delta u, vezes delta vê. O livro chama esse módulo de fator de ampliação, ou de contração, local de área. Na nossa grade: a derivada de xis em relação a u é dois u, em relação a vê, menos dois vê; a de ípsilon em relação a u é dois vê, e em relação a vê, dois u. Dois u vezes dois u, menos menos dois vê vezes dois vê: quatro u ao quadrado mais quatro vê ao quadrado. No ponto M, três vírgula vinte e cinco. E dá para medir o quanto ele acerta, usando o jacobiano do canto M para a célula inteira. Com a célula de lado zero vírgula vinte e cinco, a área de verdade é um vírgula quarenta e quatro vezes o que o jacobiano prevê. Com lado zero vírgula um, um vírgula dezesseis. Com zero vírgula zero cinco, um vírgula zero oito. Com zero vírgula zero um, um vírgula zero dois. Quanto menor a célula, mais ele acerta. E repara: o jacobiano dá zero na origem, onde as células somem, e oito no canto um, um, onde elas crescem.

### B5-1 · da área para a integral
**Tela:** D11 + C7. Layout B: a partição de B_uv em retangulinhos `Rᵢⱼ` à esquerda e as imagens `Bᵢⱼ` à direita; um ponto branco `(ūᵢ, v̄ⱼ)` e a sua imagem `(x̄ᵢ, ȳⱼ)` com a seta φ; faixa de baixo: a cadeia ① → ② → ③, com `α(Bᵢⱼ)` voando da célula da direita e `Δuᵢ Δvⱼ` da célula da esquerda; na passagem ② → ③ a partição se refina (um movimento).
**Gatilhos:** "retangulinhos, erre í jota"→partição · "bê í jota"→imagens · "soma de Riemann"→① · "imagem de um ponto"→pontos e seta · "o módulo do jacobiano"→α voa e vira |J| Δu Δv · "a soma fica quase"→② · "no plano u vê"→o ② acende a célula da esquerda · "as divisões encolhem"→refino · "dê u dê vê"→③
> [thoughtful] Agora junta tudo na integral. Divide a região do plano u vê em retangulinhos, erre í jota. Cada um vira, no papel, um pedacinho, bê í jota. A integral de f sobre B é quase a soma de f num ponto de cada pedacinho, vezes a área do pedacinho, como na soma de Riemann. Escolhe esse ponto como a imagem de um ponto do retangulinho: xis barra, ípsilon barra igual a fi de u barra, vê barra. E a área do pedacinho é quase o módulo do jacobiano vezes delta u vezes delta vê. Então a soma fica quase a soma de f de fi de u barra, vê barra, vezes o módulo do jacobiano, vezes delta u, vezes delta vê. E repara: essa é uma soma de Riemann no plano u vê! Quando as divisões encolhem, ela vai para a integral dupla, no plano u vê, de f de fi de u, vê, vezes o módulo do jacobiano, dê u dê vê.

### B5-2 · o teorema
**Tela:** D12. Layout A: o enunciado a caneta, uma hipótese por linha (`φ DE CLASSE C¹ NO ABERTO Ω` · `B_uv ⊂ Ω COMPACTO, FRONTEIRA DE CONTEÚDO NULO` · `B = φ(B_uv)` e `φ(B̊_uv) = B̊` · `φ INVERSÍVEL NO INTERIOR` · `∂(x, y)/∂(u, v) ≠ 0 NO INTERIOR` · `f INTEGRÁVEL EM B` · `⇒ ∬_B f dx dy = ∬_{B_uv} f(φ(u, v)) |∂(x, y)/∂(u, v)| du dv`), sublinhado de leitura no gatilho; ao lado, uma miniatura por hipótese; no fim, o quadro-receita do livro: `dx dy = |∂(x, y)/∂(u, v)| du dv` · `DETERMINAR B_uv COM B = φ(B_uv)`.
**Gatilhos:** "sem demonstrar"→título `TEOREMA` · "classe cê um"→linha 1 · "compacto"→linha 2 · "conteúdo nulo"→fronteira acende · "o interior vai no interior"→linha 3 · "inversível"→linha 4 · "diferente de zero"→linha 5 · "integrável"→linha 6 · "é igual"→⇒ · "Na prática"→quadro-receita
> [serious] O livro enuncia esse resultado sem demonstrar, porque a prova completa é longa, mas cada hipótese tem um papel. Fi de classe cê um num aberto ômega: as derivadas são contínuas, e de perto a célula é quase o paralelogramo. Bê u vê contido em ômega, compacto, quer dizer, fechado e limitado, e com fronteira de conteúdo nulo, como a gente viu quando estudou conteúdo nulo: a borda não pesa na soma. B é a imagem, fi de bê u vê, e o interior vai no interior: as duas regiões se correspondem. Fi inversível no interior de bê u vê: dois pontos diferentes de dentro não caem no mesmo lugar, e nenhum pedaço é contado duas vezes. E o jacobiano diferente de zero em todo ponto do interior: nenhuma célula de dentro se achata. Nessas condições, se f é integrável em B, a integral dupla de f sobre B é igual à integral sobre bê u vê de f de fi de u, vê, vezes o módulo do jacobiano, dê u dê vê. Essas condições bastam; não são as únicas possíveis. Na prática, é uma receita de dois passos: dê xis dê ípsilon vira o módulo do jacobiano dê u dê vê, e você descobre a região bê u vê que fi leva em B.

### B5-3 · por que inversível
**Tela:** D13. Layout B: o retângulo [−1, 1] × [0, 1] à esquerda (metades laranja-claro e verde-água-claro); `φ(u, v) = (u², v)`; a metade esquerda dobra por cima da direita (um movimento) e as duas caem no quadrado [0, 1]²; coluna: `∬ |J| du dv = ∫₀¹ ∫₋₁¹ 2|u| du dv = 2` × `ÁREA DA IMAGEM = 1` em ALERTA; a linha u = 0 acende com `J = 2u = 0`; a parte sobreposta acende com o selo `SOBREPOSIÇÃO: CONTOU DUAS VEZES`; por último a borda de um quadrado genérico acende fina com `NA BORDA, PODE`.
**Gatilhos:** "se não for"→retângulo · "u ao quadrado"→fórmula · "dobra por cima"→dobra · "dá dois"→conta · "a área do quadrado é um"→ALERTA · "a sobreposição"→selo · "zera no meio"→linha u = 0 · "na borda"→selo final
> [curious] Por que exigir que fi seja inversível? Olha o que acontece se não for. Fi de u, vê igual a u ao quadrado, vê, no retângulo com u entre menos um e um. A metade da esquerda dobra por cima da direita, e as duas caem no mesmo quadrado de lado um. O jacobiano é dois u, e a integral do módulo dele dá dois. Mas a área do quadrado é um. Quem conta a área duas vezes é a sobreposição: cada ponto do quadrado recebe um pedaço de cada metade. E o jacobiano ainda zera no meio, na dobra, um ponto do interior: outra hipótese que falha. Já na borda, o teorema deixa o jacobiano zerar, e deixa fi não ser injetora. Isso vai fazer diferença no próximo vídeo.

### B5-4 · conferindo o teorema
**Tela:** D14 + C8, C9. Layout A com a região entre parábolas no palco; coluna C8 inteira; depois a tira deitada no palco: entrada na parábola azul-claro `x = y²/4 − 1`, saída na coral `x = 1 − y²/4`; C9 inteira (as duas curvas vêm das bordas por glyph map: `v = y/2` substituído); `8/3 = 8/3 ✓`.
**Gatilhos:** "f igual a um"→C8 linha 1 · "Por dentro, em u"→linha 2 · "Por fora, em vê"→linha 3 · "sem jacobiano"→tira deitada · "entra na parábola"→azul-claro · "sai na"→coral · "a saída menos a entrada"→C9 linha 3 · "oito terços"→C9 linha 4 · "Bateu"→✓
> [happy] Testa o teorema na região das parábolas, com f igual a um, que dá a área. A área é a integral no quadrado de quatro u ao quadrado mais quatro vê ao quadrado. Por dentro, em u: quatro u ao cubo sobre três, mais quatro vê ao quadrado vezes u, de zero a um, que dá quatro terços mais quatro vê ao quadrado. Por fora, em vê: quatro vê sobre três, mais quatro vê ao cubo sobre três, de zero a um: quatro terços mais quatro terços, oito terços. Agora confere sem jacobiano, fatiando deitado, como no vídeo das regiões gerais. A fatia entra na parábola da esquerda, xis igual a ípsilon ao quadrado sobre quatro menos um, e sai na da direita, xis igual a um menos ípsilon ao quadrado sobre quatro. O comprimento é a saída menos a entrada: dois menos ípsilon ao quadrado sobre dois. A integral de zero a dois dá dois ípsilon menos ípsilon ao cubo sobre seis: quatro menos oito sextos, quatro menos quatro terços, oito terços. Bateu.

### B6-1 · o trapézio: as variáveis e o jacobiano
**Tela:** D15 + C10, C11. Layout B do H (o trapézio com a grade inclinada); coluna: `u = x + y` · `v = x − y`, os dois `x + y` e `x − y` voando do expoente; `u + v = 2x ⇒ x = (u + v)/2` e `u − v = 2y ⇒ y = (u − v)/2` por glyph map; as quatro derivadas; `J = −1/2` (o chip lima do B3-3 volta e encaixa); `|J| = 1/2`; a conferência `∂(u, v)/∂(x, y) = −2`; no palco, uma célula da grade inclinada acende com `LADO 1/√2` e `ÁREA 1/2`.
**Gatilhos:** "Passo um"→`u`, `v` voam · "Soma as duas"→x · "Subtrai"→y · "Passo três"→derivadas · "menos um meio"→J · "um meio"→|J| · "pelo outro lado"→conferência · "divide por dois"→`(−2)(−1/2) = 1` · "um sobre raiz de dois"→célula
> [serious] Agora sim, o trapézio. Passo um: escolher as variáveis. O integrando pede a soma e a diferença, e as bordas também. Então u igual a xis mais ípsilon, e vê igual a xis menos ípsilon. Passo dois: o teorema quer xis e ípsilon em função de u e vê. Soma as duas: u mais vê é dois xis, então xis é u mais vê sobre dois. Subtrai: u menos vê é dois ípsilon, então ípsilon é u menos vê sobre dois. Passo três: o jacobiano. A derivada de xis em relação a u é um meio, em relação a vê, um meio; a de ípsilon em relação a u é um meio, e em relação a vê, menos um meio. Um meio vezes menos um meio, menos um meio vezes um meio: menos um quarto menos um quarto, menos um meio. Módulo: um meio. E dá para conferir pelo outro lado: o jacobiano de u, vê em relação a xis, ípsilon é um vezes menos um, menos um vezes um: menos dois. A ida dobra a área, e a volta divide por dois. No papel, cada célula da grade inclinada tem lado um sobre raiz de dois, e área um meio.

### B6-2 · o trapézio: a região nova
**Tela:** D15 + C12. Layout B: os quatro lados do trapézio acendem um por um com a equação e **voam** para o plano u, v, virando `u = v` (coral), `v = 2`, `u = −v` (azul-claro), `v = 1`; os quatro cantos com as coordenadas antes e depois; a tira deitada no plano u, v (v congelado), entrada azul-claro e saída coral; `B_uv: 1 ≤ v ≤ 2, −v ≤ u ≤ v`.
**Gatilhos:** "Passo quatro"→lado 1 · "u igual a vê"→`u = v` · "vê igual a dois"→lado 2 · "u igual a menos vê"→lado 3 · "vê igual a um"→lado 4 · "Os cantos conferem"→cantos · "entra em menos vê"→azul-claro · "sai em vê"→coral · "bê u vê"→a linha final
> [thoughtful] Passo quatro: a região nova. Cada lado do trapézio vira um lado novo. O de cima, ípsilon igual a zero: aí u e vê ficam iguais a xis, então u igual a vê. A borda xis menos ípsilon igual a dois vira vê igual a dois. O lado xis igual a zero: u fica ípsilon e vê fica menos ípsilon, então u igual a menos vê. E a borda xis menos ípsilon igual a um vira vê igual a um. Os cantos conferem: um, zero vai para um, um; dois, zero vai para dois, dois; zero, menos dois vai para menos dois, dois; e zero, menos um vai para menos um, um. No plano u vê, vê vai de um a dois, e, para cada vê, a fatia em u entra em menos vê e sai em vê. Essa é a região bê u vê.

### B6-3 · o trapézio: a conta
**Tela:** D16 + C13, C14, C15. Layout A com o plano u, v no palco (a tira deitada); a coluna por glyph maps: a integral montada (o `1/2` lima voa do chip; os limites voam do palco); a primitiva e a conferência da derivada; o colchete; `v (e − 1/e)`; a de fora; `[v²/2]₁² = 4/2 − 1/2 = 3/2`; `(1/2)(e − 1/e)(3/2) = (3/4)(e − 1/e) ≈ 1,763`.
**Gatilhos:** "Passo cinco"→C13 · "o vê está congelado"→a tira acende · "vê vezes é elevado"→primitiva · "deriva e confere"→conferência · "Colchete"→C14 linha 2 · "é menos um sobre é"→C14 linha 3 · "Por fora"→C15 linha 1 · "três meios"→C15 linha 2 · "três quartos"→C15 linha 3 · "um vírgula setenta e seis"→≈
> [serious] Passo cinco: a conta. A integral fica a integral de um a dois, em vê, da integral de menos vê até vê, em u, de é elevado a u sobre vê, vezes um meio, dê u, dê vê. Por dentro, o vê está congelado, e o expoente é só u vezes um número. A primitiva de é elevado a u sobre vê, em u, é vê vezes é elevado a u sobre vê: deriva e confere, vê vezes um sobre vê dá um. Colchete de menos vê até vê: vê vezes é elevado a um, menos vê vezes é elevado a menos um. Fica vê vezes, é menos um sobre é. Por fora: um meio, vezes é menos um sobre é, vezes a integral de um a dois de vê, dê vê. A primitiva é vê ao quadrado sobre dois: quatro sobre dois menos um sobre dois, três meios. Um meio vezes três meios, três quartos. Resultado: três quartos de é menos um sobre é, mais ou menos um vírgula setenta e seis.

### B6-4 · a conferência
**Tela:** D17 + C16. Layout B: as 3 células da grade nova acendem no trapézio de u, v (`1, 2, 3`); a coluna C16; no papel, o triângulo grande de catetos 2 (GEO) e o pequeno de catetos 1 (ALERTA tracejado) que sai; `3/2 = 3/2 ✓`; o `1/2` lima ganha o rótulo `O JACOBIANO`.
**Gatilhos:** "f igual a um"→células · "dois vê"→C16 linha 1 · "três"→`= 3` · "vezes o fator"→linha 2 · "No papel"→triângulos · "três meios"→✓ · "é o jacobiano"→rótulo
> [happy] E o teste de sempre, com f igual a um. No plano u vê, a fatia vai de menos vê até vê: comprimento dois vê. A integral de um a dois de dois vê dá vê ao quadrado, quatro menos um, três. Vezes o fator, um meio: três meios. No papel, o trapézio é o triângulo grande, de catetos dois, área dois, menos o pequeno, de catetos um, área um meio: três meios também. O meio que ninguém chamou é o jacobiano. A troca não fez mágica: escolheu a grade em que tudo fica simples, e pagou com o fator de área.

### B7 · pause e tente
**Tela:** D18 + C17. Layout A: o trapézio `1 ≤ x + y ≤ 2`, `x ≥ 0`, `y ≥ 0` no palco, `∬ cos(x − y)/sen(x + y) dx dy`; `PAUSE E TENTE` por 3 s; a escada C17 linha a linha (ritmo mais rápido, cada linha a caneta); nota `SINAL TROCOU, MÓDULO NÃO` ao lado do `J = +1/2`; `= 1 ✓`.
**Gatilhos:** "Pausa o vídeo"→`PAUSE E TENTE` · "u igual a xis menos ípsilon"→C17 linha 1 · "mais um meio"→linha 2 · "trocaram de papel"→nota · "vê igual a um"→linha 3 · "dois seno de vê"→linha 4 · "dá um"→linha 5
> [curious] Pausa o vídeo e tenta este, que é do livro: a integral do cosseno de xis menos ípsilon sobre o seno de xis mais ípsilon, no trapézio entre xis mais ípsilon igual a um e xis mais ípsilon igual a dois, no primeiro quadrante. Pronto? O livro escolhe u igual a xis menos ípsilon e vê igual a xis mais ípsilon. Então xis é u mais vê sobre dois, e ípsilon é vê menos u sobre dois. O jacobiano: um meio vezes um meio, menos um meio vezes menos um meio, um quarto mais um quarto, mais um meio. As bordas viram vê igual a um, vê igual a dois, vê igual a u e vê igual a menos u. Por dentro, um sobre seno de vê sai da integral, e o seno de u, de menos vê até vê, dá seno de vê menos seno de menos vê, dois seno de vê. Dividido por seno de vê: dois. Por fora, um meio vezes a integral de um a dois de dois: um meio vezes dois vezes um, que dá um. O sinal mudou porque u e vê trocaram de papel; o fator de área, que é o módulo, não.

### B8 · o jacobiano no mundo
**Tela:** D19. Dois cartões de traço GEO: (1) a grade de Mercator (meridianos verticais, paralelos cada vez mais espaçados para o norte), uma célula em 72° acesa com `× sec²(LATITUDE)` e `≈ × 10`; (2) o quadradinho do EP. 03 escoando num campo (um movimento curto), `ÁREA × (1 + t · div F + …)` (o `…` é o resto de ordem t², sem escrever O(t²) na tela).
**Gatilhos:** "Mercator"→cartão 1 · "mais de dez vezes"→`≈ × 10` · "catorze vezes"→a célula do equador ao lado · "nos fluidos"→cartão 2 · "um, mais tê vezes o divergente"→`1 + t · div F + …`
> [thoughtful] O jacobiano aparece fora da integral também. No mapa do mundo mais comum, a projeção de Mercator, tratando a Terra como uma esfera, o fator de área é a secante da latitude ao quadrado. Na altura da Groenlândia, uns setenta e dois graus norte, cada pedacinho aparece mais de dez vezes maior do que perto do equador. É por isso que a Groenlândia parece do tamanho da África, que é umas catorze vezes maior. E nos fluidos: num tempo curtinho tê, cada pedacinho da água estica ou encolhe, e o fator de área fica um, mais tê vezes o divergente, mais termos menores. O divergente, a soma dos estiramentos das derivadas parciais, é a taxa com que o fator começa a mudar.

### S1 · síntese
**Tela:** `dx dy = |J| du dv` grande no topo; quatro caixas com ✓: `RÉGUA: dx = g′(t) dt` · `LINEAR: ÁREA × |ad − bc|` · `CURVA: ÁREA ≅ |J| ΔuΔv` · `TRAPÉZIO: (3/4)(e − 1/e)`.
**Gatilhos:** "Na régua"→caixa 1 · "No caso linear"→caixa 2 · "Na transformação curva"→caixa 3 · "no trapézio"→caixa 4 · "o fator local de área"→fórmula do topo acende
> [serious] Resumindo. Na régua do Cálculo um, o dê xis vira gê linha de tê dê tê. No caso linear, o quadrado vira paralelogramo, e a área se multiplica pelo módulo do determinante, á dê menos bê cê. Na transformação curva, cada célula é quase um paralelogramo, e a área dela é o módulo do jacobiano vezes delta u vezes delta vê. E, no trapézio, a troca certa transformou duas ordens travadas numa conta de cinco passos. Trocar as variáveis é trocar a grade, e o jacobiano é o fator local de área.

### S2 · o próximo vídeo e CTA
**Tela:** o disco x² + y² ≤ 1 no papel com `∬ e^{−(x²+y²)} dA`; tira em pé e tira deitada, cada uma com `TRAVA`; a grade quadrada some e nasce a grade de círculos (laranja) e raios (verde-água), com `r` e `θ`; uma célula do anel acende (chapa + malha) com `ÁREA ≅ ? · Δr Δθ`; cartão `NO PRÓXIMO VÍDEO: COORDENADAS POLARES` / `QUAL É O FATOR DA GRADE DE CÍRCULOS?` (≥ 8 s); depois o CTA padrão.
**Gatilhos:** "um desafio"→disco · "Em pé, trava"→placa 1 · "deitado, trava"→placa 2 · "círculos e raios"→grade nova · "pedaço de anel"→célula · "Qual é o fator"→`?` · "no próximo vídeo"→cartão · "deixa o like"→CTA
> [curious] E fica um desafio. O disco de raio um, e a integral de é elevado a menos, xis ao quadrado mais ípsilon ao quadrado. É o sino do vídeo das regiões gerais, agora girado em volta da origem. Em pé, trava; deitado, trava. Mas o disco pede outra grade: círculos e raios, com as variáveis erre e teta. Só que a célula dessa grade não é um retângulo: é um pedaço de anel, mais largo longe do centro. Qual é o fator de área dela? É o que a gente descobre no próximo vídeo: coordenadas polares. [happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual troca de variável você já fez sem saber que tinha um jacobiano escondido? Até a próxima!

## Anexo B · Como cada símbolo é lido na fala

| Símbolo | Como se lê | Âncora |
|---|---|---|
| ∬ e^{(x+y)/(x−y)} dA | "a integral dupla de é elevado à fração xis mais ípsilon sobre xis menos ípsilon" | H1 |
| u, v | "u", "vê" | H1 |
| dx dy = \|J\| du dv | "dê xis dê ípsilon vira o módulo do jacobiano vezes dê u dê vê" | H2 |
| x = 2t, dx = 2 dt | "xis igual a dois tê", "dois dê tê" | B1-1 |
| Δt, Δx | "delta tê", "delta xis" | B1-1 |
| g′(t) | "gê linha de tê" | B1-1 |
| γ(t), γ′(t), ‖γ′(t)‖ | "gama de tê", "gama linha de tê", "a norma de gama linha de tê" | B1-2 |
| Δs | "delta esse" | B1-2 |
| (x, y) = φ(u, v) | "fi de u, vê igual a xis, ípsilon" | B2-1 |
| Ω, C¹ | "ômega", "classe cê um" | B2-1 |
| B = φ(A) | "B igual a fi de A" | B2-1 |
| [a b; c d], ad − bc | "a matriz á, bê; cê, dê", "á dê menos bê cê" | B3-2 |
| \|−1/2\| | "o módulo de menos um meio" | B3-3 |
| ∂φ/∂u | "a derivada parcial de fi em relação a u" | B4-2 |
| ∧ | "produto vetorial" | B4-2 |
| i, j, k | "i, jota, cá" | B4-3 |
| ∂(x, y)/∂(u, v) | "o jacobiano de xis, ípsilon em relação a u, vê" | B4-3 |
| Rᵢⱼ, Bᵢⱼ | "erre í jota", "bê í jota" | B5-1 |
| ū, v̄, x̄, ȳ | "u barra", "vê barra", "xis barra", "ípsilon barra" | B5-1 |
| B_uv | "bê u vê" | B5-2 |
| B̊ | (não lido; a fala diz "o interior de B") | B5-2 |
| (3/4)(e − 1/e) | "três quartos de é menos um sobre é" | B6-3 |
| cos(x − y)/sen(x + y) | "o cosseno de xis menos ípsilon sobre o seno de xis mais ípsilon" | B7 |
| sec²(latitude) | "a secante da latitude ao quadrado" | B8 |
| 1 + t · div F + … | "um, mais tê vezes o divergente, mais termos menores" | B8 |
| r, θ | "erre", "teta" | S2 |
