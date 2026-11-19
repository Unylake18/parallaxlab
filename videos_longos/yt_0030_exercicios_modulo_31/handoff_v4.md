# yt_0030 · CÁLCULO III · EP. 04 · Exercícios do módulo 3.1 · HANDOFF v4 (CONTA INTEIRA)
**21 contas desenvolvidas, narração v3.4, voz PARCIAL (só os trechos novos, emendados no WAV v3.3), sincronização, 540p, 1080p e reentrega.** O arquivo é único e autocontido. O zip `yt0030_handoff_v4_conta_inteira.zip` traz os scripts e o texto.

2026-11-14. **Base:** a versão entregue em 2026-11-12/13:
- master `renders/yt_0030_master_final_1080p30.mp4`, 31:02,77, CRF 14;
- voz v3.3 `audio/narracao_final.wav`, 1861,76 s;
- 69 âncoras e 482 frases de sincronia.

**Pedido do Kaio (2026-11-14).** Ele quer trazer para este vídeo a regra CONTA INTEIRA que entrou no EP. 09: nenhum degrau da conta é pulado. A queixa é dele: "senti mt falta principalmente em 6:27, as partes finais das aplicações também, bastante parte do vídeo faltou um desenvolvimento algébrico". Ele quer **gerar só o complemento da voz**, sem regravar a voz inteira, e **mudar a animação**.

A Produção varreu o vídeo inteiro e achou **21 contas** com degrau pulado (C1–C21, §5). Exemplos:
- a regra da cadeia do D3, com o ∂s/∂x que não aparece e o ∂P/∂y copiado pronto;
- o ‖(−y, x)‖ = r;
- o limite com α = ½ sem a conta dos dois caminhos;
- a definição de diferenciável no D4;
- as derivadas de 1 − x²/9 e o rot em x = −3 no rio;
- a regra do produto no tempo do jato;
- i² = −1 e a conferência de Cauchy-Riemann no z²;
- o div E do fio sem conta;
- a derivada da distância no espaço.

**O que muda e o que não muda:**
- A narração v3.4 troca **20 parágrafos** e mantém os outros 49 palavra por palavra. No total são 6.956 palavras (+1.542), ≈ 39:50 a 2,91 palavras/s (a taxa medida na v3.3).
- Todo gatilho que já existe na cena continua no texto, na mesma ordem. Entram **126 gatilhos novos**. Conferido por script: 596 frases, 0 faltando, 0 fora de ordem.
- A voz nova é feita só nos **11 trechos** contíguos que mudaram. Eles são colados no WAV da v3.3 no meio das pausas entre parágrafos. O áudio dos 49 parágrafos que não mudam volta **bit a bit**: a emenda foi testada com áudio sintético e os trechos antigos saem idênticos.
- Toda a matemática nova foi conferida no SymPy (`verifica_yt0030_v34_contas.py`, **88/88 True**).

Este documento substitui o `handoff_final.md` **no que diverge**. Continuam como estão, salvo onde o §5 diz o contrário:
- paleta, canto, fundo violeta com a grade dos eixos;
- layouts A/B;
- a caneta;
- a costura de 0,4 s;
- o CRF;
- a ordem dos blocos.

---

## 0. Autorização, fases e modo de execução

**Fases explicitamente abertas pelo Kaio nesta unidade:**
- animação (§5);
- narração v3.4 (§2);
- **voz parcial pela API do ElevenLabs** (§3);
- sincronização (§4);
- 540p de conferência (§6);
- **render final 1080p** e master (§7);
- legenda `.srt` e capítulos;
- **reentrega** em `entregas/` (§8).

Ele pediu o handoff "com todas as instruções para dar tudo certo, alterações, voz e entrega": é para ir até o fim **sem** parar para preview de aprovação.

**Não abertas (não fazer):**
- publicação, capa, `commit`, `push`, `branch`, PR;
- qualquer mudança em `template/`, `assets/`, `pyproject.toml`, `uv.lock`, `AGENTS.md`, `docs/` e `videos/gerar_voz_elevenlabs.py`;
- regravar a voz inteira (só no caso da parada 3, com autorização).

**O que pode mudar:**
- a unidade `videos_longos/yt_0030_exercicios_modulo_31/`;
- `renders/` e `entregas/`, que são saída.

O registro `videos/entregas_registro.json` **não muda**: o master final mantém o mesmo nome de arquivo.

**Modo de execução:** não encerre a vez entre etapas. Espere cada render ou chamada de API na mesma vez, com comando em primeiro plano e timeout de até 10 min, ou com um laço `until` sobre o arquivo de saída. Depois siga direto para a auditoria. Mensagem de progresso não é entrega.

**Só há três paradas permitidas:**
1. A variável `ELEVENLABS_API_KEY` não existe na sessão. Peça ao Kaio. **Nunca** grave a chave em arquivo, commit, log ou relatório.
2. O WAV emendado passa de **41:30** (2.490 s). O previsto é ≈ 39:50. Reporte a duração e pare.
3. Um mesmo trecho reprova no QA da emenda (§3.4 ou §3.6) em **3 takes**. Reporte os números dos 3 e pare. A Produção decide se regrava o trecho junto com o parágrafo vizinho.

Qualquer outra dúvida: escolha a leitura mais provável, diga qual escolheu e siga.

**Ordem:**
1. §1 conferir o ponto de partida.
2. §2 instalar a narração v3.4.
3. §3 voz parcial (gerar → emendar → alinhar → QA).
4. §4 tempos da voz.
5. §5 as 21 contas, lote a lote, com 540p do lote.
6. §6 conferência 540p com voz do vídeo inteiro.
7. §7 1080p e master.
8. §8 QA final e reentrega.
9. §9 relatório.

Guarde este arquivo na unidade como `handoff_v4.md`.

---

## 1. Estado de partida (conferir antes de mexer)

1. `git status --short`: preserve o que existir.
2. Confira na unidade:
   - `narracao.md` = v3.3: 69 âncoras, 5.414 palavras (`python tempos.py`);
   - `audio/narracao_final.wav` = 1861,76 s;
   - `alinhamento_palavras.json` = 5.414 palavras, a última terminando em 1861,54 s;
   - `renders/yt_0030_master_final_1080p30.mp4` = 31:02,77.
   Se algum número não bater, pare e reporte: o zip foi feito sobre esse estado.
3. **Copie o estado v3.3 para arquivos históricos.** São cópias, não mova nada: os scripts da emenda leem estes nomes.

   | origem | cópia |
   |---|---|
   | `audio/narracao_final.wav` | `audio/narracao_v33.wav` (se já existir com esse nome, confira que é igual pelo tamanho e pelo SHA-256) |
   | `alinhamento_palavras.json` | `alinhamento_v33.json` |
   | `narracao.md` | `narracao_v33.md` |
   | `narracao_tags.md` | `narracao_tags_v33.md` |
   | `transcricao_stt.json` | `transcricao_stt_v33.json` |
   | `ancoras.json` | `ancoras_v33.json` |
   | `legenda.srt` | `legenda_v33.srt` |
   | `renders/capitulos_final.txt` | `renders/capitulos_v33.txt` |
   | `renders/yt_0030_master_final_1080p30.mp4` | `renders/v33/yt_0030_master_v33_1080p30.mp4` (esta é **mover**, para o nome final ficar livre; confira o tamanho antes e depois) |

4. Copie do zip para a unidade:
   - `trechos_v34/` (11 `.md` + `plano_trechos.json`);
   - `gerar_trechos_v34.py`, `emendar_voz.py`, `qa_emendas_v34.py`;
   - `confere_frases_v34.py`, `frases_sincronia_v34.json`;
   - `narracao_v34.md`, `narracao_tags_v34.md`;
   - a pasta `evidencias_v33/` (quadros do master v3.3 nos trechos com conta pulada: `d3a.jpg` mostra os 6:20–7:25).

   Copie para `verificacao/` da unidade (crie a pasta se não houver) `verifica_yt0030_v34_contas.py` e a saída `verifica_yt0030_v34_contas_saida.txt`.

---

## 2. Narração v3.4 (instalar antes de tudo)

### 2.1 Instalar
1. Copie `narracao_v34.md` por cima de `narracao.md`. O formato é o de sempre: 14 cabeçalhos `###` e 69 parágrafos.
2. Copie `narracao_tags_v34.md` por cima de `narracao_tags.md`. É a mesma fala, sem os cabeçalhos, com o título `## Texto corrido (para gravação)`.
3. `python tempos.py`: **69 âncoras, 6.956 palavras**. Sem o WAV novo, os tempos saem do orçamento a 3 p/s. Isso é normal até o §4.
4. `uv run --no-sync python confere_frases_v34.py`. Saída exigida:

   ```
   âncoras 69 · palavras 6956 · …
   (1) frases_sincronia_v34.json: 596 frases · faltando 0 · fora de ordem 0
   ```

   Rode também com `--cena`, ainda com o código de hoje: `(2) código da cena: 468 frases · faltando 0 · fora de ordem 0`. Isso prova que **nenhum gatilho antigo quebrou**.

   A tokenização é a da cena (`\w+` em minúsculas, **com** acento; a cena pega a **primeira** ocorrência da frase na âncora). Se faltar alguma frase, a cópia saiu errada. Não edite frase de gatilho para "fazer passar".

### 2.2 O que mudou no texto
- **Parágrafos trocados (20):** D3-2, D3-3, D3-6, D3b-2, D3b-4, D4-6, D4-7, D5-9, A1-2, A1-3, A1-5, A2-2, A2-3, A2-4, A4-2, A4-3, A4-4, A3-3, A3-4, A3-5. O texto completo está no Anexo A. O A4-1 **não** muda: só o layout dele muda (C16).
- **Tags:** só as de sempre (`[thoughtful]`, `[curious]`, `[excited]`, `[thoughtful, emphatic]`). Alguns parágrafos longos ganharam uma tag no meio, para a voz respirar.
- **Leituras novas de símbolo na fala:**
  - "esse" para `s` (a distância ao quadrado, D3-3);
  - "agá" para `h` e `H` (D4-6);
  - "tê" para `t` (D3-6);
  - "u" e "vê" para `u, v` (A2-2);
  - "pê" continua escrito "p", como na v3.3.

---

