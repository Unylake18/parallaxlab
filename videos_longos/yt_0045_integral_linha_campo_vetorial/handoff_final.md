# yt_0045 · CÁLCULO III · EP. 20 · Integral de linha de um campo vetorial · HANDOFF FINAL
**Oito correções de tela (R1–R8) + narração final + voz + sincronização + legenda `.srt` + render 1080p + master + entrega**

Arquivo único e autocontido. Data: 2026-11-18.

**Base:** o preview v2 (18:56, 960×540, 15 fps, sem voz, 17.047 quadros), do zip `yt0045_v2_para_gpt` e dos quadros em três partes. O v2 cumpriu o handoff v2:
- **Lata e hélice (C1):** a projeção oblíqua 2D está igual aos alvos v2. As paredes, o eixo, a base, a tampa e t = 2π caem nas linhas do papel (item 23: ≤ 0,5 px). Há 2 verticais e nenhum piso (item 27). O Three.js saiu do vídeo.
- **Campo nos nós da grade (C2):** nenhuma seta cruza curva ou rótulo nos stills (B2, B4, B5).
- **Tela vazia na primeira frase (C3):** B6-1 e S1 resolvidos.
- **Escrita e contas:** gatilhos com pior atraso +0,27 s e 0 sem frase; FLASH = 0; R5 = R5V = R6 = 0; GM1–GM11 presentes; 68/68 degraus com tempo; palco 2D 0,00 px (81 medidas); SEM-GRADE fora do CTA = 0.

O vídeo está **aprovado para a narração**. Sobraram oito detalhes de tela (R1–R8, §3). Quase todos vêm dos meus alvos v2, não da implementação. Depois deles vem o fechamento completo, sem outra rodada de preview.

No zip `yt0045_handoff_final_completo.zip` vão:
- este documento;
- `yt_0045_narracao_v1_2_final.md` (**narração final**: v1.1 + 3 precisões do refino do GPT, filtrado; gatilhos idênticos; ver §4) e `yt_0045_narracao_v1_1.md` (só referência do tempo do preview);
- `yt_0045_v1_avaliacao_e_handoff_v2.md` (histórico);
- `quadros_alvo_v3/`: os 18 alvos, seis deles refeitos (01, 09, 12, 14, 15, 16), `keys45.js` v3 com o código exato e `00_folha_contato_v3.jpg`;
- `provas_v2_x_v3/`: os cinco pares preview v2 × alvo v3 das cenas corrigidas.

Onde este documento não diverge, continuam valendo o handoff v1.1, o handoff v2 e os alvos v2 (agora v3).

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
- só `videos_longos/yt_0045_integral_linha_campo_vetorial/` (a unidade do preview v2);
- `renders/` e `entregas/`, que são saída.

**O que pode ser copiado** (sem alterar a origem), da unidade mais recente da série que já tenha esses scripts (`yt_0044_exercicios_integral_tripla/`, `yt_0043_centro_massa_momento_inercia/` ou `yt_0041_coordenadas_esfericas/`, nessa ordem de preferência):
- `alinhar_voz.py`, o modo tempo real do `gerar_ancoras.py`, `gerar_srt.py`, `capitulos.py`;
- `render1080.sh`, `render1080_fila.sh`, `montar_final.py`;
- `qa_canto.py`, `qa_fundo.py`, `qa_sync.py`, `qa_voz.py`, `qa_1080.py`, `prancha_ancoras.py`, `stills_final.py`.

**Modo de execução:**
- Não encerre a vez entre etapas.
- Depois de lançar um render ou a voz, espere na mesma vez e siga para a auditoria. Use comando em primeiro plano com timeout de até 10 min por lote, ou um laço `until` sobre o arquivo de saída.
- Mensagem de progresso não é entrega.
- Logs longos vão para arquivo; leia só o fim e os erros.

**Só há duas paradas permitidas:**
1. A variável `ELEVENLABS_API_KEY` não existe na sessão. Peça ao Kaio. **Nunca** grave a chave em arquivo, log ou relatório.
2. O WAV passa de **21:30**. Reporte a duração e pare (estimativa: 3.424 palavras a 3 palavras/s ≈ 19:11; o preview v2 tem 18:56).

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

