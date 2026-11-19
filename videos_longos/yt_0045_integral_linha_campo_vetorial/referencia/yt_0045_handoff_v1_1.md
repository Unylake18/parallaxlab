# HANDOFF v1.1 · yt_0045 · CÁLCULO III · EP. 20 · Integral de linha de um campo vetorial · PREVIEW

> Handoff para o **Claude Code** no repositório. **Substitui o v1.** A v1.1 incorpora a revisão do GPT no que muda a execução (continuidade do GM1 entre B2-1 e B2-2, calibração medida do palco 2D, o t como parâmetro na ficha, a volta integrada × a hélice do cenário), sem mudar matemática, narração, alvos, cenas ou glyph maps. Tudo o que você precisa está aqui, no `AGENTS.md` e no zip `yt0045_handoff_v1_1_completo.zip`. As regras que o yt_0041 levou quatro previews para acertar e o yt_0043/44 confirmaram (§5.1 e §7.2) valem desde o primeiro render.
> Fase aberta: **preview silencioso 960×540 / 15 fps**. Não faça voz, SRT, 1080p, master, entrega, commit, branch nem push.
> Número `yt_0045` e EP. 20 são **provisórios** até o Kaio confirmar. Duração ≈ **19:00**: é a estimativa da narração, **não** um alvo a atingir. Não acelere a escrita, não tire degrau e não estique cena para chegar num número.
> Vídeo de **teoria** que abre o módulo 3.6 (integrais de linha). Diferente dos irmãos, quase tudo é **2D** (palco com eixos e campo de setas à esquerda, coluna de conta à direita); o 3D é só a hélice na lata (H1 e B7).

---

## 0. Como trabalhar (leia primeiro)

### 0.0 Estado inicial

1. Rode `git status --short` e guarde a saída no relatório. Preserve tudo o que existe. Nada de limpeza geral do repositório.
2. **Inspecione antes de extrair.** Procure uma unidade `videos_longos/yt_0045_*`:
   - não existe: crie (§2);
   - existe e está vazia: reutilize;
   - tem trabalho desta produção: registre o estado e continue dali, sem apagar;
   - tem trabalho de origem incerta, de outro agente, ou arquivos que seriam sobrescritos: **não apague nem substitua**; relate o conflito e pare só a operação afetada.
3. Descompacte `yt0045_handoff_v1_1_completo.zip` numa pasta **fora** da unidade, confira que as referências existem e copie para `referencia/` só o que falta. Se um arquivo já existe: idêntico, mantenha; diferente com versão identificada, respeite a versão aprovada e registre; origem incerta, não sobrescreva e relate.
4. Arquivo indispensável ausente = bloqueio daquela etapa. Não recrie alvo nem trecho de narração por aproximação.

### 0.1 Fontes de verdade e precedência

1. `AGENTS.md`: ambiente, Git, regras do canal.
2. `referencia/yt_0045_narracao_v1.md`: âncoras, fala, **Tela**, **Coluna** ([ensina]/[mecânica]), **Gatilhos**: conteúdo e momento de cada ação.
3. `referencia/yt_0045_quadros_alvo_v1/` (+ `sb45.html`, `keys45.js`, `c3d45.html`): **posição, tamanho, câmera e cor**.
4. `referencia/calculo3_36t1_integral_linha_campo_vetorial_proposta_v1.md` §4: **matemática**, conta inteira C1–C9 (o porquê do C2.10, a conferência do C1.4 e as reservas do C8 e do C9 **não** vão à tela).
5. Este handoff: implementação, lotes, restrições e QA. O detalhe de um elemento (§7.1) vale sobre a regra genérica.
6. A unidade-base (§2): só para portar uma funcionalidade concreta.

**Precedência por assunto:** matemática = proposta; o que se fala, a ordem e o momento = narração; aparência, posição e câmera = alvos; procedimento e QA = este handoff; ambiente e Git = `AGENTS.md`.

Conflito objetivo de matemática: preserve a proposta e a narração, identifique os arquivos e a expressão, registre e não invente. Referência ausente: não substitua por aproximação sua.

### 0.2 Regras da passada

1. Não altere arquivos fora de `videos_longos/yt_0045_integral_linha_campo_vetorial/`.
2. Leia o `AGENTS.md` da raiz. Este handoff **não** o substitui; quando os dois parecerem divergir, siga este handoff no conteúdo e o AGENTS.md no ambiente (uv, Manim, CRF).
3. **Escopo: o vídeo inteiro numa passada só.** Você para só no fim, com o preview completo e o relatório do §9. Mas trabalha **lote a lote, nesta ordem**, e cada lote só começa quando o anterior passou no QA do §8:
   1. `PB4` primeiro (B4-1 a B4-3: o redemoinho no círculo). O B4-1 (§7.1) calibra escrita, caneta, glyph maps, papel, tamanhos **e** o palco 2D com campo de setas. Compare com os alvos 07 a 09 antes de seguir.
   2. `PB7` (B7-1 a B7-3: a hélice da lata, o pagamento do gancho do EP. 19; primeiro 3D com rótulos presos).
   3. `PB1`, `PB2`, `PB5`, `PB6`, `PH`, `PA`, `PS`, nesta ordem.
   4. `montar.py` e o QA do vídeo inteiro.
   Ordem do vídeo montado: **PH, PA, PB1, PB2, PB4, PB5, PB6, PB7, PS** (`PH` = H1 + H2; `PA` = A1; `PB1` = B1; `PB2` = B2-1 + B2-2 + B3; `PB4` = B4-1 a B4-3; `PB5` = B5-1 + B5-2; `PB6` = B6-1 + B6-2; `PB7` = B7-1 a B7-3; `PS` = S1 + S2).
   Lote reprovado: corrija só esse lote com o teste mais barato que pega o problema. Nunca declare pronto um lote reprovado nem o use de base. **Bloqueio real**: não simule evidência, não contorne em silêncio; entregue o parcial verificável e diga o que falta.
   Ao fechar cada lote, anote na `ficha.md` (seção Estado) o lote, o tempo de render e o resultado do QA.
