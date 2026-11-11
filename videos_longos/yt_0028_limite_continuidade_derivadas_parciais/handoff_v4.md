# yt_0028 · CÁLCULO III · EP. 03 · Limite, continuidade e derivadas parciais
# Avaliação do preview v3 e HANDOFF v4 (fundo violeta + grade que nasce dos eixos)

Data: 2026-11-11. Base: preview v3 (`yt_0028_preview_v3_540p15.mp4`, 15:19) e o QA que veio junto.

---

# PARTE 1 · AVALIAÇÃO (para o Kaio)

## 1.1 Veredito

A v3 cumpriu o handoff:
- os 37 alvos foram reproduzidos (diferença de 4 a 7 em 255);
- R5 (sobreposição), R7 (seta na chapa) e R8 (chapa vazia): **zero ocorrências**;
- as chapas caem a 0 px das linhas grossas;
- os trechos parados caíram de 7 acima de 6 s para **3, todos justificados** (49 trechos acima de 3 s, contra 51).

O que sobrou, vendo o vídeo inteiro e os stills:

1. **O fundo vai mudar.** Você decidiu o violeta liso com a grade que nasce dos eixos. Isso tira o milimetrado em PNG, e a minha solução da v3 (chapas e zonas alinhadas às linhas grossas) perde o sentido. A v4 refaz o alinhamento no sistema novo.
2. **Telas vazias nas trocas de layout** (a fala já passou para a próxima ideia, mas o desenho antigo saiu e o novo ainda não entrou):

   | Tempo (v3) | Troca | Vazio |
   |---|---|---|
   | 1:15–1:20 | A → B1-1 | ~4 s só com o canto |
   | 6:50–6:55 | B3-2 → B3-3 | ~5 s |
   | 9:08–9:15 | B4-4 → B5-1 | ~3 s |
   | 9:22–9:30 | B5-1 → B5-2 | ~3 s |
   | 9:48–9:55 | B5-2 → B5-3 | ~3 s |
   | 10:48–10:55 | B5-4 → B5-5 | chapas vazias com os nomes, ~2 s |
   | 12:22–12:34 | B6-7 → B7-1 | ~6 s (só o J) |

   A regra R8 só olhava chapa vazia, então não pegou. A v4 troca por uma regra de transição (R10).
3. **O gráfico "erro ÷ passo" (alvo 22) engana.** Os dois painéis usam escalas diferentes: a seta verde do nosso campo (0,33) aparece mais alta que a vermelha do encrenqueiro (2) só porque a escala é outra. Na v4 vira **um gráfico só**, com as duas curvas na mesma escala.
4. **Detalhes de leitura** (corrigidos nos alvos v4):

   | Alvo | Problema | Correção |
   |---|---|---|
   | 05 | o rótulo P fica cortado pelos círculos tracejados | vai para o anel entre os círculos |
   | 07 | `F(X)` encosta no `\|Q − L₂\| < ε`, e o ε fica minúsculo | rótulos separados e ε maior |
   | 10 | a fórmula do K cruza a borda da chapa; "PARA 0" lê como "PARA O" | fórmula acima da chapa; escrito "ZERO" |
   | 34 | as legendas do atrito viscoso têm 22 px e caem sobre as setas | 26 px, acima do cartão |
   | todos | a placa atrás de texto era azul-escuro e fica estranha no violeta | placa `rgba(22,18,54,0.9)` |

## 1.2 O fundo novo, aplicado ao vídeo

Segui a regra do prompt de hoje: fundo violeta liso (`#18143A → #0F0C26`) e grade de quadradinhos iguais (`#2B2558`, 1,2 px), desenhada **a partir dos eixos de cada cena**. O que isso resolve:

- **Alinhamento por construção.** A grade usa a mesma origem e unidade do desenho. As setas do campo (passo 0,5 u) ficam em cima dos nós da grade (passo 0,25 u).
- **Borda do painel também alinhada.** Escolhi os painéis e as escalas para que cada painel tenha um número inteiro de quadradinhos nas duas direções. Assim a grade termina exatamente na moldura, sem meio quadradinho.
- **Menos poluição.** A grade nova é bem mais fraca que o milimetrado (violeta sobre violeta, sem linha grossa) e **só aparece dentro dos painéis e gráficos**. O resto da tela fica liso.

Deixei **duas variantes** nos quadros (mesmo layout e mesmas posições):

- **B, a recomendada (pasta principal):** painel transparente com a grade do eixo dentro. É exatamente o que o prompt de hoje manda ("dois painéis: um papel por painel, e o resto liso").
- **A (`variante_A_chapa_lisa/`):** chapa opaca `#0B0820`, sem grade dentro, só com a moldura. Ainda mais limpa; a grade só aparece nos gráficos. Fica como saída de emergência, caso o campo de setas sobre a grade ainda pareça carregado no vídeo.

A troca entre A e B é uma única chave na unidade (`FUNDO_PAINEL = "grade" | "chapa"`), então dá para você ver o preview e escolher depois, sem refazer nada.

## 1.3 O que a v4 muda

- Fundo e grade (acima), nos 37 alvos.
- Gráfico único no alvo 22 (**erro ÷ passo**): a curva do nosso campo cola no eixo e vai a zero, e a do encrenqueiro sobe como 1/passo.
- Correções de leitura (§1.1-4).
- Regra de transição R10: nenhuma tela vazia por mais de 0,8 s.
- O vídeo continua com ~15:20. A narração é **idêntica à da v3**.

