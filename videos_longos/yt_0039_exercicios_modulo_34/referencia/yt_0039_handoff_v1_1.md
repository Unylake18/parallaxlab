# yt_0039 · CÁLCULO III · EP. 14 · Exercícios do módulo: jacobiano, polares e centro de massa
## HANDOFF v1.1 (para o Claude Code): preview visual do vídeo inteiro, com 3D em Three.js

Data: 2026-11-15 (v1.1: refino do GPT filtrado, ver §10). Formato: `longo_horizontal`. Unidade nova: `videos_longos/yt_0039_exercicios_modulo_34/`.

**Antes de criar a pasta, confira o número.** Se `yt_0039` já existir em `videos_longos/`, pare e reporte. O 3.4-T1 (jacobiano), o 3.4-T2 (polares) e o 3.4-T3 (massa e centro de massa) ficam com `yt_0036`, `yt_0037` e `yt_0038`; o 3.5-T1 e o 3.5-T2 ficam com `yt_0040` e `yt_0041`. Se as pastas de 0036 a 0038 ainda não existirem, siga com `yt_0039` mesmo assim e diga no relatório.

**Fase:** só o **preview visual silencioso** do vídeo inteiro, em 960×540 a 15 fps (padrão do AGENTS.md para iterar).
- O render não tem limite de tempo: o Kaio liberou render sem economia e 3D onde a câmera ajuda.
- Não gerar voz, SRT, master, 1080p nem entrega.
- Não fazer commit nem push.

Este handoff é autocontido. Tudo o que você precisa está nele e no zip `yt0039_handoff_v1_1_completo.zip`:

- `yt_0039_quadros_alvo_v1/` traz os **15 quadros-alvo** (1920×1080), os **5 quadros 3D** de referência, a `00_folha_contato_v1.jpg` e os geradores:
  - `c3d39.html` (Three.js r128, `?k=<chave>`) gera os quadros 3D `oct`, `pap_md`, `pap_arr`, `pap_toro` e `pap_anel`. Ele tem a geometria, as câmeras, as cores e a função `proj()`, que dá os pontos de tela em px. Ao lado estão as imagens `r3d_<chave>.png` (fundo transparente) e os pontos em `r3d_pts.json`. **Porte essas cenas para a unidade** (§2.2): elas são o modelo exato, não uma inspiração.
  - `sb39.html` (Canvas + KaTeX, `?k=<chave>`) gera os quadros 2D. Chaves: `h1 e12 e13 e22 e23 e31 e32 e41 e43 e52 e53 e54 e61 e63 s2`. Abra-o com as fontes, `logo_crop.png`, `katex/`, `three.min.js` e `r3d_pts.js` do lado.
  - `r3d.js` e `shot39.js` são os scripts Playwright que geraram os PNGs. Servem só de referência.
- `yt_0039_narracao_v1.md` é a **narração** (4.357 palavras ≈ 24:12 de voz). Ela vem por âncora, com a **Tela** e os **Gatilhos** de cada uma, mais a tabela de leitura dos símbolos (Anexo B). É ela que dá os tempos, as frases de disparo e o storyboard completo. A mesma narração está no Anexo A deste handoff.
- `calculo3_34e1_exercicios_integradores_proposta_v1.md` é a proposta. O §3.1 dela (**CONTA INTEIRA**) traz o texto exato de cada etapa da coluna, linha a linha (C1a a C6e). **A coluna do vídeo é aquele texto.**
- `verificacao/verifica_calc3_34e1_sympy.py` e a saída dele somam **67 checagens, todas `True`**. Todos os números da tela saem dali. Reexecute o script no checkout (§2.1): a saída do pacote não substitui a execução.

**Hierarquia quando duas fontes divergirem:** (1) matemática e cada degrau: §3.1 da proposta; (2) fala, ordem e gatilhos: narração (Anexo A); (3) regras e correções deste handoff; (4) quadros-alvo, para composição, posição, escala e aparência; (5) kits dos vídeos anteriores, só como referência de implementação. Se um erro objetivo impedir conciliar as fontes, pare naquele ponto e reporte, sem trocar o roteiro nem a matemática por conta própria.

**Antes do render inteiro**, faça só verificações pequenas: compilar e importar as seções; um still de cada estado Three.js de referência; um teste localizado de alinhamento de um pouso; um `TransformByGlyphMap` representativo. Depois, um único render completo.

A matemática, o roteiro, a narração e os textos são a especificação. Não rediscuta. Se encontrar uma inconsistência objetiva, reporte antes de mudar.

**Regras da série (Kaio):**
- **Figura:** todo enunciado e todo passo aparece com a sua figura.
- **Origem:** todo símbolo nasce do desenho, por `TransformFromCopy` do objeto para a fórmula ou pela caneta. Nada aparece pronto.
- **Conta inteira:** a fórmula-mãe vem antes do número, e cada valor voa da fonte.
  - A primitiva aparece com colchete `[G]ₐᵇ`, depois `G(b) − G(a)` com os valores substituídos, depois o número.
  - A substituição tem a linha `w = …, dw = …` e a linha dos limites novos, com o sinal quando o limite inverte (E3).
  - Cada passo é um `TransformByGlyphMap` com mapa explícito.
  - Nenhuma linha órfã começa por "=", e nenhuma seta pula degrau.
- **Grade na tela inteira:** toda cena 2D tem os quadradinhos de borda a borda, nascendo dos eixos do palco. Com dois planos, cada um tem a grade na sua metade. Só o 3D e o CTA ficam lisos.
- **"Sensacional" quer dizer clareza.** Nada de partícula, brilho, sombra, névoa, contorno em seta, pulso, luz que lava a cor ou câmera girando sem motivo.

**Lições dos EP. 06 a 13, já incorporadas aqui** (não as repita):
- MF-Tools de verdade, sem `mapa_glifos` próprio com `FadeIn`;
- nenhum bloco abrindo vazio e nenhuma moldura vazia;
- **nenhum pulso automático**: se o kit copiado tiver `_pulso_v2` ou "palco vivo", desligue (`_sem_vivo = True`);
- voo sem fantasma: a cópia sai da fonte sem duplicar o glifo e sem contorno no pouso;
- R5 testado também durante as animações;
- frase portuguesa sempre em Space Grotesk, nunca dentro de `MathTex`;
- `\dfrac` sempre;
- cartão do próximo vídeo por ≥ 8 s.

**A imagem-mãe deste vídeo:** **a chapa e o seu ⊕**. A meia arruela abre o vídeo com o ⊕ indeciso perto do buraco (H1), volta com a conta no E5 (o ⊕ cai no buraco por 0,01, visto na lupa), é pendurada por um alfinete no E5-3 (o fio de prumo cruza no ar) e gira no E6 até virar uma bola oca, que confere o mesmo 28/(9π) **sem integral nenhuma**. Os outros problemas seguem a mesma **receita de cinco passos** (H2), sempre numerados na coluna (`PASSO 1` … `PASSO 5`), e todo resultado tem conferência por outro caminho, com o ✓ menta.

---

## 0. O que entregar

1. A unidade nova, com:
   - `ficha.md` (§1);
   - `cena.py` e uma seção `sec_*.py` por bloco (H, A, E1 … E6, S);
   - `threejs/`, com as cenas 3D, o renderizador por quadro e os pedidos (§2.2).
2. O preview do vídeo inteiro, `renders/v1/yt_0039_preview_v1_540p15.mp4`, com a duração da narração (§6). Junto, `duracoes_estimadas.json`.
3. A prancha **render × alvo** `renders/v1/qa/comparacao_v1.jpg`, com uma linha por quadro-alvo (os 15 alvos e os quadros 3D `pap_md` e `pap_toro`), cada um com o still do render no gatilho ao lado do alvo.
4. Os relatórios de QA em `renders/v1/qa/` (§8):
   - `sobreposicoes_v1.txt`
   - `alinhamento3d_v1.txt`
   - `flash_por_quadro_v1.txt`
   - `palco_parado_v1.txt`
   - `texto_em_mathtex_v1.txt`
   - `glyph_maps_v1.txt`
   - `origens_v1.txt`
   - `conta_inteira_v1.txt`
   - `grade_tela_v1.txt`
   - `tempos_render_v1.txt`
5. O relatório de entrega do AGENTS.md: arquivos, renders, QA e pendências.

## 1. Ficha

```
formato: longo_horizontal
tipo: exercicios
serie_publica: CÁLCULO III · EP. 14
titulo: Exercícios do módulo: jacobiano, polares e centro de massa
disciplina: Cálculo III
modulo: 3.4 Mudança de variáveis na integral dupla (o docs/mapa_curricular.md do repositório ainda usa a numeração antiga)
bloco: 3.4-E1
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, Exercícios 4.2 (1h, 2e, 4, 5, 6) e 4.3 (1b, 1f, 3); Stewart, Cálculo, vol. 2, §15.9 (u = xy, v = y/x). Só na descrição do YouTube: nada de livro na tela nem na fala
unidades: E1 é exercício de coordenadas adimensionais (o expoente y − x² precisa ser adimensional); E2 em coordenadas normalizadas (L = 1 m, densidade de referência 1 kg/m²), por isso a massa sai em kg; E3 a E6 com comprimentos na unidade de referência; k carrega a unidade e cancela em ȳ. Não inserir unidades novas nas fórmulas
solido_3d: nenhum do arsenal Blender (o oitavo de esfera e os sólidos de revolução são superfícies simples feitas direto em Three.js, como nos EP. 05 a 13)
3d_threejs: cena1 = octante (E3: quarto de disco no chão + casca da esfera no 1º octante, com pouso de cima para o 2D); cena2 = pappus (E6: chapa em pé sobre o eixo x varrendo o sólido por um ângulo φ; formas meio disco, meia arruela e disco deslocado; quadradinho com o anel 2πy; círculo do centroide)
duracao_alvo: ≈ 25–26 min (narração v1.1: 4.357 palavras ≈ 24:12 de voz)
```

## 2. Base de código

### 2.1 Manim

- **Antes de começar:**
  - leia `docs/estado_atual.md`;
  - rode `verificacao/verifica_calc3_34e1_sympy.py` com o Python da `.venv`. As 67 linhas devem dar `True`. Se faltar sympy ou mpmath, não instale nada: diga no relatório e siga.
- **Copie, não importe.** Copie o kit da unidade mais recente da série de Cálculo III que estiver no seu checkout, nesta ordem de preferência: `yt_0038_*`, `yt_0037_*`, `yt_0036_*`, `yt_0035_*`, `yt_0034_*`. Do kit vêm:
  - `kit.py` e `render.sh`;
  - o canto de duas linhas e `placa_min`;
  - a caneta (`TC`/`TX`), `painel`, `mixl`, `chip` e o sublinhado de leitura;
  - do EP. 12 (yt_0037), se existir: o cartão polar com r, θ e o fator r, e o triângulo polar;
  - do EP. 13 (yt_0038), se existir: o ⊕ `cm()` (cheio e vazado), o mapa radial ciano `ρ = k r` do meio disco, a lupa e a régua ampliada.

  Se essas unidades não estiverem no seu checkout, use a mais recente que houver. Este handoff não depende delas: os alvos têm tudo desenhado. Não altere as outras unidades.
- **Fundo:**
  - Cenas 2D: violeta liso `#18143A → #0F0C26` na câmera, mais a grade `papel(ax)` de `assets/calculo/papel.py` **sem `area`**, ou seja, na tela inteira, nascendo dos eixos do palco, com quadradinho de 0,25 da unidade do gráfico, cor `#2B2558` e sem linhas grossas.
  - Dois planos (E1-2, E1-4, E2-1 quando houver uv): cada plano tem a grade dele na sua metade, com uma emenda vertical fina GEO a 35 % (alvo 02: emenda em x = 540 px).
  - Cartões sem gráfico (H2, A1, E5-3, S1, S2): a mesma grade com passo 0,5, nascendo do centro do cartão.
  - Cenas 3D (Three.js) e CTA: só o violeta liso. A grade entra no pouso, junto com o 2D.
- Render por bloco (`render.sh <Classe>`), depois concatene.
- **Sem economia artificial**, mas sem updater à toa:
  - o ⊕ que sobe no eixo no H1 e no E5-4 é um `ValueTracker` só;
  - a família do E6-4 (a chapa de a = 0 até a = b) é um `ValueTracker` em a, com o ⊕ preso à fórmula;
  - os mapas ciano (meia elipse ρ = k y, meia arruela ρ = k r, quadrado do uv no E2-4, faces do cubo no S2) são imagens estáticas ou grades de quadradinhos sem contorno, com a cor calculada uma vez.
- Limpe da cena o que saiu da tela. Não deixe nada invisível acumulando.

### 2.2 Three.js (o pipeline da série)

- **Copie o pipeline** da unidade de Cálculo mais recente que tiver `threejs/` (yt_0038, yt_0037, yt_0035 ou yt_0034, se estiverem no checkout; senão `videos_longos/yt_0026_funcoes_vetoriais_campos/threejs/`). Vêm de lá:
  - `r3d.js`, `package.json` (playwright-core) e `cena3d/three.min.js` (r128);
  - o esquema de pedidos:
    1. A passagem seca do Manim grava `pedidos3d/<LOTE>.json` com `{cena: [[quadro, estado], …]}`.
    2. `r3d.js` abre `cena3d/<cena>.html`, chama `window.setEstado(estado)` quadro a quadro e grava os PNGs com alfa e o `pontos.json`.
    3. O Manim cola os PNGs como `ImageMobject` em tela cheia e prende os rótulos nos pontos.
- **Porte as cenas de `c3d39.html`** para `threejs/cena3d/`. Vêm de lá:
  - `octante`: a casca `Sp(φ, θ)` da esfera de raio a no 1º octante (tom pela altura, `#123A5A → #2FA9D6`), o quarto de disco no chão (GEO a 30 % sobre o fundo), os três arcos de borda (tubo GEO fino) e as setas dos eixos x (âmbar), y (magenta) e z (branco);
  - `pappus`: o perfil da chapa no plano (x, s), s = distância ao eixo x, e o giro `G(x, s, φ) = [x, s·sen φ, s·cos φ]` (o sinal faz a varredura vir para a câmera); a superfície varrida pelas bordas de 0 a φ (tom pela normal), as duas faces de corte (a chapa em φ = 0 escurecida e a chapa em φ, GEO claro `#9AA6C4`), os tubos de borda, o quadradinho lima, o anel lima e o círculo tracejado magenta do centroide;
  - a câmera `ver(pos, alvo, cx, cy)` com `setViewOffset` e `proj()`.

  Câmera perspectiva com fov 22° e up = +z. Os pontos de `pontos.json` são da escala em que o PNG foi gerado: se o PNG sai em 1920×1080 e o preview é 960×540, divida os pontos por 2 antes de comparar. **Atenção:** `c3d39.html` desenha só o estado final de cada chave, o do quadro-alvo. Os estados abaixo são nomes sugeridos, e a animação entre eles é sua.
- **Estados por cena:**

  | cena | estados | o que anima |
  |---|---|---|
  | cena1 (octante) | `casca` 0→1 (a casca sobe do quarto de disco) · `pouso` 0→1 | **E3-1:** depois da leitura dos limites em 2D, o 3D entra **por cima do palco 2D, no mesmo quadro** (o quarto de disco 3D, visto de cima, coincide com o 2D; alinhamento ≤ 2 px); a câmera sobe para a vista de cima e de lado do alvo 06 (≈ 2,5 s, começo e fim suaves) e a casca cresce do chão (`casca` 0→1, ≈ 2 s) com `UM OITAVO DE BOLA`. **E3-2:** pouso de cima ao contrário: a casca baixa, a câmera volta à vista de cima ortográfica e o palco 2D do alvo 07 herda o quarto de disco |
  | cena2 (pappus) | `forma` (`meio_disco` SC = 2,2 · `meia_arruela` SC = 1,15, raios 1 e 2 · `toro` SC = 1,0, disco de raio 1 com centro a 2 do eixo) · `phi` 0→2π · `solido` (liga/desliga a varredura) · `anel` 0→1 · `circ_cm` 0→1 | **E6-1:** a chapa meio disco em pé (`phi` = 0) com o quadradinho lima em y₀ = 0,6a; o anel lima nasce do quadradinho e dá a volta inteira (alvo 13 = `pap_anel`, sem sólido); depois a chapa gira de 0 a 2π em **6 s** com começo e fim suaves e o sólido nasce atrás dela (`pap_md` mostra φ = 270°); ao fim, a bola inteira. **E6-2:** a bola (estado final do E6-1) com o círculo do centroide `circ_cm`, raio 4a/(3π). **E6-3:** a meia arruela gira de 0 a 2π (alvo 14 = `pap_arr`, φ = 250°, a bola oca aparece pelo corte) e o círculo tracejado magenta de raio 28/(9π) é desenhado pelo ⊕. **E6-5:** o disco deslocado gira (`pap_toro`, φ = 270°) com o círculo tracejado de raio 2 |

