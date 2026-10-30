# yt_0016 — avaliação do preview v5 com voz e HANDOFF v6 (acabamento com voz)

Base: zip `v5_para_gpt 2.zip` (preview 960×540/15 fps, 21:57,9; voz de 21:55,6; 64 âncoras; `alinhamento_palavras.json`, `asr_v4.json`).
Método: folhas de contato com um quadro a cada 2 s e a fala daqueles 2 s embaixo (o vídeo inteiro), recortes a 5 fps nos pontos
duvidosos, pausas medidas no alinhamento palavra a palavra e trechos de palco parado medidos pela diferença entre quadros.

---

## Parte 1 — Avaliação do v5

### 1.0 Veredito
O salto é grande: V1–V18 resolvidas, revisão de física toda na tela, números entrando quando são ditos e pronúncia limpa pelo ASR.
Sobram quatro famílias de problema, nesta ordem de importância:
1. **A voz não respira.** Nenhuma pausa passa de 0,54 s em 22 minutos, nem nas viradas de capítulo. O ritmo médio é de 3,12 palavras/s
   (meta 2,7–3,0), e dez âncoras passam de 3,35. Isso não exige voz nova: basta inserir silêncio (§2 do handoff).
2. **Eventos que a fala descreve e a tela não mostra.** Os blocos do T9-3 não disparam, a bola do E6 não é jogada, a bala do E7 não
   aparece e o rifle do E8 não recua (lista 1.2).
3. **Coisas adiantadas.** No T10-1 as barras já estão cheias antes de a fala chegar nelas; a normal do E7 entra 10 s antes da
   pergunta "quem segurou ele?"; o cavalo do gelo para antes do "até parar" (lista 1.3).
4. **Acabamento.** São 8 sobreposições novas, 2 morphs embaralhados e a Lua que vira disco. Além disso, T9, T10 e E8 ocupam só a metade
   de cima do quadro, e a borda do chão 3D corta o quadro no meio (listas 1.4–1.6).

A QA de "trechos parados" do v5 deu zero porque conta qualquer pixel que muda. Medindo palco quase parado (menos de 0,4% dos pixels
mudando entre quadros de 0,2 s), há 58 trechos ≥ 3 s, somando 387 s. A maioria é aceitável, porque a conta está sendo montada. Os que
importam são os da lista 1.2, onde a fala descreve uma ação e o palco fica congelado.

### 1.1 A voz
- **Pausas:** a mediana entre frases é de 0,24 s. As viradas de capítulo têm de 0,25 a 0,5 s (A6→T7 0,28; T9-7→T10 0,34; T10-4→E6 0,48).
  O resultado de cada conta emenda direto na frase seguinte.
- **Ritmo:** 4.109 palavras em 1.315 s = 3,12 palavras/s. As âncoras mais rápidas são H3 (3,57), T8-8 (3,52), T9-7 (3,47), E9-5 (3,43),
  T8-5 (3,41), A5 (3,41), T7-6 (3,40), E9-3, E6-3 e T7-2 (3,36–3,39).
- **ASR × texto:** só há diferenças de normalização ("pra", "imã", números em algarismo, "paralax"). Nenhuma palavra trocada e nenhuma
  tag lida.
- **Falta ouvir:** naturalidade, tags de emoção e se "Parallax Lab" soa como "Paralax". A transcrição não mostra isso.

