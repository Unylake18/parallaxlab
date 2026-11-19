# HANDOFF v1 · yt_0042 · CÁLCULO III · EP. 17 · Coordenadas cilíndricas na integral tripla · PREVIEW

> Handoff **autocontido**, escrito para um agente que **não** conhece este canal (DeepSeek, Gemini, NVIDIA ou outro). Tudo o que você precisa está aqui, no `AGENTS.md` do repositório e no zip `yt0042_handoff_v1_completo.zip`. Responda sempre em **português do Brasil**.
> Fase aberta: **preview silencioso 960×540 / 15 fps**. Não faça voz, SRT, 1080p, master, entrega, commit, branch nem push.

---

## 0. Como trabalhar (leia primeiro)

1. Rode `git status --short` e preserve tudo o que já existe. Não altere arquivos fora de `videos_longos/yt_0042_coordenadas_cilindricas/`.
2. Leia o `AGENTS.md` da raiz do repositório (regras do canal). Este handoff **não** substitui o AGENTS.md; quando os dois parecerem divergir, siga este handoff no conteúdo e o AGENTS.md no ambiente (uv, Manim, CRF).
3. **Escopo: o vídeo inteiro numa passada só** (decisão do Kaio, 2026-11-16). Você não para entre os lotes; você para só no fim, com o preview completo e o relatório do §9. Mas trabalha **lote a lote, nesta ordem**, e cada lote só começa quando o anterior passou no QA do §8:
   1. `PB2` primeiro (B2-1 a B2-4). A B2-3 (§7.1) calibra a escrita: caneta, glyph maps, papel e tamanhos. Compare o still dela com o alvo 08 antes de seguir.
   2. `PB1` (B1-1 a B1-3). É o primeiro lote com 3D: porte a cena `ponto` (§4), meça o alinhamento ≤ 2 px e compare com os alvos 03 e 04 antes de seguir.
   3. `PH`, `PA`, `PB3`, `PB4`, `PB5`, `PB6`, `PS`, nesta ordem.
   4. `montar.py` e o QA do vídeo inteiro.
   Se um lote falhar no QA, corrija só esse lote antes de abrir o próximo. Não deixe "para o fim" nenhum item do §8.
   Ao fechar cada lote, anote na `ficha.md` (seção Estado) o lote, o tempo de render e o resultado do QA: se a sessão cair, a próxima retoma dali sem refazer o que passou.
4. **Não invente.** Nada de efeito que não esteja escrito aqui (brilho, pulso, partículas, sombra, transparência, "palco vivo", câmera passeando, tracer). Na dúvida, faça o mais simples e anote no relatório.
5. **Olhe os quadros.** Cada teste termina com quadros extraídos do seu render, em resolução cheia, comparados com o quadro-alvo do mesmo instante. Se o seu modelo não enxerga imagens, **diga isso no relatório** e não declare o QA visual como feito: entregue as imagens lado a lado para o Kaio olhar.

## 1. O que entregar

| Saída | Caminho |
|---|---|
| Preview silencioso do vídeo inteiro (≈ 20:11, 960×540, 15 fps) | `renders/v1/yt_0042_preview_v1_540p15.mp4` |
| Um mp4 por lote | `media_<LOTE>/videos/cena/540p15/<LOTE>.mp4` |
| QA (relatórios do §8) | `renders/v1/qa/` |
| Comparação com os 17 alvos (seu still em 1920×1080 ao lado do alvo, no instante de `self.marca`) | `renders/v1/qa/comparacao/NN_<cena>.jpg` + `prancha_alvos.jpg` (todas juntas) |
| Alinhamento 3D (rótulo × ponto, por lote) | `renders/v1/qa/alinhamento3d_v1.txt` |
| `ficha.md` com a seção Estado atualizada | na unidade |

## 2. Criar a unidade

```
videos_longos/yt_0042_coordenadas_cilindricas/
  ficha.md                  (§2.1)
  referencia/               ← copie para cá: yt_0042_narracao_v1.md, este handoff, a proposta, yt_0042_quadros_alvo_v1/, verificacao/
  kit.py  v41.py            ← copie do yt_0041 SEM mudar nada (biblioteca da série)
  k42.py                    ← copie k41.py e adapte (§3.2)
  cena.py  render.sh  render3d.sh  seco.sh  still.sh  montar.py  quadros.py  gerar_ancoras.py  qa42.py (de qa41.py)
  sec_h.py sec_a.py sec_b1.py … sec_b6.py sec_s.py
  threejs/  r3d.js  package.json  cena3d/c42.js + uma página .html por cena (§4)
```

