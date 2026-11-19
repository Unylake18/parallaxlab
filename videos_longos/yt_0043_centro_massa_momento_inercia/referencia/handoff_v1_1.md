# HANDOFF v1.1 · yt_0043 · CÁLCULO III · EP. 18 · Centro de massa e momento de inércia na integral tripla · PREVIEW

> Handoff para o **Claude Code** no repositório. Substitui o v1; a v1.1 incorpora a revisão do GPT nas regras de proteção, escolha da base, sincronização e QA, sem mudar matemática, narração, alvos, cenas ou glyph maps. Tudo o que você precisa está aqui, no `AGENTS.md` e no zip `yt0043_handoff_v1_1_completo.zip`. Ele já traz as regras que o yt_0041 (EP. 16) levou quatro previews para acertar (§5.1 e §7.2): aplique desde o primeiro render.
> Fase aberta: **preview silencioso 960×540 / 15 fps**. Não faça voz, SRT, 1080p, master, entrega, commit, branch nem push.
> Número `yt_0043` e EP. 18 são **provisórios** até o Kaio confirmar.

---

## 0. Como trabalhar (leia primeiro)

### 0.0 Estado inicial

1. Rode `git status --short` e guarde a saída no relatório. Preserve tudo o que existe. Nada de limpeza geral do repositório.
2. **Inspecione antes de extrair.** Procure uma unidade `videos_longos/yt_0043_*`:
   - não existe: crie (§2);
   - existe e está vazia: reutilize;
   - tem trabalho desta produção: registre o estado e continue dali, sem apagar;
   - tem trabalho de origem incerta, de outro agente, ou arquivos que seriam sobrescritos: **não apague nem substitua**; relate o conflito e pare só a operação afetada.
3. Descompacte `yt0043_handoff_v1_1_completo.zip` numa pasta **fora** da unidade e copie as referências para `referencia/` sem sobrescrever nada que já exista.
4. Arquivo indispensável ausente = bloqueio daquela etapa. Não recrie alvo nem trecho de narração por aproximação.

### 0.1 Fontes de verdade e precedência

1. `AGENTS.md`: ambiente, Git, regras do canal.
2. `referencia/yt_0043_narracao_v1.md`: âncoras, fala, gatilhos, **conteúdo e momento** de cada ação.
3. `referencia/yt_0043_quadros_alvo_v1/` (+ `sb43.html`, `c3d43.html`): **posição, tamanho, câmera e cor**.
4. `referencia/calculo3_35t4_centro_massa_momento_inercia_proposta_v1.md` §4: **matemática**, conta inteira C1–C10 (C11 é reserva e não vai à tela).
5. Este handoff: implementação, lotes, restrições e QA. O detalhe de um elemento (ex.: §7.1) vale sobre a regra genérica (ex.: coluna em 1020; o bloco B4 tem coluna em 780, a B4-4/B4-5 em 1300).
6. A unidade-base (§2): só para portar uma funcionalidade concreta.

Conflito objetivo de matemática: preserve a proposta e a narração, registre e não invente. Referência ausente: não substitua por aproximação sua.

### 0.2 Regras da passada

1. Não altere arquivos fora de `videos_longos/yt_0043_centro_massa_momento_inercia/`.
2. Leia o `AGENTS.md` da raiz. Este handoff **não** o substitui; quando os dois parecerem divergir, siga este handoff no conteúdo e o AGENTS.md no ambiente (uv, Manim, CRF).
3. **Escopo: o vídeo inteiro numa passada só.** Você para só no fim, com o preview completo e o relatório do §9. Mas trabalha **lote a lote, nesta ordem**, e cada lote só começa quando o anterior passou no QA do §8:
   1. `PB2` primeiro (B2-1, B2-2: a taça). A B2-2 (§7.1) calibra escrita, caneta, glyph maps, papel, tamanhos **e** o primeiro 3D com rótulos presos. Compare com os alvos 08 e 09 antes de seguir.
   2. `PB1` (B1-1 a B1-3): três cenas 3D da lata em traço; meça o alinhamento ≤ 2 px.
   3. `PB3`, `PB4`, `PH`, `PA`, `PS`, nesta ordem.
   4. `montar.py` e o QA do vídeo inteiro.
   Ordem do vídeo montado: **PH, PA, PB1, PB2, PB3, PB4, PS**.
   Lote reprovado: corrija só esse lote com o teste mais barato que pega o problema. Nunca declare pronto um lote reprovado nem o use de base. **Bloqueio real**: não simule evidência, não contorne em silêncio; entregue o parcial verificável e diga o que falta.
   Ao fechar cada lote, anote na `ficha.md` (seção Estado) o lote, o tempo de render e o resultado do QA.
4. **Não invente.** Nada de efeito que não esteja escrito aqui (brilho, pulso, partículas, sombra, transparência, câmera passeando, tracer). Na dúvida, o mais simples, e anote.
5. **Olhe os quadros.** Cada lote termina com stills 1920×1080 nativos comparados lado a lado com o quadro-alvo **v1** do mesmo instante, olhados em resolução cheia.

## 1. O que entregar