## 1.4 O que fica como estava

Matemática, cores das grandezas, textos, tempos de fala, caneta, cenas novas da v3 (alvos 02, 05, 10, 13, 34) e a numeração dos 37 alvos.

---

# PARTE 2 · HANDOFF v4 (para o Claude Code)

**Fase:** só o **preview visual silencioso** do vídeo inteiro, em 960×540 a 15 fps. Não gerar voz, SRT, master, 1080p de vídeo nem entrega. Não fazer commit nem push.

Unidade: `videos_longos/yt_0028_limite_continuidade_derivadas_parciais/` (já implementada até a v3). Preserve a v3 em `renders/v3/`.

**O handoff v3 continua valendo em tudo o que este não muda** (cena a cena, gatilhos, textos, cores, caneta, regras R1–R8). Aqui entram:
- o fundo e a grade novos;
- as posições e escalas que os acompanham;
- as correções;
- uma cena trocada (alvo 22).

Vem junto (zip `yt0028_handoff_v4_completo.zip`):
- `yt_0028_quadros_alvo_v4/`: **37 quadros-alvo** 1920×1080 (variante B), `variante_A_chapa_lisa/` com os mesmos 37 na variante A, as pranchas de contato e o gerador `sb28v4.html` (Canvas + KaTeX, `?k=<chave>`; `&v=A` desenha a variante A). O gerador guarda as coordenadas exatas. O `fundo.png` do v3 **não é mais usado**.
- `verificacao/verifica_calc3_t3_sympy.py` e a saída: **63 checagens `True`** (novas: V22 e V23).

A matemática, o roteiro e os textos estão aprovados. Não rediscuta. Se encontrar inconsistência objetiva, reporte antes de mudar.

## 0. O que entregar

1. As seções alteradas e a `ficha.md` (§1).
2. O preview inteiro, `renders/v4/yt_0028_preview_v4_540p15.mp4`, na variante B (`FUNDO_PAINEL = "grade"`).
3. Stills 960×540 de **antes × depois** (v3 × v4) em 8 momentos: o gancho (alvo 01), B1-3, B2-4, B4-4, B5-3, B5-5 (o gráfico novo), B7-3 e o resumo. Sem os 37, só esses 8.
4. A prancha **render × alvo** dos 37 (`comparacao_v4.jpg` + `.txt`).
5. Os relatórios em `renders/v4/qa/`: `alinhamento_v4.txt` (§8.2), `sobreposicoes_v4.txt` (R5), `setas_na_chapa_v4.txt` (R7), `transicoes_v4.txt` (R10, novo) e `holds_v4.txt`.
6. O relatório de entrega (AGENTS.md).

## 1. Ficha (o que muda)

```
duracao_alvo: ~15,3 min (sem mudança; aguarda decisão do Kaio se passar de 15:00)
quadros_alvo: yt_0028_quadros_alvo_v4 (37)
sistema_visual: fundo violeta liso + grade que nasce dos eixos (papel.py v2); painéis com número inteiro de quadradinhos
```

## 2. Pré-requisito: `assets/calculo/papel.py` v2

Confira com `git status --short` e `grep -n "def papel" assets/calculo/papel.py`.

- **Já tem `papel(ax, area, passo)`** (aplicado pelo prompt do yt_0026 de hoje): use como está.
- **Ainda é o v1** (sem `papel(...)`): o Kaio autorizou a troca global em 2026-11-11 (prompt "fundo violeta e EP. 01"). Aplique **exatamente** o código do Anexo B em `assets/calculo/papel.py`, sem mexer em mais nada global. Não apague os PNGs antigos. Avise no relatório que o fez.

Uso na unidade: `usar_papel(self)` no início de cada cena (fundo violeta liso na câmera) e `papel(ax, area=..., passo=...)` para cada grade.

## 3. Fundo e grade (novo)

### 3.1 Cores

| Item | Valor |
|---|---|
| Fundo da câmera | degradê vertical `#18143A → #0F0C26` (do `usar_papel`) |
| Grade | `#2B2558`, traço 1,2, `z_index = -10`, parada |
| Moldura do painel | `#CDC3F0`, opacidade 0,38, 2 px |
| Placa de texto (R2) | `#161236`, opacidade 0,9 |
| Chapa da variante A | `#0B0820`, opaca |
| Canto e logo | iguais à v3 |

As cores das grandezas não mudam. Confira o contraste no violeta com stills: rot `#9C8CFF`, setas de contexto `#1A5F55`, placas do canto e do logo. Se algo sumir, ajuste só o tom da placa ou da moldura, e avise.

### 3.2 Como montar cada grade

Para cada painel, crie um `Axes` invisível com `eixos_no_papel(origem=(x_m, y_m), x_range, y_range, unidade=u_m)` e chame `papel(ax, area=(x0, x1, y0, y1), passo=...)`. Conversão do alvo (px no 1080p) para o Manim: **x_m = (x_px − 960)/135, y_m = (540 − y_px)/135, u_m = (px por unidade)/135**.

A grade tem **o mesmo passo e a mesma origem** que o desenho: tudo o que está em coordenadas do painel (`ax.c2p`) já cai nela.

### 3.3 Geometria por layout (px no 1080p)