4. **Não invente.** Nada de efeito que não esteja escrito aqui (brilho, pulso, partículas, sombra, transparência, câmera passeando, tracer, conta andando sozinha pela curva). Na dúvida, o mais simples, e anote.
5. **Olhe os quadros.** Cada lote termina com stills 1920×1080 nativos comparados lado a lado com o quadro-alvo **v1** do mesmo instante, olhados em resolução cheia.

## 1. O que entregar

| Saída | Caminho |
|---|---|
| Preview silencioso do vídeo inteiro (≈ 19:00, 960×540, 15 fps) | `renders/v1/yt_0045_preview_v1_540p15.mp4` |
| Um mp4 por lote | `media_<LOTE>/videos/cena/540p15/<LOTE>.mp4` |
| QA (relatórios do §8) | `renders/v1/qa/` |
| Comparação com os 18 alvos (seu still 1920×1080 ao lado do alvo, no instante de `self.marca`) | `renders/v1/qa/comparacao/NN_<cena>.jpg` + `prancha_alvos.jpg` |
| Alinhamento 3D (rótulo × ponto, por lote) | `renders/v1/qa/alinhamento3d_v1.txt` |
| Tamanhos medidos (altura real das letras, por bloco) | `renders/v1/qa/tamanhos_v1.txt` |
| Atraso de cada gatilho | `renders/v1/qa/gatilhos_v1.txt` |
| Calibração do palco 2D (por alvo) | `renders/v1/qa/palco2d_v1.txt` |
| `ficha.md` com a seção Estado atualizada | na unidade |

**Resolução do QA:** os stills de comparação, tamanho e alinhamento são **renderizados nativamente em 1920×1080**. Ampliar quadro de 540p não vale. Isso não autoriza master nem vídeo 1080p.

**Captura dos stills (valide antes do primeiro QA visual):** `manim -s` sozinho salva o **último** quadro da cena, não o instante de `self.marca(...)`. Antes de comparar qualquer alvo, leia como o `still.sh`/`quadros.py` da base param a cena no marcador e prove com um teste: o still do `07_B4-1` tem de mostrar a moldura do 2πR² e **não** os pedaços violeta do B4-2. Se o mecanismo da base não fizer isso, adapte só os scripts locais da unidade. Enquanto a captura não reproduzir o estado certo, nenhum alvo conta como validado.

## 2. Criar a unidade

```
videos_longos/yt_0045_integral_linha_campo_vetorial/
  ficha.md                  (§2.1)
  referencia/               ← copie: yt_0045_narracao_v1.md, este handoff, a proposta, yt_0045_quadros_alvo_v1/, verificacao/
  kit.py  v41.py            ← copie da unidade-base SEM mudar nada (biblioteca da série)
  k45.py                    ← copie o k4N.py da base e adapte (§3.2)
  cena.py  render.sh  render3d.sh  seco.sh  still.sh  montar.py  quadros.py  gerar_ancoras.py  qa45.py
  sec_h.py sec_a.py sec_b1.py sec_b2.py sec_b4.py sec_b5.py sec_b6.py sec_b7.py sec_s.py
  threejs/  r3d.js  package.json  cena3d/c45.js + uma página .html por cena (§4)
```

**Unidade-base:** `videos_longos/yt_0044_exercicios_integral_tripla/` **se** a `ficha.md` dela registrar um preview com todos os lotes aprovados no QA (é a irmã imediata: mesma lata, a mesma cena `helice` no S2, mesmos `OL`/`OC`, mesma escrita). Se não, `videos_longos/yt_0043_centro_massa_momento_inercia/` com o preview v2 aprovado registrado; se nenhuma das duas, `videos_longos/yt_0041_coordenadas_esfericas/` no estado atual. A existência de um mp4 **não** prova aprovação: vale o registro do QA na `ficha.md` e os arquivos presentes. Diga no relatório qual base usou e a evidência. A base é só leitura. Consulte só a `ficha.md` e os arquivos que vai reutilizar; não audite os vídeos anteriores. Registre a base, a evidência e as funcionalidades reutilizadas. Copie os arquivos listados; **não** copie `renders/`, `media_*`, `log_*`, `threejs/q3d/`, `threejs/pedidos3d/`.

Troque `yt_004N`/`4N` por `yt_0045`/`45` de forma **direcionada** (nunca substituição global: números de duração, resolução, índice, cor ou parâmetro não mudam) nos nomes de arquivo, nos cabeçalhos, em `gerar_ancoras.py` (lê `referencia/yt_0045_narracao_v1.md`) e em `montar.py` (`ORDEM = ["PH","PA","PB1","PB2","PB4","PB5","PB6","PB7","PS"]`). Os `sec_*.py` da base são de outro vídeo: aproveite só a estrutura (classe por lote, `ANTES`, `corpo()`), escreva as cenas novas. Confira que os dois caminhos abaixo existem antes de rodar. Os `.sh` usam o Python `K:/PycharmProjects/manim-fisica/.venv/Scripts/python.exe` e o Node com `NODE_PATH=K:/PycharmProjects/manim-fisica/videos_longos/yt_0020_cinematica_angular/threejs/node_modules`; não crie ambiente, não rode `uv sync`, `pip install` nem `npm install`.

### 2.1 ficha.md