Pare só depois do relatório. Guarde este arquivo na unidade como `handoff_final.md` e copie `quadros_alvo_v3/` para `referencia/`.

---

## 1. Estado de partida

- **Unidade:** a do preview v2, com o código das seções, o kit, a lata oblíqua do C1, o `campoG` do C2 e os scripts de QA do v2 (itens 1–27, `gatilhos`, `conta_inteira`, `flash_por_quadro`, `palco2d`, `lata_campo`).
- **Não reabrir:**
  - a matemática e os números (Anexo A);
  - as contas, degrau por degrau (68/68);
  - a ordem de montagem PH → PA → PB1 → PB2 → PB4 → PB5 → PB6 → PB7 → PS;
  - a projeção oblíqua do C1 (H1: CX 480, CY 780, U 300, k 0,20; B7: CX 300, CY 780, U 240, k 0,25), as 2 verticais, sem piso, trás tracejado em cor sólida;
  - o campo nos nós da grade (C2) e os glyph maps GM1–GM11;
  - as cores:

    | Grandeza | Cor |
    |---|---|
    | campo F | verde-menta `#2EE6A0` |
    | γ′ e deslocamentos Δγ | violeta `#B48CFF` |
    | curva / hélice | `#FFB36B` (trás `#8E6C55`) |
    | t (parâmetro) | `#E08A3C` |
    | x | âmbar `#FFC24D` |
    | y | magenta `#EA63FF` |
    | z | azul `#5AA2FF` |
    | ao longo / área / redemoinho | lima `#C6F26B` |
    | alerta / peso | `#FF5D5D` |
    | texto de apoio, lata | GEO `#B8C4DA` (trás `#5E6788`) |
    | moldura do resultado | menta `#8CFFD2` |

  - nenhum efeito novo: sem pulso, brilho, palco vivo, tracer, partícula ou sombra.
- **Notação:** F = (P, Q, R); γ(t) = (cos t, sen t, c t) na lata de raio 1; R maiúsculo só como raio nos exemplos do plano e como terceira componente no cartão do B6-1. Nenhum θ.
- **A cena segue a voz.** Os tempos do v2 não valem mais. Todos os lotes são re-renderizados com a linha do tempo da voz.

---

## 2. Avaliação do v2 (resumo)

Conferi em resolução cheia os 17 stills 1080p contra os alvos v2 e li os relatórios de QA. O preview reproduz os alvos e os números do QA batem com os quadros. A lata agora mora na grade e lê bem. O que sobra são detalhes de leitura do desenho que só apareceram com o vídeo pronto:
- o eixo z passa **por cima** dos traços da frente da hélice e da tampa, como se estivesse na frente da lata;
- no B7 a seta do meio nasce em cima do eixo, a da direita encosta no ponto `t = 0`, e as pontas furam a elipse da base;
- a 2ª volta apagada do B7 parece uma segunda tampa logo abaixo da de cima;
- no H1 a ponta da seta F fura a base, e a tela fica 1,4 s só com o canto enquanto a voz já fala;
- no B4-3 a seta de F em t = R deita em cima do círculo, e a ponta de sentido do segmento fica embaixo da seta de F;
- no B6-1 a placa `A MESMA DA SUBSTITUIÇÃO` encosta no último `dt`.

Os itens 24 e 25 (seta × curva, seta × rótulo) foram dados como "garantidos por construção", sem medida em pixel. No §7 eles passam a ser **medidos**.

---

## 3. Correções (lista fechada)

Convenção: posições em px de 1080p (Manim: x_m = (x_px − 960)/120, y_m = (540 − y_px)/120). O código exato de cada uma está em `quadros_alvo_v3/keys45.js`; o trecho que mudou em relação ao v2 vem citado em cada item. Projeção: `pr(x, y, z) = (CX + U·x, CY − U·(z + k·y))`, c = 1/(4π).

### R1 · H1: a conta e a seta F sobem para a 2ª volta

