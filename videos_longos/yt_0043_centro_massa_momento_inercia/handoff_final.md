# yt_0043 · CÁLCULO III · EP. 18 · Centro de massa e momento de inércia na integral tripla · HANDOFF FINAL
**Catorze correções de tela (R1–R14) + narração final + voz + sincronização + legenda `.srt` + render 1080p + master + entrega**

Arquivo único e autocontido. Data: 2026-11-17.

**Base:** o preview v2 (21:48, 960×540, 15 fps, sem voz), dos zips `yt0043_v2_parte1_video_stills` e `yt0043_v2_parte2_qa`. O v2 cumpriu o handoff v2:
- **Alvos v2:** A1–A8 reproduzidos. O ⊕ ficou mais perto da m₂; o disco ρ = 1 + x aparece; a célula está à direita do eixo; a casca é opaca e cresce até a parede; o s_G está em 1,00 · 0,71 · 0,63; a lata pequena está inteira; os cortes do B4-6 estão empilhados.
- **Implementação:** I1–I14 resolvidos.
  - Órfãos = 0. O PB2 em 65,27 s e 139,73 s foi conferido por quadro; os stills do v1 eram artefato do `still.sh`.
  - Plaquinha × aresta = 0. Texto × 3D ≥ 56 px.
  - Colunas ≤ 7 linhas. Painéis vazios = 0. S1 em toda a largura.
- **Fonte e escrita:** `\text` com palavra = 0; R5 = 0, R6 = 0; flash = 0.
- **Sincronização:** 149 gatilhos, maior atraso +0,27 s.
- **Conta inteira:** D1–D9 entraram, cada degrau com o seu tempo.

O vídeo está aprovado para a narração. Faltam quatro detalhes de tela (R1–R4) e dez melhorias da revisão quadro a quadro (R5–R14), todas na §3; depois vem o fechamento completo.

No zip `yt0043_handoff_final_completo.zip` vão:
- este documento;
- `yt_0043_narracao_v1_1.md` (**narração final**: v1 + refino do GPT filtrado; ver §4) e `yt_0043_narracao_v1.md` (só referência do preview v2);
- `yt_0043_v1_avaliacao_e_handoff_v2.md` (histórico);
- `quadros_alvo_v2/` (referência).
- `yt0043_v2_revisao_quadro_a_quadro.jpg` (os quadros de R5–R13 no v2).

Onde este documento não diverge, continuam valendo os handoffs v1.1 e v2 e os alvos v2.

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
- só `videos_longos/yt_0043_centro_massa_momento_inercia/`;
- `renders/` e `entregas/`, que são saída.

**O que pode ser copiado** (sem alterar a origem), da unidade mais recente da série que já tenha esses scripts (`yt_0041_coordenadas_esfericas/`, `yt_0037_coordenadas_polares/` ou `yt_0034_regioes_gerais_troca_ordem/`, nessa ordem de preferência):
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
2. O WAV passa de **24:30**. Reporte a duração e pare (estimativa: 4.122 palavras a 3 palavras/s ≈ 22:54, tabela da v1.1 ≈ 23:04; o preview v2 tem 21:48).

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

- **Unidade:** `videos_longos/yt_0043_centro_massa_momento_inercia/` (checkout principal), com o código do preview v2: as seções, o kit, `threejs/` e os scripts de QA do v2 (`orfaos`, `placas_x_arestas`, `texto_x_3d`, `paineis_vazios`, `colunas`, `conta_inteira`).
- **Não reabrir:**
  - a matemática e os números (Anexo A);
  - as contas do v2, degrau por degrau;
  - a ordem H1 → H2 → A1 → B1-1 … B4-6 → S1 → S2;
  - o sistema 3D da série (G1–G6: papel sob o 3D, piso em z = 0, 3D até x = 975, legenda colorida, coluna em x = 1020; lata pequena das contas na escala 0,60 com a coluna em x = 780; B4-4/B4-5 com a coluna em x = 680);
  - os alvos v2 e as correções I1–I14 e D1–D9 do v2;
  - as cores:

    | Grandeza | Cor |
    |---|---|
    | s (distância ao eixo) | pêssego `#FFC08A` |
    | fator s do jacobiano | lima `#C6F26B` |
    | θ | verde-água `#2EE6A6` |
    | z | azul `#5AA2FF` |
    | x | âmbar `#FFC24D` |
    | y | magenta `#EA63FF` |
    | r | laranja `#FF9440` |
    | φ | violeta `#B48CFF` |
    | ρ (densidade) | ciano `#35D9FF` |
    | u, w, t | `#E08A3C` |
    | ⊕ | anel ciano → magenta |

  - nenhum efeito novo: sem pulso, brilho, palco vivo, tracer, partícula ou sombra (`_sem_vivo = True` se o kit tiver palco vivo).