**De onde copiar:** `K:\PycharmProjects\manim-fisica\videos_longos\yt_0041_coordenadas_esfericas\` (a unidade irmã, preview v2 aprovado para seguir). Copie os arquivos listados acima; **não** copie `renders/`, `media_*`, `log_*`, `threejs/q3d/`, `threejs/pedidos3d/`. Se a pasta não existir na sua máquina, use `kit_base/` do zip (cópia dos mesmos arquivos; `sec_b4.py` e `sec_s.py` estão lá só como exemplo de estilo; a sec_b4 importa `sec_b1`, que não está no kit_base: não tente rodá-la).

Troque `yt_0041`/`41` por `yt_0042`/`42` nos nomes de arquivo e nos textos de cabeçalho, nos caminhos de `gerar_ancoras.py` (lê `referencia/yt_0042_narracao_v1.md`) e de `montar.py` (`ORDEM = ["PH","PA","PB1","PB2","PB3","PB4","PB5","PB6","PS"]`). Os scripts `.sh` usam o Python `K:/PycharmProjects/manim-fisica/.venv/Scripts/python.exe` e o Node com `NODE_PATH=K:/PycharmProjects/manim-fisica/videos_longos/yt_0020_cinematica_angular/threejs/node_modules`; não crie outro ambiente, não rode `uv sync`, `pip install` nem `npm install`.

### 2.1 ficha.md

```
formato: longo_horizontal
tipo: teoria_visual
serie_publica: CÁLCULO III · EP. 17
titulo: Coordenadas cilíndricas na integral tripla
disciplina: Cálculo III
modulo: 3.5 Integral tripla
bloco: 3.5-T3
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §5.6 (Ex. 1 lata com densidade √(x²+y²+z²); Ex. 2 cilindro fora do eixo). Livro só na descrição do YouTube
unidades: s, r, x, y, z, R, h em metros; θ e t em radianos; volumes em m³
notacao: s = distância ao eixo z; θ = ângulo das polares; z = altura; r = distância até a origem (r² = s² + z²); ρ = densidade; R, h = raio e altura fixos; T = a transformação; u, t = substituições
solido_3d: nenhum do arsenal Blender (lata, grade, ponto, caixa, latagrade, caixinha, cilindro, deslocado, giro feitos direto em Three.js)
3d_threejs: lata, grade, ponto, caixa, latagrade, caixinha, cilindroRot, deslocadoSonda, giro (geometria em referencia/yt_0042_quadros_alvo_v1/c3d42.html)
duracao_alvo: ≈ 20:11 (narração v1: 3.600 palavras)
```
Número `yt_0042` e EP. 17 são provisórios.

## 3. Base de código: o que já existe e como usar

### 3.1 Camadas

- `kit.py`: classe `Base(Scene)` com `setup_base/corpo/fim`, relógio de âncoras (`self.an("B2-3")` posiciona a cena no início da âncora; `self.gat("frase")` espera até a frase de gatilho da fala), canto do título (`TITULO = "CÁLCULO III · INTEGRAL TRIPLA"`), logo, papel, caneta `_Caneta` (traço 1,5 px na prévia; é o "fino"), `Palco3D` (cola os PNGs do Three.js atrás da camada Manim). **Não edite.**
- `v41.py`: paleta (`CI, AZC, CORAL, GEO, BR, AL, MEN`), `papel`, `parte`, `junta`, `pena`. **Não edite** (só renomeie para v42.py se quiser; o conteúdo fica igual).
- `k41.py` → **`k42.py`**: a camada da unidade. É aqui que você adapta (§3.2). Funções que você vai usar:
  - `L(pecas, x, y, size)` — uma linha de MathTex **de string única**, montada por peças com chave: `L([("i", r"\int_0^1"), ("eq", "="), …], 1010, 300, 46)`. `x, y` em px de 1080p (canto esquerdo, linha de base aproximada).
  - `sel(m, chave)` e `gl(m, *chaves)` — pegam os glifos de uma peça.
  - `parte(m, glifos, "descrição")` + `self.pena(...)` — escreve só aqueles glifos com a caneta, glifo a glifo, da esquerda para a direita.
  - `self.voos([(origem, destino)], nota="…")` — `TransformFromCopy` em arco do desenho para a coluna; a cópia sai sem fantasma.
  - `self.gm(n, A, B, pares, copia=True, nota="…")` — glyph map **n** do MF-Tools (`TransformByGlyphMap`) de A para B, com mapa explícito; `auto_fade` só no que sai; o que entra é escrito pela caneta ou voa.
  - `self.degrau("C3", "texto")` — registra um degrau de conta (o QA confere que todos os degraus do §6 apareceram, com tempo).
  - `mixl`, `chip`, `selo`, `moldura`, `painel41`, `chave_um` (chave "= 1"), `guia41`, `self.rot3(palco, "ponto", tex)` (rótulo preso ao 3D), `self.palco(cena, cam_alvo("b11"), **estado)`, `self.col(...)`, `self.sobe_sai`, `self.acende_sai`, `self.marca("08_B2-3")` (marca o instante do quadro-alvo para a comparação), `self.sai_fim()`.
- Estilo de cena: veja `kit_base/sec_b4.py` (a cebola do EP. 16). Uma classe por lote (`class PB2(B42)`), `ANTES = "…"`, `corpo()` que segue a fala com `self.gat(...)` frase a frase.

### 3.2 O que muda em k42.py

1. **Macros do preâmbulo** (copie a ideia de `k41.py` e troque pelas do `sb42.html`): `\X` x âmbar `#FFC24D`, `\Y` y magenta `#EA63FF`, `\Z` z azul `#5AA2FF`, `\S` s pêssego `#FFC08A`, `\T` θ verde-água `#2EE6A6`, `\R` r laranja `#FF9440`, `\de` ρ ciano `#35D9FF`, `\Js` o s do fator em **lima `#C6F26B`**, `\dS \dT \dZ` (d em branco + letra colorida), `\DS \DT \DZ` (Δ colorido), `\uu \du` u e du `#E08A3C`, `\Tt \dTt` t e dt `#E08A3C`, `\tg` = `\operatorname{tg}`, `\sen` = `\operatorname{sen}`, `\Ci{…}` ciano, `\Al{…}` ALERTA `#FF5D5D`, `\Ge{…}` GEO `#B8C4DA`, `\Me{…}` menta `#8CFFD2`. As definições exatas estão no topo de `referencia/yt_0042_quadros_alvo_v1/sb42.html` (procure `macros`).
2. **Câmeras e pontos 3D** = os do `c3d42.html` (§4). `cam_alvo(k)` devolve o enquadramento do alvo `k` (chaves do sb42: `h1 h2 b11 b12 b13 b21 b24 b31 b41 b52 b55 s2`).
3. `TITULO` continua `"CÁLCULO III · INTEGRAL TRIPLA"`.
4. Nada mais muda. Se você sentir vontade de "melhorar" o kit, não faça: anote no relatório.