```
formato: longo_horizontal
tipo: teoria
serie_publica: CÁLCULO III · EP. 20
titulo: Integral de linha de um campo vetorial
disciplina: Cálculo III
modulo: 3.6 Integrais de linha
bloco: 3.6-T1
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §6.1 e §6.2 (definição, outra notação, Ex. 1 e 2); didática do Stewart. Livro só na descrição do YouTube
unidades: nenhuma na tela (exemplos adimensionais). t é o PARÂMETRO da curva; na fala ele é o tempo da conta (escolha de percurso: no círculo e na hélice o ângulo cresce junto com t), e γ′ é chamada de velocidade nesse sentido. Não escrever segundos, s nem unidade de t em lugar nenhum
notacao: γ curva (laranja), γ′ velocidade (violeta), F campo com componentes P, Q, R (verde-menta), Δγᵢ e dγ deslocamentos (violeta), t parâmetro, a ≤ t ≤ b, g(t) = F(γ(t))·γ′(t), W trabalho, α ângulo entre F e o deslocamento, R raio (só nos exemplos 2D) e 3ª componente (só no cartão geral do B6-1), c subida da hélice por unidade de t (z = c t), n número de pedaços. Sem θ, sem ds
solido_3d: nenhum do arsenal Blender (tudo feito direto em Three.js)
3d_threejs: helice, heliceCampo, heliceLeitura (geometria em referencia/yt_0045_quadros_alvo_v1/c3d45.html)
duracao_alvo: ≈ 19:00 (narração v1: 3.390 palavras)
```

## 3. Base de código: o que já existe e como usar

### 3.1 Camadas

- `kit.py`: `Base(Scene)` com `setup_base/corpo/fim`, relógio de âncoras (`self.an("B4-1")`; `self.gat("frase")` espera a frase de gatilho), canto do título, logo, papel, caneta `_Caneta`, `Palco3D`. **Não edite.**
- `v41.py`: paleta, `papel`, `parte`, `junta`, `pena`. **Não edite.**
- `k4N.py` → **`k45.py`**: a camada da unidade (§3.2). As funções são as da base (`L`, `sel`, `gl`, `parte` + `self.pena`, `self.voos`, `self.gm(...)`, `self.degrau("C4.4", "…")`, `mixl`, `chip`, `selo`, `moldura`, painel opaco, `self.rot3`, `self.palco`, `self.col`, `self.sobe_sai`, `self.marca("07_B4-1")`, `self.sai_fim()`).
- Estilo de cena: telas 2D com palco de eixos à esquerda e coluna em **1020** (como os painéis 2D do yt_0043/44, ex.: `e13`/`e43` do 0044); telas 3D da hélice no modelo do `sec_b4.py` do yt_0043 (lata pequena `OC` + coluna em 780). Uma classe por lote (`class PB4(B45)`), `ANTES = "…"`, `corpo()` que segue a fala com `self.gat(...)` frase a frase.

### 3.2 O que muda em k45.py

1. **Macros do preâmbulo** = as do topo de `referencia/yt_0045_quadros_alvo_v1/sb45.html` (procure `const M=`) **mais** as que o `keys45.js` acrescenta no `Object.assign(M, …)` da primeira linha: `\g` (γ laranja `#FFB36B`), `\gp` (γ′ violeta `#B48CFF`), `\Fv` (F⃗ verde-menta `#2EE6A0`), `\dg` (dγ violeta), `\Dg` (Δγ violeta), `\DTt` (Δt `#E08A3C`), `\al` (α violeta), `\Lim{…}` (lima `#C6F26B`), `\Om` (Ω), `\uu` (u `#E08A3C`). As demais (`\X \Y \Z \Tt \dTt \dX \dY \dZ \sen \Me …`) são as do yt_0043/44. **Atenção:** `\X`, `\Y`, `\Z` já trazem a letra; nunca escreva `\X{2}`: número colorido usa `\textcolor{…}{2}`.
2. **Palco 2D (novo):** `vista(cx, cy, U)` do `head45.part`/`sb45.html` = origem dos eixos em (cx, cy) px e U px por unidade do desenho. Cada alvo diz a vista na primeira linha do seu bloco no `keys45.js` (ex.: B4 = `vista(480,560,120)`, B5-2 = `vista(480,760,240)`). Porte para `k45.py` uma função `self.palco2d(cx, cy, U)` que devolve o mapa (x, y) → ponto do Manim (`x_m = (cx + U·x − 960)/120`, `y_m = (540 − cy + U·y)/120`) e use-a para eixos, curvas, campo e rótulos. **O papel nasce dos eixos** (`papel(ax)` da série) com quadradinho de 60 px de borda a borda.
3. **Campo de setas (novo):** `self.campo(F, pontos, k, mx)` = setas verde-menta finas (3 px a 1080p, ponta 12 px), comprimento na tela `min(k·|F|, mx)` unidades do desenho, exatamente como `setaCampo`/`campo` do `keys45.js` (a grade de pontos de cada alvo está lá). O campo entra **inteiro num gatilho** (`Create` das setas juntas, `lag_ratio` ≤ 0,05, ≤ 1 s) e fica parado.
4. **Câmeras e pontos 3D** = os do `c3d45.html` (§4). Deslocamentos de tela (`head45.part`):
   - `OL = {dx:-100, dy:80, esc:.94}`: 3D grande à esquerda, coluna em **1020** (H1);
   - `OC = {dx:-120, dy:150, esc:.72}` com recorte em x = 720: 3D pequeno, coluna em **780** (B7-1, B7-2, B7-3).
5. `TITULO = "CÁLCULO III · INTEGRAIS DE LINHA"`. Se o título mora no `kit.py`, sobrescreva como atributo da classe em `k45.py`; não edite o kit.
6. Nada mais muda. Vontade de "melhorar" o kit: anote no relatório.

## 4. 3D: Three.js

1. **Passada seca:** `./render3d.sh PB7` grava `threejs/pedidos3d/PB7.json`.
2. **Render 3D:** `node threejs/r3d.js --lote PB7` → `threejs/q3d/PB7_960x540/<cena>/fNNNNN.png` (fundo transparente) + `pontos.json`.
3. **Render Manim:** o `Palco3D` cola os PNGs; rótulos por `self.rot3`. Alinhamento **≤ 2 px**, medido na mesma escala (normalize 540p × 1080p antes de calcular o erro).