| Layout | Painel (moldura) | Origem | Escala | Passo da grade (quadradinho) | `area` em unidades |
|---|---|---|---|---|---|
| **A** palco + coluna | 1 painel x 120–1080, y 180–900 | (600, 540) | 120 px/u | 0,25 (30 px) | (−4, 4, −3, 3) |
| **B** dois painéis, esquerdo | x 120–840, y 180–900 | (480, 540) | **144 px/u** (era 140) | 0,25 (36 px) | (−2,5, 2,5, −2,5, 2,5) |
| **B** dois painéis, direito | x 1080–1800, y 180–900 | **ver §3.4** | 144 px/u | 0,25 (36 px) | recalcule: (1080 − Ox)/144 … (1800 − Ox)/144 e (Oy − 180)/144 … (Oy − 900)/144 |
| **C** três cartões | x 120–600, 720–1200, 1320–1800; y 300–780 | centro de cada cartão, y = 540 | **60 px/u** (era 56) | **0,5** (30 px; 0,25 daria 15 px, abaixo do mínimo de 20 px) | (−4, 4, −4, 4) |
| Alvo 07 (sombras) | tela cheia | (600, 540) | 240 px/u | 0,25 (60 px) | tela cheia |
| Alvo 20 (gráficos C¹) | 2 retângulos: x 120–840 e 1080–1800, y 180–900 | (480, 540) e (1440, 540) | 120 px/u | 0,25 (30 px) | (−3, 3, −3, 3) |
| Alvo 22 (erro ÷ passo) | tela cheia | (600, 840) | 88 px/u | 0,25 (22 px) | tela cheia |
| Alvo 30 (matriz de movimentos) | tela cheia | (480, 420) | 120 px/u | 0,25 (30 px) | tela cheia |
| Alvo 31 (arestas) | tela cheia | (360, 780) | 150 px/u | 0,25 (37,5 px) | tela cheia |
| Alvo 13 (componentes, só texto) | tela cheia | (960, 540) | **135 px/u** (unidade padrão) | `papel()` sem `ax` | tela cheia |

Os painéis passam a ter 720×720 (antes eram 700×560 na v2 e 720×720 na v3): **não mudam em relação à v3**. O que muda é a escala (140 → 144, 56 → 60, 200 → 180) para o painel ter um número inteiro de quadradinhos: 720/36 = 20; 480/30 = 16; 960/30 = 32.

### 3.4 Regra da origem e tabela do painel direito

**A origem de cada painel é sempre um nó da grade** (a distância dela à moldura é um múltiplo inteiro do quadradinho). Quando o alvo antigo pedia outra posição, a origem vai para o nó mais próximo. Valores de v4 (px no 1080p, escala 144, quadradinho 36):

| Alvo | Origem do painel direito |
|---|---|
| 03, 04, 06 e 11 (desafio ε-δ) | (1260, 576) |
| 05 (ponto de acumulação) | (1440, 540) |
| 09 (seno do dobro) e 10 (parábola) | (1440, 576) |
| 14 (B4-1, corda em x) | (1260, 648) |
| 15 (B4-2, velocidade da ponta) | (1296, 684) |
| 16 (B4-3, derivada em y) | (1296, 648) |
| 19 (previsão × imagem) | (1440, 576) |
| 21 (malha, escala 180, quadradinho 45) | esquerdo (480, 540); direito (1170, 540) |

Em **todos os outros** casos de painel esquerdo, a origem é (480, 540).

O deslocamento é de até 18 px em relação aos alvos v3. As posições relativas dentro do painel (rótulos, setas) **seguem a origem**: use sempre `ax.c2p`.

### 3.5 Redes de setas e cartões

- **Redes dos painéis A e B:** passo 0,5 u. Com a escala da tabela, as setas caem **em nós da grade** (0,5 u = 2 quadradinhos).
- **Cartões (C):** a rede passa de passo 0,85/0,9 para **1,0 u**. Com 60 px/u as setas ficam a cada 60 px, em nós da grade de 30 px. O raio máximo da rede dos cartões de B7 sobe para 3,6 u (era 3,9).
- A regra **R7** continua: a seta só é desenhada se cabe inteira a ≥ 18 px da moldura.

### 3.6 Variante A (saída de emergência)

`FUNDO_PAINEL = "chapa"`: cada painel de campo vira uma chapa opaca `#0B0820` com a moldura, **sem** grade dentro. Os painéis de gráfico (alvos 07, 20, 22, 30, 31 e 13) mantêm a grade do eixo. A geometria é a mesma. Os quadros estão em `variante_A_chapa_lisa/`.

## 4. Cena a cena (só o que muda)

**Alvo NN** = quadro de `yt_0028_quadros_alvo_v4/` (±20 px na posição e ±5 % no tamanho; o mesmo texto e as mesmas cores).

Em **todos** os alvos: fundo, grade, molduras e origens do §3.

### H (alvo 01) e B1 (alvos 03 a 07)
- **Alvo 05:** o rótulo `P` vai para (0,95; −0,78) u do ponto P (entre o primeiro e o segundo círculo tracejado).
- **Alvo 07:** `F(X)` em (T₁ + 0,5; T₂ − 0,3) e o `ε` em (−0,55; 0,8) (30–32 px). O `|Q − L₂| < ε` fica onde estava, sem tocar o `F(X)`.

### B2 (alvos 08 a 10)
- **Alvo 10:** a fórmula do K sobe para y = 128, 34 px, sempre **acima** da moldura (a placa não passa de y = 170). A legenda passa a `PELAS RETAS: A PONTA VAI PARA ZERO`.