## 3. Voz parcial (ElevenLabs v4): só os 11 trechos novos

Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`, `mp3_44100_192` decodificado para WAV mono 16 bits 44,1 kHz: a mesma voz, o mesmo modelo e o mesmo formato da v3.3. Referência: `docs/roteiro_voz_elevenlabs_v4.md`.

### 3.1 Os trechos
Os parágrafos novos que ficam colados viram **um** trecho, para as pausas internas saírem naturais. Cada trecho tem menos de 4.500 caracteres, então é **uma chamada de API**. A tabela completa, com as durações esperadas, está no Anexo C.

| trecho | âncoras | vizinho antes / depois (ficam do WAV v3.3) |
|---|---|---|
| T01 | D3-2, D3-3 | D3-1 / D3-4 |
| T02 | D3-6 | D3-5 / D3-7 |
| T03 | D3b-2 | D3b-1 / D3b-3 |
| T04 | D3b-4 | D3b-3 / D3b-5 |
| T05 | D4-6, D4-7 | D4-5 / D4-8 |
| T06 | D5-9 | D5-8 / D5-10 |
| T07 | A1-2, A1-3 | A1-1 / A1-4 |
| T08 | A1-5 | A1-4 / A2-1 |
| T09 | A2-2, A2-3, A2-4 | A2-1 / A4-1 |
| T10 | A4-2, A4-3, A4-4 | A4-1 / A3-1 |
| T11 | A3-3, A3-4, A3-5 | A3-2 / A3-6 |

### 3.2 Gerar
```
uv run --no-sync python videos_longos/yt_0030_exercicios_modulo_31/gerar_trechos_v34.py --seco
uv run --no-sync python videos_longos/yt_0030_exercicios_modulo_31/gerar_trechos_v34.py
```
- `--seco` só lista os trechos. Confira: 11 trechos, 1 bloco cada.
- O script importa `blocos`, `extrair`, `sintetizar` e `decodificar_mp3` do `videos/gerar_voz_elevenlabs.py`, que **não muda**. Ele grava `audio/v34/<trecho>.wav`.
- Cada chamada leva `previous_text` e `next_text` com o parágrafo vizinho da v3.3, para a entonação casar com o que fica. Se a API recusar o contexto, o script repete sem ele e anota em `audio/log_voz_v34.txt`.
- **Um take por trecho.** Refazer um trecho:

  ```
  … gerar_trechos_v34.py --so T05 --take 2
  ```

  Isso grava `T05_…_take2.wav`. O take antigo fica.

### 3.3 Emendar
```
uv run --no-sync python videos_longos/yt_0030_exercicios_modulo_31/emendar_voz.py            [--take T05=2 …]
```
- **Entradas:** `audio/narracao_v33.wav`, `alinhamento_v33.json`, `narracao_v33.md`, `trechos_v34/plano_trechos.json` e os WAV de `audio/v34/`.
- **Saídas:** `audio/narracao_v34.wav`, `audio/emenda_v34.json`, `qa/emenda_v34.txt`.

Como a emenda é feita:
1. Para cada trecho, o script acha no alinhamento v3.3 o fim da última palavra do vizinho de antes, o começo e o fim do trecho antigo e o começo do vizinho de depois.
2. Corta o WAV velho **no meio** das duas pausas antigas.
3. O trecho novo entra com o **próprio** silêncio, aparado para a mesma meia pausa. Se o take tiver menos silêncio, a pausa fica menor, nunca maior. **Nenhum silêncio é inserido.**
4. Cruzamento de 10 ms em cada emenda. As duas pontas estão em silêncio.
5. Nível: o RMS da fala do trecho novo é igualado ao do trecho antigo que ele substitui.
6. O áudio velho é regravado na mesma escala da leitura: fora dos trechos, ele volta **bit a bit**.

**Aceite da emenda** (`qa/emenda_v34.txt`, saída 0):
- ganho aplicado ≤ ±6 dB;
- ritmo do trecho novo dentro de ±12 % do trecho antigo e entre 2,60 e 3,25 palavras/s;
- pausa antes e depois ≥ 0,12 s;
- clipping 0.

Se um trecho der FALHA, refaça **só ele** (`--so Tnn --take k`) e emende de novo com `--take Tnn=k`. Depois do 3º take reprovado do mesmo trecho: parada 3.

Duração esperada: **≈ 2.390 s ≈ 39:50** (Anexo C). Acima de 41:30: parada 2.

### 3.4 Instalar e alinhar
1. Copie `audio/narracao_v34.wav` para `audio/narracao_final.wav`. O WAV v3.3 está guardado em `audio/narracao_v33.wav`.
2. `ELEVENLABS_API_KEY` no ambiente:

   ```
   uv run --no-sync python alinhar_voz.py --stt
   ```

   Isso grava `alinhamento_palavras.json` (6.956 palavras) e `transcricao_stt.json`, a partir do `narracao_tags.md` v3.4.

### 3.5 QA da voz (`qa_voz.py`, adaptado na unidade)
- Troque o limite da parada de `1950` / "32:30" por **`2490` / "41:30"**.
- Acrescente à lista `chave` de pronúncias:

  ```python
  "agá": r"\bag[áa]\b"
  "tê": r"\bt[êe]\b"
  ```

  e confira que "esse", "u" e "vê" aparecem no STT nos trechos certos.
- O resto fica igual:
  - tag lida em voz alta = 0;
  - silêncio > 1,5 s dentro de parágrafo = 0;
  - clipping 0;
  - as pronúncias de antes (Cauchy-Riemann, Laplace, Mercator, Groenlândia, Coulomb…).

### 3.6 QA das 22 emendas
`uv run --no-sync python qa_emendas_v34.py` → `qa/emendas_v34.txt` (saída 0). Usa o alinhamento **novo**. Em cada emenda:
- pausa real entre a última palavra antes e a primeira depois: **0,12–0,60 s**;
- nível 2 s antes × 2 s depois: |Δ| ≤ **3 dB**;
- maior salto entre amostras na pausa ≤ **0,2**, ou seja, sem clique.

Em seguida, **ouça** as 22 emendas (±3 s em volta de cada uma). O tempo de cada emenda está em `qa/emendas_v34.txt`. Anote no relatório qualquer mudança audível de timbre ou de entonação. Se houver mudança clara, refaça o take do trecho (conta para a parada 3).

---

## 4. Tempos da voz (a cena segue a voz)
Regras permanentes:
- WAV contínuo;
- nunca cortar a voz por âncora nem inserir silêncio;
- atraso imagem × fala ≤ 0,2 s (`LEAD` 0,09 s).

1. `python tempos.py`: com o WAV e o alinhamento novos, o `voz_real()` já em uso monta os tempos sozinho. O `assert` de tokens tem que passar: a sequência do alinhamento é a do texto v3.4. Confira:
   - **69 âncoras**;
   - `voz` = duração do WAV;
   - a âncora D3-1 começa no mesmo tempo da v3.3 (±0,05 s), porque nada antes dela mudou.
2. `uv run --no-sync python confere_frases_v34.py` de novo, agora com os tempos reais: (1) 596/0/0.
3. A partir daqui **todos** os renders (540p e 1080p) usam esses tempos.

---

## 5. As 21 contas (C1–C21)

### 5.0 Regras que valem para as 21
Regra CONTA INTEIRA do projeto, a mesma do EP. 09:
- **Fórmula-mãe antes do número.**
- **Cada degrau é uma linha ou um glyph map.** Nada de "dá" pulando passo.
- **Cada valor voa de onde vem:** componente, célula, rótulo do desenho ou chip.
- **Cancelamento visível:** o par acende em CORAL e sai junto.
- **A narração lê cada degrau.** A v3.4 já faz isso; aqui a tela acompanha a fala.

Na tela:
- **Kit:** `L`, `TC`, `escreve`, `escreve_p`, `voa`, `gm`, `funde`, `Duas`, `junta`, `cancela`, `acende`, `le`, `legenda`, `leg_mix`, `pisca_cor`. Use os macros do preâmbulo (`\X \Y \Z \Pp \Qq \dx \dy \V{} \D{} \Lm \Am \Mg \rot \dv \sen \vv \Hh \E \B`) e os atalhos já definidos (`SM`, `SM1`, `dPx`, `dPy`, `dQx`, `dQy`, `NX`).
- **Coluna (layout A):** a partir de x = 1110–1120, **nada passa de x = 1800**.
- **R13:** no máximo **5 linhas de conta + o enunciado** na coluna. Um chip temporário de ≤ 4 s não conta. Se uma conta nova precisar de mais linhas, a mais antiga **vira chip ou se funde** (gm) antes de a nova entrar. As posições `y` abaixo são a recomendação; o aceite é o QA (0 sobreposição, inclusive nos voos).
- **Faixa de baixo (layout B):** linhas em y ≈ 930 e 995, no máximo 2.
- **Palavras em Space Grotesk** (`legenda`/`leg_mix`), nunca frase em português dentro de MathTex. Exceção: `\text{erro}` e unidades (`\text{rad/s}`, `\text{s}`), como já está.
- **`\dfrac` sempre,** fração ≥ 26 px em 1080p.
- **Gatilhos:** cada evento abaixo dispara no `self.gat("frase")` indicado. A lista ordenada completa, com o evento de cada frase, está no **Anexo B** (é a especificação de sincronia). As marcas são `=` (gatilho que já existe, fica) e `+` (gatilho novo). Frase de gatilho se copia do Anexo B **letra por letra**, com acento.
- **Glyph maps:** o `nota=` de cada gm novo diz o degrau, por exemplo `nota="(x·2x → 2x²)"`. **Nenhuma** nota de instrução, índice ou debug aparece no vídeo.

**Prova de cada item:**
- 540p/15 do lote, com os tempos do §4;
- um quadro PNG por item, no instante em que a conta inteira está na tela: `qa/contas_v34/Cnn.png`;
- o trecho do log com os `[gm]` e `[gatilho]` do item.

**Prancha final:** `qa/contas_v34.jpg`, com os 21 quadros.

**Ordem de trabalho por lote:** PD3 (C1–C3), PD3B (C4, C5), PD4 (C6, C7), PD5 (C8), PA1 (C9–C11), PA2 (C12–C15), PA4 (C16–C18), PA3 (C19–C21). Os lotes **PH, PD1, PD2 e PS não mudam** de código.

As linhas citadas são as do código que gerou o master v3.3. Se uma linha andou, procure pelo texto citado.

---

### C1 · D3-2 · ‖(−y, x)‖ = r e s^α = r^{2α} (5:23–5:52 · `sec_d3.py:70–97`)
**Falta:** `n1` (‖v‖ = ‖(−y,x)‖/s^α) vira `r/r^{2α}` num glyph map só. Não aparece por que o numerador é `r`, nem por que `s^α = r^{2α}`, nem a subtração dos expoentes.

**Entra:** dois chips na coluna, abaixo de `n1` (y 470):
```
K1  (1120, 545, 32):  ‖(−y, x)‖ = √((−y)² + x²)   →gm→   = √(x² + y²) = r
K2  (1120, 615, 32):  s^α = (x² + y²)^α            →gm→   = (r²)^α = r^{2α}
n2  (como hoje):      ‖v‖ = r / r^{2α}     ← voos: r de K1, r^{2α} de K2
n3  (como hoje):      ‖v‖ = r^{1−2α}       (o 1 do r e o 2α viram 1 − 2α; K1, K2 e o raio saem juntos no mesmo gm)
```
LaTeX:
- K1: `L([("n", r"\|(-\Y,\ \X)\|"), ("e", "="), ("r", r"\sqrt{(-\Y)^2+\X^2}")], 1120, 545, 32)`
- K1b: `[("n", …), ("e", "="), ("r", r"\sqrt{\X^2+\Y^2}"), ("e2", "="), ("rr", "r")]`
- K2: `L([("n", r"s^{\alpha}"), ("e", "="), ("b", r"(\X^2+\Y^2)^{\alpha}")], 1120, 615, 32)`
- K2b: `+ [("e2", "="), ("c", r"(r^2)^{\alpha}"), ("e3", "="), ("d", r"r^{2\alpha}")]`

Origens:
- o `(−y, x)` de K1 voa do numerador de `fv`;
- o `s^α` de K2 voa de `n1`;
- o `(x²+y²)` de K2 voa do denominador de `fv`;
- o `raio` (já existe) nasce com `r`.

**Gatilhos (Anexo B, D3-2):** "o vetor de cima tem tamanho" → n1 · "o sinal some no quadrado" → K1→K1b + raio · "embaixo a distância ao quadrado elevada" → K2 · "potência de potência multiplica" → K2b · "então a rapidez é a distância" → n2 · "na divisão os expoentes se subtraem" → n3.

**Aceite:**
- `qa/contas_v34/C01.png` mostra K1b, K2b e n2 juntos;
- 4 gm novos no log;
- R11 = 0.

---

### C2 · D3-3 · o rotacional inteiro (5:52–7:24 · `sec_d3.py:99–211`) · **o 6:27 do Kaio**
**Falta (quadros `evidencias_v33/d3a.jpg`):**
- **6:20–6:30:** `PR` e `P2` se fundem direto em `∂Q/∂x = s^{−α−1}(s − 2αx²)`. Não aparecem:
  - `(x)′ = 1`;
  - a cadeia `(s^{−α})′ = −α s^{−α−1} · ∂s/∂x`;
  - `∂s/∂x = 2x` (o `y²` que zera);
  - `x · 2x = 2x²`;
  - o `s^{−α} = s · s^{−α−1}` que permite a evidência.
- **6:35:** `∂P/∂y = −s^{−α−1}(s − 2αy²)` nasce por **cópia** de `F2`, sem nenhuma derivada.
- **6:50:** `s^{−α−1}(2s − 2αs)` pula direto para `(2 − 2α)/s^α`, sem o `s` em evidência e sem `s · s^{−α−1} = s^{−α}`.
- **div:** o `−y` (e o `x`) sai da derivada como constante sem dizer.

**Entra.** A coluna em 5 linhas de conta + enunciado, usando uma **linha K** (y 665) para os chips da regra. y recomendados:

| linha | y |
|---|---|
| `fv` (enunciado) | 285 |
| `R0` | 400 |
| `QL`/`PQ` | 485 |
| `PR` → `F2` | 580 |
| linha K (chips, 30 px) | 665 |
| linha P (`P2…P5`, depois `G2…G5`) | 750 |
| `F3` | 660 (depois da fusão) |
| `RS…` | 760 |
| div | como hoje (`RT` 395, `DV` 505, `DP` 605, `DQ` 700, `DS`/`DZ` 800) |

**∂Q/∂x, degrau a degrau:**
```
R0   rot = ∂Q/∂x − ∂P/∂y                                   (como hoje)
QL   Q = x s^{−α},   s = x² + y²                            (o "s = x²+y²" entra no gatilho novo "para encurtar a tela chama")
PR   ∂Q/∂x = (x)′ s^{−α} + x (s^{−α})′                      (como hoje)
K1   (x)′ = 1                                               [linha K, x = 1560]  → o 1 voa para P2
K2   (s^{−α})′ = −α s^{−α−1} · ∂s/∂x                         [linha K, x = 1120]  → o −α nasce do EXPOENTE de (s^{−α})′ em PR (cópia que desce)
K3   ∂s/∂x = 2x + 0  →gm→  2x                               [linha K, x = 1560, no lugar de K1]  → o x² de QL acende AMB e vira 2x; o y² acende CORAL e vira 0
K2b  (s^{−α})′ = −α s^{−α−1} · 2x                            (gm K2 → K2b, o 2x voa de K3)
P2   = 1·s^{−α} + x·( −α s^{−α−1} · 2x )                     (s^{−α} voa de PR; 1 de K1; x de PR; o bloco da cadeia de K2b)
P3   = s^{−α} − 2α x² s^{−α−1}                               (gm: "1·" some; x e o x de 2x → x²; o − do −α sai para a frente)
K4   s^{−α} = s · s^{−α−1}     (−α = 1 + (−α − 1))           [linha K inteira, depois que K1–K3 saem]
P4   = s · s^{−α−1} − 2α x² s^{−α−1}                          (s · s^{−α−1} voa de K4 no lugar do s^{−α})
P5   = s^{−α−1}(s − 2α x²)                                   (gm: os dois s^{−α−1} viram um, fora do parêntese)
F2   ∂Q/∂x = s^{−α−1}(s − 2αx²)                              (FUSÃO PR + P5 + K4 → F2 na linha 580, como o F2 de hoje)
```
LaTeX de P2 e P3 (as chaves fazem o mapa do degrau `x·2x → 2x²`):
```python
P2 = L([("eq", "="), ("um", r"1\cdot "), ("sm", SM), ("m", "+"), ("x", r"\X"), ("ab", r"\cdot\big("), ("mn", "-"), ("al", r"\alpha\,"), ("pw", SM1),
        ("dt", r"\cdot "), ("d2", "2"), ("dX", r"\X"), ("fp", r"\big)")], 1150, 750, 34)
P3 = L([("eq", "="), ("sm", SM), ("mn", "-"), ("d2", "2"), ("al", r"\alpha"), ("x2", r"\X^2"), ("pw", SM1)], 1150, 750, 34)
gm(self, P2, P3, rt=0.9, ka=["eq", "z", "sm", "z", "x2", "z", "mn", "al", "pw", "z", "d2", "x2", "z"], nota="(x·2x → 2x²; o − vai para a frente)")
K4 = L([("a", SM), ("e", "="), ("s", "s"), ("d", r"\cdot"), ("b", SM1), ("n", r"\qquad(-\alpha=1+(-\alpha-1))")], 1120, 665, 30)
P4 = L([("eq", "="), ("s", "s"), ("d", r"\cdot"), ("pw0", SM1), ("mn", "-"), ("c", r"2\alpha\X^2"), ("pw", SM1)], 1150, 750, 34)
gm(self, P3, P4, rt=0.8, voos={"s": K4.p("s"), "pw0": K4.p("b")}, ka=["eq", "z", "mn", "c", "c", "c", "pw"], nota="(s^{−α} = s·s^{−α−1})")
P5 = L([("eq", "="), ("pw", SM1), ("ab", r"\,(s"), ("mn", "-"), ("c", r"2\alpha\X^2"), ("fc", ")")], 1150, 750, 34)
gm(self, P4, P5, rt=0.9, ka=["eq", "ab", "ab", "pw", "mn", "c", "pw"], nota="(evidência: s^{−α−1})")
```

**∂P/∂y, degrau a degrau** (substitui o `gm(F2, F3, copia=True)` da linha 166):
```
PQ   P = −y s^{−α},  Q = x s^{−α},  s = x² + y²                (como hoje, o −y voa de fv)
G1   ∂P/∂y = (−y)′ s^{−α} + (−y)(s^{−α})′                     [linha K → vira a linha 665 depois que K4 sai]   (o −y voa duas vezes de PQ)
G2   = −1·s^{−α} + (−y)(−α s^{−α−1} · 2y)                      [linha 750]   (o −1 nasce sobre (−y)′ e voa; o 2y: o y² de PQ acende MG)
G3   = −s^{−α} + 2α y² s^{−α−1}                                (gm: os dois "−" de (−y) e de −α acendem CORAL e viram o "+"; y·2y → 2y²)
G4   = −s · s^{−α−1} + 2α y² s^{−α−1}                          (chip K4 volta 1 s ao lado; s · s^{−α−1} voa dele)
G5   = −s^{−α−1}(s − 2α y²)                                    (o "−" da frente acende CORAL no gatilho "e o sinal trocado")
F3   ∂P/∂y = −s^{−α−1}(s − 2αy²)                               (FUSÃO G1 + G5 → F3 na linha 660)
```

**A subtração e a simplificação** (RS, RS2…RS5 como hoje; entram três degraus entre RS5 e RS6):
```
RS    rot = s^{−α−1}(s − 2αx²) − ( −s^{−α−1}(s − 2αy²) )       (copia de R0 com voos de F2 e F3, como hoje, agora no gatilho novo "ao subtrair menos com menos")
RS2   = … + …     RS3   RS4   RS5 = s^{−α−1}(2s − 2αs)         (como hoje)
RS5b  = s^{−α−1} · s (2 − 2α)                                   (gm: os dois s do parêntese se juntam num s fora)
RS5c  = s^{−α}(2 − 2α)                                          (chip 1 s: s · s^{−α−1} = s^{−α}; o expoente −α−1+1 acende)
RS6   = (2 − 2α)/s^α      RS7 = (2 − 2α)/(x² + y²)^α           (como hoje)
```
```python
RS5b = L([("rot", r"\V{\rot}="), ("e", SM1), ("d", r"\cdot"), ("s", "s"), ("ap", "("), ("n2", "2"), ("m", "-"), ("al", r"2\alpha"), ("fp", ")")], 1120, 760, 34)
RS5c = L([("rot", r"\V{\rot}="), ("e", SM), ("ap", "("), ("n2", "2"), ("m", "-"), ("al", r"2\alpha"), ("fp", ")")], 1120, 760, 34)
```

**div** (as linhas `DP`/`DQ`, 30 px; a 1ª igualdade nova mostra a constante saindo):
```python
DP = L([("dPx", r"\dfrac{\partial\Pp}{\dx}="), ("my", r"-\Y"), ("d0", r"\cdot\dfrac{\partial(s^{-\alpha})}{\dx}"), ("c", r"=-\Y\big(-\alpha s^{-\alpha-1}\cdot2\X\big)"),
        ("r", r"=2\alpha\X\Y\,s^{-\alpha-1}")], 1120, 605, 30)
DQ = L([("dPx", r"\dfrac{\partial\Qq}{\dy}="), ("my", r"\X"), ("d0", r"\cdot\dfrac{\partial(s^{-\alpha})}{\dy}"), ("c", r"=\X\big(-\alpha s^{-\alpha-1}\cdot2\Y\big)"),
        ("r", r"=-2\alpha\X\Y\,s^{-\alpha-1}")], 1120, 700, 30)
