# HANDOFF v1.1 · yt_0044 · CÁLCULO III · EP. 19 · Exercícios do módulo: integral tripla · PREVIEW

> Handoff para o **Claude Code** no repositório. **Substitui o v1.** A v1.1 incorpora a revisão do GPT nas regras operacionais (captura dos stills, posições aprovadas fora da grade de 60, comparação na extração, render ≠ lote aprovado, duração como referência), sem mudar matemática, narração, alvos, cenas ou glyph maps. Tudo o que você precisa está aqui, no `AGENTS.md` e no zip `yt0044_handoff_v1_1_completo.zip`. As regras que o yt_0041 levou quatro previews para acertar e o yt_0043 confirmou (§5.1 e §7.2) valem desde o primeiro render.
> Fase aberta: **preview silencioso 960×540 / 15 fps**. Não faça voz, SRT, 1080p, master, entrega, commit, branch nem push.
> Número `yt_0044` e EP. 19 são **provisórios** até o Kaio confirmar. Duração ≈ **28:56**: é a estimativa da narração, **não** um alvo a atingir. Não acelere a escrita, não tire degrau e não estique cena para chegar num número.

---

## 0. Como trabalhar (leia primeiro)

### 0.0 Estado inicial

1. Rode `git status --short` e guarde a saída no relatório. Preserve tudo o que existe. Nada de limpeza geral do repositório.
2. **Inspecione antes de extrair.** Procure uma unidade `videos_longos/yt_0044_*`:
   - não existe: crie (§2);
   - existe e está vazia: reutilize;
   - tem trabalho desta produção: registre o estado e continue dali, sem apagar;
   - tem trabalho de origem incerta, de outro agente, ou arquivos que seriam sobrescritos: **não apague nem substitua**; relate o conflito e pare só a operação afetada.
3. Descompacte `yt0044_handoff_v1_1_completo.zip` numa pasta **fora** da unidade, confira que as referências existem e copie para `referencia/` só o que falta. Se um arquivo já existe: idêntico, mantenha; diferente com versão identificada, respeite a versão aprovada e registre; origem incerta, não sobrescreva e relate.
4. Arquivo indispensável ausente = bloqueio daquela etapa. Não recrie alvo nem trecho de narração por aproximação.

### 0.1 Fontes de verdade e precedência

1. `AGENTS.md`: ambiente, Git, regras do canal.
2. `referencia/yt_0044_narracao_v1.md`: âncoras, fala, **Tela**, **Coluna** ([ensina]/[mecânica]), **Gatilhos**: conteúdo e momento de cada ação.
3. `referencia/yt_0044_quadros_alvo_v1/` (+ `sb44.html`, `c3d44.html`, `keys44.js`, `cenas44.js`): **posição, tamanho, câmera e cor**.
4. `referencia/calculo3_35e1_exercicios_integradores_proposta_v1.md` §3: **matemática**, conta inteira C1–C6 (C6.13 é reserva e não vai à tela).
5. Este handoff: implementação, lotes, restrições e QA. O detalhe de um elemento (§7.1) vale sobre a regra genérica.
6. A unidade-base (§2): só para portar uma funcionalidade concreta.

**Precedência por assunto:** matemática = proposta; o que se fala, a ordem e o momento = narração; aparência, posição e câmera = alvos; procedimento e QA = este handoff; ambiente e Git = `AGENTS.md`.

Conflito objetivo de matemática: preserve a proposta e a narração, identifique os arquivos e a expressão, registre e não invente. Referência ausente: não substitua por aproximação sua.

### 0.2 Regras da passada

1. Não altere arquivos fora de `videos_longos/yt_0044_exercicios_integral_tripla/`.
2. Leia o `AGENTS.md` da raiz. Este handoff **não** o substitui; quando os dois parecerem divergir, siga este handoff no conteúdo e o AGENTS.md no ambiente (uv, Manim, CRF).
3. **Escopo: o vídeo inteiro numa passada só.** Você para só no fim, com o preview completo e o relatório do §9. Mas trabalha **lote a lote, nesta ordem**, e cada lote só começa quando o anterior passou no QA do §8:
   1. `PE3` primeiro (E3-1 a E3-4: o cone). A E3-1 (§7.1) calibra escrita, caneta, glyph maps, papel, tamanhos **e** o primeiro 3D com rótulos presos. Compare com os alvos 12 a 15 antes de seguir.
   2. `PE5` (E5-1 a E5-3: a lata na dobradiça, o pagamento do gancho).
   3. `PE1`, `PE2`, `PE4`, `PE6`, `PH`, `PA`, `PS`, nesta ordem.
   4. `montar.py` e o QA do vídeo inteiro.
   Ordem do vídeo montado: **PH, PA, PE1, PE2, PE3, PE4, PE5, PE6, PS** (`PH` = H1 + H2; `PA` = A1; `PS` = S1 + S2).
   Lote reprovado: corrija só esse lote com o teste mais barato que pega o problema. Nunca declare pronto um lote reprovado nem o use de base. **Bloqueio real**: não simule evidência, não contorne em silêncio; entregue o parcial verificável e diga o que falta.
   Ao fechar cada lote, anote na `ficha.md` (seção Estado) o lote, o tempo de render e o resultado do QA.
4. **Não invente.** Nada de efeito que não esteja escrito aqui (brilho, pulso, partículas, sombra, transparência, câmera passeando, tracer). Na dúvida, o mais simples, e anote.
5. **Olhe os quadros.** Cada lote termina com stills 1920×1080 nativos comparados lado a lado com o quadro-alvo **v1** do mesmo instante, olhados em resolução cheia.