**Portar as cenas:** a geometria está em `referencia/yt_0045_quadros_alvo_v1/c3d45.html` (Three.js r128, `?k=helice`; helpers `lataTraco`, `eixoZ`, `tubo`, `seta`, `piso` no próprio arquivo; os pontos projetados de cada cena em `r3d_pts.json`). Use o `c4N.js` da base como modelo de **estrutura** (`setEstado`, `piso()`; a cena `helice` do yt_0044 já existe lá e é a mesma geometria) e crie `c45.js` **com os mesmos parâmetros, câmeras e cores**. Hélice: `HX(t) = (cos t, sen t, t/(4π))` (lata de raio 1 e altura 1, duas voltas sobem 1). **Duas voltas = cenário; uma volta = conta.** No H1 a hélice inteira (0 ≤ t ≤ 4π) é o gancho; no B7 a integral é só da 1ª volta (0 ≤ t ≤ 2π, laranja cheio), que sobe 1/2, e a 2ª volta fica em traço apagado. Nunca mostre a 2ª volta em laranja cheio durante a conta, nem limites 0..4π na tela. Força: `Fh(t) = (−sen t, cos t, −1)`. Estados animáveis (os únicos permitidos):

| Cena (chave) | Usada em | Estados (0→1) |
|---|---|---|
| `helice` | H1 | `helice` (a hélice cresce de t = 0 até duas voltas, 4π), `conta` (bolinha branca em t = 1,8π), `F` (seta verde-menta `#2EE6A0` na conta, k = 0,42) |
| `heliceCampo` | B7-1, B7-2 | `helice` (a 1ª volta, 0 ≤ t ≤ 2π, cresce em laranja; a 2ª volta já está em traço apagado), `setas` (as 5 setas de F em t = 0,80π, 1,08π, 1,36π, 1,64π, 1,92π, k = 0,24, entram juntas), `t0`/`t2pi` (bolinhas brancas nos dois pontos) |
| `heliceLeitura` | B7-3 | o estado final do `heliceCampo` + `tampa` (contorno lima do disco de baixo, raio 1, em z = 0) + `subida` (régua azul `#5AA2FF` vertical entre t = 0 e t = 2π, ângulo 0, a 1,10 do eixo, de z = 0 a z = 1/2, com os dois tiquinhos) |

`heliceCampo` → `heliceLeitura` = mesma câmera e mesma lata: a troca no B7-3 é só a entrada dos dois estados novos, no gatilho, sem corte visível.

Regras do 3D: cores sólidas e opacas, sem luz dinâmica, sem brilho; a câmera **nunca** se move (todas fixas); a conta **não** anda pela hélice (o vídeo é sobre somar, não sobre animar). **Piso quadriculado em z = 0** em toda cena (`piso()` no fim do `c3d45.html`, extensões na tabela `PISOK`). PNG transparente composto **sobre o papel**.

**Câmera:** lata = `ver([9.2,-6.2,5.8],[0,0,.45],600,560)`, SC = 2,2 (a mesma do yt_0043/44).

**Escala no Manim:** quadro 16 × 9 ⇒ **1 unidade = 120 px** em 1080p (`x_m = (x_px − 960)/120`, `y_m = (540 − y_px)/120`). As funções do kit recebem px.

## 5. Sistema visual

- **Fundo:** violeta `#18143A → #0F0C26` com **papel** (quadradinhos de 60 px) de borda a borda em toda tela, também sob o 3D; nas telas 2D o papel **nasce dos eixos** do palco. Só o CTA final fica liso. Painel/cartão = opaco `#16123A` com borda GEO fina.
- **Canto:** `CÁLCULO III · INTEGRAIS DE LINHA` (pequeno, apagado) + título da cena em branco (maiúsculas, Space Grotesk; o título de cada alvo está no `keys45.js`, chamada `canto(...)`). Logo no canto superior direito. Nada do desenho sobe no canto (y < 130 entre x = 0 e 860).
- **Tamanhos (1080p):** fórmula principal 46–52 px, secundária 40–44 (linhas longas de conta 38–40, como no alvo), legenda 28–30 (mínimo 26), chips 28–32. **No máximo 7 linhas por etapa** (depois renova: o resultado vira chip no topo, como no B7-2 e no B7-3). Margem de 48 px.
- **Cores:**

  | O quê | Cor |
  |---|---|
  | campo F e setas do campo | verde-menta `#2EE6A0` |
  | γ′, Δγᵢ, dγ, α (deslocamentos e velocidade) | violeta `#B48CFF` |
  | curva γ, hélice | laranja `#FFB36B` |
  | t, Δt, dt, u | `#E08A3C` |
  | x · y · z | âmbar `#FFC24D` · magenta `#EA63FF` · azul `#5AA2FF` |
  | "ajuda", "ao longo", área (dobro da área), tampa | lima `#C6F26B` |
  | "atrapalha", ao contrário, quinas | ALERTA `#FF5D5D` |
  | "de lado", textos de apoio | GEO `#B8C4DA` |
  | moldura do resultado, ✓ | menta `#8CFFD2` |
  | pergunta do hook | ciano `#35D9FF` |

  Operadores, W, números e P, Q, R em branco.
- **Escrita:** termo novo = **caneta finíssima glifo a glifo, esquerda → direita**; termo que vem do desenho = **voo**; manipulação = **glyph map** (MathTex de string única nos dois lados). **Proibido:** `FadeIn` de linha pronta e destino na tela antes da hora (`FLASH POR QUADRO` = **0**).
- **Sem efeitos.** Destaque = sublinhado fino ou contorno que acende e apaga.
- **Conta inteira:** a tela mostra **todos** os degraus do §6.
- **✓:** menta no fim de cada conferência (B4-2, B5-2, B6-2). Nenhum ✗ neste vídeo.

### 5.1 Sistema 3D da série (G1–G6)

- **G1 · Papel sob o 3D.**
- **G2 · Piso** quadriculado em z = 0.
- **G3 · Metade esquerda.** Nada do 3D passa de **x = 975 px** (`OL`) ou **720** (`OC`), nem sai de x < 60 nem sobe no canto.
- **G4 · Sem hastes; legenda colorida** na linha y = 1020 (quadradinho na cor + texto 28–30 px), itens em x = 120 / 470 (3D) ou 120 / 560 / 720 (2D, como no alvo). Letras no desenho em placa pequena, **fora das arestas**. Rótulo z a ≤ 30 px da ponta do eixo.
- **G5 · Geometria opaca e limpa.** No máximo 12 verticais em traço na lata (as do alvo).
- **G6 · Tudo numa linha do papel.** Regra geral: coluna e linhas de base em múltiplos de 60. **Exceção:** as posições dos alvos aprovados (`keys45.js` e §7) prevalecem, mesmo fora da grade. Não mova um alvo só para cair num múltiplo de 60. Espaço entre o desenho e a coluna ≥ 60 px.

