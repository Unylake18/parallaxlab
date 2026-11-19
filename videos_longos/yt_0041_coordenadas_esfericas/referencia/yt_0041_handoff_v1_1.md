# yt_0041 · CÁLCULO III · EP. 16 (provisório) · Coordenadas esféricas na integral tripla
## HANDOFF v1.1 para o Claude Code: preview visual do vídeo inteiro, com 3D em Three.js

Data: 2026-11-15 (v1.1: notação da lei de Gauss, ρ densidade, r distância, R raio fixo, s sombra; substitui a v1). Formato: `longo_horizontal`.

Unidade nova: `videos_longos/yt_0041_coordenadas_esfericas/`. Antes de criar a pasta:
- confira que o número `yt_0041` está livre em `videos_longos/`;
- a ordem esperada é: EP. 13 = `yt_0038` (massa e centro de massa), EP. 14 = `yt_0039` (exercícios do 3.4), EP. 15 = `yt_0040` (integral tripla).

Se `yt_0041` estiver ocupado, pare e reporte.

**Fase:** só o **preview visual silencioso** do vídeo inteiro, em 960×540 a 15 fps.
- O render não tem limite de tempo: o Kaio liberou render sem economia e 3D onde a câmera ajuda.
- Não gerar voz, SRT, master, 1080p nem entrega.
- Não fazer commit nem push.

Este handoff é autocontido. Tudo o que você precisa está nele e no zip `yt0041_handoff_v1_1_completo.zip`:
- `yt_0041_quadros_alvo_v1_1/` traz os **14 quadros-alvo** (1920×1080), a `00_folha_contato_v1_1.jpg` e os geradores:
  - `c3d41.html` (Three.js r128, `?k=<chave>`) gera as **cenas 3D de referência**. Ele tem a geometria, as câmeras, as cores e a projeção dos pontos de tela. Ao lado estão os `r3d_<chave>.png` e os pontos em `r3d_pts.json`. **Porte as cenas para a unidade** (§2.2): elas são o modelo exato.
  - `sb41.html` (Canvas + KaTeX, `?k=<chave>`) gera os quadros completos. Abra-o com as fontes, `logo_crop.png`, `katex/`, `three.min.js` e `r3d_pts.js` do lado. Chaves, na ordem dos alvos 01 a 14: `h1 h2 b1 b1b b13 b21 b22 b23 b24 b31 b4 b5 b6 s2`.
  - `r3d.js` e `shot.js` são os scripts Playwright que geraram os PNGs. Servem só de referência.
- `yt_0041_narracao_v1_1.md` é a **narração**: 3.538 palavras ≈ 19:49, por âncora, com a **Tela** e os **Gatilhos** de cada âncora e a tabela de leitura dos símbolos. É ela que dá os tempos e as frases de disparo.
- `calculo3_35t2_coordenadas_esfericas_proposta_v1_1.md` é a proposta (contexto; a conta inteira C1–C10 está no §3 dela e repetida aqui no §4).
- `verificacao/verifica_calc3_35t2_sympy.py` e a saída dele somam **63 checagens, todas `True`**.

A matemática, o roteiro, a narração e os textos são especificação. Não rediscuta. Se encontrar uma inconsistência objetiva, reporte antes de mudar.

**Regras da série (Kaio):**
- **Figura:** toda definição ou enunciado formal aparece com a sua figura.
- **Origem:** todo símbolo nasce do desenho (`TransformFromCopy` do objeto para a fórmula) ou pela caneta. Nada aparece pronto.
- **CONTA INTEIRA:**
  - primitiva com colchete → F(b) − F(a) com os valores substituídos → número;
  - substituição com a linha `u = …, du = …` **e** a linha dos limites novos (e o sinal quando o limite inverte);
  - nenhum degrau pulado; a voz lê cada degrau, e a tela escreve cada degrau no gatilho da voz.
- **Grade na tela inteira:** toda cena 2D tem o papel de quadradinhos de borda a borda. Só o 3D Three.js e o cartão do CTA ficam lisos (§2.1).
- **Simplicidade:** nada de partícula, brilho, sombra, névoa, transparência, pulso, luz que lava a cor ou câmera girando sem motivo.

**Lições dos EP. 06 a 13, já incorporadas aqui** (não as repita):
- MF-Tools de verdade, sem mapa de glifos próprio com `FadeIn`;
- **nenhum pulso automático**: se o kit copiado tiver palco "vivo" (`_pulso`, `_pulso_v2`, `_wait_vivo`), desligue (`_sem_vivo = True` ou equivalente) e confirme com `grep` no log (§8);
- **nenhum fantasma nos voos**: o `TransformFromCopy` sai da fonte sem deixar contorno no pouso, e nenhum glifo é mapeado duas vezes;
- grade de borda a borda, nunca em caixa recortada;
- nenhum bloco abrindo vazio; palco parado medido só no palco;
- algarismos ≥ 30 px a 1080p, legendas ≥ 26 px, índices ≥ 22 px;
- coluna com ≤ 6 linhas por etapa (no máximo 8, com chips), renovando a tela quando passar;
- R5 testado também durante as animações;
- frase portuguesa sempre em Space Grotesk, nunca dentro de `MathTex`; `\dfrac` sempre;
- cartão do próximo vídeo por ≥ 8 s;
- no 3D, a peça nunca se separa: o lado de fora do corte vira traço `#6C7698`.

**A imagem-mãe deste vídeo:** **a célula esférica lima**, o pedaço entre duas cascas, dois cones e duas páginas. Ela aparece:
- no hook, com "?" (polo e equador);
- na caixa rφθ e na bola (B1-3);
- ampliada, com as três arestas (B2-1);
- no teste da bola e no teorema.

---

## 0. O que entregar

1. A unidade nova, com:
   - `ficha.md` (§1);
   - `cena.py` e uma `sec_*.py` por bloco (H, A, B1 … B7, S);
   - `threejs/`, com as cenas 3D, o renderizador por quadro e os pedidos (§2.2).