- **A câmera nunca se mexe durante o giro**, e o giro nunca acontece durante a escrita de uma fórmula. Um giro por forma, uma vez.
- **Pouso para o 2D no E6-1** (o "Somando" da fala): a câmera vai para a vista de frente (olhando de −y para +y, x para a direita, z para cima), ortográfica no último quadro, e a chapa em φ = 0 vira o meio disco 2D do palco (grade entra junto). Mesmo cuidado do EP. 13: dolly-zoom até a perspectiva ficar desprezível e troca para `OrthographicCamera`; diferença ≤ 2 px.
- **Estilo 3D da série:**
  - opaco e sem luz (`MeshBasicMaterial`), tom por face calculado uma vez;
  - sem sombra, névoa, brilho ou transparência;
  - `outputEncoding` linear e antialias ligado.
- **Câmeras dos alvos:**
  - `oct` (notação JS, decimal com ponto): `ver([11.5, 5.2, 7.6], [0.42*SC, 0.42*SC, 0.28*SC], 600, 580)`, com SC = 2.2. No alvo 06 o PNG foi composto reduzido a 90 % e deslocado (+40, +95) px: **enquadre direto na unidade** para o resultado do alvo (o eixo z não pode encostar no canto);
  - `pap_*` (exceto toro): `ver([8.8, -15.5, 7.2], [0, 0, 0.25], 640, 560)`;
  - `pap_toro`: `ver([11.5, -20, 9.5], [0, 0, 0.2], 700, 560)`.
- **Onde há coluna de fórmulas.** No E3-1, no E6-1 (depois do giro) e no E6-3, a cena 3D fica à esquerda e nada passa de **x = 1090 px**; a coluna começa em 1060–1120. O giro do E6-1 e o E6-5 são **3D em tela cheia**, sem coluna; as legendas ficam em placas.
- **Rótulos são do Manim**, presos aos pontos do `pontos.json` do mesmo quadro. Alinhamento ≤ 2 px. Pontos já exportados:
  - `oct`: `ex`, `ey`, `ez` (pontas das setas), `a_x`, `a_y`, `a_z`, `origem`, `casca`;
  - `pap_md` e `pap_anel`: `quad` (quadradinho), `anel_topo`, `anel_frente`, `eixo_fim`, `centro`, `chapa_topo`, `borda_dir`;
  - `pap_arr`: `cm_ini`, `cm_fim` (o ⊕ no início e no fim do giro), `oco`, `eixo_fim`, `r1`, `r2`, `topo`;
  - `pap_toro`: `centro_disco`, `eixo_fim`.

## 3. Sistema visual

### 3.1 Layouts e escala

| layout | geometria a 1080p | blocos |
|---|---|---|
| **A · palco + coluna** | Palco à esquerda; coluna de fórmulas alinhada à esquerda em **x = 1040–1180** (a dos alvos). A coluna tem **no máximo 7 linhas por etapa** (a etapa = um bloco `Cn` do §3.1 da proposta); o resultado que a próxima etapa usa sobe como **chip** (moldura GEO a 70 %, raio 10) para o topo, em y ≈ 175. | E1-1, E1-3, E2-1 a E2-4, E3-2, E4, E5-1, E5-2, E5-4 |
| **B · dois planos + coluna** | xy à esquerda, uv no meio, coluna em x = 1210 (alvo 02). Seta GEO `φ` entre os planos. | E1-2, E1-4 |
| **3D + coluna** | cena 3D à esquerda (≤ 1090 px), coluna em x = 1060–1120. | E3-1 (fim), E6-1 (fim), E6-3 |
| **3D · tela cheia** | cena 3D com legendas em placas, sem coluna. | giro do E6-1, E6-2, E6-5 |
| **C · cartão** | grade passo 0,5; desenhos em traço GEO. | H2, A1, E5-3, S1, S2 |

**Palcos dos alvos** (origem dos eixos em px, e px por unidade a 1080p):

| alvo | âncora | palco |
|---|---|---|
| 01 | H1 | meia arruela: origem (960, 820), 1 = 220 px |
| 02 | E1-2 | xy: origem (215, 985), 1 = 118 px (y até 6,35); uv: origem (720, 770), 1 = 170 px; emenda em x = 540 |
| 03 | E1-3 | uv: origem (260, 820), 1 = 250 px |
| 04 | E2-2 | xy: origem (150, 960), 1 = 300 px (vale também para o E2-1) |
| 05 | E2-3 | xy: origem (440, 990), 1 = 360 px (um movimento de câmera do palco do E2-2 para este, no gatilho da pipa) |
| 06 | E3-1 | 3D `oct` + coluna em 1060 |
| 07 | E3-2 | quarto de disco: origem (220, 900), a = 560 px |
| 08 | E4-1 | elipse a = 1,6 e b = 1 (de desenho): origem (470, 560), 1 = 240 px |
| 09 | E4-3 | meia elipse x² + 4y² ≤ 1: origem (545, 900), 1 = 470 px |
| 10 | E5-2 | meia arruela: origem (560, 860), 1 = 230 px; lupa ×10 com centro (230, 300), raio 120 px |
| 11 | E5-3 | cartão: duas chapas penduradas (alfinetes em (380, 260) e (1000, 260), 1 = 130 px) e a chapa de volta (origem (1560, 780), 1 = 105 px) |
| 12 | E5-4 | meia arruela com o mapa: origem (520, 860), 1 = 210 px; régua em pé em x = 1240, de 0,98 (y = 860) a 1,03 (y = 260), 12 px por milésimo |
| 13 | E6-1 | 3D `pap_anel` + coluna em 1120 |
| 14 | E6-3 | 3D `pap_arr` + coluna em 1120 |
| 15 | S2 | cubo de lado 2: canto (0, 0, 0) em (330, 820), 1 = 230 px, profundidade oblíqua (0,55; −0,42) por unidade |

Conversão para o Manim: x_m = (x_px − 960)/135; y_m = (540 − y_px)/135.

### 3.2 Regras (as da série)

- **R1 · Clareira:** nenhum rótulo sobre ponto, aresta, linha da grade ou número; o rótulo sai para o lado.
- **R2 · Placa:** todo rótulo solto sobre o desenho ou sobre o 3D usa `placa_min`.
- **R3:** fórmula nova nunca nasce sobre fórmula velha; a coluna limpa antes (entre etapas `Cn`), e o chip fica.
- **R4:** rótulo junto do objeto que ele nomeia, e **o rótulo sai junto com o seu objeto**.
- **R5:** QA automático de sobreposição, amostrado a cada 0,5 s **inclusive durante as animações** (§8).
- **R6:** nada sai da moldura do seu painel ou cartão. Quando há coluna, nada do 3D passa de x = 1090.
- **R-texto:**
  - **Palavra é Space Grotesk** (`Text`, maiúsculas); matemática é `MathTex`.
  - Uma linha mista é `Text` + `MathTex` lado a lado, com respiro ≥ 0,15 (`mixl()` no `sb39.html`; alvos 04, 05, 13).
  - Nenhuma frase portuguesa dentro de `MathTex`: `PASSO 1`, `DE DENTRO`, `DE FORA`, `ÁREA`, `PIPA`, `SEPARA`, `HOMOGÊNEA`, `NO BURACO`, `VOLTA PARA A CHAPA`, `CHAPA HOMOGÊNEA`, `ANEL DE COMPRIMENTO`, `MEIO DISCO`, `ARAME` são `Text`, com o símbolo em `MathTex` ao lado.
  - Cada legenda tem no máximo 6 palavras e pelo menos **26 px** a 1080p; **algarismo ≥ 30 px**. As legendas `DE DENTRO`/`DE FORA` dos alvos 03 e 10 (≈ 21 px) sobem para 26 px.
- **Fração:** sempre `\dfrac`, com o glifo da fração ≥ 26 px a 1080p. Nenhum rótulo girado. `grep -n tfrac` = 0. O alvo 05 usa `\tfrac` na coordenada do canto esquerdo da pipa: no vídeo é `\dfrac`.
- **Glifos:**
  - Zero em legenda vai por extenso (`ZERO`), porque o 0 do Space Grotesk parece O (o `CANTO (0, 0, 0)` do alvo 15 vira `MathTex`). Zero como valor é `MathTex`.
  - Nos números com vírgula decimal, use `{,}` no LaTeX.
  - `a` e `b` (raio e semieixos) são `MathTex` itálico, nunca Space Grotesk.
- **Sublinhado de leitura:** quando a voz lê um símbolo (Anexo B: "jacobiano", "módulo", "bê u vê", "dáblio", "rô", "xis barra", "ípsilon barra", "eme xis", "éle de ípsilon"), um sublinhado fino aparece sob ele no gatilho falado e sai. Não é pulso nem brilho.
- **Os cinco passos:** em E1, E2, E3 e E4, cada linha que cumpre um passo leva à esquerda o selo `PASSO n` (Text GEO, 26 px). O passo 5 é sempre "calcular e conferir": a conferência ganha o ✓ menta.
- **Um movimento por ideia, uma vez.** Uma figura nova nasce da velha (`ReplacementTransform`) e nunca pisca.
- **Nenhum bloco abre vazio:**
  - a linha 2 do canto está na tela desde o primeiro quadro de cada bloco;
  - a figura do bloco anterior fica até a nova nascer dela, ou a nova começa a entrar em ≤ 0,5 s;
  - palco vazio por mais de 0,5 s: zero ocorrências. Moldura vazia por mais de 0,1 s: zero.
- **Palco parado:**
  - Medida: trecho em que menos de 40 px do **palco** (máscara sem a coluna e sem o canto, a 960×540) mudam mais de 8 níveis ao longo de 3 s.
  - Limite de 3 s. De 3 a 5 s só é aceito se a voz estiver lendo o que está no palco, com o motivo no relatório. Acima de 5 s: zero.
  - As contas longas deixam o palco parado por natureza. Cada degrau acende no desenho a peça de onde veio (a tira, a chave, a borda, a célula, o cateto, o anel). É isso que mantém o palco vivo. Não invente movimento.
- **Pontos e marcas só os do alvo.** Nenhum ponto de debug.
- **O ⊕ do centro de massa** é o símbolo da Física: disco com degradê ciano → magenta e cruz fina (`cm()` no `sb39.html`). **O centroide** é o ⊕ vazado branco (`cm(…, vaz=true)`). No E5-4 e no E4-4 os dois ficam juntos.

### 3.3 Cores

| Papel | Cor |
|---|---|
| x, x̄, tira em pé, o `a` do semieixo em x | âmbar `#FFC24D` |
| y, ȳ, M_x, tira deitada, o `b`, o cateto `y = r sen θ` | magenta `#EA63FF` |
| u e r, `du`, `dr` / v e θ, `dv`, `dθ` | laranja `#FF9440` / verde-água `#2EE6A6` |
| J, \|J\|, o r do jacobiano, a célula, o quadradinho e o anel do Pappus | lima `#C6F26B` |
| ρ, k, m, os mapas de densidade | ciano `#35D9FF` |
| w (a substituição do Cálculo I) | lilás `#C9A7FF` |
| entrada / saída da fatia | azul-claro `#7FB2FF` / coral `#FF7A8A` |
| regiões, alfinete, fio, ícones, cartões, chapa sem densidade | GEO `#B8C4DA` |
| `TRAVA`, `NO BURACO`, a borda r = 1 do buraco no E5, o `2 INTEGRAIS`, o ✗ do S1 | ALERTA `#FF5D5D` |
| ✓, `VOLTA PARA A CHAPA`, `O MESMO NÚMERO`, `IR E VOLTAR = NÃO FAZER NADA`, `UM OITAVO DE BOLA` | menta `#8CFFD2` |
| ⊕ centro de massa / ⊕ vazado centroide | degradê ciano → magenta / branco `#F5F7FF` |

- Operadores (∫, ∬, Σ, d, =, ⇒, ≈, colchetes, barras do determinante) ficam em branco, e a cor vai na grandeza.
- A massa é **ciano** (na série de Cálculo o âmbar é o x).
- O `w` é lilás para não confundir com o u laranja.

### 3.4 Álgebra

- **Caneta** em toda fórmula nova: traço finíssimo (~0,7), glifo a glifo, da esquerda para a direita, preenchendo na cor da grandeza, sem flash e sem preview do destino.
- Um termo que nasce no desenho **voa** para a fórmula (`TransformFromCopy`, em arco, sem fantasma). No 3D, ele voa a partir do ponto projetado. **Voos obrigatórios:**
  - **E1-2:** cada borda do xy voa para a coluna (a equação `y = 1 + x²` sai da curva), e a equação nova (`v = 1`) voa da coluna para a borda do uv; os quatro cantos voam do xy para o uv (alvo 02).
  - **E1-3:** a chave `COMPRIMENTO = v` da tira deitada voa para o `(v − 0)` (alvo 03).
  - **E1-4:** `BASES 1 E 2` e `ALTURA 1` voam das chaves do trapézio para `\dfrac{1+2}{2}\cdot 1`.
  - **E2-2:** a célula lima voa para o `|J|` final (alvo 04).
  - **E2-3:** as diagonais `1` e `\dfrac{1}{\sqrt2}` voam da pipa para a linha `PIPA` (alvo 05). A pipa é estimativa geométrica (≈ 2 % de diferença), não igualdade.
  - **E2-4:** o rótulo `u = xy` da hipérbole voa para trocar o `xy` do integrando por `u`.
  - **E3-1:** `0` e `a` voam das marcas do eixo x; `0` e `\sqrt{a^2-x^2}` voam da entrada e da saída da tira.
  - **E3-2:** `r` e `θ` voam do triângulo polar; o `\dfrac{4\pi a^3}{3}` voa do ícone da bola.
  - **E4-1:** `a` e `b` voam das marcas dos eixos; `abr` voa da célula esticada.
  - **E4-3:** o chip `m = \dfrac{k}{6}` desce para o denominador de ȳ (alvo 09).
  - **E5-2:** `y = r sen θ` voa do cateto; o chip `A = \dfrac{3\pi}{2}` desce para o denominador; o `0{,}990` voa da coluna para a lupa (alvo 10).
  - **E5-4:** `0{,}990` e `1{,}023` voam dos chips para a régua em pé (alvo 12).
  - **E6-1:** o `2\pi y` voa do anel e o `\Delta A` do quadradinho (alvo 13).
  - **E6-3:** os chips `A = \dfrac{3\pi}{2}` e `\dfrac{28}{9\pi}` descem para a conta (alvo 14).
- **MF-Tools de verdade:**
  - `from MF_Tools import TransformByGlyphMap` (1.4.9), com `MathTex` de string única nos dois lados e mapa explícito.
  - O glifo que sai usa `auto_fade` (ou entra no mapa com destino vazio).
  - O glifo que **entra** nunca usa `FadeIn`: fica fora do mapa e é escrito com a caneta logo depois, ou voa da fonte.
  - Cancelamento em dois tempos: o par acende em GEO junto, depois some. A linha antiga nunca é remapeada depois de sair.
  - Não use função própria de mapa de glifos. `show_indices` só no desenvolvimento.