**O que está errado:** a conta está em t = 1,62π (590, 714) e a seta F, com s = 0,42, termina em (708, 831): a ponta fura a elipse da base (distância 0,3 px).

**O que fazer:**
- a conta (bolinha branca, raio 11 px) passa para **t = 3,62π** → **(590, 564)**, na volta de cima, na frente;
- a seta F sai da conta com **s = 0,30** (comprimento no mundo; F = (−sen t, cos t, −1)) → ponta em **(674, 648)**;
- o rótulo `F⃗` vai para **(704, 624)** (ponta + (30, −24)); antes ficava sob a ponta e encostava na volta de baixo.

No `keys45.js`: `const tc=3.62*PI; L.F(tc,C4,.30,5,20)` e `tex('\\Fv',q[0]+30,q[1]-24,36,'c')`.

**Aceite:** still do H1 no estado `F`; distância da seta à base ≥ 70 px, à volta de baixo ≥ 20 px; rótulo × hélice = 0.

### R2 · H1 e B7: o eixo z passa por trás do que está na frente

**O que está errado:** o eixo z (azul, 3 px) é desenhado por cima de tudo. Ele está **dentro** da lata, então deve sumir onde um traço **contínuo da frente** o cruza.

**O que fazer:** desenhe o eixo como segmentos, com um **corte de 8 px para cada lado** de cada cruzamento com traço contínuo da frente. Os traços tracejados de trás continuam por baixo do eixo, sem corte. Os cruzamentos ficam em x = CX, nas alturas:

| Cena | Cruzamento | y do centro do corte (px) |
|---|---|---|
| H1 | hélice da frente, t = 1,5π | 727,5 |
| H1 | hélice da frente, t = 3,5π | 577,5 |
| H1 | tampa, metade da frente | 540 |
| B7-1, B7-2, B7-3 | hélice da frente, t = 1,5π | 750 |
| B7-1, B7-2, B7-3 | tampa, metade da frente | 600 |
| só B7-3, depois do R4 | 2ª volta da frente, t = 3,5π | 630 |

Fórmula: y = CY − U·(z_c − k), com z_c = c·t na hélice ou z_c = 1 na tampa (é `pr(0, −1, z_c)`). No `keys45.js`: `eixo(z1, cortes)`.

**Atenção à animação:** durante o crescimento da hélice (H1 e B7-1), o corte aparece **quando o traço da frente passa pelo eixo**, nunca antes.

**Aceite:** recorte de 120 × 400 px em volta do eixo nos stills do H1, B7-1 e B7-3; nenhum pixel azul do eixo a menos de 6 px de um traço contínuo da frente.

### R3 · B7: duas setas do campo, curtas, longe do eixo e da base

**O que está errado:** três setas em t = 1,2π, 1,5π e 1,78π com s = 0,28.
- A de 1,5π nasce **em cima do eixo** (x = 300).
- A de 1,78π termina a 19 px do ponto `t = 0`, e a ponta encosta na base.
- A de 1,2π fura a base (1,8 px).

**O que fazer:** só **duas** setas, em **t = 1,38π e 1,62π**, com **s = 0,18**, traço 4 px e cabeça 15 px. No `keys45.js`: `for(const t of [1.38*PI,1.62*PI])L.F(t,C4,.18,4,15)`.

| t | início (px) | ponta (px) | à base | ao eixo | aos pontos t = 0 / 2π |
|---|---|---|---|---|---|
| 1,38π | (212, 753) | (252, 800) | 35 px | 48 px | 289 px |
| 1,62π | (388, 739) | (429, 778) | 19 px | 94 px | 112 px |

Vale para o B7-1, o B7-2 e o B7-3.

**Aceite:** a tabela acima medida no still (±2 px); nenhuma seta a menos de 14 px de base, eixo, pontos ou rótulos.

### R4 · B7: a 2ª volta só entra no B7-3, em laranja apagado

**O que está errado:** no B7-1 e no B7-2 a 2ª volta (t de 2π a 4π) aparece em GEO apagado. A metade da frente dela fica logo abaixo da tampa e **parece uma segunda tampa**. Ela não ajuda: a conta desses dois quadros é de **uma** volta.

