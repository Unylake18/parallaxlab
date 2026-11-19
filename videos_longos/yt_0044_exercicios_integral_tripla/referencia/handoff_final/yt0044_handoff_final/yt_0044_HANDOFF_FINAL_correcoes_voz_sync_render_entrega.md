# yt_0044 · CÁLCULO III · EP. 19 · Exercícios do módulo: integral tripla · HANDOFF FINAL
**Cinco correções de tela (F1–F5) + narração final + voz + sincronização + legenda `.srt` + render 1080p + master + entrega**

Arquivo único e autocontido. Data: 2026-11-18.

**Base:** o preview v2 (28:55, 960×540, 15 fps, sem voz), do zip `yt0044_v2_para_gpt` e dos quadros em quatro partes. O v2 cumpriu o handoff v2:
- **3D:** as 16 cenas reproduzem os alvos v2. O está num cruzamento de 60 px (erro 0,000 px em todos os quadros). As medidas são cotas fora do objeto. Não há arame redundante (Q25). A menor distância entre marcas é ≥ 40 px (Q24). Nada do 3D sobe no canto nem passa do clip (Q26, sólido).
- **Pendências do v1, resolvidas:** maior atraso de gatilho +0,13 s; palco vazio > 0,5 s = 0; as oito emendas têm o fundo idêntico (diferença média ≤ 0,58).
- **Escrita e contas:** FLASH = 0; R5 = R5V = R6 = 0; 63/63 degraus da proposta com tempo; GM1–GM21.
- **Alinhamento 3D × Manim:** pior 0,010 px.

O vídeo está **aprovado para a narração**. Faltam cinco detalhes de tela (F1–F5, §3). Depois vem o fechamento completo.

No zip `yt0044_handoff_final_completo.zip` vão:
- este documento;
- `yt_0044_narracao_v1_1_final.md` (**narração final**: v1 + 3 frases da revisão do GPT; ver §4) e `yt_0044_narracao_v1.md` (só referência do tempo do preview);
- `yt_0044_v1_avaliacao_e_handoff_v2.md` (histórico) e `quadros_alvo_v2/` (referência);
- `provas_v2/` (os recortes do v2 que mostram F2 e F3, alvo à esquerda e preview à direita).

Onde este documento não diverge, continuam valendo o handoff v1.1, o handoff v2 e os alvos v2.

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
- publicação, capa, `commit`, `push`, `merge`, `branch`, PR;
- qualquer mudança em `template/`, `assets/`, `pyproject.toml`, `uv.lock`, `AGENTS.md`, `docs/` ou em outras unidades.

**O que pode ser alterado:**
- só `videos_longos/yt_0044_exercicios_integral_tripla/` (ou o nome que a unidade tem; o mesmo do preview v2);
- `renders/` e `entregas/`, que são saída.

**O que pode ser copiado** (sem alterar a origem), da unidade mais recente da série que já tenha esses scripts (`yt_0043_centro_massa_momento_inercia/`, `yt_0041_coordenadas_esfericas/` ou `yt_0037_coordenadas_polares/`, nessa ordem de preferência):
- `alinhar_voz.py`, o modo tempo real do `gerar_ancoras.py`, `gerar_srt.py`, `capitulos.py`;
- `render1080.sh`, `render1080_fila.sh`, `montar_final.py`;
- `qa_canto.py`, `qa_fundo.py`, `qa_sync.py`, `qa_voz.py`, `qa_1080.py`, `prancha_ancoras.py`, `stills_final.py`.

**Modo de execução:**
- Não encerre a vez entre etapas.
- Depois de lançar um render (Manim ou Three.js) ou a voz, espere na mesma vez e siga para a auditoria. Use comando em primeiro plano com timeout de até 10 min por lote, ou um laço `until` sobre o arquivo de saída.
- Mensagem de progresso não é entrega.
- Logs longos vão para arquivo; leia só o fim e os erros.

**Só há duas paradas permitidas:**
1. A variável `ELEVENLABS_API_KEY` não existe na sessão. Peça ao Kaio. **Nunca** grave a chave em arquivo, log ou relatório.
2. O WAV passa de **31:30**. Reporte a duração e pare (estimativa: 5.191 palavras a 3 palavras/s, tabela da v1.1 ≈ 29:04; o preview v2 tem 28:55).