2. O preview do vídeo inteiro, `renders/v1/yt_0041_preview_v1_540p15.mp4`, com a duração da narração (§6). Junto, `duracoes_estimadas.json`.
3. A prancha **render × alvo** `renders/v1/qa/comparacao_v1.jpg`, uma linha por quadro-alvo: o still do render no gatilho ao lado do alvo, para os 14 alvos.
4. Os relatórios de QA em `renders/v1/qa/` (§8):
   - `sobreposicoes_v1.txt`
   - `alinhamento3d_v1.txt`
   - `flash_por_quadro_v1.txt`
   - `palco_parado_v1.txt`
   - `grade_v1.txt`
   - `colunas_v1.txt`
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
serie_publica: CÁLCULO III · EP. 16 (provisório)
titulo: Coordenadas esféricas na integral tripla
disciplina: Cálculo III
modulo: 3.5 Integral tripla (o docs/mapa_curricular.md do repositório ainda usa a numeração antiga)
bloco: 3.5-T2
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §5.5 (coordenadas esféricas; teorema de mudança de variáveis; Ex. 5, bola com densidade igual à distância; Exercício 5.5-4, cone + esfera); Stewart §15.8 (cunha esférica, casquinha). Só na descrição do YouTube: nada de livro na tela nem na fala
unidades: r, x, y, z, s e R em metros; φ e θ em radianos; volumes em m³
notacao: igual aos vídeos da lei de Gauss: ρ = densidade; r = distância ao centro (variável); R = raio fixo da bola (no lugar do a dos episódios anteriores); s = r sen φ, a sombra no chão (como o s do Griffiths); φ = ângulo a partir de +z, em [0, π]; θ = ângulo das polares; T = a transformação
solido_3d: nenhum do arsenal Blender (bola, cascas, cones, caixa e lata feitos direto em Three.js)
3d_threejs: bola (degradê radial de densidade, cunha de 90°), grade, superf, ponto, caixa, caixa2, bolagrade, caixinha, cebola, casquinha, lata (geometria em yt_0041_quadros_alvo_v1_1/c3d41.html)
duracao_alvo: ≈ 19:49 (narração v1.1: 3.538 palavras)
```

## 2. Base de código

### 2.1 Manim

- **Antes de começar:**
  - leia `docs/estado_atual.md`;
  - rode `verificacao/verifica_calc3_35t2_sympy.py` com o Python da `.venv`. As 63 linhas devem dar `True`. O sympy já foi instalado na `.venv` (EP. 11); se faltar o scipy, a linha B5f falha sozinha: diga no relatório e siga.
- **Copie, não importe.** Copie o kit da unidade mais recente da série de Cálculo III que estiver no seu checkout, nesta ordem: `yt_0040_*`, `yt_0039_*`, `yt_0038_*`, `yt_0037_*`. Do kit vêm:
  - `kit.py` e `render.sh`;
  - o canto de duas linhas e `placa_min`;
  - a caneta (`TC`/`TX`), `painel`, `mixl`, `chip` e o sublinhado de leitura;
  - a reta-sonda com os pontos de entrada e saída.

  Não altere as outras unidades. Se o kit tiver pulso automático, desligue-o (ver "Lições").
- **Fundo:**
  - **Cenas 2D** (B2-2, B2-3, os painéis do B3-1, A1, S1 e o cartão do S2): violeta liso `#18143A → #0F0C26` na câmera + o papel **de borda a borda**: `papel(ax)` **sem `area`** quando há eixos (nasce dos eixos, quadradinho 0,25, sem linhas grossas); `papel(passo=0.5)` quando não há eixos. Painéis e cartões por cima do papel têm fundo opaco.
  - **Cenas 3D:** só o violeta liso. A grade entra no pouso, quando o 3D sai e a cena seguinte é 2D.
  - O CTA final fica liso.
- Render por bloco (`render.sh <Classe>`), depois concatene.
- **Sem economia artificial**, mas sem updater à toa. Cada um destes é um `ValueTracker` só:
  - a câmera que gira no H1 e no B6-1 (um parâmetro de ângulo, com início e fim suaves);
  - a célula que se deforma da caixa para a bola no B1-3;
  - a sonda radial do B3-2, do B6-1 e do S2 (comprimento de 0 até a saída).
- Limpe da cena o que saiu da tela. Não deixe nada invisível acumulando.

### 2.2 Three.js (o pipeline da série)

- **Copie o pipeline** da unidade de Cálculo mais recente que tiver `threejs/` (yt_0038, yt_0037 ou yt_0036). Vêm `r3d.js`, `package.json` (playwright-core), `cena3d/three.min.js` (r128) e o esquema de pedidos:
  1. a passagem seca do Manim grava `pedidos3d/<LOTE>.json`;
  2. `r3d.js` chama `window.setEstado(estado)` quadro a quadro e grava os PNGs com alfa e o `pontos.json`;
  3. o Manim cola os PNGs em tela cheia e prende os rótulos nos pontos.
- **Porte as cenas de `c3d41.html`** para `threejs/cena3d/`. Vêm de lá:
  - `sph(r, φ, θ)` e `WS(r, φ, θ)` (mundo = `SC` · metros);
  - `sup(F, a0, a1, b0, b1, na, nb, cor)` (superfície parametrizada com tom fixo por normal), `tubo`, `tracejado`, `seta`, `arco`;
  - `tom(cor, n)` com a luz fixa `LDIR = (0,55; −0,75; 0,45)`: o tom da face é calculado uma vez, sem iluminação dinâmica;
  - `corDens(r)`: a rampa `#10243A → #35D9FF` da densidade (expoente 0,85);
  - `celula(r1, r2, f1, f2, t1, t2)`, `esferaTraco`, `bolaCortada`;
  - a câmera `ver(pos, alvo, cx, cy)` com o fator `DF` de distância e `setViewOffset`; a projeção dos pontos é feita depois de `ver()` (`projAll()`).
  - Cunha das bolas: 90°, centrada em `CAZ = atan2(−6,2; 9,2)` (de frente para a câmera). Casquinha e lata: cunha `[CA − 20°, CA + 90°]`, com a sonda na página `tb − 0,035`.

  **Atenção:**
  - `c3d41.html` desenha só o estado final de cada chave. A animação entre os estados é sua.
  - Nos alvos, o PNG 3D foi colado com deslocamento e escala (`sb41.html`, função `cena3d(k, {dx, dy, esc})`): h1 (−60, 30, 1); h2 (−30, 80, 0,94); b1 e b1b (−80, 40, 1); b21 (−110, 150, 1); b24 (−180, 60, 0,9); b31: caixa2 (20, 40, 0,56) e bolagrade (700, 40, 0,56); b4 (−80, 30, 1); b5 (−100, 30, 1); b6 (−90, 40, 1); s2 (−20, 150, 0,8). Reproduza o enquadramento com `setViewOffset`/zoom, não redimensionando o PNG.
