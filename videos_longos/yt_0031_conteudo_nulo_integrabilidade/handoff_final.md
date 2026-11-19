# yt_0031 · CÁLCULO III · EP. 06 · Conteúdo nulo e integrabilidade · HANDOFF FINAL
**Correções de tela + voz + sincronização + legenda `.srt` + render 1080p + master + entrega**

Arquivo único e autocontido. Data: 2026-11-13.

**Base:** o **preview v3** (20:10, 960×540, 15 fps, sem voz). O Kaio aprovou o v3 como base e pediu que, antes da narração, ficasse "tudo bem redondinho". A auditoria quadro a quadro do v3 (18.154 quadros) achou só correções locais. Por isso **não há outra rodada de preview com o Kaio**: corrija, confira os trechos no 540p com voz e siga até a entrega.

**Narração:** é a **v2.3 fechada** (§4). Ela vai no zip como `yt_0031_narracao_v23_fechada.md` e substitui a narração da unidade.

**O que continua valendo:**
- os handoffs v1, v2 e v3 (regras G1–G8, cores, layouts, números) e os alvos `referencia*/`, onde este documento não diverge;
- tudo o que o v3 acertou, que é quase tudo: B2-2, B6-3 (contradição e zooms), B9-1, B1-3, símbolos, B5-1, B7-1, B4-3, S1, H2, a tabela de eventos e as costuras.

---

## 0. Autorização, fases e modo de execução

**Fases abertas pelo Kaio nesta unidade:**
- correções de tela (§3);
- narração v2.3 (§4);
- voz (ElevenLabs v4);
- sincronização;
- legenda `.srt`;
- render final 1080p e master;
- entrega em `entregas/`.

**Fases não abertas (não fazer):**
- publicação, capa, `commit`, `push`, `branch`, PR;
- qualquer mudança em `template/`, `assets/`, `pyproject.toml`, `uv.lock`, `AGENTS.md`, `docs/` ou em outras unidades.

**O que pode ser alterado:**
- só a unidade `videos_longos/yt_0031_conteudo_nulo_integrabilidade/`;
- `renders/` e `entregas/`, que são saída;
- pode **copiar** scripts do pipeline de voz do yt_0028 (fechado) para dentro da unidade, sem alterar aquele vídeo.

**Modo de execução:**
- Não encerre a vez entre etapas.
- Depois de lançar um render (Manim ou Three.js) ou a geração de voz, espere na mesma vez e siga direto para a auditoria. Use um comando em primeiro plano com timeout de até 10 min por lote, ou um laço `until` que consulta o arquivo de saída.
- Mensagem de progresso não é entrega.

**Só há duas paradas permitidas:**
1. A variável `ELEVENLABS_API_KEY` não existe na sessão. Peça ao Kaio. **Nunca** grave a chave em arquivo, log ou relatório.
2. O WAV passa de **21:00**. Reporte a duração e pare: quem decide cortes é a Produção.

Qualquer outra dúvida: escolha a leitura mais provável, diga qual e siga.

**Ordem:** §3 correções no código, com stills de conferência → §4 narração v2.3 → §5 voz → §6 sincronização → §7 conferência 540p com voz (prova das correções) → §8 1080p → §9 QA e entrega → §10 relatório. Pare só depois do relatório.

Guarde este arquivo na unidade como `handoff_final.md`.

---

## 1. Estado de partida

- **Unidade:** `videos_longos/yt_0031_conteudo_nulo_integrabilidade/`.
- **Código:** `sec_h.py`, `sec_a.py`, `sec_b1.py` … `sec_b9.py`, `sec_s.py`, o kit `v31.py`.
- **QA:** `qa31v2.py` e a cadeia `cadeia_v2.sh`. Lotes em `lotes_v2.json`.
- **Three.js:** as cenas `b13`, `b13t`, `b21` e `b52` (e as que a unidade usar), com `pontos.json`.
- **Pipeline de voz:** copie do yt_0028 e adapte nomes, lotes e caminhos:
  - `alinhar_voz.py` (alinhamento forçado + STT de conferência);
  - o modo "tempo real da voz" do gerador de âncoras (hoje as âncoras saem da narração estimada);
  - `gerar_srt.py`, `render1080.sh`, `montar_final.py`, `qa_parado.py`, `qa_canto.py`, `qa_fundo.py`.
