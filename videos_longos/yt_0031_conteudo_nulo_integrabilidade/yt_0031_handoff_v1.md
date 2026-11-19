# yt_0031 · CÁLCULO III · EP. 06 · Conteúdo nulo e integrabilidade
## HANDOFF v1 (para o Claude Code): preview visual silencioso do vídeo inteiro

Data: 2026-11-12. Formato: `longo_horizontal`. Unidade nova: `videos_longos/yt_0031_conteudo_nulo_integrabilidade/`.

**Fase:** só o **preview visual silencioso** do vídeo inteiro, em 960×540 a 15 fps (padrão do AGENTS.md para iterar), sem limite de tempo de render.
- Não gerar voz, SRT, master, 1080p nem entrega.
- Não fazer `commit`, `push`, `branch` nem PR.
- Não alterar `template/`, `assets/`, `pyproject.toml`, `uv.lock`, `AGENTS.md`, `docs/` nem outras unidades. Copiar arquivos de outras unidades para dentro desta pode.

Este handoff é autocontido. Tudo o que você precisa está nele e no zip `yt0031_handoff_v1_completo.zip`:
- **`yt_0031_quadros_alvo_v1/`**:
  - os **31 quadros-alvo** (1920×1080) e a prancha `00_folha_contato_v1.jpg`;
  - **`c3d31.html`** (Three.js r128, `?k=<chave>`): as **cenas 3D de referência**, com a geometria, as câmeras, as cores e a função `proj()` que dá os pontos de tela em px. Ao lado estão as imagens `r3d_<chave>.png` e os pontos `r3d_pts.json`. **Porte essas cenas para a unidade** (§2.2). Elas são o modelo exato, não uma inspiração;
  - **`sb31.html`** (Canvas + KaTeX, `?k=<chave>`): gera os quadros completos (fundo, 2D e rótulos sobre o 3D). Abra com as fontes, `logo_crop.png`, `katex/`, `three.min.js` e `r3d_pts.js` ao lado. As funções de desenho (solda, células vermelhas, coberturas, régua da massa) estão lá com os números exatos.
- **`verificacao/verifica_calc3_32t2_sympy.py`** e a saída dele: **16 checagens, todas `True`**. Todos os números da tela saem dali.
- **`yt_0031_narracao_v2.md`**: a narração aprovada (também no Anexo A deste arquivo).

A matemática, o roteiro, a duração (≈ 19:50) e os textos estão aprovados pelo Kaio. Não rediscuta. Se encontrar uma inconsistência objetiva, reporte antes de mudar.

**Regras deste vídeo (as da série, Kaio):**
- Toda definição formal aparece com a sua figura, e **todo símbolo nasce do desenho**: `TransformFromCopy` do objeto para a fórmula, ou caneta. Nada aparece pronto.
- **Fio condutor:** a chapa de dois metais (a mesma solda do cartão do fim do EP. 05). A imagem que o espectador leva é o **muro coral de tampas em cima da solda**.
- Sem efeito não pedido: nada de partícula, brilho, sombra, névoa, contorno em seta, luz que lava a cor nem câmera girando sem motivo.

---

## 0. O que entregar

1. A unidade nova, com:
   - `ficha.md` (§1);
   - `cena.py` e uma seção `sec_*.py` por bloco (H, A, B1 … B9, S);
   - `threejs/` com as cenas 3D, o renderizador por quadro e os pedidos (§2.2);
   - `referencia/` com a cópia de `yt_0031_quadros_alvo_v1/`.
2. O preview do vídeo inteiro: `renders/v1/yt_0031_preview_v1_540p15.mp4`. A duração segue a narração estimada (§6).
3. A prancha **render × alvo** `renders/v1/qa/comparacao_v1.jpg`: uma linha por quadro-alvo, com o still do render no gatilho ao lado do alvo, para os 31 alvos.
4. Os relatórios de QA em `renders/v1/qa/`:
   - `sobreposicoes_v1.txt` (R5, zero esperado);
   - `alinhamento3d_v1.txt` (rótulos do Manim × pontos do Three.js, ≤ 2 px);
   - `flash_v1.txt` (FLASH POR QUADRO, zero esperado);
   - `tempos_render_v1.txt` (tempo por bloco, só para registro).
5. O relatório de entrega do AGENTS.md: arquivos, renders, QA e pendências.

## 1. Ficha

```
formato: longo_horizontal
tipo: teoria_visual
serie_publica: CÁLCULO III · EP. 06
titulo: Conteúdo nulo e integrabilidade
disciplina: Cálculo III
modulo: 3.2 Integrais duplas (o docs/mapa_curricular.md do repositório ainda usa a numeração antiga)
bloco: 3.2-T2
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §2.3, §2.4 e Apêndice B (só na descrição do YouTube; nada de livro na tela nem na fala)
unidades: x e y em metros; densidade em kg/m²; massa em kg
solido_3d: nenhum do arsenal Blender (caixinhas e tampas são prismas retos, feitos direto em Three.js como no EP. 05)
3d_threejs: b13 (prédio por baixo + tampas, x² + y², n = 4), b13t (só as tampas), b21 (dois metais, n = 16, muro de tampas na solda), b21s (o mesmo com n = 64, opcional), b52 (quarto de disco com f = 1 estendida por zero, tampas na borda)
duracao_alvo: ≈ 19:50 (aprovada pelo Kaio)
```

## 2. Base de código

### 2.1 Manim

- **Antes de começar:**
  - leia `docs/estado_atual.md`;
  - rode `verificacao/verifica_calc3_32t2_sympy.py` com o Python da `.venv`; as 16 linhas devem dar `True`. Se faltar sympy, não instale nada: diga no relatório e siga.
- **Copie, não importe.** O modelo é a unidade do EP. 05, a mais próxima deste vídeo: `videos_longos/yt_0029_soma_riemann_integral_dupla/`. Se ela não estiver no seu checkout, use a mais nova da série que estiver: `yt_0028_*`, depois `yt_0027_*`, depois `yt_0026_*`.
  - Do kit vêm: `kit.py`, `v7.py`, `k29.py` (renomeie para `k31.py`), `render.sh`, `render3d.sh`, o canto de duas linhas, `placa_min`, `TC`/`TX` com caneta e `painel`.
  - O fundo vem de `papel29.py` (copie como `papel31.py`): violeta liso `#18143A → #0F0C26` e a grade `#2B2558` de quadradinho 0,25 que **nasce dos eixos** de cada cena (`papel(ax)`). Nas cenas 3D, o violeta liso, sem grade.
  - Do EP. 05 vêm também, prontos para adaptar: a chapa `x² + y²` (mapa de 64 × 64), a régua da massa, a parábola do B1, o funil das duas paredes, o quarto de disco com as células da borda e o cartão de dois metais do fim.
- Render por bloco (`render.sh <Classe>`) e depois concatene.
- **Sem economia artificial**, mas com cabeça:
  - os mapas (chapa x² + y², dois metais, sen(1/x)) são grades de `Square` sem contorno ou `ImageMobject` gerado por numpy, o que for mais rápido;
  - os pontinhos da Dirichlet (B8) são **três imagens estáticas**, uma por nível de zoom, nunca milhares de objetos;
  - `ValueTracker` e updaters só onde o movimento pede (a régua de dois pontos, o número que acompanha a grade);
  - limpe da cena o que saiu da tela.

### 2.2 Three.js (o pipeline da série)

- **Copie o pipeline do yt_0029** (`threejs/`: `r3d.js`, `package.json` com playwright-core, `cena3d/three.min.js` r128 e o esquema de pedidos).
  1. A passagem seca do Manim grava `pedidos3d/<LOTE>.json` com `{cena: [[quadro, estado], …]}`.
  2. `r3d.js` abre a cena, chama `window.setEstado(estado)` quadro a quadro e grava os PNGs com alfa e o `pontos.json`.
  3. O Manim cola os PNGs como `ImageMobject` em tela cheia e prende os rótulos nos pontos.
- **Porte as cenas de `c3d31.html`** para `threejs/cena3d/` (uma `c31.js` com `window.CENA_ID`, como no yt_0029). Vêm de lá:
  - `caixas()` (geometria única com cor por vértice), `tubo()`, `seta()`, `eixos()`, `base()`, `malha()`;
  - `celulaMetal(a, b, c, d)`, que decide piso, teto e se a célula cruza a solda;
  - as câmeras `CAM_PREDIO = ver([3.6, −6.2, 8.6], [1, 1, 0.7], 600, 600)` e `CAM_BAIXO = ver([3.9, −7.2, 6.8], [1, 1, 0.35], 600, 600)`;
  - a escala vertical: ZS = 0,25 na chapa x² + y² e ZS = 0,5 nos dois metais e no quarto de disco.
- **Estados (`setEstado`)** que cada cena precisa:
  - `b13`: `afunda` de 0 a 1. Em 0, prédio azul por baixo + tampas coral. Em 1, o prédio azul desceu inteiro abaixo do chão (plano de corte em z = 0) e só as tampas ficam, soltas no ar (é o estado `b13t`). `tampas` de 0 a 1 faz as tampas crescerem do topo azul até o teto;
  - `b21`: `n` (16 ou 64), `cresce` de 0 a 1 (as colunas sobem do chão até o piso) e `muro` de 0 a 1 (as tampas coral sobem do piso até o teto, só nas células da solda);
  - `b52`: `cresce` (o bloco de altura 1 sobe) e `muro` (as tampas coral sobem, só nas células da borda).