- **Cenas e estados:**

  | cena | câmera (`ver`) | estados | o que anima |
  |---|---|---|---|
  | `bola` | `[9.2, −6.2, 4.3] → [0, 0, 0]`, `SC = 2` | `gira` 0→1 · `cunha` 0→1 · `casca084` 0/1 | **H1:** a bola inteira com o degradê, a câmera gira ~40° em ~5 s e para no quadro do alvo; a cunha de 90° abre (≈ 1,5 s) e mostra o degradê por dentro. **B5:** volta parada; em "metade da massa", a casca de r = 0,84 a 1 ganha o contorno laranja (sem brilho) |
  | `grade` / `superf` | `[9.0, −6.8, 4.0] → [0, 0, 0,05]`, `SC = 2,1` | `familias` 0→3 · `celulas` 0/1 | **H2:** a bola perde o degradê e vira traço; entram uma por vez a meia casca laranja, o cone φ = π/4 violeta e a página θ = −π/4 verde-água (`superf`); elas saem e ficam as duas células lima (`grade`: polo φ ∈ [0, π/6], equador φ ∈ [π/3, π/2], r ∈ [0,5; 1]) |
  | `ponto` | `[8.6, −5.4, 4.4] → [0, 0,6, 0,95]`, `SC = 1,35` | `rho`, `fi`, `teta`, `pagina`, `sombra` (0/1 cada) | **B1-1:** P, depois o segmento r, o arco φ, a página (chapada, `#1E3A4A`, contorno fino), a sombra s e o arco θ, cada um no seu gatilho. **B1-2:** igual, com os números (os números são do Manim) |
  | `caixa` / `caixa2` | `[8.2, −5.6, 5.6] → [1,15; 1,45; 1,0]`, `SC = 1` | `bordas` 0→3 · `parte` 0→1 | **B1-3:** a caixa (r, φ, θ) com a grade fina nas faces e a célula lima; as faces ruins tracejadas em ALERTA uma por vez. **B3-1:** `caixa2`, a caixa se parte em θ = π (as metades se afastam 0,15 e voltam: é o único afastamento do vídeo, e a peça volta a se fechar) |
  | `bolagrade` | `[9.0, −6.8, 4.0] → [0, 0, 0,05]`, `SC = 2,1` | `costura` 0/1 · `celula` 0/1 | **B1-3 e B3-1:** a bola em traço com a célula lima, a costura θ = 0 em ALERTA, o eixo z tracejado e a origem. **B2-4:** o mesmo, parado ao lado da coluna |
  | `caixinha` | `[7.2, −6.4, 4.9] → [0,95; 0,45; 0,35]`, `SC = 2,6` | `aresta` 0→3 · `raioPar` 0/1 | **B2-1:** a câmera chega na célula (corte seco do B1-3 é aceitável); as arestas acendem uma por vez (Δr laranja, rΔφ violeta, r sen φ Δθ verde-água); depois o raio do paralelo em pêssego tracejado |
  | `cebola` | `[9.2, −6.2, 4.3] → [0, 0, 0]`, `SC = 2,1` | `cascas` 0→5 | **B4:** a casca de r ∈ [0,6; 0,7] laranja; em "a bola é uma cebola", 5 cascas finas se acendem do centro para fora (só contorno, sem brilho), e fica a casca do alvo |
  | `casquinha` | `[8.6, −6.4, 4.6] → [0, 0, 1,2]`, `SC = 1,55` | `gira` 0→1 · `sonda` 0→1 · `duas` 0/1 | **B6-1:** gira ~30° e para no alvo; a sonda laranja cresce da origem até a calota. **B6-2:** em "Confere pela geometria", o cone fica violeta e a meia bola de cima ciano (só a cor muda; a peça não se separa) |
  | `lata` | `[8.4, −6.3, 4.4] → [0, 0, 0,6]`, `SC = 2,2` | `sonda1`, `sonda2`, `quina` (0/1) | **S2:** a lata cortada em cunha; a sonda da parede (φ = π/3), a da tampa (φ = π/8) e a diagonal da quina tracejada em coral |

- **Estilo 3D da série:** opaco (`MeshBasicMaterial`, tom fixo por face); sem sombra, névoa, brilho ou transparência; `outputEncoding` linear e antialias ligado.
- **Rótulos são do Manim**, presos aos pontos do `pontos.json` do mesmo quadro (≤ 2 px). Pontos já exportados por `c3d41.html`:
  - `bola`: `centro`, `casca`, `faceMeio`, `faceBorda`, `faceB`, `raio`, `topo`, `ex`, `ey`, `ez`;
  - `grade`: `celPolo`, `celEq`, `ez`;
  - `ponto`: `P`, `P1`, `meioRho`, `meioR`, `arcoFi`, `arcoTh`, `zEixo`, `O`;
  - `caixinha`: `dRho`, `dFi`, `dTh`, `raioPar`, `arcoFi`, `ez`;
  - `casquinha`: `saida`, `cone`, `calota`, `encontro`, `arcoFi`, `um`, `ez`;
  - `lata`: `parede`, `tampa`, `quina`.