- **Notação:** ρ = densidade, s = distância ao eixo, r = distância até a origem, R e h fixos, k = densidade constante, s_G = raio de giração, θ lido **téta**.
- **A cena segue a voz.** Os tempos do v2 não valem mais. Todos os lotes, inclusive os quadros do Three.js, são re-renderizados com a linha do tempo da voz.

---

## 2. Avaliação do v2 (resumo)

Os 23 stills foram conferidos lado a lado com os alvos v2 (comparações `comparacao_v2/`), junto com as crops em 1080p e os relatórios. Resultado: legível, sem sobreposição, 3D alinhado à grade, conta inteira.

Ficam aceitos, sem correção:
- **R5V (15 voos cruzando texto parado por ≤ 0,6 s)** em B1-1 (51,8 s), B1-3 (201,8 s), B4-1 (51,4 s) e B4-4 (260,8 s e 263,6 s do lote). É o glifo em trânsito do voo, sem parada em cima do texto.
- **Casca do B3-3 em pêssego cheio**, mais clara que o alvo: lê melhor.
- **Desenho dos cortes do B4-6** um pouco mais largo que o alvo: o ⊕ da lata pesada fica cerca de 15 px acima do tracejado, como pedido.

---

## 3. Correções (lista fechada)

### R1 · B3-4: rótulos s e φ empilhados perto de P (PB3 · 255–272 s do v2)
- **O que se vê (still `13b_B3-4b`, região x 520–620, y 480–560):** a plaquinha **s** fica em cima do início da sombra tracejada, e a plaquinha **φ** fica logo abaixo dela, colada, sobre o arco de φ. As duas formam um bloco só.
- **Fazer:**
  - **φ:** dentro do ângulo, entre o eixo z e o raio r, a cerca de 55 px do vértice O, na bissetriz do arco (fora do traço do arco).
  - **s:** acima do **meio** da sombra tracejada, a 24 px acima dela.
  - As duas plaquinhas ficam a ≥ 24 px uma da outra e não cobrem nem o arco nem o tracejado.
- **Aceite:** `placas_x_arestas` = 0 com o arco e a sombra incluídos como segmentos; distância entre plaquinhas ≥ 24 px no still 13b.

### R2 · B1-2: o rótulo `z = z̄` preso à célula de baixo (PB1 · 135,6 s do v2)
- **O que se vê:** `z = z̄` fica encostado na célula de baixo, como se fosse a altura dela. Ele é o nome do **plano**.
- **Fazer:** levar `z = z̄` para a ponta direita do plano menta, do lado de fora (≥ 24 px da borda), na cor menta `#8CFFD2`. A célula de baixo mantém só o sinal `−`.
- **Aceite:** o rótulo do plano a ≥ 24 px de qualquer célula e da borda do plano; still 05 refeito.

### R3 · B4-2: degraus que ainda pulam (conta inteira)
A tabela CONTAS do v2 mostra dois degraus que faltam, os dois da minha especificação:

```
C9.9   ∫₀¹ z(1 + z²)^{3/2} dz = ½ ∫₁² w^{3/2} dw
C9.9a  = ½ · ⅖ [w^{5/2}]₁²  = ⅕ [w^{5/2}]₁²                 (½ · ⅖ = ⅕)
C9.9b  = ⅕ (2^{5/2} − 1^{5/2}) = ⅕ (4√2 − 1)                 (2^{5/2} = 4√2; G(b) − G(a))
C9.10  ⅓ ∫₀¹ z⁴ dz = ⅓ [z⁵/5]₀¹ = ⅓ (1/5 − 0) = 1/15
C9.11  ⅓ · ⅕(4√2 − 1) − 1/15 = (4√2 − 1)/15 − 1/15
C9.11a = (4√2 − 1 − 1)/15 = (4√2 − 2)/15
C9.12  M_xy = 2π · (4√2 − 2)/15 = 2π · 2(2√2 − 1)/15 = 4π(2√2 − 1)/15 ≈ 1,532
```