Qualquer outra dúvida: escolha a leitura mais provável, diga qual e siga.

**Ordem:**
1. §3 correções no código, com stills de conferência (sem voz, tempos do v2 como rascunho);
2. §4 narração e busca dos gatilhos;
3. §5 voz;
4. §6 sincronização;
5. §7 conferência 540p com voz;
6. §8 1080p;
7. §9 QA e entrega;
8. §10 relatório.

Pare só depois do relatório. Guarde este arquivo na unidade como `handoff_final.md`.

---

## 1. Estado de partida

- **Unidade:** a do preview v2, com o código das seções (`sec_*.py`), o kit, `threejs/c44.js` v2 e os scripts de QA do v2 (Q21–Q29, `sonda3d.py`, `alinhamento3d`, `gatilhos`, `conta_inteira`, `flash_por_quadro`).
- **Não reabrir:**
  - a matemática e os números (Anexo A);
  - as contas, degrau por degrau (63/63);
  - a ordem PH → PA → PE1 → PE2 → PE3 → PE4 → PE5 → PE6 → PS;
  - o sistema 3D: G1–G6 do v1.1 e G7–G12 do v2 (piso finito com moldura, escala sem corte, O na grade com `SNAP`, cotas, marcas ≥ 40 px, sem arame redundante);
  - os alvos v2;
  - as cores:

    | Grandeza | Cor |
    |---|---|
    | s (distância ao eixo) | pêssego `#FFC08A` |
    | fator do volume (s, r² sen φ) | lima `#C6F26B` |
    | θ | verde-água `#2EE6A6` |
    | z | azul `#5AA2FF` |
    | x | âmbar `#FFC24D` |
    | y | magenta `#EA63FF` |
    | r | laranja `#FF9440` |
    | φ, α | violeta `#B48CFF` |
    | ρ (densidade) | ciano `#35D9FF` |
    | u, w | `#E08A3C` |
    | d | lilás `#B9A6FF` |
    | hélice | `#FFB36B` |
    | ⊕ | anel ciano → magenta |

  - nenhum efeito novo: sem pulso, brilho, palco vivo, tracer, partícula ou sombra (`_sem_vivo = True` se o kit tiver palco vivo).
- **Notação:** ρ = densidade, s = distância ao eixo, r = distância até a origem, R, h, L fixos, k = densidade constante, d = distância entre eixos paralelos, θ lido **téta**.
- **A cena segue a voz.** Os tempos do v2 não valem mais. Todos os lotes, inclusive os quadros do Three.js, são re-renderizados com a linha do tempo da voz.

---

## 2. Avaliação do v2 (resumo)

Conferi em resolução cheia os 16 pares alvo v2 × preview v2 (`comparacao_v2/`) e os 29 itens de QA. O 3D está igual aos alvos e limpo; os relatórios batem com os quadros. Os únicos defeitos visíveis são os cinco do §3. O F1 é herança dos meus alvos v2 (o próprio QA marcou `Q21 = NÃO`).

---

## 3. Correções (lista fechada)

### F1 · Piso cortado pela borda ou pelo clip (Q21 = NÃO)

**Onde:** `lataParede` (H1), `lataDobradica` (E5-1 etapa 1), `lataDob3` (E5-2), `cone`, `coneCm`, `coneCasca` (E3-1/2/3), `semi`, `semiFatia` (E4-1/2), `helice` (S2). Medido no `q21_piso_v2.txt`:

| Cena | Piso x (1080p) | Limite | Corte |
|---|---|---|---|
| lataParede / helice | 14..977 | 60..975 | esq −46, dir −2 |
| lataDobradica | 65..1069 | 60..975 | dir −94 |
| lataDob3 | −32..737 | 60..720 | esq −92, dir −17 |
| cone / coneCm / coneCasca | −67..821 | 60..820 | esq −127, dir −1 |
| semi / semiFatia | −44..795 | 60..820 | esq −104 |

**O que fazer:** em `threejs/c44.js`, na tabela `PISOK`, encolha o piso dessas cenas **só no lado que corta** (o piso pode ser assimétrico; as linhas internas continuam a cada 0,5 a partir da origem, e a moldura fecha onde o piso termina). Valores de partida, a confirmar pela sonda:
- `lataParede`, `helice`: [−1,25; 1,25] × [−1,25; 1,25];
- `lataDobradica`: [−0,5; 2,25] × [−1,25; 1,25];
- `lataDob3`: [−0,25; 2,25] × [−1,25; 1,25];
- `cone*`: [−1,1; 1,1] × [−1,1; 1,1];
- `semi*`: [−1,15; 1,15] × [−1,15; 1,15].