- **Glyph maps obrigatórios** (24 grupos; vários grupos têm mais de uma passagem, e o relatório lista todas as passagens implementadas, não só 24 chamadas; o texto de cada degrau é o do §3.1 da proposta):
  1. C1a: `J = |1 0; 2u 1|` → `= 1 · 1 − 0 · 2u` → `= 1` (o determinante abre por mapa).
  2. C1b: cada borda, `y = 1 + x²` → `v = 1` (o `x²` atravessa a igualdade e vira `v = y − x²`); quatro aplicações.
  3. C1c: `(e^v/v)[u]₀^v` → `(e^v/v)(v − 0)` → `e^v` (o par v/v acende e some).
  4. C1c: `[e^v]₁²` → `e² − e¹` → `e² − e`, e só então `≈ 4,67`.
  5. C1d: `[(2 + x²) − (1 + x²)]` → `1` e `[(2 + x²) − (x + x²)]` → `2 − x` (os x² acendem e somem); `[2x − x²/2]₁²` → `(4 − 2) − (2 − 1/2)` → `1/2`; `1 + 1/2 = 3/2`.
  6. C2a: `uv = y²`, `u/v = x²` → `x = √(u/v)`, `y = √(uv)`.
  7. C2a: `|y x; −y/x² 1/x|` → `y · (1/x) − x · (−y/x²)` → `y/x + y/x` → `2y/x` → `2v` (o `y/x` vira `v`).
  8. C2a: `∂(x,y)/∂(u,v) · 2v = 1` → `J = 1/(2v)` (o `2v` atravessa e vira denominador).
  9. C2b: `(1/(2v))[u]₁²` → `(1/(2v))(2 − 1)` → `1/(2v)`; `(1/2)[ln v]₁²` → `(1/2)(ln 2 − ln 1)` → `(ln 2)/2` (o `ln 1` vira `0` pelo chip).
  10. C2c: `∬ xy dA` → `∫₁² ∫₁² u · 1/(2v) du dv`; `(1/(2v))[u²/2]₁²` → `(1/(2v))(4/2 − 1/2)` → `(1/(2v)) · 3/2` → `3/(4v)`; `(3/4)[ln v]₁²` → `(3/4)(ln 2 − 0)`.
  11. C2c: `((3/4) ln 2)/((1/2) ln 2)` → os `ln 2` acendem e somem → `(3/4)/(1/2)` → `3/2`.
  12. C3: `y² = a² − x²` → `x² + y² = a²` (o `x²` atravessa); `z = √(a² − x² − y²)` → `x² + y² + z² = a²`.
  13. C3: `w = a² − r²`, `dw = −2r dr` → `r dr = −dw/2`; linha `r = 0 → w = a²`, `r = a → w = 0`; `∫_{a²}^0 √w (−dw/2)` → `(1/2) ∫₀^{a²} w^{1/2} dw` (**o menos inverte os limites**; selo `O MENOS INVERTE OS LIMITES`).
  14. C3: `(1/2)[(2/3) w^{3/2}]₀^{a²}` → `(1/2)(2/3)((a²)^{3/2} − 0)` → `a³/3`; `(a³/3)[θ]₀^{π/2}` → `(a³/3)(π/2 − 0)` → `πa³/6`; `(4πa³/3) ÷ 8` → `4πa³/24` → `πa³/6`.
  15. C4a: `a²r²cos²θ/a² + b²r²sen²θ/b²` → os `a²` e os `b²` cancelam → `r²(cos²θ + sen²θ)` → `r²`.
  16. C4a: `|a cos θ  −a r sen θ; b sen θ  b r cos θ|` → `abr cos²θ + abr sen²θ` → `abr`; `2ab[r²/2]₀¹[θ]₀^π` → `2ab · 1/2 · π` → `πab`.
  17. C4b: `k · (r sen θ)/2 · r/2` → `(k/4) sen θ · r²` → separa (`SEPARA: SÓ θ · SÓ r`) → `[−cos θ]₀^π = −cos π + cos 0 = 1 + 1 = 2` e `[r³/3]₀¹ = 1/3` → `(k/4) · 2 · (1/3)` → `k/6`.
  18. C4c: `((r sen θ)/2)² · k · r/2` → `(k/8) sen²θ · r³`; `sen²θ = (1 − cos 2θ)/2` → `[θ/2 − sen 2θ/4]₀^π` → `π/2 − (sen 2π)/4 − 0` → `π/2`; `[r⁴/4]₀¹ = 1/4`; `(k/8)(π/2)(1/4)` → `kπ/64`.
  19. C4c: `(kπ/64)/(k/6)` → `(kπ/64) · (6/k)` (o k cancela) → `6π/64` → `3π/32`.
  20. C4d: `k[y²/2]₀^{√(1−x²)/2}` → `k · (1/2) · (1 − x²)/4` → `k(1 − x²)/8`; `(k/8)[x − x³/3]₋₁¹` → `(k/8)(2/3 + 2/3)` → `(k/8)(4/3)` → `k/6`.
  21. C5a e C5b: `[r²/2]₁²` → `4/2 − 1/2` → `3/2` → `(3/2)π`; `π · 2²/2 − π · 1²/2` → `2π − π/2` → `3π/2`; `sen θ [r³/3]₁²` → `sen θ (8/3 − 1/3)` → `(7/3) sen θ`; `(7/3)[−cos θ]₀^π` → `(7/3)(1 + 1)` → `14/3`; `(14/3)/(3π/2)` → `(14/3) · (2/(3π))` → `28/(9π)`.
  22. C5c: `k[r³/3]₁²` → `k(8/3 − 1/3)` → `7k/3` → `7kπ/3`; `k sen θ [r⁴/4]₁²` → `k sen θ (16/4 − 1/4)` → `(15k/4) sen θ` → `15k/2`; `(15k/2)/(7kπ/3)` → `(15k/2) · (3/(7kπ))` (o k cancela) → `45/(14π)`.
  23. C6a: `ΔV ≈ 2πy ΔA` → `V = ∬_B 2πy dA` (Δ vira d, a soma vira ∬) → `= 2π ∬_B y dA` (o 2π sai) → `= 2π M_x` → `= 2π ȳ A`.
  24. C6b, C6c e C6d: `2π · 4a/(3π) · πa²/2` → `8a/3 · πa²/2` → `8πa³/6` → `4πa³/3`; `(4/3)π(8 − 1)` → `28π/3`; `V = 2πȳA` → `ȳ = V/(2πA)`; `(28π/3)/(3π²)` → `(28π/3) · 1/(3π²)` → `28/(9π)`; `4(b³ − a³)/(3π(b² − a²))` → fatora → o `(b − a)` acende e some → `4(a² + ab + b²)/(3π(a + b))` → a = 0: `4b/(3π)`; a = b: `2b/π ≈ 0,64 b`.
- **Leitura das potências:** `(a²)^{3/2}` com o parêntese visível; `sen²θ` sempre com o expoente no `sen`; `((r sen θ)/2)²` com o parêntese grande.
- **Tamanhos:** fórmula principal de 36–44 px no alvo; secundária de 30–36 px; índice ≥ 22 px; nada menor que 26 px fora dos índices.
- **Arredondamento na tela:** o exato vem antes do decimal, e o decimal sempre com `≈`: `e² − e ≈ 4,67`, `(ln 2)/2 ≈ 0,347`, `√2/4 ≈ 0,354`, `(3/4) ln 2 ≈ 0,520`, `3π/32 ≈ 0,295`, `2/(3π) ≈ 0,212`, `28/(9π) ≈ 0,990`, `45/(14π) ≈ 1,023`, `2b/π ≈ 0,64 b`, `4π² ≈ 39,5`.

## 4. Números (todos conferidos no script)

- **E1 · faixa entre parábolas** (A: 0 ≤ x ≤ 2 entre y = 1 + x² ou y = x + x² e y = 2 + x²): u = x, v = y − x², J = 1; B_uv: 1 ≤ v ≤ 2, 0 ≤ u ≤ v (trapézio); cantos (0, 1) → (0, 1), (0, 2) → (0, 2), (1, 2) → (1, 1), (2, 6) → (2, 2); **∬ e^{y−x²}/(y−x²) dA = e² − e ≈ 4,67**; área 3/2 nas duas figuras.
- **E2 · hipérboles** (R: 1 ≤ xy ≤ 2, x ≤ y ≤ 2x): u = xy, v = y/x; ∂(u,v)/∂(x,y) = 2v ⇒ **J = 1/(2v)**; área **(ln 2)/2 ≈ 0,347**; pipa com diagonais 1 e 1/√2: **√2/4 ≈ 0,354**; massa com ρ = xy: **(3/4) ln 2 ≈ 0,520 kg**; densidade média **3/2**. Fatiando em pé seriam **duas** integrais (as bordas trocam em x = 1).
- **E3 · oitavo de bola:** ∫₀^a ∫₀^{√(a²−x²)} √(a² − x² − y²) dy dx = **πa³/6** = (4πa³/3)/8.
- **E4 · elipse:** J = abr; área **πab** (metade de cima × 2); a = b ⇒ πa². **Meia elipse** x² + 4y² ≤ 1, y ≥ 0, ρ = k y: |J| = r/2; **m = k/6**; **M_x = kπ/64**; **ȳ = 3π/32 ≈ 0,295**; x̄ = 0; conferência em xy: m = k/6; homogênea: 2/(3π) ≈ 0,212.
- **E5 · meia arruela** 1 ≤ r ≤ 2, 0 ≤ θ ≤ π: **A = 3π/2**; **M_x = 14/3**; **ȳ = 28/(9π) ≈ 0,990 < 1 (no buraco)**; ρ = k r: **m = 7kπ/3**, **M_x = 15k/2**, **ȳ = 45/(14π) ≈ 1,023 > 1 (na chapa)**.
- **E6 · Pappus:** V = 2π ȳ A. Bola: 2π · 4a/(3π) · πa²/2 = **4πa³/3**. Bola oca: (4/3)π(8 − 1) = **28π/3** ⇒ ȳ = **28/(9π)** (confere o E5). Família: ȳ(a, b) = 4(a² + ab + b²)/(3π(a + b)); a = 0 → **4b/(3π)**; a = b → **2b/π ≈ 0,64 b**. Rosquinha (disco de raio 1, centro a 2 do eixo): **4π² ≈ 39,5**.
- **Desafio do CTA** (não vai para a tela nem para a fala): o buraco engole o centro quando a/b passa de ≈ 0,494.

## 5. Cena a cena

- **Gatilho** é a frase da narração (Anexo A) em que a ação começa. Cada âncora do Anexo A tem a sua **Tela** e a sua lista **Gatilhos: "frase" → ação**. Siga as duas inteiras. Abaixo só vai o que o Anexo não diz ou o que precisa de cuidado.
- **Alvo** é o quadro em `yt_0039_quadros_alvo_v1/`, reproduzido com tolerância de ±20 px na posição e ±5 % no tamanho. Para posição e escala vale o alvo; para conteúdo e ordem valem a Tela e os Gatilhos. Onde este texto corrigir o alvo, vale este texto.
- **Canto:** a linha 1 é `CÁLCULO III · INTEGRAL DUPLA`, e a linha 2 é o título da cena (o do alvo, quando há alvo).

### H · a chapa e o buraco · alvo 01
- **H1 (alvo 01).** 2D, sem coluna. O meio disco de raio 2 nasce, o de raio 1 sai dele (contorno tracejado), fica a meia arruela com `MEIA ARRUELA` e `HOMOGÊNEA` em placas. O ⊕ com `?` sobe pelo eixo (`ValueTracker`) e para **perto da borda do buraco**, sem número; a borda r = 1 acende ALERTA com `BURACO` no gatilho "abaixo de um". Depois o mapa ρ = k r pinta por cima (a pergunta da borda pesada) e sai. No fim, os ícones de traço da bola e da bola oca com `SEM INTEGRAL` (promessa do E6). **Nenhum valor numérico do ȳ no H1.**
- **H2.** Cartão: os cinco passos numerados a caneta (círculos GEO), um por gatilho, e o painel da divisão `\bar y = \dfrac{M_x}{m}` (momento sobre massa).

### A · bem-vindos
Padrão do canal: logo; o título; `NESTE VÍDEO`. Os seis chips (`1 · PARÁBOLAS`, `2 · HIPÉRBOLES`, `3 · OITAVO DE BOLA`, `4 · ELIPSE`, `5 · MEIA ARRUELA`, `6 · PAPPUS`) entram um por palavra falada, em 26 px.

### E1 · a faixa entre parábolas · alvos 02 e 03
- **E1-1.** Layout A. A tira em pé e a tira deitada com `TRAVA` (ALERTA); `y − x²` acende no integrando e nas bordas ao mesmo tempo.
- **E1-2 (alvo 02).** Layout B. A assinatura é **a tira em pé que escorrega para baixo sem esticar** (`SÓ ESCORREGA`), no gatilho do jacobiano 1. Depois as bordas voam (§3.4). Coluna C1a, depois C1b com o chip `|J| = 1`.
- **E1-3 (alvo 03).** Layout A com o uv. A tira deitada em v = 1,75 com a chave `COMPRIMENTO = v` (verde-água). Coluna C1c. **Sem moldura em volta do resultado**: o ✓ e a cor bastam.
- **E1-4.** Layout B: o trapézio com as chaves de base e altura; a área do xy por duas tiras em pé (comprimento 1 e 2 − x). Coluna C1d com ✓.

### E2 · as hipérboles · alvos 04 e 05
- **E2-1.** Layout A (palco do alvo 04). As duas tiras em pé, a troca de bordas em x = 1 e a placa `2 INTEGRAIS` (ALERTA).
- **E2-2 (alvo 04).** A grade de hipérboles (laranja) e de raios (verde-água) cobre a região; a célula lima mostra o fator (menor em cima, onde v é maior). A coluna é a C2a. `IR E VOLTAR = NÃO FAZER NADA` (menta) entra no gatilho da regra da cadeia.
- **E2-3 (alvo 05).** Um movimento de câmera para o palco do alvo 05. A pipa tracejada com as duas diagonais; os quatro cantos com as coordenadas em placas. Linha `PIPA` mista; `0{,}347 ≈ 0{,}354` com `ESTIMATIVA DA PIPA` (GEO) e **sem ✓**: é conferência de ordem de grandeza, não de igualdade. O alvo 05 já está assim.
- **E2-4.** O quadrado do uv pintado em faixas ciano (u cresce para a direita) e a reta u = 3/2 no meio; coluna C2c; `MEIO DE 1 E 2` com ✓.

### E3 · o oitavo de bola · alvos 06 e 07
- **E3-1 (alvo 06).** Primeiro o palco 2D (Tela do Anexo A: a tira varre e a saída desenha o quarto de círculo); depois a cena 3D `octante` entra (§2.2). No alvo, a legenda da esfera `x^2+y^2+z^2=a^2` é `MathTex` em placa; os limites da linha 2 da coluna estão em azul-claro e coral (entrada e saída).
- **E3-2 (alvo 07).** Pouso de volta ao 2D; a etapa A da coluna (C3: polares e a linha do w, glyph maps 13) e depois a etapa B (alvo 07) com o chip da integral em polares no topo. `UM OITAVO DA BOLA` com ✓.

### E4 · a elipse e a meia elipse pesada · alvos 08 e 09
- **E4-1 (alvo 08).** Um movimento: o círculo tracejado estica até a elipse, e **uma** célula polar estica junto (a célula lima escura do círculo vira a célula lima clara da elipse; o alvo mostra as duas para leitura). O selo `× ab` acompanha. Coluna C4a, com `METADE DE CIMA × 2` e o ✓ do caso a = b.
- **E4-2.** A meia elipse x² + 4y² ≤ 1 com o mapa ciano em faixas horizontais (`MAIS PESADA EM CIMA`); `x̄ = 0` pela simetria; coluna C4b com o selo `SEPARA`.
- **E4-3 (alvo 09).** O ⊕ pousa em ȳ com a reta tracejada magenta. **Corrija no alvo:** a marca `0,5` do eixo y encosta no arco; afaste-a (R1).
- **E4-4.** A conferência fatiando em pé (C4d) e a comparação: o meio disco homogêneo achata até a meia elipse e o ⊕ vazado desce junto (de 4/(3π) para 2/(3π)); o ⊕ cheio em 3π/32 fica acima.

### E5 · a meia arruela · alvos 10, 11 e 12
- **E5-1.** A meia arruela com a conta da área (C5a) e a conferência `2π − π/2` com ✓.
- **E5-2 (alvo 10).** O triângulo polar (raio laranja, cateto magenta `y = r sen θ`); coluna C5b; o ⊕ pousa em 0,990, encostado na borda do buraco. A **lupa ×10** é um círculo de moldura GEO com a região ampliada (chapa em cima, `BURACO` embaixo, a borda r = 1 em ALERTA e o ⊕ abaixo dela); nada de vidro nem reflexo. `NO BURACO` (ALERTA) no gatilho.
- **E5-3 (alvo 11).** Cartão. A chapa gira em torno do alfinete (rotação simples, **sem balanço**) até o ⊕ ficar embaixo do alfinete; o fio de prumo desce do alfinete pelo ⊕. Pendurada pela direita, depois pela esquerda; à direita do cartão, a chapa de volta com as duas retas cruzando no ⊕, no ar. `O EQUILÍBRIO FICA NO AR` (menta).
- **E5-4 (alvo 12).** O mapa ρ = k r pinta a chapa; coluna C5c em duas etapas (chips `m = 7kπ/3` e `\int_0^\pi \operatorname{sen}\theta\,d\theta = 2`); no fim, a régua em pé com as três marcas (0,990 HOMOGÊNEA, 1,000 BORDA DO BURACO, 1,023 ρ = k r) e o ⊕ sobe do buraco para a chapa. `VOLTA PARA A CHAPA` (menta). Os títulos dos dois chips de cima do alvo são `Text` (`HOMOGÊNEA`, `BORDA MAIS PESADA`).

### E6 · Pappus · alvos 13 e 14
- **E6-1 (alvo 13).** §2.2. O alvo mostra o estado do anel (chapa em pé, anel inteiro, sem sólido); o giro com o sólido é o `pap_md`. Depois do pouso, a coluna C6a (glyph map 23) e o selo `VOLUME = ÁREA × CAMINHO DO CENTROIDE` com `2\pi\bar y` sob `CAMINHO`. A linha das cascas entra com a fatia deitada (magenta) desenhada no meio disco 2D.
- **E6-2.** A bola (`pap_md` no fim do giro) com o círculo do centroide; coluna C6b com ✓.
- **E6-3 (alvo 14).** `pap_arr` + coluna C6c. `O MESMO NÚMERO` (menta) com ✓. A placa `CAMINHO DO CENTROIDE` fica junto do círculo tracejado (R4), não solta no canto como no alvo.
- **E6-4.** 2D: a meia arruela com `ValueTracker` em a; o buraco some (a = 0, `MEIO DISCO`) e a chapa vira arame (a = b, `ARAME`); o ⊕ acompanha; coluna C6d.
- **E6-5.** `pap_toro` em tela cheia; a linha C6e numa placa.