### 5.2 Palco 2D (novo neste vídeo)

- Eixo x âmbar, eixo y magenta, setas finas (3 px), rótulos `x`/`y` em itálico na cor do eixo a ≤ 30 px da ponta. Números dos eixos em GEO 26 px só onde o alvo mostra (B1, B5-1, B6-2).
- Curva em laranja 5–6 px com **uma** seta de sentido (onde o alvo mostra). Pontos = bolinhas brancas 7–9 px.
- **Rótulo nunca em cima de seta do campo:** onde o alvo pôs uma placa opaca atrás do rótulo (B4-3 `ÁREA πR²`), faça o mesmo; em outro lugar, se uma seta do campo cair sob um rótulo, apague **só aquela seta** (anote no relatório) em vez de mover o rótulo.
- O campo **não** se move. A curva é desenhada (`Create`) no seu gatilho, no sentido do percurso.

## 6. Contas (o que a tela escreve, linha a linha)

As contas completas, com ID de degrau, estão na proposta (§4, **C1–C9**), conferidas no sympy (`referencia/verificacao/`, **39/39**; inclui a soma de Riemann exata do círculo, a área da elipse por integral dupla e uma soma numérica de 20 000 pedaços na hélice). Use os IDs em `self.degrau(...)`. O LaTeX pronto, com as macros, está no `keys45.js` (uma chave por alvo): **copie de lá, não redigite.** Linhas que aparecem só em etapas sem alvo seguem a Coluna da narração e o texto da proposta.

Exemplo, a conta **C4.2–C4.5** do B4-1 (a primeira que você implementa):

| degrau | linha na tela (LaTeX com as macros) |
|---|---|
| C4.2 | `①\ \ \Fv(\g(\Tt))=(-R\sen\Tt,\ R\cos\Tt)` |
| C4.3 | `②\ \ \gp(\Tt)=(-R\sen\Tt,\ R\cos\Tt)` |
| C4.4 | `③\ \ \Fv(\g(\Tt))\cdot\gp(\Tt)=R^2\sen^2\Tt+R^2\cos^2\Tt` e, embaixo, `=R^2(\sen^2\Tt+\cos^2\Tt)=R^2` |
| C4.5 | `W=\int_0^{2\pi}R^2\,\dTt=R^2\Big[\Tt\Big]_0^{2\pi}=R^2(2\pi-0)=2\pi R^2` em moldura menta |

**Glyph maps previstos** (monte cada um só depois de estabilizar o LaTeX dos dois lados; `show_indices` só no desenvolvimento):

| GM | Âncora | De → para |
|---|---|---|
| GM1 | B2-1 → B2-2 | `\Dg_i` da linha `W ≈ Σ F(γ(tᵢ))·Δγᵢ` → `\gp(\Tt_i)\,\DTt_i` (C2.4 → C2.6: o Δγᵢ acende violeta e vira γ′(tᵢ)Δtᵢ; o resto da linha fica) |
| GM2 | B2-2 | `\Fv(\g(\Tt_i))\cdot\gp(\Tt_i)` → `g(\Tt_i)` (C2.6 → C2.8: o produto se recolhe no g) |
| GM3 | B4-1 | `R^2\sen^2\Tt+R^2\cos^2\Tt` → `R^2(\sen^2\Tt+\cos^2\Tt)` → `R^2` (o R² sai em evidência; sen² + cos² acende menta e vira 1) |
| GM4 | B4-2 | C4.6 → C4.7: os termos `−R² sen tᵢ cos tᵢ` e `+R² cos tᵢ sen tᵢ` (que aparecem ao abrir os produtos) acendem e saem juntos |
| GM5 | B4-2 | `\sen\Tt_i\cos\Tt_{i-1}-\cos\Tt_i\sen\Tt_{i-1}` → `\sen(\Tt_i-\Tt_{i-1})` → `\sen\tfrac{2\pi}{n}` |
| GM6 | B5-1 | `\Big[\tfrac{\Tt^2}{2}+\tfrac{\Tt^4}{2}\Big]_{-1}^{1}` → `\Big(\tfrac12+\tfrac12\Big)-\Big(\tfrac12+\tfrac12\Big)` (os limites descem para dentro) → `1-1=0` |
| GM7 | B5-2 | `\tfrac{\Tt^2}{2}+\tfrac{\Tt^4}{2}` → `\tfrac12(\X^2+\Y^2)` (o t vira x, o t² vira y; C5.8) |
| GM8 | B6-1 | C6.2 → C6.4: `\X'(\Tt)\,\dTt` → `\dX` e `\Y'(\Tt)\,\dTt` → `\dY` (cada par voa para o seu lugar; a coluna das duas identidades C6.3 fica ao lado) |
| GM9 | B6-2 | `2(\sen^2\Tt+\cos^2\Tt)\,\dTt` → `2\,\dTt` (o parêntese acende menta e vira 1) |
| GM10 | B7-2 | `\sen^2\Tt+\cos^2\Tt-c` → `1-c` (C8.7; o `\Me{…}` do alvo é esse destaque) |
| GM11 | B7-3 | `2\pi-2\pi c` com `2\pi c=\tfrac12` → `2\pi-\tfrac12` |

## 7. Cena a cena

**Fonte da verdade, nesta ordem:** (1) a narração (âncoras, Tela, Coluna, **Gatilhos**, fala); (2) os quadros-alvo (posição e tamanho; as coordenadas exatas estão no `keys45.js`, chave indicada); (3) este §7. O alvo mostra o **estado final** de uma etapa; o caminho até ele segue os gatilhos. Cada gatilho = uma frase; não há ação sem gatilho nem gatilho sem ação.