- **Pouso de entrada:** quando o 2D vira 3D (B1-2 e B2-1), a câmera parte da vista de cima, que coincide **exatamente** com a chapa 2D do Manim (canto (0, 0) em (360, 780) px, 240 px/m), e sobe em 2 s até a câmera do alvo. Copie a pose `pouso` do yt_0029 (câmera em (1, 1, d), d = 1080/(2·240·tan 11°) ≈ 11,57, `setViewOffset(1920, 1080, 360, 0, 1920, 1080)`). Na volta para o 2D, o caminho inverso. No quadro da troca, a imagem 3D e a chapa 2D batem (0 px).
- **Estilo 3D da série:**
  - opaco e sem luz (`MeshBasicMaterial`);
  - tom por face: topo na cor, faces x a 70 % e faces y a 48 % sobre o fundo;
  - contorno escuro fino até n = 16 e sem contorno de n = 32 em diante;
  - sem sombra, névoa, brilho nem transparência;
  - `outputEncoding` linear (o hex da tabela sai igual na tela), antialias ligado.
- **Rótulos são do Manim:** eixos, marcas de altura, `ρ = 1`, `ρ = 3`, `MURO DE TAMPAS`, cotas e fórmulas. O Manim os prende nos pontos do `pontos.json` do mesmo quadro. Alinhamento ≤ 2 px.
- **Câmera a serviço da leitura:**
  - fixa, fora o pouso de entrada e saída;
  - nenhum giro;
  - **a câmera nunca se mexe enquanto uma fórmula está sendo escrita.**

## 3. Sistema visual

### 3.1 Layouts e escala

| layout | geometria a 1080p | blocos |
|---|---|---|
| **A · palco + fórmulas** | Coluna de fórmulas alinhada à esquerda em **x = 1120**.<br>**A chapa R = [0, 2]² tem 1 m = 240 px, com o canto (0, 0) em (360, 780) px.** Ela vai de x = 360 a 840 e de y = 300 a 780.<br>Entre a chapa e a coluna (x 880–1090) ficam só os objetos auxiliares: a barrinha dos valores (B1-1), a barra do orçamento (B3), as barrinhas f(X), f(Y) (B6-2) e a lupa da sen(1/x) (B6-3). | B1-1, B1-4, B2, B3-1/2, B4-1, B5-1, B6, B7-1/2, B8-2 |
| **3D · palco + fórmulas** | O 3D ocupa a esquerda (até x ≈ 1000). A coluna continua em x = 1120. | B1-2, B1-3, B2-1b, B5-2, B6-1, S1 |
| **Três painéis** | 540 × 700 em x = 80, 690 e 1300, y 200–900. Chapa de cada painel com 420 px de lado. Pergunta embaixo. | H1, B7-4 |
| **B · dois painéis** | 860 × 760 em x 80–940 e 990–1850. | B4-2 |
| **C · cartões** | B3-3: 2 × 2 cartões 780 × 340. B9-1: 2 × 2 cartões 840 × 370. B9-2: três cartões 480 × 440 em x = 140, 720 e 1300. B7-3: quatro caixas de largura 1640. | B3-3, B7-3, B9 |

Conversão para o Manim: x_m = (x_px − 960)/135; y_m = (540 − y_px)/135.

### 3.2 Regras (as da série)

- **R1 · Clareira:** nenhum rótulo sobre ponto, linha grossa, aresta ou número; o rótulo sai para o lado.
- **R2 · Placa:** todo rótulo solto sobre o desenho ou sobre o 3D usa `placa_min` (`#131030` a 88 %, 4–6 px).
- **R3:** fórmula nova nunca nasce sobre fórmula velha; a coluna limpa antes.
- **R4:** rótulo junto do objeto que ele nomeia.
- **R5:** QA automático de sobreposição em cada gatilho (§8).
- **R6:** nada sai do seu painel ou cartão, e nada do 3D invade a coluna (x ≥ 1090).
- **R-texto:** legenda solta com no máximo 6 palavras por linha, em maiúsculas Space Grotesk, nunca menor que 22 px no alvo.
- **Um movimento por ideia, uma vez.** Grade nova nasce da velha (`ReplacementTransform`, cada célula se parte em quatro), nunca pisca.
- Parado no máximo 3 s. Se a fala continua e a cena acabou, o próximo passo entra mais cedo.

### 3.3 Cores

| Papel | Cor |
|---|---|
| f, ρ, z, valores de f, barrinha dos valores, bloco f = 1, arco do quarto de disco | ciano `#35D9FF` |
| Mapa da chapa x² + y² | rampa de `#10243A` (0) até `#35D9FF` (8), t = (ρ/8)^0,85 |
| Piso m_ij, s(P), soma por baixo, prédio por baixo, células **calmas** (B7-2) | azul-claro `#7FB2FF` |
| Teto M_ij, S(P), soma por cima, **tampas**, o muro | coral `#FF7A8A` |
| Metal leve (ρ = 1) / metal pesado (ρ = 3) | `#1E5072` / `#30BBE0` |
| Solda, conjunto D, fronteira | branco `#F5F7FF` |
| ε, ε₁, ε₂, **orçamento e retângulos da cobertura A_i**, ✓ | menta `#8CFFD2` (preenchimento a 22 %) |
| δ, régua de dois pontos, X, Y, X_ij, o ponto que troca de metal (H1), sondas de fronteira (B5-1) | laranja `#E08A3C` |
| Células que cruzam a solda ou a borda, células **vermelhas** (B7), ✗, `NENHUM δ SERVE` | ALERTA `#FF5D5D` (células a 55 % sobre o fundo) |
| x, Δx_i / y, Δy_j | âmbar `#FFC24D` / magenta `#EA63FF` |
| Grade da partição, molduras, eixos de valores, legendas secundárias | GEO `#B8C4DA` |

Operadores (Σ, ∪, ⊂, ∀, ∃, ⇒, ⟺, ‖ ‖, | |, ≤) em branco; a cor vai na grandeza.

### 3.4 Álgebra

- **Caneta** em toda fórmula nova: traço finíssimo (~0,7), glifo a glifo, da esquerda para a direita, preenchendo na cor da grandeza, sem flash nem preview.
- Termo que nasce do desenho **voa** para a fórmula (`TransformFromCopy`, arco curto). No 3D, ele voa a partir do ponto projetado. Os voos deste vídeo:
  - B1-1: `m_ij` e `M_ij` voam das pontas da barrinha dos valores;
  - B1-3: `M_ij − m_ij` voa da cota da tampa;
  - B2-1: o `2` da altura da tampa voa do muro;
  - B3-2: cada gasto (0,46 · 0,12 · 0,03) voa do topo da barra do orçamento;
  - B4-1: o `4` voa da cota da coluna empilhada;
  - B6-2: o `δ` voa da régua de dois pontos e o `ε` da faixa menta;
  - B7-2: `αε₂` e `4Mε₁` voam das duas cotas (calmas e vermelhas).
- Conta que continua a anterior usa `TransformByGlyphMap`: B1-3 (as duas somas viram a diferença) e B7-2 (as duas parcelas viram `αε₂ + 4Mε₁`).
- **Sublinhado de leitura:** quando a voz lê um símbolo novo (`∪`, `m(A_i)` no B3-1; `‖ ‖` no B6-2), um traço branco fino (2 px) aparece sob ele por 1,2 s e some. A frase vermelha "NOTA DO ALVO" do alvo 12 não vai ao vídeo.
- Tamanhos: fórmula principal de 40–50 px no alvo e secundária de 34–40 px. Nada menor que 22 px.
- Números com vírgula decimal (`{,}` no LaTeX).
- Os zeros em texto Space Grotesk se confundem com a letra O: nas legendas, escreva "ZERO" por extenso (os alvos já fazem isso). Em fórmula, o 0 é do LaTeX e está certo.

## 4. Números (todos conferidos no script)

- **Chapa de dois metais:** R = [0, 2]². Solda y = g(x) = 1 + 0,42 · sen(1,7x − 0,4). ρ = 1 kg/m² embaixo da solda (leve) e ρ = 3 kg/m² em cima (pesado).
  - Área do leve A₁ = 2 + (0,42/1,7)(cos 0,4 − cos 3) ≈ 2,4721 m². Massa = 12 − 2A₁ ≈ **7,06 kg**.
  - Uma célula [a, b] × [c, d] tem metal leve se c ≤ max g em [a, b] e metal pesado se d > min g em [a, b]. Se tem os dois, é **vermelha** (piso 1, teto 3, tampa 2).
  - Grade n × n:

    | n | células vermelhas | por baixo | por cima | diferença |
    |---|---:|---:|---:|---:|
    | 4 | 5 | 6,00 | 8,50 | 2,50 |
    | 8 | 11 | 6,38 | 7,75 | 1,38 |
    | 16 | 24 | 6,66 | 7,41 | 0,75 |
    | 32 | 47 | 6,88 | 7,25 | 0,37 |
    | 64 | 95 | 6,97 | 7,15 | 0,19 |

    Diferença = 2 × (área das células vermelhas), sempre.
- **Cobertura da solda (B3-2):** n caixas [x_{i−1}, x_i] × [min g, max g]: 4 caixas → **0,46 m²**; 16 → **0,12**; 64 → **0,03**. Orçamentos mostrados: ε = 1, ¼ e 0,05.
- **Caixas empilhadas (B4):**
  - parábola y = x² em [0, 2]: área ≤ 4Δ; 4 pedaços → **2**, 8 → **1**, 16 → **0,5**;
  - solda: sobe **0,58**, desce **0,36**, área ≤ **0,94Δ**;
  - arco y = √(4 − x²): área = 2Δ; 4 → **1**, 8 → **0,5**, 16 → **0,25**, 32 → **0,125**.