## 1. O que entregar

| Saída | Caminho |
|---|---|
| Preview silencioso do vídeo inteiro (≈ 28:56, 960×540, 15 fps) | `renders/v1/yt_0044_preview_v1_540p15.mp4` |
| Um mp4 por lote | `media_<LOTE>/videos/cena/540p15/<LOTE>.mp4` |
| QA (relatórios do §8) | `renders/v1/qa/` |
| Comparação com os 26 alvos (seu still 1920×1080 ao lado do alvo, no instante de `self.marca`) | `renders/v1/qa/comparacao/NN_<cena>.jpg` + `prancha_alvos.jpg` |
| Alinhamento 3D (rótulo × ponto, por lote) | `renders/v1/qa/alinhamento3d_v1.txt` |
| Tamanhos medidos (altura real das letras, por bloco) | `renders/v1/qa/tamanhos_v1.txt` |
| Atraso de cada gatilho | `renders/v1/qa/gatilhos_v1.txt` |
| `ficha.md` com a seção Estado atualizada | na unidade |

**Resolução do QA:** os stills de comparação, tamanho e alinhamento são **renderizados nativamente em 1920×1080**. Ampliar quadro de 540p não vale. Isso não autoriza master nem vídeo 1080p.

**Captura dos stills (valide antes do primeiro QA visual):** `manim -s` sozinho salva o **último** quadro da cena, não o instante de `self.marca(...)`. Antes de comparar qualquer alvo, leia como o `still.sh`/`quadros.py` da base param a cena no marcador (ex.: variável de ambiente com o nome da marca que encerra o `corpo()` ali) e prove com um teste: o still do `12_E3-1` tem de mostrar a moldura do V e **não** a coluna do E3-2. Se o mecanismo da base não fizer isso, adapte só os scripts locais da unidade. Enquanto a captura não reproduzir o estado certo, nenhum alvo conta como validado.

## 2. Criar a unidade

```
videos_longos/yt_0044_exercicios_integral_tripla/
  ficha.md                  (§2.1)
  referencia/               ← copie: yt_0044_narracao_v1.md, este handoff, a proposta, yt_0044_quadros_alvo_v1/, verificacao/
  kit.py  v41.py            ← copie da unidade-base SEM mudar nada (biblioteca da série)
  k44.py                    ← copie o k4N.py da base e adapte (§3.2)
  cena.py  render.sh  render3d.sh  seco.sh  still.sh  montar.py  quadros.py  gerar_ancoras.py  qa44.py
  sec_h.py sec_a.py sec_e1.py sec_e2.py sec_e3.py sec_e4.py sec_e5.py sec_e6.py sec_s.py
  threejs/  r3d.js  package.json  cena3d/c44.js + uma página .html por cena (§4)
```

**Unidade-base:** `videos_longos/yt_0043_centro_massa_momento_inercia/` **se** a `ficha.md` dela registrar o preview v2 com todos os lotes aprovados no QA (é a irmã imediata: mesma lata, mesmos `OL`/`OC`, mesmo ⊕, mesma escrita). Se não, `videos_longos/yt_0042_coordenadas_cilindricas/` com o preview aprovado registrado; se nenhuma das duas, `videos_longos/yt_0041_coordenadas_esfericas/` no estado atual. A existência de um mp4 **não** prova aprovação: vale o registro do QA na `ficha.md` e os arquivos presentes. Diga no relatório qual base usou e a evidência. A base é só leitura. Consulte só a `ficha.md` e os arquivos que vai reutilizar; não audite os vídeos anteriores. Registre a base, a evidência e as funcionalidades reutilizadas. Copie os arquivos listados; **não** copie `renders/`, `media_*`, `log_*`, `threejs/q3d/`, `threejs/pedidos3d/`.

Troque `yt_004N`/`4N` por `yt_0044`/`44` de forma **direcionada** (nunca substituição global: números de duração, resolução, índice, cor ou parâmetro não mudam) nos nomes de arquivo, nos cabeçalhos, em `gerar_ancoras.py` (lê `referencia/yt_0044_narracao_v1.md`) e em `montar.py` (`ORDEM = ["PH","PA","PE1","PE2","PE3","PE4","PE5","PE6","PS"]`). Confira que os dois caminhos abaixo existem antes de rodar. Os `.sh` usam o Python `K:/PycharmProjects/manim-fisica/.venv/Scripts/python.exe` e o Node com `NODE_PATH=K:/PycharmProjects/manim-fisica/videos_longos/yt_0020_cinematica_angular/threejs/node_modules`; não crie ambiente, não rode `uv sync`, `pip install` nem `npm install`.

### 2.1 ficha.md

```
formato: longo_horizontal
tipo: exercicios
serie_publica: CÁLCULO III · EP. 19
titulo: Exercícios do módulo: integral tripla
disciplina: Cálculo III
modulo: 3.5 Integral tripla
bloco: 3.5-E1
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, cap. 5 (exercícios 5.4-3, 5.4-4, 5.7-4/6 como base); didática do Stewart. Livro só na descrição do YouTube
unidades: x, y, z, s, r, R, h, L, d em metros; θ, φ, α em radianos; massa em kg; I em kg·m²
notacao: ρ = densidade; k = densidade constante; s = distância ao eixo; r = distância até a origem; φ e α só nas esféricas; R, h, L fixos; d = distância entre eixos; (x̄, ȳ, z̄) centro de massa; M_yz, M_xy momentos em relação aos planos; I_z, I_cm momentos de inércia; u, w substituições; n = divisões por aresta; Δ = maior lado
solido_3d: nenhum do arsenal Blender (tudo feito direto em Three.js)
3d_threejs: lataParede, cubo, cuboCaixas, cuboSonda, cuboDiag, cuboFolha, tetraSonda, tetraCent, tetraPlano, cone, coneCm, coneCasca, semi, semiFatia, lataDobradica, lataDob3, helice (geometria em referencia/yt_0044_quadros_alvo_v1/c3d44.html, cenas em cenas44.js)
duracao_alvo: ≈ 28:56 (narração v1: 5.168 palavras)
```