- **Câmera:**
  - no máximo um movimento por ideia;
  - **a câmera nunca se mexe enquanto uma fórmula está sendo escrita**;
  - nada de órbita contínua;
  - nada do 3D passa da borda esquerda da coluna menos 30 px.
  - No alvo 06 (`caixinha`) e no alvo 02 (`grade`), o eixo z não pode cruzar o título do canto: o alvo já está ajustado (o rótulo `z` do eixo sai na caixinha).

## 3. Sistema visual

### 3.1 Layouts (px a 1080p)

| alvo / bloco | geometria |
|---|---|
| 01 · H1 | 3D `bola` à esquerda (centro ≈ (540, 590)). Coluna em x = 1020, de y ≈ 210 a 830 |
| 02 · H2 | 3D `grade` à esquerda. Painel `A GRADE NOVA` em (1180, 330), 640 × 420 |
| 03, 04 · B1-1, B1-2 | 3D `ponto` à esquerda. Coluna em x = 1090 (B1-1 e B1-2) |
| 05 · B1-3 | Caixa à esquerda (≈ 100–650), seta `T` em x ≈ 760–880, bola em ≈ (1010, 570). Coluna `BORDAS RUINS` em x = 1450 |
| 06 · B2-1 | 3D `caixinha` à esquerda. Coluna em x = 1000–1080; painel numérico em (1060, 660), 780 × 300 |
| 07 · B2-2 | 2D, papel de borda a borda. Painel `NA PÁGINA θ` com origem em (230, 800), u = 250; painel `NO CHÃO` com origem em (1020, 800), u = 250; cartão `OS FATORES SE MULTIPLICAM` em (1500, 330), 380 × 330 |
| 08 · B2-3 | 2D, papel de borda a borda (passo 0,5). Matriz em x = 90–1040, y ≈ 270–500; expansão em y ≈ 650; linhas seguintes em y ≈ 800 e 900; chip `dV` à direita da moldura |
| 09 · B2-4 | 3D `bolagrade` à esquerda (esc 0,9). Coluna em x = 960; painel de erros em (950, 710), 900 × 250 |
| 10 · B3-1 | Em cima: `caixa2` (esc 0,56) à esquerda, seta `T`, `bolagrade` (esc 0,56) à direita, `O CORTE: VOLUME ZERO` em x = 1380. Embaixo: painel do enunciado em (60, 660), 1800 × 360 (margem de baixo de 60 px) |
| 11 · B4 | 3D `cebola` à esquerda. Coluna em x = 1060 |
| 12 · B5 | 3D `bola` à esquerda (centro ≈ (500, 580)). Coluna em x = 1010 |
| 13 · B6 | 3D `casquinha` à esquerda. Coluna em x = 1010 |
| 14 · S2 | 3D `lata` à esquerda (esc 0,8). Coluna em x = 1120; cartão `NO PRÓXIMO VÍDEO` com moldura em (1120, 420), 680 × 300 |

Conversão para o Manim: x_m = (x_px − 960)/120; y_m = (540 − y_px)/120 (o `config_horizontal.py` usa frame 16 × 9, então 120 px por unidade).

### 3.2 Regras (as da série)

- **R1 · Clareira:** nenhum rótulo sobre ponto, aresta, linha da grade ou número; o rótulo sai para o lado.
- **R2 · Placa:** todo rótulo solto sobre o desenho ou o 3D usa `placa_min`.
- **R3:** fórmula nova nunca nasce sobre fórmula velha; a coluna limpa antes.
- **R4:** rótulo junto do objeto que ele nomeia; o rótulo sai junto com o seu objeto.
- **R5:** QA automático de sobreposição a cada 0,2 s, **inclusive durante as animações e os voos** (§8).
- **R6:** nada sai da moldura do seu painel ou cartão; o 3D não invade a coluna; margem de 48 px na borda da tela.
- **R-texto:**
  - **Palavra é Space Grotesk** (`Text`, maiúsculas); matemática é `MathTex`. Nenhuma frase portuguesa dentro de `MathTex`.
  - `TRAVA`, `RAIZ E LOGARITMO JÁ NA DE DENTRO`, `LEVE NO CENTRO`, `PESADA NA CASCA`, `CASCAS`, `CONES`, `PÁGINAS`, `MESMO`, `SOMBRA NO CHÃO`, `UMA CAIXA!`, `BORDAS RUINS`, `ARESTA 1/2/3`, `ARCO = RAIO · ÂNGULO`, `RAIO DO PARALELO`, `POLO`, `EQUADOR`, `RAZÃO`, `NA PÁGINA θ`, `NO CHÃO`, `FATOR`, `OS FATORES SE MULTIPLICAM`, `LINHA DE BAIXO`, `SEM`, `METRO`, `UNIDADE CERTA, NÚMERO ERRADO`, `NO INTERIOR`, `DE CLASSE`, `COMPACTO`, `METADE`, `O CORTE: VOLUME ZERO`, `ÁREA DA ESFERA`, `ENGORDAR = UMA CASCA`, `MÉDIA`, `MASSA ATÉ`, `CONFERE`, `CONE`, `ESFERA`, `CONE + MEIA BOLA`, `MESMO INTEGRANDO`, `RACHA EM` e o cartão são `Text`.
  - Linhas mistas são `Text` + `MathTex` lado a lado, com respiro ≥ 0,15 (`mixl()`).
  - Cada legenda tem no máximo 6 palavras e ≥ 26 px. Exceções: a legenda do teorema (`NO INTERIOR: …`, uma linha só a 26 px) e `UNIDADE CERTA, NÚMERO ERRADO (O CERTO ≈ 4,19 R³)`.