- **Não reabrir:**
  - a matemática e os números (Anexo A);
  - a ordem H → A → B1 … B9 → S;
  - as cores: f ciano `#35D9FF`; m_ij, s(P) e piso azul-claro `#7FB2FF`; M_ij, S(P), tampas e teto coral `#FF7A8A`; ε e cobertura menta `#8CFFD2`; δ e pontos laranja `#E08A3C`; ALERTA `#FF5D5D`; x âmbar `#FFC24D`; y magenta `#EA63FF`; metais `#1E5072` e `#30BBE0`;
  - o fundo violeta com a grade que nasce dos eixos;
  - o 3D em Three.js;
  - nada de livros nem do Atlas na tela ou na fala.
- **A cena segue a voz.** Os tempos do v3 não valem mais: todos os lotes, inclusive os quadros do Three.js, são re-renderizados com a linha do tempo da voz.

---

## 2. Avaliação do v3 (resumo)

**Feito e aprovado:**
- **B2-2:** a fórmula `S(P) − s(P) = 2 · (…)` fica na tela em 100 % dos quadros.
- **B7-2:**
  - as 6 linhas estão nas posições do alvo 23b;
  - os cancelamentos são coral, com o `2` pequeno;
  - a frase nova casa com os 6 gatilhos;
  - a álgebra está certa.
- **B6-3:**
  - a contradição está igual ao alvo 21b, sem parado maior que 3 s;
  - os três zooms estão nas palavras certas;
  - o mapeamento da janela foi medido no pixel.
- **B9-1:** as molduras viram chips.
- **Itens médios e pequenos:** B1-2, B1-3, B5-1, B7-1, a ordem das formas do B4-3, S1, H2, os símbolos (`\dfrac`, ε a 44 px, `C^1`, B7-3) e a miniatura do muro.
- **Costuras:** nenhuma salta ou pisca.
- **Regressões:** nenhuma.
- **Relatórios do v3:** FLASH, alinhamento, comparação com os alvos, origens e glyph maps (15) batem com o vídeo.
- **R5 do v2:** a divergência "R5 58" está explicada pelos horários dos arquivos. Valem 0 e 1.

**O que sobra:** os 11 itens do §3. São todos locais.

**Duas falhas do QA para fechar no §7:**
- o R5 ignora objetos **em trânsito**, como voos e mapas;
- o QA de gatilhos não mede glifos **embolados**.

---

## 3. Correções (lista fechada)

