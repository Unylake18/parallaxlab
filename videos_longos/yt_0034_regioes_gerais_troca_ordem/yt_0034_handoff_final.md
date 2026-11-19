# yt_0034 · CÁLCULO III · EP. 09 · Regiões gerais e troca de ordem · HANDOFF FINAL
**Correções de tela (D1–D13) + narração v3.2 + voz + sincronização + legenda `.srt` + render 1080p + master + entrega**

Arquivo único e autocontido. Data: 2026-11-14. A base é o **preview v3**: 21:58, 960×540, 15 fps, sem voz. Ele cumpriu o que o handoff v3 pediu: as 9 contas C1–C9 entraram inteiras, a abertura H0 bate com os alvos, o sino 3D não separa a peça, as áreas das fatias estão certas e o gancho mostra a saída pulando em y = 3.

O Kaio perguntou se já dá para a narração. **Sim.** O que falta é só tela: 13 pontos de sobreposição, palco parado e um 3D antigo (§3). Nenhum deles muda a fala.

No zip vão:
- `narracao_v32.md` (narração v3.2 fechada; substitui o `narracao.md` da unidade);
- `quadros_do_erro/` (D01–D11 no instante do problema, 960×540) e `00_folha_erros_v3.jpg`.

Onde este documento não diverge, continuam valendo os handoffs v1, v2 e v3 e os quadros-alvo v1/v2/v3.

---

## 0. Autorização, fases e modo de execução

**Fases abertas pelo Kaio nesta unidade:**
- correções de tela (§3);
- voz (ElevenLabs v4);
- sincronização;
- legenda `.srt`;
- render final 1080p e master;
- entrega em `entregas/`.

**Fases não abertas (não fazer):**
- publicação, capa, `commit`, `push`, `branch`, PR;
- qualquer mudança em `template/`, `assets/`, `pyproject.toml`, `uv.lock` ou em outras unidades;
- `AGENTS.md` e `docs/padrao_video_longo.md`: **só** o Anexo B, e só se ainda não estiver aplicado.

**O que pode ser alterado:**
- só a unidade `videos_longos/yt_0034_regioes_gerais_troca_ordem/`;
- `renders/` e `entregas/`, que são saída;
- pode **copiar** scripts do pipeline de voz do yt_0033 (ou do yt_0032) para dentro da unidade, sem alterar esses vídeos.

**Modo de execução:**
- Não encerre a vez entre etapas.
- Depois de lançar um render (Manim ou Three.js) ou a voz, espere na mesma vez e siga para a auditoria. Use comando em primeiro plano com timeout de até 10 min por lote, ou um laço `until` sobre o arquivo de saída.
- Mensagem de progresso não é entrega.

**Só há duas paradas permitidas:**
1. A variável `ELEVENLABS_API_KEY` não existe na sessão. Peça ao Kaio. **Nunca** grave a chave em arquivo, log ou relatório.
2. O WAV passa de **23:30**. Reporte a duração e pare: quem decide cortes é a Produção. (Estimativa: 4.035 palavras a 3 palavras/s ≈ 22:25.)

Qualquer outra dúvida: escolha a leitura mais provável, diga qual e siga.

**Ordem:**
1. Anexo B (conferir a regra CONTAS SEM PULAR nos docs);
2. §3 correções no código, com stills de conferência (sem voz, tempos do v3 como rascunho);
3. §4 narração v3.2 e busca dos gatilhos;
4. §5 voz;
5. §6 sincronização;
6. §7 conferência 540p com voz;
7. §8 1080p;
8. §9 QA e entrega;
9. §10 relatório.

Pare só depois do relatório. Guarde este arquivo na unidade como `handoff_final.md` e copie `quadros_do_erro/` do zip para `referencia_final/`.

---

## 1. Estado de partida

- **Unidade:** `videos_longos/yt_0034_regioes_gerais_troca_ordem/`.
- **Código:** `sec_h`, `sec_a`, `sec_b1` … `sec_b8`, `sec_s`, `lib34.py`, `pecas34.py`, `kit.py`, `qa34.py`, `montar.py`.
- **Three.js:** cena 1 = cunha (B3), cena 2 = sino (H0 e B4-2), com as chaves e as câmeras CAMP/CAMD do v3.
- **Âncoras:** `narracao.md` → `gerar_ancoras.py` → `ancoras.json`. Hoje no modo estimativa; o modo "tempo real da voz" vem do yt_0033 (ou do yt_0032).
- **Pipeline de voz:** copie e adapte nomes, lotes e caminhos de `alinhar_voz.py`, do modo tempo real do `gerar_ancoras.py`, de `gerar_srt.py`, `render1080.sh`, `montar_final.py`, `qa_canto.py` e `qa_fundo.py`.
- **Não reabrir:**
  - a matemática e os números (Anexo A) e as contas C1–C9 do v3, degrau por degrau;
  - a ordem H0 → H1 → H2 → A1 → B1 … B8 → S1 → S2;
  - as cores: x âmbar #FFC24D (decisão do Kaio; não trocar), y magenta #EA63FF, f ciano #35D9FF, entrada #7FB2FF, saída coral #FF7A8A, resultado menta #8CFFD2, ALERTA #FF5D5D, GEO #B8C4DA, traço #6C7698;
  - o fundo violeta liso com a grade `papel(ax)`;
  - o sino 3D do v3 (peça inteira, traço, CAMP/CAMD, x = 0,2 e y = 0,6);
  - a abertura H0, os gráficos de área das fatias, o gancho e o cartão.