- **Fração:** sempre `\dfrac`, com o glifo ≥ 26 px; nos rótulos de ângulo, `\pi/4` em linha. `grep -n tfrac` = 0. Nenhum rótulo girado.
- **Decimais** com `{,}`; zero em legenda vai por extenso, zero como valor é `MathTex`.
- **Sublinhado de leitura:** quando a voz lê um símbolo (tabela de leitura da narração), um sublinhado fino aparece sob ele no gatilho e sai. Não é pulso nem brilho.
- **Um movimento por ideia, uma vez.** Uma figura nova nasce da velha (`ReplacementTransform`) e nunca pisca.
- **Nenhum bloco abre vazio:** a linha 2 do canto está na tela desde o primeiro quadro; palco vazio por mais de 0,5 s: zero.
- **Palco parado:** NÃO é portão automático. Desenho pronto com a voz explicando é aceitável; erro é só tela vazia (> 0,5 s) ou a voz falando de algo que ainda não está na tela. Proibido "animar a espera": nada de pulso, traço que acende, ponto correndo (tracer) ou 3D que escurece. O relatório lista os trechos parados acima de 5 s com o que a voz lê neles.
- **Pontos só os do alvo:** P, a origem, o encontro da casquinha, as saídas das sondas. Nenhum ponto de debug.
- **Canto:** linha 1 `CÁLCULO III · INTEGRAL TRIPLA`; linha 2 = o título da cena no alvo (`A BOLA PESADA NA CASCA`, `QUAL É O VOLUME DE CADA PEDAÇO?`, `O ENDEREÇO ESFÉRICO`, `UM PONTO DE EXEMPLO`, `A CAIXA VIRA A BOLA`, `A CAIXINHA CURVA`, `DUAS POLARES EM SEQUÊNCIA`, `O DETERMINANTE`, `O TESTE: A BOLA`, `O TEOREMA`, `A BOLA É UMA CEBOLA`, `DE VOLTA À BOLA`, `A CASQUINHA`, `E UMA LATA?`). Para B3-2, B7 e S1, que não têm alvo: `A RECEITA`, `QUANDO USAR` e `RESUMINDO`.

### 3.3 Cores

| Papel | Cor |
|---|---|
| **r** (variável, segmento, cascas, `dr`, `Δr`, a sonda, aresta 1) | laranja `#FF9440` |
| **φ** (variável, arco a partir de +z, cones, `dφ`, `Δφ`, aresta 2) | violeta `#B48CFF` |
| **θ** (variável, arco no chão, páginas, `dθ`, `Δθ`, aresta 3) | verde-água `#2EE6A6` |
| s, a sombra no chão, o raio do paralelo | pêssego `#FFC08A` |
| x, `dx` | âmbar `#FFC24D` |
| y, `dy` | magenta `#EA63FF` |
| z, `dz`, o eixo z | azul `#5AA2FF` |
| **o fator r² sen φ** (sempre o bloco inteiro), a célula | lima `#C6F26B` |
| ρ, a densidade, o degradê da bola, `√(x² + y² + z²)` como função | ciano `#35D9FF` |
| u da substituição, `du` | `#E08A3C` |
| Entrada / saída da sonda; metade θ ≤ π / θ ≥ π | azul-claro `#7FB2FF` / coral `#FF7A8A` |
| A esfera r = 2 cos φ (limite de cima da casquinha), a racha da lata | coral `#FF7A8A` |
| Resultado final, ✓ | menta `#8CFFD2` |
| Erro clássico, `TRAVA`, bordas ruins, a costura, `SEM …` | ALERTA `#FF5D5D` |
| Grade, réguas, molduras, legendas secundárias | GEO `#B8C4DA` |
| Traço do lado de fora do corte (3D) | `#6C7698` |

- Operadores (∫, ∭, ≤, ⇒, [ ], ( ), =) ficam em branco, e a cor vai na grandeza.
- **Dois r na mesma linha (B5):** o r da densidade fica **ciano** (é o valor de ρ); o r² sen φ do jacobiano fica **lima**. Em `r · r² sen φ`, o primeiro r é ciano. Depois do glyph map para `r³ sen φ`, o bloco fica branco com r laranja (já não dá para separar).
- **Limite de cima de dentro:** o limite inteiro na cor da superfície (coral em `2 cos φ`), e só a variável dentro dele na cor dela (o φ em violeta).

### 3.4 Álgebra

- **Caneta** em toda fórmula nova: traço finíssimo (~0,7), glifo a glifo, da esquerda para a direita, preenchendo na cor da grandeza, sem flash e sem preview do destino.
- **Voos obrigatórios** (`TransformFromCopy` em arco, sem deixar fantasma). No 3D, o voo parte do ponto projetado:
  - **H1:** nenhum voo (o hook só pergunta).
  - **B1-1:** `r` voa do segmento, `φ` do arco junto do eixo, `θ` do arco no chão; o `s` da linha `x = s cos θ` voa da linha `s = r sen φ`, e depois `r sen φ` voa da mesma linha para dentro do `x` e do `y`.
  - **B1-2:** `2`, `π/6` e `π/3` voam do desenho para a linha do ponto; o `√3` e o `1` do resultado voam para a altura e para a sombra no desenho (sentido inverso).
  - **B1-3:** os intervalos `[0, 1]`, `[0, π]`, `[0, 2π]` voam das arestas da caixa (rótulos `1`, `π`, `2π`); cada linha de `BORDAS RUINS` nasce da face que acende.
  - **B2-1:** `Δr`, `rΔφ` e `r sen φ Δθ` voam das arestas (na cor de cada uma) para a linha `ΔV ≈`; os valores do painel voam da célula do polo e da do equador do H2 (miniaturas no painel).
  - **B2-2:** o `r` do resultado da página voa para o cartão; o `s` do `FATOR s` voa do painel do chão; `r sen φ` voa do rótulo `s = r sen φ` do painel da página.
  - **B2-3:** cada entrada da matriz é escrita no gatilho da derivada falada; `cos φ` e `−r sen φ` do termo 1 e do termo 2 voam da linha de baixo da matriz.
  - **B2-4:** `R`, `π` e `2π` voam da bola (raio, eixo, volta); `R³/3`, `2` e `2π` voam das linhas 2–4 para a linha V.
  - **B3-1:** o lima `r² sen φ` voa do chip `dV` (miniatura do B2-3) para o lugar do módulo do jacobiano.
  - **B4:** `4πr²` voa da linha 2 para a integral V.
  - **B5:** o `r` da densidade voa do chip `x² + y² + z² = r²` (B1-2, miniatura); `π` voa do resultado para MÉDIA e para MASSA ATÉ c.
  - **B6-1:** `π/4` voa do cone, `2 cos φ` voa da calota (coral) para o limite de dentro.
  - **B6-2:** `(8/3) cos³φ sen φ` voa da linha 1 para a integral em u; `π/3` e `2π/3` voam das duas peças coloridas.
  - **S1:** os três resultados voam das suas fontes (B2-4, B5, B6-2).