| Âncora | Lote | Alvo (arquivo · chave) | Notas |
|---|---|---|---|
| H1 | PH | 01 · `h1` | `helice` (OL); coluna 1020; `QUANTO TRABALHO NUMA VOLTA?` em ciano; `VOLUME? ÁREA? A CURVA NÃO TEM NENHUM DOS DOIS` em GEO. |
| H2 | PH | 02 · `h2` | 2D: curva laranja, conta, F verde que se separa em duas setas finas (lima ao longo, GEO de lado) com o paralelogramo tracejado; legendas lima/GEO; coluna 1020. |
| A1 | PA | — | 2D, papel: logo, título `INTEGRAL DE LINHA DE UM CAMPO VETORIAL`, linha `A FORÇA SOMADA AO LONGO DO CAMINHO`. |
| B1 | PB1 | 03 · `b1` | 2D `vista` do alvo; A = (1, 1), B = (4, 1), três setas F = (2, 1) ao longo do segmento, decomposição 2 (lima) e 1 (GEO) na do meio; coluna 1020: C1.1–C1.3 (C1.3 em moldura), C1.4, os três chips C1.5. |
| B2-1 | PB2 | 04 · `b21` | 2D `vista(140,890,120)`: campo, curva com γ(a) e γ(b), régua do tempo (y = 990) com t₀…t₆, cordas violeta e pontos, F(γ(t₄)) grosso no 4º ponto, Δγ₄; coluna 1020: C2.1–C2.4. |
| B2-2 | PB2 | 05 · `b22` | mesmo palco; painel `QUASE IGUAIS` (lupa) no alto do palco com a corda Δγ₄ e γ′(t₄)Δt₄ tracejada; coluna: C2.5–C2.10 com **GM1**, **GM2**; chip C2.10. **Continuidade do GM1:** a linha C2.4 `W ≈ Σ F(γ(tᵢ))·Δγᵢ` do B2-1 **não sai**; no início do B2-2 as linhas C2.1–C2.3 saem e a C2.4 sobe para (1020, 295); a C2.5 é escrita em (1020, 190); o GM1 transforma o **mesmo objeto** da C2.4 na C2.6. B2-1 e B2-2 ficam na **mesma classe** `PB2` (ou o objeto passa de uma âncora para a outra sem ser recriado). Proibido recriar a C2.4 pronta no B2-2. |
| B3 | PB2 | 06 · `b3` | 2D pequeno à esquerda (curva, F, γ′, arco do ângulo); cartão `DEFINIÇÃO` (640–1860): hipóteses, C2.11 em moldura menta, dγ = γ′(t) dt, receita ①②③, chip do sinal. |
| B4-1 | PB4 | 07 · `b41` | Detalhe no §7.1. |
| B4-2 | PB4 | 08 · `b42` | palco do B4 com círculo GEO e 8 cordas violeta; coluna: C4.6–C4.11 com **GM4**, **GM5**; ✓ menta no fim. |
| B4-3 | PB4 | 09 · `b43` | mesmo palco: o segmento da origem até (R, 0) em laranja grosso com as setas F de lado (para cima); disco lima com placa `ÁREA πR²`; coluna: C4.12–C4.14 (moldura), chip `MESMO CAMPO, OUTRO CAMINHO, OUTRO TRABALHO`, C4.15. |
| B5-1 | PB5 | 10 · `b51` | 2D: campo F = (x, y) para fora, parábola γ(t) = (t, t²) de −1 a 1 com duas setas de sentido, pontas rotuladas; coluna: C5.1–C5.5 com **GM6**; C5.5 em moldura. |
| B5-2 | PB5 | 11 · `b52` | 2D `vista(480,760,240)`: a ida (`IDA ATÉ A ORIGEM: CONTRA`, ALERTA) e a volta (`VOLTA: A FAVOR`, lima); coluna: C5.6–C5.9 com **GM7**; ✓; chip `SÓ IMPORTAM AS PONTAS: CAMPO CONSERVATIVO`. |
| B6-1 | PB6 | 12 · `b61` | 2D tela cheia sem palco: C6.1–C6.6, mini-desenho da projeção dx; cartão geral `NO ESPAÇO` com P dx + Q dy + R dz; alerta `NÃO É ∫ EM x MAIS ∫ EM y: VOLTA SEMPRE PARA O t` (texto e cor do alvo). **GM8**. |
| B6-2 | PB6 | 13 · `b62` | 2D: elipse x = 2 cos t, y = sen t com 4 setas do redemoinho e `ÁREA = 2π`; coluna: C7.1–C7.7 com **GM9**; C7.6 em moldura; ✓; chip `CÍRCULO: 2πR² = 2 × ÁREA`. |
| B7-1 | PB7 | 14 · `b71` | `heliceCampo` (OC, recorte 720); coluna 780: C8.1, chips `REDEMOINHO: AJUDA` (lima) e `PESO: ATRAPALHA` (ALERTA), C8.2, C8.3. |
| B7-2 | PB7 | 15 · `b72` | mesmo 3D; chip C8.2 no topo; C8.4–C8.9 com **GM10**; C8.9 em moldura (52 px). |
| B7-3 | PB7 | 16 · `b73` | `heliceLeitura` (`tampa`, `subida`); rótulo `2πc` azul preso ao ponto `sub`; chip W no topo; C8.10–C8.14 com **GM11**; C8.13 em moldura + `O REDEMOINHO GANHA` lima. |
| S1 | PS | 17 · `s1` | 2D: três cartões (DEFINIÇÃO · OUTRA NOTAÇÃO · O SINAL) e a faixa dos três exemplos; cada fórmula **voa** da sua fonte quando ela está na cena; se não estiver, caneta (anote). |
| S2 | PS | 18 · `s2` | 2D: círculo com γ₁, a volta ao contrário (seta ALERTA), quadrado tracejado com quinas; coluna: γ₁, γ₂ e as perguntas; cartão `NO PRÓXIMO VÍDEO · MUDANÇA DE PARÂMETRO E CAMINHOS COM QUINA` (≥ 8 s); depois o CTA liso do kit. **Não** escrever a resposta (2πR²) nem o desafio. |