**O que fazer:**
- B7-1 e B7-2: **sem** a 2ª volta;
- B7-3: a 2ª volta entra no gatilho **"Na nossa lata"** (linha 3, `NOSSA LATA: 2 VOLTAS SOBEM 1`), desenhada de t = 2π a 4π em 1,5 s;
  - frente: `#A8794F`, 3 px, contínua;
  - trás: `#8E6C55`, 3 px, tracejado 12/9 (o mesmo da 1ª volta).
- O corte do eixo em y = 630 (R2) nasce junto com ela.

No `keys45.js`: `if(K==='b73')L.hel(C4,2*PI,4*PI,'#A8794F',3,HELB)`.

**Aceite:** stills do B7-1 e do B7-2 sem traço entre y = 540 e y = 660 além da tampa e das paredes; still do B7-3 depois do gatilho com a 2ª volta.

### R5 · H1: a lata entra na primeira palavra

**O que está errado:** `palco_parado_v2.txt` registra `PH H1 0.40–1.80 s palco vazio 1.40 s`. A voz já diz "Ficou uma pergunta no ar", e a lata só entra no gatilho "uma hélice enrolada na parede da lata".

**O que fazer:** as linhas da lata (elipse de baixo, elipse de cima, as duas paredes) e o eixo z (com o rótulo `z`) entram **na primeira palavra do H1**, em `Create` de 1,2 s. A hélice e o resto do estado `helice` continuam no gatilho de sempre. Nada mais muda de tempo.

**Aceite:** `palco vazio > 0,5 s` = 0 no PH.

### R6 · B4-3: sem seta em cima do círculo; ponta de sentido depois das setas

**O que está errado:**
- As setas verticais de F no segmento ficam em t = 0,5; 1; 1,5 e 2 (unidades do palco; R = 2). A de t = 2 = R nasce **no círculo** e deita sobre ele (x = 720).
- A ponta de sentido do segmento, de [1,2; 0] a [1,55; 0], fica embaixo da seta de t = 1,5.

**O que fazer:**
- setas de F só em **t = 0,5; 1; 1,5** → x = 540, 600 e 660 px;
- a ponta de sentido vai de **[1,55; 0] a [1,82; 0]** → x de 666 a 698 px, entre a última seta e o círculo.

No `keys45.js`: `seta([1.55,0],[1.82,0],HEL,7,24); for(const t of [.5,1,1.5])`.

**Aceite:** still do B4-3; seta × círculo = 0; a ponta de sentido a ≥ 6 px da seta de t = 1,5 e do círculo.

### R7 · B6-1: a placa respira

**O que está errado:** `A MESMA DA SUBSTITUIÇÃO` começa a ≈ 14 px do último `dt`.

**O que fazer:** a placa começa **48 px** depois da borda direita do `dt` (no alvo v3: `\hspace{0.8em}` no fim do MathTex). Mesma linha de base, mesmo tamanho. A borda direita da placa fica ≤ 1.200 px, longe do painel da projeção (x ≥ 1.420).

**Aceite:** still do B6-1; folga `dt` → placa ≥ 44 px.

### R8 · H1: o primeiro quadro sem a linha 2 do canto

**O que está errado:** `palco_parado_v2.txt` registra `canto sem a linha 2: 1` em PH H1, no quadro 0.

**O que fazer:** o canto (`CÁLCULO III · INTEGRAIS DE LINHA` + `A HÉLICE NA PAREDE DA LATA`) entra **inteiro** no primeiro quadro do vídeo, sem animação de escrita.

**Aceite:** `qa_canto.py` = 0 em todos os quadros; still do quadro 0.

**Depois do R1–R8:** prancha `correcoes_final.jpg` com os antes/depois (modelo: `provas_v2_x_v3/`).

---

## 4. Narração final