- **MF-Tools de verdade:**
  - `from MF_Tools import TransformByGlyphMap` (1.4.9), com `MathTex` de string única nos dois lados e mapa explícito;
  - o glifo que sai usa `auto_fade`; o glifo que **entra** nunca usa `FadeIn`: fica fora do mapa e é escrito com a caneta, ou voa da fonte;
  - a linha antiga nunca é remapeada depois que outra linha nasceu dela; cancelamento em dois tempos (acende, depois sai);
  - `show_indices` só no desenvolvimento.
- **Glyph maps obrigatórios (17):**
  1. B1-2: `1/4 + 3/4 + 3` → `4` → `2²`.
  2. B2-1: `Δr · rΔφ · r sen φ Δθ` → `r² sen φ Δr Δφ Δθ` (os dois r se juntam em r², que vira lima com o sen φ; os Δ vão para o fim).
  3. B2-2: `cos φ · r cos φ − (−r sen φ) · sen φ` → `r cos²φ + r sen²φ` → `r(cos²φ + sen²φ)` → `r` (o parêntese acende como `= 1` e some).
  4. B2-2: `r · s` → `r · r sen φ` → `r² sen φ`.
  5. B2-3: a linha da expansão → `r² sen φ cos²φ + r² sen³φ` (as chaves `= 1` acendem e saem; `cos φ · cos φ` → `cos²φ`; `sen φ · sen²φ` → `sen³φ`; o `+ 0` sai).
  6. B2-3: `r² sen φ cos²φ + r² sen³φ` → `r² sen φ (cos²φ + sen²φ)` → `r² sen φ`.
  7. B2-4: `R³/3 · 2 · 2π` → `4πR³/3`.
  8. B2-4: `R · 2 · 2π` → `4πR` e `R³/3 · π · 2π` → `2π²R³/3`.
  9. B3-1: `∭_{B_uvw} f(T(u, v, w)) |∂(x, y, z)/∂(u, v, w)| du dv dw` → `∭_{B_rφθ} f(T(r, φ, θ)) r² sen φ dr dφ dθ`.
  10. B4: `r² · [−cos φ]₀^π · [θ]₀^{2π}` → `r² · 2 · 2π` → `4πr²`.
  11. B4: `4π[r³/3]₀^R` → `4πR³/3`.
  12. B5: `r · r² sen φ` → `r³ sen φ`; depois `(1/4 − 0) · (1 + 1) · (2π − 0)` → `1/4 · 2 · 2π` → `π`.
  13. B5: `π/(4π/3)` → `π · 3/(4π)` → `3/4` (o π cancela em dois tempos).
  14. B5: `πc⁴ = π/2` → `c⁴ = 1/2` → `c = ⁴√(1/2)`.
  15. B6-1: `r cos φ = r sen φ` → `tg φ = 1` → `φ = π/4`; `r² = 2r cos φ` → `r = 2 cos φ` (um r de cada lado acende e sai, com a placa `(r > 0)`).
  16. B6-2: `(2 cos φ)³/3 · sen φ` → `(8/3) cos³φ sen φ`; `∫₀^{π/4} (8/3) cos³φ sen φ dφ` → `(8/3)∫₁^{√2/2} u³ (−du)` → `(8/3)∫_{√2/2}^{1} u³ du` (**os limites trocam de lugar e o menos sai**, no mesmo mapa).
  17. B6-2: `(8/3)(1/4 − 1/16)` → `(8/3)(3/16)` → `1/2` (8 com 16, 3 com 3, em dois tempos); `2π · 1/2` → `π`; `π/3 + 2π/3` → `π`.
- **Linhas de substituição e de limites** (CONTA INTEIRA): no B6-2, `u = cos φ, du = −sen φ dφ` e `φ = 0 → u = 1, φ = π/4 → u = √2/2` são escritas a caneta **antes** do glyph map 16, cada uma no seu gatilho.
- **Tamanhos:** fórmula principal 40–48 px; secundária 32–38 px; índice ≥ 22 px; algarismos ≥ 30 px; nada menor que 26 px fora dos índices.
- **Arredondamento:** o exato vem antes do decimal, e o decimal sempre com `≈`.
- **Colunas longas** (≤ 6 linhas por etapa, ≤ 8 com chips): B5 em duas etapas (até `= π` ✓; depois MÉDIA e MASSA ATÉ c); B6 em duas telas (B6-1: CONE, ESFERA, V montada; B6-2: a conta, com a V montada pequena no topo). A tela velha sobe e sai, sem `FadeOut` de tudo de uma vez.

## 4. Números e a conta inteira (todos no script, 63/63)