**Regras:** o piso continua maior que a sombra do sólido em **≥ 0,1 u** de cada lado; a câmera, a escala, o `SNAP` e o sólido **não** mudam; nada de mover o 3D.

**Aceite:** `q21_piso.txt` = OK em todas as 17 cenas, com folga ≥ 20 px em cada lado (x ≥ 80 e x ≤ clip − 20; y ≤ 1060); `q22` continua 0,000 px; stills dos cinco quadros-alvo afetados (01, 12–14, 16–17, 19–20, 26) lado a lado com o v2.

### F2 · E5-2: as células gêmeas + e − na borda da tampa (`lataDob3`, estado `p2`)

**O que está errado:** as duas celulinhas lima ficam em cima da borda da tampa; a placa `−` fica meio coberta pela lata (recorte em `provas_v2/cmp_20.jpg`).

**O que fazer:** coloque as duas células em **s = 0,6 R** do centro da lata, em θ = 0 (`+`) e θ = π (`−`), em cima da tampa (z = h + 0,005), e as placas `+` e `−` **fora** da tampa, presas à célula por proximidade (sem haste), a ≥ 40 px da célula, de qualquer outra marca e da borda da tampa.

**Aceite:** placas inteiras e legíveis; Q24 ≥ 40 px com o par mais próximo listado; still do E5-2 com o estado `p2`.

### F3 · E1-4: a placa `1/2` encostada no ⊕ (`cuboDiag`)

**O que está errado:** a menor distância é 43,7 px (placa `5/9` × ⊕), e a placa `1/2` fica a ~45 px do ⊕ do outro lado (recorte em `provas_v2/cmp_06.jpg`). Passa no limite, mas a leitura fica apertada.

**O que fazer:** leve a placa `1/2` para baixo e à esquerda do tracinho GEO de (½, ½, ½), na direção perpendicular à diagonal na tela, e a placa `5/9` para cima e à direita do ⊕, até a menor distância entre os centros de `1/2`, `5/9`, ⊕ e o tracinho ficar **≥ 60 px**. A diagonal tracejada não pode passar por baixo de nenhuma das duas placas.

**Aceite:** Q24 do E1-4 ≥ 60 px, com o par mais próximo listado; still do E1-4.

### F4 · H1: o primeiro quadro sem a linha 2 do canto

**O que está errado:** `palco_parado_v2.txt` registra `canto sem a linha 2: 1` em PH H1, no quadro 0.

**O que fazer:** o canto (`CÁLCULO III · INTEGRAL TRIPLA` + `A LATA NA DOBRADIÇA`) entra **inteiro** no primeiro quadro do vídeo, sem animação de escrita.

**Aceite:** `qa_canto.py` = 0 em todos os quadros; still do quadro 0.

### F5 · S2: a seta da força na cor do campo

**O que está errado:** no S2 a seta `F` está azul (`#5AA2FF`, a cor do z). No próximo vídeo da série, o campo F é **verde-menta `#2EE6A0`**, e a hélice (`#FFB36B`) é a mesma.

**O que fazer:** a seta `F` do estado `F` da cena `helice` e a placa `F` passam para `#2EE6A0`; a legenda `A FORÇA EMPURRA A CONTA` também (quadradinho e texto). A espessura, o tamanho e a posição não mudam.

**Aceite:** still do S2 com a seta menta; `alinhamento3d` do PS ≤ 2 px.

**Depois do F1–F5:** prancha `correcoes_final.jpg` com os antes/depois.

---

## 4. Narração final

Arquivo: **`yt_0044_narracao_v1_1_final.md`** (no zip). É a fonte do `gerar_ancoras.py` e da voz; a v1 fica só como referência do tempo do preview v2. Tem **5.191 palavras ≈ 29:04** (+23 palavras sobre a v1). O texto é a v1 palavra por palavra, com três trechos trocados, listados no topo do arquivo:
- **E4-1:** a primitiva do seno vezes o cosseno, explicada pela derivada do seno ao quadrado;
- **E5-1:** uma frase nova ("esse s mede a distância até o centro da lata, não até a dobradiça");
- **E6-3:** "se a bola é maciça e uniforme" no dois quintos.