- **Chapa x² + y² (B1):** a célula do B1-1 é [1,5; 2]², com piso **4,5** e teto **8**. O funil do B1-4 usa as somas do EP. 05 (por baixo / por cima): Δ = 0,5 → 7 / 15; 0,25 → 8,75 / 12,75; 0,125 → 9,69 / 11,69; 0,0625 → 10,17 / 11,17; limite L = 32/3.
- **B6-2:** |f(X) − f(Y)| ≤ 4√2 ‖X − Y‖ na chapa; ε = 1 → δ ≈ 0,177, **dito e escrito 0,17**. Par do alvo: X = (1,9; 1,9), Y = (1,78; 1,78), f(X) = 7,22, f(Y) = 6,34 (distância ≈ 0,17, diferença 0,88 < 1). Os dois pares "fáceis" ficam embaixo, à esquerda, tracejados.
- **B6-3:** sen(1/x): pares x = 1/(π/2 + 2πk) (seno = 1) e 1/(3π/2 + 2πk) (seno = −1). Na lupa, k = 1: x ≈ 0,127 e 0,091.
- **B7-2:** ε₁ = ε/(8M), ε₂ = ε/(2α) ⇒ αε₂ = ε/2 e 4Mε₁ = ε/2.
- **B7-4:** área do quarto de disco = π; massa ≈ 7,06 kg.
- **B8:** Dirichlet em [0, 2]²: por cima = **4**, por baixo = **0** em toda grade.
- **B9 (exemplos do livro):** Ex. 3: x + y no disco x² + y² ≤ 1. Ex. 4: x + y entre y = x² e y = 1 + x², −1 ≤ x ≤ 1. Ex. 5: f = 1 em cima do eixo x e −1 embaixo, no disco. Ex. 6: x²/(x² + y²) em [−1, 1]², f(0, 0) = 1 (vale 1/(1 + m²) na reta y = mx).

## 5. Cena a cena

- **Gatilho** é o trecho da narração (Anexo A) em que a ação começa.
- **Alvo** é o quadro em `referencia/`, reproduzido com tolerância de ±20 px na posição e ±5 % no tamanho. O alvo mostra o **estado final** da âncora; o caminho até ele é o descrito aqui.
- **Canto:** a linha 1 é `CÁLCULO III · INTEGRAL DUPLA`, e a linha 2 é o título da cena que está no alvo. H, A e S2 não têm canto.

### H · as três perguntas · alvos 01 e 02
- **H1 (alvo 01).** Três painéis entram um por pergunta (`FadeIn` só da moldura, o desenho dentro se constrói):
  - "Olha esta chapa feita de dois metais": o metal leve sobe de baixo, o pesado desce de cima, e a solda branca se desenha da esquerda para a direita. `ρ = 1` e `ρ = 3` a caneta.
  - "Agora divide a chapa em retanguinhos": a grade 16 × 16 nasce, e as células da solda acendem em vermelho, da esquerda para a direita.
  - "Se o ponto escolhido cai do lado leve": a célula [1,125; 1,25] × [1,375; 1,5] ganha contorno laranja e a lupa abre acima da chapa, com o ponto laranja no metal leve (`ρ = 1`). "Se cai do lado pesado": o ponto pula para o metal pesado (`ρ = 3`). `1 OU 3?` e `A INTEGRAL EXISTE?`.
  - "E lembra do quarto de disco?": painel do meio, o quarto de disco refina 8 → 16 → 32 com a borda vermelha. `A BORDA SEMPRE SOME?`.
  - "E tem a terceira pergunta": painel da direita, a chapa x² + y², `|S − 32/3| ≤ 16Δ` e o carimbo coral `CONTA SOB MEDIDA` (gira −7°, entra numa batida só, sem quicar). `TODA FUNÇÃO PRECISA DE UMA?`.
- **H2 (alvo 02).** "Então a pergunta de hoje": os painéis encolhem para uma fileira no topo (a lupa e os textos somem). "O que importa é onde": `O PROBLEMA NÃO É O SALTO` e, na linha de baixo, em ciano, `É ONDE ELE ACONTECE`, a caneta. "e quanto espaço elas ocupam": `E QUANTO ESPAÇO OCUPA` em GEO.

### A · bem-vindos · alvo 03
Padrão do canal, com o cartão `INTEGRAIS DUPLAS · VÍDEO 2`, o título `CONTEÚDO NULO E INTEGRABILIDADE` e as três etiquetas `1 · TAMPAS`, `2 · CONTEÚDO NULO`, `3 · TEOREMA`, que acendem uma por vez quando a voz diz cada passo.

### B1 · piso, teto e tampas · alvos 04 a 07
- **B1-1 (alvo 04).** A chapa x² + y² com a grade 4 × 4 (layout A).
  - "Pega um retanguinho": as outras células escurecem e a célula [1,5; 2]² ganha contorno branco e `R_ij`.
  - "a função assume vários valores": a barrinha dos valores (eixo 2–8, x ≈ 925) cresce em ciano de 4,5 até 8.
  - "o maior número que fica abaixo": o traço azul-claro na ponta de baixo; `m_ij` voa dele para a coluna: `m_ij : piso de f em R_ij` e `O MAIOR NÚMERO ABAIXO DE TODOS`. "O teto é o contrário": o traço coral na ponta de cima e `M_ij : teto de f em R_ij`, `O MENOR NÚMERO ACIMA DE TODOS`.
  - "ínfimo e supremo": `ÍNFIMO` e `SUPREMO` em GEO sob cada linha. "funções limitadas": `f LIMITADA: PISO E TETO EXISTEM`.
- **B1-2 (alvo 05).** "Multiplica o piso pela área": **pouso de entrada** (§2.2) e o prédio por baixo sobe em azul (`b13`, n = 4). `s(P) = ΣΣ m_ij Δx_i Δy_j` e `SOMA POR BAIXO`. "Faz o mesmo com o teto": as tampas coral crescem em cima do prédio azul; `S(P) = …` e `SOMA POR CIMA`. "qualquer soma de Riemann fica entre": `s(P) ≤ ΣΣ f(X_ij)Δx_iΔy_j ≤ S(P)` e `TODA SOMA DE RIEMANN FICA NO MEIO`.
- **B1-3 (alvo 06).** "Agora subtrai as duas somas": as duas fórmulas viram `S(P) − s(P) = ΣΣ (M_ij − m_ij) Δx_iΔy_j` por `TransformByGlyphMap`; a chave e `OSCILAÇÃO` sob `M_ij − m_ij`. "tirando o prédio azul": o prédio afunda (`afunda` 0 → 1 em 1,5 s) e as tampas ficam no ar, com a malha do chão. A cota coral `M_ij − m_ij` na tampa do canto. "o volume de todas as tampas": `= VOLUME DAS TAMPAS`.
- **B1-4 (alvo 07).** Volta ao 2D (pouso inverso). Painel com o funil: eixo horizontal `MAIOR LADO Δ` (0,125 … 0,5), vertical `VALOR DA SOMA` (5, 10, 15).
  - "se a diferença … pode ficar tão pequena": as duas paredes se desenham da direita para a esquerda, coral (S(P) desce) e azul-claro (s(P) sobe), até o ponto branco `L`.
  - "Em épsilon e delta": a coluna escreve `∀ε > 0 ∃δ > 0 :` / `Δ < δ ⇒ S(P) − s(P) < ε` / `⇓` / `f É INTEGRÁVEL`.
  - "toda soma de Riemann está presa": três pontos laranja por grade aparecem entre as paredes.
  - "fazer o volume das tampas sumir": `TAMPAS SOMEM ⇒ INTEGRAL EXISTE`.

### B2 · a chapa de dois metais · alvos 08 a 11
- **B2-1 (alvos 08 e 09).** A chapa de dois metais em 2D com a grade 4 × 4.
  - Coluna: `leve: ρ = 1 kg/m²`, `pesado: ρ = 3 kg/m²` e `≈ ALUMÍNIO E AÇO, MESMA ESPESSURA`.
  - "Numa célula inteira no metal leve": contorno branco na célula [1,5; 2] × [0; 0,5] e `TAMPA 0`; `NUM METAL SÓ` e `m_ij = M_ij ⇒ tampa 0`.
  - "nas células atravessadas pela solda": as 5 células vermelhas acendem; contorno na [1; 1,5] × [1; 1,5] e `TAMPA 2`; `NA SOLDA` e `m_ij = 1, M_ij = 3 ⇒ tampa 2`; `5 CÉLULAS CRUZAM A SOLDA`.
  - "essas tampas formam um muro coral" (alvo 09): pouso de entrada para o 3D `b21` com n = 16. As colunas sobem até o piso e, depois, as tampas coral sobem só sobre a solda. `MURO DE TAMPAS` com fio coral, `ρ = 1` e `ρ = 3` presos nos pontos, eixo z com 1 e 3. Coluna: `16 × 16 · 24 CÉLULAS NA SOLDA`, `altura de cada tampa = 3 − 1 = 2` (o 2 voa do muro), `S(P) − s(P) = 2 · (área das células na solda)`, `FORA DA SOLDA: TAMPA ZERO`.