- **A cena segue a voz.** Os tempos do v3 não valem mais. Todos os lotes, inclusive os quadros do Three.js, são re-renderizados com a linha do tempo da voz.

---

## 2. Avaliação do v3 (resumo)

**O que fica (não mexer):**
- As contas C1–C9, todas com a escada inteira. Nenhum degrau faltando: os colchetes viram G(b) − G(a) com os valores, as substituições têm a linha dos limites, e o 7/16 sai pelo complemento.
- A substituição trigonométrica nasce do triângulo no desenho (C1).
- A abertura H0 bate com `v3_01`/`v3_02`, e o sino não separa a peça.
- Os gráficos A(x) × A(y), depois de assentados, estão certos: 8/3 na cunha e 0,316 no sino.
- O gancho: a saída pula em y = 3, e o cartão com os 3 itens fica cerca de 18 s.
- O telhado, o 7/16 e as substituições u do B3-2 e do B6.

**O que falta:** são 13 pontos de tela. Os mais visíveis são estes:
- os pousos 3D ficam por cima dos gráficos de área (D1);
- o passo 3 do sino fica com o palco parado por cerca de 54 s (D2);
- a cunha 3D ainda separa as peças (D10).

O resto são sobreposições pontuais.

---

## 3. Correções (lista fechada)

Formato de cada item:
- **Onde:** bloco · tempo no v3 · quadro do erro no zip;
- **Hoje:** o que está na tela;
- **Troca:** o que fazer;
- **Aceite:** como provar.

Prove cada item com um **still no gatilho** antes da voz e, de novo, na prancha do §7.

**Regras de sempre** (valem para tudo que for refeito):
- caneta glifo a glifo, traço finíssimo;
- número que vem de um limite ou do desenho **voa** (`TransformFromCopy`);
- um `TransformByGlyphMap` por passo, com mapa explícito; `MathTex` de string única; `\dfrac` ≥ 26 px;
- nada de `FadeIn` de linha pronta;
- realce = o próprio objeto engrossa o traço na **própria cor**, nunca um preenchimento de outra cor;
- palavras em Space Grotesk, nunca dentro do `MathTex`.

### D1 · Pouso sobre os gráficos de área (cunha e sino)
- **Onde:** fim do B3-2, 10:03–10:09 (`D01a`, `D01b`); B4-2, 11:51–11:57 (`D01c`, `D01d`).
- **Hoje:** o triângulo âmbar e o retângulo magenta do pouso (cunha), e a fatia em pé do sino, continuam no palco enquanto os eixos e as curvas de A(x)/A(y) são desenhados. As formas cruzam as curvas e os eixos.
- **Troca:** é o que o v3 §3.2 já pedia ("cada ponto nasce voando da face colorida do pouso"). Antes de qualquer eixo do gráfico aparecer:
  - a face colorida do pouso **encolhe e voa** até virar o ponto da curva, em ≤ 0,6 s:
    - cunha: triângulo → ponto (1; 1,5) em A(x), retângulo → ponto (1; 1,73) em A(y);
    - sino: fatia em pé → ponto (0,2; 0,549), retângulo → ponto (0,6; 0,419);
  - o resto do pouso (eixos do pouso, chaves, rótulos) sai em ≤ 0,4 s, **junto**;
  - só então os eixos do gráfico entram, e a curva é traçada passando pelo ponto.
- **Aceite:** nenhum quadro de 10:00–10:15 e 11:48–12:03 (tempos do v3) com polígono do pouso cruzando eixo, curva ou rótulo do gráfico. Use o R5 polígono × linha nessa janela.

### D2 · Passo 3 do sino: palco parado e flash salmão
- **Onde:** B4-2b, 12:09–13:03 (`D02`, em 12:45).
- **Hoje:**
  - o palco fica com o retângulo parado por cerca de 54 s enquanto a coluna faz a conta C4;
  - em 12:45 o retângulo acende em salmão, uma cor que não é do kit.