O texto exato de cada linha está no §3 da proposta (C1–C10, mais a C7b do teorema). Resumo:
- **Ponto:** (2, π/6, π/3) ↦ z = √3, s = 1, x = 1/2, y = √3/2; 1/4 + 3/4 + 3 = 4 = 2².
- **Células** (Δr = 1/2, Δφ = Δθ = π/6, r̄ = 3/4): polo ≈ 0,020, equador ≈ 0,075, razão 2 + √3 ≈ 3,7.
- **Jacobiano:** r² sen φ, por arestas, por duas polares (r · s) e pelo determinante (Laplace na linha de baixo).
- **Bola:** R³/3 · 2 · 2π = 4πR³/3. Erros: 4πR (sem r²); 2π²R³/3 ≈ 6,58 R³ (sem sen φ; o certo ≈ 4,19 R³).
- **Cebola:** 4πr²; ∫₀^R 4πr² dr = 4πR³/3; d/dR = 4πR².
- **Bola pesada:** M = (1/4 − 0)(1 + 1)(2π − 0) = π; média 3/4; metade da massa além de ⁴√(1/2) ≈ 0,84; cartesianas no computador = 3,14159….
- **Casquinha:** φ = π/4; r = 2 cos φ; encontro r = √2, (s, z) = (1, 1); (8/3) cos³φ sen φ; u = cos φ; (8/3)(1/4 − 1/16) = (8/3)(3/16) = 1/2; V = π; confere π/3 + 2π/3.
- **Lata:** r = 1/sen φ (parede), r = 1/cos φ (tampa), racha em φ = π/4. **Nenhum valor da integral na tela** (é do próximo vídeo).

## 5. Cena a cena

- **Gatilho** é a frase da narração (`yt_0041_narracao_v1_1.md`) em que a ação começa. Cada âncora tem a sua lista **Gatilhos**. Siga-a inteira; abaixo só vai o que ela não diz ou o que precisa de cuidado.
- **Alvo** é o quadro em `yt_0041_quadros_alvo_v1_1/`, reproduzido com tolerância de ±20 px na posição e ±5 % no tamanho. Onde o alvo e o texto (narração ou este handoff) divergirem, **vale o texto**: os itens marcados "(não está no alvo)" na narração entram mesmo assim.

### H · a bola pesada · alvos 01 e 02
- H1: a bola gira ~5 s **antes** da coluna; a câmera para, e só então a caneta começa. A integral cartesiana entra limite a limite, de fora para dentro, no gatilho "os limites já assustam". A primitiva com o colchete entra no gatilho "a integral de dentro". Selo `TRAVA` em ALERTA.
- H2: a bola do H1 perde o degradê por um `ReplacementTransform` (mesma geometria) e vira traço. As três famílias entram uma por vez e saem antes das células. As duas células ficam com `?` até o fim do H2; o título do canto troca para `QUAL É O VOLUME DE CADA PEDAÇO?` em "qual é o volume".

### A · bem-vindos
- Logo, título e a linha `NESTE VÍDEO: …`. 2D com papel de borda a borda (passo 0,5).

### B1 · o endereço · alvos 03, 04 e 05
- B1-1: a página é um triângulo chapado escuro com contorno fino (sem transparência). O arco φ sai do eixo z, nunca do chão.
- B1-2: o mesmo 3D do B1-1 (não recarregue a câmera), com os números presos aos pontos.
- B1-3: a célula lima da caixa e a da bola são **o mesmo objeto** (deforma em ~2 s, sem cópia). As três bordas ruins acendem na caixa e na bola ao mesmo tempo.

### B2 · o fator por três caminhos · alvos 06, 07, 08 e 09
- B2-1: o painel numérico abre só no gatilho "Com delta erre igual a um meio" e as linhas POLO, EQUADOR e RAZÃO entram cada uma no seu gatilho.
- B2-2: 2D. Os dois painéis entram em sequência (página primeiro). O determinante 2×2 é escrito degrau a degrau (glyph map 3).
- B2-3: 2D. A matriz é escrita **coluna por coluna** (o que a fala lê). Cada menor é sublinhado na matriz no instante em que o seu termo é escrito. A moldura menta só entra na última linha.
- B2-4: o 3D `bolagrade` fica parado ao lado da coluna. As linhas 2–4 nascem só no gatilho de cada uma (nada de esqueleto).

### B3 · o teorema e a receita · alvo 10
- B3-1: as peças 3D (lisas) em cima; o painel do enunciado embaixo é opaco, sobre o papel de borda a borda. Depois do enunciado geral, o glyph map 9 leva ao caso esférico (a linha nova fica embaixo da geral, dentro do painel; o painel cresce se precisar, sem sair da tela).
- B3-2 (sem alvo): a bola em traço (`bolagrade` sem a célula) com uma região genérica (casca entre dois cones, só contorno); os selos ①②③ na coluna em x = 1080; a sonda cresce da origem, entra em azul-claro e sai em coral; o cartão `θ E φ FORA: NÚMEROS · r DENTRO: DA SONDA`.

### B4 · a cebola · alvo 11
- As 5 cascas acendem do centro para fora e voltam para a casca do alvo (um movimento só, ~2 s). A última linha (`ρ SÓ DE r`) entra no gatilho "Para uma densidade".

### B5 · a bola pesada · alvo 12
- A bola do H1 volta parada (mesmo PNG, sem girar). Chaves `DENSIDADE` e `JACOBIANO` por 2 s e saem. Etapa 2 em "Mais duas leituras".

### B6 · a casquinha · alvo 13
- B6-1: o 3D gira ~30° e para antes da coluna. A sonda cresce no gatilho "Rô: a sonda sai da origem". O ponto de encontro e o `1` entram em "o encontro".
- B6-2: a coluna renova (§3.4). O ✓ só depois de `V = π`. A troca de cor das peças em "Confere pela geometria".

### B7 · quando usar (sem alvo)
- Três miniaturas com ✓ (bola, casca, casquinha, recortes dos PNGs 3D em cartões opacos) e a lata em silhueta com ✗, sobre o papel de borda a borda. Legendas da Tela.

### S · síntese e próximo · alvo 14
- S1 (sem alvo): três colunas com ✓, sobre o papel; os resultados voam das suas fontes.
- S2: a lata, as duas sondas (uma por vez), a diagonal da quina e `RACHA EM φ = π/4`; o cartão `NO PRÓXIMO VÍDEO · COORDENADAS CILÍNDRICAS · POLARES NO CHÃO + A ALTURA z` por ≥ 8 s; depois o CTA liso.