### 1.2 Fala descreve, tela não mostra (inserir)
| Tempo v5 | Âncora | Fala | Tela hoje | Fazer |
|---|---|---|---|---|
| 9:28–9:44 | T9-3 | "A mola dispara os dois… o leve sai para a esquerda… o pesado para a direita" | Os blocos ficam colados na mola o tempo todo; só aparecem setas. Palco parado 23 s | No "dispara", o disparo em câmera lenta (~0,6 s): os blocos se separam e as setas de velocidade presas a eles. Depois, congela com o chip `LOGO APÓS O DISPARO` |
| 11:19–11:46 | T10-1 | "A mola dispara…", "os dois momentos têm o mesmo tamanho", "Repara nas barras… Mas as energias… não" | Disparo e barras cheias logo em 11:20; depois, 24 s parado | Disparo no "A mola dispara" (11:20,5). Barras de MOMENTO crescem em "os dois momentos têm o mesmo tamanho" (11:32), com as setas opostas. Barras de ENERGIA crescem em "Mas as energias… não" (11:44,5). Realce nas barras em "Repara nas barras" |
| 12:44–13:00 | E6-1 | "Um amigo joga em você uma bola… a dez metros por segundo. O sistema é você mais a bola" | Manequim parado 16 s; a bola só aparece em 13:00,4 e é agarrada em 0,4 s. A fronteira `VOCÊ + A BOLA` é desenhada sem a bola | A bola entra pela esquerda no "joga em você uma bola" (12:49) e para no ar com o rótulo `10,0 m/s` no "dez metros por segundo". A fronteira se desenha em volta dos dois no "O sistema é você mais a bola" (12:54). A bola retoma no "você agarra a bola" (13:02), em câmera lenta de ~1,5 s |
| 13:20–13:22 | E6-3 | "E se a bola bate no seu peito e volta a oito metros por segundo?" | O rebate dura 1,6 s com o chip `CÂMERA LENTA`, e a bola some no meio do quadro | Rebate de ~2,5 s; a bola sai pela borda esquerda com a seta `8,0 m/s` |
| 14:23–14:32 | E7-2 | "Primeiro, o tiro na horizontal… o momento da bala para a frente é igual ao momento do caçador para trás" | Só um clarão de um quadro; nem bala nem p⃗ | Bala (traço de aço) saindo pela borda no "o tiro na horizontal". No "o momento da bala para a frente é igual ao momento do caçador para trás", duas setas magenta do mesmo tamanho: p⃗_bala na ponta do cano e p⃗_caçador nas costas, opostas. Esta é a ideia central do exercício |
| 16:12–16:20 | E8-1 | "A bala sai a seiscentos e um… E o rifle recua a um vírgula oitenta e cinco" | Fumaça e setas, mas o rifle não se mexe | O rifle desliza para trás no apoio frouxo no "o rifle recua"; a bala sai em traço pela borda no "A bala sai" |
| 16:24–16:31 | E8-2 | "Os seiscentos e um são em relação ao cano, e o cano está andando para trás" | A coluna da CONTA fica vazia por ~6 s | Realce no rótulo `EM RELAÇÃO AO CANO` e depois em `EM RELAÇÃO AO CHÃO`. A pergunta `OS GASES CARREGAM MOMENTO?` (hoje só 2 s, em 16:22) fica no canto da CONTA até "São os gases!" (16:56) |
| 4:44–4:48 | T7-9 | "Na bola em parábola, o peso só puxa na vertical" | A bola parada no fim da parábola; o voo só aparece no replay (4:50) | O primeiro voo vai no "Na bola em parábola", com a seta do peso. O replay fica para "Uma direção pode conservar e a outra não" (4:52), com pₓ fixa e p_y mudando |
| 14:49–14:53 | E7-3 | "o caçador deveria ganhar momento para baixo. Só que ele não afunda no gelo" | Nada | Seta magenta tracejada para baixo no caçador, com "?", no "deveria ganhar momento para baixo"; ela é riscada no "não afunda no gelo" |
| 6:43–6:49 | T8-5 | "E aqui está a resposta da pergunta do começo. Sim, a corda puxa o cavalo para trás" | Coluna da direita vazia por ~5 s | A pergunta do hook volta pequena no canto da CONTA e se apaga quando entra `2.800 N > 2.608 N` |
| 1:44–1:50 | A6 | "deixa de ser um fato sobre dois discos e vira uma ferramenta para qualquer sistema" | Palco parado ~7 s (só o "?" pulsa) | O ícone dos dois discos do A4 aparece e vira o ícone das três esferas no "vira uma ferramenta" |
| 0:28–0:37 | A2 | (apresentação) | Miniatura parada por 8,4 s | Push-in lento na miniatura e realce da pergunta no "essa pergunta" (0:34) |
| 18:48–18:50 | E9-5 | "Os corpúsculos acelerariam ao entrar na água" | O espaçamento dos corpúsculos é igual no ar e na água | Na água, o espaçamento entre os corpúsculos aumenta (mais rápidos = mais espaçados), com o rótulo `PREVISÃO DE NEWTON` |
| 21:48–21:58 | EN2 | "os pedaços voam para todo lado… mas uma coisa continua exatamente na mesma parábola" | Os pedaços somem em ~0,5 s; o ponto fica parado 8 s no fim da parábola | Cada pedaço segue a própria parábola e sai do quadro. O ponto do CM percorre a parábola até o chão no "na mesma parábola" (21:52), em degradê ciano→magenta como no yt_0017 |
| 20:56–20:58 | S1 | "A corda puxa, sim, o cavalo para trás" | Só o rótulo INTERNA na corda | Setas T⃗ e −T⃗ em cinza por 2 s |