- **Troca:** o palco acompanha a conta.
  1. O retângulo volta ao **magenta** de `v3_06`. Realce só por traço na própria cor.
  2. **"Altura vezes comprimento"**: a chave `y` (COMPRIMENTO) e a chave `e^(−y²)` (ALTURA) acendem uma depois da outra, e o produto `y e^(−y²)` voa do retângulo para a coluna (O2).
  3. **"Agora a de fora"**: o retângulo encolhe até o ponto (0,6; 0,419), na mesma regra do D1. Entra o gráfico de `A(y) = y e^(−y²)` em [0, 1], na mesma escala do `v3_05`, curva magenta traçada da esquerda para a direita. Um ponto desliza de y = 0 a y = 1 (a fatia andando).
  4. **"Chama u de ípsilon ao quadrado"**: embaixo do eixo y, uma segunda régua fina em GEO, `u = y²`, escrita a caneta. Marcas y 0 → u 0, y 0,5 → u 0,25, y 1 → u 1.
  5. **"Ípsilon igual a zero dá u igual a zero"** e **"ípsilon igual a um dá u igual a um"**: as marcas 0 e 1 da régua ganham um sublinhado fino, cada uma no seu gatilho.
  6. **"Em um, menos um sobre é; em zero, menos um"**: a área sob a curva pinta por tiras, da esquerda para a direita, em magenta com alpha 0,35. A pintura termina na frase **"Metade disso"**.
  7. **"zero vírgula três um seis"**: o `0,316` menta voa do resultado da coluna para dentro da área.
- **Aceite:** palco parado (medido **só no palco**) = 0 trechos acima de 5 s no B4-2b; flash = 0. O still final fica lado a lado com `v3_05`.

