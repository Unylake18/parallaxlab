# yt_0036 · CÁLCULO III · EP. 11 · Jacobiano e mudança de variáveis
## Avaliação do preview v1 + HANDOFF v2 (preview com papel na tela inteira, álgebra construída e as correções de quadro)

Data: 2026-11-15. Preview avaliado: `yt_0036_preview_v1_540p15.mp4` (20:20, silencioso). Vi o vídeo inteiro em quadros a cada 4 s, cerca de 60 quadros em resolução cheia e os relatórios de QA do v1. Os degraus novos da conta foram conferidos no sympy: `verificacao/verifica_yt0036_v2_degraus.py`, 26/26 True.

---

## Parte A · Avaliação (resumo para o Kaio)

**Veredito: v2 de preview, não handoff final.** A estrutura, o 3D, as cores e a ordem das ideias funcionam. O que falta é a tela acompanhar a fala em quatro frentes: fundo, sobreposições, MF-Tools e conta.

**O que está bom:**
- A sequência régua → linear → curva → teorema → trapézio fica clara.
- O pouso do 3D no B4-2 tem ≤ 1 px de erro.
- O losango que "vira de costas" (B3-3) e a tabela 1,44 → 1,02 (B4-3) são os melhores momentos.
- O gancho de polares (S2) já está pronto para o EP. 12.

### A.1 O fundo: qual era o critério

O padrão da série (`docs/padrao_video_longo.md`, seção "Série Cálculo I–IV", item 3, de 2026-11-11) diz três coisas:
- com um gráfico, a grade cobre a tela inteira;
- com dois painéis, cada um tem a sua grade "e o resto liso";
- sem gráfico, `papel()` na unidade padrão.

Na prática, o liso ganhou espaço por dois motivos:
1. **O handoff v1 deste vídeo** (escrito por mim) mandou "cartões sem gráfico: só o violeta liso" (H2, A1, S1, B8, cartão do S2). Isso contraria o próprio padrão.
2. **O render limitou cada grade ao retângulo dos eixos**, mesmo quando havia um gráfico só.

Como este módulo vive de layouts com dois planos e coluna de fórmulas, sobrou pouca área com quadradinhos. No B4-3 (8:20–9:50) e nos cartões, não há grade nenhuma.

**Critério novo, o que eu recomendo e já está no handoff: papel na tela inteira, sempre.**
- Um gráfico: a grade dele cobre os 1920 × 1080, inclusive embaixo da coluna e do canto.
- Dois planos: cada grade cobre a sua metade da tela, com a emenda vertical no meio do vão entre os painéis (embaixo da seta φ).
- Sem gráfico: `papel()` na unidade padrão (quadradinho de 30 px a 1080p).
- Exceções: o trecho 3D do B4-2 (a grade sai enquanto o 3D está na tela, regra da série) e o CTA.

Veja `yt_0036_v1_quadros_erros/F1–F3_fundo_antes_depois.jpg`. Neles, a mesma grade foi pintada nos quadros do v1 só onde o fundo aparece.

### A.2 Os 16 quadros de erro (`yt_0036_v1_quadros_erros/Q01–Q16.jpg`)

| # | Tempo v1 | Cena | O que está errado |
|---|---|---|---|
| Q01 | 0:00–0:50 | H1 | O papel x, y ocupa só o quarto direito; a metade esquerda fica vazia por ~50 s. Em 0:00 a tela está quase preta. |
| Q02 | 2:32 | B1-1 | O glyph map do C1 escreve `· 2 dt` em cima do `∫₀¹ … t dt` novo. |
| Q03 | 3:56 | B2-1 | `Δu` colado em `v₀ CONSTANTE`; `u₀ CONSTANTE` encostado na reta tracejada. |
| Q04 | 5:00 | B3-1 | `(2, 1)` sobre a ponta da seta e a quina; a linha da CAIXA termina a ~40 px da borda. Os pedaços mostram só `1`, `3/2`, sem os catetos. |
| Q05 | 5:32 | B3-2 | O cancelamento deixa buracos e um `+` solto: `= +ad + bc + bd   − bd − 2bc`. |
| Q06 | 5:48 | B3-2 | As placas `5 Δu Δv` ficam sobre as linhas da malha. |
| Q07 | 6:50 e 1:20 | B4-1, H2 | Tracinhos brancos em cada linha da malha rosa (artefato). |
| Q08 | 8:24–9:00 | B4-3 | O det i j k fica borrado (o contorno da caneta não sai) e é o único objeto na tela por ~40 s. |
| Q09 | 10:24 | B5-1 | Voo em bolo: blocos borrados de `B_ij`, `Δu`, `Δv` passando por cima do eixo e da linha ①. |
| Q10 | 11:08, 11:52 | B5-2 | Seis molduras vazias antes dos gatilhos. A miniatura 6 (`NA BORDA, PODE`) não é a hipótese 6 (`f INTEGRÁVEL`). As miniaturas 2 e 6 são retângulos que não dizem nada. |
| Q11 | 12:40 | B5-3 | Quadrado e caixa `NA J•` soltos no canto; `J = 2u = 0` cruzando o eixo v; `∫₀¹∫₋₁¹ 2\|u\| du dv = 2` sem degraus. |
| Q12 | 15:00, 15:24 | B6-2 | A faixa de baixo mostra uma linha por vez e apaga a anterior; `y = 0` em cima do eixo; `x − y = 1` e `(0, −2)` batem nos tiques. |
| Q13 | 15:44, 16:08 | B6-3 | A integral é montada em bolo (o `1/2` pousa em `du dv`); o plano u, v começa em x = 0, sem margem. |
| Q14 | 16:50 | B6-4 | O `3` cai numa meia célula; a terceira célula é ½ + ½. |
| Q15 | 17:48, 18:16 | B7 | A borda `x + y = 1` aparece duas vezes, deslocada. Falta o plano u, v da região. A conta pula `[2v]₁²`. |
| Q16 | 18:24, 19:04, 20:04 | B8, S1, S2 | As molduras dos cartões nascem vazias e ficam assim por segundos. |