### 1.3 Adiantado ou atrasado (sincronia fina)
| Tempo v5 | Âncora | O que está fora | Corrigir para |
|---|---|---|---|
| 7:26–7:36 | T8-6 | O cavalo para (v = 0) em 7:26–7:28, e a fala só diz "o conjunto freia… até parar" em 7:30–7:36. Depois fica 10 s congelado | A frenagem termina no "até parar" (≈ 7:35,5); o mostrador chega a 0,00 nesse instante |
| 14:46 | E7-3 | N⃗ (EXTERNA, IMPULSIVA) entra 10 s antes de "Foi o gelo!" e entrega a resposta de "Quem segurou ele?" | N⃗ entra em "Foi o gelo!" (14:55) e cresce em "a normal do gelo cresce de repente" (14:57) |
| 3:51–3:56 | T7-6 | As células se apagam em 3:51, antes de "As células se apagam duas a duas" (≈ 3:55); a diagonal nunca acende | Realce da diagonal em "A diagonal fica vazia" (3:52); apagar os pares, dois a dois, em "se apagam duas a duas" |
| 3:59–4:13 | T7-7 | O "?" do canto some em ~4:00; a fala "A interrogação do canto virou esta equação" é em 4:12,5 | O "?" fica até 4:12 e voa para dentro da caixa de dP⃗/dt = F⃗ᵉˣᵗ nessa frase |
| 14:34 | E7-2 | `= 0,0559 m/s` entra junto com "A velocidade de recuo é…", ~3 s antes de "uns cinco vírgula seis centímetros" | A fração entra primeiro e o `= 0,0559 m/s` no número falado. Regra geral: **o resultado depois do sinal de igual entra quando é dito, não no começo da frase** |
| 20:32 | C-2 | `LASER DE 1 W (ABSORVIDO): 3,3 nN` entra 4–5 s antes de "três vírgula três nanonewtons" (20:36,5) | Rótulo no "E um laser"; o `3,3 nN` no número falado |
| 11:34 | T10-1 | `(MÓDULOS)` aparece sozinho antes de m₁v₁ | Entra junto com a igualdade |
| 11:08–11:12 | T9-7 | A DICA some enquanto a fala ainda diz "quem eu deixei de fora do sistema?" | Fica até o fim da frase (+0,5 s) |
| 15:58 | E7-5 | A DICA `ISOLADO NA HORIZONTAL…` entra durante "A força do recuo depende também de quanto tempo dura o impulso" | Entra depois dessa frase, ou antes do "Mas cuidado" |
| 11:20–11:22 | T10-1 | Selo `ANTES DOS BATENTES` antes de "Antes de qualquer um bater num batente" (11:24) | No "Antes de qualquer um bater" |

### 1.4 Sobreposições novas
| Tempo v5 | Âncora | Problema |
|---|---|---|
| N1 · 8:22–8:26 | T8-8 | A câmera acompanha o andar e leva o rótulo `ATRITO DO CHÃO` para baixo da caixa da DICA (encostam e se cobrem) |
| N2 · 15:26,4–15:28,4 | E7-5 | `CÂMERA LENTA` e `REPLAY` grudados ("CÂMERA LENTAREPLAY") por 2 s na troca de chips |
| N3 · 18:38–19:12 | E9-5/6 | `SE APROXIMA DA NORMAL` sobre o último corpúsculo do raio na água |
| N4 · 18:00–19:12 | E9-3/4 | O raio de corpúsculos passa por cima da origem das setas v_t/v_n (ANTES), e `J⃗ NORMAL`, θ₂ e v_n se amontoam junto do ponto de entrada |
| N5 · 20:06–20:52 | C-2/C-3 | Os traços dos fótons atravessam a vela por cima. Numa vela refletora, eles devem parar na vela e voltar |
| N6 · 15:04–15:24 | E7-4 | Decomposição de p⃗_bala espremida na ponta do cano: `p⃗_bala`, ×, p_y e pₓ em ~60 px, e p_y encosta na linha da fronteira |
| N7 · 14:02 | E6-4 | `SÓ SE CONSERVA SE A COLISÃO FOR ELÁSTICA` a < 0,25 da caixa da DICA |
| N8 · 8:36–9:16 | T9-1/2 | `m g⃗` encosta na cota vertical de 10 m |