| Saída | Caminho |
|---|---|
| Preview silencioso do vídeo inteiro (≈ 21:48, 960×540, 15 fps) | `renders/v1/yt_0043_preview_v1_540p15.mp4` |
| Um mp4 por lote | `media_<LOTE>/videos/cena/540p15/<LOTE>.mp4` |
| QA (relatórios do §8) | `renders/v1/qa/` |
| Comparação com os 23 alvos (seu still 1920×1080 ao lado do alvo, no instante de `self.marca`) | `renders/v1/qa/comparacao/NN_<cena>.jpg` + `prancha_alvos.jpg` |
| Alinhamento 3D (rótulo × ponto, por lote) | `renders/v1/qa/alinhamento3d_v1.txt` |
| Tamanhos medidos (altura real das letras, por bloco) | `renders/v1/qa/tamanhos_v1.txt` |
| Atraso de cada gatilho | `renders/v1/qa/gatilhos_v1.txt` |
| `ficha.md` com a seção Estado atualizada | na unidade |

**Resolução do QA:** os stills de comparação, tamanho e alinhamento são **renderizados nativamente em 1920×1080** por `still.sh` (`manim -r 1920,1080 -s` no instante pedido). Ampliar quadro de 540p não vale. Isso não autoriza master nem vídeo 1080p.

## 2. Criar a unidade

```
videos_longos/yt_0043_centro_massa_momento_inercia/
  ficha.md                  (§2.1)
  referencia/               ← copie: yt_0043_narracao_v1.md, este handoff, a proposta, yt_0043_quadros_alvo_v1/, verificacao/
  kit.py  v41.py            ← copie da unidade-base SEM mudar nada (biblioteca da série)
  k43.py                    ← copie o k4N.py da base e adapte (§3.2)
  cena.py  render.sh  render3d.sh  seco.sh  still.sh  montar.py  quadros.py  gerar_ancoras.py  qa43.py
  sec_h.py sec_a.py sec_b1.py sec_b2.py sec_b3.py sec_b4.py sec_s.py
  threejs/  r3d.js  package.json  cena3d/c43.js + uma página .html por cena (§4)
```

**Unidade-base:** `videos_longos/yt_0042_coordenadas_cilindricas/` **se** a `ficha.md` dela registrar o preview com todos os lotes aprovados no QA do handoff v1.2 (é a irmã imediata: mesma lata, mesmo triângulo, mesmo `cta`). Se não, `videos_longos/yt_0041_coordenadas_esfericas/` no estado atual (preview v4 / handoff final). A existência de um mp4 **não** prova aprovação: vale o registro do QA na `ficha.md` e os arquivos presentes. Diga no relatório qual base usou e a evidência. A base é só leitura. Copie os arquivos listados; **não** copie `renders/`, `media_*`, `log_*`, `threejs/q3d/`, `threejs/pedidos3d/`.

Troque `yt_004N`/`4N` por `yt_0043`/`43` de forma **direcionada** (nunca substituição global: números de duração, resolução, índice, cor ou parâmetro não mudam) nos nomes de arquivo, nos cabeçalhos, em `gerar_ancoras.py` (lê `referencia/yt_0043_narracao_v1.md`) e em `montar.py` (`ORDEM = ["PH","PA","PB1","PB2","PB3","PB4","PS"]`). Confira que os dois caminhos abaixo existem antes de rodar. Os `.sh` usam o Python `K:/PycharmProjects/manim-fisica/.venv/Scripts/python.exe` e o Node com `NODE_PATH=K:/PycharmProjects/manim-fisica/videos_longos/yt_0020_cinematica_angular/threejs/node_modules`; não crie ambiente, não rode `uv sync`, `pip install` nem `npm install`.

### 2.1 ficha.md

```
formato: longo_horizontal
tipo: teoria_visual
serie_publica: CÁLCULO III · EP. 18
titulo: Centro de massa e momento de inércia na integral tripla
disciplina: Cálculo III
modulo: 3.5 Integral tripla
bloco: 3.5-T4
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §5.7 (Ex. 1 esfera em relação a um diâmetro; Ex. 2 corpo x² + y² ≤ z ≤ 1); didática do Stewart. Livro só na descrição do YouTube
unidades: s, r, x, y, z, R, h em metros; θ, φ e t em radianos; massa em kg; I em kg·m²
notacao: ρ = densidade; k = densidade constante; s = distância ao eixo z; r = distância até a origem; φ só nas esféricas; R, h fixos; (x̄, ȳ, z̄) centro de massa; M_yz, M_xz, M_xy momentos em relação aos planos; I_z momento de inércia em relação ao eixo z; s_G raio de giração; u, w, t substituições; Iₙ = ∫₀^{π/4} secⁿt dt
solido_3d: nenhum do arsenal Blender (tudo feito direto em Three.js)
3d_threejs: lataGiro, lataPesada, lataDuas, cmPontos, lataCel, lataPlano, lataSim, lataSim2, taca, giroCel, distEixo, cilindroH, esferaOct, lataParede (geometria em referencia/yt_0043_quadros_alvo_v1/c3d43.html, cenas em cenas43.js)
duracao_alvo: ≈ 21:48 (narração v1: 3.892 palavras)
```

## 3. Base de código: o que já existe e como usar

### 3.1 Camadas