## 4. 3D: Three.js (pipeline da unidade irmã)

1. **Passada seca:** `./render3d.sh PB1` roda o Manim com `PEDIDOS3D=1 --dry_run` e grava `threejs/pedidos3d/PB1.json` (o estado 3D pedido em cada quadro).
2. **Render 3D:** `node threejs/r3d.js --lote PB1` abre `threejs/cena3d/<cena>.html` no Chrome (playwright-core, `CHROMIUM_PATH` = Chrome do Windows), espera `window.cenaPronta`, chama `setEstado(estado)` por quadro e grava `threejs/q3d/PB1_960x540/<cena>/fNNNNN.png` (fundo transparente) + `pontos.json` (pixel de cada ponto nomeado).
3. **Render Manim:** o `Palco3D` cola os PNGs atrás da camada Manim; os rótulos usam `pontos.json` (`self.rot3`). Alinhamento exigido: **≤ 2 px** entre o rótulo e o ponto 3D.

**Portar as cenas:** a geometria pronta está em `referencia/yt_0042_quadros_alvo_v1/c3d42.html` (Three.js r128, uma chave por cena: `?k=ponto`). Copie `kit_base/threejs/cena3d/c41.js` como modelo de **estrutura** (como o yt_0041 transforma uma chave do `c3d41.html` em página animável com `setEstado`) e crie `c42.js` com as cenas desta unidade, **com os mesmos parâmetros, câmeras e cores do c3d42.html**. Uma página `.html` por cena (`window.CENA_ID = "ponto"`). Estados animáveis (os únicos permitidos):