Tempos do preview v3. Os arquivo:linha são da unidade como está agora. Cada item tem a troca e um **aceite** com o arquivo de prova. Os stills do erro estão no PC de mesa, em `C:\Users\Pichau\AppData\Local\Temp\yt0031_audit_v3\citados\`, com o tempo no nome. Copie-os para `referencia_final/`.

### F1 · ALTA · B6-3 · 12:55.40–12:55.80 · `CONTRADIÇÃO` só 0,4 s na tela (`sec_b6.py:300-304`)
- "Contradição" é a última palavra da fala, e o bloco começa a sair em 12:55.87.
- A narração v2.3 acrescenta, logo depois: *"Então, numa região fechada e limitada, toda função contínua é uniformemente contínua."* (§4).
- **Troca:**
  - o quadro 21b fica inteiro até o fim dessa frase;
  - em "uniformemente contínua", a borda branca da chapa acende 1 s (troca de cor e volta).
- O B6-3 só sai depois da última palavra.
- **Aceite:** `CONTRADIÇÃO` fica ≥ 3,0 s na tela, medido no 540p com voz. Prova em `qa/final/F1_*.png`, com 3 stills: na palavra, +1,5 s e no último quadro do B6-3.

### F2 · MÉDIA · B7-2 · voos que atravessam outras linhas (`sec_b7.py:237` e `:254`)
- **14:42.53–14:43.07 (mapa 4a):** a cópia de `ε/(8M)` passa sobre o `= ε/2` da linha 550, e a de `4Mε₁` sobre a linha 420.
- **14:50.53–14:51.20 (soma):** `S(P) − s(P) <` voa da linha 250 até a 840 por cima de `ESCOLHA DOS DOIS ε`, da linha 420 e do `4Mε₁ =` da 690. Os dois `ε/2` empilham sobre o `ε/2` da 690.
- **Troca:**
  - o `S(P) − s(P) <` da linha 840 entra **a caneta**, sem voo;
  - os dois `ε/2` voam em arco pela **direita** (`path_arc` ≈ −0,8 rad), sempre com x ≥ 1600 px no 1080p;
  - no mapa 4a, `4Mε₁` faz arco pela direita (x ≥ 1700) e `ε/(8M)` pela esquerda (x ≤ 1300).
  - Se o `TransformByGlyphMap` não aceitar `path_arc` por par, faça o voo em dois tempos: desce pela lateral e depois desliza para o lugar.
- **Aceite:** o R5 **com objetos em trânsito** (§7) dá zero entre 14:28 e o fim do B7-2. Prova em `qa/final/F2_*.png`: 6 stills a cada 0,1 s em cada um dos dois voos.

### F3 · MÉDIA · B4-1 · 8:10.13–8:10.53 e 8:11.07–8:11.33 · glifos embolados nos mapas 5a/5b (`sec_b4.py:96` e `:107`)
- O `2` de 0,25 é escrito sobre o `5`, que ainda desliza (aparece "0,2Ƨ5"). O `1` de 0,125 é escrito sobre o `2`.
- **Troca, em dois tempos:**
  1. os pares andam (0,4 s) e abrem o espaço;
  2. a caneta escreve o glifo novo nesse espaço (0,3 s).
  Os glifos que saem usam `auto_fade` **antes** do mapa.
- **Aceite:** nenhum quadro com dois glifos sobrepostos nesses trechos. Prova em `qa/final/F3_*.png`, um quadro a cada 2.

### F4 · MÉDIA · B2-1 · 4:29.7–4:47.7 · a placa `TAMPA 0` encosta nas bordas da célula (`sec_b2.py:62` e `:73`)
- A placa tem ≈ 114 px numa célula de 120 px, com ≈ 3 px de folga, nas duas células. O contorno laranja do metal pesado tem 2 px e quase não aparece sobre o ciano.
- **Troca:**
  - `TAMPA` e `0` em duas linhas centradas, a 24 e 28 px, numa placa de ≈ 80 px com margem ≥ 20 px até as bordas da célula;
  - contorno laranja da célula com 4 px.
- **Aceite:** folga ≥ 20 px nos quatro lados, nas duas células. Prova em `qa/final/F4_*.png`.

### F5 · MÉDIA-BAIXA · B4-3 · 9:03.0 e 9:04.67 · topos e bases das caixas quase invisíveis ao acender (`sec_b4.py:262-270`)
- **Troca:**
  - em "soma por cima": uma **escada contínua** pelos topos das caixas (polilinha), coral, 6 px, por 1 s;
  - em "soma por baixo": o mesmo pelas bases, em azul-claro.
- **Aceite:** stills nos dois gatilhos (`qa/final/F5_*.png`) com a escada visível no 540p.

### F6 · BAIXA · A1 · 1:32.4–1:34.2 · o contorno do chip 2 nasce vazio (`sec_a.py:43-46`)
- O contorno nasce ≈ 1,8 s antes do texto, o mesmo defeito que já foi corrigido no chip 3.
- **Troca:** na linha 43, crie só `caixas[0]`. `caixas[1]` nasce junto com o texto dele.
- **Aceite:** nenhum contorno de chip vazio no A1.

### F7 · BAIXA · B7-2 · símbolos pequenos (`sec_b7.py:189` e `:204`)
- O `2` sob o 8 cancelado tem ≈ 14 px. O `ε` de `ESCOLHA DOS DOIS ε` tem ≈ 10 px.
- **Troca:**
  - `\underset{\textstyle 2}{\cancel{8}}`;
  - o ε da legenda como `MathTex` próprio (`TP(r"\eps", …, 34)`), em menta, alinhado à linha da legenda.
- **Aceite:** os dois ≥ 22 px no 1080p.

### F8 · BAIXA · B6-2 · 12:03–12:13 · `X` encostado no canto da chapa e `ε` pequeno
- **Troca:**
  - o `X` sobe 12 px e vai 12 px para a direita, com folga ≥ 16 px da chapa e do `f(X)`;
  - o `ε` sobre as barras vai a 30 px.

### F9 · BAIXA · S2 · 19:44 · o `?` de `\overset{?}{=}` tem ≈ 12 px (`sec_s.py:84`)
- **Troca:** `\overset{\textstyle ?}{=}`.

### F10 · BAIXA · B3-3 · 7:10–7:39 · borda tremendo
- A borda do 2º retângulo do segmento treme 1 px a cada 4 quadros. É o único "flash" do vídeo.
- **Troca:** arredonde o y dos retângulos para o pixel (ou desenhe-os com a espessura em número par de px).
- Confira também no 1080p se o ε de 44 px sai menta. No 540p ele parece cinza, provavelmente pela compressão; se continuar cinza no 1080p, aplique a cor `#8CFFD2` direto no glifo.
- **Aceite:** FLASH = 0 também neste trecho, medido no 1080p.