### 7.1 B4-1 em detalhe (o primeiro lote: calibra o resto)

Palco 2D à esquerda, `vista(480,560,120)` (origem em (480, 560) px, 120 px por unidade, R = 2 no desenho = 240 px), papel nascendo dos eixos de borda a borda. Posições do alvo 07 (`keys45.js`, chave `b41`), px de 1080p:

| Elemento | Posição | Tamanho | Entra em |
|---|---|---|---|
| eixos x, y (−3,6..3,7 × −3,4..3,4) + campo (−y, x): anéis de raio 1, 2, 3, oito setas cada, em ângulos k·π/4 + π/8, `k = .32`, `mx = 1.0` + linha `F(x, y) = (−y, x)` + legenda verde `F = (−y, x): GIRA EM VOLTA DA ORIGEM` | palco · (1020, 190) · legenda (120, 1020) | 48 · 28 | "o redemoinho" |
| círculo de raio R (laranja 6 px, `Create` anti-horário a partir de (R, 0)), seta de sentido em t = 0,62π, raio GEO em −π/5 com `R` + linha γ(t) + legenda laranja `CÍRCULO DE RAIO R` | palco · (1020, 285) · legenda (700, 1020) | 42 · 28 | "A curva é o círculo de raio R" |
| C4.2 ① | (1020, 380) | 42 | "Passo um" |
| C4.3 ② | (1020, 470) | 42 | "Passo dois" |
| ponto em t = π/4 (bolinha branca), F verde grossa (6 px) e γ′ violeta (5 px, deslocada 0,16 para fora) lado a lado, rótulos `F` e `γ′` | palco | 32 | "deu exatamente o mesmo vetor" |
| C4.4 ③ (duas linhas) com **GM3** | (1020, 565) · (1112, 640) | 38 | "Passo três" |
| C4.5 em moldura menta | (1020, 770) | 40 | "Integra de zero a dois pi" |

Meça o tamanho real das letras nos stills (KaTeX e MathTex diferem) e ajuste até a fórmula principal ter 46–52 px de corpo e nada < 26 px. Nenhum silêncio: se a escrita acabar antes da frase seguinte, a tela espera parada.

### 7.2 Lições que valem desde o primeiro render

1. **Rótulo sai junto com o seu objeto** (legenda, seta, chip, moldura saem no mesmo `FadeOut` da fórmula ou do desenho).
2. **A coluna de um bloco sai antes da do próximo.** Nunca duas colunas ao mesmo tempo.
3. **O painel aparece com a primeira linha dele** (painel, lupa ou cartão vazio esperando é proibido).
4. **3D inteiro dentro da sua faixa** (G3), nunca sob painel ou texto, nunca no canto.
5. **Tamanho real medido**, não o pedido.
6. **Voo não cruza linha já escrita** (arco por fora; R5V = 0).
7. **Gatilho ≤ 0,3 s** da frase, sem comprimir a caneta; se não couber, liste no relatório.
8. **CTA só depois** do cartão do próximo vídeo (S2).
9. **Câmera e escala fixas** dentro de cada bloco; o palco 2D de um bloco (B2, B4) fica no mesmo lugar entre as âncoras do bloco, sem pulo.
10. **Placas fora das arestas** e sem órfãos nas emendas do 3D.
11. **Rótulo de palco 2D nunca sobre seta do campo** (§5.2).
12. **Manipulação que atravessa âncoras guarda o objeto de origem** (GM1: B2-1 → B2-2). O mesmo vale para resultado que vira chip no topo (B7-2 e B7-3): o chip é o objeto que encolhe e sobe, não um novo `Write`.
13. **Palco 2D calibrado antes do resto** (§8, item 22): o B4-1 só passa com o palco medido.

## 8. QA (rode `qa45.py`, adaptado do `qa4N.py` da base) e critérios de aceite

Cada item precisa de número medido no relatório. **Aceite = todos os itens dentro do limite.**

| # | Item | Como medir | Limite |
|---|---|---|---|
| 1 | Erros de render | `log_<LOTE>.txt` | 0 Traceback |
| 2 | Gatilhos | todo `self.gat(...)` achou a frase em `duracoes_estimadas.json` | 0 `gatilho-sem` |
| 3 | Flash por quadro | `[flash]` | **0** |
| 4 | Sobreposição texto × texto e voo × texto | `[R5]`, `[R5V]` | **0** |
| 5 | Margem e painel | `[R6]` (48 px; nada atravessa painel) | 0 |
| 6 | Papel | `[grade]`: papel em toda tela, inclusive sob o 3D; só o CTA liso | 0 s sem papel |
| 7 | Palco parado | `[parado]`: nada se move sem gatilho (campo, eixos e câmera parados) | 0 fora da tabela do §4 |
| 8 | Glyph maps | `[gm]`: GM1–GM11, cada um no seu lote | 100 % |
| 9 | Degraus | `[degrau]`: todos os degraus C1–C9 que vão à tela, com tempo | 100 % |
| 10 | Texto em MathTex | fórmula como `Text` ou texto corrido dentro de MathTex | 0 |
| 11 | Tamanho **real** das letras | altura medida nos stills 1080p, `qa/tamanhos_v1.txt` | principal 46–52 px, nada < 26 px |
| 12 | Alinhamento 3D | rótulo × ponto do `pontos.json` | ≤ 2 px |
| 13 | Comparação com o alvo **v1** | still do instante `self.marca(...)` ao lado do alvo, em resolução cheia | ±20 px, mesmas cores, mesmo conteúdo |
| 14 | Duração | lote × soma das âncoras | ±0,5 s por âncora |
| 15 | Efeitos | busca por `Flash`, `Indicate`, `Wiggle`, `glow`, `opacity` < 1 em formas, `always_redraw` decorativo, `MoveAlongPath` | 0 |
| 16 | Linha órfã | varredura a cada 0,5 s | 0 |
| 17 | 3D cortado, escondido ou no canto | pixels do 3D fora da faixa G3, sob painel/texto ou no canto | 0 |
| 18 | G1–G6 por cena 3D | tabela OK/NÃO + prancha 2×3 por cena 3D | tudo OK |
| 19 | Atraso de gatilho | início de cada degrau × instante da frase, `qa/gatilhos_v1.txt` | ≤ 0,3 s; não acelere a caneta |
| 20 | Linhas por etapa e CTA | ≤ 7 linhas na coluna; CTA só depois do cartão do próximo vídeo (≥ 8 s), tela lisa | 0 excessos; R5 = 0 no S2 |
| 21 | Rótulo × seta do campo | caixa de cada rótulo do palco 2D × caixas das setas do campo | 0 (ou seta apagada e anotada) |
| 22 | Calibração do palco 2D | no still 1080p de cada alvo 2D com palco: origem dos eixos, ponta do eixo x, um ponto da curva (no B4: (R, 0) e (0, R)) e a base e a ponta de 3 setas do campo × as mesmas posições calculadas pela `vista(cx, cy, U)` do `keys45.js`; `qa/palco2d_v1.txt` | ≤ 2 px |