## 3. Base de código: o que já existe e como usar

### 3.1 Camadas

- `kit.py`: `Base(Scene)` com `setup_base/corpo/fim`, relógio de âncoras (`self.an("E3-1")`; `self.gat("frase")` espera a frase de gatilho), canto do título (`TITULO = "CÁLCULO III · INTEGRAL TRIPLA"`), logo, papel, caneta `_Caneta`, `Palco3D`. **Não edite.**
- `v41.py`: paleta, `papel`, `parte`, `junta`, `pena`. **Não edite.**
- `k4N.py` → **`k44.py`**: a camada da unidade (§3.2). As funções são as da base (`L`, `sel`, `gl`, `parte` + `self.pena`, `self.voos`, `self.gm(...)`, `self.degrau("C3.4", "…")`, `mixl`, `chip`, `selo`, `moldura`, painel opaco, `self.rot3`, `self.palco`, `self.col`, `self.sobe_sai`, `self.marca("12_E3-1")`, `self.sai_fim()`).
- Estilo de cena: o `sec_b4.py` do yt_0043 (lata pequena + coluna em 780). Uma classe por lote (`class PE3(B44)`), `ANTES = "…"`, `corpo()` que segue a fala com `self.gat(...)` frase a frase.

### 3.2 O que muda em k44.py

1. **Macros do preâmbulo** = as do topo de `referencia/yt_0044_quadros_alvo_v1/sb44.html` (procure `const M=`) **mais** as que o `keys44.js` acrescenta na primeira linha: `\dd` (d lilás `#B9A6FF`), `\al` (α violeta `#B48CFF`), `\Icm` (I_cm), `\Dz` (Δz azul). As demais (`\X \Y \Z \S \T \R \F \de \Js \Jr \dS \dT \dZ \dR \dF \dX \dY \uu \du \ww \dw \xb \yb \zb \dm \Myz \Mxy \sen \Me …`) são as do yt_0043.
2. **Câmeras e pontos 3D** = os do `c3d44.html` (§4). `cam_alvo(k)` devolve o enquadramento do alvo `k` (chaves do sb44: `h1 h2 e11 e12 e13 e14 e15 e21 e22 e23 e24 e31 e32 e33 e34 e41 e42 e43 e51 e52 e53 e61 e62 e63 s1 s2`). Deslocamentos de tela (`keys44.js`/`sb44.html`):
   - `OL = {dx:-100, dy:80, esc:.94}`: 3D grande à esquerda, coluna em **1020** (H1, E1-1, E1-5, S2);
   - `OC = {dx:-120, dy:150, esc:.72}`: 3D pequeno, coluna em **780** (E1-3, E1-4, E2-2, E5-2);
   - `OT = {dx:-70, dy:130, esc:.84}`: tetraedro grande, coluna em **1020** (E2-1, E2-3);
   - `OM = {dx:-110, dy:175, esc:.74}`: cone e meia bola, coluna em **860** (E3-1 a E3-3, E4-1, E4-2).
3. `TITULO` continua `"CÁLCULO III · INTEGRAL TRIPLA"`.
4. Nada mais muda. Vontade de "melhorar" o kit: anote no relatório.

## 4. 3D: Three.js

1. **Passada seca:** `./render3d.sh PE3` grava `threejs/pedidos3d/PE3.json`.
2. **Render 3D:** `node threejs/r3d.js --lote PE3` → `threejs/q3d/PE3_960x540/<cena>/fNNNNN.png` (fundo transparente) + `pontos.json`.
3. **Render Manim:** o `Palco3D` cola os PNGs; rótulos por `self.rot3`. Alinhamento **≤ 2 px**, medido na mesma escala (normalize 540p × 1080p antes de calcular o erro).

**Portar as cenas:** a geometria está em `referencia/yt_0044_quadros_alvo_v1/c3d44.html` (Three.js r128, `?k=cone`; o código das cenas está em `cenas44.js`, os helpers e o piso no próprio `c3d44.html`; os pontos projetados de cada cena em `r3d_pts.json`). Use o `c4N.js` da base como modelo de **estrutura** (`setEstado`, `piso()`) e crie `c44.js` **com os mesmos parâmetros, câmeras e cores**. Estados animáveis (os únicos permitidos):