**Por que o QA deu zero:**
- O R5 não amostrou objetos em voo nem a meio da escrita (Q02, Q09, Q13).
- Não existe teste de moldura vazia (Q10, Q16).
- O teste de palco vazio usa 300 px de tinta, e o det borrado do Q08 passa.

### A.3 MF-Tools, didática e conta

- **MF-Tools:**
  - Os 64 passos de glyph map estão concentrados no H1, B1 e B3.
  - Do B4 em diante, quase toda linha derivada nasce a caneta, inteira, embaixo da anterior, sem mostrar o que virou o quê.
  - O §4 lista dez mapas novos (meta: ≥ 100 passos) e uma regra: linha que nasce da de cima vem por mapa, nunca por caneta.
- **Conta pulada:** parte disso estava no meu handoff v1.
  - `[ … ]₀¹ = 4/3 + 4v²` sem G(1) − G(0).
  - O J em M sem a substituição.
  - A dobra sem as derivadas.
  - `sen(−v)` sem a identidade.
  - `[2v]₁²` pulado.
  - O §3 reescreve essas linhas, e a **narração v1.1** lê cada degrau novo: +226 palavras, ≈ 21:32.
- **Didática:**
  - Fórmulas pequenas: o dígito `2` das colunas mede ~18 px a 1080p.
  - O chip `|J| = 1/2` fica na tela do B3-3 ao B6 (≈ 8 min), enquanto as cenas falam de outros J (4u² + 4v², 2u).
  - O B4-3 constrói o determinante sem figura.
  - O B7 não mostra a região nova.
  - Nas miniaturas do teorema, duas não ilustram nada.
  - O §6 trata cada ponto, e a dobra ganha uma conferência curta: com a metade da direita, u = 0 vira borda e o teorema vale (área 1).

**O que vai no zip:**
- este handoff;
- a narração v1.1;
- os 16 quadros de erro + 3 de fundo + a folha;
- o script sympy dos degraus;
- de novo, o pacote do v1: o handoff v1, a proposta v2 e os quadros-alvo, porque o Claude Code não enxerga esta pasta.

---

## Parte B · HANDOFF v2 (para o Claude Code)

### 0. Escopo e entregas

**Escopo:** preview v2 do vídeo inteiro, em 540p15, silencioso, na mesma unidade e no mesmo worktree do v1. Não gerar voz, SRT, master, 1080p nem entrega. Não fazer commit nem push.

**O que vale:**
- O `yt_0036_handoff_v1.md` (no zip) continua valendo em tudo o que este documento não muda.
- Onde os dois divergirem, vale este.
- Os quadros-alvo do v1 continuam valendo para o desenho, **com o papel na tela inteira** (§1) e as fontes maiores (§6.1).

**Entregas:**
1. `renders/v2/yt_0036_preview_v2_540p15.mp4`, com a duração da **narração v1.1** (`yt_0036_narracao_v1_1.md`, deste zip; copie para a unidade). A duração esperada é ≈ 21:32, com `duracoes_estimadas.json` atualizado.
2. `renders/v2/qa/correcoes_v2.jpg`: cada quadro Q01–Q16 e F1–F3 do v1 ao lado do still do v2 no mesmo ponto da fala.
3. `renders/v2/qa/comparacao_v2.jpg`: render × alvo nos 16 gatilhos dos alvos.
4. Os relatórios do v1 com sufixo `_v2`, mais os novos do §7: `grade_na_tela_v2.txt`, `moldura_vazia_v2.txt`, `tamanho_v2.txt`, `linha_derivada_v2.txt` e `margem_v2.txt`.
5. A mudança de doc do §1.4, que é a única edição fora da unidade.

### 1. Fundo: papel na tela inteira

**1.1 A regra.** Toda cena tem a grade `papel(…)` cobrindo os 1920 × 1080. Isso inclui o vão entre os painéis, a área embaixo da coluna de fórmulas, embaixo do canto e embaixo do logo. A grade continua parada, com a cor `#2B2558`, traço 1,2 e `z_index` −10, e sem placa escura atrás da coluna. O único fundo liso fica:
- no trecho 3D do B4-2 (a grade sai em fade enquanto o 3D está na tela e volta no pouso, regra da série);
- no CTA padrão.