| Cena (chave) | Usada em | Estados (0→1) |
|---|---|---|
| `lata` | H1, B5-1, B5-2, B5-5 | `giro` (câmera ~30° em volta de z, só no H1), `quina` (contorno ALERTA na quina da tampa, B5-5) |
| `grade` | H2 | `traco` (degradê → traço), `cil`, `pag`, `andar` (cada família entra e sai), `cels` (as duas células lima) |
| `ponto` | B1-1, B1-2 | `sombra`, `s`, `arco`, `z`, `fio` (fio horizontal do eixo até P), `pag` (o triângulo da página), `xy` (tracejados x e y no chão) |
| `caixa` + `latagrade` | B1-3, B3-1 | `cel` (cópia viaja e curva), `eixo` (face s = 0 + eixo em ALERTA), `costura` (faces θ = 0, 2π + costura), `parte` (só B3-1: metades afastam 0,15 e voltam) |
| `caixinha` | B2-1 | `orbita` (~30° em ~3 s, para antes da 1ª aresta), `a1` Δs, `a3` Δz, `a2` arco sΔθ + raio tracejado |
| `cilindroRot` | B2-4 | `rotulo` (parede em contorno ALERTA) |
| `deslocadoSonda` | B3-2, B4-1 | `sombra`, `sonda` (cresce do chão ao telhado), `eixoNovo` |
| `giro` | S2 | `seta` (seta curva de giro), `cel` (célula + fio s) |

Regras do 3D: cores sólidas e opacas, sem luz dinâmica, sem brilho; a câmera só se move onde a tabela diz; no pouso para o 2D a câmera está parada. O 3D é **liso** (sem papel); o papel entra quando a cena vira 2D.

**Escala no Manim:** o quadro é 16 × 9 unidades ⇒ **1 unidade = 120 px** em 1080p (`x_m = (x_px − 960)/120`, `y_m = (540 − y_px)/120`). As funções do kit já recebem px; use px.

## 5. Sistema visual (vale para todas as cenas)

- **Fundo:** violeta liso `#18143A → #0F0C26` (do kit). **Papel** (quadradinhos) de borda a borda em toda tela 2D: com eixos, `papel(ax)` nascendo dos eixos; sem eixos, `papel(passo=0.5)`. Painel 2D dentro de cena 3D = painel opaco `#16123A` com grade própria de 30 px. 3D e CTA ficam lisos.
- **Canto:** duas linhas no canto superior esquerdo: `CÁLCULO III · INTEGRAL TRIPLA` (pequeno, apagado) e o título da cena em branco (maiúsculas, Space Grotesk). Logo no canto superior direito.
- **Tamanhos (em 1080p):** fórmula principal 50–54 px, secundária 44–46, legenda 30 (mínimo 26), chips 30. Coluna de fórmulas em **x ≥ 1010 px** quando há 3D à esquerda; **no máximo 5 linhas por etapa** (depois renova: as linhas antigas sobem e saem, e o resultado vira chip no topo). Margem de 48 px nas bordas.
- **Cores das grandezas** (texto e desenho): s pêssego `#FFC08A`; θ verde-água `#2EE6A6`; z azul `#5AA2FF`; x âmbar `#FFC24D`; y magenta `#EA63FF`; r laranja `#FF9440`; ρ ciano `#35D9FF`; **o fator s do jacobiano em lima `#C6F26B`** (sempre); u, t `#E08A3C`; ALERTA `#FF5D5D`; GEO (neutro) `#B8C4DA`; menta (ok, moldura do resultado) `#8CFFD2`; entrada da sonda `#7FB2FF`; saída da sonda `#FF7A8A`. Operadores (d, ∫, =, +) em branco.
- **Escrita (regra do canal):** termo novo = **caneta finíssima glifo a glifo, esquerda → direita**; termo que vem do desenho = **voo** (`TransformFromCopy`) do desenho para a coluna; manipulação algébrica = **glyph map** (`TransformByGlyphMap`, MathTex de string única nos dois lados). **Proibido:** `FadeIn` de linha pronta; `Write`/`FadeIn`/`TransformFromCopy` dentro de `Succession(Wait…)` ou `AnimationGroup` que ponha o destino na tela antes da hora (o QA `FLASH POR QUADRO` tem de dar **zero**).
- **Sem efeitos:** nada de pulso, brilho, partícula, sombra, transparência, tracer, palco vivo. Destaque = sublinhado fino ou contorno que acende e apaga.
- **Conta inteira:** a tela mostra **todos** os degraus do §6, um por linha. A voz (depois) não lê número por número; a tela, sim, escreve tudo.