Nenhuma tela muda: a cena segue a voz. **Nenhum gatilho mudou**: os 176 batem com a fala (conferido por script, tokens contíguos, na ordem). Se o Kaio colar outra narração refinada junto deste handoff, ela substitui a v1.1 do mesmo jeito: refaça a busca de gatilhos e reporte os que mudaram.

**Regras já aplicadas na v1.1 (não alterar):**
- A tela mostra a conta inteira; a voz conversa como professor (marcação [ensina]/[mecânica] por linha da coluna), sem ler número por número e sem silêncio. Não encurtar.
- Letras latinas com a caixa da tela (s, x, y, z, r, R, h, k, u, w, d, L, M, I, n); "x barra", "z barra"; gregas pelo nome ("rô", "fi", "alfa", "pi", "delta"); θ sempre **téta**.
- Nenhum vídeo citado como existente: as cilíndricas, as esféricas e o momento de inércia aparecem só como conteúdo. "No próximo vídeo" só no cartão do S2.

**Passos:**
1. Gere `narracao_tags.md` (com a seção `## Texto corrido (para gravação)`) e `narracao_limpa.md` a partir da v1.1, como no yt_0043. Tags de áudio `[ ]` em inglês, uma por trecho, base `[thoughtful]`/`[curious]`, `[excited]` só na descoberta (E5-2), sem `[slowly]`; sem tags na legenda.
2. `grep -c '\bteta\b'` = 0 na fala, nos gatilhos e nos arquivos de tags.
3. Rode a busca de gatilhos: `[gatilho-sem-frase]` = 0 antes da voz.

---

## 5. Voz (ElevenLabs v4)

Referência: `docs/roteiro_voz_elevenlabs_v4.md`.