- `kit.py`: `Base(Scene)` com `setup_base/corpo/fim`, relógio de âncoras (`self.an("B2-2")`; `self.gat("frase")` espera a frase de gatilho), canto do título (`TITULO = "CÁLCULO III · INTEGRAL TRIPLA"`), logo, papel, caneta `_Caneta`, `Palco3D`. **Não edite.**
- `v41.py`: paleta, `papel`, `parte`, `junta`, `pena`. **Não edite.**
- `k4N.py` → **`k43.py`**: a camada da unidade (§3.2). Funções: `L(pecas, x, y, size)` (MathTex de **string única** montado por peças com chave), `sel`, `gl`, `parte` + `self.pena`, `self.voos`, `self.gm(n, A, B, pares, copia=True, nota=…)`, `self.degrau("C4.5", "…")`, `mixl`, `chip`, `selo`, `moldura`, painel opaco, `self.rot3(palco, "ponto", tex)`, `self.palco(cena, cam_alvo("b22"), **estado)`, `self.col`, `self.sobe_sai`, `self.marca("09_B2-2")`, `self.sai_fim()`.
- Estilo de cena: o `sec_b5.py` do yt_0042 (lata pesada) ou o `sec_b4.py` do yt_0041. Uma classe por lote (`class PB2(B43)`), `ANTES = "…"`, `corpo()` que segue a fala com `self.gat(...)` frase a frase.

### 3.2 O que muda em k43.py

1. **Macros do preâmbulo** = as do topo de `referencia/yt_0043_quadros_alvo_v1/head43.js` (procure `const M=`). Iguais às do yt_0042 (`\X \Y \Z \S \T \R \de \Js \dS \dT \dZ \uu \du \Tt \dTt \tg \sen \Ci \Al \Ge \Me`) **mais as novas**: `\xb \yb \zb` (x̄, ȳ, z̄ na cor da letra), `\dm` (dm), `\ww \dw` (w e dw `#E08A3C`), `\Sg` (s_G pêssego), `\Mxy \Myz \Mxz` (M com o índice nas cores das letras), `\Jr` (o r² do jacobiano esférico em lima). O φ violeta `#B48CFF` vai como no head43.js (procure `varphi`).
2. **Câmeras e pontos 3D** = os do `c3d43.html` (§4). `cam_alvo(k)` devolve o enquadramento do alvo `k` (chaves do sb43: `h1 h2 b11a b11b b12 b13a b13b b21 b22 b31 b32 b33 b34a b34b b41 b42 b43 s2`). Os deslocamentos de tela do `keys43.js` são `OL = {dx:-100, dy:80, esc:.94}` (3D grande à esquerda) e `OC = {dx:-120, dy:150, esc:.72}` (lata pequena do bloco B4).
3. `TITULO` continua `"CÁLCULO III · INTEGRAL TRIPLA"`.
4. Nada mais muda. Vontade de "melhorar" o kit: anote no relatório.

## 4. 3D: Three.js

1. **Passada seca:** `./render3d.sh PB2` grava `threejs/pedidos3d/PB2.json`.
2. **Render 3D:** `node threejs/r3d.js --lote PB2` → `threejs/q3d/PB2_960x540/<cena>/fNNNNN.png` (fundo transparente) + `pontos.json`.
3. **Render Manim:** o `Palco3D` cola os PNGs; rótulos por `self.rot3`. Alinhamento **≤ 2 px**, medido na mesma escala: se o `pontos.json` é de 540p e o still é de 1080p, normalize antes de calcular o erro.

**Portar as cenas:** a geometria está em `referencia/yt_0043_quadros_alvo_v1/c3d43.html` (Three.js r128, `?k=taca`; o código das cenas está separado em `cenas43.js`, os helpers `cyl`, `WC`, `bolinha`, `corR`, `lataTraco`, `celC` em `_helpers.txt`). Use o `c4N.js` da base como modelo de **estrutura** (`setEstado`, `piso()`) e crie `c43.js` **com os mesmos parâmetros, câmeras e cores**. Estados animáveis (os únicos permitidos):

| Cena (chave) | Usada em | Estados (0→1) |
|---|---|---|
| `lataGiro` / `lataPesada` | H1 (`lataGiro`), B4-1 a B4-3 (`lataPesada`, escala `OC`) | `giro` (câmera ~30° em volta de z, só no H1, para antes da coluna), `seta` (seta curva de giro, H1 e B4-3), `cm` (⊕ em z ≈ 0,555 + tracejado GEO em z = 1/2, B4-2) |
| `lataDuas` | H2 | `traco` (degradê → traço), `cel1` (perto da origem), `cel2` (na quina) |
| `cmPontos` | B1-1 etapa 1 | `b1`, `b2`, `b3` (cada bolinha com o seu fio ao piso), `cm` (⊕) |
| `lataCel` | B1-1 etapa 2 | `cel` (célula Δm), `fios` (tracejados x e y no chão) |
| `lataPlano` | B1-2 | `plano` (contorno menta z = z̄), `celA` (acima, `+`), `celB` (abaixo, `−`), `fios` |
| `lataSim` | B1-3 etapa 1 | `gemeos` (duas células em θ e θ + π), `fios` |
| `lataSim2` | B1-3 etapa 2 | `lado` (o lado x > 0 escurece em ciano: ρ = 1 + x) |
| `taca` | B2-1, B2-2 | `sonda` (cresce da entrada z = s² à saída z = 1), `cm` (⊕ em z = 2/3), `meio` (tracejado em z = 1/2) |
| `giroCel` | B3-1 | `seta`, `cel`, `fio` (s), `v` (seta tangente) |
| `distEixo` | B3-2 | `P`, `s` (fio ao eixo z), `fioX` (fio GEO ao eixo x), `r` (da origem) |
| `cilindroH` | B3-3 | `casca` (raio da casca pêssego cresce de 0,1R a R) |
| `esferaOct` | B3-4 | `P`, `r`, `phi` (arco), `fio` (s) |
| `lataParede` | S2 | `eixo` (reta ALERTA em x = 1, y = 0), `seta` |