```
- "na primeira o menos ípsilon é constante": `DP` até `d0`, com o `−y` acendendo GEO.
- "na segunda o xis é constante": `DQ` até `d0`, por cópia + mapa.
- "só a regra da cadeia trabalha": as duas `c`.
- "e sai o mesmo termo": as duas `r`.
- `DS`, `cancela` e `DZ` como hoje.

**Gatilhos:** os 45 do Anexo B, D3-3, na ordem. A "legenda REGRA DO PRODUTO · REGRA DA CADEIA" (`lg`) **sai**: agora cada regra aparece escrita na própria conta.

**Aceite:**
- `C02a.png` (P5 completa, com K4 na tela);
- `C02b.png` (G5 completa);
- `C02c.png` (RS5c);
- `C02d.png` (DP e DQ completas);
- ≥ 14 gm novos no D3-3;
- nenhuma linha da coluna nasce já com o resultado (R11 = 0);
- R13 ≤ 5 + enunciado;
- o atraso de cada gatilho ≤ 0,2 s.

---

### C3 · D3-6 · o limite na origem com as contas (8:18–8:54 · `sec_d3.py:306–388`)
**Falta:**
- "a rapidez vai a zero" sem dizer **por quê** (1 − 2α > 0).
- Com α = ½, `o2`/`o3` só dizem "pelo eixo x: v → (0, 1)", com o valor voando da seta. Não existe a conta.
- "a seta explode" sem o expoente negativo.

**Entra:**
```
rz0 (1320, 240, 34, "c"):  ‖v‖ = r^{1−2α}
rz  (gm, 32 px):           0 < α < ½  ⇒  1 − 2α > 0  ⇒  r^{1−2α} → 0
o2a (1120, 370, 34):       X = (t, 0):   v = (−0, t)/√(t²)
o2  (gm):                  … = (0, t)/t = (0, 1)              (a última seta do caminho x e o (0,1) acendem juntos)
o3a (1120, 470, 34):       X = (0, t):   v = (−t, 0)/√(t²)
o3  (gm):                  … = (−t, 0)/t = (−1, 0)
rz1 (360, 240, 28, "c"):   1 − 2α > 0  ⇒  r^{1−2α} → 0        (sobre o cartão 1, na volta aos cartões)
rz2 (1560, 240, 28, "c"):  1 − 2α < 0  ⇒  r^{1−2α} = 1/r^{2α−1} → ∞    (sobre o cartão 3)
```
LaTeX:
- o2a: `L([("t", r"X=(t,\,0):\ \ "), ("v", r"\vv="), ("f", r"\dfrac{(-0,\ t)}{\sqrt{t^2}}")], 1120, 370, 34)`
- o2: `+ [("e", "="), ("g", r"\dfrac{(0,\ t)}{t}"), ("e2", "="), ("val", r"(0,\,1)")]`
- o3 é o mesmo, com `(-t,\ 0)` e `(-1,\,0)`.
- rz2: `r"1-2\alpha<0\ \Rightarrow\ r^{1-2\alpha}=\dfrac{1}{r^{2\alpha-1}}\to\infty"`

**No palco:** o ponto laranja de cada caminho ganha o rótulo `t` (26 px, junto do ponto), e uma legenda `t > 0` (GEO, 24 px) no canto do palco.

**Gatilhos:** Anexo B, D3-6 (7 novos).

**Aceite:**
- `C03a.png`: o2 e o3 completas, com as setas acesas;
- `C03b.png`: os cartões com rz1 e rz2;
- sobreposição 0 entre `rz1`, `rz2`, os títulos e os cartões.

---

### C4 · D3b-2 · o gradiente com as derivadas (10:23–10:33 · `sec_d3b.py:110–131`)
**Falta:** `ph` = `φ = ½(x² − y²), ∇φ = (x, −y)` sai pronto.

**Entra** (no lugar de `ph`; `dm` desce para y 715):
```
PH1 (1120, 510, 36):  φ = ½(x² − y²)
PH2 (1120, 580, 32):  φ_x = ½·2x = x ,   φ_y = ½·(−2y) = −y      (o 2 do expoente de x² e de y² desce: cópia do expoente voa para a frente)
PH3 (1120, 650, 34):  ∇φ = (φ_x, φ_y) = (x, −y)                  (x e −y voam de PH2)
```
LaTeX de PH2:
```python
L([("fx", r"\varphi_{\Am x}"), ("ex", r"=\tfrac12\cdot2\X"), ("rx", r"=\X"), ("vg", r",\qquad "), ("fy", r"\varphi_{\Mg y}"), ("ey", r"=\tfrac12\cdot(-2\Y)"), ("ry", r"=-\Y")], 1120, 580, 32)
```
"e pela regra que acabamos" → `RZ` (rot ∇φ = 0) acende VIO.

**Aceite:** `C04.png`.

---

### C5 · D3b-4 · as três parciais do teste (10:53–11:14 · `sec_d3b.py:184–219`)
**Falta:** `sen y`, `−sen y` e `1` voam prontos das frações.

**Entra.** `RR` começa com o degrau de cada parcela; depois um gm junta:
```
RR  (1150, 650, 36):   = 1·sen y + (−sen y) + 1
RR2 (gm):              = sen y − sen y + 1        → cancela s1, s2 (CORAL) → R2 = 1 ≠ 0 (como hoje)
```
Antes de cada voo, a fração acende o que fica parado (GEO) e o que varia (cor da variável):
- em t1, `sen y` parado e `x` variando; o 1 nasce do `x`;
- em t2, `cos y`;
- em t3, `−xy` parado e `z` variando.

`RR = L([("e", "="), ("u1", r"1\cdot"), ("s1", r"\sen\Y"), ("p2", "+"), ("s2", r"(-\sen\Y)"), ("um", "+1")], 1150, 650, 36)`

**Aceite:** `C05.png` (RR completa) + o log com o gm `RR → RR2`.

---

### C6 · D4-6 · a definição de diferenciável e a conta do ½ (14:04–14:54 · `sec_d4.py:332–402`)
**Falta:** a única conta é `RZ` (uma linha na faixa): `F(h,h) = (h/2, h/2) ⇒ ‖erro‖/‖H‖ = (h√2/2)/(h√2) = ½`. Faltam:
- a **definição** (F(H) = F(0) + J·H + erro(H), com erro/‖H‖ → 0);
- por que o erro é o próprio F;
- a conta de F(h,h);
- as duas normas.

**Layout novo:** depois do HS2, no gatilho "agora a definição":
- o **painel da direita (×100) sai inteiro**: `pd`, `z10`, `oz2`, `nz3`;
- a **coluna** nasce no lugar dele (x ≥ 1100, y 230–880);
- `HS2` fica na faixa, como resultado da homogeneidade;
- `RZ` **não existe mais**.

O palco fica sendo o painel da esquerda (zoom ×1). No fim, os **quatro quadradinhos andam nele**, com `peds`/`fans` no viewport `vl` e a `clareira` em `z1` (é o mesmo desenho: homogeneidade).
```
DF1 (1100, 260, 30):  F(H) = F(0) + J H + erro(H),     ‖erro(H)‖/‖H‖ → 0          + legenda DIFERENCIÁVEL EM 0 (GEO, 24 px, y 315)
DF3 (1100, 390, 30):  F(0) = 0,  J = 0   ⇒   erro(H) = F(H)                         + legenda DO ITEM C (GEO, 22 px, à direita)
DF4 (1100, 490, 32):  H = (h, h):   F(h,h) = (h·h)/(h² + h²) · (h, h)
     →gm→  = h²/(2h²) · (h, h) = ½ (h, h)    →gm→   = ½(h, h) = (h/2, h/2)
DF5 (1100, 600, 30):  ‖erro‖ = √(h²/4 + h²/4) = h√2/2 ,     ‖H‖ = √(h² + h²) = h√2     (os h/2 voam de DF4)
DF6 (1100, 710, 34):  ‖erro‖/‖H‖ = (h√2/2)/(h√2) = ½   ↛ 0                          (½ AMB; "↛ 0" CORAL)
```
LaTeX:
- DF1: `r"\F(\Hh)=\F(\vec0)+J\,\Hh+\text{erro}(\Hh),\quad \dfrac{\|\text{erro}(\Hh)\|}{\|\Hh\|}\to0"`
- DF4: `r"\Hh=(h,\,h):\ \ \F(h,h)=\dfrac{h\cdot h}{h^2+h^2}(h,\,h)"`
- DF5: `r"\|\text{erro}\|=\sqrt{\dfrac{h^2}{4}+\dfrac{h^2}{4}}=\dfrac{h\sqrt2}{2},\qquad \|\Hh\|=\sqrt{h^2+h^2}=h\sqrt2"`
- DF6: `r"\dfrac{\|\text{erro}\|}{\|\Hh\|}=\dfrac{h\sqrt2/2}{h\sqrt2}=\dfrac12\ \not\to\ 0"`. Se `\not\to` sair torto, use `\nrightarrow`.

**No palco (painel esquerdo), no gatilho "testa na diagonal com o passo":**
- o ponto `H = (1,2; 1,2)`;
- o vetor `H` desde a origem (BR, 2 px);
- a seta do campo nele (CAMPO2), de comprimento metade;
- a legenda `H` (26 px).

Tudo isso sai em "tem quadradinho crescendo".

**Gatilhos:** Anexo B, D4-6 (11 novos).

**Aceite:**
- `C06.png`: DF1–DF6 + o palco com H;
- painel vazio 0: a moldura da direita sai junto com o campo ×100 e não fica caixa vazia;
- o quadro da prancha dos alvos do zoom (alvo 17) continua batendo **até** "agora a definição".

---

### C7 · D4-7 · N′, D′, a distributiva termo a termo, os eixos e a diagonal (14:54–16:08 · `sec_d4.py:404–497`)
**Falta:**
- `N′ = 2xy` e `D′ = 2x` só falados;
- a distributiva aparece de uma vez;
- os eixos são só a legenda "NOS EIXOS: 0";
- na diagonal, `(x² + x²)² = (2x²)²` é pulado.

**Entra:**
```
ND (1110, 470, 28):   N′ = ∂(x²y)/∂x = 2xy ,      D′ = ∂(x² + y²)/∂x = 2x + 0 = 2x     (o x² acende AMB; o y em N fica GEO: parado)
Q1 (1110, 545, 34):   como hoje, mas com voos: N′ e D′ de ND; N e D de QM
Q2 (1140, 660, 34):   = (2x³y + 2xy³ − 2x³y)/(x² + y²)²     — os três termos nascem UM POR VEZ, cada um por TransformFromCopy dos dois fatores de Q1
EX (1110, 420, 30):   y = 0:  2x·0³/(x²)² = 0 ,      x = 0:  2·0·y³/(y²)² = 0           (substitui a legenda ne_ "NOS EIXOS: 0")
DG (1110, 532, 32):   y = x:  2x·x³/(x² + x²)²  =  2x⁴/(2x²)²  =  2x⁴/4x⁴  =  ½
```
LaTeX:
- EX: `r"\Y=0:\ \dfrac{2\X\cdot0^3}{(\X^2)^2}=0,\qquad \X=0:\ \dfrac{2\cdot0\cdot\Y^3}{(\Y^2)^2}=0"`
- DG: `L([("y", r"\Y=\X:\quad "), ("a", r"\dfrac{2\X\cdot\X^3}{(\X^2+\X^2)^2}"), ("b", r"=\dfrac{2\X^4}{(2\X^2)^2}"), ("c", r"=\dfrac{2\X^4}{4\X^4}"), ("d", r"=\dfrac12")], 1110, 532, 32)`

**Gatilhos:** Anexo B, D4-7 (8 novos).

**Aceite:** `C07a.png` (ND + Q1 + Q2) e `C07b.png` (EX + DG + os rótulos ½ do palco).

---

### C8 · D5-9 · o degrau do meio de cada célula de z² (19:10–19:41 · `sec_d5.py:91–119` e `352–390`)
**Falta:** a `deriva` vai direto de `x² − y²` para `2x`. O termo parado só fica coral e some.

**Entra.** `deriva` ganha um degrau opcional `inter` (glyph map `mid → inter → val`, 0,4 s cada). Ele vale só no campo ③:

| célula | mid | inter | val |
|---|---|---|---|
| (0,0) | `x² − y²` | `2x − 0` (o −y² acende CORAL e vira `−0`) | `2x` |
| (0,1) | `x² − y²` | `0 − 2y` | `−2y` |
| (1,0) | `2xy` | `2·y·1` | `2y` |
| (1,1) | `2xy` | `2·x·1` | `2x` |

No plano da tabela, o gatilho da célula (0,1) passa a ser **"em ípsilon o xis ao quadrado"**. A frase "e menos duas vezes a vertical" continua no texto, sem evento.

**Aceite:**
- `C08.png`: o quadro do degrau `0 − 2y` a caminho da célula;
- 4 gm a mais no D5-9;
- nada fica escrito fora da tabela.

---

### C9 · A1-2 · a tabela do rio pelas derivadas (21:34–21:41 · `sec_a1.py:98–114`)
**Falta:** `Jv = (0 0; −2x/9 0)` é escrita direto.

**Entra.** O mesmo mecanismo do D5:
1. Mova `LoteD5.deriva` (`sec_d5.py:91–107`) para `lib30.py` como função `deriva_cel(cena, comp, alvo, col, mid_p, val_p, ka, some=(), extra=(), y_mid=372, inter=None, inter_ka=None)`.
2. `LoteD5.deriva` passa a chamá-la, com o mesmo comportamento, mais o `inter` do C8.

No A1:
- `y_mid = 335` (abaixo de `V2`, y 270);
- `Jm` com `caneta=False`;
- `cel, resto = celulas(Jm)`;
- os parênteses (`resto`) entram com o primeiro voo.

| célula | de onde | mid → inter → val |
|---|---|---|
| (0,0), (0,1) | o `0` de `v = (0, …)` | `0 → 0` (rótulo ∂/∂x, depois ∂/∂y) |
| (1,1) | `1 − x²/9` de `V2` | `1 − x²/9` todo CORAL `→ 0` (não tem y) |
| (1,0) | `1 − x²/9` de `V2` | `1 − x²/9 → 0 − 2x/9 → −2x/9` (o 2 do expoente desce) |

`DV`/`DV2` como hoje, no gatilho novo "divergente zero mais zero".

**Para caber o R13:**
- no início do A1-3, `DV2` vira o chip `div = 0` (30 px, ao lado direito de `Jm`, x ≈ 1600, y 390);
- `RT` sobe para y 490.

**Aceite:** `C09.png`, com uma célula a caminho.

---

### C10 · A1-3 · o rot nas margens, ω e T com as contas (21:41–22:29 · `sec_a1.py:116–144`)
**Falta:**
- `XR` = "x = −3: rot = 2/3", sem a substituição;
- `ω = 1/3` e `T = 6π ≈ 19 s` sem a divisão;
- a margem direita e o centro sem conta.

**Entra** (y: `RT` 490, `XR` 575, `OM1` 660, `OM2` 745):
```
RT2  rot = Q_x − P_y = −2x/9 − 0 = −2x/9                   (como hoje; o "− 0" acende em "menos a derivada da primeira componente")
XR   rot(−3) = −2(−3)/9   →gm→  = 6/9   →gm→  = 2/3          (o −3 voa do rótulo x = −3 do palco; 6/9 → 2/3 com o ÷3 acendendo)
OM1  ω = rot/2 = (2/3)/2 = 1/3 rad/s                       (o 2/3 voa de XR)
OM2  T = 2π/ω = 2π/(1/3) = 2π·3 = 6π ≈ 18,8 ≈ 19 s           (o 1/3 voa de OM1; o ≈ 18,8 entra em "com pi perto de três vírgula catorze")
XR'  rot(−3) = 2/3 ,  rot(3) = −2·3/9 = −2/3 ,  rot(0) = 0    (XR vira chip à esquerda; o 3 voa do rótulo x = 3; o 0 junto das setas do meio)
```
LaTeX:
- OM1: `r"\omega=\dfrac{\rot}{2}=\dfrac{2/3}{2}=\dfrac13\ \text{rad/s}"`
- OM2: `r"T=\dfrac{2\pi}{\omega}=\dfrac{2\pi}{1/3}=2\pi\cdot3=6\pi\approx18{,}8\approx19\ \text{s}"`

Os sublinhados de leitura de ω e T (`le`, leituras 17 e 18) ficam como estão, cada um no glifo de hoje.

**Aceite:** `C10a.png` (XR, OM1, OM2) e `C10b.png` (XR′).

---

### C11 · A1-5 · d₂ nas margens (22:44–23:06 · `sec_a1.py:169–197`)
**Falta:**
- `DD` numa linha só;
- "máxima nas margens" sem calcular d₂ em ±3.

**Entra** (o `DD` de hoje vira duas linhas, mais a linha das margens; a legenda vai para a faixa de baixo):
```
DD1 (1120, 660, 32):  d₁ = P_x − Q_y = 0 − 0 = 0                    (voos das células)
DD2 (1120, 745, 32):  d₂ = Q_x + P_y = −2x/9 + 0 = −2x/9
DD3 (1120, 830, 32):  |d₂(±3)| = 2·3/9 = 2/3 ,    d₂(0) = 0          (as margens acendem LIMA; depois o meio)
ATRITO VISCOSO: MÁXIMO NAS MARGENS   (legenda LIMA 26 px, y 945)
```

**Aceite:** `C11.png`.

---

### C12 · A2-2 · a tabela do jato pelas derivadas (23:24–24:25 · `sec_a2.py:62–96`)
**Falta:** `Jm = (1 0; 0 −1)` sai pronta.

**Entra.** `deriva_cel` (C9) a partir de `VV`, no mesmo padrão do D5 (`sec_d5.py:370–382`):
- o `x` de `VV` → células (0,0) e (0,1): `x → 1` com ∂/∂x, `x → 0` com ∂/∂y, o x todo CORAL;
- o `−y` de `VV` → células (1,0) e (1,1): `−y → 0`, `−y → −1`.

Gatilhos: "segundo a tabela derivada por derivada" (molde) · "a primeira componente é xis" · "a segunda é menos ípsilon" · "a tabela tem um e zero" (acende as 4). Os moldes `Ms` de rot/div/d₁ e o laço deles ficam como hoje.

**Aceite:** `C12.png`.

---

### C13 · A2-2 · a regra do produto no tempo e a hipérbole (`sec_a2.py:97–138`)
**Falta:**
- `d(xy)/dt = u y + x v` nasce sem a regra do produto no tempo e sem `dx/dt = u`, `dy/dt = v`;
- "o produto constante" sem `y = c/x`.

**Entra** (o bloco da tabela já saiu nas hipérboles):
```
HP (1120, 340, 34):  xy = c  ⇒  y = c/x
DT (1120, 420, 34):  d(xy)/dt = (dx/dt)·y + x·(dy/dt)            (regra do produto, agora no tempo)
CH (1120, 505, 30):  dx/dt = u ,    dy/dt = v                    (u e v voam do "(u, v)" de VV)
DT2 (gm, 420):       d(xy)/dt = u·y + x·v                         (= o DT de hoje; u e v voam de CH)
D2…D4 (1150, 585):   = x·y + x(−y) = xy − xy = 0                  (como hoje, só muda o y: 470 → 585)
pn  (legenda, 650)
```
LaTeX:
- DT: `L([("d", r"\dfrac{d(\X\Y)}{dt}="), ("a", r"\dfrac{d\X}{dt}\,"), ("y", r"\Y"), ("pl", "+"), ("x", r"\X\,"), ("b", r"\dfrac{d\Y}{dt}")], 1120, 420, 34)`
- CH: `r"\dfrac{d\X}{dt}=u,\qquad \dfrac{d\Y}{dt}=v"`

O sublinhado da leitura 19 fica no `d(xy)/dt`, com o `ate="andando com a água"` de hoje. Ele agora dura ≈ 8 s; é aceitável.

**Aceite:** `C13.png` (DT, CH, DT2 e D4 juntas).

---

### C14 · A2-3 · o potencial com as derivadas (24:25–24:42 · `sec_a2.py:140–160`)
**Falta:** `PH` = `φ_x = x, φ_y = −y` pronto.

**Entra.** No gatilho "esse campo é o gradiente", a fusão do produto que hoje está no começo do A2-4 vem para cá:
- `HP` + `DT2`/`D4` + `pn` → o chip `xy = c ,  d(xy)/dt = 0` (1120, 340, 30);
- a coluna fica livre para o potencial:
```
PH1 (1120, 420, 34):  φ = ½(x² − y²)                     + legenda POTENCIAL DE VELOCIDADE (GEO, 24 px) em "essa função se chama potencial"
PH2 (1110, 500, 28):  φ_x = ½·2x = x ,  φ_y = ½·(−2y) = −y   ⇒   ∇φ = v        (o v voa de VV)
LX  (1120, 580, 34):  φ_xx = 1 ,  φ_yy = −1                (como hoje, gm de PH2)
LP  (1120, 660, 36):  ∇²φ = φ_xx + φ_yy = 1 + (−1) = 0     (como hoje)
```

**Aceite:** `C14.png`.

---

### C15 · A2-4 · div ∇φ = ∇²φ com as derivadas (24:42–25:11 · `sec_a2.py:162–190`)
**Falta:** `C2` = `div ∇φ = ∇²φ` afirmado.

**Entra:**
- O `C2` vira a conta, na faixa (1110, 965, 28):

  ```
  div ∇φ = ∂(φ_x)/∂x + ∂(φ_y)/∂y = φ_xx + φ_yy = ∇²φ = 0
  ```

  LaTeX: `r"\D{\dv}\,\nabla\varphi=\dfrac{\partial\varphi_{\Am x}}{\dx}+\dfrac{\partial\varphi_{\Mg y}}{\dy}=\varphi_{\Am{xx}}+\varphi_{\Mg{yy}}=\nabla^2\varphi"` e depois `"=0"`.
- Em "é a primeira das duas regras": o chip de lembrança `rot ∇φ = 0` (VIO, 26 px, 1,5 s) ao lado de C1a, com `_origem = "lembrança"`.
- A fusão do produto **sai** do A2-4 (foi para o C14).

**Aceite:** `C15.png`; a faixa não passa de x = 1800.

---

### C16 · A4-1/A4-2 · Cauchy-Riemann e z² inteiros, em layout A (25:12–26:08 · `sec_a4.py:116–164`)
**Falta:**
- a faixa de baixo do layout B só tem 2 linhas, e o z² pula de `x² + 2ixy + i²y²` para `(x² − y²) + i(2xy)`;
- não há o molde `(a + b)²`, nem `i² = −1` como degrau, nem o agrupamento;
- **não há a conferência de Cauchy-Riemann** no próprio z², que é o ponto do A4.

**Layout novo:** no A4-1 e no A4-2, **layout A**:
- palco: o campo ③ com eixos, o mesmo do D5-9 (`sec_d5.py:355–366`: chapa `LA`, `V3`, `ex3`, `campo30(V3, F3, …)`);
- coluna à direita.

A malha, as marcas, o círculo pequeno e a legenda "UMA MALHA DE QUADRADINHOS" passam para o A4-3. O A4-3 volta ao **layout B** de hoje (C17).
```
D1  (1120, 280, 34):   d₁ = P_x − Q_y = 0  →gm→  … ⇒ P_x = Q_y              (como hoje, só muda a posição)
D2  (1120, 360, 34):   d₂ = Q_x + P_y = 0  →gm→  … ⇒ P_y = −Q_x
    legenda EQUAÇÕES DE CAUCHY-RIEMANN (GEO, 26 px, y 425) em "essas são as equações de cauchy"