- **Fazer:** entram C9.9a, C9.9b, C9.11a e o meio-degrau `2π · 2(2√2 − 1)/15` do C9.12, com caneta. A manipulação de `4√2 − 2 = 2(2√2 − 1)` usa `TransformByGlyphMap` (GM novo). Os degraus vão nos gatilhos atuais.
- **Conferir também:** a tabela CONTAS do v2 lista `C9.14` duas vezes (15:55,77 e 15:57,64). Garanta a ordem C9.13 → C9.13b → C9.14a (48/15) → C9.14 (16/5 ≈ 0,555), cada uma com o seu tempo e sem linha repetida na tela.
- **Aceite:** a tabela CONTAS lista cada degrau acima com o tempo e a frase.

### R4 · B2-2: G(b) − G(a) explícito nas duas integrais em s (PB2 · 7:14 e 7:42 do v2)
```
∫₀¹ (s − s³) ds = [s²/2 − s⁴/4]₀¹ = (1/2 − 1/4) − (0 − 0) = 1/4
∫₀¹ (s/2 − s⁵/2) ds = [s²/4 − s⁶/12]₀¹ = (1/4 − 1/12) − (0 − 0) = 1/6
```
- **Fazer:** inserir o `(… ) − (0 − 0)` nas duas linhas (mesma linha, sem renovar a coluna, se couber no 1860; senão, numa linha de continuação).
- **Aceite:** degrau presente na tabela CONTAS e no still.

### Revisão quadro a quadro (R5–R14)
O vídeo v2 inteiro foi revisto em 262 quadros (um a cada 5 s) e nas transições, com crops em resolução cheia nos pontos suspeitos. Os itens abaixo escaparam ao QA por still. Os tempos são do vídeo v2 inteiro (mm:ss).

### R5 · B1-3b: o x̄ = 1/4 perde a origem (5:28–5:45)
- **O que se vê:** a coluna renova em 5:28 e somem as linhas `M = π` e `M_yz = ∭x dV + ∭x² dV`. Em 5:45, `x̄ = (π/4)/π = 1/4` aparece sem M nem M_yz na tela.
- **Fazer:** na renovação, `M = π` e `M_yz = 0 + ∭x² dV` viram **chips no topo**, voando das linhas originais. A linha final passa a ser `x̄ = M_yz / M = (π/4)/π = 1/4`: o π/4 voa do resultado `∭x² dV = π/4` e o π voa do chip M.
- **Aceite:** no still de 5:45, os chips M e M_yz estão visíveis; a tabela ORIGENS mostra os dois voos.

### R6 · O 2π sem origem (B4-2 em 14:50, B4-3 e B4-5 em 19:38)
- **O que se vê:** no B4-2, a coluna renova com `∫₀¹ z · ⅓[…] dz = …` e, no fim, `M_xy = 2π · (4√2 − 2)/15`. O 2π (a integral em θ) nunca aparece escrito. O resultado em s do B4-1, que a narração manda virar chip no topo, também não está na tela em 14:50. O mesmo vale para `I_z = 2π[…]` no B4-5.
- **Fazer:**
  - **B4-2:** chip no topo `∫₀¹ √(s²+z²) s ds = ⅓[(1+z²)^{3/2} − z³]`, voando da última linha do B4-1. A primeira linha da coluna passa a ser:
    ```
    M_xy = ∫₀^{2π} dθ · ∫₀¹ z · ⅓[(1+z²)^{3/2} − z³] dz = 2π · ∫₀¹ z · ⅓[(1+z²)^{3/2} − z³] dz
    ```
    O ⅓[…] voa do chip.
  - **B4-3:** depois do resultado em s, entra `I_z = ∫₀^{2π} dθ · ∫₀¹ (resultado em s) dz = 2π · ∫₀¹ [⅕(…) − (z²/3)(…)] dz`.
  - **B4-5b:** `I_z = 2π[…]` não é escrito de novo à caneta. O colchete **voa do chip** `INTEGRAL EM z` (TransformFromCopy) e o 2π entra à caneta.