Regras do 3D: cores sólidas e opacas, sem luz dinâmica, sem brilho; a câmera só se move onde a tabela diz; no pouso para o 2D ela está parada. **Piso quadriculado em z = 0** em toda cena (`piso()` no fim do `c3d43.html`, extensões na tabela `PISOK`). PNG transparente composto **sobre o papel**.

**Câmera da lata** igual em `lataGiro`, `lataDuas`, `lataCel`, `lataPlano`, `giroCel`, `lataParede`: `ver([9.2,-6.2,5.8],[0,0,.45],600,560)`, SC = 2,2 (a origem cai no mesmo pixel). A `lataPesada` do B4 é a mesma câmera com o deslocamento `OC`.

**Escala no Manim:** quadro 16 × 9 ⇒ **1 unidade = 120 px** em 1080p (`x_m = (x_px − 960)/120`, `y_m = (540 − y_px)/120`). As funções do kit recebem px.

## 5. Sistema visual

- **Fundo:** violeta `#18143A → #0F0C26` com **papel** (quadradinhos de 60 px) de borda a borda em toda tela, também sob o 3D. Só o CTA final fica liso. Painel 2D dentro de cena 3D = painel opaco `#16123A` com grade própria de 30 px.
- **Canto:** `CÁLCULO III · INTEGRAL TRIPLA` (pequeno, apagado) + título da cena em branco (maiúsculas, Space Grotesk). Logo no canto superior direito.
- **Tamanhos (1080p):** fórmula principal 50–54 px, secundária 44–46 (as linhas longas do B4 podem ir a 40–42, como no alvo), legenda 30 (mínimo 26), chips 30. Coluna em **x = 1020** com 3D grande à esquerda; **x = 780** no B4-1 a B4-3 (lata pequena); **x = 1300** no B4-4/B4-5 (painel do triângulo à esquerda). **No máximo 6 linhas por etapa** (depois renova: o resultado vira chip no topo). Margem de 48 px.
- **Cores:** s pêssego `#FFC08A`; θ `#2EE6A6`; z azul `#5AA2FF`; x âmbar `#FFC24D`; y magenta `#EA63FF`; r laranja `#FF9440`; φ violeta `#B48CFF`; ρ ciano `#35D9FF`; **fator do jacobiano em lima `#C6F26B`** (o s das cilíndricas e o r² sen φ das esféricas); u, w, t `#E08A3C`; ALERTA `#FF5D5D`; GEO `#B8C4DA`; menta `#8CFFD2`; célula Δm lima; **⊕ do centro de massa com degradê ciano → magenta** (o mesmo da série). Operadores em branco.
- **Escrita:** termo novo = **caneta finíssima glifo a glifo, esquerda → direita**; termo que vem do desenho = **voo**; manipulação = **glyph map** (MathTex de string única nos dois lados). **Proibido:** `FadeIn` de linha pronta e destino na tela antes da hora (`FLASH POR QUADRO` = **0**).
- **Sem efeitos.** Destaque = sublinhado fino ou contorno que acende e apaga.
- **Conta inteira:** a tela mostra **todos** os degraus do §6.

### 5.1 Sistema 3D da série (G1–G6)

- **G1 · Papel sob o 3D.**
- **G2 · Piso** quadriculado em z = 0.
- **G3 · Metade esquerda.** Nada do 3D passa de **x = 975 px** nem sai de x < 60 nas peças principais (o plano do B1-2 incluído). No B4, a lata pequena fica dentro de x = 60..720.
- **G4 · Sem hastes; legenda colorida** na linha y = 1020 (quadradinho na cor + texto 30 px), itens em x = 120 / 540 (até 3 itens: 120, 440, 720). Letras de variável no desenho, em placa pequena, **fora das arestas**. No máximo 2 hastes por quadro, ≤ 90 px. Rótulos x, y, z a ≤ 30 px da ponta da seta.
- **G5 · Geometria opaca e limpa.** No máximo 8 verticais e 4 anéis em traço.
- **G6 · Tudo numa linha do papel.** Coluna e linhas de base em múltiplos de 60. Espaço entre o 3D e a coluna ≥ 60 px.

## 6. Contas (o que a tela escreve, linha a linha)

As contas completas, com ID de degrau, estão na proposta (§4, **C1–C10**), conferidas no sympy (`referencia/verificacao/`, **62/62**; inclui conferência numérica em cartesianas: I ≈ 1,5391 e M_xy ≈ 1,5318). Use os IDs em `self.degrau(...)`. Exemplo, a conta **C4** da B2-2 (a primeira que você implementa):