| Cena (chave) | Usada em | Estados (0→1) |
|---|---|---|
| `lataParede` | H1 | `eixo` (eixo central tracejado azul), `parede` (reta ALERTA em x = R, y = 0), `seta` (seta curva de giro em volta da reta) |
| `cubo` → `cuboCaixas` | E1-1, E1-2 (fundo da etapa 1) | `cubo` (degradê de densidade), `grade` (divisão 2 × 2 × 2 nas faces), `caixas` (troca para as 8 caixinhas afastadas, cada uma com o ρ do ponto médio no topo: placas 5/4, 7/4, 9/4…) |
| `cuboSonda` | E1-3 | `sonda` (cresce de z = 0, azul-claro, a z = 1, coral) |
| `cuboDiag` | E1-4 | `diag` (diagonal tracejada GEO), `centro` (anel GEO em (½,½,½)), `cm` (⊕ em (5/9,5/9,5/9)) |
| `cuboFolha` | E1-5 | `folha` (tampa z = 1 lima), `caixas` (camada de altura Δz, placa `Δz`) |
| `tetraSonda` | E2-1, E2-2 | `sombra` (triângulo pêssego no chão), `sonda` (de z = 0 ao plano) |
| `tetraCent` | E2-3 | `vertices` (4 bolinhas), `centroide` (anel GEO em (¼,¼,¼) + tracejados aos vértices) |
| `tetraPlano` | E2-4 etapa 1 | `plano` (corte z = 1/5 menta + tracejado GEO em z = 1/4, placas) |
| `cone` / `coneCm` / `coneCasca` | E3-1 / E3-2 / E3-3 | `sonda`; `cm` (⊕ em z = 3h/4 + tracejado em h/2); `casca` (casca pêssego de raio s, fio s, seta de giro) |
| `semi` / `semiFatia` | E4-1 / E4-2 | `P` (ponto + r + φ + z), `cm` (⊕ em 3R/8); `fatia` (disco lima em z, raio √(R² − z²)) |
| `lataDobradica` → `lataDob3` | E5-1 etapa 1, E5-2 | `eixo` (eixo z na parede, azul contínuo), `seta`; no E5-2: `p1` (fio R lilás do eixo ao centro), `p2` (células gêmeas `+`/`−`), `p3` (casca pêssego de raio s em volta do centro) |
| `helice` | S2 | `helice` (cresce de t = 0 a duas voltas), `conta` (bolinha), `F` (seta azul) |

Regras do 3D: cores sólidas e opacas, sem luz dinâmica, sem brilho; a câmera só se move onde a tabela diz (aqui: **nunca**; todas as câmeras são fixas); no pouso para o 2D ela está parada. **Piso quadriculado em z = 0** em toda cena (`piso()` no fim do `c3d44.html`, extensões na tabela `PISOK`). PNG transparente composto **sobre o papel**.

**Câmeras:** lata = `ver([9.2,-6.2,5.8],[0,0,.45],600,560)`, SC = 2,2 (a mesma do yt_0043); lata na dobradiça = `ver([10.2,-6.2,5.8],[1,0,.45])`; cubos = `ver([9.2,-6.2,5.8],[.5,.5,.45])`; tetraedro = `ver([8.2,7.4,5.6],[.34,.34,.28])` (aberto pela face inclinada); cone e meia bola como no `cenas44.js`. Troca de cena dentro de um bloco (cubo → cuboCaixas; lataDobradica → lataDob3) = corte limpo no gatilho, mesmo lugar na tela.

**Escala no Manim:** quadro 16 × 9 ⇒ **1 unidade = 120 px** em 1080p (`x_m = (x_px − 960)/120`, `y_m = (540 − y_px)/120`). As funções do kit recebem px.

## 5. Sistema visual

- **Fundo:** violeta `#18143A → #0F0C26` com **papel** (quadradinhos de 60 px) de borda a borda em toda tela, também sob o 3D. Só o CTA final fica liso. Painel 2D = painel opaco `#16123A` com grade própria de 30 px.
- **Canto:** `CÁLCULO III · INTEGRAL TRIPLA` (pequeno, apagado) + título da cena em branco (maiúsculas, Space Grotesk; o título de cada alvo está no `keys44.js`, chamada `canto(...)`). Logo no canto superior direito. **Nada do 3D sobe no canto** (y < 110 entre x = 0 e 720): nos alvos 08 e 10 a ponta do eixo z do tetraedro encosta no título; na implementação, encurte o eixo z dessa cena (ponta em z = 1,25) ou desça o `OT` até o eixo ficar abaixo de y = 110.
- **Tamanhos (1080p):** fórmula principal 50–54 px, secundária 42–46 (linhas longas de conta 36–40, como no alvo), legenda 30 (mínimo 26), chips 28–30. **No máximo 7 linhas por etapa** (depois renova: o resultado vira chip no topo). Margem de 48 px.
- **Cores:** s pêssego `#FFC08A`; θ `#2EE6A6`; z azul `#5AA2FF`; x âmbar `#FFC24D`; y magenta `#EA63FF`; r laranja `#FF9440`; φ e α violeta `#B48CFF`; ρ ciano `#35D9FF`; **fator do volume em lima `#C6F26B`** (o s das cilíndricas e o r² sen φ das esféricas); u, w `#E08A3C`; d lilás `#B9A6FF`; ALERTA `#FF5D5D`; GEO `#B8C4DA`; menta `#8CFFD2`; entrada `#7FB2FF`; saída `#FF7A8A`; hélice `#FFB36B`; **⊕ do centro de massa com degradê ciano → magenta**. Operadores em branco.
- **Escrita:** termo novo = **caneta finíssima glifo a glifo, esquerda → direita**; termo que vem do desenho = **voo**; manipulação = **glyph map** (MathTex de string única nos dois lados). **Proibido:** `FadeIn` de linha pronta e destino na tela antes da hora (`FLASH POR QUADRO` = **0**).
- **Sem efeitos.** Destaque = sublinhado fino ou contorno que acende e apaga.
- **Conta inteira:** a tela mostra **todos** os degraus do §6.
- **✓ e ✗:** ✓ menta no fim de cada conferência; ✗ ALERTA só no erro clássico (E6-3) e nos cinco erros (S1).