- **Aceite:** 2π sempre com `∫₀^{2π} dθ` escrito antes; tabela ORIGENS com os voos.

### R7 · B4-3: igualdade falsa depois da renovação (16:58–17:15)
- **O que se vê:** depois da renovação, as linhas `= ½∫(u^{3/2} − z²u^{1/2}) du`, `= ½[…]`, … ficam logo abaixo de `I_z = ∫∫∫ …`. Lidas em sequência, dizem que **I_z é igual à integral em s**, o que é falso: falta o ∫dz e o 2π.
- **Fazer:** a cadeia começa com o lado esquerdo próprio, `∫₀¹ s³ √(s²+z²) ds = ½ ∫_{z²}^{1+z²} (u − z²) u^{1/2} du = …` (como estava em 16:55, antes da renovação). A linha do I_z fica acima, separada por 30 px a mais, ou vira chip.
- **Aceite:** nenhuma linha que comece com `=` tem acima uma expressão diferente do seu lado esquerdo verdadeiro (conferência visual por still, listada).

### R8 · B4-3 → B4-4: falta a linha que distribui (17:15–17:25)
- **O que se vê:** o B4-3 termina em `⅕[(1+z²)^{5/2} − z⁵] − (z²/3)[(1+z²)^{3/2} − z³]`, e o B4-4 abre com o chip `−⅕z⁵ + ⅓z⁵ = (2/15)z⁵`. Ninguém mostra de onde vem o `+⅓z⁵`.
- **Fazer:** última linha do B4-3, com `TransformByGlyphMap` (GM novo; o par `− · −` acende e vira `+`):
  ```
  = ⅕(1+z²)^{5/2} − (z²/3)(1+z²)^{3/2} − ⅕z⁵ + ⅓z⁵            (−(z²/3)·(−z³) = +z⁵/3)
  ```
  O chip do B4-4 voa dos dois termos `− ⅕z⁵ + ⅓z⁵`, e a linha SOBRA voa dos dois termos com raiz.
- **Gatilho:** "os dois pedaços sem raiz" (já existe).

### R9 · B4-4: tela vazia e chip vazio na abertura (17:22–17:40)
- **O que se vê:**
  - de 17:22 a 17:24, a tela fica só com o papel e o canto, e a moldura do chip aparece **vazia** antes do conteúdo;
  - de 17:20 a cerca de 17:40, a metade esquerda fica vazia até o gatilho "o triângulo".
- **Fazer:**
  - **Chip:** a moldura nasce no mesmo `play` do conteúdo (ou depois dele). Vale para **todo** chip e painel do vídeo.
  - **Metade esquerda:** a lata 3D do B4-3 (`lataGiro`) fica na metade esquerda até "o triângulo"; aí sai por corte limpo e entra o painel com o triângulo já desenhado (mesmo `play`).
  - Conferir a mesma troca em B4-4 → B4-5 (18:25): o painel novo não pode aparecer vazio.
- **Aceite:** varredura de PAINÉIS VAZIOS **a cada 0,2 s** (não só nos stills) = 0; nenhum trecho com metade da tela só de papel > 3 s fora do A1 e do CTA.

### R10 · B3-3: a casca só aparece no fim (10:05–11:00)
- **O que se vê:** durante toda a conta (10:05–10:55), o cilindro está em traço, sem a casca e sem a placa s. A casca só entra em 11:00, já crescendo.
- **Fazer:** a casca opaca pêssego com a placa s entra em **s = 0,55** no gatilho "o s ao quadrado da distância encontra o s do fator" (como no alvo v2, `12_B3-3_cilindro.jpg`). O crescimento até a parede continua em "Se toda a massa estivesse na parede".
- **Aceite:** still em 10:20 com a casca e a placa s.

### R11 · B2-2: a plaquinha 1/2 cobre a sonda (7:55–8:10)
- **O que se vê:** a plaquinha `1/2` fica em cima da linha branca da sonda (entra/sai).
- **Fazer:** levar `1/2` para a ponta **esquerda** do tracejado z = 1/2, fora da taça (≥ 24 px da parede). A sonda entra na lista de segmentos do QA PLAQUINHA × ARESTA.