FZ0 (1120, 510, 34):   F = (x² − y², 2xy)                                     (no gatilho "o nosso campo é exatamente o quadrado"; o campo ③ acende)
Z0  (1120, 590, 34):   (x + iy)²                                               (leitura 21 do i: como hoje, no i de Z0)
MO  (1120, 660, 30):   (a + b)² = a² + 2ab + b²
Z1  (gm, 590):         (x + iy)² = x² + 2x(iy) + (iy)²      →gm→  = x² + 2ixy + i²y²     (a = x e b = iy voam de Z0 para o molde)
I2  (1120, 660, 30):   i² = −1                               (no lugar de MO, que sai)
Z2  (gm, 590):         = x² + 2ixy − y²                      (o −1 voa de I2)
Z3  (gm, 590):         = (x² − y²) + i(2xy)                  (x² e −y² se juntam; 2ixy vira i(2xy))
    → (x² − y²) e (2xy) voam para FZ0, que acende; chaves P e Q sob as componentes de FZ0 (como as chaves do D5)
CR1 (1120, 600, 30):   P_x = ∂(x² − y²)/∂x = 2x  =  ∂(2xy)/∂y = Q_y  ✓
CR2 (1120, 680, 30):   P_y = ∂(x² − y²)/∂y = −2y  =  −∂(2xy)/∂x = −Q_x  ✓      (Z0…Z3 e I2 já saíram em "confere as equações")
    legenda TODA FUNÇÃO COMPLEXA DERIVÁVEL: z³, eᶻ (leg_mix, GEO, y 760)
```
LaTeX:
- CR1: `r"\Pp_{\Am x}=\dfrac{\partial(\X^2-\Y^2)}{\dx}=2\X\ =\ \dfrac{\partial(2\X\Y)}{\dy}=\Qq_{\Mg y}\ \checkmark"`
- CR2: `r"\Pp_{\Mg y}=\dfrac{\partial(\X^2-\Y^2)}{\dy}=-2\Y\ =\ -\dfrac{\partial(2\X\Y)}{\dx}=-\Qq_{\Am x}\ \checkmark"`

Os ✓ acendem CAMPO2 em "passou". Se `\checkmark` não existir no preâmbulo, use a legenda "✓" em Space Grotesk.

**Aceite:**
- `C16a.png` (Z3 + FZ0 com as chaves);
- `C16b.png` (CR1 + CR2);
- o campo ③ no palco o tempo todo: `palco_parado` ≤ 8 s, com o campo acendendo nos gatilhos que citam ele.

---

### C17 · A4-3 · por que a tabela de z² só gira e escala (26:09–26:35 · `sec_a4.py:166–200`)
**Falta:** "uma tabela assim só gira e muda a escala" é só falado.

**Entra.** Volta ao layout B (malha à esquerda, malha que se transforma à direita), e a faixa de baixo ganha a conta, uma linha por vez (gm no lugar, x = 140, y 958, 30 px):
```
JC1:  J = (2x  −2y; 2y  2x) = (a  −b; b  a),    a = 2x, b = 2y
JC2:  (a  −b; b  a) = √(a² + b²) · (cos θ  −sen θ; sen θ  cos θ),     √(a² + b²) = 2√(x² + y²) = 2r
JC3:  (1,1):   J = (2  −2; 2  2) = 2√2 · (cos 45°  −sen 45°; sen 45°  cos 45°)
```
Matrizes como no D5: coluna x em âmbar e coluna y em magenta na JC1; a JC2 e a JC3 em branco.

**No palco:**
- A morfose `z^s` (s de 1 a 2, como hoje) roda em "agora lê como transformação".
- Em "no ponto um um ela é", um quadradinho pequeno em (1,1) do painel esquerdo é **copiado e voa** para a imagem dele no painel direito, z²(1+i) = (0, 2). No caminho ele gira 45° e cresce ×2√2 (`Transform`). É a JC3 acontecendo.
- Em "as duas colunas têm o mesmo tamanho": as duas colunas `(2, 2)` e `(−2, 2)` em setas finas BR nesse ponto, com a marca de ângulo reto.
- Os gatilhos de hoje (círculo, marcas, Mercator) ficam.

**Aceite:**
- `C17.png` (JC3 + o quadradinho girado na direita);
- `palco_parado` ≤ 8 s entre a morfose e "quadradinhos pequenos viram quadradinhos". Se passar, acenda as marcas em "uma tabela assim é um número vezes".

---

### C18 · A4-4 · o irmão com as derivadas (26:35–26:43 · `sec_a4.py:202–213`)
**Falta:** `J` e `rot`/`div` do irmão saem prontos, e d₁ e d₂ não aparecem.

**Entra.** Na faixa, depois que JC3 sai:
```
I0 (140, 930, 30):   F = (x² − y², −2xy)
I1 (560, 958, 30):   J = (2x  −2y; −2y  −2x)                      (a 1ª linha em "as derivadas da primeira são", a 2ª em "as da segunda")
I2 (860, 930, 26):   rot = Q_x − P_y = −2y − (−2y) = 0 ,    div = P_x + Q_y = 2x − 2x = 0
I3 (860, 990, 26):   d₁ = P_x − Q_y = 2x − (−2x) = 4x ,    d₂ = Q_x + P_y = −2y − 2y = −4y
```
A legenda "SÓ DEFORMA" (LIMA) vai para o painel da direita, no lugar da legenda do Mercator (1440, 868), e entra em "esse irmão não gira".

**Aceite:** `C18.png`; a faixa não passa de x = 1800.

---

### C19 · A3-3 · o denominador positivo e ‖B‖ com origem (27:26–27:51 · `sec_a3.py:84–121`)
**Falta:**
- "o numerador zera" sem dizer que o denominador nunca é zero;
- `NB` = `r/r^{2α}` nasce escrito, sem a origem de `r` e de `r^{2α}`.

**Entra:**
```
DEN (1120, 545, 32):  (x² + y²)^α > 0              (o denominador de RB0 voa; sai quando N0 entra)
N0, N1, N2 (1120, 615): como hoje (só o y muda: 590 → 615); o −2α de N0 acende CORAL em "passa o dois alfa para o outro lado"
NB1 (1120, 700, 38):  ‖B‖ = ‖(−y, x)‖/(x² + y²)^α                     (voos do campo B do topo)
     chip (1460, 700, 28, 1 s):  ‖(−y, x)‖ = √(y² + x²) = r
NB2 (gm):  = r/(x² + y²)^α     →gm→  NB3 = r/r^{2α}     →gm→  NB4 = r/r² = 1/r     (o α = 1 de N2 acende e voa para o expoente)
```

**Aceite:** `C19.png` (NB4 com o gráfico embaixo, como hoje).

---

### C20 · A3-4 · o div E calculado de verdade (27:51–28:11 · `sec_a3.py:123–150`)
**Falta:** `DE` = `div E = (2 − 2α)/(x² + y²)^α` nasce de um gm "rot → div" **sem nenhuma conta**.

**Entra.** Em "calcula o divergente como no terceiro":
- `RB0` e `N2` saem;
- `NB4` vira o chip `‖B‖ = 1/r` (1560, 380, 30), à direita da legenda `ga`.
```
DV (1120, 460, 32):  div E = ∂(x s^{−α})/∂x + ∂(y s^{−α})/∂y ,    s = x² + y²
T1 (1120, 545, 30):  ∂(x s^{−α})/∂x = 1·s^{−α} + x(−α s^{−α−1}·2x)    →gm→   = s^{−α} − 2αx² s^{−α−1}
T2 (1120, 625, 30):  ∂(y s^{−α})/∂y = s^{−α} − 2αy² s^{−α−1}          (cópia de T1 + mapa que só troca x → y)
S1 (1120, 705, 32):  div E = 2s^{−α} − 2α(x² + y²) s^{−α−1}            (os dois s^{−α} se juntam; os dois termos com α se juntam)
S2 (gm):             = 2s^{−α} − 2α s·s^{−α−1}     →gm→  S3 = 2s^{−α} − 2α s^{−α}     →gm→  S4 = (2 − 2α)/s^α
DE (FUSÃO DV…S4 → 1120, 460, 38):  div E = (2 − 2α)/(x² + y²)^α = 0  ⇒  α = 1       (o "= 0 ⇒ α = 1" entra em "igual a zero alfa um")
NE (gm do chip ‖B‖, 1120, 690, 40):  ‖E‖ = r/r^{2α} = r/r² = 1/r    (como hoje)
```
O gráfico `gf` (782–900) fica: as linhas novas param em y ≤ 740.

**Aceite:** `C20.png` (S1 com T1 e T2 na tela) + o log com os gm `S1 → S2 → S3 → S4`.

---

### C21 · A3-5 · a derivada da distância e a junção das potências (28:11–29:28 · `sec_a3.py:152–253`)
**Falta:**
- `DN` = `∂‖X‖/∂x = x/‖X‖` vem pronto;
- `PA → PB` junta `‖X‖^{−p−1} · ‖X‖^{−1}` sem mostrar;
- `P3` diz `r/r³` sem a origem.

**Entra:**
```
DN0 (1120, 380, 32):  ‖X‖ = (x² + y² + z²)^{1/2}
DN1 (gm):             ∂‖X‖/∂x = ½ (x² + y² + z²)^{−1/2} · 2x           (o ½ desce do expoente; o 2x da cadeia)
DN  (gm):             ∂‖X‖/∂x = x/‖X‖                                  (½ e 2 acendem CORAL e somem; a potência −½ vira 1/‖X‖)
PA  (como hoje)
PB0 (1150, 640, 32):  = 1/‖X‖^p − p x² ‖X‖^{−p−1} ‖X‖^{−1}
PB1 (gm):             = 1/‖X‖^p − p x² ‖X‖^{−p−2}                      (os expoentes −p−1 e −1 acendem e se somam)
PB  (gm):             = 1/‖X‖^p − p x²/‖X‖^{p+2}                       (como hoje)
P3  (1120, 370, 36):  p = 3  ⇒  ‖E‖ = ‖X‖/‖X‖³ = r/r³ = 1/r²            (a 2ª parte em "a intensidade fica a distância dividida")
```
LaTeX:
- DN1: `L([("d", r"\dfrac{\partial" + NX + r"}{\dx}"), ("e", "="), ("h", r"\tfrac12"), ("r", r"(\X^2+\Y^2+\Z^2)^{-1/2}"), ("c", r"\cdot2\X")], 1120, 380, 32)`
- PB0: `("m", r"-p\,\X^2\," + NX + r"^{-p-1}" + NX + r"^{-1}")`

**Aceite:** `C21a.png` (DN1) e `C21b.png` (PB0 → PB1).

---

### O que NÃO mexer
- Os lotes PH, PD1, PD2 e PS (código), o gancho, a abertura, a escada, o cartão do próximo vídeo e o CTA.
- Todo parágrafo que não está no Anexo A: o texto é o da v3.3, e as cenas deles ficam como estão (só os tempos andam).
- Paleta, fundo, canto, logo, caneta (piso 0,20 s/glifo), costura de 0,4 s, CRF e capítulos (mesmos títulos).
- Nenhum efeito novo: sem partícula, brilho, sombra ou 3D. Acender é `acende` (cor) e nada mais.

---

## 6. Conferência 540p com voz (vídeo inteiro, antes do 1080p)
Render dos **12 lotes** em 540p/15 com os tempos do §4. Depois:
- `montar.py` com a costura de 0,4 s;
- o preview com voz em `renders/v4/yt_0030_preview_v4_540p15_voz.mp4`;
- **todos** os portões abaixo. Feche o que falhar antes do 1080p.

| Portão | Meta |
|---|---|
| As 21 contas | `qa/contas_v34/C01…C21*.png` + `qa/contas_v34.jpg` (prancha) + `qa/contas_v34.txt`: para cada C, cada degrau com o tempo em que aparece (do log `[gm]`/`[origem]`) |
| Gatilhos (código) | `confere_frases_v34.py --cena`: 0 faltando, 0 fora de ordem; log `[gatilho-sem-frase]` = 0 |
| SYNC (`qa_sync.py`) | 69 âncoras e todos os gatilhos/fins de sublinhado com atraso ≤ 0,2 s; liste os que passarem |
| Estouros | `[estouro]` > 1 s: 0. A conta nova é mais longa que a fala? Encurte dentro da cadência da caneta (piso 0,20 s/glifo), nunca acelere a voz |
| Glyph maps | ≥ os 160 da v3.3 + os novos (esperado ≥ 210); `TransformMatchingShapes` = 0 |
| Sem origem (R11) / R12 / R13 | 0 / 0 / ≤ 5 linhas + enunciado (chip ≤ 4 s fora) |
| Sobreposições | 0, inclusive em 25/50/75 % de cada transição e durante os voos |
| Margens | 0 texto cortado; nada além de x = 1800 na coluna e na faixa |
| `FLASH` (caneta) | 0 |
| `palco_parado` > 8 s | 0 |
| `painel_vazio` > 2 s | 0 (atenção ao D4-6, que tira o painel direito, e ao A4-3) |
| Canto (`qa_canto.py`) | linha 2 nunca some > 0,6 s fora do H e do cartão/CTA |
| Fundo (`qa_fundo.py`) | violeta + grade em todos os lotes |
| Leituras | 22/22 com sublinhado no gatilho |
| PAUSE E TENTE | as 10, cada uma na sua frase |
| VOZ (`qa/voz.txt`, `qa/emenda_v34.txt`, `qa/emendas_v34.txt`) | sem tag lida, sem silêncio > 1,5 s dentro de parágrafo, 22 emendas OK |
| Prancha das âncoras | `qa/prancha_ancoras.jpg`: 69 quadros, um no instante da primeira palavra de cada âncora |

---

## 7. Render final 1080p e master
1. `CRF=0 ./render1080_todos.sh` (os 12 lotes, 6 por vez, `media1080_*`). Os custos da v3.3 estão em `log1080_custo.txt`. Espere o PD3 e o PA3 mais longos (contas novas).
2. `montar1080.py`:
   - mesma ordem, `K = 12`;
   - saída `renders/yt_0030_sem_audio_1080p30.mp4` em libx264, yuv420p, **CRF 14**, preset `slow`;
   - grava `renders/lotes_final_1080.json`;
   - confira que o início de cada lote = `ini` da 1ª âncora × 30 (±1 quadro).
3. Master, com o **mesmo nome** de antes (o registro aponta para ele):

   ```
   uv run python videos/montar_master.py videos_longos/yt_0030_exercicios_modulo_31/renders/yt_0030_sem_audio_1080p30.mp4 videos_longos/yt_0030_exercicios_modulo_31/audio/narracao_final.wav videos_longos/yt_0030_exercicios_modulo_31/renders/yt_0030_master_final_1080p30.mp4
   ```

   Confira:
   - 1920×1080, 30 fps;
   - duração = WAV + 1,0 s;
   - `crf=14.0`, com o comando do AGENTS.
4. `.srt` (`gerar_srt.py` → `legenda.srt`) e capítulos (`gerar_capitulos.py` → `renders/capitulos_final.txt`). As regras são as de antes:
   - até 2 linhas × 42 caracteres, de 2 a 5 s;
   - "Cálculo três" → "Cálculo III", "cê um" → "C¹";
   - os mesmos 13 capítulos, com os tempos novos.
5. Depois que o master passar no §8, apague os `media1080_*` **desta** unidade.

---

## 8. QA final e reentrega
- **QA no 1080p:**
  - os portões do §6 por amostragem por lote; a prancha das contas e a das âncoras rodam inteiras;
  - A/V contínuo;
  - o `.srt` conferido em 5 pontos: início, a conta do D3-3, a do D4-6, o A4-2 e o fim;
  - `crf=14.0`.
- **Pasta de entrega.** A entrega da v3.3 está em `entregas/Vídeos Longos/Cálculo III/Cálculo III - EP 04 - Exercícios do módulo 3.1 - 0030/`. Se ela estiver em outro lugar, procure pelo nome com `- 0030`.
  1. Dentro dela, crie `versao_v33 - 31m02/` e **mova** para lá os arquivos da v3.3:
     - `master - 0030.mp4`;
     - `legenda - 0030.srt`;
     - `audio/`;
     - `texto/`;
     - `manifesto - 0030.json`.

     Confira o tamanho de cada um antes e depois. Nada é apagado.
  2. Rode o `entregar.py` apontando para a pasta-mãe certa:

     ```
     PARALLAX_ENTREGAS="entregas/Vídeos Longos/Cálculo III" uv run python videos/entregar.py yt_0030 --dry-run
     PARALLAX_ENTREGAS="entregas/Vídeos Longos/Cálculo III" uv run python videos/entregar.py yt_0030
     ```

     O dry-run tem que mostrar o destino **igual** à pasta acima. Se mostrar outro nome, pare e reporte antes de copiar.
  3. Esperado na pasta:
     - `master - 0030.mp4` (v3.4);
     - `legenda - 0030.srt`;
     - `audio/narracao_final - 0030.wav`;
     - `texto/` (ficha, `texto_narracao.txt`);
     - `manifesto - 0030.json`;
     - a subpasta `versao_v33 - 31m02/`.

     Sem capa.
- **Ficha:** em `## Estado`, acrescente a linha da v3.4 (data, WAV, duração, master, `.srt`, pasta) e troque `duracao_alvo` pela duração real.
- **YouTube:** se a v3.3 já foi publicada, o vídeo novo **não substitui** o antigo no mesmo link (o YouTube não troca o arquivo de um vídeo publicado). Diga isso no relatório; a decisão é do Kaio.