### B5 · o engano (alvos 18 a 22)
- **Alvo 22 (trocado)**, depois de "com um erro que some mais rápido que o passo". **Cena de gráfico único, sem painéis duplos.** Origem (600, 840), 88 px/u, grade de tela cheia.
  - **Eixos:** x = 16 × passo (0 a 8 u, passo de 0 a 0,5), com marcas em 2, 4 e 8 rotuladas `0,125`, `0,25` e `0,5`, e o nome `passo ‖H‖` embaixo. y de 0 a 8 u, com marcas 2, 4 e 8 e o rótulo `‖erro‖/‖H‖` (34 px).
  - **Curva verde** `#8CFFD2` (5 px): o máximo de ‖F(P + H) − F(P) − J·H‖/‖H‖ com ‖H‖ = passo, calculado ponto a ponto para passo de 0,5/60 a 0,5 (60 pontos). Passa por (2; 0,068), (4; 0,145) e (8; 0,33) e **cola no eixo**.
  - **Curva vermelha** ALERTA (5 px): y = 16/x, de x = 2 (passo 0,125, y = 8) até x = 8 (passo 0,5, y = 2). Passa por (2; 8), (4; 4) e (8; 2).
  - **Pontos** de 8 px nas duas curvas, com os valores: verde `0,07`, `0,15` e `0,33`; vermelho `8`, `4` e `2` (28 px, com placa).
  - **Gatilhos:**
    1. "dividindo o erro pelo passo": os eixos, a grade e o rótulo `‖erro‖/‖H‖`;
    2. "No nosso campo, quando o passo cai pela metade": a curva verde, da direita para a esquerda (o passo diminui), com os três pontos e o texto `NOSSO CAMPO:` / `CAI PELA METADE E VAI A ZERO` (verde, 30 e 26 px) em x = 1390;
    3. "No encrenqueiro, ela dobra": a curva vermelha, da direita para a esquerda, com os três pontos e `O ENCRENQUEIRO:` / `DOBRA E VAI A INFINITO` (vermelho);
    4. fim da frase: `‖erro‖/‖H‖ → 0 quando H → 0` (34 px, em x = 1390, y = 650) e `CLASSE C¹: O ERRO SOME` / `MAIS RÁPIDO QUE O PASSO` (GEO 26).
  - Números: V19, V20, V22 e V23.

### B7 (alvos 30 a 34)
- **Alvo 34:** as legendas vão **acima** de cada cartão, 26 px, em y = 288 (acima da moldura, que começa em y = 300): `SEM ATRITO VISCOSO` (violeta `#9C8CFF`) sobre o cartão GIRA e `ATRITO VISCOSO AQUI` (lima `#C6F26B`) sobre o DEFORMA. A moldura colorida continua 4 px.

## 5. Transições (R10, novo)

**R10:** em toda troca de layout, **nenhum quadro** com menos de um objeto além do canto e do logo por mais de **0,8 s**. Como fazer:
- o primeiro objeto do layout novo (painel com a rede de setas, ou o texto principal) **entra enquanto o antigo ainda sai**: `FadeIn` e `FadeOut` de 0,4 s no mesmo `AnimationGroup`;
- a primeira fórmula ou rótulo novo começa a ser escrito quando o painel entra, não depois.

As sete trocas que ficaram vazias na v3 (tempos aproximados):

| Troca | O que muda |
|---|---|
| A → B1-1 (1:15) | os dois painéis (com a grade) entram junto com a saída do `NESTE VÍDEO`; o campo e o canto `CHEGAR PERTO` na mesma 0,4 s |
| B3-2 → B3-3 (6:50) | os cartões só saem quando `F = (P, Q) contínuo ⟺ P e Q contínuas` começa a ser escrita |
| B4-4 → B5-1 (9:08) | o palco do B5-1 entra com o campo G enquanto o B4-4 sai |
| B5-1 → B5-2 (9:22) | os dois painéis do B5-2 entram com a rede e a malha |
| B5-2 → B5-3 (9:48) | os dois retângulos de gráfico entram **com os eixos já desenhados** |
| B5-4 → B5-5 (10:48) | o gráfico do alvo 22 entra com os eixos; nenhuma chapa vazia |
| B6-7 → B7-1 (12:22) | a primeira célula e os parênteses da matriz entram com o `J` |

`transicoes_v4.txt`: lista de cada troca de layout, com tempo de início e fim e o número de objetos visíveis em cada quadro; o limite é 0,8 s com menos de um objeto (zero ocorrências esperadas).

## 6. Narração e tempo

**A narração é idêntica à da v3** (Anexo A). O preview v3 durou 15:19 (919,5 s); a v4 fica igual (±3 s). Se passar de 15:00, avise e **não corte nada**. Não gerar voz.

## 7. O que NÃO fazer

- Nenhum 3D, partícula, lupa, laço contínuo, brilho, sombra, pulso, contorno ou transparência em seta, nem barra.
- Nenhuma grade fora dos painéis e gráficos (a tela fora deles fica lisa), e nenhuma linha grossa.
- Grade só com `papel(...)`, parada (`z_index = −10`), com `FadeIn`/`FadeOut`; nunca updater.
- Não mexer em `template/`, `docs/`, `AGENTS.md` nem nas unidades yt_0026, yt_0027 e yt_0029. O único arquivo global permitido é o `assets/calculo/papel.py` (§2), e só se ainda for o v1.
- Não citar livro nem o Atlas na tela.
- Não gerar voz, SRT, master, 1080p de vídeo nem entrega. Não fazer commit nem push.