**1.2 Como chamar.**
- **Um gráfico na cena:** `papel(ax)` sem `area=`. O padrão do `papel.py` já cobre o quadro inteiro.
- **Dois planos (layout B):**
  - `papel(ax_uv, area=…)` cobre de x = 0 até a emenda, na altura toda.
  - `papel(ax_xy, area=…)` cobre da emenda até x = 1920.
  - A **emenda** é vertical, no meio do vão entre as caixas dos dois painéis (eixos, setas e rótulos incluídos), embaixo da seta φ. Calcule por cena a partir das caixas reais, por exemplo H1/B6-2 ≈ 820 px a 1080p (é a emenda do quadro F2), e reporte o x usado em cada cena.
  - Converta o x da emenda para unidades de cada gráfico com `ax.p2c`. Não desenhe traço de divisória: a emenda é só onde uma grade termina e a outra começa.
- **Sem gráfico** (B4-3 antes das miniaturas, B5-2, B8, S1, H2 fora da célula, A1, cartão do S2): `papel()`, unidade padrão (1 u = 120 px, passo 0,25 = 30 px), origem no centro.
- **B4-2 zoom:** `papel(ax_zoom, passo=0.05)` na tela inteira, como o alvo 09.

**1.3 Quando os planos se mexem.** A grade pertence ao grupo do plano durante o movimento (anda e escala junto). Logo depois, ela faz crossfade de ≤ 0,4 s para a grade de tela inteira da posição nova. Nenhum trecho de liso maior que 0,5 s fora das exceções do §1.1.

**1.4 Doc.** Em `docs/padrao_video_longo.md`, seção "Série Cálculo I–IV", item 3:
- troque a frase `Dois painéis com escalas diferentes: papel(ax1, area=...) e papel(ax2, area=...) (área em unidades de cada gráfico), um por painel, e o resto liso.` por `Dois painéis com escalas diferentes: papel(ax1, area=...) e papel(ax2, area=...), cada um cobrindo a sua metade da tela, com a emenda vertical no meio do vão entre os painéis. A grade cobre sempre a tela inteira (inclusive sob colunas de fórmulas, canto e cartões); só o trecho 3D e o CTA ficam lisos (Kaio, 2026-11-15).`;
- acrescente no fim do item: `Cartão sem gráfico também leva papel(): o liso não é o padrão de nenhuma cena 2D.`

Não mexa em `assets/calculo/papel.py`: o `area=` já basta.

**1.5 Aceite.** `grade_na_tela_v2.txt` (§7) com 100% das amostras ≥ 95% de cobertura fora das exceções.

### 2. Correções por quadro (Q01–Q16)

Cada item traz o tempo do v1, a correção e o aceite. A **margem** vale para todos: nada (texto, eixo, rótulo, seta) a menos de 48 px da borda do quadro a 1080p, exceto o canto e o logo.

**Q01 · H1 (0:00–0:50).**
- O trapézio entra grande e centrado: papel x, y em `vista(700, 280, 260)`, de modo que o centro (1, −1) da caixa do trapézio fica em (960, 540), com o papel na tela inteira.
- Ele já está desenhando no quadro 0, sem tela escura no começo.
- A integral a caneta fica na faixa de baixo (y ≈ 985), centrada.
- As tiras, as placas `TRAVA`, os acendimentos do expoente e as duas famílias de retas acontecem nesse tamanho.
- No gatilho "o trapézio fica reto", **um movimento só** leva o papel x, y para `vista(1180, 330, 175)` enquanto o plano u, v nasce à esquerda em `vista(400, 640, 120)`, e o trapézio voa para ele (o voo do v1).
- A integral desliza para a posição do v1 no mesmo movimento.
- **Aceite:** até o voo, a caixa do papel x, y tem ≥ 520 px de lado.

**Q02 · B1-1 C1 linha 3 (2:32).**
- A linha 3 do C1 vira três linhas alinhadas no `=`:
  - `∫₀² x dx = ∫₀¹ (2t) · 2 dt`
  - `= 4 ∫₀¹ t dt`
  - `= 4 [t²/2]₀¹ = 4 · (1/2 − 0) = 2 ✓`
- Cada uma vem da de cima por glyph map, com os dois `2` acendendo juntos e virando o `4`.
- Nenhum glifo pousa onde já existe outro.
- **Aceite:** R5 durante a animação = 0 (§7).

**Q03 · B2-1 (3:56).**
- `Δu` fica centrado embaixo da aresta de baixo da célula, a 16 px dela.
- `Δv` fica à direita da aresta da direita, também a 16 px.
- `v₀ CONSTANTE` vai para a ponta direita da reta tracejada, depois da caixa da célula, com ≥ 24 px de folga do `Δu`.
- `u₀ CONSTANTE` fica 12 px acima do topo da reta, à direita dela.