---

## 9. Relatório de entrega (obrigatório, e depois pare)
1. **Arquivos alterados e criados:**
   - código, com o arquivo e as linhas de cada C1–C21;
   - `deriva_cel` em `lib30.py`;
   - `qa_voz.py`;
   - narração v3.4 (`narracao.md`, `narracao_tags.md`);
   - os arquivos `_v33` guardados;
   - `trechos_v34/`, `audio/v34/`, `ancoras.json`, `.srt`, capítulos, ficha.
2. **Voz:**
   - os 11 trechos (take usado, contexto sim/não, duração, ganho, ritmo);
   - `qa/emenda_v34.txt` e `qa/emendas_v34.txt`;
   - a escuta das 22 emendas;
   - a duração final e a taxa real (palavras ÷ segundos), comparadas com a estimativa de 39:50.
3. **As 21 contas:** cada uma com o caminho do PNG e o número de gm novos; a prancha.
4. **Portões do §6** com os números reais (540p com voz e 1080p), sync e estouros.
5. **Caminhos:** WAV, preview 540p com voz, master 1080p, `.srt`, capítulos, a pasta em `entregas/` e a subpasta da v3.3.
6. **Custo de render** por lote (540p e 1080p).
7. **Pendências reais.**

Depois do relatório: **pare**. Sem publicação, capa, commit ou push.

---

## Anexo A · Os 20 parágrafos novos da narração v3.4 (texto exato; o completo está em `narracao_v34.md`)

**D3-2** (141 palavras)

> [curious] As setas continuam tangentes às circunferências em volta da origem, sempre no sentido anti-horário. Muda o comprimento. O vetor de cima tem tamanho raiz de menos ípsilon ao quadrado mais xis ao quadrado. O sinal some no quadrado, e sobra a raiz de xis ao quadrado mais ípsilon ao quadrado: a distância, o erre da tela. Embaixo, a distância ao quadrado elevada a alfa. Potência de potência multiplica os expoentes, e fica a distância elevada a dois alfa. Então a rapidez é a distância dividida pela distância elevada a dois alfa. Na divisão, os expoentes se subtraem: um menos dois alfa. Com alfa zero, a rapidez cresce com a distância: é a rotação rígida. Com alfa meio, a rapidez vale um, independentemente da posição. Com alfa um, ela cai com um sobre a distância: é o vórtice que já conhecemos.

**D3-3** (485 palavras)

> [thoughtful] Agora a conta do rotacional. Na tela, P e Q são as duas componentes, e o d arredondado é a derivada parcial. O rotacional é a derivada da componente vertical na direção horizontal, menos a derivada da componente horizontal na direção vertical. A componente vertical é a coordenada horizontal multiplicada pela distância ao quadrado elevada a menos alfa. Para encurtar, a tela chama a distância ao quadrado de esse. Regra do produto: a derivada do primeiro vezes o segundo, mais o primeiro vezes a derivada do segundo. A primeira parte dá a própria potência, porque a derivada de xis em relação a xis é um. A segunda, pela regra da cadeia: o expoente desce, menos alfa, a potência fica com um a menos no expoente, e ainda multiplica pela derivada de dentro. A derivada de esse em relação a xis é duas vezes a coordenada horizontal, porque o ípsilon ao quadrado não depende de xis. Então fica menos alfa vezes a potência com um a menos, vezes duas vezes a coordenada horizontal, vezes a coordenada horizontal de novo. Xis vezes dois xis dá dois xis ao quadrado. [thoughtful] Agora o truque: a potência menos alfa é esse vezes a potência com um a menos, porque somar um no expoente é multiplicar por esse. Põe a potência com um a menos em evidência: no parêntese, sobra esse menos dois alfa vezes o quadrado da coordenada horizontal. A outra derivada é igualzinha. A componente horizontal é menos ípsilon vezes a mesma potência. A derivada de menos ípsilon em relação a ípsilon é menos um, e a cadeia agora traz duas vezes ípsilon. Sai menos a potência, mais dois alfa ípsilon ao quadrado vezes a potência com um a menos. Em evidência, o mesmo parêntese, com a coordenada vertical e o sinal trocado. Ao subtrair, menos com menos vira mais. A distância ao quadrado aparece duas vezes, e os dois termos com alfa se juntam em dois alfa vezes a soma dos quadrados, que é a distância ao quadrado de novo. No parêntese, sobra dois esse menos dois alfa esse. Esse em evidência, vezes dois menos dois alfa. E esse vezes a potência com um a menos volta a ser a potência menos alfa. Sobra uma fórmula curtinha: dois menos dois alfa, sobre a distância ao quadrado elevada a alfa. [curious] E o divergente? Agora é a soma: a derivada da componente horizontal na direção horizontal, mais a da vertical na direção vertical. Na primeira, o menos ípsilon é constante em xis; na segunda, o xis é constante em ípsilon. Nas duas, só a regra da cadeia trabalha, e sai o mesmo termo, dois alfa vezes o produto das coordenadas vezes a potência com um a menos: uma vez com sinal de mais, outra com sinal de menos. Eles se cancelam: zero, para qualquer alfa. Nenhum desses redemoinhos muda a área local do fluido. Ainda pode haver giro e deformação.

**D3-6** (206 palavras)

> [thoughtful] E na origem? Primeiro precisamos perguntar se existe limite. Lê-se: limite de F quando X tende à origem. Com alfa zero, não tem divisão nenhuma: é a rotação rígida, definida e contínua no centro. Com alfa entre zero e meio, a fórmula original não vale na origem, mas olha o expoente da rapidez: um menos dois alfa é positivo. Distância pequena elevada a um número positivo fica pequena: a rapidez vai a zero quando nos aproximamos. Então o limite é o vetor nulo e, definindo a seta da origem como zero, o campo fica contínuo. Com alfa meio, a rapidez fica um, só que a direção depende do caminho. Chegando pelo eixo xis, o ponto é tê, zero, com tê positivo. Em cima fica zero, tê; embaixo, raiz de tê ao quadrado, que é tê. A seta é zero, um: para cima. Chegando pelo eixo ípsilon, o ponto é zero, tê. Em cima fica menos tê, zero; dividido por tê, menos um, zero: para a esquerda. Dois caminhos, duas setas diferentes: não tem limite. E, com alfa maior que meio, o expoente um menos dois alfa fica negativo: a distância pequena vai para o denominador, e a seta explode perto da origem. Sem limite finito.

**D3b-2** (76 palavras)

> [curious] Lembra do campo que esticava o quadradinho no episódio passado? Ele é o gradiente da metade da diferença entre os quadrados das coordenadas. Confere. Derivando fi em xis, o meio vezes dois xis dá xis. Derivando em ípsilon, o meio vezes menos dois ípsilon dá menos ípsilon. O gradiente é xis, menos ípsilon: exatamente o campo. E, pela regra que acabamos de ver, o rotacional dele é zero. Por isso o quadradinho deformava, mas não girava.

**D3b-4** (112 palavras)

> [curious] E isso vira teste. Alguém mostra este campo e pergunta: existe outro campo cujo rotacional seja ele? Não precisa procurar. Calcula o divergente, uma parcela de cada vez. Na primeira, o ípsilon fica parado e só o xis varia: a derivada de xis é um, e a primeira parcela dá seno de ípsilon. Na segunda, a derivada do cosseno é menos o seno: a segunda dá menos seno de ípsilon. Na terceira, o xis e o ípsilon ficam parados, só o zê varia, e a terceira dá um. Seno menos seno cancela. Total: um. Se ele fosse o rotacional de um campo regular, seu divergente seria zero. Então não existe esse campo.

**D4-6** (259 palavras)

> [curious] Item d: confere com um zoom. No episódio passado, o campo suave deixava as setas arrumadinhas quando a gente ampliava uma região pequena. Aqui, olha: o zoom de dez vezes mostra exatamente o mesmo padrão. E o de cem vezes, também. Isso se chama homogeneidade: multiplicar a posição por um número faz o vetor do campo ser multiplicado pelo mesmo número. Na conta, o número aparece ao quadrado em cima e embaixo da fração, cancela, e sobra o fator que multiplica o vetor posição. [thoughtful] Agora a definição. Ser diferenciável na origem quer dizer: o campo no ponto agá é o valor na origem, mais a tabela vezes agá, mais um erro; e o erro, dividido pelo tamanho de agá, vai a zero. Agá é o passo a partir da origem. Aqui, o valor na origem é zero e a tabela é zero, então o erro é o próprio campo. Testa na diagonal, com o passo agá, agá. Em cima, agá vezes agá; embaixo, agá ao quadrado mais agá ao quadrado: a fração vale meio. Na diagonal, a seta tem sempre metade do tamanho do deslocamento: agá meio, agá meio. O tamanho do erro é agá raiz de dois sobre dois; o do passo, agá raiz de dois. O erro, dividido pelo passo, fica em meio. Para haver diferenciabilidade, essa razão teria que ir a zero. Não vai. Então o desenho não se aproxima da tabela zero. Em qualquer vizinhança, por menor que seja, tem quadradinho crescendo nas diagonais de subida, encolhendo nas outras, e girando para os dois lados.

**D4-7** (317 palavras)

> [thoughtful, emphatic] A tabela errou. Por quê? Item e: calcula a derivada da componente horizontal em relação à coordenada horizontal, fora da origem. A componente horizontal é o quadrado da coordenada horizontal vezes a vertical, dividido pela distância ao quadrado. Regra do quociente: derivada de cima vezes a de baixo, menos a de cima vezes a derivada de baixo, sobre o quadrado do denominador. A derivada de cima é duas vezes o produto das coordenadas, porque o ípsilon fica parado e xis ao quadrado vira dois xis. A de baixo é duas vezes a coordenada horizontal. Substitui no molde e abre os produtos. Dois xis ípsilon vezes xis ao quadrado dá dois xis ao cubo ípsilon. Dois xis ípsilon vezes ípsilon ao quadrado dá dois xis ípsilon ao cubo. E xis ao quadrado ípsilon vezes dois xis dá, de novo, dois xis ao cubo ípsilon. Os termos com a quarta potência se cancelam, e sobra duas vezes a coordenada horizontal vezes o cubo da vertical, sobre a distância à quarta potência. Agora olha essa derivada se aproximando da origem. Nos eixos, ela vale zero, fora do centro: com ípsilon zero, o cubo zera o numerador; com xis zero, o fator xis zera. Na diagonal, as duas coordenadas são iguais. Em cima, dois xis vezes xis ao cubo. Embaixo, xis ao quadrado mais xis ao quadrado, que é dois xis ao quadrado, tudo ao quadrado. Aparece duas vezes a quarta potência em cima e quatro vezes a quarta potência embaixo. Resultado: meio. E vale meio na diagonal inteira, por menor que seja a distância da origem. A derivada não é contínua na origem. O campo não é de classe cê um, e a tabela perde a garantia de ser uma boa aproximação. Repara: o cê um é uma garantia, não uma exigência. Tem campo que não é cê um e mesmo assim é diferenciável. Aqui demonstramos que a aproximação falha.

**D5-9** (119 palavras)

> [thoughtful] Terceiro campo: a primeira componente é a diferença dos quadrados das coordenadas; a segunda, duas vezes o produto delas. Agora a tabela não é constante: muda com a posição. Derivando a diferença dos quadrados em xis, o xis ao quadrado dá duas vezes a horizontal, e o ípsilon ao quadrado, parado, dá zero. Em ípsilon, o xis ao quadrado é que dá zero, e menos duas vezes a vertical fica na primeira linha. Derivando duas vezes o produto, uma coordenada fica parada e a outra vira um: aparecem duas vezes a vertical e duas vezes a horizontal na segunda. Então o ponto importa. Pausa o vídeo e prevê nos três pontos mostrados: um, zero; zero, um; e um, um.

**A1-2** (75 palavras)

> [curious] Primeira: a velocidade só tem componente na direção do canal, e ela não muda ao longo do canal. Monta a tabela pelas derivadas. A primeira componente é zero: as duas derivadas dela são zero. A segunda, um menos xis ao quadrado sobre nove, não tem ípsilon: derivada em ípsilon, zero. Em xis, o um some, e o xis ao quadrado sobre nove vira menos dois xis sobre nove. Divergente: zero mais zero. Divergente zero: incompressível.

**A1-3** (214 palavras)

> [thoughtful] Segunda: as linhas de corrente são retas. Dá vontade de dizer que não gira. Mas o rotacional é a derivada da velocidade ao longo do canal entre as margens, menos a derivada da primeira componente, que é zero. Dá menos dois nonos da coordenada horizontal. Na margem esquerda, menos dois nonos vezes menos três: menos com menos dá mais, seis nonos, que simplifica para dois terços por segundo. Um galho ali gira no sentido anti-horário, no modelo de uma rodinha ideal pequena, perto da margem. Lembra que o rotacional é o dobro da velocidade angular dessa rodinha. Então divide por dois: o galho gira com ômega, a velocidade angular, igual a um terço de radiano por segundo, porque dois terços dividido por dois é um terço. E o período, o T da tela, o tempo de uma volta, é a volta inteira, dois pi, dividida por ômega: dois pi dividido por um terço, que é dois pi vezes três, seis pi. Com pi perto de três vírgula catorze, dá uns dezoito vírgula oito: quase dezenove segundos. Na margem direita, menos dois terços, porque agora é menos dois nonos vezes três positivo: o giro é horário. Bem no centro, com xis zero, a rotação local é zero: o galho desce o rio sem girar.

**A1-5** (96 palavras)

> [thoughtful] Terceira: o atrito. O atrito viscoso vem da deformação: da diferença de velocidade entre camadas vizinhas. Aqui, a primeira deformação é zero menos zero: zero. A segunda é menos dois nonos da coordenada horizontal, mais zero. Na margem, com xis igual a três ou a menos três, o tamanho dela é dois vezes três sobre nove: dois terços. No centro, com xis zero, ela vale zero. Em módulo, é máxima nas margens e zero no centro. É perto das margens que as camadas de água mais deslizam umas sobre as outras: ali o atrito é maior.

**A2-2** (263 palavras)

> [curious] Primeiro: na parede, a componente vertical é zero, então a água não a atravessa: ela desliza. Numa parede de verdade, a viscosidade faz uma camada fina de água grudar nela, e este modelo ideal ignora essa camada. Segundo: a tabela, derivada por derivada. A primeira componente é xis: derivada um em xis, zero em ípsilon. A segunda é menos ípsilon: zero em xis, menos um em ípsilon. Então a tabela tem um e zero em cima, zero e menos um embaixo. Rotacional zero menos zero, zero; divergente um menos um, zero; e primeira deformação um menos menos um, dois. A água não gira e não comprime: só deforma. Uma gota de tinta que desce pelo eixo se achata e se espalha pela parede, sempre com a mesma área. E as linhas de corrente são hipérboles, fora dos eixos: as curvas onde o produto das coordenadas é constante, ípsilon igual a uma constante sobre xis. Confere. Lê-se dê xis ípsilon, dê tê: a taxa de variação do produto no tempo. Regra do produto, agora no tempo: a derivada de xis vezes ípsilon, mais xis vezes a derivada de ípsilon. Andando com a água, a posição muda com a velocidade: a derivada de xis no tempo é u, e a de ípsilon é vê. Então o produto muda pela velocidade horizontal vezes a coordenada vertical, mais a horizontal vezes a velocidade vertical. Com u igual a xis e vê igual a menos ípsilon, dá o produto menos o produto: zero. O produto não muda: a água anda em cima da hipérbole, ou do eixo.