### D3 · Triângulo da cunha com tinta oliva
- **Onde:** B3-1, 8:33 (`D03`).
- **Hoje:** o triângulo da fatia em pé (2D) lê como oliva/verde-musgo: é o âmbar com alpha baixo sobre o violeta.
- **Troca:** use o mesmo preenchimento âmbar das faces do pouso e do `v3_04` (âmbar #FFC24D, alpha ≥ 0,55, borda âmbar cheia).
- **Aceite:** um still em 8:33 ao lado de `D01b`, com a mesma cor nas duas faces âmbar.

### D4 · Coluna sobreposta no glyph map do sen(x³)
- **Onde:** B6, 16:39 (`D04`).
- **Hoje:** a linha `∫₀^{x²} sen(x³) dy = sen(x³)[y]₀^{x²} …` monta com dois `sen(x³)` encavalados no meio da animação.
- **Troca:** dois degraus, cada um com o seu glyph map:
  - linha a: `∫₀^{x²} sen(x³) dy = sen(x³)·[y]₀^{x²}`; o `sen(x³)` desliza para fora da integral e o `dy` sai por `auto_fade`;
  - linha b: `= sen(x³)·(x² − 0) = x² sen(x³)`; o `x²` voa da chave do comprimento do painel ESTA FATIA, e o `− 0` acende em GEO e sai.

  Nenhum glifo cruza outro.
- **Aceite:** quadros a 50 % de cada glyph map, sem glifo sobreposto.

### D5 · "= x² −" sobreposto ao isolar o x
- **Onde:** B3-2, 8:51 (`D05`).
- **Hoje:** em `y² = 4 − x²` → `x² = 4 − y²`, o `x²` e o `y²` se cruzam no meio do caminho e o "=x²−" fica encavalado.
- **Troca:** o `x²` atravessa a igualdade por **cima**, com `path_arc` positivo, e o `y²` por **baixo**, com `path_arc` negativo. Os sinais saem por `auto_fade` e entram a caneta. A linha nova nasce **abaixo** da anterior, nunca em cima dela.
- **Aceite:** quadros a 25 %, 50 % e 75 % do glyph map, sem sobreposição.

### D6 · "2" solto na coluna
- **Onde:** B1-3, 5:27 (`D06`).
- **Hoje:** um `2` sozinho fica na coluna, abaixo do chip `∫₀² √(4 − x²) dx = π`. É sobra de uma linha que saiu (ou o rótulo do raio duplicado).
- **Troca:** a linha sai inteira, com todos os glifos; nenhum glifo fica para trás quando o resultado vira chip.
- **Aceite:** um still em 5:27 só com o chip na coluna.

### D7 · Glifos minúsculos dentro da região
- **Onde:** B1-1, 2:39 (`D07`).
- **Hoje:** há restos de rótulo de uns 6 px dentro da região, perto do arco e da fatia (à direita, junto do `y = √(4 − x²)` que encolheu, e perto do `0`).
- **Troca:** rótulo que encolhe ao sair **sai** (`FadeOut`); nada fica com escala < 0,5 na cena. Acrescente ao R5 a regra "objeto com altura < 10 px na tela = erro".
- **Aceite:** um still em 2:39 com o R5 novo zerado no B1.

### D8 · "e ≈ 2,718" apertado
- **Onde:** H1, 0:33 (`D08`).
- **Hoje:** o `e ≈ 2,718` fica colado à direita da integral, pequeno, parecendo um expoente.
- **Troca:** uma linha própria abaixo da integral, tamanho do corpo da coluna (≥ 26 px), escrita a caneta na frase **"o número de Euler"**.
- **Aceite:** um still em 0:33 com a folga ≥ 12 px até a integral.

### D9 · Traços fantasmas no S1
- **Onde:** S1, 20:45 (`D09`).
- **Hoje:** na vaga do terceiro painel aparecem dois tracinhos ciano soltos, antes do painel.
- **Troca:** o terceiro painel nasce inteiro (borda, título e conteúdo na mesma animação) no seu gatilho, **"uma fatia curva pode virar um retângulo"**. Antes disso, a vaga fica vazia.
- **Aceite:** stills 1 s antes e 1 s depois do gatilho.

### D10 · A cunha 3D ainda separa as peças
- **Onde:** B3-1/B3-2, cena 1 do Three.js, 8:20–9:10 (`D10`, em 9:03, a peça deitada sai pela borda de baixo do quadro).
- **Hoje:** a cunha separa as metades e a peça deitada cai para fora do quadro. A regra do Kaio é: a peça nunca se separa.
- **Nota:** no v3 eu disse que a cunha ficava como no v2. Vendo o v3, ela tem o mesmo defeito do sino antigo. Aplique o mesmo método.
- **Troca:** o método do sino, porte de `c3d34.html` (`traco()` e as duas câmeras):
  - **faca em pé em x = 1:** fica opaca a parte `0 ≤ x ≤ 1`, com a face âmbar (o triângulo, altura y, base √3); a parte `x > 1` vira traço #6C7698;
  - **faca deitada em y = 1:** fica opaca a parte `y ≥ 1`, com a face magenta (o retângulo, altura 1, comprimento √3); a parte `y < 1` vira traço;
  - uma câmera de frente para cada corte, com a mesma lógica de CAMP/CAMD; entre as duas, a órbita em 2 s com a peça inteira opaca;
  - enquadramento: a peça inteira dentro do palco (x < 1090), com margem ≥ 60 px até a borda e o canto livre;
  - rótulos do Manim presos aos pontos projetados, ≤ 2 px;
  - os pousos laterais e as faces que voam para os gráficos (D1) continuam iguais.
- **Aceite:** stills no estado final de cada faca, mais um quadro a cada 0,5 s da órbita. Nenhum pedaço afastado, nenhum vértice fora do quadro; alinhamento ≤ 2 px (`timeline.json`).

### D11 · Câmera da abertura perto do canto
- **Onde:** H0, 0:00–0:16 (`D11`, em 0:04).
- **Hoje:** a peça do sino sobe e encosta no bloco do canto (UMA INTEGRAL QUE TRAVA); a câmera está perto demais.
- **Troca:** recue a câmera cerca de 10 % na mesma direção (distância × 1,1) e abaixe o enquadramento até o topo da peça ficar ≥ 40 px abaixo do canto em todos os quadros do H0. Os ângulos de CAMP/CAMD não mudam, só a distância e o alvo em z.
- **Aceite:** quadros em 0:00, 0:02, 0:05, 0:09, 0:12 e 0:15, com a folga ao canto medida.

### D12 · Abertura do B4-1 lenta
- **Onde:** B4-1, primeiros 4–6 s.
- **Hoje:** os limites voam numa sequência lenta e descolada da fala.
- **Troca:** cada voo no seu gatilho:
  - `0` e `1` no eixo x em "xis vai de zero a um";
  - a reta `y = x` (azul-claro) em "a diagonal";
  - a reta `y = 1` (coral) em "ípsilon igual a um";
  - as tiras em pé em "essas fatias pintam um triângulo".
- **Aceite:** atraso de cada voo ≤ 0,2 s no `qa/sync.txt`.

### D13 · Gráfico do sino parado no H1
- **Onde:** H1, 0:21–0:33.
- **Hoje:** o gráfico de `e^(−y²)` fica parado por cerca de 12 s.
- **Troca:** em **"é elevado a menos ípsilon ao quadrado"**, um ponto ciano percorre a curva da esquerda para a direita (3 s), com a linha pontilhada da altura descendo até o eixo. Em **"teto curvo"** e **"teto reto"**, o realce acontece no gráfico (traço mais grosso na própria cor), como no v2.
- **Aceite:** palco parado no H1 = 0 trechos acima de 5 s.

---

## 4. Narração v3.2

Copie `narracao_v32.md` do zip por cima do `narracao.md` da unidade. São **4.035 palavras**, cerca de 22:25 de fala, com as mesmas 23 âncoras do v3. O que mudou em relação à v3:

- **Nenhuma referência a outro vídeo** fora do "no próximo vídeo" do S2. São três frases:

| Âncora | v3 | v3.2 |
|---|---|---|
| H1 | "Pela regra do vídeo passado, a gente começa por dentro" | "Pelo teorema de Fubini, a gente começa por dentro" |
| A1 | "No vídeo passado, o teorema de Fubini transformou a integral dupla num retângulo…" | "O teorema de Fubini transforma a integral dupla num retângulo…" |
| B1-2 | "Mas será que o teorema do vídeo passado ainda vale aqui?" | "Mas será que o teorema de Fubini ainda vale aqui?" |

- **Letras escritas como a voz lê:**
  - `f` → `éfe`;
  - `B` → `bê` (inclusive "bê um", "bê dois");
  - `R` → `erre`.

  O `é` do número de Euler, `xis`, `ípsilon`, `teta`, `u`, `dê u`, `cê`, `dê`, `á`, `bê` já estavam por extenso.

- **Degraus lidos que faltavam** (refino do GPT filtrado pela Produção; a tela já mostra esses degraus, agora a voz também lê):
  - H0: termina com "Como isso é possível?";
  - B1-1: "sobra ípsilon ao quadrado igual a três" antes de "raiz de três"; "E são essas curvas que vão virar os limites da integral";
  - B4-2b (C4): "os dois sinais de menos viram mais"; fecho "Ninguém inventou primitiva nova";
  - B4-3: "Essa escrita não define a integral que a gente quer";
  - B5-1 (C5): a primitiva de fora lida em dois e em zero;
  - B5-2 (C6): a primitiva `8y/3 + 2y³/3 − y⁴/3` lida antes dos valores;
  - B6-1 (C7): "cosseno de zero, que é um";
  - B7-1 (C8): a primitiva da direita; o comprimento deitado como "um menos ípsilon, menos o parêntese ípsilon menos um"; a primitiva `2y − y²` em um e em zero;
  - B8 (C9): "como o quadrado inteiro tem área um"; a curva normal "depois de ajustar a escala".

Nenhuma conta, tag ou primeira palavra de âncora mudou, e todos os gatilhos citados no §3 continuam no texto. Se um `self.gat("…")` do v3 citava `f`, `B` ou `vídeo passado`, troque pela grafia nova e liste no relatório. Rode a busca dos gatilhos contra o texto novo: `[gatilho-sem-frase]` = 0 antes de gerar a voz.

**Texto para gravação:** crie `narracao_tags.md` com a seção `## Texto corrido (para gravação)`, só com os parágrafos `> [...]`, na ordem, sem títulos.
- Tags: as que já estão ([curious], [thoughtful], [serious], [happy], [excited]), uma por parágrafo.
- Sem [slowly] e sem [pause].

Crie também `narracao_limpa.md`, sem tags, para o alinhamento e o `.srt`.

---

## 5. Voz (ElevenLabs v4)

Referência: `docs/roteiro_voz_elevenlabs_v4.md`.

1. Confirme `ELEVENLABS_API_KEY` (primeira parada, §0).
   - Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`.
   - Formato `mp3_44100_192`, decodificado para WAV mono 16 bits 44,1 kHz.
2. Rode primeiro com `--seco`, depois sem ele:

   ```
   uv run --no-sync python videos/gerar_voz_elevenlabs.py videos_longos/yt_0034_regioes_gerais_troca_ordem/narracao_tags.md videos_longos/yt_0034_regioes_gerais_troca_ordem/audio/narracao_v1.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)" --seco
   ```

3. **Uma tomada completa.** Siga com ela. O Kaio ouve em paralelo; se reprovar, ele regera e a §6 refaz tudo sozinha. A tomada aprovada vira `audio/narracao_final.wav`.
4. `qa/voz.txt`:
   - duração;
   - picos e clipping;
   - silêncio > 1,5 s dentro de um parágrafo;
   - tag lida em voz alta (procure na transcrição de conferência);
   - fronteiras entre blocos sem corte audível;
   - pronúncia de:
     - "éfe", "bê", "erre", "xis", "ípsilon", "cê de xis", "dê de xis", "á de ípsilon";
     - "teta", "u", "dê u", "é elevado a menos ípsilon ao quadrado", "o é é o número de Euler";
     - "raiz de quatro menos xis ao quadrado", "seno de xis ao cubo", "um menos cosseno de um", "sete dezesseis avos";
     - "pi", "Fubini", "Parallax Lab".
5. No relatório: modelo, voz, número de blocos, duração e taxa real (palavras ÷ segundos de fala).

---

## 6. Sincronização (a cena segue a voz)

Regras permanentes dos longos:
- WAV contínuo;
- **nunca** cortar a voz por âncora nem inserir silêncio;
- atraso imagem × fala **≤ 0,2 s** (LEAD 0,15 s);
- quando a fala é mais longa que a construção, a espera se divide entre os gatilhos, nunca tudo no fim da âncora.

1. `alinhar_voz.py` → `alinhamento_palavras.json`.
2. `ancoras.json` **gerado por script**: `gerar_ancoras.py` no modo tempo real. Cada âncora começa na primeira palavra do seu trecho (tabela abaixo). Os `self.gat("…")` são buscados no alinhamento.
3. **3D:** a linha do tempo do Three.js sai do mesmo `ancoras.json`. Re-renderize a cena 1 (cunha, já com o D10) e a cena 2 (sino: H0 com o D11, e B4-2). Rode o QA de alinhamento (≤ 2 px) e o QA dos pousos.
4. Rode os lotes 540p e confira:
   - `[gatilho-sem-frase]` = 0;
   - os `[estouro]`, cada um com o motivo. Estouro > 1 s numa âncora: encurte a animação dentro da regra da caneta (piso de 0,20 s por glifo) ou deixe a âncora seguinte começar mais tarde. **Nunca** acelere a voz.
5. `qa/sync.txt`: o atraso de cada âncora, de cada degrau das contas C1–C9 e de cada gatilho do §3 (meta ≤ 0,2 s).
6. **Legenda `.srt`** (`gerar_srt.py`):
   - até 2 linhas × 42 caracteres, de 2 a 5 s por bloco;
   - tempo do WAV = tempo do vídeo;
   - mantenha as trocas que o script já faz (xis → x, ípsilon → y etc.) e acrescente:
     - "éfe" → "f", "bê" (região) → "B", "bê um/dois" → "B₁/B₂", "erre" → "R";
     - "teta" → "θ", "pi" → "π";
     - "é" do número de Euler → "e" (só em "é elevado…", "sobre é", "o é é o número de Euler");
     - "Cálculo um" → "Cálculo I".

| Âncora | Começa em |
|---|---|
| H0 | "Olha esta peça. O volume dela" |
| H1 | "Vamos devagar. A integral é esta" |
| H2 | "A resposta está no desenho." |
| A1 | "Fala, pessoal! Bem-vindos ao Parallax Lab!" |
| B1-1 | "Volta no quarto de disco de raio" |
| B1-2 | "Mas será que o teorema de Fubini" |
| B1-3 | "Agora o caso mais simples: éfe igual" |
| B2-1 | "Agora o enunciado, com o rigor do" |
| B2-2 | "Trocando os papéis, vem a região que" |
| B3-1 | "Agora uma chapa em forma de quarto" |
| B3-2 | "Agora deitado. Primeiro, um passo que vai" |
| B4-1 | "Agora sim, a integral do começo." |
| B4-2 | "Segundo passo: reler o triângulo deitado." |
| B4-2b | "Terceiro passo: calcular. A de dentro" |
| B4-3 | "Cuidado com o erro mais comum nessa" |
| B5-1 | "Agora, para fixar o método, uma conta" |
| B5-2 | "E deitado? Congela o ípsilon." |
| B6-1 | "Mais uma, agora com curva: integral de" |
| B7-1 | "Mas às vezes uma ordem obriga a" |
| B7-2 | "Então, quando vale a pena trocar a" |
| B8 | "E onde isso aparece? Na probabilidade," |
| S1 | "Então, juntando tudo. Nas regiões que se" |
| S2 | "E fica um desafio. Olha a região" |

---

## 7. Conferência 540p com voz (antes do 1080p)

Render de **todos os lotes** em 540p/15 fps com os tempos da voz, e preview com voz. Feche o que falhar antes do 1080p.

**Portões:**
- `FLASH POR QUADRO` = 0;
- R5 = 0 a cada 0,2 s: texto × texto, texto × linhas/polígonos e polígono × linha (D1), também durante os voos e os glyph maps; objeto < 10 px = 0 (D7);
- margem segura e folga ao canto (D11);
- `\dfrac` ≥ 26 px, sem `\tfrac`, sem rótulo girado; `\text{}` só para nome de grandeza;
- alinhamento 3D ≤ 2 px; pousos sem pisca; nenhuma peça 3D separada (D10);
- **tela parada, medida só no palco: zero trechos acima de 5,0 s**; a lista de 3 a 5 s vai com a fala ao lado;
- `[gatilho-sem-frase]` = 0;
- tabela CONTAS: C1–C9, cada degrau com o tempo e a frase que o dispara, nenhum ausente;
- `qa_canto.py` e `qa_fundo.py`;
- logo em todos os quadros do A1;
- cartão do S2 ≥ 8 s, com os três itens no gatilho falado;
- SYNC e VOZ.

**Pranchas:**
- `correcoes_final.jpg`: para cada D1–D13, o quadro do erro (`referencia_final/`, quando houver) ao lado do quadro corrigido no gatilho do item.
- Uma prancha com **um quadro de cada âncora no instante da primeira palavra** (23 quadros).
- Lado a lado com os alvos v3 (`v3_01` … `v3_07`), para confirmar que nada regrediu.

---

## 8. Render final 1080p

1. **Three.js em 1080p** (cena 1 cunha, cena 2 sino), com a mesma câmera e a linha do tempo da voz, e QA 3D de novo sobre o 1080p.
2. **Manim em 1080p30** pelo fluxo normal, com `template/config_horizontal.py`.
   - Não configure CRF: o `template/qualidade.py` já usa **14** em renders ≥ 1080p.
   - Não recodifique. Sem teto de tempo de render.
3. **Emenda** com `montar_final.py` (remux, sem reencodar), na ordem dos lotes.
4. **Master:**

   ```
   uv run python videos/montar_master.py <sem_audio_1080p30.mp4> audio/narracao_final.wav renders/yt_0034_master_final_1080p30.mp4
   ```

   Confira:
   - 1920×1080, 30 fps;
   - duração do master = WAV (+ a cauda do CTA, se a montagem a mantiver);
   - `crf=14.0`, com o comando do AGENTS.md.
5. Se o disco apertar, apague só PNGs e renders 540p **desta** unidade já auditados.

---

## 9. QA final e entrega

**QA completo no vídeo final:**
- os portões do §7 sobre o 1080p (amostragem por lote);
- A/V contínuo;
- `crf=14.0`;
- `.srt` conferido em 5 pontos:
  - início;
  - meio;
  - fim;
  - a substituição trigonométrica do B1-3 (θ, π);
  - o passo 3 do sino (u, e, 0,316).
- `renders/capitulos_final.txt` com os tempos da voz:

| Âncora | Título |
|---|---|
| H0 | `UMA INTEGRAL QUE TRAVA` |
| A1 | `BEM-VINDOS` |
| B1-1 | `A FATIA QUE TERMINA NA CURVA` |
| B2-1 | `O TEOREMA EM REGIÕES GERAIS` |
| B3-1 | `A CUNHA NAS DUAS ORDENS` |
| B4-1 | `TROCAR A ORDEM: O SINO` |
| B4-3 | `O ERRO CLÁSSICO` |
| B5-1 | `A CHAPA NA DIAGONAL` |
| B6-1 | `SENO DE X AO CUBO` |
| B7-1 | `QUANDO A REGIÃO SE DIVIDE` |
| B7-2 | `QUANDO VALE TROCAR` |
| B8 | `NO MUNDO: PROBABILIDADE` |
| S1 | `SÍNTESE E DESAFIO` |

**Entrega:** `uv run python videos/entregar.py yt_0034` (cópia). A pasta em `entregas/` leva:
- `master`;
- `legenda` (`.srt`);
- `audio/`;
- `texto/`: ficha, `narracao_tags.md`, `narracao_limpa.md`, este handoff e os capítulos;
- `manifesto`.

O número `0034` vai no fim de cada nome. Não há capa. Série, EP e assunto vêm da `ficha.md`: `CÁLCULO III · EP. 09`, `# Regiões gerais e troca de ordem`.