## 6. Contas (o que a tela escreve, linha a linha)

As contas completas, com ID de degrau, estão na proposta (`referencia/calculo3_35t3_coordenadas_cilindricas_proposta_v1.md`, §3, C1–C10) e foram conferidas no sympy (`referencia/verificacao/`, 56/56). Use os IDs **C1…C9** em `self.degrau(...)`. Exemplo, a conta **C3** da B2-3 (a primeira que você implementa):

| degrau | linha na tela (LaTeX com as macros) |
|---|---|
| C3.1 | `\dfrac{\partial(\X,\Y,\Z)}{\partial(\S,\T,\Z)}=\left|\begin{matrix}\cos\T & -\S\sen\T & 0\\ \sen\T & \S\cos\T & 0\\ 0 & 0 & 1\end{matrix}\right|` (escrita **coluna por coluna**) |
| C3.2 | `=\Ge{0}\cdot M_{31}-\Ge{0}\cdot M_{32}+1\cdot M_{33}` |
| C3.3 | `M_{33}=\left|\begin{matrix}\cos\T & -\S\sen\T\\ \sen\T & \S\cos\T\end{matrix}\right|` |
| C3.4 | `M_{33}=\cos\T\cdot\S\cos\T-(-\S\sen\T)\cdot\sen\T` (os 4 fatores **voam** das células da matriz) |
| C3.5 | `=\S\cos^2\T+\S\sen^2\T` (glyph map GM2) |
| C3.6 | `=\S\,\underbrace{(\cos^2\T+\sen^2\T)}_{=1}` (glyph map GM3; a chave "= 1" entra depois, pela caneta) |
| C3.7 | `=\Js` dentro da moldura menta · chip `\S\ge 0\ \Rightarrow\ |J|=\Js` |

## 7. Cena a cena

**Fonte da verdade, nesta ordem:** (1) a narração `referencia/yt_0042_narracao_v1.md` (âncoras, Tela, Coluna, **Gatilhos**, fala); (2) os quadros-alvo `referencia/yt_0042_quadros_alvo_v1/` (posição e tamanho de cada coisa; as coordenadas exatas estão no `sb42.html`, chave indicada); (3) este §7. O quadro-alvo mostra o **estado final** de uma etapa; o caminho até ele segue os gatilhos da narração.

Cada gatilho = uma frase da fala; a ação de tela começa nela (`self.gat("frase")`). Não há ação sem gatilho, e não há gatilho sem ação (exceto os marcados "nada novo").