- **B2-2 (alvo 10).** Volta ao 2D. "Refina a grade": 4 → 8 → 16 → 32 → 64, cada passo um `ReplacementTransform` de 0,6 s. As células vermelhas se refazem a cada passo. A tabela `n · CÉLULAS · POR BAIXO · POR CIMA · DIFERENÇA` ganha uma linha por passo, no instante em que a voz diz o número. A última linha fica com o contorno. `DOBROU n → DIFERENÇA ÷ 2`.
  - "As duas somas apertam": a régua da massa (0–12 kg) com a faixa entre 6,97 (traço azul) e 7,15 (traço coral) e o ponto branco `≈ 7,06`. A faixa encolhe junto com a tabela.
  - "o salto continua exatamente o mesmo": `O SALTO NÃO MUDA; A ÁREA DIMINUI`.
- **B2-3 (alvo 11).** Os metais e a grade saem e fica **só a solda branca** (mais grossa, 5 px) com os eixos. `O CONJUNTO ONDE f SALTA` acima. Coluna: `A SOLDA CABE` / `EM ÁREA PEQUENA?` (menta) e `RETÂNGULOS COM ÁREA TOTAL` / `TÃO PEQUENA QUANTO SE QUEIRA`.

### B3 · conteúdo nulo · alvos 12 a 14
- **B3-1 (alvo 12).** "cobrir a linha inteira com retângulos": os 4 retângulos menta nascem sobre a solda, da esquerda para a direita, com `A₁ … A₄`. `D` em placa à esquerda da chapa. A barra do orçamento (`ε = 1`, `GASTO`) enche até 0,46.
  - A definição a caneta, em quatro linhas: `D tem conteúdo nulo ⟺` / `∀ε > 0 ∃ A₁, …, A_n retângulos:` / `D ⊂ A₁ ∪ A₂ ∪ ⋯ ∪ A_n` / `e Σ m(A_i) < ε`.
  - Sublinhado de leitura no `∪` ("Esse U grande") e no `m(A_i)` ("eme de a i").
  - `∪: UNIÃO · m(Aᵢ): ÁREA DE Aᵢ` e `NÚMERO FINITO DE RETÂNGULOS`.
- **B3-2 (alvo 13).** "Pensa no épsilon como um orçamento": `ORÇAMENTO DE ÁREA`. A marca do topo da barra desce (ε = 1 → ¼ → 0,05; a escala da barra se ajusta para a marca ficar no mesmo lugar), e a cobertura se refaz (4 → 16 → 64 retângulos). Cada gasto voa da barra para a sua linha: `ε = 1 → 4 retângulos → 0,46 m²`, `ε = ¼ → 16 → 0,12 m²`, `ε = 0,05 → 64 → 0,03 m²`. "três exemplos não demonstram nada": `3 EXEMPLOS NÃO SÃO PROVA` e `QUALQUER ε POSITIVO DÁ CONTA`.
- **B3-3 (alvo 14).** Quatro cartões 2 × 2, um por exemplo:
  - `UM PONTO`: o quadradinho encolhe três vezes em volta do ponto;
  - `PONTOS EM NÚMERO FINITO`: um quadradinho em cada um;
  - `UM SEGMENTO`: o retângulo afina três vezes;
  - `UM DISCO CHEIO`: a cobertura de quadradinhos e a barra que **estoura** a marca ε (a parte de cima fica vermelha, `ESTOURA`). ✗ vermelho.
  - As duas regras embaixo: `PEDAÇO DE NULO: NULO` e `UNIÃO FINITA DE NULOS: NULO`.

### B4 · curvas têm conteúdo nulo · alvos 15 a 17
- **B4-1 (alvo 15).** A parábola do EP. 05 (eixo vertical comprimido para caber; mesma cor). "desenha uma caixa que vai do menor ao maior valor": 8 caixas menta, da esquerda para a direita. "empurrar as caixas para a direita e empilhar": cada caixa desliza para a coluna da direita (largura Δ, altura 4), uma por vez, de baixo para cima. A cota `4` e o `Δ` embaixo. Coluna: `CAIXAS: DO PISO AO TETO`, `área das caixas ≤ 4Δ` e as três linhas `4 pedaços → 2`, `8 → 1`, `16 → 0,5`. `O GRÁFICO TEM CONTEÚDO NULO`.
- **B4-2 (alvo 16).** Dois painéis. Esquerda: a solda com 8 caixas; as da subida (mais claras) e as da descida (mais escuras) se empilham em duas colunas, `0,58` / `SOBE` e `0,36` / `DESCE`; `área ≤ 0,94Δ`. Direita: o arco com 8 caixas que se empilham numa coluna de altura `2`; `área = 2Δ` e `4 → 1 · 8 → 0,5 · 16 → 0,25 · 32 → 0,125`, um número por vez com a voz.
- **B4-3 (alvo 17).** Sem desenho de chapa. A caneta escreve `f contínua em [a, b] ⇒ gráfico de f tem conteúdo nulo` e `ÁREA DAS CAIXAS = S − s DA INTEGRAL SIMPLES → ZERO`. Depois `curva de classe C¹ (por partes) ⇒ conteúdo nulo` e `C¹: DERIVADA CONTÍNUA`. Os quatro ícones ciano (polígono, círculo, elipse, segmento) se desenham e ganham ✓ um por vez. Fecha em `1ª PERGUNTA: SIM, PARA ESSAS BORDAS` (menta).

### B5 · fronteira: a borda é uma solda · alvos 18 e 19
- **B5-1 (alvo 18).** O quarto de disco cheio (ciano a 45 %), a borda branca (arco + 2 segmentos) e `B` em placa.
  - "desenha em volta dele uma bola aberta": `BOLA ABERTA: DISCO SEM A BORDA`.
  - "uma bola inteira dentro": a sonda tracejada branca em (0,9; 0,55), `INTERIOR`. "inteira fora": a sonda em (1,82; 1,8), `EXTERIOR`.
  - "não importa o quanto a bola encolhe": a sonda laranja em (√2, √2) encolhe três vezes (0,28 → 0,17 → 0,08), sempre metade dentro e metade fora. `FRONTEIRA`. Coluna: `TODA BOLA PEGA B` / `E PEGA FORA DE B` (laranja).
  - "a fronteira é o arco e os dois segmentos": a borda pisca uma vez em branco mais grosso; `FRONTEIRA DE B` e `O ARCO + OS 2 SEGMENTOS`. "pode pertencer à região ou não": `PODE ESTAR EM B OU NÃO`.
- **B5-2 (alvo 19).** "Coloca a região dentro de um retângulo maior": a fórmula `g = { f em B ; 0 fora de B }` a caneta. "A função salta de um para zero!": pouso de entrada para o 3D `b52`. O bloco ciano de altura 1 sobe (`f = 1`), e o chão fora fica vazio (`f = 0 fora`). "as tampas só aparecem nos retângulos atravessados pela fronteira": as tampas coral sobem só na borda; `TAMPAS SÓ NA BORDA`. "A borda funciona exatamente como a solda": `BORDA = SOLDA` / `ENTRE f E ZERO`, e a miniatura do muro dos dois metais (o quadro do alvo 09) entra no painel de baixo, com `A CHAPA DE DOIS METAIS`.

### B6 · continuidade uniforme · alvos 06 (reaproveitado), 20 e 21
- **B6-1 (sem alvo próprio).** Reaproveita o 3D `b13t` do alvo 06 (as tampas soltas da chapa x² + y²), sem as fórmulas do B1. "longe da solda, a densidade era constante": miniatura do muro dos dois metais à direita, embaixo. "quase toda célula tem o piso diferente do teto": as tampas da x² + y² ficam em destaque. Coluna: `E ONDE f É CONTÍNUA?` (48 px) e `UM δ PARA A CHAPA INTEIRA?`.
- **B6-2 (alvo 20).** Volta ao 2D: a chapa x² + y² com o mapa.
  - "Dá, quando a região é fechada e limitada": `K FECHADO E LIMITADO, f CONTÍNUA EM K`.
  - O enunciado a caneta: `∀ε > 0 ∃δ > 0 : ∀X, Y ∈ K,` / `‖X − Y‖ < δ ⇒ |f(X) − f(Y)| < ε`. Sublinhado de leitura no `‖ ‖` e `‖ ‖: NORMA, A DISTÂNCIA`.
  - **A régua de dois pontos** (2 pontos laranja + barra de comprimento δ, objeto único) passeia por um caminho fixo (`MoveAlongPath`): começa embaixo, à esquerda, e termina no canto de cima, em X = (1,9; 1,9), Y = (1,78; 1,78). As posições que ela deixa para trás ficam tracejadas. Enquanto anda, as duas barrinhas ciano f(X) e f(Y) (entre a chapa e a coluna) mudam de altura, sempre dentro da faixa menta de altura ε.
  - "O mesmo delta serve para todos os pares": `O MESMO δ SERVE EM TODO LUGAR` e `CONTINUIDADE UNIFORME (HEINE-CANTOR)`.
  - "o canto de cima é o mais exigente": a faixa fica justa no canto. `ε = 1 → δ = 0,17` (o δ voa da régua) e `O CANTO DE CIMA ESCOLHE O δ`.
- **B6-3 (alvo 21).** A chapa vira o mapa de sen(1/x): faixas ciano que se apertam perto da borda esquerda, desenhada **tracejada** (`BORDA DA ESQUERDA FICA FORA`). Coluna: `f(x, y) = sen 1/x`.
  - "ela oscila cada vez mais rápido": a lupa abre (retângulo tracejado GEO na chapa e o painel ampliado ao lado), e `PERTO DA BORDA QUE FALTA:` / `ONDULA CADA VEZ MAIS RÁPIDO`.
  - "dois pontos tão próximos": a régua laranja na lupa com `+1` e `−1`; ela encolhe duas vezes para perto da borda (passando para os pares com k = 2 e 3) e os valores continuam `+1` e `−1`. `distância → 0, diferença = 2` e `NENHUM δ SERVE` (vermelho).
  - "esses pares se aproximam de um mesmo ponto": `FECHADA E LIMITADA: OS PARES` / `SE ACUMULAM NUM PONTO DA CHAPA`.