### 5.1 Sistema 3D da série (G1–G6)

- **G1 · Papel sob o 3D.**
- **G2 · Piso** quadriculado em z = 0.
- **G3 · Metade esquerda.** Nada do 3D passa de **x = 975 px** (`OL`/`OT`), **720** (`OC`) ou **820** (`OM`), nem sai de x < 60 nem sobe no canto.
- **G4 · Sem hastes; legenda colorida** na linha y = 1020 (quadradinho na cor + texto 30 px), itens em x = 120 / 440 / 720 (ou 120 / 560 com dois itens longos). Letras de variável no desenho em placa pequena, **fora das arestas**. No máximo 2 hastes por quadro, ≤ 90 px. Rótulos x, y, z a ≤ 30 px da ponta da seta.
- **G5 · Geometria opaca e limpa.** No máximo 8 verticais e 4 anéis em traço.
- **G6 · Tudo numa linha do papel.** Regra geral: coluna e linhas de base em múltiplos de 60 (ou 20 dentro dos painéis). **Exceção:** as posições dos alvos aprovados (`keys44.js` e §7) prevalecem, mesmo fora da grade: colunas em 700, 720, 760, 860, 920, 1010, 1060. Não mova um alvo só para cair num múltiplo de 60. Espaço entre o 3D e a coluna ≥ 60 px.

## 6. Contas (o que a tela escreve, linha a linha)

As contas completas, com ID de degrau, estão na proposta (§3, **C1–C6**), conferidas no sympy (`referencia/verificacao/`, **94/94**; inclui conferências numéricas). Use os IDs em `self.degrau(...)`. O LaTeX pronto, com as macros, está no `keys44.js` (uma chave por alvo): **copie de lá, não redigite.** Linhas que aparecem só em etapas sem alvo (ex.: o volume do tetraedro dentro do E2-3, a etapa 1 do E5-1) seguem a Coluna da narração e o texto da proposta.

Exemplo, a conta **C3.2–C3.4** do E3-1 (a primeira que você implementa):

| degrau | linha na tela (LaTeX com as macros) |
|---|---|
| C3.2 | `\int_{h\S/R}^{h}\S\,\dZ=\S\Big[\Z\Big]_{h\S/R}^{h}=\S\Big(h-\dfrac{h\S}{R}\Big)=h\S-\dfrac hR\S^2` |
| C3.3 | `\int_0^R\Big(h\S-\dfrac hR\S^2\Big)\dS=\Big[\dfrac{h\S^2}{2}-\dfrac hR\dfrac{\S^3}{3}\Big]_0^R=\dfrac{hR^2}{2}-\dfrac{hR^2}{3}=\dfrac{hR^2}{6}` |
| C3.4 | `V=2\pi\cdot\dfrac{hR^2}{6}=\dfrac{\pi R^2h}{3}` em moldura menta (50 px) |

**Glyph maps previstos** (monte cada um só depois de estabilizar o LaTeX dos dois lados; `show_indices` só no desenvolvimento):

| GM | Âncora | De → para |
|---|---|---|
| GM1 | E1-1 | `4·¼ + 4·¾` → `1 + 3` → `4` |
| GM2 | E1-2 | `CIMA − BAIXO` → `3/n` (os dois 3/2 acendem e saem) |
| GM3 | E1-3 | `[xz + yz + z²/2]₀¹` → `x + y + ½` |
| GM4 | E1-3 | `x + ½ + ½` → `x + 1` |
| GM5 | E1-4 | `∭ x(x + y + z) dV` → `∭x² dV + ∭xy dV + ∭xz dV` |
| GM6 | E1-4 | `(5/6)/(3/2)` → `5/6 · 2/3` → `10/18` → `5/9` |
| GM7 | E2-2 | `(x + y)(1 − x − y) dy` → `w(1 − w) dw` (os dois `x + y` acendem em `#E08A3C` e viram w; os limites trocam para x e 1) |
| GM8 | E2-2 | `1/6 − 1/6 + 1/12` → `1/12` (os dois 1/6 acendem e saem) |
| GM9 | E2-4 | `∫₀¹∫ₓ¹ … dw dx` → `∫₀¹ …(∫₀ʷ dx) dw` (troca de ordem: os limites trocam de lugar) |
| GM10 | E2-4 | `w²(1 − w)²` → `w² − 2w³ + w⁴` |
| GM11 | E3-1 | `s(h − hs/R)` → `hs − (h/R)s²` |
| GM12 | E3-3 | `s² · s` → `s³` (chave lima) |
| GM13 | E3-3 | `(πkR⁴h/10)/(πkR²h/3)` → `(3/10)MR²` (π, k, h acendem e saem) |
| GM14 | E3-4 | `∫₀^α sen φ/cos³φ dφ` → `∫₁^{cos α} −u⁻³ du` (sen φ dφ vira −du; os limites φ viram u) |
| GM15 | E3-4 | `1/cos²α − 1` → `tg²α` → `R²/h²` |
| GM16 | E4-1 | `(πkR⁴/4)/((2/3)πkR³)` → `(1/4)/(2/3) R` → `3R/8` |
| GM17 | E5-1 | `(R + s cos θ)² + (s sen θ)²` → `R² + 2Rs cos θ + s² cos²θ + s² sen²θ` → `R² + 2Rs cos θ + s²` (cos² + sen² = 1 acende em menta) |
| GM18 | E5-2 | o integrando `R² + 2Rs cos θ + s²` se divide nos três pedaços ① ② ③ (cada termo voa para a sua linha) |
| GM19 | E5-3 | `cos⁴θ` → `((1 + cos 2θ)/2)²` → `3/8 + ½cos 2θ + ⅛cos 4θ` |
| GM20 | E6-1 | `(x − d)² + y²` → `(x² + y²) − 2dx + d²`; depois `−2d · Mx̄` → `0` quando x̄ = 0 |
| GM21 | E6-3 | `I_A + M(2R)²` riscado em ALERTA (✗) → `I_A − MR²` e `+ MR²` (✓ menta) |