| degrau | linha na tela (LaTeX com as macros) |
|---|---|
| C4.1 | `\iiint\Z\,dV=\int_0^{2\pi}\!\!\int_0^1\!\!\int_{\S^2}^1\Z\,\Js\,\dZ\,\dS\,\dT` |
| C4.2 | `\int_{\S^2}^1\Z\,\S\,\dZ=\S\Big[\dfrac{\Z^2}{2}\Big]_{\S^2}^1=\S\Big(\dfrac12-\dfrac{\S^4}{2}\Big)=\dfrac{\S}{2}-\dfrac{\S^5}{2}` |
| C4.3 | `\int_0^1\Big(\dfrac{\S}{2}-\dfrac{\S^5}{2}\Big)\dS=\Big[\dfrac{\S^2}{4}-\dfrac{\S^6}{12}\Big]_0^1=\dfrac14-\dfrac1{12}=\dfrac16` |
| C4.4 | `\iiint\Z\,dV=2\pi\cdot\dfrac16=\dfrac{\pi}{3}` |
| C4.5 | `\zb=\dfrac{\pi/3}{\pi/2}=\dfrac23` em moldura menta (54 px) |

As demais linhas, já em LaTeX com as macros, estão no `keys43.js` (uma chave por alvo): copie de lá, não redigite.

**Glyph maps previstos** (monte cada um só depois de estabilizar o LaTeX dos dois lados; `show_indices` só no desenvolvimento):

| GM | Âncora | De → para |
|---|---|---|
| GM1 | B1-2 | `∭ z ρ dV − z̄ ∭ ρ dV` → `M_xy − z̄ M` (cada integral vira a sua letra) |
| GM2 | B1-2 | `M_xy − z̄ M` → `M z̄ − z̄ M = 0` (M_xy = M z̄; os dois termos acendem e saem) |
| GM3 | B1-3 | `∭ x(1 + x) dV` → `∭ x dV + ∭ x² dV` |
| GM4 | B2-2 | `[s z]_{s²}^1` → `s · 1 − s · s²` → `s − s³` (C3.2) |
| GM5 | B2-2 | `(π/3)/(π/2)` → `2/3` (os π acendem juntos e saem) |
| GM6 | B3-3 | `πkR⁴h/2` → `(1/2)(kπR²h) R²` (o R⁴ se separa em R² · R²) |
| GM7 | B3-4 | `∫₁^{−1}(1 − u²)(−du)` → `∫_{−1}^1 (1 − u²) du` (o menos acende em ALERTA e leva os limites trocados) |
| GM8 | B3-4 | `(8/15)/(4/3)` → `2/5` |
| GM9 | B4-1 | `√(s² + z²) s ds` → `(1/2) u^{1/2} du` (o s do fator e o s do du acendem juntos, sublinhado lima) |
| GM10 | B4-1 | `(z²)^{3/2}` → `z³` |
| GM11 | B4-2 | `z(1 + z²)^{3/2} dz` → `(1/2) w^{3/2} dw` |
| GM12 | B4-2 | `2π(4√2 − 2)/15` → `4π(2√2 − 1)/15` (o 2 sai do parêntese) |
| GM13 | B4-3 | `(u − z²) u^{1/2}` → `u^{3/2} − z² u^{1/2}` |
| GM14 | B4-4 | `−(1/5)z⁵ + (1/3)z⁵` → `(2/15)z⁵` |
| GM15 | B4-4 | `tg²t` → `(sec²t − 1)` → `(sec⁷t − sec⁵t)` |
| GM16 | B4-5 | `(1/3)I₅ − (1/9)I₅` → `(2/9)I₅` |
| GM17 | B4-5 | `7√2/36 − 4√2/45` → `35√2/180 − 16√2/180` → `19√2/180` |
| GM18 | B4-5 | `2π[(19√2 + 4)/180 + (1/12)ln(1 + √2)]` → `(π/90)(19√2 + 4 + 15 ln(1 + √2))` |

## 7. Cena a cena

**Fonte da verdade, nesta ordem:** (1) a narração (âncoras, Tela, Coluna, **Gatilhos**, fala); (2) os quadros-alvo (posição e tamanho; as coordenadas exatas estão no `keys43.js`, chave indicada); (3) este §7. O alvo mostra o **estado final** de uma etapa; o caminho até ele segue os gatilhos. Cada gatilho = uma frase; não há ação sem gatilho nem gatilho sem ação (exceto os marcados "nada novo").