### F11 · MÉDIA · B4-3 · rótulo `CÍRCULO` (`sec_b4.py`, fileira das formas)
- Em português, "círculo" pode ser lido como o **disco cheio**, que **não** tem conteúdo nulo (é o contraexemplo do B3-3). A narração v2.3 diz "circunferências".
- **Troca:** o rótulo `CÍRCULO` vira `CIRCUNFERÊNCIA` (24 px, Space Grotesk, como os outros), e o gatilho dessa forma passa a ser a palavra "circunferências".
- Se o rótulo não couber com ≥ 16 px de folga dos vizinhos, afaste as quatro formas igualmente (x = 1050 / 1280 / 1520 / 1750). Não diminua a fonte.
- **Aceite:** still em `qa/final/F11_*.png`; R5 = 0 na fileira.

---

## 4. Narração v2.3 fechada (v2 + 2 frases + 5 ajustes de rigor)

Copie `yt_0031_narracao_v23_fechada.md` do zip para a unidade **no lugar do arquivo de narração atual**, mantendo o nome que o gerador de âncoras usa.

São 3.606 palavras, ≈ 20:17 a 3 palavras/s, com as mesmas 31 âncoras e as mesmas primeiras falas. Mudam duas frases inteiras (já previstas no v3 e no F1) e cinco trechos curtos.

**As duas frases novas:**

| Bloco | Frase nova | Onde |
|---|---|---|
| B7-2 | "Com épsilon dois igual a épsilon sobre dois alfa, o alfa cancela, e sobra épsilon sobre dois. Com épsilon um igual a épsilon sobre oito eme, o eme cancela, o quatro com o oito vira um meio, e sobra épsilon sobre dois de novo. Meio épsilon mais meio épsilon: a diferença fica menor que épsilon." | depois de "…menor que metade da tolerância." (já está no v3 e nos gatilhos) |
| B6-3 | "Então, numa região fechada e limitada, toda função contínua é uniformemente contínua." | depois de "Contradição." (F1) |

**Os cinco ajustes de rigor e os gatilhos que mudam:**

| Bloco | v2.2 → v2.3 | Gatilho no código |
|---|---|---|
| B4-3 | "círculos" → "circunferências" | o da forma: `círculos` → `circunferências` (F11) |
| B4-3 | "…de derivada contínua, também tem…" → "…de derivada contínua num intervalo fechado, também tem…" | nenhum; se houver gatilho em "também tem conteúdo nulo", ele continua achando a frase |
| B6-3 | "esses pares se aproximam de um mesmo ponto da própria região" → "dá para escolher entre esses pares uma sequência que se aproxima de um mesmo ponto da própria região" | o do anel em P*: `se aproximam de um mesmo ponto` → `se aproxima de um mesmo ponto` |
| B7-1 | "um número eme maiúsculo que limita" → "um número eme maiúsculo, positivo, que limita" | `existe um número eme maiúsculo` fica |
| B9-1 | "E a fronteira da região tem conteúdo nulo?" → "E, se a região não é um retângulo, a fronteira dela tem conteúdo nulo?" | o da 3ª pergunta grande: `e a fronteira da região` → `a fronteira dela tem` |