### R12 · Tela vazia entre B3-4 e B3-5 (12:42, cerca de 1 s)
- **O que se vê:** a bola sai e, por cerca de 1 s, só fica o papel antes dos cartões do B3-5.
- **Fazer:** os cartões do B3-5 começam a entrar enquanto a bola sai (sobreposição de 0,3 s), sem quadro só de papel.
- **Aceite:** palco vazio ≤ 0,5 s em todas as trocas de bloco.

### R13 · S1: 18 s com só a linha do topo (20:37–20:55)
- **O que se vê:** a síntese abre com as fórmulas do topo e a tela abaixo vazia até "a taça".
- **Fazer:** as duas fórmulas-resumo (`CENTRO DE MASSA: x̄ = M_yz/M, …` e `MOMENTO DE INÉRCIA: I_z = ∭s²ρ dV`) entram **grandes e centradas** (52 px, em y ≈ 420 e 560), uma por linha. Em "a taça", sobem para o topo no tamanho atual (Transform simples, sem efeito) e os cartões entram como hoje.
- **Aceite:** nenhum quadro do S1 com mais de metade da tela só de papel.

### R14 · Varreduras do QA que precisam ser por quadro
Os itens R9, R12 e R13 passaram porque PAINÉIS VAZIOS e PALCO VAZIO foram medidos só nos stills. Na §7, as duas varreduras rodam **a cada 0,2 s no vídeo inteiro**, e o relatório lista os intervalos.

Nenhuma outra correção. **Não mexer** em A1–A8, I1–I14 e D1–D9 do v2.

---

## 4. Narração final

Arquivo: **`yt_0043_narracao_v1_1.md`** (no zip). É a fonte do `gerar_ancoras.py` e da voz; a v1 fica só como referência do tempo do preview v2. Tem **4.122 palavras ≈ 23:04** (+230 palavras ≈ +1:16 sobre a v1). O texto é a v1 palavra por palavra, com 9 trechos alterados, listados no topo do arquivo (H1, B1-1, B1-2, B3-1, B3-4, B3-5, B4-3, B4-5). Nenhuma tela muda: a cena segue a voz e os degraus que já existem ficam mais tempo na tela (nunca acelere caneta nem tire degrau). Os 150 gatilhos batem com a fala; **um gatilho mudou**: no B4-3, `"um s a mais"` passou a `"dois s a mais"` (linha 2, o s² acende em pêssego). Atualize o `self.gat(...)` correspondente. Os gatilhos das correções R9 (`"o triângulo"`) e R10 (`"o s ao quadrado da distância encontra o s do fator"`) não mudaram. Se o Kaio colar outra narração refinada junto deste handoff, ela substitui a v1.1 do mesmo jeito: refaça a busca de gatilhos e reporte os que mudaram.

**Regras já aplicadas na v1.1 (não alterar):**
- A tela mostra a conta inteira; a voz conversa como professor (marcação [ensina]/[mecânica] por linha da coluna), sem ler número por número e sem silêncio. Não encurtar.
- Letras latinas com a caixa da tela (s, x, y, z, r, R, h, k, u, w, t, M, I); "x barra", "y barra", "z barra"; gregas pelo nome ("rô", "fi", "pi", "ômega", "delta"); θ sempre **téta**.
- A tabela `## Leitura dos símbolos` do arquivo vale para a voz e para a legenda.
- Nenhum vídeo citado como existente: as cilíndricas e as esféricas aparecem só como conteúdo.

**Passos:**
1. Gere `narracao_tags.md` (com a seção `## Texto corrido (para gravação)`) e `narracao_limpa.md` a partir da v1.1, como no yt_0041. Tags de áudio `[ ]` em inglês, uma por trecho, base `[thoughtful]`/`[curious]`, `[excited]` só na descoberta, sem `[slowly]`; sem tags na legenda.
2. `grep -c '\bteta\b'` = 0 na fala, nos gatilhos e nos arquivos de tags.
3. Rode a busca de gatilhos: `[gatilho-sem-frase]` = 0 antes da voz.

---

## 5. Voz (ElevenLabs v4)

Referência: `docs/roteiro_voz_elevenlabs_v4.md`.