## 7. Cena a cena

**Fonte da verdade, nesta ordem:** (1) a narração (âncoras, Tela, Coluna, **Gatilhos**, fala); (2) os quadros-alvo (posição e tamanho; as coordenadas exatas estão no `keys44.js`, chave indicada); (3) este §7. O alvo mostra o **estado final** de uma etapa; o caminho até ele segue os gatilhos. Cada gatilho = uma frase; não há ação sem gatilho nem gatilho sem ação.

| Âncora | Lote | Alvo (arquivo · chave) | Notas |
|---|---|---|---|
| H1 | PH | 01 · `h1` | `lataParede` (OL); cartões ① e ② opacos aparecem com a primeira linha deles; `MAIS CARO. QUANTO MAIS?` em ciano. **Não** escrever (3/2)MR² aqui. |
| H2 | PH | 02 · `h2` | 2D: quatro cartões em fila, cada um no seu gatilho; faixa das três fórmulas embaixo. |
| A1 | PA | — | 2D, papel: logo, título `EXERCÍCIOS DO MÓDULO: INTEGRAL TRIPLA`, linha `CUBO · TETRAEDRO · CONE · MEIA BOLA · A LATA NA DOBRADIÇA`. |
| E1-1 | PE1 | 03 · `e11` | `cubo` (degradê) → `grade` → troca para `cuboCaixas` (8 caixinhas com o ρ do ponto médio, placas no topo); coluna em 1020; Σ ρ ΔV em moldura menta. |
| E1-2 | PE1 | 04 · `e12` | 2D: painel `VISTA DE FRENTE DE UMA CAMADA` com os três jeitos de escolher o ponto; régua 0..3 com os pares baixo/cima se fechando em 3/2; coluna direita em 1010 (BAIXO, CIMA, tabela n = 2, 4, 10, desigualdade, CIMA − BAIXO com **GM2**). |
| E1-3 | PE1 | 05 · `e13` | `cuboSonda` (OC), coluna 780; C1.9–C1.11 com **GM3**, **GM4**; selo ✓ `CONFERE COM A SOMA DE RIEMANN`. |
| E1-4 | PE1 | 06 · `e14` | `cuboDiag` (OC); C1.12–C1.15 com **GM5**, **GM6**; ⊕ entra no `cm` com a moldura do x̄. |
| E1-5 | PE1 | 07 · `e15` | `cuboFolha` (OL); `folha` → `caixas`; integral = 0 em moldura; selo ALERTA `ρ > 0 E INTEGRAL ZERO?`, resposta em menta. |
| E2-1 | PE2 | 08 · `e21` | `tetraSonda` (OT); painel `A SOMBRA` com a tira de 0 a 1 − x; coluna em 1020. |
| E2-2 | PE2 | 09 · `e22` | `tetraSonda` (OC); coluna 780; C2.2–C2.6 com **GM7**, **GM8**; 1/12 em moldura. |
| E2-3 | PE2 | 10 · `e23` | `tetraCent` (OT); chip M = 1/12; centroide, ρ(centroide), V; ✓ em moldura; regra linear; selo ALERTA ρ = x². |
| E2-4 | PE2 | 11 · `e24` | etapa 1 (sem alvo): `tetraPlano` (OC) com o corte z = 1/5 e o tracejado 1/4, C2.11–C2.12; etapa 2 (= 11): o tetra sai, painel `O TRIÂNGULO EM (x, w)` à esquerda, C2.13–C2.16 com **GM9**, **GM10**; z̄ = 1/5 em moldura. |
| E3-1 | PE3 | 12 · `e31` | Detalhe no §7.1. |
| E3-2 | PE3 | 13 · `e32` | `coneCm` (OM); chip V; C3.5–C3.8; ⊕ em 3h/4 + tracejado h/2; legenda `DO VÉRTICE: 3h/4 · DA TAMPA: h/4` (o z̄ é medido **do vértice**; não troque o referencial). |
| E3-3 | PE3 | 14 · `e33` | `coneCasca` (OM); chip z̄; C3.9–C3.12 com **GM12**, **GM13**; legenda `CILINDRO 1/2 · CONE 3/10`. |
| E3-4 | PE3 | 15 · `e34` | 2D: painel `CORTE PELO EIXO` (α, φ, r = h/cos φ); coluna 700: C3.14–C3.18 com **GM14**, **GM15**; ✓ `O MESMO hR²/6`. |
| E4-1 | PE4 | 16 · `e41` | `semi` (OM); C4.1–C4.5 com **GM16**; chip `[−cos φ] = 1`. |
| E4-2 | PE4 | 17 · `e42` | `semiFatia` (OM); fatias C4.6–C4.8; três ✓. |
| E4-3 | PE4 | 18 · `e43` | 2D: dois cortes (UNIFORME e ρ = k r em degradê radial) com ⊕ em 0,375R e 0,4R; régua z̄/R com 3/8, 2/5, 1/2; coluna 1060: C4.9–C4.11; chip menta `TUDO NA CASCA ⇒ R/2`. |
| E5-1 | PE5 | 19 · `e51` | etapa 1 (sem alvo): `lataDobradica` (OL) com o eixo z na parede e a seta; etapa 2 (= 19): a lata sai, painel `DE CIMA` à esquerda (centro C = (R, 0), fio s, ângulo θ, fio √(x² + y²) da origem); coluna 1010: C5.1–C5.2 com **GM17**. |
| E5-2 | PE5 | 20 · `e52` | `lataDob3` (OC); a integral com **GM18** e os pedaços ① ② ③, cada um acendendo o seu estado no 3D (`p1`, `p2`, `p3`); a parcela ② que zera aparece escrita e cancelada (nunca omitida); moldura (3/2)MR². |
| E5-3 | PE5 | 21 · `e53` | 2D: painel `DE CIMA` (três raios da origem até a borda, s = 2R cos θ, arco −π/2..π/2); coluna 760: C5.7–C5.12 com **GM19**; ✓ em moldura. |
| E6-1 | PE6 | 22 · `e61` | 2D: corpo qualquer, ⊕, eixo novo em (d, 0), célula dm; coluna 920: C6.1–C6.2 com **GM20**; chip menta `O EIXO MAIS BARATO PASSA PELO CENTRO DE MASSA`. O eixo novo é **paralelo** ao eixo pelo CM (nada de eixo inclinado). |
| E6-2 | PE6 | 23 · `e62` | 2D: o cubo visto de cima, d = L/√2; coluna 720: C6.3–C6.7. |
| E6-3 | PE6 | 24 · `e63` | 2D: dois cartões (bola tangente; parede → parede oposta da lata); coluna 700: C6.8, ✗ com **GM21**, os dois ✓; legenda menta. |
| S1 | PS | 25 · `s1` | 2D: quatro cartões da receita, cada exemplo **voa** da sua fonte (guarde as fontes no lote; se não estiverem na cena, reescreva com caneta e anote); `OS CINCO ERROS` com ✗ ALERTA. Textos do alvo (são a versão curta da narração). |
| S2 | PS | 26 · `s2` | `helice` (OL): a hélice cresce, a conta e a força entram; cartão `NO PRÓXIMO VÍDEO · INTEGRAIS DE LINHA` (≥ 8 s); depois o CTA liso do kit. **Não** escrever o desafio do cone na tela. |