Item que não se aplica ao lote = **N/A**, nunca "OK" (ex.: 12, 17, 18 nos lotes só 2D; 22 no PB7 e no PA). **Render concluído não é lote aprovado:** um lote sem Traceback ainda reprova por leitura, sincronia ou composição. Uma verificação só conta se foi executada e deixou evidência; não atribua ao `qa45.py` o que ele não mede (diga no relatório o que é automático e o que foi olhado). Rode primeiro o mais barato (`./seco.sh LOTE`) e só depois o render; refaça **só** o lote afetado.

### 8.1 Três tipos de evidência (não misture)

1. **Automático** (`qa45.py`, `seco.sh`): itens 1–10, 14–16, 19, 20, 21.
2. **Medido** (números em arquivo): 11, 12, 17, 19, 22.
3. **Inspeção visual** (você olhando em resolução cheia): 13, 18. Para cada um dos 18 alvos: still nativo 1920×1080 no instante de `self.marca(...)`, ao lado do alvo, e uma linha no relatório com o que difere. A prancha consolidada complementa; não substitui os stills.

Olhe também **instantes intermediários**: entrada do campo, `Create` das curvas, caneta em movimento, glyph maps, voos (GM8 no B6-1), a entrada da lupa no B2-2, os estados novos do 3D no B7-3, troca de coluna, renovação de etapa.

### 8.2 Sincronização

Para cada gatilho, `gatilhos_v1.txt` traz: âncora, frase, instante previsto, início da animação, desvio. Duração das âncoras **preservada**: se a escrita acabar antes, a tela espera parada; se não couber, **não acelere a caneta** e **não tire degrau**: registre âncora e segundos que faltam. Duração atingida acelerando a escrita não é aprovação.

### 8.3 Montagem

Depois do `montar.py`: ordem PH → PS, nenhum lote repetido ou ausente, nenhum quadro preto inesperado, nenhuma coluna ou rótulo antigo na emenda, salto de palco ou papel nas emendas, duração total (≈ 19:00) e arquivo íntegro (abre e toca até o fim).

### 8.4 A verificação da matemática não valida a implementação

Os 39/39 do sympy conferem a **proposta**. O que prova a implementação são os itens 8 e 9 e a comparação visual: confira que cada linha na tela é a da proposta, caractere a caractere.

## 9. Relatório obrigatório (no fim, uma vez)

0. Estado inicial (`git status`), o que existia em `yt_0045_*` e a unidade-base usada com a evidência.
1. Arquivos criados e alterados.
2. Comandos rodados e resultado (tempo de render por lote).
3. Tabela do §8 com o número medido de cada item, **por lote**.
4. Caminhos do vídeo, dos quadros de comparação e da pasta de QA.
5. Quantos dos 18 alvos você inspecionou de fato; o que ficou diferente e por quê; o que não conseguiu; o que **não** verificou.
6. Cenas Three.js: o que foi portado, resolução, custo por quadro, alinhamento medido (px).
7. Setas do campo apagadas sob rótulos (§5.2), se houver.
8. Lotes concluídos e, se houver, bloqueados. Pare. Não comece voz, SRT, 1080p nem entrega.

## 10. O que não fazer

- Não alterar `template/`, `assets/`, `docs/`, `AGENTS.md`, `pyproject.toml`, `uv.lock` nem unidades de outros vídeos (a unidade-base é só leitura).
- Não usar restaurações globais (`git restore .`, `git reset --hard`, `git clean -fdx`).
- Não instalar nada, não recriar `.venv`, não rodar `npm install`.
- Não usar Blender, `ponte.py` nem `Solido3D`; não fazer 3D dentro do Manim.
- Não mudar matemática, notação, cores, texto da tela ou a narração. Se achar erro, **reporte** antes.
- Não escrever θ nem ds em lugar nenhum.
- Não citar livro na tela. Não citar vídeo não publicado ("como vimos no EP. 19" é proibido; "nas cilíndricas", "a soma de Riemann que vocês conhecem" são permitidos). O teorema de Green e os campos conservativos são citados como assunto ("mais adiante no curso"); na tela, só o chip do alvo 11 (`SÓ IMPORTAM AS PONTAS: CAMPO CONSERVATIVO`), sem prometer vídeo.
- Não fazer voz, SRT, 1080p, master, entrega, commit, branch, push.

## 11. Condição de parada

Pronto quando: a unidade nova existe sem ter sobrescrito trabalho anterior; o palco 2D foi calibrado (item 22); todos os lotes passaram no §8; os 18 alvos v1 foram comparados em 1920×1080; o preview completo foi montado e as emendas conferidas; a `ficha.md` tem o Estado final; o relatório do §9 traz caminhos e números. **Depois disso, pare.**