**Na ficha:** a duração real.

Não rode `entregar.py` se um portão do §7 estiver aberto. Pare e reporte.

---

## 10. Relatório de entrega (obrigatório, e depois pare)

1. Arquivos alterados e criados (incluindo se o Anexo B foi aplicado agora ou já estava aplicado).
2. D1–D13, cada um com o caminho do still que prova, e a prancha `correcoes_final.jpg`.
3. Todos os portões do §7 com números reais, a tabela CONTAS, a sincronização das 23 âncoras e o QA de voz.
4. Caminhos: WAV, preview 540p com voz, master 1080p, `.srt`, capítulos e a pasta em `entregas/`.
5. Three.js: resolução, custo por quadro no 1080p, alinhamento medido (px), e o que foi portado de `c3d34.html` para a cunha.
6. Duração final e taxa real da voz, comparadas com 3 palavras/s.
7. Pendências reais.

Depois do relatório: **pare**. Não faça publicação, capa, commit nem push.

---

## Anexo A · Números congelados

| Onde | Conta | Valor |
|---|---|---|
| C1 · B1-3 | `∫₀² √(4 − x²) dx`, x = 2 sen θ, θ de 0 a π/2, `∫ 4cos²θ dθ = 2[θ + sen 2θ/2]₀^{π/2}` | `π ≈ 3,1416` (somas 3,25 / 3,17 / 3,15 com 8 / 16 / 32 fatias, como no v3) |
| C2 · B3-1 | `[y²/2]₀^{√(4 − x²)} = (4 − x²)/2`; `½[4x − x³/3]₀² = ½(8 − 8/3)` | `8/3` |
| C3 · B3-2 | `x = √(4 − y²)`; `∫₀² y√(4 − y²) dy`, u = 4 − y², y 0 → u 4, y 2 → u 0; `½∫₀⁴ √u du = ½·⅔·4^{3/2}` | `8/3` |
| Áreas cunha | `A(x) = (4 − x²)/2`, `A(1) = 1,5`; `A(y) = y√(4 − y²)`, `A(1) = √3 ≈ 1,73` | área 8/3 nos dois |
| C4 · B4-2b | `∫₀^y e^(−y²) dx = y e^(−y²)`; u = y², y 0 → u 0, y 1 → u 1; `½[−e^(−u)]₀¹ = ½(−1/e + 1)` | `(1 − 1/e)/2 ≈ 0,316` (0,31606) |
| Áreas sino | `A(x) = (√π/2)(erf 1 − erf x)`: A(0) = 0,7468, A(0,2) ≈ 0,549; `A(y) = y e^(−y²)`: A(0,6) ≈ 0,419 | área 0,316 nos dois |
| C5/C6 · B5 | f = x² + y² no triângulo 0 ≤ y ≤ x ≤ 2. Em pé: `[x²y + y³/3]₀^x = 4x³/3`, `(4/3)[x⁴/4]₀²`. Deitado: `[x³/3 + y²x]_y² = 8/3 + 2y² − 4y³/3`, `[8y/3 + 2y³/3 − y⁴/3]₀²` | `16/3` nas duas ordens |
| C7 · B6 | `∫₀¹ x² sen(x³) dx`, u = x³; `⅓[−cos u]₀¹` | `(1 − cos 1)/3 ≈ 0,153` |
| C8 · B7-1 | telhado. Em pé: `[x + x²/2]₋₁⁰ + [x − x²/2]₀¹ = ½ + ½`. Deitado: `∫₀¹ (2 − 2y) dy = [2y − y²]₀¹` | `1` nas duas |
| C9 · B8 | `1 − 2·(½·¾·¾) = 1 − 9/16` | `7/16 ≈ 43,75 %` |
| S2 | região entre y = x e y = 4x − x², 0 ≤ x ≤ 3; `x = 2 ∓ √(4 − y)`; a saída troca em y = 3 | área `9/2` (só no EP. 10) |