### B7 · o teorema · alvos 22 a 25
- **B7-1 (alvo 22).** Uma função genérica sobre a chapa dos dois metais: o mapa ciano contínuo em cada lado (ver `sb31.html`, chave `b71`) com a solda branca = D.
  - "existe um número eme maiúsculo": `|f| ≤ M` e `f LIMITADA`. "chama de D": `D` em placa.
  - "cobre D com um número finito de retângulos": 8 retângulos menta, contorno cheio; `1 · COBRE D: ÁREA < ε₁`.
  - "engorda um pouquinho": cada retângulo ganha o contorno tracejado, maior; `2 · ENGORDA: ÁREA < 2ε₁`.
  - "margem de segurança": a lupa abre com zoom na célula [0,833; 0,917] × [1,333; 1,417]. Ela encosta no retângulo original e fica inteira dentro do tracejado. `MARGEM: A CÉLULA CABE`.
  - "Fora da cobertura … continuidade uniforme": `FORA DA COBERTURA: f CONTÍNUA` / `→ CONTINUIDADE UNIFORME (ε₂)`.
  - "escolhe uma grade fina": a grade 24 × 24 nasce; as células que encostam na cobertura ficam vermelhas. `3 · GRADE MENOR` / `QUE OS DOIS δ`.
- **B7-2 (alvo 23).** A lupa sai. As células se dividem: calmas em azul-claro a 22 %, vermelhas em ALERTA.
  - "células calmas": `CALMAS` na chapa e na coluna; `tampa < ε₂, área ≤ α ⇒ < αε₂`; `α: ÁREA DO RETÂNGULO`.
  - "células vermelhas": `VERMELHAS` na chapa (acima do pico da solda) e na coluna; `tampa ≤ 2M, área < 2ε₁ ⇒ < 4Mε₁`.
  - "Somando os dois grupos": `αε₂` e `4Mε₁` voam das duas linhas para `S(P) − s(P) < αε₂ + 4Mε₁` (`TransformByGlyphMap`).
  - "metade da tolerância": `αε₂ < ε/2   e   4Mε₁ < ε/2`.
  - "As tampas somem!": `AS TAMPAS SOMEM` (ciano).
- **B7-3 (alvo 24).** Quatro caixas de contorno fino, **sem preenchimento**, uma por vez com a voz: `TEOREMA 1` (ciano), `CASO D = ∅` (menta), `TEOREMA 2` (ciano), `OBSERVAÇÃO` (GEO). O texto de cada uma a caneta.
- **B7-4 (alvo 25).** A fileira dos três painéis do H volta e cresce para o tamanho do H1, **na ordem da fala**: quarto de disco (`ÁREA = π`, `FRONTEIRA DE CONTEÚDO NULO`), dois metais (`MASSA ≈ 7,06 kg`, `SALTA SÓ NA SOLDA`), x² + y² (`INTEGRÁVEL`, `CONTÍNUA NO RETÂNGULO`). Cada painel ganha o ✓ menta quando a voz fecha a resposta. `TRÊS PROBLEMAS, UM TEOREMA`.

### B8 · quando falha · alvos 26 e 27
- **B8-1 (alvo 26).** A coluna escreve a função de Dirichlet e `RACIONAL: FRAÇÃO DE INTEIROS`.
  - "Pega qualquer retanguinho": uma célula de pontinhos ciano (1) e escuros (0). Zoom ×10 e ×100 (três imagens fixas, `ReplacementTransform` entre elas): `A MISTURA NÃO MUDA`.
  - "em todas as células, o piso é zero e o teto é um": `em toda célula: m_ij = 0, M_ij = 1`.
  - "A soma por cima dá sempre quatro": as duas barras (coral 4, azul-claro 0) para 4 × 4, 8 × 8, 16 × 16 e 64 × 64, uma por vez, todas iguais. `4 CONTRA ZERO: NÃO É INTEGRÁVEL`.
- **B8-2 (alvo 27).** A chapa com os pontinhos (o conjunto dos racionais) e a borda vermelha. "Qualquer disquinho": a sonda laranja tracejada e `TODA BOLA PEGA PONTOS DOS DOIS`. `{(x, y) : x, y racionais}`, `FRONTEIRA = O QUADRADO TODO`, `ÁREA 4: NÃO É CONTEÚDO NULO`. "condição suficiente": `CONDIÇÃO SUFICIENTE`, `HIPÓTESES VALEM → INTEGRAL EXISTE` e `NÃO VALEM → OLHE AS SOMAS`.

### B9 · num exercício · alvos 28 e 29
- **B9-1 (alvo 28).** As três perguntas entram como etiquetas no alto, uma por pergunta da fala: `LIMITADA?`, `DESCONTINUIDADES: NULO?`, `FRONTEIRA: NULO?`. Os quatro cartões entram um por exemplo, com a figura, a fórmula e a legenda curta, e os três ✓ menta acendem no fim de cada exemplo. `AS QUATRO SÃO INTEGRÁVEIS`.
  - Nota: a v2 da narração listava a etiqueta "SALTOS EM CONTEÚDO NULO?". O alvo usa `DESCONTINUIDADES: NULO?`, porque o exemplo 6 não é um salto e a frase-tese do vídeo é sobre descontinuidade. Vale o alvo.
- **B9-2 (alvo 29).** Três cartões: `DOIS MATERIAIS` / `MASSA` (a chapa de dois metais lisa), `DIVISA NO MAPA` / `POPULAÇÃO` (duas regiões com uma divisa ondulada), `ALVO REDONDO` / `PROBABILIDADE` (disco). `OS SALTOS MORAM EM CURVAS` e `CURVAS TÊM CONTEÚDO NULO → A INTEGRAL EXISTE`.

### S · síntese e próximo vídeo · alvos 30 e 31
- **S1 (alvo 30).** O 3D `b21` (o muro, n = 16) à esquerda, um pouco menor (escala 0,9). As três caixas entram com a voz: `TAMPAS` / `S(P) − s(P) TENDE A ZERO` (coral), `CONTEÚDO NULO` / `ONDE f SALTA` (menta) e `CONTINUIDADE UNIFORME` / `ONDE f É CONTÍNUA` (ciano). "Juntando as duas ideias, sai o teorema": `⇓` e `O TEOREMA`.
- **S2 (alvo 31).** Sem canto. `NO PRÓXIMO VÍDEO` e `PROPRIEDADES DA INTEGRAL DUPLA`. A chapa de dois metais se **separa** em duas regiões (leve desce 0,03 m, pesado sobe 0,03 m) e a solda fica sozinha no meio. `∬_R ρ dA ≟ ∬_leve ρ dA + ∬_pesado ρ dA` a caneta e `A SOLDA PESA ALGUMA COISA?` (menta). Depois o CTA padrão do canal ("Se essa aula te ajudou…").

## 6. Duração (narração estimada)

Para montar o preview silencioso, use a duração estimada de cada âncora: 0,15 s + palavras/3 + 0,35 s.

| Âncora | Palavras | Voz (s) | Início |
|---|---:|---:|---:|
| H1 | 146 | 49,2 | 0:00 |
| H2 | 72 | 24,5 | 0:49 |
| A1 | 69 | 23,5 | 1:13 |
| B1-1 | 118 | 39,8 | 1:37 |
| B1-2 | 110 | 37,2 | 2:17 |
| B1-3 | 92 | 31,2 | 2:54 |
| B1-4 | 128 | 43,2 | 3:25 |
| B2-1 | 113 | 38,2 | 4:08 |
| B2-2 | 116 | 39,2 | 4:46 |
| B2-3 | 58 | 19,8 | 5:25 |
| B3-1 | 124 | 41,8 | 5:45 |
| B3-2 | 89 | 30,2 | 6:27 |
| B3-3 | 119 | 40,2 | 6:57 |
| B4-1 | 111 | 37,5 | 7:37 |
| B4-2 | 101 | 34,2 | 8:15 |
| B4-3 | 132 | 44,5 | 8:49 |
| B5-1 | 113 | 38,2 | 9:34 |
| B5-2 | 116 | 39,2 | 10:12 |
| B6-1 | 101 | 34,2 | 10:51 |
| B6-2 | 136 | 45,8 | 11:25 |
| B6-3 | 125 | 42,2 | 12:11 |
| B7-1 | 141 | 47,5 | 12:53 |
| B7-2 | 171 | 57,5 | 13:40 |
| B7-3 | 141 | 47,5 | 14:38 |
| B7-4 | 117 | 39,5 | 15:25 |
| B8-1 | 116 | 39,2 | 16:05 |
| B8-2 | 103 | 34,8 | 16:44 |
| B9-1 | 132 | 44,5 | 17:19 |
| B9-2 | 69 | 23,5 | 18:03 |
| S1 | 106 | 35,8 | 18:27 |
| S2 | 137 | 46,2 | 19:03 |
| **Total** | **3.522** | **≈ 19:49** | |