### 7.1 E3-1 em detalhe (o primeiro lote: calibra o resto)

`cone` parado à esquerda (`OM`), papel de borda a borda. Posições do alvo 12 (`keys44.js`, chave `e31`), px de 1080p:

| Elemento | Posição | Tamanho | Entra em |
|---|---|---|---|
| `CONE: (h/R)s ≤ z ≤ h, ρ = k` (o cone 3D entra junto) | (860, 180) | 40 | 1º gatilho do E3-1 |
| `SOMBRA: 0 ≤ s ≤ R, 0 ≤ θ ≤ 2π` + chip lima `dV = s ds dθ dz` (o s voa para a integral) | (860, 280) · chip (1460, 280) | 40 · 28 | gatilho da sombra |
| sonda (`sonda`) + legendas `ENTRA NA PAREDE` / `SAI NA TAMPA` | 3D · legendas (120, 1020) e (560, 1020) | 30 | gatilho de entra/sai |
| C3.1 (fim) `V = ∫∫∫ s dz ds dθ` com os limites da sonda | (860, 390) | 44 | gatilho da montagem |
| C3.2 com **GM11** | (860, 510) | 40 | "a de dentro" |
| C3.3 | (860, 640) | 38 | integral em s |
| C3.4 em moldura menta + legenda `UM TERÇO DO CILINDRO` | (870, 780) · (1420, 790) | 50 · 28 | resultado |

Meça o tamanho real das letras nos stills (KaTeX e MathTex diferem) e ajuste até a fórmula principal ter 50–54 px de corpo e nada < 26 px. Nenhum silêncio: se a escrita acabar antes da frase seguinte, a tela espera parada.

### 7.2 Lições que valem desde o primeiro render

1. **Rótulo sai junto com o seu objeto** (legenda, seta, chip, moldura saem no mesmo `FadeOut` da fórmula ou do desenho).
2. **A coluna de um bloco sai antes da do próximo.** Nunca duas colunas ao mesmo tempo.
3. **O painel aparece com a primeira linha dele** (painel ou cartão vazio esperando é proibido).
4. **3D inteiro dentro da sua faixa** (G3), nunca sob painel ou texto, nunca no canto.
5. **Tamanho real medido**, não o pedido.
6. **Voo não cruza linha já escrita** (arco por fora; R5V = 0).
7. **Gatilho ≤ 0,3 s** da frase, sem comprimir a caneta; se não couber, liste no relatório.
8. **CTA só depois** do cartão do próximo vídeo (S2).
9. **Câmera e escala fixas** dentro de cada bloco; troca de cena 3D = corte limpo no gatilho, sem as duas ao mesmo tempo.
10. **Placas fora das arestas** e sem órfãos nas emendas do 3D (o que deixou o yt_0043 v1 reprovado).