### 1.5 Morphs e glitches
- **0:41,6–42,4 (A3):** a área sob a curva vira uma mancha roxa que voa até `dp⃗/dt`. Trocar por um realce da área e FadeIn do termo.
- **12:11–12:13 (T10-2→T10-3):** a conta inteira derrete em glifos embaralhados (igual ao V3 antigo). Primeiro a conta sai com FadeOut;
  depois só o resultado `K₁/K₂ = m₂/m₁` sobe (TransformFromCopy da caixa).
- **7:44 e 8:10 (T8-7):** a Lua crescente vira um disco cheio no realce do "Lua". Manter a forma de crescente e fazer o realce com brilho.

### 1.6 Composição e cosméticos
- **Metade de baixo vazia:** T9-3 a T9-7, T10 e E8 ficam nos ~45% de cima do quadro. Escalar o palco em ×1,4 a ×1,6 e centralizar na
  altura (os gráficos de P(t) continuam embaixo do palco).
- **Diagramas do E9 pequenos:** espelho e refração em ×1,3, com a decomposição (ANTES/DEPOIS) deslocada para fora do caminho do raio.
- **Borda do chão 3D:** em T7, T8, E6, E7 e no resumo, o chão 3D termina numa aresta vertical no meio do quadro (x ≈ 0,55 W). Agora é
  a rodada final: fazer um degradê de alfa nos ~15% da direita da camada 3D. A placa de gelo com cara de tapete continua opcional.
- `v_Terra = …` (T9-2) está com contraste baixo. Subir para o tom dos outros números.

### 1.7 As duas decisões que o Claude Code deixou
- **Hook com 23,8 s:** aceito. A fala do Anexo A é essa, e o hook está bom.
- **C-2 com `(ABSORVIDO)` e `≈ PESO DE 3 A 4 GRÃOS DE ARROZ`:** aceito. Os dois acompanham a fala.

---

## Parte 2 — HANDOFF v6 (acabamento com voz)

### 0. Rodada
- Unidade `videos_longos/yt_0016_sistemas_momento/` (preview v5). Rode `git status --short`. Copie a unidade para `_v5/` (código, ficha,
  âncoras e `audio/narracao_v4.wav`; sem renders). Salve este handoff como `handoff_v6.md`.
- **Objetivo:** (1) dar respiro à voz sem gerar voz nova (§1); (2) refazer as âncoras e a sincronia pela voz nova (§2); (3) corrigir a
  tela (§3); (4) entregar um preview v6 com voz, 960×540 / 15 fps, completo.
- Sem SRT, master, legendado, `entregar.py`, commit ou push. A narração (texto) não muda. Não alterar `template/`, `docs/`, `assets/`,
  `experimentos/threejs/` nem o yt_0015.

### 1. Voz com respiro (sem ElevenLabs)
Inserir silêncio em `audio/narracao_v4.wav` e salvar como `audio/narracao_v4_pausas.wav` (não sobrescrever o original):
- Cortar sempre no meio do intervalo entre duas palavras, pelo `alinhamento_palavras.json`. O silêncio é digital, com fade de 10 ms
  nas duas emendas (sem clique). Conferir que nenhum corte cai dentro de uma palavra.
- **Virada de capítulo:** +1,0 s. São 11: A6→T7, T7-9→T8, T8-8→T9, T9-7→T10, T10-4→E6, E6-4→E7, E7-5→E8, E8-4→E9, E9-7→C-1, C-3→S1,
  S2→EN1. Também H3→A1: +0,6 s.
- **Demais viradas de âncora:** +0,35 s.
- **Depois de cada resultado:** +0,5 s depois da última palavra destes trechos: T8-3 "…metros por segundo ao quadrado"; T8-4 "Fecha
  certinho"; T8-6 "…até parar"; T9-2 "…menos vinte e quatro metros por segundo"; T9-6 "ele volta a zero"; T10-3 "…ficam com o mais leve";
  E6-2 "Bem devagarinho"; E6-3 "quase o dobro"; E7-2 "…dá para ver"; E7-4 "…três centímetros por segundo"; E7-5 "…massa da bala";
  E8-3 "a soma dá zero"; E9-6 "era mais lenta!"; C-2 "…três vírgula três nanonewtons".