**A2-3** (81 palavras)

> [thoughtful] Terceiro: esse campo é o gradiente da metade da diferença entre os quadrados das coordenadas. Derivando, o meio vezes dois xis dá xis, e o meio vezes menos dois ípsilon dá menos ípsilon. Essa função se chama potencial de velocidade. E o laplaciano dela, escrito nabla dois fi, a soma das duas derivadas segundas, aquela curiosidade do segundo episódio. Derivando de novo: xis em xis dá um, e menos ípsilon em ípsilon dá menos um. Soma: dá um menos um, zero.

**A2-4** (100 palavras)

> [thoughtful, emphatic] E isso não é coincidência. Se a velocidade é um gradiente, o campo é irrotacional, se suficientemente suave: é a primeira das duas regras. Se também tem divergente zero, então o divergente do gradiente é zero. E o divergente do gradiente é o laplaciano: deriva fi xis em xis, deriva fi ípsilon em ípsilon e soma, as duas derivadas segundas. Escoamento irrotacional e incompressível quer dizer laplaciano do potencial igual a zero: é a equação de Laplace. A mesma equação aparece no potencial elétrico em regiões sem cargas e na temperatura de uma chapa em equilíbrio, sob as hipóteses adequadas.

**A4-2** (185 palavras)

> [thoughtful] Elas aparecem quando juntamos as duas componentes num número complexo. O nosso campo é exatamente o quadrado do número complexo com parte real horizontal e imaginária vertical. Abre o quadrado com o molde da soma ao quadrado: o primeiro ao quadrado, mais duas vezes o primeiro vezes o segundo, mais o segundo ao quadrado. O i da tela é a unidade imaginária. Sai o quadrado da horizontal, mais duas vezes i vezes o produto, mais i ao quadrado vezes o quadrado da vertical. E o quadrado da unidade imaginária é menos um: o último termo vira menos o quadrado da vertical. Junta o que não tem i e o que tem i. Sobra a diferença dos quadrados na parte real e duas vezes o produto na parte imaginária: a primeira e a segunda componente do campo. [curious] Confere as equações. A derivada horizontal da primeira é dois xis, igual à derivada vertical da segunda. A derivada vertical da primeira é menos dois ípsilon, igual a menos a derivada horizontal da segunda. Passou. E toda função complexa derivável satisfaz essas equações, como o cubo e a exponencial.

**A4-3** (167 palavras)

> [curious] Agora lê como transformação. A tabela desse campo, a do terceiro campo do desafio, tem a forma a, menos b, b, a, com a igual a dois xis e b igual a dois ípsilon. Uma tabela assim é um número vezes uma rotação: o número é a raiz de a ao quadrado mais b ao quadrado, que dá duas vezes a distância. No ponto um, um, ela é dois, menos dois, dois, dois: dois raiz de dois vezes uma rotação de quarenta e cinco graus. As duas colunas têm o mesmo tamanho e são perpendiculares. Onde a derivada complexa não é zero, uma tabela assim só gira e muda a escala: quadradinhos pequenos viram quadradinhos, maiores ou menores, mas sempre com ângulos retos. Isso se chama mapa conforme. E você conhece um: o mapa-múndi de Mercator preserva os ângulos, mas distorce as áreas, ainda mais perto dos polos. Por isso a Groenlândia aparece quase do tamanho da África, mas com o formato certo em cada pedacinho.

**A4-4** (88 palavras)

> [thoughtful] E o irmão desse campo, com o sinal da segunda componente trocado: xis ao quadrado menos ípsilon ao quadrado, e menos dois xis ípsilon. As derivadas da primeira são dois xis e menos dois ípsilon; as da segunda, menos dois ípsilon e menos dois xis. Rotacional: menos dois ípsilon, menos menos dois ípsilon, zero. Divergente: dois xis menos dois xis, zero. Rotacional zero, divergente zero, e as duas deformações, quatro xis e menos quatro ípsilon, só zeram na origem. Esse irmão não gira nem comprime: só deformação local.

**A3-3** (148 palavras)

> [curious] Agora usa a fórmula que a gente guardou. O rotacional é dois menos dois alfa, sobre a distância ao quadrado elevada a alfa. Para ser zero fora do fio, olha o denominador: a distância ao quadrado é positiva fora do fio, e uma potência de número positivo nunca é zero. Então o numerador zera: dois menos dois alfa igual a zero. Passa o dois alfa para o outro lado: dois igual a dois alfa, e alfa igual a um. Então o tamanho do campo: em cima, o tamanho de menos ípsilon, xis, que é a distância, como no terceiro degrau. Embaixo, a distância elevada a dois alfa, que agora é dois. Fica a distância dividida pela distância ao quadrado: um sobre a distância. O campo do fio cai com um sobre a distância. A intensidade ainda depende da corrente; o que a conta escolhe é como ela cai.

**A3-4** (145 palavras)

> [thoughtful] Faz o mesmo com um fio carregado. O campo elétrico aponta para fora para carga positiva, então ele tem a forma da explosão radial do terceiro degrau: xis, ípsilon, dividido pela potência da distância. Fora do fio não tem carga, e a lei de Gauss dá divergente zero. Calcula o divergente, como no terceiro degrau. A primeira parcela é xis vezes a potência: pela regra do produto, sai a própria potência, menos dois alfa xis ao quadrado vezes a potência com um a menos. A segunda é igual, com ípsilon. Somando, aparecem duas vezes a potência e, de novo, dois alfa vezes a distância ao quadrado vezes a potência com um a menos, que é dois alfa vezes a potência. Divergente: dois menos dois alfa, dividido pela potência da distância. Igual a zero: alfa um, e o campo também cai com um sobre a distância.

**A3-5** (344 palavras)

> [excited] E uma carga pontual no espaço? Escreve o campo como o vetor posição dividido pela distância elevada a um expoente. O X maiúsculo é o vetor posição; as barras duplas, a distância; p, o expoente. No plano, o divergente teria dois menos esse expoente. Agora, no espaço. Faz a conta de uma parcela: a derivada da coordenada horizontal dividida pela distância elevada ao expoente, em relação à horizontal. [thoughtful] Primeiro, a derivada da distância. A distância é a raiz de xis ao quadrado mais ípsilon ao quadrado mais zê ao quadrado, e raiz é potência meio. O meio desce, a potência fica com menos meio, e a cadeia traz dois xis. O meio com o dois cancela. A derivada da distância, nessa direção, é a coordenada horizontal dividida pela distância. Agora a regra do produto, com xis vezes a distância elevada a menos p. A derivada de xis é um: sobra um sobre a distância elevada ao expoente. Na outra parte, menos p vezes a distância elevada a menos p menos um, vezes a derivada da distância, xis sobre a distância. Xis vezes xis dá xis ao quadrado, e as potências da distância se juntam: menos p menos um, mais menos um, dá menos p menos dois. Então dá um sobre a distância elevada ao expoente, menos o expoente vezes o quadrado da coordenada horizontal, sobre a distância elevada ao expoente mais dois. As outras parcelas são iguais, cada uma com sua coordenada. [excited] Agora soma. Os primeiros termos dão três vezes a mesma potência inversa; os quadrados das coordenadas somam a distância ao quadrado, que cancela o mais dois do expoente. Sobra o número de parcelas menos o expoente, sobre a distância elevada ao expoente. No plano são duas parcelas; no espaço, três. O divergente no espaço é três menos o expoente, sobre a distância elevada a esse expoente. Para zerar, o expoente é três. A intensidade fica a distância dividida pela distância ao cubo: um sobre a distância ao quadrado. Essa é a dependência de duas leis: a de Coulomb e a da gravitação.


---

## Anexo B · Roteiro de sincronia (frase-gatilho → evento), na ordem da fala
Marcas: `=` gatilho que já existe no código (fica) · `+` gatilho novo · `le` leitura com sublinhado (existe) · `ate` fim do sublinhado (existe). Copie as frases **letra por letra, com acento**.


### D3-2

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | tangentes às circunferências | Create(circs) (como hoje) |
| 2 | `=` | o vetor de cima tem tamanho | escreve n1 (‖v‖ = ‖(−y, x)‖ / s^α) |
| 3 | `+` | o sinal some no quadrado | K1 nasce em caneta: ‖(−y, x)‖ = √((−y)² + x²); o (−y, x) voa do numerador de fv; gm K1 → K1b = √(x² + y²) = r; Create(raio); r e raio acendem AMB |
| 4 | `+` | embaixo a distância ao quadrado elevada | K2 nasce: s^α = (x² + y²)^α ; o s^α voa de n1 |
| 5 | `+` | potência de potência multiplica | gm K2 → K2b = (r²)^α = r^{2α} |
| 6 | `=` | então a rapidez é a distância | gm n1 → n2 (‖v‖ = r / r^{2α}) com voos: r de K1b, r^{2α} de K2b |
| 7 | `+` | na divisão os expoentes se subtraem | gm n2 → n3 (‖v‖ = r^{1−2α}); o 1 do r e o 2α viram 1 − 2α; K1b, K2b e raio saem (fusão R13) |
| 8 | `=` | com alfa zero a rapidez cresce | acende n3 + seletor α = 0 (como hoje) |
| 9 | `=` | com alfa meio a rapidez | troca_a(.5) |
| 10 | `=` | com alfa um ela cai | troca_a(1) |

### D3-3

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | agora a conta do rotacional | R0 (como hoje) |
| 2 | `=` | na tela p e q | leituras P, Q e ∂ (como hoje) |
| 3 | `le` | P e Q são as duas componentes |  |
| 4 | `le` | o d arredondado é a derivada parcial |  |
| 5 | `ate` | e o d arredondado | fim do sublinhado (como hoje) |
| 6 | `ate` | o rotacional é a derivada | fim do sublinhado (como hoje) |
| 7 | `=` | menos a derivada da componente horizontal | acende dP (como hoje) |
| 8 | `=` | a componente vertical é a coordenada | QL: só 'Q =' + x voa de fv + s^{−α} (sem o 's = x²+y²' ainda) |
| 9 | `+` | para encurtar a tela chama | QL: escreve ', s =' e o x²+y² voa do denominador de fv; junta(QL) |
| 10 | `=` | regra do produto | escreve PR (molde aplicado: ∂Q/∂x = (x)′ s^{−α} + x (s^{−α})′) |
| 11 | `+` | a derivada do primeiro vezes o segundo | acende (x)′·s^{−α} e depois x·(s^{−α})′ (0,6 s cada, AMB) |
| 12 | `=` | a primeira parte dá a própria | P2: escreve '=' e voa s^{−α} da 1ª parcela de PR |
| 13 | `+` | porque a derivada de xis em relação | K-linha: K1 = (x)′ = 1 (caneta); o 1 voa para P2 ('1 ·') |
| 14 | `=` | a segunda pela regra da cadeia | P2: '+ x · (' com o x voando de PR |
| 15 | `+` | o expoente desce | K2 = (s^{−α})′ = −α s^{−α−1} · ∂s/∂x : o −α voa do EXPOENTE de PR (cópia desce), s^{−α−1} em caneta |
| 16 | `+` | e ainda multiplica pela derivada de dentro | acende ∂s/∂x de K2 (CAMPO2) |
| 17 | `+` | a derivada de esse em relação a xis | K3 = ∂s/∂x = 2x + 0 = 2x : x² do QL acende AMB e vira 2x; y² acende CORAL e vira 0; gm K2 → K2b (−α s^{−α−1}·2x) |
| 18 | `=` | vezes duas vezes a coordenada horizontal | o bloco −α s^{−α−1}·2x voa de K2b para P2; fecha ')'; junta(P2) |
| 19 | `+` | xis vezes dois xis dá dois | gm P2 → P3 (= s^{−α} − 2α x² s^{−α−1}); mapa: '1·' some, x e x de 2x → x², o − do −α sai para fora |
| 20 | `+` | agora o truque | K1, K2b, K3 saem; K4 nasce na K-linha: s^{−α} = s · s^{−α−1} (com o expoente escrito: −α = 1 + (−α − 1)) |
| 21 | `=` | põe a potência com um a menos | gm P3 → P4 (= s·s^{−α−1} − 2αx² s^{−α−1}, s·s^{−α−1} voa de K4) → P5 (= s^{−α−1}(s − 2αx²)); depois FUSÃO PR+P2..P5+K4 → F2 (∂Q/∂x = s^{−α−1}(s − 2αx²)) na linha 580 |
| 22 | `=` | a outra derivada é igualzinha | gm QL → PQ (como hoje, −y voa de fv) |
| 23 | `+` | a componente horizontal é menos ípsilon | G1 = ∂P/∂y = (−y)′ s^{−α} + (−y)(s^{−α})′ (cópia do molde de PR, mapa só troca x → −y) |
| 24 | `+` | a derivada de menos ípsilon em relação | G2 = −1·s^{−α} + (−y)(−α s^{−α−1}·2y) : o −1 nasce acima de (−y)′ e voa |
| 25 | `+` | e a cadeia agora traz duas vezes | acende o ·2y de G2 (y² do PQ acende MG por 0,6 s) |
| 26 | `+` | sai menos a potência mais | gm G2 → G3 (= −s^{−α} + 2αy² s^{−α−1}); (−y)·(−α)·2y → +2αy² |
| 27 | `+` | em evidência o mesmo parêntese | gm G3 → G4 (= −s·s^{−α−1} + 2αy² s^{−α−1}) → G5 (= −s^{−α−1}(s − 2αy²)) |
| 28 | `=` | e o sinal trocado | o '−' da frente de G5 acende CORAL; FUSÃO G1..G5 → F3 (∂P/∂y = −s^{−α−1}(s − 2αy²)) na linha 660 |
| 29 | `+` | ao subtrair menos com menos | gm R0 → RS (copia, voos de F2 e F3, como hoje) e logo gm RS → RS2 (o '−(−' vira '+') |
| 30 | `=` | a distância ao quadrado aparece duas vezes | RS2 → RS3 (como hoje) |
| 31 | `=` | os dois termos com alfa se juntam | RS3 → RS4 (como hoje) |
| 32 | `=` | que é a distância ao quadrado de novo | RS4 → RS5 (como hoje) |
| 33 | `+` | no parêntese sobra dois esse | acende (2s − 2αs) de RS5 |
| 34 | `+` | esse em evidência vezes dois | gm RS5 → RS5b (= s^{−α−1} · s (2 − 2α)); os dois s se juntam num s fora do parêntese |
| 35 | `+` | e esse vezes a potência com um | chip K5 1 s: s · s^{−α−1} = s^{−α}; gm RS5b → RS5c (= s^{−α}(2 − 2α)) |
| 36 | `=` | sobra uma fórmula curtinha | RS5c → RS6 ((2 − 2α)/s^α) → RS7 (como hoje) |
| 37 | `=` | e o divergente | fusão para RT no topo (como hoje) |
| 38 | `=` | agora é a soma | DV (como hoje) |
| 39 | `+` | na primeira o menos ípsilon é constante | DP só até '= −y · ∂(s^{−α})/∂x' (o −y acende GEO: constante) |
| 40 | `+` | na segunda o xis é constante | DQ só até '= x · ∂(s^{−α})/∂y' (cópia de DP, mapa) |
| 41 | `=` | só a regra da cadeia trabalha | DP e DQ ganham '= −y(−α s^{−α−1}·2x)' e '= x(−α s^{−α−1}·2y)' |
| 42 | `=` | e sai o mesmo termo | DP e DQ ganham os resultados ±2αxy s^{−α−1} |
| 43 | `=` | uma vez com sinal de mais | DS (como hoje) |
| 44 | `=` | eles se cancelam zero | cancela + DZ (como hoje) |
| 45 | `=` | nenhum desses redemoinhos | quadradinho anda (como hoje) |

### D3-6

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | lê-se limite de f quando x tende à origem | lim (como hoje) |
| 2 | `le` | limite de F quando X tende à origem |  |
| 3 | `ate` | com alfa zero não tem divisão |  |
| 4 | `=` | com alfa entre zero e meio | t1[0], t2[0] (como hoje) |
| 5 | `+` | mas olha o expoente da rapidez | rz0 = ‖v‖ = r^{1−2α} (topo, 1320, 240) |
| 6 | `+` | distância pequena elevada a um número | gm rz0 → rz = 0 < α < ½ ⇒ 1 − 2α > 0 ⇒ r^{1−2α} → 0 |
| 7 | `=` | a rapidez vai a zero | acende o '→ 0' de rz (CAMPO2) |
| 8 | `=` | o campo fica contínuo | t3[0] (como hoje) |
| 9 | `=` | com alfa meio a rapidez fica um | palco α = ½ (como hoje), o1 |
| 10 | `+` | chegando pelo eixo xis | o2a = X = (t, 0): v = (−0, t)/√(t²) (o ponto laranja anda pelo eixo x, como hoje) |
| 11 | `+` | a seta é zero um | gm o2a → o2 = (0, t)/t = (0, 1); a última seta do caminho x e o (0,1) acendem juntos |
| 12 | `+` | chegando pelo eixo ípsilon | o3a = X = (0, t): v = (−t, 0)/√(t²) (o ponto do eixo y) |
| 13 | `+` | dividido por tê menos um | gm o3a → o3 = (−t, 0)/t = (−1, 0); acende com a seta |
| 14 | `=` | não tem limite | NÃO TEM LIMITE (como hoje) |
| 15 | `=` | e com alfa maior que meio | volta aos cartões (como hoje) |
| 16 | `+` | o expoente um menos dois alfa fica negativo | rz2 no topo: α > ½ ⇒ 1 − 2α < 0 ⇒ r^{1−2α} = 1/r^{2α−1} → ∞ |
| 17 | `=` | a seta explode | t3[2] (como hoje) |