1. Confirme `ELEVENLABS_API_KEY` (primeira parada, §0).
   - Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`.
   - Formato `mp3_44100_192`, decodificado para WAV mono 16 bits 44,1 kHz.
2. **Amostras de pronúncia primeiro** (curtas, para o Kaio ouvir em paralelo). Gere 6 mp3 em `audio/teste_pronuncia/` com estas frases e siga sem esperar:
   - "O x barra e o z barra são as coordenadas do centro de massa."
   - "Com w igual a um mais z ao quadrado, o d w é dois z d z."
   - "A velocidade é ômega vezes s."
   - "s ao quadrado vezes s dá s ao cubo d s."
   - "Com téta indo de zero a dois pi, e rô igual a um mais x."
   - "Um mais z ao quadrado, elevado a cinco meios, é secante à quinta de t."
3. Rode `narracao_tags.md` com `--seco`, depois sem ele:
   ```
   uv run --no-sync python videos/gerar_voz_elevenlabs.py videos_longos/yt_0043_centro_massa_momento_inercia/narracao_tags.md videos_longos/yt_0043_centro_massa_momento_inercia/audio/narracao_v1.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)" --seco
   ```
4. **Uma tomada completa.** Siga com ela. O Kaio ouve em paralelo; se reprovar, ele regera e a §6 refaz tudo sozinha. A tomada aprovada vira `audio/narracao_final.wav`.
5. `qa/voz.txt` (`qa_voz.py`):
   - duração;
   - picos e clipping;
   - silêncio > 1,5 s dentro de um parágrafo;
   - tag lida em voz alta;
   - fronteiras sem corte audível;
   - pronúncia de:
     - letras: "x barra", "y barra", "z barra", "s", "r", "k", "u", "w", "t", "d m", "d V", "téta" (nunca "teta"), "fi", "rô", "pi", "ômega";
     - funções: "secante à sétima", "secante à quinta", "logaritmo de um mais raiz de dois";
     - números: "dois terços", "um quarto", "dois quintos", "zero vírgula cinco cinco cinco", "um vírgula cinco três nove";
     - unidades e nomes: "quilograma vezes metro ao quadrado", "Parallax Lab".
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
2. `ancoras.json` **gerado por script**: `gerar_ancoras.py` no modo tempo real. Cada âncora começa na primeira palavra do seu trecho. Os `self.gat("…")` são buscados no alinhamento.
3. **3D:** a linha do tempo do Three.js sai do mesmo `ancoras.json`.
   - Re-renderize todas as cenas com câmera em movimento, pouso ou animação: o giro da lata no H1, a casca que cresce no B3-3, a seta de giro do B3-1 e do S2, o disco ρ = 1 + x do B1-3b, e as demais que dependem do tempo.
   - Rode o QA 3D da unidade: alinhamento ≤ 2 px, 3D dentro de x 60..975 nas cenas de metade esquerda, pousos sem pisca, órfãos = 0 em cada troca de 3D.
4. Rode os lotes 540p e confira:
   - `[gatilho-sem-frase]` = 0;
   - os `[estouro]`, cada um com o motivo. Estouro > 1 s numa âncora: deixe a âncora seguinte começar mais tarde (a voz continua) ou divida a espera entre os degraus. **Nunca** acelere a voz nem a caneta.
5. `qa/sync.txt` (`qa_sync.py`): o atraso de cada âncora, de cada degrau das contas (C1–C11, D1–D9, R3–R8) e de cada gatilho (meta ≤ 0,2 s).
6. **Legenda `.srt`** (`gerar_srt.py`):
   - até 2 linhas × 42 caracteres, de 2 a 5 s por bloco;
   - tempo do WAV = tempo do vídeo;
   - trocas:
     - "x barra" → x̄, "y barra" → ȳ, "z barra" → z̄; letras sozinhas ficam como na tela (s, r, R, h, k, u, w, t, M, I);
     - "téta" → θ, "fi" → φ, "rô" → ρ, "pi" → π, "ômega" → ω;
     - "d s", "d z", "d téta", "d w", "d m", "d V" → ds, dz, dθ, dw, dm, dV;
     - "Cálculo três" → "Cálculo III".

---

## 7. Conferência 540p com voz (antes do 1080p)

Render de **todos os lotes** em 540p/15 fps com os tempos da voz, e preview com voz. Feche o que falhar antes do 1080p.

**Portões:**
- `FLASH POR QUADRO` = 0;
- sem pulso nem palco vivo (efeito não pedido) e sem tracer;
- **GRADE** de tela inteira em todo quadro 2D e papel sob o 3D;
- **PAINÉIS VAZIOS** = 0, varredura a cada 0,2 s no vídeo inteiro (R14);
- **ÓRFÃOS** = 0, com varredura a cada 0,2 s e em todas as trocas de 3D;
- **PLAQUINHA × ARESTA** = 0 (inclui o arco de φ e a sombra do B3-4, do R1);
- **TEXTO × 3D** ≥ 24 px;
- R5 = 0 a cada 0,2 s, também durante os voos; R5V listado com o motivo;
- R6 (margens) = 0; zona do logo (x > 1600, y < 130) sem texto;
- COLUNAS ≤ 7 linhas, folga do rodapé ≥ 40 px;
- `\text` com palavra no MathTex = 0;
- 3D: nada fora de x 60..975 nas cenas de metade esquerda;
- canto: troca no primeiro play de cada bloco;
- tamanhos: corpo ≥ 26 px, algarismo ≥ 30 px, fórmula principal 44–58;
- alinhamento 3D ≤ 2 px; pousos sem pisca;
- palco vazio ≤ 0,5 s, varredura a cada 0,2 s (R12, R14); metade da tela só de papel ≤ 3 s fora do A1 e do CTA (R9, R13);
- `[gatilho-sem-frase]` = 0;
- tabela CONTAS com cada degrau, o tempo e a frase que o dispara;
- geometria: s_G 1,00 · 0,71 · 0,63 (± 0,01); ⊕–m₂ < ⊕–m₃; ⊕ da lata pesada ≥ 12 px acima de z = 1/2;
- `qa_canto.py` e `qa_fundo.py`;
- cartão do S2 ≥ 8 s, sem sobreposição com o CTA;
- SYNC e VOZ.

**Pranchas:**
- `correcoes_final.jpg`: R1–R14, cada um com antes/depois (os degraus de R3, R4, R6 e R8 em close);
- uma prancha com **um quadro de cada âncora no instante da primeira palavra** (21 quadros);
- lado a lado com os 23 alvos v2;
- pranchas 3D por lote.

---

## 8. Render final 1080p

1. **Three.js em 1080p** (todas as cenas), com a mesma câmera e a linha do tempo da voz, e QA 3D de novo sobre o 1080p.
2. **Manim em 1080p30** pelo fluxo normal, com `template/config_horizontal.py`.
   - Não configure CRF: o `template/qualidade.py` já usa **14** em renders ≥ 1080p.
   - Não recodifique. Sem teto de tempo de render.
3. **Emenda** com `montar_final.py` (remux, sem reencodar), na ordem PH → PA → PB1 → PB2 → PB3 → PB4 → PS.
4. **Master:**
   ```
   uv run python videos/montar_master.py <sem_audio_1080p30.mp4> audio/narracao_final.wav renders/yt_0043_master_final_1080p30.mp4
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
  - `z̄ = 2/3` da taça (B2-2);
  - `I = ½ MR²` do cilindro (B3-3);
  - `z̄ ≈ 0,555` (B4-2);
  - `I_z ≈ 1,539` (B4-5);
  - fim.