| Âncora | Lote | Alvo (arquivo · chave sb42) | Notas de implementação |
|---|---|---|---|
| H1 | PH | 01 · `h1` | lata 3D à esquerda (`lata`, gira ~30° e para antes da coluna); coluna x = 1010; painel `EM ESFÉRICAS` 2D opaco (corte 1 × 1, duas sondas, diagonal tracejada ALERTA). |
| H2 | PH | 02 · `h2` | `grade`: traço; famílias entram uma por vez e saem; as duas células lima com `?`; painel `A GRADE DA LATA`. |
| A1 | PA | — | 2D, papel passo 0,5: logo, título `COORDENADAS CILÍNDRICAS NA INTEGRAL TRIPLA`, linha `NESTE VÍDEO: O ENDEREÇO (s, θ, z) · O FATOR s · A LATA PESADA`. |
| B1-1 | PB1 | 03 · `b11` | `ponto` à esquerda; painéis `DE CIMA` e `DE LADO` opacos (410 × 330 px) em (1010, 150) e (1450, 150); linhas `x = s cos θ, y = s sen θ, z = z` (52 px, voam do painel DE CIMA e da altura 3D), `s = DISTÂNCIA AO EIXO z`, `NÃO É A DISTÂNCIA ATÉ A ORIGEM` (ALERTA), `r² = s² + z²` (voa do triângulo do painel DE LADO), `s ≥ 0, 0 ≤ θ < 2π`. |
| B1-2 | PB1 | 04 · `b12` | mesmo 3D, sem recarregar a câmera; números presos (`2`, `π/3`, `3/2`, depois `1`, `√3`); coluna de 5 linhas (C1); a linha `r = 5/2` e a legenda `3-4-5 PELA METADE` renovam a coluna. |
| B1-3 | PB1 | 05 · `b13` | `caixa` (esc 0,72) à esquerda, seta `T`, `latagrade` (esc 0,58) ao centro; coluna em x = 1250. A cópia da célula viaja e se curva (um movimento); as bordas ruins acendem **juntas nas duas peças**, uma família por vez. |
| B2-1 | PB2 | 06 · `b21` | `caixinha`: órbita curta e para; arestas uma por vez com rótulo em placa **fora** da célula + fio-guia; **GM1** `ΔV ≈ Δs·sΔθ·Δz → = s Δs Δθ Δz` (o s vira lima); painel numérico (C2). |
| B2-2 | PB2 | 07 · `b22` | 2D com papel: painéis `DE CIMA` (setor de anel) e `DE LADO` (retângulo Δz), cartão à direita; `dV = s ds dθ dz` em moldura menta (58 px), centrada embaixo. |
| B2-3 | PB2 | 08 · `b23` | Detalhe no §7.1 (é a primeira cena que você implementa). |
| B2-4 | PB2 | 09 · `b24` | `cilindroRot` à esquerda; C4 na coluna; **GM4** `(h−0)(R²/2−0)(2π−0) → πR²h` (o 2 de baixo cancela com o 2 do 2π: os dois acendem e saem juntos); painel `SEM O s:` embaixo; o rótulo da parede acende em ALERTA (só contorno). |
| B3-1 | PB3 | 10 · `b31` | caixa + lata em cima (3D liso numa faixa), painel do teorema embaixo (painel opaco sobre o papel); **GM5** teorema geral → fórmula das cilíndricas (o s lima voa do chip dV). |
| B3-2 | PB3 | (sem alvo) | `deslocadoSonda` parado à esquerda; selos ①②③ e as três linhas da receita (ver narração). |
| B4-1 | PB4 | 11 · `b41` (etapa 2) | etapa 1 (sem alvo): desigualdades, `+1` dos dois lados, **GM6** `x² − 2x + 1 + y² ≤ 1 → (x − 1)² + y² ≤ 1`, polo, chip `O 1 NÃO DEPENDE DE NADA ⇒ JACOBIANO s`; etapa 2 (= alvo 11): ①②③, **GM7** telhado `x + y → 1 + s cos θ + s sen θ`; painel `DE CIMA` embaixo à direita. |
| B4-2 | PB4 | 12 · `b42` (tela da conta em θ) | o 3D sai; painel `DE CIMA` à esquerda (440 × 460); coluna em x = 560; tela 1 (sem alvo): linhas 7–8 da C5 com **GM8** (distribui o s); tela 2 (= alvo 12): primitiva com o `−(1/3) cos θ` em ALERTA, chips dos valores, **GM9** até `π/2 + 2/3 ≈ 2,24` em moldura menta, três chips de leitura, legenda DESAFIO. |
| B5-1 | PB5 | (sem alvo) | lata parada à esquerda; chip `r² = s² + z²` no topo; linha ρ (o `s² + z²` voa do chip), CAIXA, M com as chaves `DENSIDADE` (ciano) e `FATOR` (lima), chip ALERTA `z POR DENTRO: LOGARITMO → TRAVA`, chip menta `s POR DENTRO: O s DO FATOR AJUDA`. |
| B5-2 | PB5 | 13 · `b52` | C6; **GM10** `√(s²+z²) s ds → (1/2) u^{1/2} du`; **GM11** `(z²)^{3/2} → z³`; o s do fator e o s do du acendem juntos (sublinhado lima) e apagam. |
| B5-3 | PB5 | 14 · `b53` | painel `O TRIÂNGULO` à esquerda (opaco); coluna em x = 680; C7; **GM12** `(1+z²)^{3/2} dz → sec³t · sec²t dt → sec⁵t dt`; o caso z = 1 aparece por 1 s no painel (só o cateto muda) e volta. |
| B5-4 | PB5 | 15 · `b54` (etapa 2) | etapa 1: cartão RECORRÊNCIA + n = 5 + n = 3 + chips do triângulo; etapa 2 (= alvo 15): três colchetes e I; **GM13** `4√2/8 + 3√2/8 → 7√2/8`; termos com tg 0 e ln 1 acendem e saem. |
| B5-5 | PB5 | 16 · `b55` | lata parada; C9; **GM14** `7√2π/12 + (π/4)ln(1+√2) − π/6 → (π/12)(7√2 − 2 + 3ln(1+√2))`; moldura menta + ✓; CONFERE; depois renova com MÉDIA e a legenda ρ VAI DE 0 A √2 (a quina acende no 3D, só contorno). |
| B6 | PB6 | (sem alvo) | 2D com papel; quatro cartões opacos com miniaturas dos PNGs 3D (lata ✓, deslocado ✓, cilindro ✓, bola ✗ ESFÉRICAS em contorno simples); cinco legendas ✓/✗. |
| S1 | PS | (sem alvo) | 2D com papel; três colunas ✓ com os resultados que **voam** das suas fontes (πR²h, π/2 + 2/3, ≈ 2,76). |
| S2 | PS | 17 · `s2` | `giro`: seta de giro, célula + fio s; três linhas; cartão `NO PRÓXIMO VÍDEO · CENTRO DE MASSA · E MOMENTO DE INÉRCIA · NA INTEGRAL TRIPLA` (≥ 8 s); depois o CTA liso do kit (`cta41`). |