### D3b-2

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | lembra do campo que esticava | fusão → RZ (como hoje) |
| 2 | `=` | ele é o gradiente da metade | PH1 = φ = ½(x² − y²) (linha 510) |
| 3 | `+` | derivando fi em xis | PH2 parte 1: φ_x = ½·2x = x (linha 575) |
| 4 | `+` | derivando em ípsilon | PH2 parte 2: φ_y = ½·(−2y) = −y |
| 5 | `+` | o gradiente é xis menos ípsilon | PH3 = ∇φ = (φ_x, φ_y) = (x, −y) (linha 640), x e −y voam de PH2 |
| 6 | `+` | e pela regra que acabamos | acende RZ (rot ∇φ = 0) VIO |
| 7 | `=` | por isso o quadradinho deformava | quadradinho anda + DEFORMA, MAS NÃO GIRA (linha 715) |

### D3b-4

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | e isso vira teste | como hoje |
| 2 | `=` | existe outro campo cujo rotacional | como hoje |
| 3 | `=` | calcula o divergente | DV (como hoje) + RR só com '=' |
| 4 | `+` | na primeira o ípsilon fica parado | em t1 o sen y acende GEO (parado) e o x acende AMB |
| 5 | `=` | a primeira parcela dá seno | t1 voa para RR: '1·sen y' (o 1 = derivada de x) |
| 6 | `+` | na segunda a derivada do cosseno | t2 acende MG |
| 7 | `=` | a segunda dá menos seno | t2 voa para RR: '+(−sen y)' |
| 8 | `+` | na terceira o xis e o ípsilon | em t3 o −xy acende GEO e o z acende |
| 9 | `=` | e a terceira dá um | t3 voa para RR: '+1' |
| 10 | `+` | seno menos seno cancela | gm RR → RR2 (= sen y − sen y + 1); cancela s1, s2 |
| 11 | `=` | total um | R2 (= 1 ≠ 0) |
| 12 | `=` | então não existe | como hoje |

### D4-6

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | item d confere com um zoom | como hoje |
| 2 | `=` | deixava as setas arrumadinhas | como hoje |
| 3 | `=` | aqui olha o zoom de dez vezes | como hoje |
| 4 | `=` | e o de cem vezes também | como hoje |
| 5 | `=` | multiplicar a posição por um número | HS (faixa de baixo, como hoje) |
| 6 | `=` | o número aparece ao quadrado em cima | cancela + HS2 (como hoje) |
| 7 | `+` | agora a definição | o painel da DIREITA (×100) sai inteiro; a coluna nasce no lugar dele (x ≥ 1100): DF1 = F(H) = F(0) + J H + erro(H) |
| 8 | `+` | e o erro dividido pelo tamanho | DF2 = ‖erro(H)‖/‖H‖ → 0 + legenda DIFERENCIÁVEL EM 0 (GEO) |
| 9 | `+` | aqui o valor na origem é zero | DF3 parte 1: F(0) = 0, J = 0 (o ponto da origem do painel esquerdo acende; legenda pequena DO ITEM C) |
| 10 | `+` | então o erro é o próprio campo | DF3 parte 2: ⇒ erro(H) = F(H) |
| 11 | `+` | testa na diagonal com o passo | painel esquerdo: o ponto H = (h, h) na diagonal, o vetor H (traço BR fino) e a seta do campo nele (CAMPO2); DF4 = H = (h, h): F(h, h) = (h·h)/(h² + h²) · (h, h) |
| 12 | `+` | a fração vale meio | gm DF4 → DF4b = (h²/2h²)(h, h) = ½(h, h) |
| 13 | `=` | na diagonal a seta tem sempre metade | gm DF4b → DF4c = ½(h, h) = (h/2, h/2); a seta do painel e o (h/2, h/2) acendem juntos |
| 14 | `+` | o tamanho do erro é | DF5 parte 1: ‖erro‖ = √(h²/4 + h²/4) = h√2/2 |
| 15 | `+` | o do passo agá raiz de dois | DF5 parte 2: ‖H‖ = √(h² + h²) = h√2 |
| 16 | `=` | pelo passo fica em meio | DF6 = ‖erro‖/‖H‖ = (h√2/2)/(h√2) = ½; o ½ acende AMB |
| 17 | `=` | essa razão teria que ir a zero | DF6 ganha '↛ 0' em CORAL |
| 18 | `+` | então o desenho não se aproxima | acende o painel esquerdo inteiro (moldura CAMPO2, 0,8 s) |
| 19 | `=` | tem quadradinho crescendo | os 4 quadradinhos andam NO PAINEL ESQUERDO (×1, mesmo desenho) |

### D4-7

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | item e calcula a derivada | como hoje |
| 2 | `=` | a componente horizontal é o quadrado | PQ (como hoje) |
| 3 | `=` | regra do quociente | QM (como hoje) |
| 4 | `=` | a derivada de cima é duas vezes | ND parte 1: N′ = ∂(x²y)/∂x = 2xy (o x² de N acende AMB) |
| 5 | `+` | porque o ípsilon fica parado | o y de N′ acende GEO (constante) |
| 6 | `+` | a de baixo é duas vezes | ND parte 2: D′ = ∂(x² + y²)/∂x = 2x + 0 = 2x |
| 7 | `+` | substitui no molde e abre | gm QM → Q1 (copia), voos: N′ e D′ de ND, N e D da QM |
| 8 | `+` | dois xis ípsilon vezes xis ao quadrado | Q2 termo a: 2x³y (cópias de 2xy e x² de Q1) |
| 9 | `+` | dois xis ípsilon vezes ípsilon ao quadrado | Q2 termo b: + 2xy³ |
| 10 | `+` | e xis ao quadrado ípsilon vezes dois | Q2 termo c: − 2x³y |
| 11 | `=` | os termos com a quarta potência | cancela a, c + Q3 (como hoje) |
| 12 | `=` | agora olha essa derivada | fusão → RES (como hoje) |
| 13 | `=` | nos eixos ela vale zero | pontos dos eixos + rótulos 0 (como hoje); a legenda NOS EIXOS: 0 SAI |
| 14 | `+` | com ípsilon zero o cubo zera | EX parte 1: y = 0: 2x·0³/(x²)² = 0 |
| 15 | `+` | com xis zero o fator xis zera | EX parte 2: x = 0: 2·0·y³/(y²)² = 0 |
| 16 | `=` | na diagonal as duas coordenadas são iguais | DG parte 1: y = x: 2x·x³/(x² + x²)² (copia de RES) |
| 17 | `+` | embaixo xis ao quadrado mais xis | DG parte 2: = 2x⁴/(2x²)² |
| 18 | `=` | duas vezes a quarta potência | DG parte 3: = 2x⁴/(4x⁴) = ½; o ½ acende AMB |
| 19 | `=` | e vale meio na diagonal inteira | como hoje |
| 20 | `=` | o campo não é de classe | como hoje |
| 21 | `=` | e a tabela perde a garantia | como hoje |
| 22 | `=` | o cê um é uma garantia | como hoje |
| 23 | `=` | tem campo que não é | como hoje |
| 24 | `=` | que a aproximação falha | como hoje |

### D5-9

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | terceiro campo | como hoje |
| 2 | `=` | agora a tabela não é constante | como hoje |
| 3 | `=` | derivando a diferença dos quadrados | célula (0,0) por deriva com passo intermediário: x² − y² → 2x − 0 → 2x |
| 4 | `+` | em ípsilon o xis ao quadrado | célula (0,1): x² − y² → 0 − 2y → −2y (no plano da tabela, ESTE vira o gatilho da célula; 'e menos duas vezes a vertical' fica sem evento) |
| 5 | `=` | e menos duas vezes a vertical | sem evento novo (a célula já está a caminho) |
| 6 | `=` | derivando duas vezes o produto | célula (1,0): 2xy → 2·y·1 → 2y; célula (1,1) logo depois: 2xy → 2·x·1 → 2x |
| 7 | `=` | pausa o vídeo e prevê | como hoje |

### A1-2

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | primeira a velocidade só tem | en sai (como hoje) |
| 2 | `=` | e ela não muda ao longo do canal | a coluna de setas do meio acende CAMPO2 (mesmo tamanho de cima a baixo) |
| 3 | `+` | monta a tabela pelas derivadas | escreve Jm (molde ∂) e os parênteses de Jv (vazios) |
| 4 | `+` | a primeira componente é zero | células (0,0) e (0,1) por deriva_cel: o 0 de v voa, 0 → 0 |
| 5 | `+` | a segunda um menos xis | célula (1,1): 1 − x²/9 → 0 (tudo CORAL: não tem y) |
| 6 | `+` | em xis o um some | célula (1,0): 1 − x²/9 → 0 − 2x/9 → −2x/9 |
| 7 | `+` | divergente zero mais zero | DV + DV2 (voos das células, como hoje) |
| 8 | `=` | divergente zero incompressível | acende o 0 final de DV2 (D) |

### A1-3

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | o rotacional é a derivada | RT (como hoje) |
| 2 | `+` | menos a derivada da primeira componente | acende a célula (0,1) = 0 |
| 3 | `=` | dá menos dois nonos | RT → RT2 (como hoje) |
| 4 | `=` | na margem esquerda menos dois nonos | XR parte 1: rot(−3) = −2(−3)/9 ; o −3 voa do rótulo x = −3 do palco |
| 5 | `+` | menos com menos dá mais | gm XR → XRb (= 6/9) |
| 6 | `+` | que simplifica para dois terços | gm XRb → XRc (= 2/3): o 6 e o 9 acendem e viram 2 e 3 (÷3) |
| 7 | `=` | um galho ali gira | acende (como hoje) |
| 8 | `=` | lembra que o rotacional é o dobro | acende (como hoje) |
| 9 | `=` | o galho gira com ômega | OM1 = ω = rot/2 = (2/3)/2 = 1/3 rad/s (o 2/3 voa de XRc) |
| 10 | `le` | ômega, a velocidade angular |  |
| 11 | `ate` | igual a um terço |  |
| 12 | `=` | e o período o t da tela | OM2 = T = 2π/ω (linha 815) |
| 13 | `le` | o período, o T da tela, o tempo de uma volta |  |
| 14 | `ate` | dois pi dividido por um terço |  |
| 15 | `+` | que é dois pi vezes três | OM2 ganha '= 2π/(1/3) = 2π·3 = 6π' (o 1/3 voa de OM1) |
| 16 | `+` | com pi perto de três vírgula catorze | OM2 ganha '≈ 18,8 ≈ 19 s' |
| 17 | `=` | na margem direita menos dois terços | XR vira chip 'rot(−3) = 2/3' e ganha 'rot(3) = ...' (o 3 voa do rótulo x = 3) |
| 18 | `+` | porque agora é menos dois nonos | 'rot(3) = −2·3/9 = −2/3' |
| 19 | `+` | bem no centro com xis zero | 'rot(0) = 0' (as setas do meio acendem) |

### A1-5

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | terceira o atrito | fusão ω, T → XR3 (como hoje) |
| 2 | `=` | o atrito viscoso vem da deformação | como hoje |
| 3 | `=` | da diferença de velocidade entre camadas | como hoje |
| 4 | `=` | aqui a primeira deformação | DD1 (linha 745) = d₁ = P_x − Q_y = 0 − 0 = 0 (voos das células) |
| 5 | `+` | a segunda é menos dois nonos | DD2 (linha 810) = d₂ = Q_x + P_y = −2x/9 + 0 = −2x/9 |
| 6 | `+` | na margem com xis igual a três | DD3 (linha 880) = ∣d₂(±3)∣ = 2·3/9 = 2/3 (as margens acendem LIMA) |
| 7 | `+` | no centro com xis zero | DD3 ganha ', d₂(0) = 0' |
| 8 | `=` | máxima nas margens | legenda ATRITO VISCOSO: MÁXIMO NAS MARGENS (faixa de baixo, y 945) |

### A2-2

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | na parede a componente vertical é zero | como hoje |
| 2 | `=` | numa parede de verdade | como hoje |
| 3 | `+` | segundo a tabela derivada por derivada | escreve o molde Jm vazio (∂ nas 4 posições) + os moldes Ms (como hoje) |
| 4 | `+` | a primeira componente é xis | células (0,0) e (0,1) por deriva_cel a partir do x de VV: x → 1 ; x → 0 |
| 5 | `+` | a segunda é menos ípsilon | células (1,0) e (1,1) a partir do −y de VV: −y → 0 ; −y → −1 |
| 6 | `=` | a tabela tem um e zero | acende as 4 células (BR) |
| 7 | `=` | rotacional zero | como hoje (laço MS) |
| 8 | `=` | divergente um menos um | como hoje |
| 9 | `=` | primeira deformação um menos | como hoje |
| 10 | `=` | uma gota de tinta | como hoje |
| 11 | `=` | e as linhas de corrente são hipérboles | hipérboles + o bloco sai (como hoje) |
| 12 | `+` | ípsilon igual a uma constante sobre xis | HP (linha 340) = xy = c ⇒ y = c/x |
| 13 | `=` | lê-se dê xis ípsilon dê tê | DT parte 1 (linha 420): d(xy)/dt = (como hoje) |
| 14 | `le` | dê xis ípsilon, dê tê: a taxa de variação do produto no tempo |  |
| 15 | `ate` | andando com a água | fica como está (o sublinhado agora dura até a frase da posição; aceitável, ≤ 9 s) |
| 16 | `+` | regra do produto agora no tempo | DT parte 2: = (dx/dt)·y + x·(dy/dt) |
| 17 | `+` | a posição muda com a velocidade | CH (linha 500) = dx/dt = u, dy/dt = v (o u e o v voam de VV '(u, v)') |
| 18 | `=` | o produto muda pela velocidade horizontal | gm DT → DT2 (= u·y + x·v), u e v voam de CH |
| 19 | `=` | mais a horizontal vezes a velocidade vertical | acende x·v |
| 20 | `+` | com u igual a xis | D2 (linha 580) = x·y + x·(−y), voos de VV |
| 21 | `=` | dá o produto menos o produto | D3, cancela, D4 (como hoje, na linha 580) |
| 22 | `=` | o produto não muda | rótulo xy = 1, legenda pn (linha 650), gota (como hoje) |

### A2-3

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | esse campo é o gradiente | FUSÃO HP/DT/CH/D4/pn → chip 'd(xy)/dt = 0' (linha 420; sai daqui do A2-4); PH1 = φ = ½(x² − y²) (linha 500) |
| 2 | `+` | derivando o meio vezes dois xis | PH2 (linha 570) = φ_x = ½·2x = x |
| 3 | `+` | e o meio vezes menos dois ípsilon | PH2 ganha ', φ_y = ½·(−2y) = −y ⇒ ∇φ = v' (o v voa de VV) |
| 4 | `+` | essa função se chama potencial | legenda POTENCIAL DE VELOCIDADE (GEO) ao lado do φ |
| 5 | `=` | e o laplaciano dela | LP molde (linha 710) (como hoje) |
| 6 | `=` | escrito nabla dois fi | leitura (como hoje) |
| 7 | `le` | nabla dois fi, a soma das duas derivadas segundas |  |
| 8 | `ate` | aquela curiosidade do segundo episódio |  |
| 9 | `+` | derivando de novo | gm PH2 → LX (copia; φ_x = x → φ_xx = 1; φ_y = −y → φ_yy = −1) (linha 640) |
| 10 | `=` | dá um menos um | LP ganha '= 1 + (−1) = 0' (como hoje) |

### A2-4

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | se a velocidade é um gradiente | C1a (como hoje; a fusão do produto já foi feita no A2-3) |
| 2 | `+` | é a primeira das duas regras | chip de lembrança 'rot ∇φ = 0' (VIO, 1,5 s) ao lado de C1a |
| 3 | `=` | se também tem divergente zero | C1b |
| 4 | `=` | então o divergente do gradiente é zero | C1c |
| 5 | `=` | e o divergente do gradiente é o laplaciano | C2 parte 1: div ∇φ = ∂(φ_x)/∂x + ∂(φ_y)/∂y |
| 6 | `+` | deriva fi xis em xis | C2 parte 2: = φ_xx + φ_yy = ∇²φ |
| 7 | `=` | quer dizer laplaciano do potencial igual a zero | C2 ganha '= 0' |
| 8 | `=` | aparece no potencial elétrico | como hoje |
| 9 | `=` | e na temperatura de uma chapa | como hoje |

### A4-1

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | deformação zero em todo lugar | LAYOUT A: palco = campo ③ (F3) com eixos; coluna: D1 (linha 280), D2 (linha 360) |
| 2 | `=` | iguala cada deformação a zero | gm D1 → D1b (como hoje) |
| 3 | `=` | e a derivada vertical da primeira | gm D2 → D2b (como hoje) |
| 4 | `+` | essas são as equações de cauchy | legenda EQUAÇÕES DE CAUCHY-RIEMANN (GEO, linha 430) |