Depois de trocar, rode a busca dos gatilhos contra o texto novo: `[gatilho-sem-frase]` = 0 antes de gerar a voz.

**Texto para gravação:** crie `narracao_tags.md` a partir da seção `## 2. Texto corrido (para gravação)` do arquivo do zip. Ela tem só os parágrafos, na ordem, sem títulos e sem as linhas **Tela:**. No `narracao_tags.md`, o título da seção fica exatamente `## Texto corrido (para gravação)`, que é o nome que o `--secao` do §5 procura.
- Tags permitidas: [curious], [thoughtful], [surprised], [happy], [excited], [serious]. Uma por parágrafo; o S2 tem duas.
- Não use [slowly] nem [pause].
- As letras ficam escritas como a voz deve ler: xis, ípsilon, eme, esse, éle, épsilon, delta, alfa, cê um.

Crie também `narracao_limpa.md`, sem tags, para o alinhamento e o `.srt`.

---

## 5. Voz (ElevenLabs v4)

Referência: `docs/roteiro_voz_elevenlabs_v4.md`.

1. Confirme `ELEVENLABS_API_KEY` (primeira parada, §0).
   - Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`.
   - Formato `mp3_44100_192`, decodificado para WAV mono 16 bits 44,1 kHz.
2. Rode primeiro com `--seco`, depois sem ele:

   ```
   uv run --no-sync python videos/gerar_voz_elevenlabs.py videos_longos/yt_0031_conteudo_nulo_integrabilidade/narracao_tags.md videos_longos/yt_0031_conteudo_nulo_integrabilidade/audio/narracao_v1.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)" --seco
   ```

3. **Uma tomada completa.** Siga com ela. O Kaio ouve em paralelo; se reprovar, regera, e a §6 refaz tudo sozinha. Por isso a sincronização precisa ser automática e reproduzível. A tomada aprovada vira `audio/narracao_final.wav`.
4. `qa/voz.txt`:
   - duração;
   - picos e clipping;
   - silêncio > 1,5 s dentro de um parágrafo;
   - tag lida em voz alta, procurada na transcrição de conferência;
   - pronúncia certa de "épsilon", "delta", "alfa", "eme", "esse minúsculo de P", "erre i j", "Riemann", "Dirichlet", "Heine-Cantor", "cê um" e "Parallax Lab";
   - fronteiras entre blocos sem corte audível.
5. No relatório: modelo, voz, número de blocos, duração e taxa real (palavras ÷ segundos de fala).

---

## 6. Sincronização (a cena segue a voz)

Regras permanentes dos longos:
- WAV contínuo;
- **nunca** cortar a voz por âncora nem inserir silêncio;
- atraso imagem × fala **≤ 0,2 s** (LEAD 0,15 s);
- quando a fala é mais longa que a construção, a espera se divide entre os gatilhos, nunca tudo no fim da âncora.

1. `alinhar_voz.py` → `alinhamento_palavras.json`.
2. `ancoras.json` **gerado por script**, no modo tempo real. Cada âncora começa na primeira fala do seu trecho (coluna "Começa em" da tabela da narração v2.3). Os gatilhos de cada seção são buscados no alinhamento.
3. **3D:** a linha do tempo do Three.js sai do mesmo `ancoras.json`. Re-renderize os quadros 3D de todos os lotes que os usam e rode o QA de alinhamento (≤ 2 px; pousos com 0 px nos quatro cantos).
4. Rode os lotes 540p e confira:
   - `[gatilho-sem-frase]` = 0;
   - os `[estouro]`, listados com o motivo.

   Estouro > 1 s numa âncora: encurte a animação dentro da regra da caneta (piso de 0,20 s por glifo) ou deixe a âncora seguinte começar mais tarde. **Nunca** acelere a voz.
5. `qa/sync.txt`: o atraso de cada âncora e de cada gatilho (meta ≤ 0,2 s).
6. **Legenda `.srt`** (`gerar_srt.py`):
   - até 2 linhas × 42 caracteres, de 2 a 5 s por bloco;
   - tempo do WAV = tempo do vídeo;
   - conversões de letras faladas para símbolos:

     | Falado | Na legenda |
     |---|---|
     | "épsilon" | ε |
     | "épsilon um", "épsilon dois" | ε₁, ε₂ |
     | "delta" | δ |
     | "alfa" | α |
     | "eme minúsculo i j" | m_ij |
     | "eme maiúsculo i j" | M_ij |
     | "esse minúsculo de P" | s(P) |
     | "esse maiúsculo de P" | S(P) |
     | "erre i j" | R_ij |
     | "cê um" | C¹ |
     | "xis" e "ípsilon" (minúsculos) | x e y |
     | "xis e ípsilon maiúsculos" | X e Y |
     | "eme" (cota da função) | M |
     | "D" | D |

---

## 7. Conferência 540p com voz (antes do 1080p)

Render de **todos os lotes** em 540p/15 fps com os tempos da voz, e preview com voz. Feche o que falhar antes do 1080p. **Não é rodada com o Kaio:** é a sua conferência interna.

**Portões:**
- `FLASH` = 0;
- sobreposição = 0 a cada 0,2 s, **inclusive objetos em trânsito** (voos, mapas, `ReplacementTransform`). Isso fecha a falha do R5 do v3;
- glifos embolados = 0: dois glifos de fórmula com mais de 30 % de área em comum em qualquer quadro;
- margem segura;
- texto ≥ 24 px e índices ≥ 22 px;
- `\dfrac` sem `\tfrac`;
- alinhamento 3D ≤ 2 px;
- palco parado > 3 s só com a voz lendo a tela, com o motivo em `parados_final.txt`; palco parado > 5 s = 0;
- `[gatilho-sem-frase]` = 0;
- `qa_canto.py` (linha 2 do canto desde o 1º quadro de cada bloco) e `qa_fundo.py`;
- logo em todos os quadros do A1;
- cartão do próximo vídeo (S2) ≥ 8 s, com o CTA só na tag `[happy]`;
- SYNC;
- VOZ.

**Pranchas:**
- `correcoes_final.jpg`: para cada F1–F11, o quadro do erro do v3 (`referencia_final/`) ao lado do quadro corrigido no gatilho.
- Uma prancha com **um quadro de cada âncora no instante da primeira fala** (31 quadros).
- Lado a lado com os alvos `21b`, `23b`, `28a`, `13`, `17`, `20`, `24`, `28` e `30`, para confirmar que nada regrediu.

---

## 8. Render final 1080p

1. **Three.js em 1080p**, com a mesma câmera e a linha do tempo da voz, e QA 3D de novo sobre o 1080p.
2. **Manim em 1080p30** pelo fluxo normal, com `template/config_horizontal.py`.
   - Não configure CRF: o `template/qualidade.py` já usa **14** em renders ≥ 1080p.
   - Não recodifique.
   - Sem teto de tempo de render.
3. **Emenda** com `montar_final.py` (remux, sem reencodar), na ordem dos lotes de `lotes_v2.json`, de H a S.
4. **Master:**

   ```
   uv run python videos/montar_master.py <sem_audio_1080p30.mp4> audio/narracao_final.wav renders/yt_0031_master_final_1080p30.mp4
   ```

   Confira:
   - 1920×1080, 30 fps;
   - duração do master = WAV (+ a cauda do CTA, se a montagem a mantiver);
   - `crf=14.0`, com o comando do AGENTS.md.
5. Se o disco apertar, apague só PNGs e renders 540p **desta** unidade já auditados. Os zips para o GPT (`yt0031_v*_para_gpt*.zip`) podem ser apagados.

---

## 9. QA final e entrega

**QA completo no vídeo final:**
- os portões do §7 sobre o 1080p (amostragem por lote; nos trechos de F2, F3 e F10, quadro a quadro);
- A/V contínuo;
- `.srt` conferido em 5 pontos: início, meio, fim, o B7-2 (ε₂ = ε/(2α)) e o B6-2 (Heine-Cantor);
- `crf=14.0`;
- `renders/capitulos_final.txt` com os tempos da voz e estes títulos:
  - `TRÊS PERGUNTAS`
  - `BEM-VINDOS`
  - `PISO, TETO E TAMPAS`
  - `A CHAPA DE DOIS METAIS`
  - `CONTEÚDO NULO`
  - `CURVAS TÊM CONTEÚDO NULO`
  - `FRONTEIRA`
  - `CONTINUIDADE UNIFORME`
  - `O TEOREMA`
  - `QUANDO FALHA`
  - `NUM EXERCÍCIO`
  - `SÍNTESE E PRÓXIMO`

**Entrega:** `uv run python videos/entregar.py yt_0031` (cópia). A pasta em `entregas/` leva:
- `master`;
- `legenda` (`.srt`);
- `audio/`;
- `texto/`: ficha, `narracao_tags.md`, `narracao_limpa.md`, este handoff e os capítulos;
- `manifesto`.

O número `0031` vai no fim de cada nome. Não há capa. Série, EP e assunto vêm da `ficha.md`: `CÁLCULO III · EP. 06`, `# Conteúdo nulo e integrabilidade`.