Os glyph maps GM2 e GM3 estão na B2-3; GM1…GM14 numerados acima. Monte cada glyph map só depois de estabilizar o LaTeX das duas linhas (índices mudam com qualquer espaço). Use `show_indices` só para desenvolver; nunca deixe índices no render.

### 7.1 B2-3 em detalhe (o primeiro lote: calibra o resto)

Tela 2D inteira com papel de borda a borda (passo 0,5). Posições do alvo 08 (`sb42.html`, chave `b23`), em px de 1080p:

| Elemento | Posição | Tamanho | Entra em |
|---|---|---|---|
| legenda `1ª COLUNA: EM s · 2ª: EM θ · 3ª: EM z` | (60, 185) | 30 | "Cada coluna é a derivada" (caneta) |
| C3.1 (matriz) | (60, 360) | 54 (vale o alvo; a linha "Tela" da narração dizia 44) | a fração ∂(x,y,z)/∂(s,θ,z), o `=` e as barras entram em "Cada coluna é a derivada"; depois a matriz é escrita **linha por linha**, entrada a entrada: linha 1 (derivadas de x em s, θ, z) em "Derivando x igual a s cosseno de téta"; linha 2 em "O y é igual"; linha 3 em "o z é o mais preguiçoso". |
| seta + `LINHA DE BAIXO: + − +` (menta) | seta da direita até a linha 3 da matriz, texto 30 px | — | "Então expande por ela" |
| C3.2 | (60, 610) | 48 | "Então expande por ela" (logo depois da seta) |
| os dois `0 · M` acendem e saem | — | — | "Os dois zeros matam" |
| tracejado lima no menor 2 × 2 (linhas 1–2, colunas 1–2) + legenda `O MENOR DO 1: TAMPA A LINHA 3 E A COLUNA 3` (lima, 30) | legenda em (60, 720) | — | "tampa a linha três e a coluna três" |
| C3.3 (o 2 × 2) | (60, 860) | 48 | logo depois (as 4 entradas **voam** do tracejado) |
| C3.4 | (1010, 560) | 46 | "Diagonal principal menos a secundária" (os 4 fatores voam das entradas do 2 × 2) |
| C3.5 | (1060, 680) | 48 | "Cuidado com o menos com menos" (**GM2**: `−(−s sen θ)·sen θ` → `+ s sen²θ`; os dois menos acendem em ALERTA antes de sair) |
| C3.6 | (1060, 800) | 48 | "Põe o s em evidência" (**GM3**; a chave `= 1` entra pela caneta) |
| `= s` em moldura menta | logo à direita da C3.6, 54 px | — | "O determinante é s" |
| chip `s ≥ 0 ⇒ \|J\| = s` | (1060, 950) | 40 | "nunca é negativo" |