## 6. Narração (para o tempo do preview)

O preview é silencioso, mas cada âncora dura o tempo da tabela da narração (3 palavras/s + 0,15 s antes + 0,35 s depois). Grave em `duracoes_estimadas.json` o início e o fim de cada âncora e o instante de cada gatilho (posição da frase de disparo no texto, na mesma taxa).

| Bloco | Âncoras | Tempo |
|---|---|---:|
| H | H1, H2 | 1:32 |
| A | A1 | 0:16 |
| B1 | B1-1, B1-2, B1-3 | 3:14 |
| B2 | B2-1 a B2-4 | 5:32 |
| B3 | B3-1, B3-2 | 2:00 |
| B4 | B4 | 1:02 |
| B5 | B5 | 1:35 |
| B6 | B6-1, B6-2 | 2:52 |
| B7 | B7 | 0:27 |
| S | S1, S2 | 1:20 |
| **Total** | | **≈ 19:49** |

No texto da voz, toda variável latina é a letra maiúscula (R, S, X, Y, Z, D V…), sem fonética forçada; gregas pelo nome (téta, fi, rô). Regra do Kaio depois do teste de pronúncia. Não gere áudio.

## 7. O que NÃO fazer

- Nada de partícula, brilho, sombra, transparência, pulso ou laço contínuo; nada de palco "vivo" automático.
- Nenhuma grade em caixa recortada; nenhum quadro 2D liso (exceto o CTA).
- Nenhum `FadeIn` de linha pronta; nenhum `Write`/`TransformFromCopy` dentro de `Succession(Wait…)` ou `AnimationGroup` que ponha o destino na cena antes da vez.
- Nenhum número de episódio, livro ou Atlas na tela; nenhum "vídeo passado".
- Notação fixa (decisão do Kaio, igual aos vídeos da lei de Gauss): ρ é densidade, r é a distância ao centro, R é o raio fixo, s é a sombra. Nunca `a` para o raio nem δ para a densidade.
- Não mexer em `template/`, `assets/` (inclusive `assets/calculo/papel.py`), `docs/`, `AGENTS.md`, `pyproject.toml`, `uv.lock` nem em outras unidades.
- Sem voz, SRT, master, 1080p, entrega, commit ou push.

## 8. QA do preview (obrigatório antes de entregar)

1. **Render × alvo:** um still em cada um dos 14 gatilhos dos alvos, comparado a 960×540 (tolerância de 10 px). Prancha `comparacao_v1.jpg` + `.txt` com toda diferença que sobrar e o motivo. Diferenças vindas de itens "(não está no alvo)" não contam.
2. **Alinhamento 3D × Manim** (`alinhamento3d_v1.txt`): os rótulos contra os pontos do `pontos.json` do mesmo quadro (≤ 2 px), em todas as cenas da §2.2.
3. **R5 · sobreposição** (`sobreposicoes_v1.txt`), a cada 0,2 s, **durante** as animações e os voos, mais: rótulo × tick e rótulo × rótulo de eixo; placa × silhueta 3D (pelo `pontos.json`); eixo 3D × canto (o eixo z não pode cruzar o título). Esperado: zero, sem "achados aceitos".
4. **R6:** nada sai do painel ou do cartão; o 3D não invade a coluna; margem de 48 px.
5. **Flash por quadro = 0** (`flash_por_quadro_v1.txt`).
6. **Grade** (`grade_v1.txt`): uma amostra por segundo, classificada como 2D com grade de borda a borda, 2D sem grade (esperado: zero, exceto o CTA) ou 3D liso; um still de cada lote.
7. **Colunas** (`colunas_v1.txt`): o máximo de linhas por etapa (≤ 6; ≤ 8 com chips) e a folga do rodapé (≥ 40 px a 1080p).
8. **Glyph maps** (`glyph_maps_v1.txt`): os 17 do §3.4, com o mapa, o bloco e o tempo; nenhuma linha órfã com "="; `grep -n "from MF_Tools"` ≥ 1.
9. **Conta inteira** (`conta_inteira_v1.txt`): para cada conta (C1 a C10 e C7b da proposta), a lista de degraus com o tempo em que cada um é escrito. Nenhum degrau pode faltar em relação à narração. Em especial: os três colchetes com os valores no B2-4 e no B5; o `−cos π − (−cos 0)`; a linha dos limites novos e a inversão do B6-2; o `(√2/2)⁴ = 1/4` e o `÷ 4 = 1/16`.
10. **Texto em MathTex** (`texto_em_mathtex_v1.txt`): zero `\text{…}` com mais de uma palavra; `grep -n tfrac` = 0.
11. **Palco parado** (`palco_parado_v1.txt`): palco vazio > 0,5 s: zero; canto sem a linha 2: zero; voz falando de algo ainda fora da tela: zero. Trechos parados > 5 s só listados, com o que a voz lê (não é reprovação). Nenhum efeito para "animar" a espera.
12. **Sem pulso:** `grep -c "_pulso\|vivo-palco\|_wait_vivo" log_*.txt` = 0 (ou a prova de que `_sem_vivo` está ligado).
13. **Cores e origens** (`origens_v1.txt`): o fator r² sen φ é lima em toda linha em que aparece; o r da densidade no B5 é ciano; a entrada da sonda é azul-claro e a saída coral; para cada número e limite do §4, de onde ele voa ou qual mapa o produz.
14. **Cartão do próximo vídeo:** ≥ 8 s na tela, sem o CTA por cima.
15. **Números:** a saída do `verifica_calc3_35t2_sympy.py` (63/63) no relatório.
16. **Tempo de render por bloco** (`tempos_render_v1.txt`), com o custo por quadro de cada cena 3D.

## 9. Parada

Entregue o preview, a prancha, os relatórios e o relatório de entrega, incluindo:
- as cenas Three.js e o que foi portado de `c3d41.html`;
- a resolução e o custo por quadro;
- o alinhamento medido.

Pare. Não inicie voz nem 1080p.