Arquivo: **`yt_0045_narracao_v1_2_final.md`** (no zip). É a fonte do `gerar_ancoras.py` e da voz; a v1.1 fica só como referência do tempo do preview v2.
- Tem **3.424 palavras ≈ 19:11** (+34 sobre a v1.1), em 19 âncoras e 122 gatilhos.
- O texto é a v1.1 palavra por palavra, com três frases trocadas (listadas no topo do arquivo): H2 (a parte ao longo pode ajudar ou atrapalhar), B6-2 ("mede área" só em curva fechada simples, anti-horária) e B7-3 (c = 1 é outra hélice, mais alta que a lata).
- **Nenhum gatilho mudou**: os 122 batem com a fala (conferido por script, tokens contíguos, na ordem). O R4 usa o gatilho que já existe ("Na nossa lata"), e o R5 usa a primeira palavra da âncora.
- Se o Kaio colar outra narração refinada junto deste handoff, ela substitui a v1.2: refaça a busca de gatilhos e reporte os que mudaram.

**Regras já aplicadas (não alterar):**
- A tela mostra a conta inteira; a voz conversa como professor (marcação [ensina]/[mecânica] por linha da coluna), sem ler número por número e sem silêncio. Não encurtar.
- Letras latinas com a caixa da tela (x, y, z, t, u, c, n, i, a, b, A, B, F, P, Q, R, W, "d x", "d y", "d z", "d t"); gregas pelo nome ("gama", "gama linha", "delta", "ômega", "pi"). Nenhum θ.
- Nenhum vídeo citado como existente. "No próximo vídeo" só no cartão do S2. Green e campos conservativos só como "mais adiante no curso".

**Passos:**
1. Gere `narracao_tags.md` (com a seção `## Texto corrido (para gravação)`) e `narracao_limpa.md` a partir da v1.2, como no yt_0044.
   - Tags de áudio `[ ]` em inglês, uma por trecho, as que já estão na v1.2; sem `[slowly]`.
   - Sem tags na legenda.
2. `grep -c 'θ\|téta\|teta'` = 0 na fala, nos gatilhos e nos arquivos de tags.
3. Rode a busca de gatilhos: `[gatilho-sem-frase]` = 0 antes da voz.

---

## 5. Voz (ElevenLabs v4)

Referência: `docs/roteiro_voz_elevenlabs_v4.md`.