**Q04 · B3-1 (5:00).**
- `(2, 1)` e `(1, 3)` ficam fora da caixa 3 × 4, do lado de fora da ponta da seta, com placa e 14 px de folga.
- A coluna começa em x = 1400 e termina antes de x = 1872. Se não couber, a linha da CAIXA quebra no segundo `=`.
- Os seis pedaços mostram a origem antes do valor (forma O2), por exemplo `2 · 1 / 2` escrito no triângulo, que vira `1` por glyph map. Ver C2 no §3.

**Q05 · B3-2 (5:32).**
- Linha 2 inteira, como no C3: `= ac + ad + bc + bd − ac − bd − 2bc`.
- Os pares `ac`/`−ac` acendem na mesma cor e somem juntos; depois `bd`/`−bd`.
- Um glyph map **fecha os buracos** e escreve a linha 3, `= ad + bc − 2bc`.
- Outro mapa faz `bc − 2bc` virar `−bc`: `= ad − bc`.
- Nunca fica um `+` no começo da linha, nem um buraco maior que um espaço.

**Q06 · B3-2 (5:48).** As placas `5 Δu Δv` ficam centradas nas células, com fonte que caiba com ≥ 8 px de folga de cada linha da malha. Se não couber, marque só duas células e escreva o selo `FATOR CONSTANTE`.

**Q07 · B4-1 e H2 (6:50, 1:20).**
- Os tracinhos brancos curtos em cada linha da malha rosa saem.
- A malha é **uma** linha `#FFB3BC` por divisa, sem segmento sobreposto nem cap de outra cor.
- Procure uma segunda malha, ou os tiques dos eixos, desenhados por cima da chapa.
- **Aceite:** recorte de 200 % sem pontos brancos sobre a chapa.

**Q08 · B4-3 (8:20–9:00).** É a correção didática principal; ver §6.2.
- O det 3 × 3 termina a caneta com `stroke_width = 0` e preenchimento na cor, igual às outras linhas: o contorno da caneta não fica.
- Enquanto o C6 é construído, o palco à direita mostra o paralelogramo do B4-2 (vista de cima, alvo 09 reduzido) com as duas setas e as pernas que geram x_u, y_u, x_v e y_v.
- **Aceite:** palco vazio = 0 e nenhum glifo com traço > 1,2.

**Q09 · B5-1 (10:24).**
- Os voos de `R_ij → B_ij` e de `α(B_ij)` acontecem **um de cada vez**, cada um ≥ 0,6 s, por um caminho em arco **acima** da linha ①, sem cruzar o eixo u.
- Voa o **glifo**, nunca um bloco ou retângulo colorido.
- **Aceite:** R5 durante a animação = 0.

**Q10 · B5-2 (11:08–12:00).**
- Cada moldura nasce **junto** com a sua miniatura, no gatilho da hipótese, e nenhuma fica vazia na tela.
- As etiquetas seguem as hipóteses de 1 a 5. A sexta caixa vira `NOTA · NA BORDA, PODE`, sem número.
- Conteúdo de três miniaturas:
  - **2:** o retângulo com a borda acesa num traço fino brilhante e `BORDA: ÁREA 0`.
  - **5:** a célula achatada, como no v1, mais `J ≠ 0`.
  - **NOTA:** o quadrado com a aresta da esquerda em ALERTA e `J = 0 SÓ NA BORDA`.
- A hipótese 6 (f integrável) não tem miniatura; ela é sobre f, não sobre φ.
- O quadro-receita fica com ≥ 32 px de folga das miniaturas.

**Q11 · B5-3 (12:20–13:00).**
- Sai a caixa solta do canto inferior esquerdo.
- O rótulo `J = 2u = 0` vai para a direita da reta da dobra (u = 0), com placa, longe do eixo v.
- A conta é o C18 do §3, com a metade da direita no fim (§6.6).
- O selo `SOBREPOSIÇÃO: CONTOU DUAS VEZES` fica.

**Q12 · B6-2 (15:00–15:40 no v1).**
- A faixa de baixo vira uma **grade 2 × 2** que acumula: cada borda de x, y acende numa cor, e a sua imagem no plano u, v acende na mesma cor.
  - `y = 0 ⇒ u = v`
  - `x − y = 2 ⇒ v = 2`
  - `x = 0 ⇒ u = −v`
  - `x − y = 1 ⇒ v = 1`
- Depois vem a linha dos vértices e, por último, `B_uv: 1 ≤ v ≤ 2, −v ≤ u ≤ v`. Tudo fica até o fim da cena.
- `y = 0` vai 14 px acima do eixo x, à direita do vértice (2, 0).
- `x − y = 1` sai para a esquerda do tique −1, ≥ 16 px.
- `(0, −2)` fica à direita do vértice, longe do `−2`.

**Q13 · B6-3 (15:40–16:30).**
- A integral é montada por mapas, em quatro passos (ver M8 no §4):
  1. `x + y → u` e `x − y → v` no expoente.
  2. `dx dy → (1/2) du dv`: o `1/2` voa do `|J| = 1/2` do B6-1.
  3. Os limites `1`, `2` voam das arestas v = 1 e v = 2 do palco, um por vez.
  4. `−v`, `v` voam das arestas u = −v e u = v.