## 8. QA do preview (obrigatório)

1. **Render × alvo (37)** a 960×540 (tolerância de 10 px nessa escala), em `comparacao_v4.jpg` + `.txt`. Compare com a variante B.
2. **Alinhamento (`alinhamento_v4.txt`)**, medido no pixel em stills 1080p dos 37 alvos:
   - em cada painel com grade, a **moldura cai numa linha da grade** nos 4 lados (resíduo ≤ 1 px);
   - a **origem do painel é um nó** da grade;
   - em cada rede de setas, o centro de cada seta cai num nó (resíduo ≤ 1 px);
   - nos alvos 07, 20, 22, 30 e 31, as linhas dos eixos e as bordas das faixas ficam em cima das linhas da grade (resíduo ≤ 1 px).
3. **R5 · sobreposição** em cada gatilho, medindo a seta inteira → `sobreposicoes_v4.txt`.
4. **R7 · seta na chapa**, quadro a quadro → `setas_na_chapa_v4.txt` (zero esperado). Acrescente: **nenhum texto, rótulo ou placa cruza a moldura** do seu painel (uma caixa de texto ou está toda dentro ou toda fora).
5. **R10 · transições** → `transicoes_v4.txt` (zero esperado).
6. **Flash por quadro = 0:** nenhuma fórmula aparece inteira antes da caneta.
7. **Holds:** `holds_v4.txt` com motivo para cada trecho > 3 s e nenhum > 6 s sem justificativa. Exceções já aceitas: B6-2, B7-5 (TAMBÉM VALE) e o resumo S.
8. **Números:** os valores do alvo 22 (verde 0,07/0,15/0,33; vermelho 8/4/2) na tela, com vírgula decimal.

## 9. Parada

Entregue o preview v4, as pranchas (`comparacao_v4`, antes × depois de 8 momentos), os cinco relatórios de QA e o relatório de entrega. Pare e não inicie voz nem 1080p de vídeo.

---

## Anexo A · Narração canônica

**Idêntica à do handoff v3** (`yt_0028_v2_avaliacao_e_handoff_v3.md`, Anexo A), com as quatro frases novas dela. Está repetida abaixo para este documento ficar autocontido.

### H · O quadradinho que deforma

[curious] Lembra do campo que fechou o episódio passado? A componente horizontal é a própria coordenada horizontal, e a vertical é menos a coordenada vertical. Coloca um quadradinho de fluido no meio e faz as contas que a gente já conhece. O rotacional dá zero, em todo ponto: nenhuma rodinha gira. O divergente também dá zero: nenhum pedacinho muda de área.

[thoughtful] Então, pelas duas medidas, não acontece nada. Só que agora deixa o fluido andar… e o quadradinho estica para os lados e achata na vertical. A área continua a mesma, e ele não girou nem um grau. Mas virou outra coisa.

[curious] Então tem alguma coisa nesse campo que o rotacional e o divergente não enxergam. Que número mede isso? E de onde ele sai? A resposta está nas derivadas parciais do campo. Só que, para usar essas derivadas com segurança, a gente precisa começar pelo chão: o que quer dizer chegar perto de um ponto.

### A · Bem-vindos

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab. Hoje são três ideias que se apoiam uma na outra: limite, continuidade e derivadas parciais de um campo vetorial. E, no fim, a gente vai juntar tudo numa tabela de quatro números que mostra, bem de perto, como o campo muda em volta de um ponto.

### B1 · Chegar perto

[thoughtful] Vamos usar duas telas. Na da esquerda está o campo, e é ali que você anda: tem um ponto fixo, e você vai se aproximando dele. Na da direita, eu trago cada seta para a mesma origem, para comparar só onde a ponta dela chega.

[curious] Conforme você chega perto do ponto, a ponta da seta vai chegando perto de uma seta-alvo. Essa seta-alvo é a candidata a limite. Os dois números de baixo contam a história: a distância até o ponto encolhe, e a distância da ponta até o alvo encolhe junto. Só que "encolhe junto" ainda é vago. Então a definição vira um desafio.

[thoughtful] Primeiro, alguém escolhe uma tolerância na chegada: um disquinho de raio épsilon em volta da ponta do alvo. Qualquer épsilon pode ser escolhido, por isso a definição começa com "para todo épsilon". Depois é a sua vez: você responde com um disquinho de raio delta em volta do ponto. E olha o que acontece do outro lado: cada ponto do seu disco manda a ponta da seta para algum lugar, e todas essas pontas juntas formam uma mancha. A pergunta é uma só: a mancha cabe no disco épsilon?

[curious] Com delta igual a zero vírgula sete, não cabe: um monte de pontas escapa. Diminui o delta… e a mancha encolhe junto. Em zero vírgula quatro um, ela fica inteira por dentro. Achou: é isso que "existe delta" quer dizer. Se o desafio aperta para meio, você aperta para zero vírgula dois um. Para um quarto, zero vírgula um zero. O delta depende do épsilon, e o limite existe quando você sempre consegue responder.