**Na ficha:**
- `3d_threejs:` lista as cenas realmente usadas;
- a duração vira a real.

Não rode `entregar.py` se um portão do §7 estiver aberto. Pare e reporte.

---

## 10. Relatório de entrega (obrigatório, e depois pare)

1. Arquivos alterados e criados.
2. F1 a F11, cada um com o caminho do still que prova, e a prancha `correcoes_final.jpg`.
3. Todos os portões do §7 com números reais, a sincronização das 31 âncoras e o QA de voz.
4. Caminhos: WAV, preview 540p com voz, master 1080p, `.srt`, capítulos e a pasta em `entregas/`.
5. Three.js: resolução, custo por quadro no 1080p e alinhamento medido (px).
6. Duração final e taxa real da voz, comparadas com 3 palavras/s.
7. Pendências reais.

Depois do relatório: **pare**. Não faça publicação, capa, commit nem push.

---

## Anexo A · Números congelados

| Grandeza | Valor |
|---|---|
| Solda | y = 1 + 0,42 · sen(1,7x − 0,4); ρ = 1 embaixo e 3 em cima (kg/m²) |
| Massa | ≈ 7,06 kg |
| Tabela (n = 4, 8, 16, 32, 64) | células na solda 5 / 11 / 24 / 47 / 95; por baixo · por cima: 6,00 · 8,50 → … → 6,97 · 7,15; diferenças 2,5 · 1,38 · 0,75 · 0,37 · 0,19 |
| Altura da tampa na solda | 3 − 1 = 2; S(P) − s(P) = 2 · (área das células na solda) |
| Orçamento | ε = 1 → 4 retângulos → 0,46 m²; ε = 1/4 → 16 → 0,12; ε = 0,05 → 64 → 0,03 |
| Parábola | área ≤ 4Δ: 4 pedaços → 2; 8 → 1; 16 → 0,5 |
| Solda (caixas) | sobe 0,58, desce 0,36, total 0,94Δ |
| Arco | 2Δ: 4 → 1; 8 → 0,5; 16 → 0,25; 32 → 0,125 |
| Continuidade uniforme (x² + y²) | ε = 1 → δ = 0,17 |
| sen(1/x), pares k = 1, 2, 3 | sen = 1 em 1/(π/2 + 2πk) = 0,1273 / 0,0707 / 0,0490; sen = −1 em 1/(3π/2 + 2πk) = 0,0909 / 0,0579 / 0,0424; distâncias 0,036 / 0,013 / 0,0065 m; diferença sempre 2 |
| Prova | ε₂ = ε/(2α) → αε₂ = ε/2; ε₁ = ε/(8M) → 4Mε₁ = ε/2; S(P) − s(P) < ε |
| Três respostas | área do quarto de disco = π; massa ≈ 7,06 kg; x² + y² integrável |
| Formas do B4-3 | SEGMENTO, POLÍGONO, CIRCUNFERÊNCIA, ELIPSE (curvas, todas com conteúdo nulo) |
| Dirichlet | soma por cima 4, por baixo 0 |