- Nada pousa sobre outro glifo.
- O plano u, v do B6-3, B6-4 passa para `vista(420, 700, 140)`, de modo que a aresta u = −2 fique em x = 140 e os rótulos `u = −v` não passem da margem.

**Q14 · B6-4 (16:38–17:10).**
- As células 1 e 2 acendem inteiras.
- As duas pontas (triângulos de área ½) acendem juntas com `½`. A ponta da esquerda **voa** e encaixa na da direita, formando uma célula inteira; escreve `½ + ½ = 1` e então o `3`.
- O C16 segue.

**Q15 · B7 (17:13–18:30).**
- A borda `x + y = 1` é desenhada uma vez só, sobre a aresta.
- A tela ganha o plano u, v com a região nova:
  - x, y em `vista(140, 560, 150)` à esquerda, em cima;
  - u, v em `vista(400, 980, 105)` à esquerda, embaixo;
  - a coluna fica em x = 760.
  - Respeite R6: os dois planos não se tocam.
- A região de u, v é **a mesma do trapézio do B6** (1 ≤ v ≤ 2, −v ≤ u ≤ v). Quando ela nasce, um selo GEO pequeno `A MESMA REGIÃO DO TRAPÉZIO` aparece por 3 s. É verdade: o livro só trocou u por v.
- A conta é o C17 v2 (§3).

**Q16 · B8, S1, S2.**
- Toda moldura (cartão, caixa da síntese, cartão do próximo vídeo) nasce **com** o primeiro conteúdo: a moldura desenha em ≤ 0,5 s enquanto o primeiro elemento começa.
- No B8, o segundo cartão só nasce no gatilho dele ("O jacobiano aparece…/divergente").
- No S1, cada caixa nasce no gatilho da sua frase.
- **Aceite:** `moldura_vazia_v2.txt` = 0.

### 3. CONTA INTEIRA v2 (só as linhas que mudam; o resto do §3.5 do handoff v1 fica)

Formas de origem da série:
- **O1:** primitiva com colchete → G(b) − G(a) com os valores → número.
- **O2:** geometria com as chaves no desenho.
- **O5:** valor no ponto com a conta.

Cores como no v1.

**C2 · área do paralelogramo (B3-1).** Mesmas linhas, mas cada pedaço mostra a origem no desenho antes do valor:
- os dois triângulos de catetos 2 e 1: `2 · 1 / 2` → `1`;
- os dois de catetos 1 e 3: `1 · 3 / 2` → `3/2`;
- os dois retangulinhos: `1 · 1` → `1`.

O `2` da linha `− 2 · (2 · 1)/2` voa do par de triângulos.

**C3 · com letras (B3-2)**
1. `ÁREA = (a + b)(c + d) − 2 · ac/2 − 2 · bd/2 − 2 · bc`
2. `= (a + b)(c + d) − ac − bd − 2bc` (mapa: `2 · ac/2 → ac`, o 2 de cima e o de baixo acendem e somem juntos; idem bd)
3. `= ac + ad + bc + bd − ac − bd − 2bc` (mapa do produto aberto)
4. pares `ac`/`−ac` e `bd`/`−bd` acendem e somem → `= ad + bc − 2bc` (mapa que fecha os buracos)
5. `= ad − bc = det [a b; c d]` · `2 · 3 − 1 · 1 = 6 − 1 = 5 ✓`
6. `CÉLULA Δu × Δv ⇒ ÁREA = 5 Δu Δv` · selo `FATOR CONSTANTE`

**C5 · o jacobiano do caso curvo (B4-3)**
1. `x = u² − v², y = 2uv`
2. `∂x/∂u = 2u` · `∂x/∂v = −2v` · `∂y/∂u = 2v` · `∂y/∂v = 2u` (cada derivada nasce a caneta embaixo da sua fórmula e voa para a matriz)
3. `∂(x, y)/∂(u, v) = det [2u −2v; 2v 2u]`
4. `= (2u)(2u) − (−2v)(2v)`
5. `= 4u² − (−4v²)` (o par de sinais `−(−` acende ALERTA)
6. `= 4u² + 4v²`
7. `M = (0,75; 0,5): 4 · (0,75)² + 4 · (0,5)²` (o 0,75 e o 0,5 voam da legenda `M = φ(0,75; 0,5)`)
8. `= 4 · 0,5625 + 4 · 0,25 = 2,25 + 1 = 3,25`
9. `J(0, 0) = 4 · 0² + 4 · 0² = 0` · `J(1, 1) = 4 · 1² + 4 · 1² = 8`

**C8 · área 8/3 com jacobiano (B5-4)**
1. `ÁREA = ∬_{[0,1]²} (4u² + 4v²) du dv`
2. `∫₀¹ (4u² + 4v²) du = [4u³/3 + 4v² u]_{u=0}^{u=1}`
3. `= (4/3 + 4v²) − (0 + 0) = 4/3 + 4v²`
4. `∫₀¹ (4/3 + 4v²) dv = [4v/3 + 4v³/3]₀¹`
5. `= (4/3 + 4/3) − (0 + 0) = 8/3`