Duração da âncora ≈ 1:11,8 (214 palavras); a cena segue os instantes de `duracoes_estimadas.json` (gerado por `gerar_ancoras.py`). Nenhum silêncio: se a escrita acabar antes da próxima frase, a tela espera parada (o QA mede).

## 8. QA (rode `qa42.py`, adaptado do `qa41.py`) e critérios de aceite

Cada item precisa de número medido no relatório. **Aceite = todos os itens dentro do limite.**

| # | Item | Como medir | Limite |
|---|---|---|---|
| 1 | Erros de render | `log_<LOTE>.txt` | 0 Traceback |
| 2 | Gatilhos | todo `self.gat(...)` achou a frase em `duracoes_estimadas.json` | 0 `gatilho-sem` |
| 3 | Flash por quadro | `[flash]` no log (destino visível antes da hora) | **0** |
| 4 | Sobreposição texto × texto e voo × texto | `[R5]`, `[R5V]` | **0** |
| 5 | Margem e painel | `[R6]` (48 px; nada atravessa painel) | 0 |
| 6 | Papel | `[grade]`: toda tela 2D com papel de borda a borda; 3D e CTA lisos | 0 `2D-SEM-GRADE` |
| 7 | Palco parado | `[parado]`: nenhum objeto se move sem gatilho | 0 fora da tabela do §4 |
| 8 | Glyph maps | `[gm]`: os números previstos apareceram (GM1–GM14, cada um no seu lote) | 100 % |
| 9 | Degraus | `[degrau]`: todos os degraus C1–C9 com tempo | 100 % |
| 10 | Texto em MathTex | fórmula escrita como `Text` ou texto corrido dentro de MathTex | 0 |
| 11 | Tamanho das fórmulas | altura do x-height medida em quadro 1080p (`still.sh`) | principal ≥ 50 px, legenda ≥ 26 px |
| 12 | Alinhamento 3D | rótulo × ponto do `pontos.json` (todos os lotes com 3D) | ≤ 2 px |
| 13 | Comparação com o alvo | quadro do instante `self.marca(...)` lado a lado com o alvo (`quadros.py`), em resolução cheia | posições ±20 px, mesmas cores, mesmo conteúdo |
| 14 | Duração | lote × soma das âncoras | ±0,5 s por âncora |
| 15 | Efeitos | busca no código por `Flash`, `Indicate`, `Wiggle`, `glow`, `opacity` < 1 em formas, `always_redraw` decorativo | 0 |

Rode primeiro o mais barato (`./seco.sh LOTE`, que já pega gatilhos, R5 e flash) e só depois o render. Quando um item falhar, refaça **só** o lote afetado.

## 9. Relatório obrigatório (no fim, uma vez)

1. Arquivos criados e alterados (caminhos).
2. Comandos rodados e resultado de cada um (tempo de render por lote).
3. Tabela do §8 com o número medido de cada item, **por lote**.
4. Caminhos do vídeo, dos quadros de comparação e da pasta de QA.
5. O que ficou diferente do alvo e por quê; o que você não conseguiu fazer; o que você **não** verificou (seja explícito: "não olhei os quadros" é melhor que "QA ok").
6. Pare. Não comece voz, SRT, 1080p nem entrega.

## 10. O que não fazer

- Não alterar `template/`, `assets/`, `docs/`, `AGENTS.md`, `pyproject.toml`, `uv.lock` nem unidades de outros vídeos.
- Não instalar nada, não recriar `.venv`, não rodar `npm install`.
- Não usar Blender, `ponte.py` nem `Solido3D`; não fazer 3D dentro do Manim.
- Não mudar matemática, notação, cores, texto da tela ou a narração. Se achar erro, **reporte** antes de mudar.
- Não citar livro na tela. Não citar vídeo não publicado ("como vimos no EP. 16" é proibido; "nas esféricas" é permitido).
- Não fazer voz, SRT, 1080p, master, entrega, commit, branch, push.