---

## Anexo B · Regra CONTAS SEM PULAR nos docs (conferir antes de tudo)

O handoff v3 (§10) autorizou duas edições globais, a pedido explícito do Kaio. Confira se elas existem:
- `AGENTS.md`, seção "Animações matemáticas": o item **Contas sem pular (desde 2026-11-14)**;
- `docs/padrao_video_longo.md`, fim do §8: a subseção **8.x Contas sem pular (desde 2026-11-14)**.

Se as duas já estão lá, não mexa e diga isso no relatório. Se faltar alguma, aplique **só** o texto abaixo, nada mais desses arquivos.

**a) `AGENTS.md`**, logo depois do item **Escrita (desde 2026-11-08)**:

```
- **Contas sem pular (desde 2026-11-14):** toda conta, em longo ou curto, é desenvolvida passo a passo, na tela e na fala, do básico ao avançado. Nenhum resultado aparece sem os degraus:
  - primitiva com colchete `[G]ₐᵇ` → `G(b) − G(a)` com os valores substituídos → número;
  - substituição com a linha `u = … ⇒ du = …`, a linha dos limites novos e o sinal quando o limite inverte;
  - substituição trigonométrica com o triângulo no desenho;
  - comprimento da fatia = saída − entrada;
  - número que vem da geometria nasce no desenho com chave e voa para a coluna.
  Nada de "dá" nem de seta pulando degrau; a narração lê cada degrau (acrescentar frases se preciso). O QA lista cada conta com o tempo de cada degrau. Detalhe: `docs/padrao_video_longo.md` §8.
```