## 8. QA (rode `qa44.py`, adaptado do `qa4N.py` da base) e critérios de aceite

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
| 8 | Glyph maps | `[gm]`: GM1–GM21, cada um no seu lote | 100 % |
| 9 | Degraus | `[degrau]`: todos os degraus C1–C6 (menos C6.13) com tempo | 100 % |
| 10 | Texto em MathTex | fórmula como `Text` ou texto corrido dentro de MathTex | 0 |
| 11 | Tamanho **real** das letras | altura medida nos stills 1080p, `qa/tamanhos_v1.txt` | principal 50–54 px, nada < 26 px |
| 12 | Alinhamento 3D | rótulo × ponto do `pontos.json` | ≤ 2 px |
| 13 | Comparação com o alvo **v1** | still do instante `self.marca(...)` ao lado do alvo, em resolução cheia | ±20 px, mesmas cores, mesmo conteúdo |
| 14 | Duração | lote × soma das âncoras | ±0,5 s por âncora |
| 15 | Efeitos | busca por `Flash`, `Indicate`, `Wiggle`, `glow`, `opacity` < 1 em formas, `always_redraw` decorativo | 0 |
| 16 | Linha órfã | varredura a cada 0,5 s | 0 |
| 17 | 3D cortado, escondido ou no canto | pixels do 3D fora da faixa G3, sob painel/texto ou em y < 110 | 0 |
| 18 | G1–G6 por cena 3D | tabela OK/NÃO + prancha 2×3 por cena 3D | tudo OK |
| 19 | Atraso de gatilho | início de cada degrau × instante da frase, `qa/gatilhos_v1.txt` | ≤ 0,3 s; não acelere a caneta |
| 20 | Linhas por etapa e CTA | ≤ 7 linhas na coluna; CTA só depois do cartão do próximo vídeo (≥ 8 s), tela lisa | 0 excessos; R5 = 0 no S2 |

Item que não se aplica ao lote = **N/A**, nunca "OK". **Render concluído não é lote aprovado:** um lote sem Traceback ainda reprova por leitura, sincronia ou composição. Uma verificação só conta se foi executada e deixou evidência; não atribua ao `qa44.py` o que ele não mede (diga no relatório o que é automático e o que foi olhado). Rode primeiro o mais barato (`./seco.sh LOTE`) e só depois o render; refaça **só** o lote afetado.

### 8.1 Três tipos de evidência (não misture)

1. **Automático** (`qa44.py`, `seco.sh`): itens 1–10, 14–16, 19, 20.
2. **Medido** (números em arquivo): 11, 12, 17, 19.
3. **Inspeção visual** (você olhando em resolução cheia): 13, 18. Para cada um dos 26 alvos: still nativo 1920×1080 no instante de `self.marca(...)`, ao lado do alvo, e uma linha no relatório com o que difere. A prancha consolidada complementa; não substitui os stills.

Olhe também **instantes intermediários**: entrada e saída de objetos, caneta em movimento, glyph maps, voos, trocas de cena 3D (E1-1, E2-4, E5-1), troca de coluna, renovação de etapa.

### 8.2 Sincronização

Para cada gatilho, `gatilhos_v1.txt` traz: âncora, frase, instante previsto, início da animação, desvio. Duração das âncoras **preservada**: se a escrita acabar antes, a tela espera parada; se não couber, **não acelere a caneta** e **não tire degrau**: registre âncora e segundos que faltam. Duração atingida acelerando a escrita não é aprovação.

### 8.3 Montagem

Depois do `montar.py`: ordem PH → PS, nenhum lote repetido ou ausente, nenhum quadro preto inesperado, nenhuma coluna ou rótulo antigo na emenda, salto de câmera ou papel nas emendas, duração total (≈ 28:56) e arquivo íntegro (abre e toca até o fim).

### 8.4 A verificação da matemática não valida a implementação

Os 94/94 do sympy conferem a **proposta**. O que prova a implementação são os itens 8 e 9 e a comparação visual: confira que cada linha na tela é a da proposta, caractere a caractere.

## 9. Relatório obrigatório (no fim, uma vez)

0. Estado inicial (`git status`), o que existia em `yt_0044_*` e a unidade-base usada com a evidência.
1. Arquivos criados e alterados.
2. Comandos rodados e resultado (tempo de render por lote).
3. Tabela do §8 com o número medido de cada item, **por lote**.
4. Caminhos do vídeo, dos quadros de comparação e da pasta de QA.
5. Quantos dos 26 alvos você inspecionou de fato; o que ficou diferente e por quê; o que não conseguiu; o que **não** verificou.
6. Cenas Three.js: o que foi portado, resolução, custo por quadro, alinhamento medido (px).
7. Lotes concluídos e, se houver, bloqueados. Pare. Não comece voz, SRT, 1080p nem entrega.

## 10. O que não fazer

- Não alterar `template/`, `assets/`, `docs/`, `AGENTS.md`, `pyproject.toml`, `uv.lock` nem unidades de outros vídeos (a unidade-base é só leitura).
- Não usar restaurações globais (`git restore .`, `git reset --hard`, `git clean -fdx`).
- Não instalar nada, não recriar `.venv`, não rodar `npm install`.
- Não usar Blender, `ponte.py` nem `Solido3D`; não fazer 3D dentro do Manim.
- Não mudar matemática, notação, cores, texto da tela ou a narração. Se achar erro, **reporte** antes.
- Não citar livro na tela. Não citar vídeo não publicado ("como vimos no EP. 18" é proibido; "nas cilíndricas", "a gente já sabe" são permitidos).
- Não fazer voz, SRT, 1080p, master, entrega, commit, branch, push.

## 11. Condição de parada

Pronto quando: a unidade nova existe sem ter sobrescrito trabalho anterior; todos os lotes passaram no §8; os 26 alvos v1 foram comparados em 1920×1080; o preview completo foi montado e as emendas conferidas; a `ficha.md` tem o Estado final; o relatório do §9 traz caminhos e números. **Depois disso, pare.**