### S · síntese e próximo · alvo 15
- **S1.** Cartão com os cinco erros (✗ ALERTA → ✓ menta), um por gatilho, em linhas de ≤ 6 palavras.
- **S2 (alvo 15).** A chapa [0, 2]² com o mapa ciano **ganha altura** e vira o cubo de lado 2 (extrusão desenhada no Manim, três faces em perspectiva fixa, sem cena 3D nova); arestas escondidas **não** aparecem. `\rho = x^2+y^2+z^2` e `MAIS PESADO LONGE DO CANTO`; `QUANTO PESA ESTE CUBO?`; a caixinha lima com `\Delta x\,\Delta y\,\Delta z` (MathTex) ao lado (o alvo não tem o rótulo: ponha). O canto `(0, 0, 0)` é `MathTex`. Cartão `NO PRÓXIMO VÍDEO` / `INTEGRAL TRIPLA` **≥ 8 s**, sem o CTA por cima. O CTA padrão entra só em "deixa o like", com o desafio `A PARTIR DE QUE BURACO O CENTRO CAI NELE?`.

## 6. Narração (para o tempo do preview)

O preview é silencioso, mas cada âncora dura o tempo estimado da fala do Anexo A: 3 palavras/s, mais 0,15 s antes e 0,35 s depois de cada âncora. O total da voz é ≈ **24:12**; com as esperas das contas, o vídeo fica em ≈ 25–26 min. A coluna **Início** é a soma da voz, não um timecode fixo do MP4 depois das esperas. A duração não é teto: clareza e gatilhos mandam.

| Âncora | Palavras | Voz (s) | Início |
|---|---:|---:|---:|
| H1 | 146 | 48,7 | 0:00 |
| H2 | 95 | 31,7 | 0:48 |
| A1 | 57 | 19,0 | 1:20 |
| E1-1 | 141 | 47,0 | 1:39 |
| E1-2 | 242 | 80,7 | 2:26 |
| E1-3 | 131 | 43,7 | 3:47 |
| E1-4 | 164 | 54,7 | 4:30 |
| E2-1 | 136 | 45,3 | 5:25 |
| E2-2 | 212 | 70,7 | 6:10 |
| E2-3 | 196 | 65,3 | 7:21 |
| E2-4 | 158 | 52,7 | 8:26 |
| E3-1 | 148 | 49,3 | 9:19 |
| E3-2 | 223 | 74,3 | 10:08 |
| E4-1 | 229 | 76,3 | 11:23 |
| E4-2 | 214 | 71,3 | 12:39 |
| E4-3 | 205 | 68,3 | 13:50 |
| E4-4 | 165 | 55,0 | 14:59 |
| E5-1 | 141 | 47,0 | 15:54 |
| E5-2 | 155 | 51,7 | 16:41 |
| E5-3 | 98 | 32,7 | 17:32 |
| E5-4 | 198 | 66,0 | 18:05 |
| E6-1 | 165 | 55,0 | 19:11 |
| E6-2 | 98 | 32,7 | 20:06 |
| E6-3 | 137 | 45,7 | 20:39 |
| E6-4 | 184 | 61,3 | 21:24 |
| E6-5 | 64 | 21,3 | 22:26 |
| S1 | 128 | 42,7 | 22:47 |
| S2 | 127 | 42,3 | 23:30 |
| **Total** | **4.357** | | **24:12** |

- Gere o `duracoes_estimadas.json` por âncora, como nas unidades anteriores, para a voz encaixar depois (WAV contínuo, cena segue a voz).
- Os gatilhos do §5 e do Anexo A são frases dessa narração. Marque o instante estimado de cada um pela contagem de palavras.
- As tags `[curious]`, `[serious]` etc. não contam palavras.
- **Não gerar voz.**

## 7. O que NÃO fazer

- Nada de `ThreeDScene`, `Surface` ou `Prism` do Manim: todo 3D é Three.js. O cubo do S2 é desenho 2D em perspectiva fixa.
- Nenhuma partícula, brilho, sombra, névoa, contorno em seta, pulso automático ou transparência no 3D.
- A chapa do fio de prumo não balança: gira e para.
- A câmera nunca se mexe durante a escrita de uma fórmula nem durante o giro do Pappus.
- Não usar `u` na substituição do Cálculo I: é `w` (u e v são coordenadas neste vídeo).
- Não usar R maiúsculo para raio: é `a` (e `b`).
- Não pôr o valor do ȳ da meia arruela no H1; ele só aparece no E5.
- Não pôr a resposta do desafio do CTA (≈ 0,494) na tela nem na fala.
- Não escrever decimal sem `≈`, nem o decimal antes do exato.
- Não dizer "vídeo passado" nem "aula passada", e não citar número de episódio, livro nem o Atlas na tela.
- Não pôr frase portuguesa dentro de `MathTex`, nem `\tfrac`, nem `FadeIn` de linha pronta. Nenhum rótulo girado. Nenhuma moldura em volta de resultado.
- Não mexer em `template/`, `assets/`, `docs/`, `AGENTS.md` nem nas outras unidades.
- Não gerar voz, SRT, master, 1080p nem entrega. Não fazer commit nem push.

## 8. QA do preview (obrigatório antes de entregar)

1. **Render × alvo:** um still em cada gatilho de alvo (15 alvos + `pap_md` e `pap_toro`), tirado quando o estado do alvo está completo e comparado na mesma resolução (alvo reduzido a 960×540, tolerância de 10 px nessa escala). Prancha `comparacao_v1.jpg`. Toda diferença que sobrar vai listada com o motivo (as correções do §5 contam como motivo).
2. **Alinhamento 3D × Manim** (`alinhamento3d_v1.txt`):
   - para cada quadro 3D, os rótulos contra os pontos do `pontos.json` do mesmo quadro (≤ 2 px);
   - para a entrada e o pouso do `octante` (E3-1 e E3-2) e para o pouso do `pappus` no E6-1, o contorno 2D contra o contorno no PNG (≤ 2 px).
3. **R5 · sobreposição** (`sobreposicoes_v1.txt`): caixas de `Text` e `MathTex` contra outros textos, linhas, arestas, setas, bordas de painel e chapa, rótulos dos eixos e arestas do 3D. A amostragem é **a cada 0,5 s, inclusive durante as animações**, em especial a tira que escorrega e as bordas que voam no E1-2, a câmera do E2-3, a casca que cresce no E3-1, o círculo que estica no E4-1, a lupa do E5-2, a chapa que gira no E5-3, a régua do E5-4, o giro do E6 e a família do E6-4. Esperado: zero.
4. **R6:** nada sai do painel ou do cartão; com coluna, o 3D não passa de x = 1090.
5. **Flash por quadro = 0** (`flash_por_quadro_v1.txt`): nenhuma fórmula aparece inteira antes da caneta. Nada de `FadeIn`, `TransformFromCopy` ou `Write` dentro de `Succession(Wait…)`/`AnimationGroup` que ponha o destino na cena no instante 0.
6. **Glyph maps** (`glyph_maps_v1.txt`): os 24 do §3.4, com mapa → bloco → tempo, e nenhuma linha órfã com "=". `grep -n "from MF_Tools"` ≥ 1 e nenhuma função própria de mapa de glifos.
7. **Conta inteira** (`conta_inteira_v1.txt`): para cada etapa C1a … C6e da proposta, a lista de degraus com o tempo de cada um, comparada linha a linha com o texto da proposta. Cada colchete `[G]ₐᵇ` precisa ter o seu `G(b) − G(a)` escrito, e o `w` do E3 as suas duas linhas e o selo do sinal.
8. **Texto em MathTex** (`texto_em_mathtex_v1.txt`): liste todo `\text{…}`. Esperado: zero. Inclua também `grep -n tfrac` = 0.
9. **Grade na tela** (`grade_tela_v1.txt`): em cada cena 2D, um still por bloco mostrando a grade de borda a borda (com dois planos, cada um na sua metade). Liso só no 3D e no CTA.
10. **Palco parado** (`palco_parado_v1.txt`): medido só no palco (§3.2). Nenhum trecho acima de 5 s; de 3 a 5 s, só com o motivo. Inclua o palco vazio (> 0,5 s: zero), a moldura vazia (> 0,1 s: zero) e o canto sem a linha 2 (zero).
11. **Origens** (`origens_v1.txt`): para cada número e símbolo do §4 que aparece na tela, de onde ele voa (objeto-fonte) ou qual mapa o produz. Os voos do §3.4 são obrigatórios.
12. **Cores:** massa e ρ em ciano; u/r laranja, v/θ verde-água, J lima, w lilás; ⊕ cheio só no centro de massa e vazado só no centroide.
13. **Cartão do próximo vídeo:** ≥ 8 s na tela, sem o CTA por cima.
14. **Tempo de render por bloco** em `tempos_render_v1.txt`, só para registro, com o custo por quadro do 3D. Se um pouso 3D ficar tecnicamente inviável depois de um diagnóstico concreto, use a vista 2D equivalente e registre o que falhou e quais alvos não foram cumpridos. **Nunca troque 3D por 2D só para poupar render.**
15. **Aceite:** as 28 âncoras na ordem; os 15 alvos e os estados 3D conferidos; todos os degraus C1a–C6e na tela; zero flash; o relatório dos 24 grupos de glyph maps; alinhamento e sobreposição medidos na escala certa; cartão ≥ 8 s; MP4 960×540, 15 fps, silencioso. O R5 automático é triagem: confira nos stills os trechos sinalizados e **nunca escreva "zero colisões" sem evidência**. Item que falhar vai para o relatório com causa e bloco, sem declarar aprovação plena.

## 9. Parada

Entregue o preview, a prancha, os relatórios e o relatório de entrega. O relatório inclui as cenas Three.js, o que foi portado de `c3d39.html`, a resolução, o custo por quadro e o alinhamento medido. Pare. Não inicie voz nem 1080p.

---

## 10. O que mudou na v1.1 (refino do GPT, filtrado)

Entrou: a hierarquia das fontes; as verificações pequenas antes do render inteiro; reexecutar o sympy; as unidades (E1 adimensional, E2 normalizado); a escala dos pontos 3D no preview; a notação JS das câmeras; os glyph maps como grupos; o critério de aceite e "nunca zero colisões sem evidência"; nunca trocar 3D por 2D para poupar render; a tabela de tempos não é timecode; e a **pipa como estimativa** (sem ✓, com a frase da fala ajustada). Na narração saíram as molduras de resultado (E1-3, E2-3, E4-2) e os dois `\text{…}` (E2-4 e S1). Ficou de fora o que repetia o AGENTS.md (git status, não sobrescrever ao descompactar, trabalhar na main).

## Anexo A · narração v1.1 por âncora (cópia de `yt_0039_narracao_v1.md`, com a Tela e os Gatilhos)

### Tempo por âncora

| Âncora | Trecho | Palavras | Voz (s) | Início estimado |
|---|---|---:|---:|---:|
| H1 | a chapa que equilibra no buraco? | 146 | 48.7 | 0:00 |
| H2 | cinco passos e uma divisão | 95 | 31.7 | 0:48 |
| A1 | bem-vindos | 57 | 19.0 | 1:20 |
| E1-1 | a faixa entre parábolas: trava | 141 | 47.0 | 1:39 |
| E1-2 | os passos um a quatro | 242 | 80.7 | 2:26 |
| E1-3 | a conta: o comprimento cancela | 131 | 43.7 | 3:47 |
| E1-4 | conferindo pela área | 164 | 54.7 | 4:30 |
| E2-1 | as hipérboles: dois pedaços | 136 | 45.3 | 5:25 |
| E2-2 | o jacobiano da volta | 212 | 70.7 | 6:10 |
| E2-3 | a área e a pipa | 196 | 65.3 | 7:21 |
| E2-4 | a massa e a densidade média | 158 | 52.7 | 8:26 |
| E3-1 | ler a região nos limites | 148 | 49.3 | 9:19 |
| E3-2 | polares e o oitavo de bola | 223 | 74.3 | 10:08 |
| E4-1 | a elipse: polares esticadas | 229 | 76.3 | 11:23 |
| E4-2 | a meia elipse pesada: a massa | 214 | 71.3 | 12:39 |
| E4-3 | o momento e o centro de massa | 205 | 68.3 | 13:50 |
| E4-4 | conferindo a massa e comparando | 165 | 55.0 | 14:59 |
| E5-1 | a meia arruela: a área | 141 | 47.0 | 15:54 |
| E5-2 | o momento e o buraco | 155 | 51.7 | 16:41 |
| E5-3 | o fio de prumo | 98 | 32.7 | 17:32 |
| E5-4 | a borda mais pesada | 198 | 66.0 | 18:05 |
| E6-1 | Pappus: o volume pelo centroide | 165 | 55.0 | 19:11 |
| E6-2 | a bola confere o meio disco | 98 | 32.7 | 20:06 |
| E6-3 | a casca confere a meia arruela | 137 | 45.7 | 20:39 |
| E6-4 | a família: do meio disco ao arame | 184 | 61.3 | 21:24 |
| E6-5 | a rosquinha | 64 | 21.3 | 22:26 |
| S1 | síntese: os cinco erros | 128 | 42.7 | 22:47 |
| S2 | o próximo vídeo e CTA | 127 | 42.3 | 23:30 |
| **Total** | | **4.357** | **24:12** | |

Com as respirações entre âncoras e as esperas de leitura das contas (o padrão da série é ≈ +6 %), o vídeo fica em **≈ 25–26 min**; a conta inteira na tela costuma esticar mais 1 a 2 min no render.

---

### H1 · a chapa que equilibra no buraco?
**Tela:** layout A sem coluna, grade da tela inteira nascendo dos eixos (origem em (960, 820), 1 = 220 px). (1) O meio disco de raio 2 nasce em GEO translúcido; o meio disco de raio 1 **sai** dele (recorte com contorno tracejado), e fica a meia arruela. (2) `HOMOGÊNEA` (placa). (3) O eixo y acende branco tracejado (`SIMETRIA`). (4) Um ⊕ com `?` sobe e desce no eixo, entre y = 0,6 e y = 1,4, e para perto da borda do buraco (y ≈ 1), sem número. A borda r = 1 acende em ALERTA no gatilho "abaixo de um": a faixa 0 ≤ y < 1 do eixo vira `BURACO` (ALERTA). (5) O mapa radial ρ = k r (ciano, cresce para fora) pinta a chapa; `MAIS PESADA NA BORDA` em ciano; o ⊕ dá um pulinho para cima com `?`. (6) No fim, no canto inferior direito, entram dois ícones em traço GEO: uma bola e uma bola cortada ao meio (oca), com `SEM INTEGRAL` embaixo.
Canto: `A CHAPA E O BURACO`.
**Gatilhos:** "Olha esta chapa"→meio disco grande · "tira, do meio dele"→recorte · "meia arruela"→rótulo · "homogênea"→placa · "Pela simetria"→eixo acende · "Mas em que altura"→⊕ com ? anda · "abaixo de um"→borda r = 1 em ALERTA e `BURACO` · "a borda de fora pesar mais"→mapa ρ = k r e legenda · "sobe de volta"→⊕ pula · "uma bola e uma bola oca"→dois ícones e `SEM INTEGRAL`
> [curious] Olha esta chapa. É o que sobra de um meio disco de raio dois quando a gente tira, do meio dele, um meio disco de raio um. Ficou uma meia arruela. E ela é homogênea: a mesma densidade em todo ponto. A pergunta é: onde fica o centro de massa dela, o ponto em que ela equilibra? Pela simetria, ele está em cima do eixo ípsilon. Mas em que altura? Se a altura der abaixo de um, o centro de massa cai no buraco: num lugar onde não tem chapa nenhuma. E se a borda de fora pesar mais, com a densidade crescendo com a distância até o centro? Será que ele sobe de volta para a chapa? Hoje a gente responde as duas perguntas, com a conta inteira. E, no fim, uma bola e uma bola oca vão conferir esse número sem fazer integral nenhuma.

### H2 · cinco passos e uma divisão
**Tela:** cartão sem gráfico (grade padrão, passo 0,5). Coluna central (x = 560) a caneta, um item por gatilho, cada número num círculo GEO: `1 · ESCOLHER AS VARIÁVEIS NOVAS` · `2 · ESCREVER` `x, y` `EM FUNÇÃO DELAS` · `3 · JACOBIANO, EM MÓDULO` (com `|J|` em lima) · `4 · DESENHAR A REGIÃO NOVA` · `5 · CALCULAR E CONFERIR` (✓ menta). À direita (x = 1300), num painel: `CENTRO DE MASSA` / `\bar y = \dfrac{M_x}{m}` (M_x magenta, m ciano) / `MOMENTO ÷ MASSA`.
**Gatilhos:** "cinco passos"→painel · "escolher as variáveis"→1 · "xis e ípsilon em função delas"→2 · "o jacobiano"→3 · "a região nova"→4 · "calcular e conferir"→5 com ✓ · "uma divisão só"→painel da direita · "momento sobre massa"→fórmula
> [serious] Este vídeo junta o módulo inteiro, e tudo cabe em cinco passos e uma divisão. Toda troca de variáveis segue os mesmos cinco passos: escolher as variáveis novas; escrever xis e ípsilon em função delas; calcular o jacobiano e tomar o módulo; desenhar a região nova, borda por borda; e calcular e conferir por outro caminho. E o centro de massa é sempre uma divisão só: momento sobre massa. A ordem de hoje é a do módulo: primeiro o jacobiano, depois as polares, depois massa e centro de massa, e no fim a meia arruela.