**C9 linha 4 (B5-4, deitado)**
- `∫₀² (2 − y²/2) dy = [2y − y³/6]₀²`
- `= (4 − 8/6) − (0 − 0) = 4 − 4/3 = 8/3 ✓`

**C16 linha 1 (B6-4)**
- `PLANO u, v: ∫₁² (v − (−v)) dv = ∫₁² 2v dv = [v²]₁² = 2² − 1² = 4 − 1 = 3`

**C17 · Ex. 1 do livro (B7)**
1. `u = x − y, v = x + y`
2. `u + v = 2x ⇒ x = (u + v)/2` · `v − u = 2y ⇒ y = (v − u)/2`
3. `x_u = 1/2 · x_v = 1/2 · y_u = −1/2 · y_v = 1/2`
4. `J = (1/2)(1/2) − (1/2)(−1/2) = 1/4 + 1/4 = 1/2` · selo `SINAL TROCOU, MÓDULO NÃO`
5. `x + y = 1 ⇒ v = 1` · `x + y = 2 ⇒ v = 2` · `y = 0 ⇒ v = u` · `x = 0 ⇒ v = −u` · `B_uv: 1 ≤ v ≤ 2, −v ≤ u ≤ v`
6. `∫_{−v}^{v} (cos u)/(sen v) du = (1/sen v) [sen u]_{u=−v}^{u=v}`
7. `= (sen v − sen(−v)) / sen v` · ao lado: `sen(−v) = −sen v`
8. `= (sen v + sen v) / sen v = 2 sen v / sen v = 2`
9. `(1/2) ∫₁² 2 dv = (1/2) [2v]₁² = (1/2)(2 · 2 − 2 · 1) = (1/2) · 2 = 1 ✓`

**C18 · a dobra (B5-3) — nova**
1. `φ(u, v) = (u², v)` · `x_u = 2u · x_v = 0 · y_u = 0 · y_v = 1`
2. `J = det [2u 0; 0 1] = 2u · 1 − 0 · 0 = 2u`
3. `∬_{[−1,1]×[0,1]} |2u| du dv`
4. `∫₋₁¹ |2u| du = ∫₋₁⁰ (−2u) du + ∫₀¹ 2u du` (as duas metades do retângulo acendem, cada uma com a sua parte)
5. `= [−u²]₋₁⁰ + [u²]₀¹ = (0 − (−1)) + (1 − 0) = 1 + 1 = 2`
6. `∫₀¹ 2 dv = [2v]₀¹ = 2 − 0 = 2`
7. `ÁREA DA IMAGEM = 1 · 1 = 1` (BASE e ALTURA com chave no quadrado) → `2 ≠ 1` · selo `SOBREPOSIÇÃO: CONTOU DUAS VEZES`
8. **Metade da direita (nova, §6.6):** `∬_{[0,1]×[0,1]} 2u du dv = ∫₀¹ [u²]₀¹ dv = ∫₀¹ (1 − 0) dv = 1 ✓` · legenda `u = 0 É BORDA: J = 0 SÓ ALI`

Todas essas linhas estão conferidas em `verificacao/verifica_yt0036_v2_degraus.py` (26/26).

### 4. MF-Tools: mapas novos (meta ≥ 100 passos; o v1 tem 64)

**Regra nova:** uma linha cujos glifos vêm da linha de cima (começa com `=`, ou repete termos dela) nasce por `TransformByGlyphMap` a partir de uma cópia da linha de cima. Só os glifos **novos** vêm pela caneta ou pelo voo. Linha derivada escrita inteira a caneta é defeito (`linha_derivada_v2.txt`, §7).

| # | Cena | Mapa |
|---|---|---|
| M1 | B3-1 | `2 · 1 / 2 → 1`, `1 · 3 / 2 → 3/2` e `1 · 1 → 1` nos pedaços (C2); `12 − 2 − 3 − 2 → 5` fica |
| M2 | B3-2 | C3 linhas 2 → 3 → 4 → 5 (o produto aberto, os pares que somem juntos, os buracos que fecham, `bc − 2bc → −bc`) |
| M3 | B4-3 | C6: `det 3×3 → (x_u y_v − x_v y_u) k`, com a coluna dos zeros e os termos de i e j acesos e saindo, e o menor 2 × 2 acendendo antes; `→ det [x_u x_v; y_u y_v] k`, a transposta com cada linha virando coluna |
| M4 | B4-3 | C5 linhas 3 → 4 → 5 → 6 (`−(−` vira `+`) e 7 → 8 → `3,25` |
| M5 | B5-1 | ① → ②: `α(B_ij)` vira `\|J(ū, v̄)\| Δu Δv` **no lugar** e `f(x̄, ȳ)` vira `f(φ(ū, v̄))` no lugar; ② → ③: `Σ Σ → ∬_{B_uv}` e `Δu Δv → du dv` |
| M6 | B5-3 | C18 linhas 2, 4 → 5 → 6 (o `\|2u\|` se parte em duas integrais por mapa) |
| M7 | B5-4 | C8 e C9: cada colchete → G(b) − G(a) → número |
| M8 | B6-1/B6-3 | C10: `u + v = 2x ⇒ x = (u + v)/2` (o 2 atravessa e vai para baixo); idem y. C13: `x + y → u`, `x − y → v`, `dx dy → (1/2) du dv` |
| M9 | B6-3/B6-4 | C14 e C15 por mapa, e C16 (`[v²]₁² → 2² − 1² → 4 − 1 → 3`, `× 1/2 → 3/2`) |
| M10 | B7 | C17 linhas 2 → 4, 6 → 7 → 8 (`sen(−v) → −sen v`, os dois `sen v` se juntam em `2 sen v`, o par `sen v / sen v` acende e some) e 9 |