[thoughtful] E tem um detalhe no seu disco: o próprio ponto fica de fora. É o "maior que zero" da definição. O limite só olha para quem está chegando, nunca para o que acontece em cima do ponto. Aliás, o ponto nem precisa estar no domínio: basta ter pontos do domínio tão perto dele quanto você quiser. O nome disso é ponto de acumulação. Já um ponto do domínio sozinho, sem vizinhos, não serve: ninguém chega perto dele. Agora sim, escrito: a seta-alvo é o limite quando, para todo épsilon positivo, existe um delta positivo tal que, para todo ponto do domínio a uma distância maior que zero e menor que delta, a seta fica a menos de épsilon do alvo. A metade da esquerda fala de onde você anda. A da direita, de onde a seta chega.

[curious] E tem um atalho. Se a ponta está no disco épsilon, as duas sombras dela, a horizontal e a vertical, ficam a menos de épsilon das sombras do alvo. E o contrário também vale: se as duas sombras estão perto, a ponta cai num quadrado, que cabe num disco só um pouquinho maior. Então o limite de um campo existe exatamente quando o limite de cada componente existe, e aí é o limite de funções de várias variáveis que você já conhece.

### B2 · Quando o limite não existe

[curious] Agora um campo encrenqueiro. Todas as setas são horizontais. Nos eixos, não tem seta nenhuma; nas diagonais, as setas têm tamanho um: numa delas apontam para a direita, na outra, para a esquerda.

[thoughtful] Vem andando até a origem pelo eixo horizontal: a seta é zero o caminho todo. Pela diagonal de subida: um, para a direita. Pela outra: um, para a esquerda. Numa reta qualquer pela origem, o campo vale o dobro da inclinação, dividido por um mais a inclinação ao quadrado. Muda a reta, muda o valor.

[curious] E dá para ver isso de um jeito mais bonito. Em coordenadas polares, a componente horizontal vira o seno do dobro do ângulo. O campo não depende da distância, só da direção. Então dá uma volta num círculo minúsculo em volta da origem: a ponta da seta varre o segmento inteiro, de menos um até um. E isso acontece em qualquer círculo, por menor que seja.

[thoughtful, emphatic] Agora joga o desafio. Escolhe um alvo qualquer e um épsilon de meio. O disco tem largura um, e o segmento tem largura dois: não cabe, seja qual for o alvo. Então não existe limite na origem. E fica um cuidado: dois caminhos com valores diferentes provam que o limite não existe. Mas todas as retas darem o mesmo valor ainda não provam que ele existe, porque dá para chegar por uma curva. Olha este campo: por qualquer reta, a seta vai para zero. Mas, pela parábola, ela fica em meio o caminho todo. Também não tem limite.

### B3 · Continuidade

[thoughtful] Agora a continuidade. A definição tem três pedaços, e cada um pode falhar. Um: o ponto está no domínio, então a seta do ponto existe. Dois: o limite ali existe. Três: o limite é igual à própria seta do ponto. Na figura, é o mesmo desafio de antes, só que agora o disco épsilon fica em volta da ponta da seta do próprio ponto. No nosso campo, a mancha cabe. Contínuo.

[curious] Agora, três jeitos de dar errado. No campo elétrico de uma carga, o ponto da carga nem está no domínio. Falha o primeiro pedaço, e a pergunta nem se faz; em todo o resto, ele é contínuo. No campo encrenqueiro, definido como zero na origem, a seta existe, mas o limite não: falha o segundo. E neste aqui todas as setas apontam para a direita, menos a do centro, que aponta para cima. O limite existe e é a seta para a direita, mas a seta do ponto é outra. Falha o terceiro: um salto bem em cima do ponto.

[thoughtful] E, de novo, por componentes: o campo é contínuo exatamente quando cada componente é contínua. Por isso quase todo campo que vem de fórmula é contínuo onde está definido: somas, produtos, quocientes com denominador diferente de zero e composições de funções contínuas continuam contínuas. A primeira componente do nosso campo é uma constante mais senos: contínua. E o campo da carga é um quociente: contínuo em todo lugar, menos em cima da carga.

### B4 · Derivada parcial de um campo

[thoughtful] Agora sim: medir como a seta muda. Fica no ponto e anda só na horizontal, um passo. A seta muda de uma para outra, e a diferença entre as duas é um vetor, que liga a ponta velha à ponta nova. Divide esse vetor pelo tamanho do passo e encolhe o passo. Esse limite é a derivada parcial do campo na direção horizontal.

[curious] Com passo um, o quociente vale zero vírgula oito quatro e dois vírgula um quatro. Com meio, zero vírgula nove seis e dois vírgula um seis. Com passo cada vez menor, ele vai chegando em um e dois. E olha a tela da chegada: andando na horizontal, a ponta da seta desenha uma curva. A diferença é uma corda dessa curva, e, dividida pelo passo, ela vira a seta tangente. Então a derivada parcial é a velocidade da ponta, quando você anda na horizontal com velocidade um.

[thoughtful] E essa velocidade tem duas sombras. A horizontal diz quanto muda a componente horizontal do campo: um. A vertical diz quanto muda a componente vertical: dois. Por isso a conta é por componentes: a derivada do campo é a derivada de cada componente.

[curious] Agora na vertical. Andando para cima, a ponta anda num círculo, e o quociente vai chegando em menos um e zero: a derivada na direção vertical aponta para a esquerda, tangente ao círculo.