### A4-2

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | o nosso campo é exatamente o quadrado | acende o campo ③ do palco; FZ0 = F = (x² − y², 2xy) (linha 510) |
| 2 | `=` | abre o quadrado | Z0 (linha 590) = (x + iy)² |
| 3 | `+` | com o molde da soma ao quadrado | MO (linha 660, 30 px, GEO) = (a + b)² = a² + 2ab + b² |
| 4 | `=` | o i da tela é a unidade imaginária | leitura do i (como hoje) |
| 5 | `le` | o i da tela é a unidade imaginária |  |
| 6 | `ate` | o quadrado da horizontal |  |
| 7 | `+` | mais duas vezes i vezes o produto | Z1 = (x + iy)² = x² + 2x(iy) + (iy)²: a = x e b = iy voam de Z0 para os lugares do molde; gm → = x² + 2ixy + i²y² |
| 8 | `=` | é menos um | chip I2 (linha 660, no lugar de MO, que sai) = i² = −1; gm Z1 → Z2 (= x² + 2ixy − y²), o −1 voa do chip |
| 9 | `+` | junta o que não tem i | gm Z2 → Z3 (= (x² − y²) + i(2xy)): x² e −y² se juntam, 2ixy vira i(2xy) |
| 10 | `=` | sobra a diferença dos quadrados | (x² − y²) e (2xy) acendem e voam para FZ0, que acende (fecha o círculo) |
| 11 | `+` | a primeira e a segunda componente | chaves P e Q sob as componentes de FZ0 (como as chaves do D5) |
| 12 | `+` | confere as equações | D1b, D2b e Z0..Z3 saem; CR1 (linha 600) = P_x = 2x |
| 13 | `+` | igual à derivada vertical da segunda | CR1 ganha '= Q_y = 2x ✓' |
| 14 | `+` | a derivada vertical da primeira é menos | CR2 (linha 680) = P_y = −2y |
| 15 | `+` | igual a menos a derivada horizontal | CR2 ganha '= −Q_x = −2y ✓' |
| 16 | `+` | passou | os dois ✓ acendem CAMPO2 |
| 17 | `=` | e toda função complexa derivável | legenda (GEO, linha 760) TODA FUNÇÃO COMPLEXA DERIVÁVEL: z³, eᶻ |

### A4-3

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | agora lê como transformação | o palco vira LAYOUT B: malha à esquerda (Malha + Marcas + círculo pequeno, como o A4-1 de hoje) e a malha a ser transformada à direita; a coluna vira faixa de baixo |
| 2 | `+` | a tabela desse campo | JC1 na faixa (y 958, x 140) = J = (2x −2y; 2y 2x) |
| 3 | `+` | tem a forma a menos b | JC1 ganha '= (a −b; b a), a = 2x, b = 2y' |
| 4 | `+` | uma tabela assim é um número vezes | gm JC1 → JC2 = (a −b; b a) = √(a² + b²)·(cos θ −sen θ; sen θ cos θ) |
| 5 | `+` | que dá duas vezes a distância | JC2 ganha ', √(a² + b²) = 2√(x² + y²) = 2r' |
| 6 | `+` | no ponto um um ela é | gm JC2 → JC3 = (1,1): J = (2 −2; 2 2) = 2√2·(cos 45° −sen 45°; sen 45° cos 45°) |
| 7 | `+` | as duas colunas têm o mesmo tamanho | no painel da direita, no ponto (1,1), as duas colunas (2,2) e (−2,2) em setas finas BR com a marca de ângulo reto |
| 8 | `=` | quadradinhos pequenos viram quadradinhos | morfose z^s + círculo (o morfose agora começa aqui; ver C17) |
| 9 | `=` | mas sempre com ângulos retos | acende marcas (como hoje) |
| 10 | `=` | o mapa múndi de mercator | como hoje |
| 11 | `=` | preserva os ângulos | como hoje |
| 12 | `=` | por isso a groenlândia aparece | como hoje |

### A4-4

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | e o irmão desse campo | JC3 sai; I0 na faixa (y 930, x 140) = F = (x² − y², −2xy) |
| 2 | `+` | as derivadas da primeira são | I1 (y 930, à direita de I0) = J = (2x −2y; ⋯): a 1ª linha em caneta |
| 3 | `+` | as da segunda menos dois ípsilon | I1 ganha a 2ª linha (−2y −2x) |
| 4 | `+` | rotacional menos dois ípsilon | I2 (y 995) = rot = −2y − (−2y) = 0 |
| 5 | `+` | divergente dois xis menos | I2 ganha ', div = 2x − 2x = 0' |
| 6 | `=` | rotacional zero divergente zero | acende os dois 0 |
| 7 | `+` | e as duas deformações quatro xis | I3 (y 995, à direita) = d₁ = 4x, d₂ = −4y |
| 8 | `+` | esse irmão não gira | SÓ DEFORMA (LIMA) |

### A3-3

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | agora usa a fórmula que a gente guardou | como hoje |
| 2 | `=` | para ser zero | RB0 (como hoje) |
| 3 | `+` | olha o denominador | DEN (linha 545) = (x² + y²)^α > 0 : o denominador de RB0 voa (cópia) |
| 4 | `=` | o numerador zera | N0 (linha 615) (como hoje); DEN sai |
| 5 | `+` | passa o dois alfa para o outro lado | o −2α de N0 acende CORAL |
| 6 | `=` | dois igual a dois alfa | N0 → N1 (como hoje) |
| 7 | `=` | e alfa igual a um | N1 → N2 (como hoje) |
| 8 | `=` | então o tamanho do campo | NB1 (linha 700) = ‖B‖ = ‖(−y, x)‖/(x² + y²)^α (voos do campo B no topo) |
| 9 | `+` | em cima o tamanho de menos ípsilon | chip 1 s '√(y² + x²) = r' ao lado; gm NB1 → NB2 (numerador = r) |
| 10 | `+` | embaixo a distância elevada a dois alfa | gm NB2 → NB3 (= r/r^{2α}); o α = 1 de N2 acende |
| 11 | `=` | a distância dividida pela distância ao quadrado | gm NB3 → NB4 (= r/r²) |
| 12 | `=` | um sobre a distância o campo | NB4 ganha '= 1/r' |
| 13 | `=` | o campo do fio cai | gráfico (como hoje) |

### A3-4

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | faz o mesmo com um fio carregado | como hoje |
| 2 | `=` | o campo elétrico aponta para fora | BB → EE (como hoje) |
| 3 | `=` | fora do fio não tem carga | acende ga (como hoje) |
| 4 | `+` | calcula o divergente como no terceiro | RB0 e N2 saem; NB4 vira chip '‖B‖ = 1/r' (1560, 380, 30 px); DV (linha 460) = div E = ∂(x s^{−α})/∂x + ∂(y s^{−α})/∂y, s = x² + y² |
| 5 | `+` | a primeira parcela é xis vezes | T1 (linha 540) = ∂(x s^{−α})/∂x = 1·s^{−α} + x(−α s^{−α−1}·2x) |
| 6 | `+` | sai a própria potência menos | gm T1 → T1b (= s^{−α} − 2αx² s^{−α−1}) |
| 7 | `+` | a segunda é igual com ípsilon | T2 (linha 615) = ∂(y s^{−α})/∂y = s^{−α} − 2αy² s^{−α−1} (cópia de T1b, só x → y) |
| 8 | `+` | somando aparecem duas vezes | S1 (linha 700) = div E = 2s^{−α} − 2α(x² + y²) s^{−α−1} |
| 9 | `+` | que é dois alfa vezes a potência | gm S1 → S2 (= 2s^{−α} − 2α s·s^{−α−1}) → S3 (= 2s^{−α} − 2α s^{−α}) |
| 10 | `=` | divergente dois menos dois alfa | gm S3 → S4 (= (2 − 2α)/s^α); FUSÃO DV..S4 → DE (linha 460) |
| 11 | `+` | igual a zero alfa um | DE ganha '= 0 ⇒ α = 1' |
| 12 | `=` | alfa um e o campo também cai | gm chip ‖B‖ → NE (linha 690) = ‖E‖ = r/r^{2α} = r/r² = 1/r |

### A3-5

| # | marca | frase | evento na tela |
|---|---|---|---|
| 1 | `=` | e uma carga pontual | como hoje |
| 2 | `=` | escreve o campo como o vetor posição | como hoje |
| 3 | `=` | o x maiúsculo é o vetor posição | leituras (como hoje) |
| 4 | `le` | o X maiúsculo é o vetor posição |  |
| 5 | `ate` | as barras duplas a distância |  |
| 6 | `le` | as barras duplas, a distância |  |
| 7 | `ate` | p o expoente |  |
| 8 | `le` | p, o expoente |  |
| 9 | `=` | faz a conta de uma parcela | PA parte 'd' (como hoje) |
| 10 | `+` | primeiro a derivada da distância | DN0 (linha 380) = ‖X‖ = (x² + y² + z²)^{1/2} |
| 11 | `+` | o meio desce | gm DN0 → DN1 = ∂‖X‖/∂x = ½(x² + y² + z²)^{−1/2}·2x |
| 12 | `+` | o meio com o dois cancela | ½ e 2 acendem CORAL e somem |
| 13 | `=` | a derivada da distância nessa direção | gm DN1 → DN (= x/‖X‖) |
| 14 | `+` | agora a regra do produto com xis | PA ganha t1 e m em caneta (como hoje, sem o voo) |
| 15 | `+` | vezes a derivada da distância xis | voo DN → PA r (como hoje); junta(PA) |
| 16 | `+` | xis vezes xis dá xis ao quadrado | PB0 (linha 640) = 1/‖X‖^p − p x² ‖X‖^{−p−1}‖X‖^{−1} |
| 17 | `+` | e as potências da distância se juntam | gm PB0 → PB1 (= 1/‖X‖^p − p x² ‖X‖^{−p−2}) |
| 18 | `=` | então dá um sobre a distância | gm PB1 → PB (= 1/‖X‖^p − p x²/‖X‖^{p+2}) |
| 19 | `=` | menos o expoente vezes o quadrado | acende t2 de PB |
| 20 | `=` | as outras parcelas são iguais | como hoje |
| 21 | `=` | agora soma | como hoje |
| 22 | `=` | os quadrados das coordenadas somam | como hoje |
| 23 | `=` | que cancela o mais dois | como hoje |
| 24 | `=` | sobra o número de parcelas | como hoje |
| 25 | `=` | no plano são duas parcelas | como hoje |
| 26 | `=` | o divergente no espaço é três | como hoje |
| 27 | `=` | para zerar o expoente é três | fusão → DF (como hoje) + P3 parte 1: p = 3 |
| 28 | `+` | a intensidade fica a distância dividida | P3 parte 2: ⇒ ‖E‖ = ‖X‖/‖X‖³ = r/r³ = 1/r² |
| 29 | `=` | a de coulomb | como hoje |
| 30 | `=` | e a da gravitação | como hoje |

Total de gatilhos novos: **126**.


---

## Anexo C · Os 11 trechos de voz
Duração esperada = palavras ÷ 2,91 p/s (taxa da v3.3) + pausas internas; aceite de ritmo 2,60–3,25 p/s e ±12 % do trecho antigo.

| trecho | âncoras | caracteres | palavras | ≈ duração |
|---|---|---|---|---|
| T01_D3-2_D3-3 | D3-2, D3-3 | 3544 | 626 | 3:35.7 |
| T02_D3-6 | D3-6 | 1117 | 206 | 1:10.8 |
| T03_D3b-2 | D3b-2 | 447 | 76 | 0:26.1 |
| T04_D3b-4 | D3b-4 | 603 | 112 | 0:38.5 |
| T05_D4-6_D4-7 | D4-6, D4-7 | 3193 | 576 | 3:18.5 |
| T06_D5-9 | D5-9 | 666 | 119 | 0:40.9 |
| T07_A1-2_A1-3 | A1-2, A1-3 | 1618 | 289 | 1:39.9 |
| T08_A1-5 | A1-5 | 536 | 96 | 0:33.0 |
| T09_A2-2_A2-4 | A2-2, A2-3, A2-4 | 2512 | 444 | 2:33.8 |
| T10_A4-2_A4-4 | A4-2, A4-3, A4-4 | 2499 | 440 | 2:32.4 |
| T11_A3-3_A3-5 | A3-3, A3-4, A3-5 | 3572 | 637 | 3:40.1 |

Total previsto do WAV emendado ≈ 2.390 s (39:50). Parada se > 2.490 s (41:30).


---

## Anexo D · Conferência simbólica (SymPy)
`verificacao/verifica_yt0030_v34_contas.py` (no zip): 88 checagens das contas C1–C21, todas True. Resumo da saída:

```
True  C1 ‖(−y,x)‖ = √((−y)²+x²) = √(x²+y²)
True  C1 s^α = (r²)^α = r^{2α}
True  C1 r / r^{2α} = r^{1−2α}
True  C1 ‖v‖ = r^{1−2α} (r = √s)
True  C2 (x)' = 1
True  C2 ∂s/∂x = 2x
True  C2 (s^{−α})'_x = −α s^{−α−1}·2x
True  C2 ∂Q/∂x = 1·s^{−α} + x(−α s^{−α−1}·2x)
True  C2 = s^{−α} − 2αx² s^{−α−1}
True  C2 K4: s^{−α} = s·s^{−α−1}
True  C2 P5: = s^{−α−1}(s − 2αx²)
True  C2 ∂P/∂y = −1·s^{−α} + (−y)(−α s^{−α−1}·2y)
True  C2 G3 = −s^{−α} + 2αy² s^{−α−1}
True  C2 G5 = −s^{−α−1}(s − 2αy²)
True  C2 RS = rot
True  C2 RS5 = s^{−α−1}(2s − 2αs)
True  C2 RS5b = s^{−α−1}·s(2 − 2α)
True  C2 RS5c = s^{−α}(2 − 2α) = (2 − 2α)/s^α
True  C2 DP = −y(−α s^{−α−1}·2x) = 2αxy s^{−α−1}
True  C2 DQ = x(−α s^{−α−1}·2y) = −2αxy s^{−α−1}
True  C2 div = 0
True  C3 v(t,0) = (0,1)
True  C3 v(0,t) = (−1,0)
True  C3 α=¼: r^{1−2α} → 0 (r → 0⁺)
True  C3 α=1: r^{1−2α} → ∞ (r → 0⁺)
True  C4 φ_x = ½·2x = x
True  C4 φ_y = ½·(−2y) = −y
True  C14 φ_xx = 1, φ_yy = −1, ∇²φ = 0
True  C5 ∂(x sen y)/∂x = sen y
True  C5 ∂(cos y)/∂y = −sen y
True  C5 ∂(z − xy)/∂z = 1
True  C6 homogeneidade F(sx,sy) = s F(x,y)
True  C6 F(h,h) = (h·h)/(h²+h²)(h,h) = ½(h,h) = (h/2,h/2)
True  C6 ‖erro‖ = √(h²/4 + h²/4) = h√2/2
True  C6 ‖H‖ = √(h²+h²) = h√2
True  C6 razão = ½
True  C7 N' = 2xy
True  C7 D' = 2x
True  C7 abre: 2xy(x²+y²) − x²y·2x = 2x³y + 2xy³ − 2x³y
True  C7 ∂P/∂x = 2xy³/(x²+y²)²
True  C7 y=0: 0
True  C7 x=0: 0
True  C7 y=x: 2x·x³/(x²+x²)² = 2x⁴/(2x²)² = 2x⁴/4x⁴ = ½
True  C8 P_x = 2x − 0
True  C8 P_y = 0 − 2y
True  C8 Q_x = 2·y·1
True  C8 Q_y = 2·x·1
True  C9 Q_x = 0 − 2x/9
True  C9 Q_y = 0
True  C10 rot(−3) = −2(−3)/9 = 6/9 = 2/3
True  C10 rot(3) = −2·3/9 = −2/3
True  C10 rot(0) = 0
True  C10 ω = (2/3)/2 = 1/3
True  C10 T = 2π/(1/3) = 6π
True  C10 6π ≈ 18,8 (≈ 19 s)
True  C11 |d₂(±3)| = 2·3/9 = 2/3
True  C11 d₂(0) = 0
True  C12 u_x=1, u_y=0, v_x=0, v_y=−1
True  C13 d(xy)/dt = ẋ y + x ẏ
True  C13 u·y + x·v = xy − xy = 0
True  C13 xy = c ⇒ y = c/x
True  C15 div ∇φ = φ_xx + φ_yy
True  C16 (x+iy)² = x² + 2x(iy) + (iy)²
True  C16 i² = −1
True  C16 = (x² − y²) + i(2xy)
True  C16 CR: P_x = 2x = Q_y
True  C16 CR: P_y = −2y = −Q_x
True  C17 J = (2x −2y; 2y 2x)
True  C17 J = 2r·R(θ), 2r = √(a²+b²) = 2√(x²+y²)
True  C17 J(1,1) = (2 −2; 2 2) = 2√2·R(45°)
True  C17 colunas (2,2)·(−2,2) = 0, mesmo tamanho 2√2
True  C18 P_x=2x, P_y=−2y, Q_x=−2y, Q_y=−2x
True  C18 rot = −2y − (−2y) = 0
True  C18 div = 2x − 2x = 0
True  C18 d₁ = 4x, d₂ = −4y
True  C19 2 − 2α = 0 ⇒ α = 1
True  C19 ‖B‖ = r/r^{2α} com α=1 = 1/r
True  C20 T1 = ∂(x s^{−α})/∂x
True  C20 T1b = s^{−α} − 2αx² s^{−α−1}
True  C20 S1 = div E
True  C20 S3 = 2s^{−α} − 2α s^{−α}
True  C20 S4 = (2 − 2α)/s^α
True  C21 ∂‖X‖/∂x = ½(x²+y²+z²)^{−1/2}·2x = x/‖X‖
True  C21 PA = ∂/∂x (x/‖X‖^p)
True  C21 PB0 = 1/‖X‖^p − p x² ‖X‖^{−p−1}‖X‖^{−1}
True  C21 PB1 = … ‖X‖^{−p−2} = PB
True  C21 div E = (3 − p)/‖X‖^p
True  C21 p=3: ‖E‖ = r/r³ = 1/r²

88/88 True
```