**b) `docs/padrao_video_longo.md`**, no fim do §8:

```
### 8.x Contas sem pular (desde 2026-11-14)

Regra do Kaio para todos os vídeos com conta. Cada degrau é uma linha a caneta ou um TransformByGlyphMap a partir da linha de cima.

| Forma | Escada obrigatória |
|---|---|
| O1 primitiva | `∫ₐᵇ g = [G]ₐᵇ = G(b) − G(a) = número` (G(b) e G(a) escritos com os valores) |
| O2 geometria | a expressão nasce no desenho com chave (base·altura/2, πr², altura = 2 cos θ…) e voa para a coluna |
| O3 comprimento | `[x]` ou `[y]` entre os limites → saída − entrada |
| O4 substituição | `u = … ⇒ du = … ⇒ (pedaço) = …du`; linha dos limites novos; linha do sinal se o limite inverte |
| O5 valor no ponto | `f(x₀, y₀)` com a conta |
| O6 fórmula-mãe | a fórmula geral antes de qualquer número |

- A coluna tem no máximo 7 linhas; o resultado parcial vira chip no topo; nunca linha órfã começando por "=".
- A narração lê cada degrau; se a fala não cobre um degrau, acrescentar a frase.
- QA obrigatório: tabela "CONTAS" com cada degrau, o tempo em que aparece e a frase que o dispara. Nenhum degrau ausente.
- Modelo: as contas C1–C9 do yt_0034 (handoff v3 §2).
```

Sem commit nem push.