| Âncora | Lote | Alvo (arquivo · chave) | Notas |
|---|---|---|---|
| H1 | PH | 01 · `h1` | `lataGiro` à esquerda (gira ~30° e para antes da coluna); coluna em 1020: densidade, limites da lata, cartões ① e ② (opacos), `E A LATA PESADA?` em ciano; legendas `LEVE NA ORIGEM` / `PESADA NA QUINA`. |
| H2 | PH | 02 · `h2` | `lataDuas`: degradê → traço (`ReplacementTransform` da mesma geometria), as duas células lima com `dm`; coluna: `dm = ρ dV`, ① `z · dm`, ② `s² · dm`, `SOMA DE TUDO`. |
| A1 | PA | — | 2D, papel: logo, título `CENTRO DE MASSA E MOMENTO DE INÉRCIA NA INTEGRAL TRIPLA`, linha `NESTE VÍDEO: z̄ · SIMETRIA · I = ∭ s² ρ dV · A LATA PESADA`. |
| B1-1 | PB1 | 03 · `b11a` → 04 · `b11b` | etapa 1: `cmPontos`, bolinhas uma por vez (raio ∝ massa^{1/3}), ⊕ entra perto da mais pesada; três médias. Etapa 2: troca para `lataCel` (mesmo lugar na tela), a etapa 1 vira chip; Δm → integral → M → x̄ → M_xy; legendas ȳ, z̄ e "os outros dois planos" abaixo das linhas. |
| B1-2 | PB1 | 05 · `b12` | `lataPlano`: plano menta (só contorno, dentro de x ≥ 60), células `+` e `−`; C1 com **GM1** e **GM2**; legenda menta de duas linhas. |
| B1-3 | PB1 | 06 · `b13a` → 07 · `b13b` | etapa 1: `lataSim` (gêmeos), C2.1–C2.4, cartão menta; etapa 2: `lataSim2` (lado x > 0 em ciano), C2.5–C2.9 com **GM3**, chip ALERTA `A DENSIDADE QUEBROU A SIMETRIA`. |
| B2-1 | PB2 | 08 · `b21` | `taca` à esquerda; sonda cresce de z = s² (entrada `#7FB2FF`) a z = 1 (saída `#FF7A8A`); coluna: TAÇA, cilíndricas, sombra, chip SIMETRIA, z̄ = M_xy/M com o k cancelando (os dois k acendem e saem), chip `CHUTE: z̄ = 1/2 ?` em âmbar. |
| B2-2 | PB2 | 09 · `b22` | Detalhe no §7.1. |
| B3-1 | PB3 | 10 · `b31` | `giroCel`: seta de giro + ω, célula `dm` na parede, fio s, seta v; C5; `I = ∭ s² ρ dV` em moldura menta (52 px); chip unidade. |
| B3-2 | PB3 | 11 · `b32` | `distEixo` (eixos x, y, z; P = (1; 1,2; 1)); fio s ao eixo z, fio GEO ao eixo x, r laranja da origem; três linhas por eixo; chip ALERTA `NÃO É r² = x² + y² + z²`. |
| B3-3 | PB3 | 12 · `b33` | `cilindroH`: a casca pêssego cresce até a parede (estado `casca`); C6 com a chave lima `s² · s = s³`, **GM6**; última linha `CASCA FINA: I = MR²`. **Sem painel extra.** |
| B3-4 | PB3 | 13 · `b34a` → 13b · `b34b` | `esferaOct` (octante aberto), P, r, φ, fio s; etapa 1: C7.1–C7.4; etapa 2 (= 13): C7.5–C7.9 com o limite invertido (ALERTA) e **GM7**; etapa 3 (= 13b): C7.10–C7.12 com **GM8**, moldura menta. |
| B3-5 | PB3 | 14 · `b35` | 2D: três cartões opacos (tubo, cilindro, bola) com o corte meridiano, eixo tracejado e s_G em pêssego; régua `I/MR²` com 2/5, 1/2, 1; C8 embaixo. |
| B4-1 | PB4 | 15 · `b41` | `lataPesada` pequena (`OC`), coluna em 780; chips M ≈ 2,76 e SIMETRIA; C9.2–C9.6 com as chaves ALTURA/DENSIDADE/FATOR, **GM9**, **GM10**. |
| B4-2 | PB4 | 16 · `b42` | etapa 1 (sem alvo): C9.7–C9.12 com **GM11**, **GM12**; etapa 2 (= 16): C9.13–C9.15, moldura menta ≈ 0,555, chip CONFERE; no 3D, estado `cm` (⊕ + tracejado 1/2); legendas em 120 e 700. |
| B4-3 | PB4 | 17 · `b43` | lata pequena com a `seta` de giro; chip z̄ ≈ 0,555; C10.1–C10.5 com **GM13**. |
| B4-4 | PB4 | 18 · `b44` | a lata sai; painel 2D opaco `O TRIÂNGULO` à esquerda (catetos 1 e `z = tg t`, hipotenusa `√(1 + z²) = sec t`, ângulo t); coluna em 1300; C10.6–C10.11 com **GM14**, **GM15**. |
| B4-5 | PB4 | 19 · `b45a` → 19b · `b45b` | painel no caso t = π/4; etapa 1 (sem alvo): cartão RECORRÊNCIA + C10.12–C10.15 (I₇ vira chip); etapa 2 (= 19): C10.16–C10.19 com **GM16**, **GM17**; etapa 3 (= 19b): C10.20–C10.21 com **GM18**, moldura menta ≈ 1,539, chip CONFERE. |
| B4-6 | PB4 | 20 · `b46` | 2D: dois cortes meridianos (comum GEO, pesada em degradê ciano) com o ⊕ (0,5 e 0,555) e s_G; tabela COMUM × PESADA (z̄, I/M, s_G); duas legendas. Os valores **voam** das molduras do B4-2 e do B4-5. |
| S1 | PS | — | 2D, papel; três colunas ✓ com os resultados que **voam** das fontes: taça z̄ = 2/3, cilindro e bola MR²/2 · (2/5)MR², lata pesada z̄ ≈ 0,555 · I ≈ 1,539. |
| S2 | PS | 21 · `s2` | `lataParede`: reta ALERTA na parede + seta de giro; pergunta e linha ALERTA; cartão `NO PRÓXIMO VÍDEO · EXERCÍCIOS DO MÓDULO · INTEGRAL TRIPLA` (≥ 8 s); depois o CTA liso do kit. **Não** escrever o resultado (3/2)MR² na tela: é o desafio do próximo vídeo. |