Monte `narracao.md` com o Anexo A e gere `ancoras.json` com esses tempos (o `gerar_ancoras.py` do yt_0029 tem o modo "estimado"). Dentro de cada âncora, distribua os gatilhos do §5 pela posição da frase no parágrafo, a 3 palavras/s. Na fase de voz, a cena vai seguir o WAV contínuo; aqui, só a estimativa.

## 7. O que NÃO fazer

- Voz, SRT, 1080p, master, entrega, capa, publicação, `commit`, `push`, branch ou PR.
- Mexer em arquivos globais ou em outras unidades (copiar delas pode).
- Blender, `ponte.py` ou `Solido3D`; 3D dentro do Manim (`ThreeDScene`).
- Câmera girando, partícula, brilho, sombra, névoa, transparência no 3D, contorno em seta, caixa de fundo azul atrás de fórmula.
- `FadeIn` de fórmula pronta, `Write` dentro de `Succession(Wait…)` ou `AnimationGroup` que ponha o destino na tela antes da hora.
- Livro, autor, Atlas ou "episódio N" na tela.
- O texto vermelho "NOTA DO ALVO" do alvo 12.

## 8. QA

1. **Render × alvo:** para cada um dos 31 alvos, tire o still no fim da âncora (estado final) e monte a prancha `comparacao_v1.jpg`, com o render à esquerda e o alvo à direita. Liste toda diferença que sobrar, com o motivo.
2. **Alinhamento 3D × Manim:** para cada quadro 3D, compare os rótulos com os pontos do `pontos.json` do mesmo quadro (≤ 2 px). Nos pousos (B1-2, B1-4, B2-1, B2-2, B5-2), confira os quatro cantos da chapa 3D contra a chapa 2D (0 px esperado). Relatório em `alinhamento3d_v1.txt`.
3. **R5 · sobreposição:** em cada gatilho, as caixas de texto e `MathTex` não se cruzam entre si nem com pontos, arestas ou linhas grossas. Relatório em `sobreposicoes_v1.txt`.
4. **R6:** nada sai do painel ou cartão, e o 3D não invade a coluna.
5. **FLASH POR QUADRO = 0:** nenhuma fórmula aparece inteira antes da caneta. Relatório em `flash_v1.txt`.
6. **Parado ≤ 3 s.**
7. **Números:** confira na tela os valores do §4 (tabela dos dois metais, coberturas, colunas empilhadas, 0,17, 7,06).
8. **Tempo de render por bloco** em `tempos_render_v1.txt`, só para registro.

## 9. Parada

Entregue o preview, a prancha, os relatórios e o relatório de entrega. Pare. Não inicie voz nem 1080p.

---

## Anexo A · Narração (v2 aprovada, com tags do ElevenLabs v4)

Tags permitidas: [curious], [thoughtful], [surprised], [happy], [excited], [serious]. Uma por parágrafo (o S2 tem duas). Sem [slowly] e sem [pause]. Números por extenso. Leituras: "éle" = L; "eme minúsculo/maiúsculo i j" = m_ij/M_ij; "esse minúsculo/maiúsculo de P" = s(P)/S(P); "cê um" = C¹; "alfa" = α. A linha **Tela** de cada âncora é só referência (o §5 manda).

### H1 · as três perguntas
**Tela:** os três painéis (dois metais, quarto de disco, x² + y² com 16Δ) entram um por pergunta; o ponto laranja troca de metal.
> [curious] Olha esta chapa feita de dois metais. Embaixo, a densidade é de um quilo por metro quadrado. Em cima, três. E, entre os dois, uma linha de solda. Agora divide a chapa em retanguinhos, como no vídeo passado. E os pedaços que cruzam a solda? Se o ponto escolhido cai do lado leve, a densidade é uma. Se cai do lado pesado, é três vezes maior! Será que as somas de Riemann ainda chegam a um único resultado? E lembra do quarto de disco? Quando a grade refinava, a área dos quadradinhos que cruzavam a borda diminuía. Mas isso acontece com qualquer borda? E tem a terceira pergunta: para provar que a massa da chapa do vídeo passado era trinta e dois terços, a gente fez uma conta sob medida, aquele dezesseis vezes o maior lado. Será que precisa inventar uma prova nova para cada função?

### H2 · a ideia do vídeo
**Tela:** os painéis sobem para uma fileira no topo; `O PROBLEMA NÃO É O SALTO` / `É ONDE ELE ACONTECE`.
> [serious] Então a pergunta de hoje é esta: como saber se uma integral dupla existe sem calcular o valor dela? E a resposta é surpreendente. Uma função pode ter descontinuidades e, mesmo assim, ser integrável. O que importa é onde essas descontinuidades acontecem e quanto espaço elas ocupam. E, no caminho, você vai ver por que a chapa de dois metais tem uma massa bem definida, mesmo com a densidade saltando na solda.