- `renders/capitulos_final.txt` com os tempos da voz:

| Âncora | Título |
|---|---|
| H1 | `A LATA QUE GIRA` |
| A1 | `BEM-VINDOS` |
| B1-1 | `DO SISTEMA DE PONTOS AO CORPO` |
| B1-2 | `O QUE O CENTRO DE MASSA GARANTE` |
| B1-3 | `SIMETRIA` |
| B2-1 | `A TAÇA: MONTAR` |
| B2-2 | `A TAÇA: A CONTA` |
| B3-1 | `MOMENTO DE INÉRCIA` |
| B3-2 | `DISTÂNCIA AO EIXO` |
| B3-3 | `O CILINDRO UNIFORME` |
| B3-4 | `A BOLA UNIFORME` |
| B3-5 | `QUEM GIRA MAIS FÁCIL` |
| B4-1 | `ONDE A LATA PESADA EQUILIBRA` |
| B4-3 | `QUANTO CUSTA GIRAR A LATA` |
| B4-4 | `O TRIÂNGULO` |
| B4-5 | `A SECANTE À SÉTIMA` |
| B4-6 | `O QUE OS DOIS NÚMEROS DIZEM` |
| S1 | `RESUMINDO` |
| S2 | `E SE O EIXO ESTIVER NA PAREDE?` |