1. Confirme `ELEVENLABS_API_KEY` (primeira parada, §0).
   - Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4` (os mesmos do yt_0044).
   - Formato `mp3_44100_192`, decodificado para WAV mono 16 bits 44,1 kHz.
2. **Amostras de pronúncia primeiro.** São curtas, para o Kaio ouvir em paralelo. Gere 6 mp3 em `audio/teste_pronuncia/` com estas frases e siga sem esperar:
   - "F de gama de t, escalar gama linha de t, d t."
   - "Integral sobre gama de P d x mais Q d y mais R d z."
   - "Gama de t igual a cosseno de t, seno de t, c t."
   - "Dois pi menos meio, mais ou menos cinco vírgula setenta e oito."
   - "c é um sobre quatro pi, e o trabalho zera quando c vale um."
   - "n R ao quadrado seno de dois pi sobre n: a soma de Riemann do redemoinho."
3. Rode `narracao_tags.md` com `--seco`, depois sem ele:
   ```
   uv run --no-sync python videos/gerar_voz_elevenlabs.py videos_longos/yt_0045_integral_linha_campo_vetorial/narracao_tags.md videos_longos/yt_0045_integral_linha_campo_vetorial/audio/narracao_v1.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)" --seco
   ```
4. **Uma tomada completa.** Siga com ela. O Kaio ouve em paralelo; se reprovar, ele regera e a §6 refaz tudo sozinha. A tomada aprovada vira `audio/narracao_final.wav`.
5. `qa/voz.txt` (`qa_voz.py`):
   - duração;
   - picos e clipping;
   - silêncio > 1,5 s dentro de um parágrafo;
   - tag lida em voz alta;
   - fronteiras sem corte audível;
   - pronúncia de:
     - letras: "gama", "gama linha", "delta gama i", "ômega", "P", "Q", "R", "W", "c", "d x", "d y", "d z", "d t";
     - números: "dois pi R ao quadrado", "quatro pi", "um sobre quatro pi", "dois pi menos meio", "cinco vírgula setenta e oito", "seis vírgula vinte e oito", "t mais dois t ao cubo";
     - nomes: "Riemann", "Green", "Parallax Lab".
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
2. `ancoras.json` **gerado por script**: `gerar_ancoras.py` no modo tempo real, lendo `referencia/yt_0045_narracao_v1_2_final.md`. Cada âncora começa na primeira palavra do seu trecho. Os `self.gat("…")` são buscados no alinhamento.
3. **Animações da lata:**
   - a hélice cresce no H1 (duas voltas) e no B7-1 (uma volta) com velocidade constante em t, dentro da frase do gatilho;
   - os cortes do eixo (R2) acompanham o traço;
   - a 2ª volta do B7-3 (R4) vai no gatilho "Na nossa lata".
4. Rode os lotes 540p e confira:
   - `[gatilho-sem-frase]` = 0;
   - os `[estouro]`, cada um com o motivo. Estouro > 1 s numa âncora: deixe a âncora seguinte começar mais tarde (a voz continua) ou divida a espera entre os degraus. **Nunca** acelere a voz nem a caneta.
5. `qa/sync.txt` (`qa_sync.py`): o atraso de cada âncora, de cada degrau das contas (os 68 da tabela CONTAS) e de cada gatilho (meta ≤ 0,2 s).
6. **Legenda `.srt`** (`gerar_srt.py`):
   - até 2 linhas × 42 caracteres, de 2 a 5 s por bloco;
   - tempo do WAV = tempo do vídeo;
   - trocas:
     - "gama linha" → γ′, "gama" → γ, "delta gama i" → Δγᵢ, "delta t i" → Δtᵢ, "ômega" → Ω, "pi" → π;
     - "d x", "d y", "d z", "d t" → dx, dy, dz, dt;
     - "F" → F; letras sozinhas ficam como na tela (P, Q, R, W, c, t, n);
     - "Cálculo três" → "Cálculo III".

---

## 7. Conferência 540p com voz (antes do 1080p)

Render de **todos os lotes** em 540p/15 fps com os tempos da voz, e preview com voz. Feche o que falhar antes do 1080p.

**Portões:**
- `FLASH POR QUADRO` = 0;
- sem pulso nem palco vivo (efeito não pedido) e sem tracer;
- **GRADE** de tela inteira em todo quadro, menos o CTA;
- **item 23** (lata na grade ≤ 1 px) e **item 27** (2 verticais, sem piso, dentro de x ∈ [60, 900] no H1 e [60, 740] no B7);
- **R2 medido:** nenhum pixel do eixo a menos de 6 px de traço contínuo da frente;
- **itens 24 e 25 medidos em pixel**, não "por construção": distância mínima de cada seta do campo à curva do palco (≥ 14 px, B5 ≥ 12 px) e a qualquer rótulo (0 cruzamentos). Isso inclui as setas da lata (R1, R3) contra a base, o eixo e os pontos `t = 0`, `t = 2π`. Tabela por âncora com o par mais próximo;
- R5 = 0 a cada 0,2 s, também durante os voos; R5V = 0;
- R6 (margens) = 0; zona do logo (x > 1600, y < 130) sem texto;
- COLUNAS ≤ 7 linhas, folga do rodapé ≥ 40 px;
- `\text` com palavra no MathTex = 0;
- canto: inteiro desde o quadro 0 (R8) e trocado no primeiro play de cada bloco;
- tamanhos: corpo ≥ 26 px, algarismo ≥ 30 px, fórmula principal 44–58;
- palco vazio ≤ 0,5 s, varredura a cada 0,2 s (R5 incluído); tela só com papel e título = 0 fora do A1 e do CTA;
- emendas: diferença média de fundo ≤ 1,0 em todas;
- `[gatilho-sem-frase]` = 0;
- tabela CONTAS com cada degrau (68), o tempo e a frase que o dispara;
- `qa_canto.py` e `qa_fundo.py`;
- cartão `NO PRÓXIMO VÍDEO · MUDANÇA DE PARÂMETRO E CAMINHOS COM QUINA` do S2 ≥ 8 s, sem sobreposição com o CTA;
- SYNC e VOZ.

**Pranchas:**
- `correcoes_final.jpg`: R1–R8 com antes/depois;
- uma prancha com **um quadro de cada âncora no instante da primeira palavra** (19 quadros);
- lado a lado com os 18 alvos v3.

---

## 8. Render final 1080p

1. **Sem Three.js nesta unidade.** A lata é 2D no Manim (C1). Não renderize cenas 3D, não use `threejs/` e não use `ThreeDScene`.
2. **Manim em 1080p30** pelo fluxo normal, com `template/config_horizontal.py`.
   - Não configure CRF: o `template/qualidade.py` já usa **14** em renders ≥ 1080p.
   - Não recodifique. Sem teto de tempo de render.
3. **Emenda** com `montar_final.py` (remux, sem reencodar), na ordem PH → PA → PB1 → PB2 → PB4 → PB5 → PB6 → PB7 → PS.
4. **Master:**
   ```
   uv run python videos/montar_master.py <sem_audio_1080p30.mp4> audio/narracao_final.wav renders/yt_0045_master_final_1080p30.mp4
   ```
   Confira:
   - 1920×1080, 30 fps;
   - duração do master = WAV (+ a cauda do CTA, se a montagem a mantiver);
   - `crf=14.0`, com o comando do AGENTS.md.
5. Se o disco apertar, apague só PNGs e renders 540p **desta** unidade já auditados.

---

## 9. QA final e entrega

**QA completo no vídeo final (`qa_1080.py`):**
- os portões do §7 sobre o 1080p (amostragem por lote; a lata do H1 e do B7 em todos os estados);
- A/V contínuo;
- `crf=14.0`;
- `.srt` conferido em 6 pontos:
  - início;
  - `W = 6` (B1);
  - `W = 2πR²` (B4-1);
  - `1 − 1 = 0` (B5-1);
  - `W = 2π − 1/2 ≈ 5,78` (B7-3);
  - fim.
- `renders/capitulos_final.txt` com os tempos da voz:

| Âncora | Título |
|---|---|
| H1 | `A HÉLICE NA PAREDE DA LATA` |
| H2 | `SÓ A PARTE AO LONGO DO CAMINHO TRABALHA` |
| A1 | `BEM-VINDOS` |
| B1 | `FORÇA CONSTANTE, CAMINHO RETO` |
| B2-1 | `CAMINHO CURVO, FORÇA QUE MUDA` |
| B2-2 | `APARECE UMA SOMA DE RIEMANN` |
| B3 | `A DEFINIÇÃO` |
| B4-1 | `O REDEMOINHO NO CÍRCULO` |
| B4-2 | `CONFERINDO PELA SOMA, NA MÃO` |
| B4-3 | `NO RAIO: A FORÇA DE LADO` |
| B5-1 | `O VENTO QUE SOPRA PARA FORA` |
| B5-2 | `POR QUE DEU ZERO` |
| B6-1 | `OUTRA NOTAÇÃO` |
| B6-2 | `A ELIPSE E O DOBRO DA ÁREA` |
| B7-1 | `A HÉLICE DA LATA: MONTANDO` |
| B7-2 | `A HÉLICE DA LATA: A CONTA` |
| B7-3 | `LENDO A RESPOSTA` |
| S1 | `RESUMO` |
| S2 | `MAIS RÁPIDO, AO CONTRÁRIO, COM QUINA` |

**Entrega:** `uv run python videos/entregar.py yt_0045` (cópia).
- O destino tem de ser o `entregas/` do checkout principal.
- A pasta leva:
  - `master`;
  - `legenda` (`.srt`);
  - `audio/`;
  - `texto/`: ficha, `narracao_tags.md`, `narracao_limpa.md`, este handoff e os capítulos;
  - `manifesto`.
- O número `0045` vai no fim de cada nome. Não há capa.
- Série, EP e assunto vêm da `ficha.md`: `CÁLCULO III · EP. 20`, `# Integral de linha de um campo vetorial`. Se o Kaio mudar o número antes da entrega, ele avisa; sem aviso, use o da ficha.
- **Na ficha:** a duração real; `3d_threejs: nenhuma (lata e hélice em projeção oblíqua 2D)`.