### A1 · bem-vindos
**Tela:** logo; `EXERCÍCIOS DO MÓDULO`; embaixo, seis chips numerados que acendem um a um: `1 PARÁBOLAS` · `2 HIPÉRBOLES` · `3 OITAVO DE BOLA` · `4 ELIPSE` · `5 MEIA ARRUELA` · `6 PAPPUS`.
**Gatilhos:** "Bem-vindos"→logo · "seis problemas"→título · "duas parábolas"…"o teorema de Pappus"→os seis chips, um por item falado
> [happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Hoje é dia de exercício: seis problemas que começam parecidos e vão ficando mais espertos. Duas parábolas, duas hipérboles, um oitavo de bola, uma elipse, a meia arruela e, no fim, o teorema de Pappus. Pega papel e lápis: em cada um tem a hora de pausar o vídeo e tentar.

### E1-1 · a faixa entre parábolas: trava
**Tela:** layout A. Palco xy à esquerda (origem em (300, 960), 1 = 130 px; x de 0 a 2,4, y de 0 a 6,6), grade da tela inteira. As curvas nascem uma por gatilho: `y = 1 + x²` e `y = 2 + x²` (GEO), `y = x + x²` (GEO tracejado fino), o eixo `x = 0`; a região A acende em GEO translúcido, com os quatro cantos (0, 1), (0, 2), (1, 2), (2, 6) em pontos brancos pequenos. Coluna (x = 1080): o enunciado `\iint_A \dfrac{e^{y-x^2}}{y-x^2}\,dA` a caneta e a etiqueta `PAUSE E TENTE` ao lado. Tira em pé âmbar com a placa `TRAVA`; tira deitada magenta com `TRAVA`. Depois `y − x²` acende verde-água no expoente **e** no denominador; as bordas `y = 1 + x²` e `y = 2 + x²` acendem verde-água.
Canto: `1 · A FAIXA ENTRE PARÁBOLAS`.
**Gatilhos:** "Primeiro problema"→palco · "um mais xis ao quadrado"→curva 1 · "dois mais xis ao quadrado"→curva 2 · "xis mais xis ao quadrado"→curva 3 · "xis maior ou igual a zero"→eixo e região · "a integral dupla"→enunciado · "pausa o vídeo"→`PAUSE E TENTE` · "em pé"→tira âmbar · "Trava"→placa 1 · "deitada"→tira magenta · "trava também"→placa 2 · "ípsilon menos xis ao quadrado"→acende no integrando · "as bordas também"→bordas acendem
> [curious] Primeiro problema. A região A fica entre a parábola ípsilon igual a um mais xis ao quadrado e a parábola ípsilon igual a dois mais xis ao quadrado, acima da curva ípsilon igual a xis mais xis ao quadrado, com xis maior ou igual a zero. Calcule a integral dupla, em A, de é elevado a ípsilon menos xis ao quadrado, sobre ípsilon menos xis ao quadrado. Se quiser, pausa o vídeo e tenta. Fatia em pé: a integral de dentro, em ípsilon, pede a primitiva de é elevado a alguma coisa sobre essa mesma coisa, que não se escreve com as funções do Cálculo um. Trava. Fatia deitada: trava também. Agora repara: o integrando só enxerga ípsilon menos xis ao quadrado. E as bordas também: duas delas são ípsilon menos xis ao quadrado igual a um e igual a dois.

### E1-2 · os passos um a quatro
**Tela:** layout B: palco xy à esquerda (o mesmo), plano u, v no meio (origem em (640, 760), 1 = 170 px; u de 0 a 2,3 laranja, v de 0 a 2,3 verde-água), coluna em x = 1160. Coluna C1a (passos 1 a 3) e depois C1b (passo 4), em duas etapas (a coluna limpa entre elas, e o chip `|J| = 1` fica no topo). Passo 1: `u = x`, `v = y − x²` (o `y − x²` **voa** do expoente). Passo 2: `x = u`, `y = v + u²` (glyph map: o `x²` vira `u²` e atravessa a igualdade). Passo 3: a matriz das derivadas, o determinante, `|J| = 1` em lima. No palco xy, uma tira em pé âmbar fina (x = 0,6) **escorrega para baixo** sem esticar até o plano u, v (selo `SÓ ESCORREGA`). Passo 4: cada borda acende no xy e **voa** para o plano u, v já como a borda nova: `v = 1`, `v = 2`, `u = 0`, `v = u` (coral, saída); os quatro cantos com as coordenadas antes → depois. Fica o trapézio `B_{uv}` em GEO translúcido.
**Gatilhos:** "Passo um"→`u`, `v` · "Passo dois"→glyph map · "Passo três"→matriz · "um, zero"→1ª linha · "dois u, um"→2ª linha · "um vezes um"→det · "o jacobiano é um"→`|J| = 1` · "só escorrega"→a tira desce · "Passo quatro"→coluna limpa, chip `|J| = 1` sobe · "vê igual a um"…"vê igual a u"→as quatro bordas voam · "Os cantos conferem"→cantos · "um trapézio"→B_uv acende
> [thoughtful] Passo um: escolher. Chama xis de u, e ípsilon menos xis ao quadrado de vê. Passo dois: xis e ípsilon em função de u e vê. Xis é u. E, de vê igual a ípsilon menos xis ao quadrado, ípsilon é vê mais u ao quadrado. Passo três: o jacobiano. A derivada de xis em relação a u é um, em relação a vê, zero: a primeira linha é um, zero. A de ípsilon em relação a u é dois u, e em relação a vê, um: a segunda linha é dois u, um. O determinante: um vezes um, menos zero vezes dois u. O jacobiano é um. Faz sentido: com xis parado, ípsilon só perde xis ao quadrado. Cada fatia em pé só escorrega para baixo, sem esticar, e a área não muda. Passo quatro: a região nova, borda por borda. Ípsilon igual a um mais xis ao quadrado vira vê igual a um. Ípsilon igual a dois mais xis ao quadrado vira vê igual a dois. Xis igual a zero vira u igual a zero. E ípsilon igual a xis mais xis ao quadrado vira vê igual a u. Os cantos conferem: zero, um fica zero, um; zero, dois fica zero, dois; um, dois vai para um, um; e dois, seis vai para dois, dois. No plano u vê, a região é um trapézio: vê vai de um a dois, e, para cada vê, u vai de zero até vê.

### E1-3 · a conta: o comprimento cancela
**Tela:** layout A com o plano u, v no palco (o trapézio, uma tira deitada verde-água em v = 1,5: entrada azul-claro em u = 0, saída coral em u = v, chave `COMPRIMENTO v` embaixo dela). Coluna C1c por glyph maps: a integral montada (o `1` lima voa do chip; os limites voam do palco: `0` da entrada, `v` da saída, `1` e `2` das bordas); `DE DENTRO` (Space Grotesk) + a linha da integral de dentro; `[u]₀^v`; `(v − 0)`; o par `v`/`v` acende e some junto; `= e^v`; a de fora; `[e^v]₁²`; `e² − e¹`; `= e² − e ≈ 4,67` em menta, com ✓ e sem moldura.
**Gatilhos:** "Passo cinco"→integral montada · "vezes o módulo do jacobiano"→o `1` voa · "a de dentro"→linha de dentro · "não depende de u"→`e^v/v` acende, sai para fora · "u, de zero a vê"→`[u]₀^v` · "vê menos zero"→`(v − 0)` · "cancela"→o par some · "Sobra é elevado a vê"→`e^v` · "A de fora"→linha de fora · "é ao quadrado menos é"→resultado
> [excited] Passo cinco: calcular. A integral vira a integral de um a dois, da integral de zero a vê, de é elevado a vê sobre vê, vezes o módulo do jacobiano, que é um, dê u dê vê. A de dentro é em u, e é elevado a vê sobre vê não depende de u: sai da integral. Sobra a integral de dê u, que é u, de zero a vê: vê menos zero. E esse vê, o comprimento da fatia, cancela o vê de baixo. Sobra é elevado a vê. A de fora: a primitiva de é elevado a vê é ela mesma, de um a dois: é ao quadrado menos é elevado a um. A resposta é é ao quadrado menos é, mais ou menos quatro vírgula sessenta e sete.

### E1-4 · conferindo pela área
**Tela:** layout B (xy à esquerda, u, v no meio). Coluna C1d. Primeiro, no u, v: chaves `BASE 1` (em v = 1) e `BASE 2` (em v = 2), `ALTURA 1`; `ÁREA DE B = \dfrac{1+2}{2}\cdot 1 = \dfrac{3}{2}` (os três números voam das chaves). Depois no xy: tira em pé em x = 0,5 (entrada azul-claro em `1 + x²`, saída coral em `2 + x²`, chave `COMPRIMENTO 1`) e tira em x = 1,5 (entrada em `x + x²`, saída em `2 + x²`, chave `2 − x`); a coluna escreve as duas integrais com os colchetes e o resultado `= 3/2 ✓`. As duas áreas ficam lado a lado com `=` grande menta entre os dois palcos.
**Gatilhos:** "conferir pela área"→coluna limpa · "a área de B"→chaves no trapézio · "três meios"→conta do trapézio · "fatia em pé"→tira 1 · "o xis ao quadrado cancela"→os dois `x²` acendem e somem · "de um a dois"→tira 2 · "dois menos xis"→chave · "um meio"→colchete · "três meios de novo"→✓ e `=` menta
> [thoughtful] E como conferir? Pela área, que o jacobiano um promete conservar. A área de bê u vê é a de um trapézio: bases um e dois, altura um. Base média vezes altura: um mais dois sobre dois, vezes um, três meios. Agora a área de A direto em xis e ípsilon, fatiando em pé. De zero a um, a fatia sai em dois mais xis ao quadrado e entra em um mais xis ao quadrado: o xis ao quadrado cancela e o comprimento é um. De um a dois, ela entra em xis mais xis ao quadrado e sai em dois mais xis ao quadrado: comprimento dois menos xis. A primeira: xis de zero a um, um menos zero, um. A segunda: a primitiva é dois xis menos xis ao quadrado sobre dois; em dois, quatro menos dois; em um, dois menos um meio; a diferença é um meio. Um mais um meio: três meios de novo. A troca não ganhou nem perdeu área.

### E2-1 · as hipérboles: dois pedaços
**Tela:** layout A. Palco xy (origem em (260, 940), 1 = 330 px; x de 0 a 1,6, y de 0 a 2,3); as hipérboles `xy = 1`, `xy = 2` (GEO) e as retas `y = x`, `y = 2x` (GEO); a região R acende em GEO translúcido; os quatro cantos com pontos brancos. Enunciado na coluna: `ÁREA DE R` e `MASSA DE R COM` `\rho = xy` (ρ ciano), `PAUSE E TENTE`. Duas tiras em pé (x = 0,85 e x = 1,2) com entrada azul-claro e saída coral mostram a troca: à esquerda entra na hipérbole `xy = 1` e sai na reta `y = 2x`; à direita entra na reta `y = x` e sai na hipérbole `xy = 2`; tracejado vertical em `x = 1` e as marcas `\dfrac{1}{\sqrt2}` e `\sqrt2` no eixo; placa `2 INTEGRAIS` em ALERTA.
Canto: `2 · AS HIPÉRBOLES`.
**Gatilhos:** "Segundo problema"→palco · "xis ípsilon igual a um"→hipérbole 1 · "igual a dois"→hipérbole 2 · "ípsilon igual a xis"→reta 1 · "dois xis"→reta 2 · "a área"→enunciado 1 · "a massa"→enunciado 2 · "Pausa e tenta"→`PAUSE E TENTE` · "um sobre raiz de dois até raiz de dois"→marcas · "as bordas trocam"→tracejado em x = 1 · "entra na hipérbole de baixo"→tira 1 · "entra na reta de baixo"→tira 2 · "duas integrais"→placa
> [curious] Segundo problema. A região erre fica no primeiro quadrante, entre as hipérboles xis ípsilon igual a um e xis ípsilon igual a dois, e entre as retas ípsilon igual a xis e ípsilon igual a dois xis. Calcule a área dela, e a massa de uma chapa com esse formato e densidade rô igual a xis vezes ípsilon. Pausa e tenta. Fatiando em pé, a fatia vai de um sobre raiz de dois até raiz de dois, e em xis igual a um as bordas trocam: até ali ela entra na hipérbole de baixo e sai na reta de cima; depois, entra na reta de baixo e sai na hipérbole de cima. Seriam duas integrais, cada uma com o seu logaritmo. Mas olha as bordas de novo: são xis ípsilon constante e ípsilon sobre xis constante.

### E2-2 · o jacobiano da volta
**Tela:** layout B (xy à esquerda, plano u, v no meio, coluna em x = 1160). Coluna C2a. Passo 1: `u = xy`, `v = y/x` (u laranja, v verde-água); as hipérboles acendem laranja, as retas verde-água; a grade nova (hipérboles e raios) cobre a região. Passo 2: `uv = y²`, `u/v = x²` ⇒ `x = \sqrt{u/v}`, `y = \sqrt{uv}`; as raízes ganham a placa `DERIVAR DÁ TRABALHO`. Passo 3 pelo **atalho**: a matriz `\dfrac{\partial(u,v)}{\partial(x,y)}` com as quatro derivadas a caneta, uma por gatilho (`y`, `x`, `-y/x^2`, `1/x`); o determinante `y·\dfrac1x − x·\left(−\dfrac{y}{x^2}\right) = \dfrac{y}{x}+\dfrac{y}{x} = \dfrac{2y}{x} = 2v` (o `y/x` vira `v` por glyph map); depois a linha-regra `\dfrac{\partial(x,y)}{\partial(u,v)}\cdot\dfrac{\partial(u,v)}{\partial(x,y)} = 1` com o selo `IR E VOLTAR = NÃO FAZER NADA`; `J = \dfrac{1}{2v}` e `|J| = \dfrac{1}{2v}` (v > 0) em lima. No palco, uma célula da grade nova acende com `ÁREA ≈ \dfrac{1}{2v}\,\Delta u\,\Delta v`.
**Gatilhos:** "Passo um"→`u`, `v` · "a grade"→grade nova · "Passo dois"→`uv`, `u/v` · "raiz"→raízes e placa · "o atalho"→a matriz da ida · "derivada de u em relação a xis"…"um sobre xis"→quatro entradas · "o determinante"→linha do det · "dois vê"→glyph map · "ir e voltar"→linha-regra e selo · "um sobre dois vê"→J · "o módulo"→|J|
> [thoughtful] Passo um: u igual a xis ípsilon e vê igual a ípsilon sobre xis. As bordas viram u igual a um, u igual a dois, vê igual a um, vê igual a dois, e a grade nova é feita de hipérboles e de raios. Passo dois: multiplicando, u vê é ípsilon ao quadrado; dividindo, u sobre vê é xis ao quadrado. Então xis é raiz de u sobre vê, e ípsilon é raiz de u vê. Derivar essas raízes dá trabalho. Então vai o atalho: calcular o jacobiano da ida, de u e vê em relação a xis e ípsilon. A derivada de u em relação a xis é ípsilon, em relação a ípsilon, xis. A de vê em relação a xis é menos ípsilon sobre xis ao quadrado, e em relação a ípsilon, um sobre xis. O determinante: ípsilon vezes um sobre xis, menos xis vezes menos ípsilon sobre xis ao quadrado. Ípsilon sobre xis mais ípsilon sobre xis: dois ípsilon sobre xis, que é dois vê. Agora, ir e voltar é não fazer nada: o jacobiano da volta vezes o da ida dá um, pela regra da cadeia. Então o jacobiano que a gente quer é um sobre dois vê. E, como vê é positivo, o módulo é o mesmo.

### E2-3 · a área e a pipa
**Tela:** layout A com o plano u, v no palco: o quadrado [1, 2] × [1, 2] em GEO translúcido, com `B_{uv}`; a célula lima. Coluna C2b: a integral montada (`|J|` voa do chip; os limites voam das bordas), de dentro (`\dfrac{1}{2v}` sai, `[u]_1^2 = 2 − 1`), de fora (`\dfrac12[\ln v]_1^2`, `\dfrac12(\ln 2 − \ln 1)`, `\ln 1 = 0` com chip), `= \dfrac{\ln 2}{2} ≈ 0{,}347` em menta, sem moldura. Depois o palco volta para o xy: as duas diagonais da pipa dos quatro cantos (vertical de (1, 1) a (1, 2): `DIAGONAL 1`; horizontal em y = √2 de (1/√2, √2) a (√2, √2): `DIAGONAL` `\dfrac{1}{\sqrt2}`); a pipa em traço GEO; `PIPA = \dfrac{1\cdot\frac{1}{\sqrt2}}{2} = \dfrac{\sqrt2}{4} ≈ 0{,}354`; as faixas entre as hipérboles e os lados da pipa acendem (a de baixo menta `ENTRA`, a de cima ALERTA `SAI`); `0{,}347 ≈ 0{,}354` com `ESTIMATIVA DA PIPA` (GEO), sem ✓: é ordem de grandeza, não igualdade.
**Gatilhos:** "um quadrado"→B_uv · "a área"→integral · "a de dentro"→linha · "dois menos um"→`[u]` · "a de fora"→linha · "logaritmo de um é zero"→chip · "logaritmo de dois sobre dois"→resultado · "a pipa"→palco xy e pipa · "diagonal vezes diagonal"→chaves e conta · "raiz de dois sobre quatro"→`≈ 0,354` · "um tiquinho"→faixas · "bate"→✓
> [serious] Passo quatro: no plano u vê, a região é o quadrado de um a dois nas duas direções. Passo cinco: a área é a integral de um a dois, da integral de um a dois, de um sobre dois vê, dê u dê vê. A de dentro é em u, e um sobre dois vê sai: fica u de um a dois, dois menos um, um. Sobra um sobre dois vê. A de fora: um meio vezes logaritmo de vê, de um a dois. Logaritmo de dois menos logaritmo de um, e logaritmo de um é zero. A área é logaritmo de dois sobre dois, mais ou menos zero vírgula trezentos e quarenta e sete. Para conferir sem integral, liga os quatro cantos: dá uma pipa. As diagonais são perpendiculares: a vertical mede um, e a horizontal, raiz de dois menos um sobre raiz de dois, que é um sobre raiz de dois. Diagonal vezes diagonal sobre dois: raiz de dois sobre quatro, zero vírgula trezentos e cinquenta e quatro. As bordas curvas tiram um tiquinho de um lado e põem do outro, e a pipa chega bem perto: é uma estimativa, não a área exata.

### E2-4 · a massa e a densidade média
**Tela:** layout A com o plano u, v; o quadrado pintado em faixas verticais de ciano (u cresce para a direita = a densidade xy). Coluna C2c: `m = \iint_R xy\,dA` com `xy` virando `u` (glyph map); `= \int_1^2\!\int_1^2 u\cdot\dfrac{1}{2v}\,du\,dv`; de dentro `\dfrac{1}{2v}\left[\dfrac{u^2}{2}\right]_1^2 = \dfrac{1}{2v}\left(\dfrac42 − \dfrac12\right) = \dfrac{1}{2v}\cdot\dfrac32 = \dfrac{3}{4v}`; de fora `\dfrac34[\ln v]_1^2 = \dfrac34(\ln 2 − 0) = \dfrac34\ln 2 ≈ 0{,}520\ \mathrm{kg}`. Conferência: `DENSIDADE MÉDIA` (Space Grotesk) e, ao lado, em MathTex, `= \dfrac{m}{A} = \dfrac{\frac34\ln2}{\frac12\ln 2} = \dfrac32`; no palco a reta u = 3/2 acende branca no meio do quadrado, com `MEIO DE 1 E 2`; ✓.
**Gatilhos:** "a massa"→linha 1 · "xis ípsilon é u"→glyph map · "a de dentro"→colchete · "quatro meios menos um meio"→linha · "três sobre quatro vê"→resultado de dentro · "a de fora"→linha · "três quartos de logaritmo de dois"→resultado · "a densidade média"→linha · "três meios"→reta u = 3/2 · "só depende de vê"→|J| acende no chip · "bem no meio"→✓
> [thoughtful] Agora a massa. A densidade é xis vezes ípsilon, e xis vezes ípsilon é u. Então a massa é a integral de u vezes um sobre dois vê, no mesmo quadrado. A de dentro: um sobre dois vê, vezes u ao quadrado sobre dois, de um a dois. Quatro meios menos um meio, três meios. Três meios vezes um sobre dois vê: três sobre quatro vê. A de fora: três quartos de logaritmo de vê, de um a dois: três quartos de logaritmo de dois, mais ou menos zero vírgula cinquenta e dois quilos. E tem conferência esperta. A densidade média é a massa dividida pela área: três quartos de logaritmo de dois, sobre um meio de logaritmo de dois, três meios. Bem no meio entre um e dois. Faz sentido: o jacobiano só depende de vê, então, na direção do u, a área se espalha por igual, e a média de u é o ponto do meio.

### E3-1 · ler a região nos limites
**Tela:** layout A. Coluna (x = 1080): o enunciado `\int_0^a\left[\int_0^{\sqrt{a^2-x^2}}\sqrt{a^2-x^2-y^2}\,dy\right]dx` + `PAUSE E TENTE`. Palco xy (origem (300, 900), a = 520 px; papel nascendo dos eixos). Leitura dos limites: `x` de `0` a `a` (âmbar, as duas marcas no eixo); uma tira em pé âmbar varre de x = 0 a x = a: entrada azul-claro em `y = 0`, saída coral em `y = \sqrt{a^2-x^2}`; a saída deixa rastro e desenha o quarto de círculo; a coluna escreve `y^2 = a^2 − x^2 ⇒ x^2 + y^2 = a^2` (glyph map: o `x²` atravessa); o quarto de disco acende GEO com `QUARTO DE DISCO`. Depois o integrando: `z = \sqrt{a^2-x^2-y^2} ⇒ x^2+y^2+z^2 = a^2` e a cena 3D `octante` entra (câmera de cima e de lado; o quarto de disco no chão, a casca da esfera por cima, opaca, em ciano escuro; os três eixos) com `UM OITAVO DE BOLA`.
Canto: `3 · O OITAVO DE BOLA`.
**Gatilhos:** "Terceiro problema"→enunciado · "pausa"→`PAUSE E TENTE` · "xis vai de zero a á"→marcas · "entra em ípsilon igual a zero"→entrada · "sai na raiz"→saída · "elevando ao quadrado"→linhas da coluna · "é o círculo"→rastro fecha o arco · "um quarto de disco"→região · "o integrando"→linha de z · "a esfera de raio á"→3D · "um oitavo de bola"→legenda
> [curious] Terceiro problema, do jeito que cai em prova: passe para polares e calcule esta integral repetida. A integral de zero a á, da integral de zero a raiz de á ao quadrado menos xis ao quadrado, de raiz de á ao quadrado menos xis ao quadrado menos ípsilon ao quadrado. Pausa e tenta. O primeiro trabalho é ler a região nos limites. Xis vai de zero a á. Para cada xis, a fatia entra em ípsilon igual a zero e sai na raiz de á ao quadrado menos xis ao quadrado. Elevando ao quadrado: ípsilon ao quadrado mais xis ao quadrado igual a á ao quadrado. É o círculo de raio á, e a região é um quarto de disco. E o integrando? Zê igual àquela raiz é a esfera de raio á, a parte de cima. A integral é o volume embaixo dela: um oitavo de bola.

### E3-2 · polares e o oitavo de bola
**Tela:** o 3D faz o pouso de cima para o quarto de disco 2D (grade entra no pouso); o raio laranja varre de θ = 0 a π/2 (verde-água) com a tira radial entrada na origem, saída no arco. Coluna C3 em duas etapas. Etapa A: `x^2+y^2 = r^2`; `0 ≤ r ≤ a`, `0 ≤ θ ≤ \dfrac{\pi}{2}`; a integral `\int_0^{\pi/2}\!\int_0^a \sqrt{a^2-r^2}\;\Rj\,dr\,d\theta` (o fator r em lima, com chave `JACOBIANO`); a linha `w = a^2 - r^2,\quad dw = -2r\,dr ⇒ r\,dr = -\dfrac{dw}{2}` (w em lilás); a linha dos limites `r = 0 → w = a^2`, `r = a → w = 0`; `\int_{a^2}^{0}\sqrt{w}\left(-\dfrac{dw}{2}\right) = \dfrac12\int_0^{a^2} w^{1/2}\,dw` com o selo `O MENOS INVERTE OS LIMITES`. Etapa B (chip `DE DENTRO` no topo): `\dfrac12\left[\dfrac23 w^{3/2}\right]_0^{a^2} = \dfrac12\cdot\dfrac23\left((a^2)^{3/2} − 0\right) = \dfrac{a^3}{3}`; a de fora `\dfrac{a^3}{3}[\theta]_0^{\pi/2} = \dfrac{a^3}{3}\left(\dfrac{\pi}{2} − 0\right) = \dfrac{\pi a^3}{6}`; a conferência `\dfrac{4\pi a^3}{3} \div 8 = \dfrac{4\pi a^3}{24} = \dfrac{\pi a^3}{6}` ✓ com um ícone da bola cortada em oito (traço GEO).
**Gatilhos:** "xis ao quadrado mais ípsilon ao quadrado é erre ao quadrado"→linha 1 · "de zero a á"→raio varre · "de zero a pi sobre dois"→θ · "vezes erre"→fator lima · "o jacobiano das polares"→chave · "dáblio igual a"→linha w · "os limites"→linha dos limites · "o sinal de menos"→selo · "dois terços"→colchete · "á ao quadrado elevado a três meios"→`(a²)^{3/2}` acende · "á ao cubo sobre três"→resultado · "a de fora"→linha · "pi á ao cubo sobre seis"→resultado · "a bola inteira"→conferência · "um oitavo"→✓
> [thoughtful] Em polares, xis ao quadrado mais ípsilon ao quadrado é erre ao quadrado, então o integrando vira raiz de á ao quadrado menos erre ao quadrado. O quarto de disco é erre de zero a á e téta de zero a pi sobre dois. E não esquece o fator: vezes erre, o jacobiano das polares. A de dentro pede uma substituição: dáblio igual a á ao quadrado menos erre ao quadrado. Dê dáblio é menos dois erre dê erre, então erre dê erre é menos dê dáblio sobre dois. Os limites mudam: erre igual a zero dá dáblio igual a á ao quadrado; erre igual a á dá dáblio igual a zero. O sinal de menos inverte os limites: fica um meio da integral de zero a á ao quadrado de dáblio elevado a um meio. A primitiva é dois terços de dáblio elevado a três meios. Em á ao quadrado, á ao quadrado elevado a três meios é á ao cubo; em zero, zero. Um meio vezes dois terços vezes á ao cubo: á ao cubo sobre três. A de fora multiplica pelo comprimento do intervalo de téta, pi sobre dois: pi á ao cubo sobre seis. Confere com a bola inteira: quatro terços de pi á ao cubo, dividido por oito, é pi á ao cubo sobre seis. Um oitavo, certinho.

### E4-1 · a elipse: polares esticadas
**Tela:** layout A. Palco: o círculo unitário (GEO) com uma célula polar lima (r ≈ 0,7, θ ≈ 0,8) se estica em x por `a` (âmbar) e em y por `b` (magenta) até a elipse de semieixos a = 1,6 e b = 1 (1 = 260 px, centro em (520, 560)); a célula estica junto. Coluna C4a: `\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}\le 1`; `x = a\,r\cos\theta`, `y = b\,r\,\mathrm{sen}\,\theta`; a substituição `\dfrac{a^2r^2\cos^2\theta}{a^2}+\dfrac{b^2r^2\mathrm{sen}^2\theta}{b^2} = r^2(\cos^2\theta+\mathrm{sen}^2\theta) = r^2 \le 1` (os pares a²/a² e b²/b² acendem e somem); a matriz `\begin{vmatrix} a\cos\theta & -a r\,\mathrm{sen}\,\theta\\ b\,\mathrm{sen}\,\theta & b r\cos\theta\end{vmatrix}`; `= abr\cos^2\theta + abr\,\mathrm{sen}^2\theta = abr` (lima); a área pela metade de cima, dobrada (selo `METADE DE CIMA × 2`, como no disco): `A = 2\int_0^{\pi}\!\int_0^1 abr\,dr\,d\theta = 2ab\left[\dfrac{r^2}{2}\right]_0^1[\theta]_0^{\pi} = 2ab\cdot\dfrac12\cdot \pi = \pi ab`; `a = b ⇒ \pi a^2` ✓ (o chip).
Canto: `4 · A ELIPSE`.
**Gatilhos:** "Quarto problema"→elipse · "Estica as polares"→o círculo estica · "xis igual a á erre"→linha · "Substituindo"→linha da substituição · "cancela"→pares somem · "seno ao quadrado mais cosseno ao quadrado"→`(cos² + sen²)` acende · "o disco de raio um"→linha final · "o determinante"→matriz · "á bê erre"→resultado · "esticar por á e por bê"→a célula ganha a chave `× ab` · "metade de cima"→selo · "pi á bê"→área · "o pi á ao quadrado"→✓
> [curious] Quarto problema: a área da elipse xis ao quadrado sobre á ao quadrado mais ípsilon ao quadrado sobre bê ao quadrado menor ou igual a um. Polares comuns não endireitam a elipse. Estica as polares: xis igual a á erre cosseno de téta, e ípsilon igual a bê erre seno de téta. Substituindo: á ao quadrado erre ao quadrado cosseno ao quadrado sobre á ao quadrado; o á ao quadrado cancela. Do mesmo jeito, o bê ao quadrado cancela. Sobra erre ao quadrado vezes cosseno ao quadrado mais seno ao quadrado, que é um. A elipse vira erre menor ou igual a um: o disco de raio um. O jacobiano: o determinante de á cosseno de téta, menos á erre seno de téta; bê seno de téta, bê erre cosseno de téta. Á bê erre cosseno ao quadrado, mais á bê erre seno ao quadrado: á bê erre. Esticar por á e por bê multiplica a área por á bê, e as polares põem o erre. Para a área, como no disco, faz a metade de cima, téta de zero a pi, e dobra. Duas vezes á bê, vezes erre ao quadrado sobre dois de zero a um, vezes téta de zero a pi: duas vezes á bê vezes um meio vezes pi, pi á bê. Com á igual a bê, volta o pi á ao quadrado do círculo.

### E4-2 · a meia elipse pesada: a massa
**Tela:** layout A. Palco: a meia elipse `x² + 4y² ≤ 1, y ≥ 0` (a = 1, b = 1/2; 1 = 560 px, centro da base em (540, 800)), pintada com o mapa ciano de `ρ = k y` (faixas horizontais, mais claro em cima); a reta de simetria x = 0 tracejada; chave `DISTÂNCIA ATÉ O EIXO` `x` = `y` (magenta) num ponto. Coluna C4b (etapa A): o enunciado `x^2+4y^2\le 1,\ y\ge0`, `\rho = k\,y`, `PAUSE E TENTE`; `\bar x = 0` (SIMETRIA); `a = 1,\ b = \dfrac12`; `x = r\cos\theta`, `y = \dfrac12 r\,\mathrm{sen}\,\theta`, `|J| = 1\cdot\dfrac12\cdot r = \dfrac{r}{2}` (o `ab r` voa do chip do E4-1); `0\le r\le1,\ 0\le\theta\le\pi`. Etapa B (massa): `m = \int_0^{\pi}\!\int_0^1 k\cdot\dfrac{r\,\mathrm{sen}\,\theta}{2}\cdot\dfrac{r}{2}\,dr\,d\theta` (o `k y` voa da legenda; o `r/2` voa do chip); `= \dfrac{k}{4}\int_0^{\pi}\mathrm{sen}\,\theta\,d\theta\int_0^1 r^2\,dr` (selo `SEPARA: SÓ θ · SÓ r` em Space Grotesk, com θ e r em MathTex); `\left[-\cos\theta\right]_0^{\pi} = -\cos\pi + \cos 0 = 1 + 1 = 2`; `\left[\dfrac{r^3}{3}\right]_0^1 = \dfrac13`; `m = \dfrac{k}{4}\cdot 2\cdot\dfrac13 = \dfrac{k}{6}` (sobe como chip, sem moldura em volta).
Canto: `4 · A MEIA ELIPSE PESADA`.
**Gatilhos:** "meia elipse"→palco · "distância até o eixo xis"→mapa e chave · "Pausa e tenta"→`PAUSE E TENTE` · "a simetria"→x̄ = 0 · "á igual a um"→linha · "um meio de erre"→|J| · "téta de zero a pi"→limites · "A massa"→integral · "separa"→selo · "menos cosseno"→colchete θ · "erre ao cubo sobre três"→colchete r · "cá sobre seis"→resultado
> [thoughtful] Agora a elipse ganha massa. Uma chapa com a forma da meia elipse xis ao quadrado mais quatro ípsilon ao quadrado menor ou igual a um, com ípsilon positivo, e densidade proporcional à distância até o eixo xis: rô igual a cá vezes ípsilon. Onde fica o centro de massa? Pausa e tenta. Pela simetria em torno do eixo ípsilon, xis barra é zero. Aqui, á é um e bê é um meio: xis igual a erre cosseno de téta, ípsilon igual a um meio de erre seno de téta, e o módulo do jacobiano é á bê erre, erre sobre dois. A meia elipse é erre de zero a um e téta de zero a pi. A massa: a integral de cá vezes ípsilon, que é cá vezes erre seno de téta sobre dois, vezes erre sobre dois. O integrando separa num pedaço só de téta e num só de erre: cá sobre quatro, vezes a integral do seno de téta de zero a pi, vezes a integral de erre ao quadrado de zero a um. A primeira: menos cosseno de pi mais cosseno de zero, um mais um, dois. A segunda: erre ao cubo sobre três, um terço. A massa é cá sobre quatro, vezes dois, vezes um terço: cá sobre seis.

### E4-3 · o momento e o centro de massa
**Tela:** o mesmo palco. Coluna C4c (etapa C, chip `m = k/6` no topo): `M_x = \iint_B y\,\rho\,dA = \int_0^{\pi}\!\int_0^1 \left(\dfrac{r\,\mathrm{sen}\,\theta}{2}\right)^2 k\,\dfrac{r}{2}\,dr\,d\theta` (y magenta, k ciano); `= \dfrac{k}{8}\int_0^{\pi}\mathrm{sen}^2\theta\,d\theta\int_0^1 r^3\,dr` (o `1/4` do quadrado e o `1/2` do jacobiano viram `1/8`); `\mathrm{sen}^2\theta = \dfrac{1-\cos 2\theta}{2}` (chip `IDENTIDADE`); `\left[\dfrac{\theta}{2} - \dfrac{\mathrm{sen}\,2\theta}{4}\right]_0^{\pi} = \dfrac{\pi}{2} - \dfrac{\mathrm{sen}\,2\pi}{4} - 0 = \dfrac{\pi}{2}`; `\left[\dfrac{r^4}{4}\right]_0^1 = \dfrac14`; `M_x = \dfrac{k}{8}\cdot\dfrac{\pi}{2}\cdot\dfrac14 = \dfrac{k\pi}{64}`. Etapa D: `\bar y = \dfrac{M_x}{m} = \dfrac{k\pi/64}{k/6} = \dfrac{k\pi}{64}\cdot\dfrac{6}{k} = \dfrac{6\pi}{64} = \dfrac{3\pi}{32} \approx 0{,}295` (o par k/k acende e some; 6/64 simplifica por 2). No palco o ⊕ desce do topo e pousa em (0; 0,295), com as chaves `0,295` (magenta) e `ALTURA 0,5` (GEO).
**Gatilhos:** "o momento em relação ao eixo xis"→linha 1 · "ípsilon vezes rô"→y e ρ acendem · "um oitavo"→linha 2 · "seno ao quadrado"→chip · "téta sobre dois"→colchete · "seno de dois pi é zero"→linha · "erre à quarta"→colchete · "cá pi sobre sessenta e quatro"→resultado · "momento sobre massa"→linha ȳ · "o cá cancela"→par some · "três pi sobre trinta e dois"→resultado · "zero vírgula duzentos e noventa e cinco"→⊕ pousa
> [serious] O momento em relação ao eixo xis é a integral de ípsilon vezes rô: ípsilon ao quadrado vezes cá, vezes o jacobiano. Ípsilon ao quadrado é erre ao quadrado seno ao quadrado de téta sobre quatro; vezes erre sobre dois, um oitavo. Fica cá sobre oito, vezes a integral de seno ao quadrado de téta de zero a pi, vezes a integral de erre ao cubo de zero a um. Para o seno ao quadrado, a identidade: seno ao quadrado é um menos cosseno de dois téta, sobre dois. A primitiva é téta sobre dois menos seno de dois téta sobre quatro. Em pi: pi sobre dois, menos seno de dois pi sobre quatro, e seno de dois pi é zero. Em zero, zero. Dá pi sobre dois. A de erre: erre à quarta sobre quatro, um quarto. O momento é cá sobre oito, vezes pi sobre dois, vezes um quarto: cá pi sobre sessenta e quatro. E ípsilon barra é momento sobre massa: cá pi sobre sessenta e quatro, dividido por cá sobre seis. Inverte e multiplica, o cá cancela, e sobra seis pi sobre sessenta e quatro: três pi sobre trinta e dois, mais ou menos zero vírgula duzentos e noventa e cinco.

### E4-4 · conferindo a massa e comparando
**Tela:** palco xy da meia elipse com uma tira em pé âmbar (x = 0,35): entrada azul-claro em y = 0, saída coral em `y = \dfrac{\sqrt{1-x^2}}{2}`. Coluna C4d: `m = \int_{-1}^{1}\!\int_0^{\sqrt{1-x^2}/2} k\,y\,dy\,dx`; de dentro `k\left[\dfrac{y^2}{2}\right]_0^{\sqrt{1-x^2}/2} = k\cdot\dfrac{1}{2}\cdot\dfrac{1-x^2}{4} = \dfrac{k(1-x^2)}{8}`; de fora `\dfrac{k}{8}\left[x - \dfrac{x^3}{3}\right]_{-1}^{1} = \dfrac{k}{8}\left(\dfrac23 + \dfrac23\right) = \dfrac{k}{8}\cdot\dfrac43 = \dfrac{k}{6}` ✓ (o chip `m = k/6` acende ao lado). Depois a comparação: o centroide ⊕ vazado em (0; 0,212) com o chip `\dfrac{4b}{3\pi} = \dfrac{4\cdot\frac12}{3\pi} = \dfrac{2}{3\pi} \approx 0{,}212` (`HOMOGÊNEA`) e o ⊕ cheio em 0,295 (`ρ = k y`); seta magenta de 0,212 para 0,295 com `A DENSIDADE PUXA PARA CIMA`. O meio disco de raio 1 aparece por trás em traço GEO fino e **achata** até a meia elipse (um movimento), levando o ⊕ vazado de 0,424 para 0,212: `ESTICA JUNTO`.
**Gatilhos:** "conferir a massa"→tira · "fatiando em pé"→linha 1 · "ípsilon ao quadrado sobre dois"→de dentro · "um oitavo"→linha · "dois terços mais dois terços"→de fora · "cá sobre seis de novo"→✓ · "se a chapa fosse homogênea"→⊕ vazado · "quatro bê sobre três pi"→chip · "achatar o meio disco"→o meio disco achata · "estica junto"→legenda · "puxa o centro para cima"→seta
> [thoughtful] Dá para conferir a massa sem polares, fatiando em pé. Xis vai de menos um a um, e ípsilon de zero até raiz de um menos xis ao quadrado, sobre dois. A de dentro: cá vezes ípsilon ao quadrado sobre dois, no topo da fatia: cá vezes um meio vezes um menos xis ao quadrado sobre quatro, cá vezes um menos xis ao quadrado sobre oito. A de fora: cá sobre oito, vezes xis menos xis ao cubo sobre três, de menos um a um. Dois terços mais dois terços, quatro terços. Cá sobre oito vezes quatro terços: cá sobre seis de novo. E se a chapa fosse homogênea? A meia elipse é o meio disco achatado pela metade, e o centroide achata junto: quatro bê sobre três pi, com bê igual a um meio, dois sobre três pi, zero vírgula duzentos e doze. A densidade que cresce para cima puxa o centro de massa para cima, até zero vírgula duzentos e noventa e cinco.

### E5-1 · a meia arruela: a área
**Tela:** o H1 volta: a meia arruela (origem em (700, 860), 1 = 230 px), grade da tela inteira, raio laranja e θ verde-água. Coluna C5a (x = 1180): `B:\ 1\le r\le 2,\ 0\le\theta\le\pi` (os limites voam das bordas: `1` do arco de dentro, `2` do de fora, `0` e `π` das duas metades da base); `\bar x = 0` (SIMETRIA); `A = \int_0^{\pi}\!\int_1^2 \Rj\,dr\,d\theta`; de dentro `\left[\dfrac{r^2}{2}\right]_1^2 = \dfrac42 - \dfrac12 = \dfrac32`; de fora `\dfrac32[\theta]_0^{\pi} = \dfrac32\,\pi`; `A = \dfrac{3\pi}{2}`. Conferência: no palco o meio disco grande acende (`\dfrac{\pi\cdot 2^2}{2} = 2\pi`) e o pequeno (`\dfrac{\pi\cdot1^2}{2} = \dfrac{\pi}{2}`); `2\pi - \dfrac{\pi}{2} = \dfrac{3\pi}{2}` ✓.
Canto: `5 · A MEIA ARRUELA`.
**Gatilhos:** "Agora sim, a meia arruela"→palco · "erre de um a dois"→limites de r · "téta de zero a pi"→limites de θ · "xis barra é zero"→linha · "A área"→integral · "erre ao quadrado sobre dois"→colchete · "três meios"→de dentro · "três pi sobre dois"→resultado · "o meio disco grande"→2π · "o pequeno"→π/2 · "a diferença"→✓
> [curious] Agora sim, a meia arruela. Em polares, ela é um retângulo: erre vai de um a dois, e téta de zero a pi. A densidade é a mesma em todo lugar; pode chamar de um. Pela simetria, xis barra é zero; falta ípsilon barra, e para ele a gente precisa da área e do momento. A área é a integral de zero a pi, da integral de um a dois, de erre dê erre dê téta: o erre é o jacobiano. A de dentro: erre ao quadrado sobre dois, de um a dois. Quatro meios menos um meio: três meios. A de fora: três meios vezes pi. A área é três pi sobre dois. E confere: o meio disco grande tem pi vezes dois ao quadrado sobre dois, dois pi. O pequeno, pi sobre dois. A diferença: três pi sobre dois.

### E5-2 · o momento e o buraco
**Tela:** o mesmo palco; o cateto `y = r\,\mathrm{sen}\,\theta` do triângulo polar (ponto em r = 1,6, θ = 1,0) acende magenta. Coluna C5b (chip `A = 3π/2` no topo): `M_x = \iint_B y\,dA = \int_0^{\pi}\!\int_1^2 r\,\mathrm{sen}\,\theta\cdot\Rj\,dr\,d\theta` (o `r sen θ` voa do cateto); de dentro `\mathrm{sen}\,\theta\left[\dfrac{r^3}{3}\right]_1^2 = \mathrm{sen}\,\theta\left(\dfrac83 - \dfrac13\right) = \dfrac73\,\mathrm{sen}\,\theta`; de fora `\dfrac73\left[-\cos\theta\right]_0^{\pi} = \dfrac73(1+1) = \dfrac{14}{3}`; `\bar y = \dfrac{14/3}{3\pi/2} = \dfrac{14}{3}\cdot\dfrac{2}{3\pi} = \dfrac{28}{9\pi} \approx 0{,}990`. No palco o ⊕ desce e pousa em (0; 0,990), **dentro do buraco**, a 0,01 da borda r = 1; uma lupa (fundo opaco, ×10) mostra o ⊕ e a borda com `0,990 < 1`; `NO BURACO` em ALERTA.
**Gatilhos:** "o momento"→linha 1 · "ípsilon é erre seno de téta"→cateto voa · "erre ao cubo sobre três"→colchete · "oito terços menos um terço"→linha · "sete terços de seno"→resultado · "menos cosseno"→colchete θ · "catorze terços"→M_x · "momento sobre área"→ȳ · "vinte e oito sobre nove pi"→resultado · "zero vírgula novecentos e noventa"→⊕ pousa · "um centésimo"→lupa · "cai no buraco"→`NO BURACO`
> [serious] O momento em relação ao eixo xis é a integral de ípsilon dê á, e ípsilon é erre seno de téta. Fica a integral de erre seno de téta vezes erre, dê erre dê téta. A de dentro: seno de téta vezes erre ao cubo sobre três, de um a dois. Oito terços menos um terço, sete terços: sete terços de seno de téta. A de fora: sete terços vezes menos cosseno de téta, de zero a pi. Menos cosseno de pi é um; mais cosseno de zero, um: dois. O momento é catorze terços. E ípsilon barra é momento sobre área, porque a densidade é um: catorze terços sobre três pi sobre dois. Inverte e multiplica: catorze terços vezes dois sobre três pi, vinte e oito sobre nove pi. Mais ou menos zero vírgula novecentos e noventa. Menor que um, por um centésimo. O centro de massa da meia arruela homogênea cai no buraco.

### E5-3 · o fio de prumo
**Tela:** cartão 2D (grade padrão). A meia arruela em GEO opaco, presa por um alfinete branco na ponta de fora da base, à direita (2, 0). Ela **gira** em torno do alfinete até o repouso (um movimento, 1,5 s, sem balanço): o ⊕ fica exatamente abaixo do alfinete; o fio de prumo (traço branco fino com um peso pequeno) cai do alfinete e atravessa o buraco. A chapa volta à posição original com a linha do fio desenhada nela (tracejado branco). Depois o mesmo pela outra ponta (−2, 0): segunda linha. As duas linhas se cruzam no buraco, no ⊕. Legenda `O EQUILÍBRIO FICA NO AR`. Embaixo, três miniaturas em traço GEO com o ⊕ fora do corpo: `ANEL`, `FERRADURA`, `BUMERANGUE`.
**Gatilhos:** "recorta essa meia arruela"→chapa · "pendura por uma ponta"→alfinete · "ela gira"→a chapa gira · "fio de prumo"→fio · "pela outra ponta"→segunda · "se cruzam"→cruzamento e ⊕ · "no ar"→legenda · "anel"…"bumerangue"→miniaturas
> [excited] Dá para ver isso em casa. Recorta essa meia arruela num papelão e pendura por uma ponta, com um alfinete. Ela gira até o centro de massa ficar bem embaixo do alfinete. Pendura um fio de prumo no mesmo alfinete e risca a linha do fio. Agora pendura pela outra ponta e risca de novo. As duas linhas se cruzam no buraco, no ar, onde não tem papelão. O centro de massa não precisa estar dentro do corpo. Acontece com um anel, com uma ferradura, com um bumerangue. Nesses corpos, o ponto de equilíbrio fica fora da peça.

### E5-4 · a borda mais pesada
**Tela:** layout A, palco da meia arruela com o mapa radial `ρ = k r` (ciano cresce para fora). Coluna C5c em duas etapas. Etapa A (massa): `m = \int_0^{\pi}\!\int_1^2 (k\,r)\cdot\Rj\,dr\,d\theta` com as chaves `DENSIDADE` (ciano, no primeiro r) e `JACOBIANO` (lima, no segundo); de dentro `k\left[\dfrac{r^3}{3}\right]_1^2 = k\left(\dfrac83-\dfrac13\right) = \dfrac{7k}{3}`; de fora `\dfrac{7k}{3}[\theta]_0^{\pi} = \dfrac{7k\pi}{3}`. Etapa B (chip `m = 7kπ/3`): `M_x = \int_0^{\pi}\!\int_1^2 r\,\mathrm{sen}\,\theta\cdot k\,r\cdot \Rj\,dr\,d\theta`; de dentro `k\,\mathrm{sen}\,\theta\left[\dfrac{r^4}{4}\right]_1^2 = k\,\mathrm{sen}\,\theta\left(\dfrac{16}{4}-\dfrac14\right) = \dfrac{15k}{4}\,\mathrm{sen}\,\theta`; de fora `\dfrac{15k}{4}\cdot 2 = \dfrac{15k}{2}` (o `2` voa do chip `∫sen = 2` do E5-2); `\bar y = \dfrac{15k/2}{7k\pi/3} = \dfrac{15k}{2}\cdot\dfrac{3}{7k\pi} = \dfrac{45}{14\pi} \approx 1{,}023`. Etapa C, a comparação (alvo): coluna limpa com dois chips (`\dfrac{28}{9\pi}\approx 0{,}990` e `\dfrac{45}{14\pi}\approx 1{,}023`); régua em pé ampliada (0,98 a 1,03 em 600 px) à direita do palco, com as guias tracejadas das alturas: 0,990 (`HOMOGÊNEA`, branco, no buraco), 1,000 (`BORDA DO BURACO`, ALERTA), 1,023 (`ρ = k r`, ciano, na chapa); o ⊕ sobe do buraco para a chapa; `VOLTA PARA A CHAPA` em menta.
**Gatilhos:** "E se a borda pesar mais"→mapa · "dois erres"→chaves · "a massa"→integral · "sete cá sobre três"→de dentro · "sete cá pi sobre três"→m · "o momento"→integral · "três erres"→os três r acendem · "erre à quarta sobre quatro"→colchete · "quinze cá sobre quatro"→de dentro · "o mesmo dois"→o 2 voa · "quinze cá sobre dois"→M_x · "o cá cancela"→par some · "quarenta e cinco sobre catorze pi"→resultado · "um vírgula zero vinte e três"→régua e ⊕ sobe · "volta para a chapa"→legenda
> [curious] E se a borda pesar mais, com a densidade crescendo com a distância até o centro: rô igual a cá vezes erre? Agora aparecem dois erres na massa, e cada um tem um dono: um é da densidade, o outro é do jacobiano. A massa é a integral de cá erre vezes erre. A de dentro: cá vezes erre ao cubo sobre três, de um a dois: oito terços menos um terço, sete cá sobre três. A de fora multiplica por pi: sete cá pi sobre três. No momento, entram três erres: o ípsilon, que é erre seno de téta, a densidade e o jacobiano. A de dentro: cá seno de téta vezes erre à quarta sobre quatro, de um a dois. Dezesseis quartos menos um quarto, quinze quartos. A de fora traz o mesmo dois da integral do seno: quinze cá sobre dois. Ípsilon barra é quinze cá sobre dois, dividido por sete cá pi sobre três. Inverte e multiplica, o cá cancela: quarenta e cinco sobre catorze pi. Mais ou menos um vírgula zero vinte e três. Maior que um: com a borda mais pesada, o centro de massa volta para a chapa, por dois centésimos.

### E6-1 · Pappus: o volume pelo centroide
**Tela:** cena 3D `pappus` (Three.js). (1) O meio disco de raio a (GEO claro, opaco) em pé sobre o eixo x (âmbar), com um quadradinho lima a uma altura y e a chave `y` (magenta). (2) O meio disco gira em torno do eixo x (ângulo φ de 0 a 2π, 6 s, com começo e fim suaves) e o sólido varrido nasce atrás dele (ciano escuro opaco, só a parte já varrida); o quadradinho deixa um anel lima fino de raio y: legenda `ANEL DE COMPRIMENTO 2πy`. Ao fim, a bola inteira. (3) Corte para 2D (pouso do 3D para a vista de frente, ortográfica, grade entra): coluna C6a (x = 1120): `\Delta V \approx 2\pi y\,\Delta A`; `V = \iint_B 2\pi y\,dA` (glyph map, Δ → d e a soma vira ∬); `= 2\pi\iint_B y\,dA = 2\pi\,M_x` (o 2π sai); `= 2\pi\,\bar y\,A` (porque `\bar y = \dfrac{M_x}{A}` na chapa homogênea; chip). Selo grande: `VOLUME = ÁREA × CAMINHO DO CENTROIDE` com `2\pi\bar y` sob `CAMINHO`. Embaixo, à esquerda, a fatia deitada do meio disco na altura y (comprimento `L(y)`, entrada azul-claro, saída coral) e a linha `\iint_B 2\pi y\,dA = \int_0^a 2\pi y\,L(y)\,dy` com o selo `CASCAS DO CÁLCULO I`.
Canto: `6 · O TEOREMA DE PAPPUS`.
**Gatilhos:** "Último problema"→3D · "gira em torno do eixo xis"→começa a girar · "um anel"→anel lima · "dois pi ípsilon"→legenda · "a bola"→fim do giro · "Somando"→pouso e coluna · "dois pi sai"→linha · "momento"→M_x · "ípsilon barra vezes a área"→linha · "o caminho do centroide"→selo · "fatia deitada"→a fatia · "o método das cascas"→linha e selo
> [excited] Último problema, e ele junta tudo. Pega uma chapa homogênea acima do eixo xis e gira em torno do eixo xis. Ela varre um sólido. Qual o volume? Olha um quadradinho da chapa, de área delta á, a uma altura ípsilon. Girando, ele desenha um anel de comprimento dois pi ípsilon, e varre um volume de mais ou menos dois pi ípsilon vezes delta á. Somando, no limite: o volume é a integral dupla de dois pi ípsilon dê á. O dois pi sai, e o que sobra é o momento em relação ao eixo xis. E o momento é ípsilon barra vezes a área. Então o volume é a área vezes dois pi ípsilon barra: a área, vezes o caminho que o centroide percorre numa volta. Esse é o teorema de Pappus. E não é mágica: fatiando deitado, cada fatia, de comprimento éle de ípsilon, gira e vira uma casca de cilindro. É o método das cascas do Cálculo um, com a fatia inteira.

### E6-2 · a bola confere o meio disco
**Tela:** 3D `pappus` com o meio disco de raio a; o ⊕ vazado (centroide) em `4a/(3π)` desenha o seu círculo magenta tracejado durante um giro (a bola completa fica só em contorno de traço GEO, para o círculo do centroide aparecer). Coluna C6b: `\bar y = \dfrac{4a}{3\pi}` (chip `MEIO DISCO HOMOGÊNEO`); `A = \dfrac{\pi a^2}{2}`; `V = 2\pi\cdot\dfrac{4a}{3\pi}\cdot\dfrac{\pi a^2}{2}`; `= \dfrac{8a}{3}\cdot\dfrac{\pi a^2}{2}` (o π de cima cancela o de baixo); `= \dfrac{8\pi a^3}{6} = \dfrac{4\pi a^3}{3}` ✓ `A BOLA`.
**Gatilhos:** "o meio disco"→3D · "quatro á sobre três pi"→chip e ⊕ · "a área"→A · "o volume"→linha · "o pi cancela"→par some · "oito á sobre três"→linha · "quatro terços de pi á ao cubo"→✓ · "a bola"→legenda
> [happy] Testa no meio disco de raio á. O centroide dele fica a quatro á sobre três pi da base, e a área é pi á ao quadrado sobre dois. Girando em torno da base, ele varre uma bola. Pappus diz: dois pi vezes quatro á sobre três pi, vezes pi á ao quadrado sobre dois. Dois pi vezes quatro á sobre três pi: o pi cancela, oito á sobre três. Vezes pi á ao quadrado sobre dois: oito pi á ao cubo sobre seis, quatro terços de pi á ao cubo. O volume da bola, sem integral nenhuma.

### E6-3 · a casca confere a meia arruela
**Tela:** 3D `pappus` com a meia arruela 1 ≤ r ≤ 2: o giro varre a bola oca (o sólido parcial mostra o oco pela face do corte, como uma laranja descascada por dentro); depois pouso 2D. Coluna C6c: `V = \dfrac43\pi\cdot2^3 - \dfrac43\pi\cdot1^3 = \dfrac43\pi(8-1) = \dfrac{28\pi}{3}` (os raios 2 e 1 voam das bordas); `V = 2\pi\,\bar y\,A ⇒ \bar y = \dfrac{V}{2\pi A}` (glyph map: o `2πA` atravessa a igualdade); `= \dfrac{28\pi/3}{2\pi\cdot 3\pi/2}` (o `A = 3π/2` voa do chip do E5-1); `2\pi\cdot\dfrac{3\pi}{2} = 3\pi^2`; `= \dfrac{28\pi}{3}\cdot\dfrac{1}{3\pi^2} = \dfrac{28}{9\pi}` ✓ e o chip `\dfrac{28}{9\pi}` do E5-2 desce e encaixa ao lado: `O MESMO NÚMERO`.
**Gatilhos:** "a meia arruela"→3D · "uma bola oca"→o oco aparece · "a bola de raio dois menos a de raio um"→linha V · "vinte e oito pi sobre três"→resultado · "Pappus ao contrário"→glyph map · "a área"→A voa · "três pi ao quadrado"→linha · "vinte e oito sobre nove pi"→✓ · "o mesmo número"→chip encaixa
> [excited] Agora a meia arruela. Girando em torno da base, ela varre uma bola oca: a bola de raio dois menos a bola de raio um. O volume é quatro terços de pi vezes dois ao cubo, menos quatro terços de pi vezes um ao cubo: quatro terços de pi vezes oito menos um, vinte e oito pi sobre três. Agora usa Pappus ao contrário: ípsilon barra é o volume dividido por dois pi vezes a área. A área é três pi sobre dois, e dois pi vezes três pi sobre dois é três pi ao quadrado. Vinte e oito pi sobre três, dividido por três pi ao quadrado: vinte e oito sobre nove pi. O mesmo número da integral. Duas contas que não têm nada a ver, e o centro de massa cai no buraco nas duas.

### E6-4 · a família: do meio disco ao arame
**Tela:** layout A. Palco 2D: meia arruela genérica de raios `a` (dentro) e `b` (fora), com um `ValueTracker` em a; o ⊕ vazado acompanha a altura pela fórmula. Coluna C6d: `\bar y = \dfrac{\frac43\pi(b^3-a^3)}{2\pi\cdot\frac{\pi}{2}(b^2-a^2)} = \dfrac{4(b^3-a^3)}{3\pi(b^2-a^2)}`; as fatorações `b^3-a^3 = (b-a)(a^2+ab+b^2)` e `b^2-a^2 = (b-a)(a+b)` (o par `(b − a)` acende e some); `\bar y = \dfrac{4(a^2+ab+b^2)}{3\pi(a+b)}`. Dois casos-limite por chips, com o palco acompanhando: `a = 0:\ \dfrac{4b^2}{3\pi b} = \dfrac{4b}{3\pi}` (`MEIO DISCO`; o buraco some); `a = b:\ \dfrac{4\cdot 3b^2}{3\pi\cdot 2b} = \dfrac{2b}{\pi} \approx 0{,}64\,b` (`ARAME`; a chapa afina até virar um arco de arame, e o ⊕ fica a 0,64 b, no ar).
**Gatilhos:** "em geral"→palco genérico · "raios á e bê"→chaves · "a mesma conta"→linha 1 · "fatora"→fatorações · "bê menos á cancela"→par some · "com á igual a zero"→chip 1 e o buraco some · "o meio disco"→legenda · "á igual a bê"→chip 2 e a chapa afina · "dois bê sobre pi"→resultado · "arame"→legenda
> [thoughtful] E a mesma conta vale para qualquer meia arruela, de raio de dentro á e raio de fora bê. Quatro terços de pi vezes bê ao cubo menos á ao cubo, dividido por dois pi vezes pi sobre dois vezes bê ao quadrado menos á ao quadrado: quatro vezes bê ao cubo menos á ao cubo, sobre três pi vezes bê ao quadrado menos á ao quadrado. Fatora as duas diferenças. Bê ao cubo menos á ao cubo é bê menos á, vezes á ao quadrado mais á bê mais bê ao quadrado. Bê ao quadrado menos á ao quadrado é bê menos á, vezes á mais bê. O bê menos á cancela. Com á igual a zero, sem buraco: quatro bê ao quadrado sobre três pi bê, quatro bê sobre três pi, o meio disco. Com á igual a bê, a chapa vira um arame dobrado em meia volta: quatro vezes três bê ao quadrado, sobre três pi vezes dois bê, dois bê sobre pi. O centro de um arame em semicírculo fica a sessenta e quatro por cento do raio, no ar.

### E6-5 · a rosquinha
**Tela:** 3D `pappus` com o disco de raio 1 e centro a 2 do eixo (o disco em pé, chave `2` magenta do eixo até o centro, chave `1` do raio); o giro varre o toro opaco; o centro do disco desenha o círculo magenta tracejado de raio 2. Coluna C6e: `V = 2\pi\cdot 2\cdot\pi\cdot1^2 = 4\pi^2 \approx 39{,}5`, com as chaves `CAMINHO DO CENTRO` sob `2π · 2` e `ÁREA DO DISCO` sob `π · 1²`.
**Gatilhos:** "uma rosquinha"→3D · "a dois do eixo"→chave 2 · "raio um"→chave 1 · "o centro do disco"→círculo do centro · "dois pi vezes dois"→caminho · "pi vezes um ao quadrado"→área · "quatro pi ao quadrado"→resultado
> [happy] E um bônus: uma rosquinha. Um disco de raio um, com o centro a dois do eixo, girando em volta dele. O centroide do disco é o próprio centro, que percorre dois pi vezes dois. A área é pi vezes um ao quadrado. O volume do toro é quatro pi ao quadrado, mais ou menos trinta e nove vírgula cinco. Uma linha de conta.

### S1 · síntese: os cinco erros
**Tela:** cartão (grade padrão), cinco linhas que entram uma por gatilho, cada uma com ✗ ALERTA à esquerda e a correção em menta à direita: `ESQUECER O JACOBIANO` → `dA = r\,dr\,d\theta` · `JACOBIANO SEM MÓDULO, OU O DA IDA` → `|J|` e `INVERTA O DA IDA` (Space Grotesk) · `LIMITES SEM DESENHAR` → `BORDA POR BORDA` · `DIVIDIR PELA ÁREA COM ρ VARIÁVEL` → `\bar y = \dfrac{M_x}{m}` · `PAPPUS COM CHAPA NÃO HOMOGÊNEA` → `SÓ COM O CENTROIDE`. No fim, a miniatura da meia arruela com os dois ⊕ (0,990 e 1,023).
**Gatilhos:** "Resumindo"→cartão · "esquecer o jacobiano"→linha 1 · "o módulo"→linha 2 · "desenhar a região"→linha 3 · "dividir pela área"→linha 4 · "Pappus"→linha 5 · "a meia arruela"→miniatura
> [serious] Resumindo, os cinco erros que mais custam ponto neste módulo. Um: esquecer o jacobiano. Em polares, dê á é erre dê erre dê téta, sempre. Dois: usar o jacobiano sem módulo, ou usar o da ida no lugar do da volta. Se só a ida é fácil, inverte. Três: escrever os limites da região nova sem desenhar. Borda por borda, e os cantos conferem. Quatro: no centro de massa com densidade variável, dividir pela área. Divide pela massa: momento sobre massa. E cinco: usar Pappus com chapa não homogênea. Pappus fala do centroide, a geometria pura. E a meia arruela? Homogênea, o equilíbrio cai no buraco, em zero vírgula novecentos e noventa. Com a borda mais pesada, volta para a chapa, em um vírgula zero vinte e três.

### S2 · o próximo vídeo e CTA
**Tela:** à esquerda, a chapa [0, 2]² com o mapa ciano de `x² + y²` (a do quadrado da massa) em perspectiva 2D leve; ela **ganha altura** e vira um cubo de lado 2 em traço GEO (sem 3D novo: a extrusão é desenhada em Manim com três faces em perspectiva fixa), com o mapa ciano de `x² + y² + z²` nas faces visíveis e `MAIS PESADO LONGE DO CANTO`; `QUANTO PESA ESTE CUBO?`; uma caixinha lima pequena dentro do cubo com `Δx Δy Δz`. **Cartão:** moldura, `NO PRÓXIMO VÍDEO` e `INTEGRAL TRIPLA` entram juntos no gatilho "no próximo vídeo"; fica ≥ 8 s. Depois o CTA padrão (logo, anéis, INSCREVA-SE) com o desafio `A PARTIR DE QUE BURACO O CENTRO CAI NELE?`.
**Gatilhos:** "toda massa foi de chapa"→chapa · "dentro de um sólido"→a chapa vira cubo · "longe de um canto"→mapa e legenda · "Quanto pesa"→pergunta · "caixinhas"→caixinha · "no próximo vídeo"→cartão · "deixa o like"→CTA · "a partir de que tamanho de buraco"→desafio
> [curious] Até aqui, toda massa foi de chapa: densidade por área, integral dupla. E se a densidade mudar dentro de um sólido, ponto a ponto? Um cubo de lado dois, por exemplo, mais pesado longe de um canto: a densidade é xis ao quadrado mais ípsilon ao quadrado mais zê ao quadrado. Quanto pesa esse cubo? Aí a massa vira uma soma de caixinhas em três dimensões: a integral tripla. É o que a gente começa no próximo vídeo. [happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e fica o desafio para os comentários: a partir de que tamanho de buraco o centro de massa da meia arruela homogênea cai dentro dele? Dica: a fórmula da família já tem tudo. Até a próxima!

---

## Anexo B · Como cada símbolo é lido na fala

| Símbolo | Leitura | Primeira âncora |
|---|---|---|
| ∬_A f dA | integral dupla, em A, de f, dê á | E1-1 |
| e^{y − x²} | é elevado a ípsilon menos xis ao quadrado | E1-1 |
| u, v | u, vê | E1-2 |
| ∂(x, y)/∂(u, v), J | o jacobiano (de xis, ípsilon em relação a u, vê); ∂ não é lido sozinho | E1-2 |
| \|J\| | o módulo do jacobiano | E1-2 |
| B_uv | bê u vê | E1-4 |
| [F]ₐᵇ | F, de á a bê | E1-3 |
| ln v | logaritmo de vê | E2-3 |
| √(u/v) | raiz de u sobre vê | E2-2 |
| ρ | rô | E2-1 |
| r, θ | erre, téta | E3-2 |
| w | dáblio | E3-2 |
| (a²)^{3/2} | á ao quadrado elevado a três meios | E3-2 |
| a, b (semieixos) | á, bê | E4-1 |
| x̄, ȳ | xis barra, ípsilon barra | E4-2 |
| M_x | o momento em relação ao eixo xis (na coluna, "eme xis") | E4-3 |
| m | a massa (na coluna, "eme") | E4-2 |
| k | cá | E4-2 |
| sen²θ | seno ao quadrado de téta | E4-3 |
| ΔA, ΔV | delta á, delta vê | E6-1 |
| L(y) | éle de ípsilon | E6-1 |
| ≈ | mais ou menos | E1-3 |