**Entrega:** `uv run python videos/entregar.py yt_0043` (cópia).
- O destino tem de ser o `entregas/` do checkout principal.
- A pasta leva:
  - `master`;
  - `legenda` (`.srt`);
  - `audio/`;
  - `texto/`: ficha, `narracao_tags.md`, `narracao_limpa.md`, este handoff e os capítulos;
  - `manifesto`.
- O número `0043` vai no fim de cada nome. Não há capa.
- Série, EP e assunto vêm da `ficha.md`: `CÁLCULO III · EP. 18`, `# Centro de massa e momento de inércia na integral tripla`. Se o Kaio mudar o número antes da entrega, ele avisa; sem aviso, use o da ficha.
- **Na ficha:** a duração real.

Não rode `entregar.py` se um portão do §7 estiver aberto. Pare e reporte.

---

## 10. Relatório de entrega (obrigatório, e depois pare)

1. Arquivos alterados e criados.
2. R1–R14, cada um com o caminho do still que prova, e a prancha `correcoes_final.jpg`.
3. Todos os portões do §7 com números reais, a tabela CONTAS, a sincronização das 21 âncoras e o QA de voz.
4. Caminhos: WAV, amostras de pronúncia, preview 540p com voz, master 1080p, `.srt`, capítulos e a pasta em `entregas/`.
5. Three.js: cenas, resolução, custo por quadro no 1080p, alinhamento medido (px).
6. Duração final e taxa real da voz, comparadas com 3 palavras/s.
7. Pendências reais.

Depois do relatório: **pare**. Não faça publicação, capa, commit, merge nem push.

---

## Anexo A · Números congelados

- **Três bolinhas:** m₁ = 1 em (2,4; 2,0; 0,4), m₂ = 3 em (2,3; 0,4; 1,1), m₃ = 2 em (0,4; 2,4; 1,8); CM = (1,683; 1,333; 1,217).
- **Equilíbrio:** ∭(z − z̄)ρ dV = M_xy − z̄M = 0.
- **Simetria:** ∫₀^{2π} cos θ dθ = 0. Contraexemplo ρ = 1 + x no cilindro R = 1, h = 1: M = π, ∭x² dV = π/4, x̄ = 1/4.
- **Taça** x² + y² ≤ z ≤ 1: V = π/2, ∭z dV = π/3, z̄ = 2/3.
- **Momento de inércia:**
  - K = ½ I ω², I = ∭ s² ρ dV.
  - Cilindro: I = ½ MR². Bola: ∫₀^π sen³φ dφ = 4/3, I = 2/5 MR². Tubo: I = MR².
  - Raio de giração: s_G = R, R/√2 ≈ 0,71 R, √(2/5) R ≈ 0,63 R.
- **Lata pesada** ρ = √(s² + z²), R = h = 1:
  - massa e centro de massa: M = (π/12)(7√2 − 2 + 3 ln(1+√2)) ≈ 2,760; M_xy = 4π(2√2 − 1)/15 ≈ 1,532; z̄ = 16(2√2 − 1)/(5(7√2 − 2 + 3 ln(1+√2))) ≈ 0,555;
  - momento de inércia: I₅ = 7√2/8 + (3/8) ln(1+√2); I₇ = 2√2/3 + (5/6) I₅; a integral em z = (19√2 + 4)/180 + (1/12) ln(1+√2); I_z = (π/90)(19√2 + 4 + 15 ln(1+√2)) ≈ 1,539;
  - comparação: I/M ≈ 0,558 R², s_G ≈ 0,747 R (lata comum: 0,500 e 0,707).
- **Gancho S2:** eixo na parede; pergunta nos comentários: centro de massa de meia bola uniforme. Cartão "NO PRÓXIMO VÍDEO · EXERCÍCIOS DO MÓDULO · INTEGRAL TRIPLA".