As regras do v1 continuam valendo:
- `MathTex` de string única nos dois lados;
- `auto_fade` só para o glifo que sai;
- sem `show_indices` no vídeo.

Reporte os passos por cena em `glyph_maps_v2.txt`.

### 5. Narração v1.1 (no zip)

São 10 trocas pontuais, +226 palavras: 3.840 palavras, ≈ 21:32. As outras âncoras não mudaram.

| Âncora | Trecho novo (resumo) | Gatilhos novos → tela |
|---|---|---|
| B4-3 | "u vale zero vírgula setenta e cinco… dá dois vírgula vinte e cinco… dá um. Somando, três vírgula vinte e cinco" | "zero vírgula setenta e cinco"→os valores voam de M · "dois vírgula vinte e cinco"→C5.8 · "Somando"→`3,25` |
| B4-3 | "na origem, quatro vezes zero mais quatro vezes zero, zero… no canto um, um, quatro mais quatro, oito" | "na origem"→`J(0, 0)` · "no canto um, um"→`J(1, 1)` |
| B5-3 | "As derivadas… O jacobiano é dois u vezes um, menos zero vezes zero: dois u" | "As derivadas"→C18.1 · "dois u vezes um"→C18.2 |
| B5-3 | "Na metade da direita… um. Na da esquerda… um. Somando, dois. E, em vê… dois" | "metade da direita"→metade acende + C18.4/5 · "Somando"→`= 2` · "em vê"→C18.6 |
| B5-3 | "Fica só com a metade da direita: agora u igual a zero é borda… a área certa" | "metade da direita"→a esquerda some · "é borda"→aresta u = 0 ALERTA · "a área certa"→C18.8 ✓ |
| B5-4 | "Em um, quatro terços mais quatro vê ao quadrado; em zero, zero" (×2) e "Em dois, quatro menos oito sextos; em zero, zero" | "Em um"/"Em dois"→G(b) · "em zero"→− G(a) |
| B7 | "Somando, u mais vê é dois xis… Subtraindo, vê menos u é dois ípsilon" | C17.2 |
| B7 | "Seno de menos vê é menos seno de vê… dois seno de vê" | C17.7 → C17.8 |
| B7 | "A primitiva de dois é dois vê: quatro menos dois, dois. Um meio vezes dois: um" | C17.9 |

O texto exato está em `yt_0036_narracao_v1_1.md`; a tabela de tempo por âncora está no topo do arquivo.

### 6. Didática

**6.1 Tamanho.**
- Nas colunas, o dígito `2` mede no mínimo **26 px de altura a 1080p** (no v1, ~18 px). Nas linhas-chave (definição emoldurada, teorema, resultado final), no mínimo **32 px**.
- Índices ≥ 18 px.
- Para caber, quebre a linha no `=` (alinhado), nunca encolha.
- Linha que já serviu sai ou vira chip no topo da coluna (regra da série). Nada de linha estacionada no pé da tela.
- Relatório: `tamanho_v2.txt`.

**6.2 B4-3 com figura** (Q08; regra "definição com figura").
- No palco, à direita da cadeia C6, fica o paralelogramo do B4-2 (vista de cima, como o alvo 09, escala reduzida para caber em x 900–1800).
- A seta `∂φ/∂u Δu` ganha as duas pernas tracejadas: horizontal `x_u Δu` (âmbar) e vertical `y_u Δu` (magenta). Idem a seta `∂φ/∂v Δv`.
- No gatilho "as derivadas de xis e de ípsilon em relação a u", `x_u` e `y_u` **voam das pernas** para a segunda linha do det; depois `x_v` e `y_v` para a terceira.
- O `k` da linha 2 aponta para fora da tela num pequeno símbolo ⊙ no canto do paralelogramo, sem 3D novo.
- O C5 e a tabela entram como no v1, e o paralelogramo cede lugar à célula de M que encolhe.

**6.3 O chip `|J| = 1/2`.**
- O chip sai no fim do B3-3: depois de ser mostrado, volta para dentro do `ÁREA = 1/2` e some.
- Ele **não fica** do B4 ao B5, onde as cenas falam de outros J.
- No B6-1, `|J| = 1/2` nasce da conta C11 (caneta e mapa) e ganha a moldura lima nesse momento, com o selo GEO pequeno `O MEIO DO LOSANGO` por 3 s.
- O `1/2` da integral do B6-3 voa dali.

**6.4 B5-2: miniaturas que explicam.** Ver Q10. Cada miniatura mostra o que a hipótese impede, na mesma cor da frase da narração.