[thoughtful, emphatic] Então a derivada parcial de um campo não é um número: é um vetor, que diz como a seta muda quando você anda numa direção. Na conta, a derivada na horizontal dá cosseno e dois cossenos mais seno, da coordenada horizontal; no ponto, um e dois. A derivada na vertical dá menos cosseno e seno da coordenada vertical; no ponto, menos um e zero. A conta bate com o desenho. E, num campo no espaço, aparece uma terceira, na direção da profundidade, com a mesma ideia.

### B5 · O engano

[curious] Só que tem uma armadilha. Volta no campo encrenqueiro e calcula as derivadas parciais na origem. Pelo eixo horizontal, a seta é zero o tempo todo: derivada zero. Pelo vertical, mesma coisa. As duas existem, e as duas são zero.

[thoughtful] Se você confiasse só nelas, ia prever que, perto da origem, tudo vai para perto do zero: um quadradinho em volta da origem iria parar num ponto só. Mas olha a imagem de verdade: a ponta varre o segmento inteiro, de menos um até um. A previsão errou feio. As parciais só olham duas retas, e esse campo esconde tudo nas diagonais. Ele nem é contínuo na origem.

[thoughtful, emphatic] O que faltou? Olha as próprias derivadas, andando pelo eixo vertical. No nosso campo, a derivada na horizontal vale um o caminho todo, sem salto nenhum. No encrenqueiro, ela vale dois dividido pela altura: explode perto da origem, e na origem vale zero. Essa é a condição de classe cê um: as derivadas parciais existem e são contínuas. Classe cê erre é o mesmo, até as derivadas de ordem erre.

[curious] E com ela vem a promessa. Pega uma malhinha em volta do ponto e manda para a tela da chegada. As linhas horizontais viram curvas na direção da derivada horizontal, e as verticais, curvas na direção da derivada vertical. Cada quadradinho da malha vira quase um paralelogramo, com lados de passo vezes derivada. Escrito: a seta num ponto vizinho é a seta do ponto, mais o passo horizontal vezes a derivada na horizontal, mais o passo vertical vezes a derivada na vertical, com um erro que some mais rápido que o passo. O nosso campo, feito de senos e cossenos, é cê um. O encrenqueiro, não. E dá para ver isso dividindo o erro pelo passo. No nosso campo, quando o passo cai pela metade, essa conta cai pela metade também, e vai para zero. No encrenqueiro, ela dobra.

### B6 · A tabela

[curious] Então vamos usar isso. Pega o campo da aula e chega dez vezes mais perto do ponto: essa janelinha vira o palco inteiro. De perto, todas as setas ficam parecidas com a seta do centro. Cada uma é a seta do centro, mais um restinho. Tira a seta do centro de todas… e sobra só a mudança. Olha que campo arrumadinho.

[thoughtful] Bem de perto, essa mudança é escrita com as duas derivadas. Então coloca as duas lado a lado, como colunas: a derivada na horizontal na primeira, a derivada na vertical na segunda. Fica uma tabela de quatro números, com as derivadas das duas componentes nas duas direções. Ela tem nome: matriz jacobiana. No nosso ponto, um e menos um em cima, dois e zero embaixo.

[curious] E ela funciona assim: um passo com uma parte horizontal e uma vertical vira a parte horizontal vezes a primeira coluna, mais a parte vertical vezes a segunda. A seta do modelo é a soma das duas.

[thoughtful] Agora coloca um quadradinho com a quina no ponto. A quina da direita é empurrada pela primeira coluna; a de cima, pela segunda. Cada coluna empurra uma aresta. Solta o fluido no modelo… e o quadradinho gira, cresce e entorta, tudo ao mesmo tempo. Tudo isso estava nos quatro números.

### B7 · Quatro números, quatro medidas

[thoughtful] E dá para separar essa bagunça, lendo cada número da tabela como um movimento de aresta. Em cima, à esquerda: quanto a aresta horizontal estica. Aqui, um. Embaixo, à esquerda: quanto ela gira. Dois. Em cima, à direita: quanto a aresta vertical tomba para o lado. Menos um, para a esquerda. Embaixo, à direita: quanto ela estica. Zero.

[curious] Agora junta. Os dois giros no mesmo sentido, somados, dão o rotacional: dois mais um, três. Os dois estiramentos somados dão o divergente: um mais zero, um. E sobram duas comparações. Estiramento horizontal menos vertical: um. Essa é a primeira deformação, quanto o pedacinho estica mais numa direção do que na outra. E a diferença entre os dois giros: dois menos um, um. Essa é a segunda, quanto o ângulo reto do quadradinho fecha, como uma tesoura.

[thoughtful, emphatic] Quatro números entram, quatro medidas saem, e nada se perde no caminho. Bem de perto e sem a seta do centro, todo campo cê um se comporta como uma mistura de quatro campos simples: um redemoinho, uma explosão e duas deformações. E isso não é só matemática: num fluido, o atrito viscoso vem da deformação. Um bloco de fluido girando inteiro, rígido, não tem atrito viscoso nenhum por dentro.

[curious] Agora volta lá no começo. No campo que esticava o quadradinho, a tabela é um e zero em cima, zero e menos um embaixo. A aresta horizontal estica, a vertical encolhe na mesma medida, e ninguém gira. Rotacional zero, divergente zero, e a primeira deformação vale dois. É tudo deformação.