Não rode `entregar.py` se um portão do §7 estiver aberto. Pare e reporte.

---

## 10. Relatório de entrega (obrigatório, e depois pare)

1. Arquivos alterados e criados.
2. R1–R8, cada um com o caminho do still que prova, e a prancha `correcoes_final.jpg`.
3. Todos os portões do §7 com números reais: a tabela das setas (itens 24/25, medidos), a tabela CONTAS, a sincronização das 19 âncoras e o QA de voz.
4. Caminhos: WAV, amostras de pronúncia, preview 540p com voz, master 1080p, `.srt`, capítulos e a pasta em `entregas/`.
5. Duração final e taxa real da voz, comparadas com 3 palavras/s.
6. Pendências reais.

Depois do relatório: **pare**. Não faça publicação, capa, commit, merge nem push.

---

## Anexo A · Números congelados

- **B1 · força constante:** F = (2, 1), de A = (1, 1) a B = (4, 1): deslocamento (3, 0), W = 2·3 + 1·0 = 6 (o "1 de lado" não trabalha).
- **B2 · definição:** Δγᵢ = γ(tᵢ) − γ(tᵢ₋₁) ≈ γ′(tᵢ)Δtᵢ; W ≈ Σ F(γ(tᵢ))·γ′(tᵢ)Δtᵢ = soma de Riemann de g(t) = F(γ(t))·γ′(t) em [a, b]; γ de classe C¹; ∫_γ F·dγ = ∫ₐᵇ F(γ(t))·γ′(t) dt.
- **B4 · redemoinho** F = (−y, x) no círculo de raio R, 0 ≤ t ≤ 2π:
  - F(γ(t)) = γ′(t) = (−R sen t, R cos t); produto = R²; W = 2πR² = 2 × área do disco;
  - soma na mão: n R² sen(2π/n): n = 4 → 4R²; n = 8 → ≈ 5,66R²; n = 16 → ≈ 6,12R²; → 2πR²;
  - no raio γ(t) = (t, 0), 0 ≤ t ≤ R: F = (0, t), γ′ = (1, 0), produto 0, W = 0.