**6.5 B6-2: tabela das bordas.** Ver Q12. A cor de cada borda é a mesma nos dois planos e na linha da tabela.

**6.6 B5-3: a metade da direita** (conteúdo novo, uma frase).
- Depois do `2 ≠ 1` e da frase da borda, a metade esquerda do retângulo some.
- A aresta u = 0 acende em ALERTA com `J = 0 SÓ ALI` e a imagem continua o quadrado inteiro.
- O C18.8 dá `1 ✓`.
- É a hipótese "na borda, pode" funcionando na frente do aluno.

**6.7 B7: a região nova.** Ver Q15.

### 7. QA v2

Mantém tudo do §8 do handoff v1, com estas mudanças:

1. **R5 · sobreposição** (`sobreposicoes_v2.txt`):
   - amostra a cada 0,5 s, **incluindo objetos em voo, em `TransformByGlyphMap` e a meio da escrita** (qualquer opacidade > 0,15), contra textos, linhas, eixos, arestas, setas, tiques, molduras, o canto, o logo e as arestas do 3D;
   - liste os Q02, Q09 e Q13 do v1 rodados no v2;
   - esperado: 0.
2. **GRADE NA TELA** (`grade_na_tela_v2.txt`, novo):
   - em cada amostra de 0,5 s, divida o quadro em blocos de 60 × 60 px (1080p). Conte os blocos com fundo aparente, isto é, com ≥ 20 % de pixels a ≤ 16 níveis do degradê violeta. Destes, conte os que têm ao menos uma linha de grade.
   - esperado: ≥ 95 % em todas as amostras fora do trecho 3D e do CTA.
   - liste as janelas < 95 %.
3. **MOLDURA VAZIA** (`moldura_vazia_v2.txt`, novo): todo `Rectangle`/`RoundedRectangle`/`SurroundingRectangle` sem nenhum objeto dentro por mais de 0,5 s. Esperado: 0.
4. **TAMANHO** (`tamanho_v2.txt`, novo): menor altura do dígito em cada coluna, por âncora, a 1080p. Esperado: ≥ 26 px (≥ 32 px nas linhas-chave).
5. **LINHA DERIVADA** (`linha_derivada_v2.txt`, novo): para cada linha da coluna, diga se nasceu por mapa, voo ou caneta, e a fração de glifos que já existiam na linha de cima. Esperado: nenhuma linha a caneta com > 50 % de glifos herdados.
6. **MARGEM** (`margem_v2.txt`, novo): objetos a menos de 48 px da borda, fora o canto e o logo. Esperado: 0.
7. **CONTA INTEIRA:** `conta_inteira_v2.txt` com cada degrau de C2, C3, C5, C8, C9, C16, C17 e C18 e o tempo em que aparece. Diga quais degraus a narração lê.
8. **PALCO VAZIO:** mude o limiar para "menos de 15 % dos blocos de 60 × 60 com tinta que não seja a grade", por > 3 s (o det borrado do Q08 passou no limiar de 300 px).
9. **FLASH, CANTO, ALINHAMENTO 3D, CARTÃO ≥ 8 s:** como no v1.

### 8. O que NÃO mudar

- **Cena Three.js do B4-2:** câmera, decolagem e pouso (≤ 1 px no v1).
- **O losango que vira de costas (B3-3)**, a tabela do Δ (B4-3), o gancho do S2 e o cartão.
- **Cores das grandezas**, âmbar no x, a escrita a caneta finíssima e a ordem das cenas.
- **Números do vídeo:** os do §4 do handoff v1 continuam certos.
- **O resto:** não acrescentar efeitos (partículas, brilho, sombra, câmera girando no 2D) e não mexer em `papel.py`, `template/` ou em outras unidades.

### 9. Parada

Ao terminar, pare e reporte:
- arquivos alterados (a unidade e a linha do doc do §1.4);
- verificações e renders rodados, com os resultados dos relatórios do §7;
- caminhos do preview v2, das pranchas e dos relatórios;
- pendências reais.

Não gerar voz nem 1080p. Monte o zip para avaliação como no v1: `yt0036_v2_para_gpt.zip`, com o preview, as pranchas, os relatórios e os quadros a cada 2 s.

---

## Conteúdo do zip `yt0036_handoff_v2_completo.zip`

- `yt_0036_v1_avaliacao_e_handoff_v2.md` (este arquivo)
- `yt_0036_narracao_v1_1.md`
- `yt_0036_v1_quadros_erros/`: Q01–Q16, F1–F3, `00_folha_erros.jpg`
- `verificacao/verifica_yt0036_v2_degraus.py` + `verifica_yt0036_v2_degraus_saida.txt` (26/26) e `verifica_calc3_34t1_sympy.py` + `verifica_calc3_34t1_saida.txt` (41/41)
- `v1/`: `yt_0036_handoff_v1.md`, `yt_0036_narracao_v1.md`, `calculo3_34t1_jacobiano_mudanca_variaveis_proposta_v2.md` e `yt_0036_quadros_alvo_v1/` (alvos, `sb36.html`, `c3d36.html` e o kit do Three.js)