1. Confirme `ELEVENLABS_API_KEY` (primeira parada, §0).
   - Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`.
   - Formato `mp3_44100_192`, decodificado para WAV mono 16 bits 44,1 kHz.
2. **Amostras de pronúncia primeiro** (curtas, para o Kaio ouvir em paralelo). Gere 6 mp3 em `audio/teste_pronuncia/` com estas frases e siga sem esperar:
   - "O x barra é cinco nonos, e o z barra é um quinto."
   - "Com w igual a x mais y, o d w é d y."
   - "Rô igual a k vezes r, e o centro sobe para dois quintos de R."
   - "Com téta indo de menos pi sobre dois a pi sobre dois, s vai até dois R cosseno de téta."
   - "r ao quadrado seno de fi, e a tangente de alfa é R sobre h."
   - "Três décimos de M R ao quadrado, e o cubo pela aresta dá dois terços de M L ao quadrado."
3. Rode `narracao_tags.md` com `--seco`, depois sem ele:
   ```
   uv run --no-sync python videos/gerar_voz_elevenlabs.py videos_longos/yt_0044_exercicios_integral_tripla/narracao_tags.md videos_longos/yt_0044_exercicios_integral_tripla/audio/narracao_v1.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)" --seco
   ```
4. **Uma tomada completa.** Siga com ela. O Kaio ouve em paralelo; se reprovar, ele regera e a §6 refaz tudo sozinha. A tomada aprovada vira `audio/narracao_final.wav`.
5. `qa/voz.txt` (`qa_voz.py`):
   - duração;
   - picos e clipping;
   - silêncio > 1,5 s dentro de um parágrafo;
   - tag lida em voz alta;
   - fronteiras sem corte audível;
   - pronúncia de:
     - letras: "x barra", "z barra", "s", "r", "R", "k", "u", "w", "d", "L", "n", "d V", "d m", "téta" (nunca "teta"), "fi", "alfa", "rô", "pi", "delta z";
     - números: "três meios", "cinco nonos", "um doze avos", "um sessenta avos", "um noventa e seis avos", "três oitavos", "dois quintos", "três décimos", "sete quintos", "onze meios";
     - nomes: "Steiner", "Riemann", "Parallax Lab".
6. No relatório: modelo, voz, número de blocos, duração e taxa real (palavras ÷ segundos de fala).

---

## 6. Sincronização (a cena segue a voz)

Regras permanentes dos longos:
- WAV contínuo;
- **nunca** cortar a voz por âncora nem inserir silêncio;
- atraso imagem × fala **≤ 0,2 s** (LEAD 0,15 s);
- quando a fala é mais longa que a construção, a espera se divide entre os gatilhos, nunca tudo no fim da âncora;
- a caneta **não acelera**; nada é escrito em silêncio.

1. `alinhar_voz.py` → `alinhamento_palavras.json`.
2. `ancoras.json` **gerado por script**: `gerar_ancoras.py` no modo tempo real, lendo `referencia/yt_0044_narracao_v1_1_final.md`. Cada âncora começa na primeira palavra do seu trecho. Os `self.gat("…")` são buscados no alinhamento.
3. **3D:** a linha do tempo do Three.js sai do mesmo `ancoras.json`.
   - Re-renderize todas as cenas com estado animado (sonda, caixas, fatia, casca, seta de giro, hélice que cresce, troca `lataParede` → `lataDobradica`, estados `p1`/`p2`/`p3`).
   - Rode o QA 3D da unidade: alinhamento ≤ 2 px; Q21 (com o F1), Q22, Q24, Q26; trocas de cena com corte limpo no gatilho.
4. Rode os lotes 540p e confira:
   - `[gatilho-sem-frase]` = 0;
   - os `[estouro]`, cada um com o motivo. Estouro > 1 s numa âncora: deixe a âncora seguinte começar mais tarde (a voz continua) ou divida a espera entre os degraus. **Nunca** acelere a voz nem a caneta.
5. `qa/sync.txt` (`qa_sync.py`): o atraso de cada âncora, de cada degrau das contas (os 63 da tabela CONTAS) e de cada gatilho (meta ≤ 0,2 s).
6. **Legenda `.srt`** (`gerar_srt.py`):
   - até 2 linhas × 42 caracteres, de 2 a 5 s por bloco;
   - tempo do WAV = tempo do vídeo;
   - trocas:
     - "x barra" → x̄, "y barra" → ȳ, "z barra" → z̄; letras sozinhas ficam como na tela (s, r, R, h, k, u, w, d, L, M, I, n);
     - "téta" → θ, "fi" → φ, "alfa" → α, "rô" → ρ, "pi" → π, "delta z" → Δz;
     - "d s", "d z", "d téta", "d w", "d y", "d m", "d V" → ds, dz, dθ, dw, dy, dm, dV;
     - "Cálculo três" → "Cálculo III".

---

## 7. Conferência 540p com voz (antes do 1080p)

Render de **todos os lotes** em 540p/15 fps com os tempos da voz, e preview com voz. Feche o que falhar antes do 1080p.

**Portões:**
- `FLASH POR QUADRO` = 0;
- sem pulso nem palco vivo (efeito não pedido) e sem tracer;
- **GRADE** de tela inteira em todo quadro 2D e papel sob o 3D;
- **Q21–Q26 do v2** sobre o vídeo com voz (piso inteiro com folga ≥ 20 px; O na grade ≤ 2 px; cotas; marcas ≥ 40 px, E1-4 ≥ 60 px; sem arame; nada cortado);
- R5 = 0 a cada 0,2 s, também durante os voos; R5V = 0;
- R6 (margens) = 0; zona do logo (x > 1600, y < 130) sem texto;
- COLUNAS ≤ 7 linhas, folga do rodapé ≥ 40 px;
- `\text` com palavra no MathTex = 0;
- canto: inteiro desde o quadro 0 (F4) e trocado no primeiro play de cada bloco;
- tamanhos: corpo ≥ 26 px, algarismo ≥ 30 px, fórmula principal 44–58;
- alinhamento 3D ≤ 2 px; trocas de cena sem pisca;
- palco vazio ≤ 0,5 s, varredura a cada 0,2 s; tela só com papel e título = 0 fora do A1 e do CTA;
- emendas: diferença média de fundo ≤ 1,0 em todas;
- `[gatilho-sem-frase]` = 0;
- tabela CONTAS com cada degrau (63), o tempo e a frase que o dispara;
- `qa_canto.py` e `qa_fundo.py`;
- cartão `NO PRÓXIMO VÍDEO · INTEGRAIS DE LINHA` do S2 ≥ 8 s, sem sobreposição com o CTA; o desafio do cone **não** aparece na tela;
- SYNC e VOZ.

**Pranchas:**
- `correcoes_final.jpg`: F1–F5 com antes/depois;
- uma prancha com **um quadro de cada âncora no instante da primeira palavra** (27 quadros);
- lado a lado com os 26 alvos v2;
- pranchas 3D por lote.

---

## 8. Render final 1080p

1. **Three.js em 1080p** (todas as cenas), com a mesma câmera e a linha do tempo da voz, e QA 3D de novo sobre o 1080p.
2. **Manim em 1080p30** pelo fluxo normal, com `template/config_horizontal.py`.
   - Não configure CRF: o `template/qualidade.py` já usa **14** em renders ≥ 1080p.
   - Não recodifique. Sem teto de tempo de render.
3. **Emenda** com `montar_final.py` (remux, sem reencodar), na ordem PH → PA → PE1 → PE2 → PE3 → PE4 → PE5 → PE6 → PS.
4. **Master:**
   ```
   uv run python videos/montar_master.py <sem_audio_1080p30.mp4> audio/narracao_final.wav renders/yt_0044_master_final_1080p30.mp4
   ```
   Confira:
   - 1920×1080, 30 fps;
   - duração do master = WAV (+ a cauda do CTA, se a montagem a mantiver);
   - `crf=14.0`, com o comando do AGENTS.md.
5. Se o disco apertar, apague só PNGs e renders 540p **desta** unidade já auditados.

---

## 9. QA final e entrega

**QA completo no vídeo final (`qa_1080.py`):**
- os portões do §7 sobre o 1080p (amostragem por lote);
- A/V contínuo;
- `crf=14.0`;
- `.srt` conferido em 6 pontos:
  - início;
  - `∑ρΔV = 3/2` (E1-1);
  - `M = 1/12` (E2-2);
  - `z̄ = 3h/4` (E3-2);
  - `I_z = (3/2)MR²` (E5-2);
  - fim.
- `renders/capitulos_final.txt` com os tempos da voz:

| Âncora | Título |
|---|---|
| H1 | `A LATA NA DOBRADIÇA` |
| H2 | `A RECEITA EM QUATRO PERGUNTAS` |
| A1 | `BEM-VINDOS` |
| E1-1 | `O CUBO: A SOMA DE RIEMANN` |
| E1-2 | `O LIMITE DAS SOMAS` |
| E1-3 | `O CUBO: A CONTA EXATA` |
| E1-4 | `ONDE O CUBO EQUILIBRA` |
| E1-5 | `A FOLHA QUE NÃO PESA` |
| E2-1 | `O TETRAEDRO: SOMBRA E SONDA` |
| E2-2 | `O TETRAEDRO: A MASSA` |
| E2-3 | `CONFERINDO PELO CENTROIDE` |
| E2-4 | `ONDE O TETRAEDRO EQUILIBRA` |
| E3-1 | `O CONE EM CILÍNDRICAS` |
| E3-2 | `ONDE O CONE EQUILIBRA` |
| E3-3 | `QUANTO CUSTA GIRAR O CONE` |
| E3-4 | `O CONE EM ESFÉRICAS` |
| E4-1 | `A MEIA BOLA` |
| E4-2 | `CONFERINDO POR FATIAS` |
| E4-3 | `DENSIDADE QUE CRESCE PARA FORA` |
| E5-1 | `A LATA NA DOBRADIÇA: MONTAR` |
| E5-2 | `TRÊS PEDAÇOS` |
| E5-3 | `CONFERINDO COM O POLO NA DOBRADIÇA` |
| E6-1 | `O TEOREMA DOS EIXOS PARALELOS` |
| E6-2 | `O CUBO PELA ARESTA` |
| E6-3 | `A BOLA ENCOSTADA E O ERRO CLÁSSICO` |
| S1 | `A RECEITA E OS CINCO ERROS` |
| S2 | `E SE A SOMA FOR AO LONGO DE UM CAMINHO?` |

**Entrega:** `uv run python videos/entregar.py yt_0044` (cópia).
- O destino tem de ser o `entregas/` do checkout principal.
- A pasta leva:
  - `master`;
  - `legenda` (`.srt`);
  - `audio/`;
  - `texto/`: ficha, `narracao_tags.md`, `narracao_limpa.md`, este handoff e os capítulos;
  - `manifesto`.
- O número `0044` vai no fim de cada nome. Não há capa.
- Série, EP e assunto vêm da `ficha.md`: `CÁLCULO III · EP. 19`, `# Exercícios do módulo: integral tripla`. Se o Kaio mudar o número antes da entrega, ele avisa; sem aviso, use o da ficha.
- **Na ficha:** a duração real.