### 7.1 B2-2 em detalhe (o primeiro lote: calibra o resto)

`taca` parada à esquerda (`OL`), papel de borda a borda. Posições do alvo 09 (`keys43.js`, chave `b22`), px de 1080p:

| Elemento | Posição | Tamanho | Entra em |
|---|---|---|---|
| etapa 1: C3.1 `V = ∫₀^{2π}∫₀^1∫_{s²}^1 s dz ds dθ` (o s lima voa do chip dV do B2-1) | (1020, 270) | 46 | "Primeiro o volume" |
| C3.2 com **GM4** | (1020, 400) | 44 | "A de dentro, em z" |
| C3.3 | (1020, 530) | 44 | "Agora em s" |
| C3.4 `V = 2π · 1/4 = π/2` | (1020, 650) | 46 | "a volta inteira em téta" |
| renova: as 4 linhas sobem e saem; `V = π/2` vira chip | chip (1020, 150) | 30 | "Agora o momento" |
| C4.1 | (1020, 270) | 42 | "Agora o momento" |
| C4.2 | (1020, 400) | 40 | "o s fica parado" |
| C4.3 | (1020, 530) | 40 | "potência de novo" |
| C4.4 | (1020, 650) | 44 | "multiplica por dois pi" |
| C4.5 em moldura menta, com **GM5**; ⊕ entra no 3D em z = 2/3 com a placa `2/3` | (1030, 790) | 54 | "dois terços" |
| tracejado GEO em z = 1/2 + placa `1/2`; legenda `ACIMA DO MEIO: A TAÇA É LARGA EM CIMA` | legenda (1020, 900) | 30 | "acima do meio" |

Meça o tamanho real das letras nos stills (KaTeX e MathTex diferem) e ajuste até a fórmula principal ter 50–54 px de corpo e nada < 26 px. Nenhum silêncio: se a escrita acabar antes da frase seguinte, a tela espera parada.

### 7.2 Lições do yt_0041 que valem desde o primeiro render

1. **Rótulo sai junto com o seu objeto** (legenda, seta, chip, moldura saem no mesmo `FadeOut` da fórmula ou do desenho).
2. **A coluna de um bloco sai antes da do próximo.** Nunca duas colunas ao mesmo tempo.
3. **O painel aparece com a primeira linha dele** (painel vazio esperando é proibido). Vale para o painel do triângulo e os cartões do H1.
4. **3D inteiro dentro de x = 60..975** (B4: 60..720), nunca sob painel ou texto.
5. **Tamanho real medido**, não o pedido.
6. **Voo não cruza linha já escrita** (arco por fora; R5V = 0).
7. **Gatilho ≤ 0,3 s** da frase, sem comprimir a caneta; se não couber, liste no relatório.
8. **CTA só depois** do cartão do próximo vídeo (S2).
9. **Câmera e escala fixas** entre as cenas da lata (H1, H2, B1-1b, B1-2, B1-3, B3-1, S2) e entre as três telas do B4 (`OC`).
10. **Troca de cena 3D no mesmo bloco** (B1-1: `cmPontos` → `lataCel`; B1-3: `lataSim` → `lataSim2`): a cena nova entra no lugar da antiga num corte limpo, no gatilho; sem as duas ao mesmo tempo.

## 8. QA (rode `qa43.py`, adaptado do `qa4N.py` da base) e critérios de aceite

Cada item precisa de número medido no relatório. **Aceite = todos os itens dentro do limite.**

| # | Item | Como medir | Limite |
|---|---|---|---|
| 1 | Erros de render | `log_<LOTE>.txt` | 0 Traceback |
| 2 | Gatilhos | todo `self.gat(...)` achou a frase em `duracoes_estimadas.json` | 0 `gatilho-sem` |
| 3 | Flash por quadro | `[flash]` | **0** |
| 4 | Sobreposição texto × texto e voo × texto | `[R5]`, `[R5V]` | **0** |
| 5 | Margem e painel | `[R6]` (48 px; nada atravessa painel) | 0 |
| 6 | Papel | `[grade]`: papel em toda tela, inclusive sob o 3D; só o CTA liso | 0 s sem papel |
| 7 | Palco parado | `[parado]`: nada se move sem gatilho | 0 fora da tabela do §4 |
| 8 | Glyph maps | `[gm]`: GM1–GM18, cada um no seu lote | 100 % |
| 9 | Degraus | `[degrau]`: todos os degraus C1–C10 com tempo | 100 % |
| 10 | Texto em MathTex | fórmula como `Text` ou texto corrido dentro de MathTex | 0 |
| 11 | Tamanho **real** das letras | altura medida nos stills 1080p, tabela `qa/tamanhos_v1.txt` | principal 50–54 px, nada < 26 px |
| 12 | Alinhamento 3D | rótulo × ponto do `pontos.json` | ≤ 2 px |
| 13 | Comparação com o alvo **v1** | still do instante `self.marca(...)` ao lado do alvo, olhado em resolução cheia | ±20 px, mesmas cores, mesmo conteúdo |
| 14 | Duração | lote × soma das âncoras | ±0,5 s por âncora |
| 15 | Efeitos | busca por `Flash`, `Indicate`, `Wiggle`, `glow`, `opacity` < 1 em formas, `always_redraw` decorativo | 0 |
| 16 | Linha órfã | varredura a cada 0,5 s | 0 |
| 17 | 3D cortado ou escondido | pixels do 3D fora de x = 60..975 (B4: 60..720) e sob painel ou texto | 0 |
| 18 | G1–G6 por cena 3D | tabela OK/NÃO + prancha 2×3 por cena 3D | tudo OK |
| 19 | Atraso de gatilho | início de cada degrau × instante da frase, `qa/gatilhos_v1.txt` | ≤ 0,3 s; não acelere a caneta |
| 20 | CTA | só depois do cartão do próximo vídeo (≥ 8 s), tela lisa | R5 = 0 no S2 |