### A1 · bem-vindos
**Tela:** logo; `INTEGRAIS DUPLAS`; `NESTE VÍDEO: TAMPAS · CONTEÚDO NULO · TEOREMA`.
> [happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Este é o segundo vídeo do módulo de integrais duplas. No vídeo passado, a gente construiu a integral a partir das somas de Riemann; hoje a pergunta é quando dá para garantir que essas somas convergem. São três passos: medir a diferença entre a soma por cima e a soma por baixo, entender o que é conteúdo nulo e juntar tudo num teorema.

### B1-1 · piso e teto
**Tela:** D1, uma célula da chapa x² + y² e a barrinha dos valores; `m_ij` azul-claro, `M_ij` coral.
> [thoughtful] Começa pela chapa do vídeo passado. Pega um retanguinho da grade, o erre i j. Dentro dele, a função assume vários valores. Agora procura o maior número que fica abaixo de todos esses valores: esse é o piso da célula, eme minúsculo i j. O teto é o contrário: o menor número que fica acima de todos, eme maiúsculo i j. Na matemática, esses números se chamam ínfimo e supremo. Nos exemplos de hoje, eles são o menor e o maior valor de verdade. Mas nem toda função chega a atingir esses extremos, e por isso o nome certo é ínfimo e supremo. E a gente trabalha com funções limitadas, para que o piso e o teto existam.

### B1-2 · as duas somas
**Tela:** D2 e D3, o prédio por baixo e por cima; `s(P) ≤ ΣΣ f(X_ij)Δx_iΔy_j ≤ S(P)`.
> [curious] Multiplica o piso pela área da célula e soma em todas as células da grade: essa é a soma por baixo, esse minúsculo de P. Faz o mesmo com o teto e você tem a soma por cima, esse maiúsculo de P. E repara: qualquer ponto que você escolhe dentro de uma célula dá um valor entre o piso e o teto. Então qualquer soma de Riemann fica entre a soma por baixo e a soma por cima. Lê-se: esse minúsculo de P é menor ou igual à soma de Riemann, que é menor ou igual a esse maiúsculo de P. Todas as aproximações possíveis ficam presas entre duas paredes.

### B1-3 · o volume das tampas
**Tela:** D4, o prédio azul afunda e sobram as tampas; `S(P) − s(P) = ΣΣ (M_ij − m_ij) Δx_iΔy_j`; `OSCILAÇÃO` sob M_ij − m_ij.
> [thoughtful] Agora subtrai as duas somas. Em cada retanguinho sobra o teto menos o piso, vezes a área da base. Essa diferença entre teto e piso tem nome: a oscilação da função na célula. E olha no desenho: tirando o prédio azul, o de baixo, o que sobra do prédio de cima são as tampas coral. Cada tampa tem a altura do teto menos o piso. Então esse maiúsculo menos esse minúsculo de P é exatamente o volume de todas as tampas juntas. Guarda essa imagem, porque ela vai conduzir a demonstração inteira.

### B1-4 · quando as tampas somem
**Tela:** D5, as duas paredes; `∀ε > 0 ∃δ > 0 : Δ < δ ⇒ S(P) − s(P) < ε` → `f INTEGRÁVEL`.
> [serious] E aqui está o critério da aula. Se a diferença entre a soma por cima e a soma por baixo pode ficar tão pequena quanto se queira, só deixando a grade fina o bastante, então a função é integrável. Em épsilon e delta: para todo épsilon maior que zero, existe delta maior que zero tal que, se o maior lado da partição for menor que delta, a diferença entre as duas somas é menor que épsilon. Por que isso funciona? Porque toda soma de Riemann está presa entre as duas paredes. Quando as paredes se fecham num mesmo número, todas as escolhas são obrigadas a chegar nele também. Então, para provar que uma integral dupla existe, a gente persegue uma coisa só: fazer o volume das tampas sumir.

### B2-1 · onde estão as tampas?
**Tela:** a chapa com a solda, ρ₁ = 1 e ρ₂ = 3; uma célula do metal leve, uma do pesado, as células cruzadas em vermelho; o muro coral no 3D.
> [curious] Agora volta na chapa de dois metais. Embaixo da solda, um quilo por metro quadrado; em cima, três. É mais ou menos a diferença entre uma chapa de alumínio e uma de aço com a mesma espessura. Coloca uma grade. Numa célula inteira no metal leve, a densidade vale um em todo ponto: o piso é um, o teto é um, e a tampa tem altura zero. No metal pesado, o mesmo, com três. Mas, nas células atravessadas pela solda, aparecem as duas densidades: o piso é um e o teto é três. Tampa de altura dois, o tamanho do salto. E, juntas, essas tampas formam um muro coral em cima da solda.

### B2-2 · o muro vai sumindo
**Tela:** a grade refina 4 → 64; tabela n · células · por baixo · por cima · diferença; régua da massa apertando em 7,06.
> [thoughtful] Então a diferença entre as duas somas é o salto, dois, vezes a área das células que a solda atravessa. Refina a grade. Com quatro divisões por lado, cinco células cruzam a solda; a soma por baixo dá seis quilos e a por cima, oito e meio. Diferença de dois e meio. Com oito divisões, a diferença cai para um vírgula trinta e oito. Com dezesseis, setenta e cinco centésimos. Com trinta e duas, trinta e sete centésimos. Com sessenta e quatro, dezenove centésimos. As duas somas apertam em torno de sete vírgula zero seis quilos. E repara: o salto continua exatamente o mesmo. O que diminui é a área das células que atravessam a solda.

### B2-3 · a pergunta certa
**Tela:** só a solda branca; `A SOLDA CABE EM ÁREA PEQUENA?`.
> [curious] Então a descoberta é esta: o problema não era a densidade saltar. O problema era quanto espaço os pontos de descontinuidade ocupam. Se a região problemática pode ser coberta por retângulos de área total tão pequena quanto se queira, dá para controlar a contribuição dela na diferença entre as somas. E essa propriedade tem um nome: conteúdo nulo.

### B3-1 · a definição
**Tela:** a definição escrita a caneta em três linhas; sublinhados no ∪ e no m(A_i).
> [thoughtful] Monta a definição com a própria solda. A ideia é cobrir a linha inteira com retângulos, quantos você quiser, desde que seja um número finito. E a condição é: a soma das áreas tem que poder ficar menor que qualquer número positivo escolhido, o épsilon. Então a definição diz: um conjunto D tem conteúdo nulo se, para todo épsilon maior que zero, existe um número finito de retângulos, a um até a ene, tais que D está contido na união deles e a soma das áreas é menor que épsilon. Esse U grande é a união dos conjuntos. E eme de a i é a área do retângulo a i. Ou seja: cobrir o conjunto inteiro gastando menos área do que a tolerância permite.

### B3-2 · um orçamento de área
**Tela:** D6, a barra do orçamento; coberturas com 4, 16 e 64 retângulos.
> [curious] Pensa no épsilon como um orçamento. Alguém diz: você pode gastar no máximo um metro quadrado de cobertura. Quatro retângulos em volta da solda gastam quarenta e seis centésimos. Deu. Agora o orçamento cai para um quarto de metro quadrado. Tudo bem: dezesseis retângulos mais finos gastam doze centésimos. E se cair para cinco centésimos? Sessenta e quatro retângulos gastam três. Mas cuidado: três exemplos não demonstram nada. O que a definição pede é que funcione para qualquer orçamento positivo, por menor que seja. Isso é ter conteúdo nulo.

### B3-3 · o que tem e o que não tem
**Tela:** D7, quatro miniaturas; a barra estoura no disco cheio.
> [thoughtful] Alguns exemplos. Um ponto tem conteúdo nulo: basta um quadradinho em volta dele, tão pequeno quanto o orçamento pedir. Um número finito de pontos também: um quadradinho para cada um. Um segmento de reta: um retângulo comprido e cada vez mais fino. E daí saem duas regras úteis. Um pedaço de um conjunto de conteúdo nulo também tem conteúdo nulo, e juntar um número finito desses conjuntos continua dando conteúdo nulo. Agora, um disco cheio não tem. Para cobri-lo, os retângulos gastam pelo menos a área do disco, e um orçamento menor que isso nunca dá conta. Então a ideia não é o conjunto parecer fino no desenho. É dar para cobri-lo com área tão pequena quanto se queira.

### B4-1 · a parábola
**Tela:** D8 na parábola; as caixas se empilham numa coluna Δ × 4; 2 · 1 · 0,5.
> [curious] E uma curva inteira? Lembra da parábola do vídeo passado, xis ao quadrado? Divide o eixo em pedaços e, em cada pedaço, desenha uma caixa que vai do menor ao maior valor da curva ali. Juntas, as caixas cobrem a parábola. Agora o truque: a curva é crescente, então dá para empurrar as caixas para a direita e empilhar. Todas cabem numa coluna com a largura do maior lado e altura quatro, a subida total da parábola. Área total: no máximo quatro vezes o maior lado. Com quatro pedaços, dois; com oito, um; com dezesseis, meio. E refinando, fica tão pequena quanto se queira. O gráfico da parábola tem conteúdo nulo.

### B4-2 · a solda e o arco
**Tela:** D8 na solda (duas colunas) e no arco (uma coluna de altura 2); 1 · 0,5 · 0,25 · 0,125.
> [thoughtful] A solda não cresce o tempo todo: primeiro sobe, depois desce. Então separa os dois movimentos. As caixas da subida se empilham numa coluna de cinquenta e oito centésimos de altura, e as da descida numa de trinta e seis. Área total: no máximo noventa e quatro centésimos vezes o maior lado, que vai a zero junto com o maior lado. O arco do quarto de disco desce de dois até zero, então as caixas dele somam duas vezes o maior lado. Com quatro divisões, um metro quadrado; com oito, meio; com dezesseis, um quarto; com trinta e duas, um oitavo.

### B4-3 · o resultado geral
**Tela:** `f CONTÍNUA EM [a, b] ⇒ GRÁFICO DE f TEM CONTEÚDO NULO`; ícones de polígono, círculo e elipse com ✓.
> [serious] E dá para ir além dos exemplos: o gráfico de qualquer função contínua num intervalo fechado tem conteúdo nulo. Por quê? A área das caixas que cobrem o gráfico é exatamente a diferença entre a soma por cima e a soma por baixo da integral simples. E toda função contínua num intervalo fechado é integrável, então essa diferença vai a zero. O livro vai além: toda curva de classe cê um, ou seja, com uma parametrização de derivada contínua, também tem conteúdo nulo. E o mesmo vale para curvas feitas de um número finito desses pedaços: segmentos, polígonos, círculos, elipses e quase toda borda que aparece num problema. Para essas bordas, a primeira pergunta tem resposta: sim, a área some. Mas isso não quer dizer que qualquer fronteira imaginável tenha essa propriedade.

### B5-1 · interior, exterior e fronteira
**Tela:** D9, as três sondas no quarto de disco.
> [thoughtful] Agora a borda de uma região ganha nome matemático. Pega um ponto e desenha em volta dele uma bola aberta: um disquinho sem a circunferência da borda. Se dá para escolher uma bola inteira dentro da região B, o ponto é interior. Se dá para escolher uma inteira fora, é exterior. Mas existem pontos em que nenhuma das duas coisas acontece: não importa o quanto a bola encolhe, ela sempre pega pontos de B e pontos de fora. Esses são os pontos de fronteira. No quarto de disco, a fronteira é o arco e os dois segmentos sobre os eixos. E um detalhe: um ponto de fronteira pode pertencer à região ou não.

### B5-2 · a borda é uma solda
**Tela:** D10 em Three.js; `BORDA = SOLDA ENTRE f E 0`.
> [excited] E aqui as duas primeiras perguntas se encontram. Lembra como se integra numa região que não é retangular? Coloca a região dentro de um retângulo maior e faz a função valer zero fora dela. No quarto de disco, a função vale um dentro e zero fora. E o que acontece quando você atravessa a borda? A função salta de um para zero! A borda funciona exatamente como a solda da chapa de dois metais. Olha o prédio: as tampas só aparecem nos retângulos atravessados pela fronteira. E, se a fronteira tem conteúdo nulo, a área dessas células pode ficar tão pequena quanto se queira. Uma borda curva e uma linha de solda eram o mesmo problema.

### B6-1 · um delta para a chapa inteira
**Tela:** a chapa x² + y² com tampas em todas as células; `E ONDE f É CONTÍNUA?`.
> [curious] Só que falta uma peça. Na chapa de dois metais, longe da solda, a densidade era constante, e as tampas eram zero. Mas numa densidade que varia, como xis ao quadrado mais ípsilon ao quadrado, quase toda célula tem o piso diferente do teto. Então não basta cuidar de onde a função salta: onde ela é contínua, as tampas também têm que poder ficar pequenas. E aí aparece um detalhe. Ser contínua quer dizer que, perto de cada ponto, a função muda pouco. Mas dá para escolher uma única distância que sirva para todos os pontos da chapa ao mesmo tempo?

### B6-2 · continuidade uniforme
**Tela:** D11, a régua de dois pontos; o enunciado escrito a caneta; `ε = 1 → δ = 0,17`.
> [thoughtful] Dá, quando a região é fechada e limitada e a função é contínua nela: é o teorema de Heine-Cantor. Para todo épsilon maior que zero, existe delta maior que zero tal que quaisquer dois pontos da região, xis e ípsilon maiúsculos, a menos de delta um do outro, têm valores que diferem menos que épsilon. As barras duplas lê-se norma: a distância entre os dois pontos. O mesmo delta serve para todos os pares, e por isso se chama continuidade uniforme. Na chapa de densidade xis ao quadrado mais ípsilon ao quadrado, o canto de cima é o mais exigente, porque a função muda mais rápido ali. Com épsilon igual a um, um delta de dezessete centésimos serve na chapa inteira. É esse delta que controla, ao mesmo tempo, a oscilação de todas as células pequenas.

### B6-3 · por que fechado e limitado?
**Tela:** D12, sen(1/x) na chapa sem a borda esquerda; a régua encolhe e a diferença continua 2.
> [curious] E por que a região precisa ser fechada e limitada? Olha esta função: seno de um sobre xis, numa faixa sem a borda onde xis vale zero. Perto dessa borda que falta, ela oscila cada vez mais rápido. Dá para achar dois pontos tão próximos quanto você quiser, um onde o seno vale um e outro onde vale menos um. A diferença continua dois, e nenhum delta serve para a faixa inteira. Numa região fechada e limitada, isso não acontece. Se a continuidade uniforme falhasse, haveria pares de pontos cada vez mais próximos com valores sempre longe um do outro. Só que, numa região fechada e limitada, esses pares se aproximam de um mesmo ponto da própria região. E ali a função seria descontínua. Contradição.

### B7-1 · separando os pontos problemáticos
**Tela:** D13, etapas 1 a 3: cobertura de D (< ε₁), engorda (< 2ε₁), grade fina; zoom na célula que encosta na cobertura (§2, item 3).
> [serious] Agora a demonstração principal, juntando tudo. Pega uma função limitada num retângulo: existe um número eme maiúsculo que limita o módulo dos valores dela. E chama de D o conjunto dos pontos onde ela não é contínua, com conteúdo nulo. O objetivo é provar que ela é integrável. Primeiro, cobre D com um número finito de retângulos, gastando área total menor que épsilon um. Depois, engorda um pouquinho esses retângulos, sem passar de duas vezes épsilon um. Por que engordar? É uma margem de segurança: toda célula pequena da grade que encosta na cobertura original fica inteira dentro da cobertura engordada. Fora da cobertura, sobra uma região fechada onde a função é contínua, então a continuidade uniforme controla a função ali. Agora escolhe uma grade fina o bastante para respeitar as duas coisas: a margem e o delta da continuidade uniforme.

### B7-2 · dois grupos de tampas
**Tela:** D13, etapas 4 e 5: calmas e vermelhas, as duas cotas; `S(P) − s(P) < αε₂ + 4Mε₁`; `αε₂ < ε/2` e `4Mε₁ < ε/2` (§2, item 4).
> [thoughtful] As células da grade se dividem em dois grupos. O primeiro é o das células calmas, longe dos pontos problemáticos. Nelas, a continuidade uniforme garante que o teto e o piso estão muito próximos: cada tampa tem altura menor que épsilon dois. E a área total delas não passa da área do retângulo, que a gente chama de alfa. Contribuição: menos que alfa vezes épsilon dois. O segundo grupo é o das células vermelhas, perto das descontinuidades. Ali a função pode variar bastante, mas o módulo dela nunca passa de eme, então a tampa nunca passa de dois eme. E essas células cabem na cobertura engordada, de área menor que dois épsilon um. Contribuição: menos que quatro eme épsilon um. Somando os dois grupos, esse maiúsculo menos esse minúsculo de P é menor que alfa épsilon dois mais quatro eme épsilon um. Agora escolhe os dois épsilons para que cada parcela fique menor que metade da tolerância. As tampas somem! E, pelo critério do começo da aula, a função é integrável.

### B7-3 · o teorema
**Tela:** `TEOREMA 1`, o corolário (D = ∅), `TEOREMA 2` e a observação, em caixas de contorno fino.
> [excited] E esse é o teorema: se uma função é limitada num retângulo e o conjunto dos pontos onde ela é descontínua tem conteúdo nulo, então ela é integrável. Repara na força disso. Não precisa calcular o valor da integral nem testar mil grades: basta verificar duas propriedades da função. E sai uma consequência imediata. Se a função é contínua no retângulo inteiro, o conjunto das descontinuidades é vazio, e o vazio tem conteúdo nulo. Então toda função contínua num retângulo é integrável. Dá para ir além: numa região limitada com fronteira de conteúdo nulo, estende a função por zero. Se ela é contínua e limitada na região, a extensão só pode ser descontínua na fronteira, e o teorema garante a integral. E o livro ainda observa: pode ter descontinuidades dentro da região também, desde que fiquem num conjunto de conteúdo nulo.

### B7-4 · as três respostas
**Tela:** a fileira dos três painéis do hook volta e ganha os ✓; régua com 7,06.
> [happy] Agora volta nas três perguntas. O quarto de disco: a fronteira é um arco e dois segmentos, todos com conteúdo nulo. Então a função que vale um dentro e zero fora é integrável, e a área existe: é pi. A chapa de dois metais: a densidade fica entre um e três e só é descontínua na solda, que é o gráfico de uma função contínua e tem conteúdo nulo. A massa está bem definida: sete vírgula zero seis quilos, mais ou menos. E a chapa de densidade xis ao quadrado mais ípsilon ao quadrado: a função é contínua no retângulo inteiro, então é integrável, sem refazer a conta do dezesseis delta. Três problemas diferentes, um teorema só.

### B8-1 · a função de Dirichlet
**Tela:** D15, a célula com duas cores e o zoom que não muda; `POR CIMA = 4`, `POR BAIXO = 0`.
> [surprised] Mas toda função limitada é integrável? Não. Olha esta função estranha: vale um quando as duas coordenadas do ponto são números racionais, aqueles que se escrevem como fração de inteiros, e vale zero nos outros casos. Pega qualquer retanguinho da grade. Por menor que seja, ele tem pontos com as duas coordenadas racionais e pontos com pelo menos uma coordenada irracional. Então, em todas as células, o piso é zero e o teto é um. A soma por cima dá sempre quatro, a área do quadrado, e a soma por baixo dá sempre zero. Refina quanto quiser: a diferença continua quatro. As paredes nunca se aproximam, e essa função não é integrável no sentido de Riemann.

### B8-2 · uma fronteira que não some
**Tela:** o conjunto dos pontos racionais (pontilhado) e a fronteira = o quadrado todo; `CONDIÇÃO SUFICIENTE`.
> [thoughtful] E isso responde à última dúvida do vídeo passado: existem bordas que não somem? Existem. Pega o conjunto dos pontos do quadrado com as duas coordenadas racionais. Qualquer disquinho dentro do quadrado encontra pontos dele e pontos de fora. Então a fronteira dele é o quadrado inteiro: não é uma curva, é uma região de área positiva, e não tem conteúdo nulo. Um último cuidado: o teorema dá uma condição suficiente. Quando as hipóteses valem, a integral existe com certeza. Quando não valem, isso sozinho não prova que ela não existe. Aqui, a não integrabilidade saiu direto das somas, que nunca se aproximam.

### B9-1 · o teste em três perguntas
**Tela:** D16, quatro cartões e o checklist (LIMITADA? · SALTOS EM CONTEÚDO NULO? · FRONTEIRA EM CONTEÚDO NULO?).
> [curious] Num exercício, o teorema vira três perguntas. A função é limitada? As descontinuidades ficam num conjunto de conteúdo nulo? E a fronteira da região tem conteúdo nulo? Os exemplos do livro passam nas três. Xis mais ípsilon no disco de raio um: contínua, e a fronteira é uma circunferência. Xis mais ípsilon entre as parábolas ípsilon igual a xis ao quadrado e ípsilon igual a um mais xis ao quadrado: a fronteira são dois gráficos e dois segmentos. No disco, a função que vale um acima do eixo xis e menos um abaixo: uma chapa de dois metais com solda reta. E xis ao quadrado sobre xis ao quadrado mais ípsilon ao quadrado, valendo um na origem: só é descontínua na origem, e um ponto tem conteúdo nulo. As quatro são integráveis.

### B9-2 · por que isso importa
**Tela:** três cartões pequenos: `DOIS MATERIAIS` · `DIVISA NO MAPA` · `ALVO REDONDO`.
> [excited] E isso aparece fora dos exercícios: uma peça feita de dois materiais, a densidade de população que muda na divisa entre duas cidades, a probabilidade espalhada por igual dentro de um alvo redondo e zero fora dele. Todas essas funções têm descontinuidades. Mas são limitadas, e as descontinuidades moram em curvas, então a integral existe. O teorema amplia muito o tipo de função que dá para integrar com segurança.

### S1 · síntese
**Tela:** `TAMPAS · CONTEÚDO NULO · CONTINUIDADE UNIFORME`, e o teorema fecha embaixo (§2, item 5); o muro coral na solda.
> [thoughtful] Então olha o caminho. A soma por baixo e a soma por cima prendem todas as aproximações, e a diferença entre elas é o volume das tampas. Onde a função é contínua, a continuidade uniforme achata as tampas todas de uma vez. Onde ela é descontínua, as tampas podem ser altas, mas os pontos problemáticos precisam ficar num conjunto de conteúdo nulo: um conjunto que dá para cobrir com um número finito de retângulos, gastando tão pouca área quanto se queira. Juntando as duas ideias, sai o teorema. Uma integral dupla não exige que tudo seja contínuo: o importante é controlar a diferença entre as aproximações.

### S2 · o próximo vídeo e CTA
**Tela:** cartão `NO PRÓXIMO VÍDEO: PROPRIEDADES DA INTEGRAL DUPLA`; a chapa partida em duas regiões; `A SOLDA PESA ALGUMA COISA?`; depois o CTA padrão.
> [curious] Mas ficou uma pergunta. Na chapa de dois metais, dá para calcular a massa do pedaço leve e a do pesado separadamente. Então a massa total devia ser a soma das duas, certo? Só que os dois pedaços se encontram na solda, que fica na fronteira dos dois. Ela entra duas vezes na conta? E, no nosso modelo, a solda é uma linha sem espessura: ela tem alguma massa? No próximo vídeo, as propriedades da integral dupla: somar funções, tirar constante, comparar integrais, dividir a região em pedaços e entender por que mudar a função num conjunto de conteúdo nulo não muda a integral. [happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: em que outra situação uma grandeza muda de repente ao atravessar uma fronteira? Até a próxima!