Não rode `entregar.py` se um portão do §7 estiver aberto. Pare e reporte.

---

## 10. Relatório de entrega (obrigatório, e depois pare)

1. Arquivos alterados e criados.
2. F1–F5, cada um com o caminho do still que prova, e a prancha `correcoes_final.jpg`.
3. Todos os portões do §7 com números reais, a tabela CONTAS, a sincronização das 27 âncoras e o QA de voz.
4. Caminhos: WAV, amostras de pronúncia, preview 540p com voz, master 1080p, `.srt`, capítulos e a pasta em `entregas/`.
5. Three.js: cenas, resolução, custo por quadro no 1080p, alinhamento medido (px), e os `PISOK` finais do F1.
6. Duração final e taxa real da voz, comparadas com 3 palavras/s.
7. Pendências reais.

Depois do relatório: **pare**. Não faça publicação, capa, commit, merge nem push.

---

## Anexo A · Números congelados

- **E1 · cubo** 0 ≤ x, y, z ≤ 1, ρ = x + y + z:
  - chute ρ(centro)·V = 3/2; Riemann n = 2 no ponto médio = 12 · 1/8 = 3/2;
  - canto de baixo 3/4, canto de cima 9/4; limites 3/2 ∓ 3/(2n); CIMA − BAIXO = 3/n;
  - Fubini: ∫(x + y + z)dz = x + y + 1/2; ∫ dy = x + 1; ∫ dx = 3/2;
  - M_yz = 1/3 + 1/4 + 1/4 = 5/6; x̄ = ȳ = z̄ = 5/9 ≈ 0,556;
  - folha z = 1: 0 ≤ soma ≤ 3Δz → 0.