Item que não se aplica ao lote = **N/A**, nunca "OK". Rode primeiro o mais barato (`./seco.sh LOTE`) e só depois o render; refaça **só** o lote afetado.

### 8.1 Três tipos de evidência (não misture)

1. **Automático** (`qa43.py`, `seco.sh`): itens 1–10, 14–16, 19.
2. **Medido** (números em arquivo): 11 (`tamanhos_v1.txt`), 12 (`alinhamento3d_v1.txt`), 17, 19 (`gatilhos_v1.txt`).
3. **Inspeção visual** (você olhando em resolução cheia): 13, 18, 20. Para cada um dos 23 alvos: still nativo 1920×1080 no instante de `self.marca(...)`, ao lado do alvo, e uma linha no relatório com o que difere (posição, escala, cor, conteúdo, leitura). A prancha consolidada complementa; não substitui os stills.

Olhe também **instantes intermediários**, não só o estado final do alvo: entrada e saída de objetos, caneta em movimento, glyph maps, voos, trocas de cena 3D, troca de coluna, rótulos enquanto o 3D se move. Para cada cena 3D, a prancha 2×3 do item 18.

### 8.2 Sincronização

Para cada gatilho, `gatilhos_v1.txt` traz: âncora, frase, instante previsto, início da animação, desvio. Duração das âncoras **preservada**: se a escrita acabar antes, a tela espera parada; se não couber, **não acelere a caneta** e **não tire degrau**: registre âncora e segundos que faltam. Antecipar só quando a frase anterior já fala da mesma linha.

### 8.3 Montagem

Depois do `montar.py`: ordem PH → PS, nenhum lote repetido ou ausente, nenhum quadro preto inesperado, nenhuma coluna ou rótulo antigo na emenda, salto de câmera ou papel nas emendas, duração total e arquivo íntegro (abre e toca até o fim). O QA por lote não substitui isso.

### 8.4 A verificação da matemática não valida a implementação

Os 62/62 do sympy conferem a **proposta**. O que prova a implementação são os itens 8 e 9 (glyph maps e degraus com tempo) e a comparação visual: confira que cada linha na tela é a da proposta, caractere a caractere.

## 9. Relatório obrigatório (no fim, uma vez)

0. Estado inicial (`git status`), o que existia em `yt_0043_*` e a unidade-base usada (yt_0042 ou yt_0041) com a evidência.
1. Arquivos criados e alterados.
2. Comandos rodados e resultado (tempo de render por lote).
3. Tabela do §8 com o número medido de cada item, **por lote**.
4. Caminhos do vídeo, dos quadros de comparação e da pasta de QA.
5. Quantos dos 23 alvos você inspecionou de fato; o que ficou diferente do alvo e por quê; o que não conseguiu; o que **não** verificou. Nada de "QA passou" sem número e caminho.
6. Cenas Three.js: o que foi portado, resolução, custo por quadro, alinhamento medido (px).
7. Lotes concluídos e, se houver, bloqueados. Pare. Não comece voz, SRT, 1080p nem entrega.

## 10. O que não fazer

- Não alterar `template/`, `assets/`, `docs/`, `AGENTS.md`, `pyproject.toml`, `uv.lock` nem unidades de outros vídeos (a unidade-base é só leitura).
- Não usar restaurações globais (`git restore .`, `git reset --hard`, `git clean -fdx`).
- Não instalar nada, não recriar `.venv`, não rodar `npm install`.
- Não usar Blender, `ponte.py` nem `Solido3D`; não fazer 3D dentro do Manim.
- Não mudar matemática, notação, cores, texto da tela ou a narração. Se achar erro, **reporte** antes.
- Não citar livro na tela. Não citar vídeo não publicado ("como vimos no EP. 17" é proibido; "nas cilíndricas" e "das cilíndricas" são permitidos).
- Não fazer voz, SRT, 1080p, master, entrega, commit, branch, push.

## 11. Condição de parada

Pronto quando: a unidade nova existe sem ter sobrescrito trabalho anterior; todos os lotes passaram no §8; os 23 alvos v1 foram comparados em 1920×1080; o preview completo foi montado e as emendas conferidas; a `ficha.md` tem o Estado final; o relatório do §9 traz caminhos e números. **Depois disso, pare.**