[happy] E lá no episódio passado ficou um desafio: achar outro campo, que não fosse constante, com rotacional e divergente zero. Um deles é este, que troca as coordenadas de lugar. As duas arestas giram uma contra a outra: a segunda deformação vale dois, e o quadradinho vira losango. É o mesmo campo de antes, girado quarenta e cinco graus. E quem achou um de segundo grau, como o da tela, também acertou.

### S · Síntese e encerramento

[thoughtful] Resumindo: limite é ganhar o desafio do épsilon com um delta. Continuidade é o limite igual à seta do ponto, sem salto. A derivada parcial é a velocidade da ponta numa direção. E, quando essas derivadas são contínuas, a tabela delas descreve o campo bem perto do ponto: giro, área e deformação. E uma curiosidade: no espaço, a tabela tem nove números, que se separam em três de giro, um de volume e cinco de deformação.

[excited] No próximo vídeo, a gente coloca o módulo inteiro para trabalhar em exercícios: campo vetorial, rotacional, divergente, limite e derivadas parciais, tudo junto. Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual dessas quatro medidas você acha que aparece mais na física? Até a próxima!


---

## Anexo B · `assets/calculo/papel.py` (v2)

Aplicar só se o arquivo no repositório ainda for o v1 (§2). Substitua o conteúdo inteiro:

```python
"""Papel da série de longos de Cálculo I–IV, v2 (Kaio, 2026-11-11): fundo violeta liso + grade de quadradinhos que NASCE DOS EIXOS.

- Fundo da câmera: degradê violeta liso (`usar_papel(cena)`), parado, sem grade na imagem.
- Grade: `papel(ax)` desenha quadradinhos iguais (sem linha grossa) com a MESMA origem e unidade dos eixos -> alinha por construção.
  Passo padrão 0,25 da unidade do gráfico; se o quadradinho ficar < 20 px em 1080p, passa sozinho para 0,5 (e depois 1).
  `passo=` força outro valor quando o vídeo pedir. `area=(x0, x1, y0, y1)` (unidades do gráfico) limita a grade a um painel.
- Sem gráfico na cena: `papel()` usa a unidade padrão (1 u do Manim, origem no centro do quadro).
- A grade é um VGroup parado (z_index -10): entra/sai com FadeIn/FadeOut; nunca com updater.
"""
from pathlib import Path
import numpy as np
from manim import Axes, Line, VGroup, config, ORIGIN, RIGHT, UP
from PIL import Image

AQUI = Path(__file__).parent
COR_GRADE, LARG_GRADE = "#2B2558", 1.2
TOPO, BASE = "#18143A", "#0F0C26"
MIN_PX = 20


def _arq(nome="fundo_calculo_violeta_liso"):
    w, h = config.pixel_width, config.pixel_height
    p = AQUI / f"{nome}_{w}x{h}.png"
    if not p.exists():
        hx = lambda c: np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)
        v = np.linspace(0, 1, h)[:, None, None] * np.ones((1, w, 1))
        Image.fromarray((hx(TOPO) * (1 - v) + hx(BASE) * v).astype(np.uint8)).save(p)
    return p


def usar_papel(cena, arquivo=None):
    cena.camera.background_image = str(arquivo or _arq())
    cena.camera.init_background()


class _Padrao:
    """Eixos 'virtuais' da unidade padrão: 1 u do Manim, origem no centro do quadro."""
    def c2p(self, x, y):
        return ORIGIN + RIGHT * x + UP * y


def papel(ax=None, area=None, passo=None, cor=COR_GRADE, largura=LARG_GRADE):
    ax = ax or _Padrao()
    o = np.array(ax.c2p(0, 0)); ux = ax.c2p(1, 0)[0] - o[0]; uy = ax.c2p(0, 1)[1] - o[1]
    px_u = config.pixel_width / config.frame_width          # px por unidade do Manim
    if passo is None:
        passo = 0.25
        while min(abs(ux), abs(uy)) * passo * px_u * 1920 / config.pixel_width < MIN_PX and passo < 1:
            passo *= 2                                      # 0,25 -> 0,5 -> 1
    if area is None:
        fw, fh = config.frame_width / 2, config.frame_height / 2
        area = ((-fw - o[0]) / ux, (fw - o[0]) / ux, (-fh - o[1]) / uy, (fh - o[1]) / uy)
    x0, x1, y0, y1 = area
    ks = lambda a, b: np.arange(np.ceil(min(a, b) / passo - 1e-9), np.floor(max(a, b) / passo + 1e-9) + 1) * passo
    g = VGroup(*[Line(ax.c2p(x, y0), ax.c2p(x, y1)) for x in ks(x0, x1)],
               *[Line(ax.c2p(x0, y), ax.c2p(x1, y)) for y in ks(y0, y1)])
    g.set_stroke(cor, largura).set_z_index(-10)
    g.passo = passo
    return g


def eixos_no_papel(origem, x_range, y_range, unidade=1.0, unidade_y=None, **kw):
    """Mantido por compatibilidade (v1). Com a grade nascendo dos eixos, não é mais preciso encaixar; só cria e posiciona os eixos."""
    ux, uy = unidade, unidade_y or unidade
    ax = Axes(x_range=x_range, y_range=y_range, x_length=(x_range[1] - x_range[0]) * ux,
              y_length=(y_range[1] - y_range[0]) * uy, tips=False, **kw)
    ax.shift(np.array([*origem, 0][:3], float) - ax.c2p(0, 0))
    return ax
```