- **E2 · tetraedro** x + y + z ≤ 1 no primeiro octante, ρ = x + y:
  - M = 1/12 (w = x + y); centroide (1/4, 1/4, 1/4), ρ = 1/2, V = 1/6, 1/2 · 1/6 = 1/12;
  - ρ = x²: o certo dá 1/60, o atalho daria 1/96;
  - M_xy = 1/60 (trocando a ordem em (x, w)); z̄ = 1/5 (centroide em 1/4).
- **E3 · cone** vértice na origem, (h/R)s ≤ z ≤ h, ρ = k:
  - V = πR²h/3; z̄ = 3h/4 do vértice (h/4 da tampa);
  - I_z = (3/10)MR² (1/4 − 1/5 = 1/20);
  - em esféricas: φ ≤ α, tg α = R/h, r ≤ h/cos φ, u = cos φ ⇒ V = πR²h/3.
- **E4 · meia bola** raio R, ρ = k:
  - M = (2/3)πkR³; M_xy = πkR⁴/4; z̄ = 3R/8;
  - fatias: área π(R² − z²), mesmo resultado;
  - ρ = kr ⇒ z̄ = 2R/5; casca fina ⇒ z̄ = R/2.
- **E5 · lata na dobradiça** (x − R)² + y² ≤ R², 0 ≤ z ≤ h, ρ = k:
  - x = R + s cos θ, y = s sen θ: x² + y² = R² + 2Rs cos θ + s²;
  - pedaços: MR² + 0 + MR²/2 = (3/2)MR²;
  - polo na dobradiça: s ≤ 2R cos θ, −π/2 ≤ θ ≤ π/2, ∫cos⁴θ dθ = 3π/8 ⇒ (3/2)MR².
- **E6 · Steiner:** I = I_cm + Md²;
  - cubo pela aresta: I_cm = (1/6)ML², d² = L²/2 ⇒ (2/3)ML²;
  - bola maciça encostada: (2/5 + 1)MR² = (7/5)MR²;
  - erro clássico entre as duas paredes: (3/2 + 4)MR² = (11/2)MR² (errado); certo (3/2)MR².
- **Gancho S2:** hélice s = R, θ = t, z = ct na parede da lata; cartão "NO PRÓXIMO VÍDEO · INTEGRAIS DE LINHA". Desafio dos comentários (só na fala): momento de inércia do cone em torno de um diâmetro da tampa.