- **Pergunta retórica no meio de uma âncora** (frase terminada em "?" seguida de outra frase): +0,4 s.
- Meta: ~+45 a 55 s no total, ritmo final entre 2,95 e 3,0 palavras/s. Reporte a duração e a lista das inserções (tempo → duração).
- Recalcular os tempos das palavras somando o deslocamento acumulado. Depois, rodar o alinhamento de novo só para conferir (desvio
  ≤ 0,05 s).

### 2. Âncoras e sincronia
- `gerar_ancoras.py` com a voz nova. Cada âncora abre ~0,15 s antes da primeira palavra. Todos os `diz()` passam a ler os tempos
  novos (o kit já segue o tempo absoluto da voz).
- **Regra de resultado:** o termo depois do sinal de igual entra no instante em que o número é dito, e não quando a frase começa (ver
  E7-2 e C-2 na tabela 1.3). Conferir isso em todas as contas.
- O silêncio novo é tempo de leitura: a conta parada durante a pausa é aceitável, mas o palco não congela (o "palco vivo" continua).

### 3. Correções de tela
Fazer tudo da Parte 1: tabela 1.2 (inserções; os disparos e tiros contam como o evento do bloco e continuam com no máximo um replay),
tabela 1.3 (sincronia), tabela 1.4 (sobreposições N1–N8, na ordem da tabela), lista 1.5 (morphs e a Lua) e lista 1.6 (composição,
diagramas do E9 e a borda do chão 3D).

Detalhes que valem para todas:
- **E7-2:** as duas setas p⃗_bala e p⃗_caçador são do mesmo comprimento na tela (câmera lateral ou rótulo `MESMO TAMANHO`).
- **E7-4:** monte a decomposição numa cópia ampliada de p⃗_bala na coluna da CONTA (TransformFromCopy da seta) e deixe na ponta do cano
  só a seta e o ×.
- **T9-3:** o disparo aqui é curto e congela, porque o disparo principal, com o gráfico, continua no T9-5.
- **EN2:** a granada é só um teaser; não precisa de Three.js.
- Regras que continuam valendo: nada escrito sobre corpo 3D; rótulos pela ponta livre da seta, com `buff ≥ 0,15`; folga ≥ 0,25 entre
  textos; viradas de cena em sequência; nenhum texto a menos de 0,3 da borda; Three.js para o 3D.

### 4. QA
- Sobreposição: auditoria completa, conferindo um por um N1–N8 e V1–V18 (sem regressão).
- **Palco congelado (métrica nova):** quadros a 5 fps reduzidos para 240×135 em cinza. Um pixel conta como mudado se mudar > 18 níveis
  entre quadros seguidos; um trecho conta como congelado se < 0,4% dos pixels mudarem. Listar todos os trechos ≥ 6 s. Meta: nenhum
  ≥ 8 s, e cada um de 6 a 8 s justificado no relatório. No v5 havia 58 trechos ≥ 3 s, somando 387 s; os maiores eram T9-3 (23 s),
  T10-1 (23 s), E8-2/3 (30 s) e T9-6/7 (17 s).
- Sincronia: abertura de cada âncora (≤ 0,3 s); cada número da tabela de conferência (tempo falado × tempo em que aparece); cada evento
  da tabela 1.2 (tempo da palavra-gatilho × tempo do evento).
- Áudio: pico ≤ −1 dBFS; sem clique nas emendas novas (o mesmo teste das emendas de bloco do v5); lista das pausas inseridas.
- Alinhamento 3D × Manim ≤ 2 px.

### 5. Parada e relatório
Pare com o preview v6 com voz. O relatório (AGENTS.md) leva: arquivos alterados; cada item das tabelas 1.2–1.6 (feito / não feito e
por quê); a voz (pausas inseridas, duração nova e ritmo); o mapa de âncoras e `capitulos_v6.txt`; os resultados do QA, incluindo a
lista de palco congelado; as pendências.

Zip para avaliação como no v5: preview com voz, `ancoras.json`, `capitulos_v6.txt`, logs, quadros a 5 fps e stills dos itens de 1.2 e
de N1–N8. Sem SRT, master, commit nem push.