- **B5 · vento para fora** F = (x, y) em γ(t) = (t, t²), −1 ≤ t ≤ 1: produto t + 2t³; primitiva t²/2 + t⁴/2; W = (1/2 + 1/2) − (1/2 + 1/2) = 0; −1 na ida, +1 na volta; t²/2 + t⁴/2 = ½(x² + y²).
- **B6 · outra notação:** ∫_γ F·dγ = ∫_γ P dx + Q dy (+ R dz no espaço); dx = x′(t)dt, dy = y′(t)dt; redemoinho = ∫ −y dx + x dy; elipse x = 2 cos t, y = sen t: −y dx + x dy = 2(sen²t + cos²t)dt = 2 dt, W = 4π = 2 × área (π·2·1).
- **B7 · hélice** γ(t) = (cos t, sen t, c t), 0 ≤ t ≤ 2π, F = (−y, x, −1):
  - −y dx = sen²t dt; x dy = cos²t dt; −dz = −c dt;
  - W = ∫₀^{2π}(1 − c)dt = 2π − 2πc;
  - 2π = 2 × área da tampa (π·1²); 2πc = subida numa volta (peso × subida, com sinal −);
  - lata do canal: 2 voltas sobem 1 ⇒ 2πc = 1/2 ⇒ c = 1/(4π); W = 2π − 1/2 ≈ 5,78 > 0;
  - W = 0 ⟺ c = 1 (sobe 2π ≈ 6,28 por volta).
- **Gancho S2:** γ₁(t) = (R cos t, R sen t), 0 ≤ t ≤ 2π; γ₂(u) = (R cos 2u, R sen 2u), 0 ≤ u ≤ π (duas vezes mais rápido); ao contrário; caminho com quina. Cartão "NO PRÓXIMO VÍDEO · MUDANÇA DE PARÂMETRO E CAMINHOS COM QUINA".
