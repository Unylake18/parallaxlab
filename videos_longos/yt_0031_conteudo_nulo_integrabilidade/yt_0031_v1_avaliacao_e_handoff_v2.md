# yt_0031 · CÁLCULO III · EP. 06 · Conteúdo nulo e integrabilidade
# AVALIAÇÃO DO PREVIEW v1 + HANDOFF v2 · preview silencioso (540p, 15 fps)

2026-11-12. Produção → Claude Code. Este documento é **autocontido**. Ele vale junto com:
- o handoff v1, que continua na unidade;
- a pasta `yt_0031_quadros_alvo_v2/` do zip, que traz os 31 alvos (5 deles redesenhados, marcados "v2" na folha de contato `00_folha_contato_v2.jpg`) e o gerador `sb31.html` atualizado.

Onde este documento e o v1 divergirem, **vale este**. A narração v2 (Anexo A do v1) **não muda**.

Fase aberta: **preview visual silencioso v2**. Sem voz, sem SRT, sem 1080p, sem master, sem entrega, sem commit e sem push.

---

## 0. O que entregar

1. A mesma unidade `videos_longos/yt_0031_conteudo_nulo_integrabilidade/`, com as mudanças deste documento. O v1 fica em `renders/v1/`; não apague nada dele.
2. `renders/v2/yt_0031_preview_v2_540p15.mp4` (960×540, 15 fps, sem áudio), com o mesmo tempo da narração v2 (≈ 19:50).
3. `renders/v2/qa/` com tudo o que o §6 pede, incluindo os relatórios novos:
   - `parados_v2.txt`;
   - `glyphmaps_v2.txt`;
   - `origens_v2.txt`;
   - `sobreposicoes_v2.txt` (com o R5 ampliado).
4. A prancha `comparacao_v2.jpg` com os 31 alvos da pasta v2.
5. O relatório de entrega do AGENTS.md.

---

## 1. Avaliação do v1

### O que está certo e não deve mudar
- Duração (19:52), sistema visual (fundo violeta, grade `papel`, layouts, cores) e todos os números da tela, que foram conferidos.
- As cenas 3D, os pousos 3D ↔ 2D e o alinhamento (0 px).
- FLASH POR QUADRO = 0.
- A divisa do B9-2 ficou melhor que a do alvo. Mantenha a sua.
- A separação dos dois pedaços no S2 (≈ 0,17 m) bate com o alvo 31. O "0,03 m" do texto do v1 estava errado; vale o alvo.

### O que precisa mudar: 5 famílias de problemas

| # | Família | Onde aparece |
|---|---|---|
| 1 | **Sobreposições que o R5 não pega.** Texto sobre linha, aresta, ponta de seta ou borda de painel; painéis que se cruzam **durante** a animação; curva vazando da lupa. | B6-2, B7-1, B7-4, B6-3, B1-2, B4-2, B5-1, B6-1 |
| 2 | **Parados longos.** 7,0 s · 6,5 s · 6,3 s · 5,7 s · 5,3 s · 5,2 s e mais uns 20 trechos de 3 a 5 s. | §3, âncora a âncora |
| 3 | **Tela vazia ou canto incompleto no começo do bloco.** B6, B8 e B9 abrem com o palco vazio e sem a linha 2 do canto; H2 fica vazio de 0:53 a 1:00. | §2 G2 |
| 4 | **MF-Tools não usado.** Não há `from MF_Tools import` na unidade. A função própria `mapa_glifos` (`v31.py`, perto da linha 775) faz `FadeIn` dos glifos sem par, e é isso que põe `S(P) − s(P) <` e o `+` na tela sem caneta no B7-2. | §2 G1, §4 |
| 5 | **A figura não acompanha a fala.** São estes casos: <br>• a contagem de caixas fica em 8 enquanto a voz diz 4 e 16; <br>• o orçamento não cai, porque a escala se reajusta; <br>• o ponto não desliza no "qualquer ponto"; <br>• "encolher" virou três cópias; <br>• a régua da lupa colapsa num ponto. | §3 |

---

## 2. Regras globais novas (valem para o vídeo inteiro)

**G1 · MF-Tools de verdade.**
- Use `from MF_Tools import TransformByGlyphMap` (1.4.9) com `MathTex` de string única nos dois lados e mapa explícito. **Aposente `mapa_glifos`.**
- Glifo que **sai** usa `auto_fade` (ou entra no mapa com destino vazio).
- Glifo que **entra** (não existe na linha de cima) **nunca** usa `FadeIn`. Ele fica fora do mapa e é escrito com a caneta (`Write`, traço ~0,7) logo depois do mapa, ou voa da fonte (`TransformFromCopy`) se tiver origem no desenho.
- Se o 1.4.9 aceitar um introdutor por entrada, use a caneta como introdutor. Se não aceitar, use a sequência mapa → caneta.
- `show_indices` só no desenvolvimento.

**G2 · Nenhum bloco abre vazio.**
- A linha 2 do canto (título da cena) está na tela **desde o primeiro quadro** de cada bloco.
- A figura do bloco anterior fica até a nova nascer dela (`ReplacementTransform`), ou a nova figura começa a entrar em ≤ 0,5 s.
- Palco vazio por mais de 0,5 s: zero ocorrências.

**G3 · Parado, medido de verdade.**
- Definição: trecho em que menos de 40 px do quadro de 960×540 mudam (diferença > 8 níveis em qualquer canal) ao longo de 3 s.
- Limite: 3 s.
- De 3 a 5 s só é aceito se a voz estiver **lendo** o que está na tela. Escreva o motivo em `parados_v2.txt`.
- Acima de 5 s: zero.
- Todo evento novo do §3 é ligado a uma palavra da fala, com atraso ≤ 0,2 s.

**G4 · R5 ampliado.**
- O teste cruza a caixa de **todo** texto e `MathTex` contra:
  - outros textos;
  - linhas, arestas e setas (pontas incluídas);
  - bordas de chapa, painel, cartão e lupa;
  - os rótulos do eixo;
  - as arestas do 3D (pelo `pontos.json`).
- Amostra a cada 0,5 s, **inclusive durante as animações** (crescimento, movimento), e não só no gatilho.
- Esperado: zero.

**G5 · Recorte nas janelas.**
- O que está dentro de lupa, painel ou cartão é **calculado** para caber nele: restrinja o parâmetro da curva à janela e corte os retângulos na borda da janela.
- Nada de máscara opaca por cima.

**G6 · Tamanhos.**
- Texto solto: ≥ 24 px no 1080p. Fórmula: ≥ 34 px, para que o índice fique ≥ 22 px.
- `\frac` em vez de `\tfrac` em ε/2, ε/(2α) e ε/(8M).
- Elementos irmãos com o mesmo tamanho (as quatro caixas do B7-3 a 38 px; os três painéis do B7-4).

**G7 · Glifos.**
- Conjunto vazio = `\emptyset` em LaTeX, nunca o caractere em Space Grotesk (ele sai como ø).
- Os zeros em legenda continuam "ZERO" por extenso.

**G8 · Pontos e marcas só os do alvo.** Nenhum ponto laranja, branco ou de debug a mais (B1-1, B1-2, B7-1, S2).

---

## 3. Correções âncora a âncora

Tempos do preview v1. "Alvo NN" é o arquivo da pasta v2; os marcados **(v2)** foram redesenhados.

### H1 · as três perguntas (alvo 01)
- O carimbo `CONTA SOB MEDIDA` entrou 4 s atrasado. Ele entra na palavra "sob medida".
- A lupa ficou parada ~5 s. O ponto laranja muda de metal **duas vezes**, ligado à fala:
  - em "Se o ponto escolhido cai do lado leve", vai para o metal leve e acende `ρ = 1`;
  - em "Se cai do lado pesado", vai para o metal pesado e acende `ρ = 3`.
- Os `ρ` ao lado da lupa vão a 24 px **com placa**, como no alvo.

### H2 · a ideia do vídeo (alvo 02)
- A borda vermelha das células na miniatura dos dois metais sumiu. Ela fica.
- De 0:53 a 1:00 o palco ficou vazio. As três miniaturas ficam na fileira do topo até o fim do H2. `O PROBLEMA NÃO É O SALTO` entra em "pode ter descontinuidades" e `É ONDE ELE ACONTECE` em "onde essas descontinuidades acontecem".

### B1-1 · piso e teto (alvo 04)
- Tire os pontos laranja extras sobre o contorno branco (G8).
- Os rótulos da barrinha estavam com ~20 px. Vão a 24 px.

### B1-2 · as duas somas (alvo 05)
- **5 s parado em "qualquer ponto".** O ponto `X_ij` **desliza** dentro da célula por 3 posições: começa em "qualquer ponto que você escolhe" e dura até "entre o piso e o teto". A marca dele na barrinha anda junto, sempre entre m_ij e M_ij.
- A desigualdade foi escrita inteira. Agora é assim:
  - `s(P)` voa do rótulo do prédio de baixo;
  - `S(P)` voa do rótulo do prédio de cima;
  - `f(X_ij)` voa do ponto;
  - os `≤` e o `ΣΣ … Δx_iΔy_j` vão a caneta, na ordem da frase "Lê-se: …".
- A placa de `f(X_ij)` estava sobre uma aresta do prisma. Ela sai para o lado (R1).

### B1-3 · o volume das tampas (alvo 06)
- Tire o rótulo `TAMPAS` solto que sobrou.
- **O voo está ao contrário.** `M_ij − m_ij` voa **da cota da tampa para a fórmula**, nunca da fórmula para a cota.
- As duas somas viram a diferença por `TransformByGlyphMap` (§4, mapa 1).
- Parados de 4,3 e 3,2 s:
  - `OSCILAÇÃO` entra sob `M_ij − m_ij` na palavra "oscilação";
  - as tampas coral acendem (cor por 1 s) em "o que sobra do prédio de cima são as tampas coral".

### B1-4 · quando as tampas somem (alvo 07)
- Parados de 4,4 e 4,2 s:
  - as duas paredes **se aproximam** em "Quando as paredes se fecham num mesmo número";
  - `f INTEGRÁVEL` entra em "a função é integrável";
  - em "persegue uma coisa só", as tampas acendem.

### B2-1 · onde estão as tampas? (alvos 08 e 09)
- `TAMPA 0` estava na célula errada. Vai na célula que fica **inteira no metal leve**, como no alvo 08.
- **4:43–4:56 (grave):** a coluna do alvo 09 foi escrita tarde e cortada, e o voo do `2` se perdeu.
  - Em "Tampa de altura dois", o `2` voa do muro para `altura de cada tampa = 3 − 1 = 2`. O `3` e o `1` voam dos rótulos ρ = 3 e ρ = 1.
  - A linha `S(P) − s(P) = 2 · (área das células na solda)` entra inteira, a caneta, em "Então a diferença entre as duas somas é o salto, dois, vezes a área" (começo do B2-2), antes de "Refina a grade".
  - Nada da coluna sai da tela nem é cortado.

### B2-2 · o muro vai sumindo (alvo 10)
- Parados de 4,6 e 3,4 s. Cada linha da tabela entra **no número que a voz diz** (4, 8, 16, 32, 64). Na mesma hora:
  - a grade refina;
  - a faixa da régua aperta.
- Tabela e régua estavam com ~20 px. Vão a 24 px.

### B3-1 · a definição (alvo 12)
- Os números que estavam sobre a borda de cima da barra sobem 10 px, com placa.
- O índice de `A_i` estava minúsculo. A definição vai a 40 px (G6).
- Parado de 3,9 s: os sublinhados de leitura do `∪` e do `m(A_i)` ficam ligados às palavras "união" e "área".

### B3-2 · um orçamento de área (alvo 13, v2) · 6:38–6:51
- **O orçamento não caía**, porque a escala se reajustava. Agora a escala é **fixa**: 1 m² = 400 px na tela.
  - O ε = 1 começa no topo.
  - Em "o orçamento cai para um quarto", a marca **desce** para ε = 1/4, e a anterior fica tracejada e apagada.
  - Em "E se cair para cinco centésimos?", ela desce para ε = 0,05.
  - Uma seta menta mostra a queda.
- O gasto (0,46 · 0,12 · 0,03) é a barra cheia na mesma escala. O número dele **voa do topo da barra** para a linha da coluna.
- No fim, `0,03` cabe dentro de `ε = 0,05`, e isso se vê.

### B3-3 · o que tem e o que não tem (alvo 14)
- "Encolhe" saiu como três cópias. Agora é **um** quadradinho em volta do ponto, que **encolhe no lugar** (90 → 56 → 30 px) em "tão pequeno quanto o orçamento pedir". Os tamanhos anteriores ficam como contornos finos tracejados concêntricos.
- O `ε` da barra do disco estava ilegível. Vai a 26 px, com placa, ao lado da barra.

### B4-1 · a parábola (alvo 15) · 8:00–8:05
- 5,3 s parado, e 8 caixas na tela enquanto a voz falava em 4 e 16. A contagem **segue a voz**:
  - "Divide o eixo em pedaços": **4 caixas**. O empilhamento é feito com essas 4.
  - "Com quatro pedaços, dois": 4 caixas e `4 pedaços → 2`.
  - "com oito, um": cada caixa se parte em duas (`ReplacementTransform`), e a coluna se refaz.
  - "com dezesseis, meio": 16 caixas.
- O `4` da cota da coluna voa para `área ≤ 4Δ` (como no v1).

### B4-2 · a solda e o arco (alvo 16)
- A legenda de baixo estava com ~20 px e encostava na borda. Vai a 24 px, a 16 px da borda.
- A metade direita ficou vazia ~20 s. Os **dois painéis nascem juntos** no começo: o arco aparece já desenhado, sem caixas. As caixas do arco entram em "O arco do quarto de disco".
- O arco mostrava sempre 8 caixas. Ele refina **com a voz**: 4 → 8 → 16 → 32 em "Com quatro divisões / com oito / com dezesseis / com trinta e duas". A coluna fica com altura 2 e afina, e a área atualiza junto (1 · 0,5 · 0,25 · 0,125).
- Parado de 5,2 s: em "separa os dois movimentos", as caixas da subida acendem e depois as da descida.

### B4-3 · o resultado geral (alvo 17, v2)
- Eram ~33 s só de texto. Agora há figura:
  - a parábola do B4-1 encolhe para o painel da esquerda com 16 caixas e a coluna empilhada (`ReplacementTransform`), e `área ≤ 4Δ = 0,5` fica embaixo;
  - a fórmula do topo é escrita a caneta em "o gráfico de qualquer função contínua";
  - `CAIXAS = S − s → ZERO` entra em "é exatamente a diferença";
  - as linhas de C¹ entram em "classe cê um";
  - as quatro formas entram **uma por vez** em "segmentos, polígonos, círculos, elipses", cada uma com o seu ✓;
  - a frase de baixo entra em "a primeira pergunta tem resposta".
- A legenda longa do v1 virou `CAIXAS = S − s → ZERO` (R-texto: até 6 palavras).

### B5-1 · interior, exterior e fronteira (alvo 18)
- `EXTERIOR` encostava na borda. Fica a ≥ 16 px.
- A sonda da fronteira **encolhe de verdade** (3 tamanhos, contínuo) em "não importa o quanto a bola encolhe", sempre pegando dentro e fora.
- Os parados: cada sonda entra na sua palavra ("interior", "exterior", "fronteira"). Os dois segmentos dos eixos acendem em "os dois segmentos sobre os eixos".

### B5-2 · a borda é uma solda (alvo 19) · 10:46–10:52
- Parados de 6,5 e 4,9 s:
  - em "Coloca a região dentro de um retângulo maior", a moldura do retângulo **acende** (GEO → branco por 1 s) e a parte de fora ganha `f = 0`;
  - em "salta de um para zero", a borda acende;
  - em "Olha o prédio", as tampas da borda sobem.

### B6-1 · um delta para a chapa inteira · 10:53–10:58
- Tela vazia e sem a linha 2 do canto (G2). A chapa x² + y² com as tampas nasce da cena do B5-2.
- O eixo y atravessava o aramado. Tire os eixos desta cena 3D, ou desenhe-os com teste de profundidade para que passem **atrás** das tampas.

### B6-2 · continuidade uniforme (alvo 20, v2) · 11:41–11:58
- **As barrinhas f(X), f(Y) estavam minúsculas e em cima da ponta da seta do eixo x e do rótulo "x".** Agora:
  - as barras ficam em x = 990 px, com a base em y = 640 px (140 px acima do eixo), e 1 unidade de f = 38 px;
  - a faixa menta tem altura ε = 1 (38 px);
  - os rótulos ficam fora da faixa.
- Os rótulos `X`, `Y`, `δ` no canto de cima ficam com placa, nas posições do alvo, sem se tocar.

### B6-3 · por que fechado e limitado? (alvo 21) · 12:35–12:55
**A régua colapsava num ponto na borda esquerda, e as placas +1/−1 se cruzavam.** A régua da lupa **não encolhe na tela**. Quem muda é o **zoom da lupa**, que vai chegando perto da borda. Em cada zoom, a régua liga um ponto onde o seno vale 1 a um onde vale −1:

| Zoom (na fala) | Janela em x (m) | Ponto onde sen = 1 | Ponto onde sen = −1 | Distância |
|---|---|---|---|---|
| 1 · "Dá para achar dois pontos" | [0,06; 0,16] | 0,1273 | 0,0909 | 0,036 |
| 2 · "tão próximos" | [0,05; 0,085] | 0,0707 | 0,0579 | 0,013 |
| 3 · "quanto você quiser" | [0,035; 0,06] | 0,0490 | 0,0424 | 0,0065 |

(Os pontos são 1/(π/2 + 2πk) e 1/(3π/2 + 2πk), com k = 1, 2, 3.)

- Em cada zoom:
  - o retângulo tracejado na chapa encolhe em direção à borda esquerda;
  - a régua fica com ~60 px na lupa;
  - `+1` fica acima e `−1` abaixo (nunca na mesma altura);
  - na coluna, `distância = …` troca de número e `diferença = 2` fica.
- As faixas do palco não apertavam visivelmente. Desenhe o palco com **supersample**, de pelo menos 8 amostras por coluna de pixel: perto da borda, as listras viram um cinza médio, e onde a = 0,05–0,2 m elas apertam de forma visível.
- Na lupa, as listras também apertam da direita para a esquerda (é a mesma função; com a janela certa, isso aparece).

### B7-1 · separando os pontos problemáticos (alvo 22)
- **13:05–13:12, 7,0 s parado.**
  - Em "existe um número eme maiúsculo", entram `|f| ≤ M` e `f LIMITADA`.
  - Em "chama de D", `D` é escrito a caneta, com placa, e a solda acende.
- **13:29–13:43, a curva vazava da lupa** perto de `2 · ENGORDA`. Aplique o G5: a curva da lupa é recortada na janela. `2 · ENGORDA` fica fora da lupa, na coluna.
- A solda estava em escada pixelada. Desenhe-a como curva paramétrica lisa (≥ 200 amostras), nunca a partir das células.
- Tire os pontos brancos soltos (G8).

### B7-2 · dois grupos de tampas (alvo 23)
- `S(P) − s(P) <` e o `+` entraram por `FadeIn` (G1). A sequência certa está no §4, mapas 2 a 4.
- Parados de até 5,7 s: cada contribuição entra na sua frase:
  - "Contribuição: menos que alfa vezes épsilon dois";
  - "Contribuição: menos que quatro eme épsilon um".
- `ε/2` estava pequeno. Use `\frac` a ≥ 38 px (G6).

### B7-3 · o teorema (alvo 24, v2)
- Eram 47 s só de texto. Agora cada caixa tem uma **miniatura** à direita, que entra com a caixa:
  - Teorema 1: os dois metais com as células da solda;
  - caso D = ∅: o mapa contínuo x² + y²;
  - Teorema 2: o quarto de disco com as células da borda;
  - Observação: o quarto de disco com uma curva de descontinuidade dentro.
- O `∅` saía como ø. Agora é `\emptyset` em LaTeX (G7).
- O `TEOREMA 2` estava menor. As quatro caixas usam 38 px, e o Teorema 1 e o 2 quebram em duas linhas (veja o alvo).
- Cada caixa entra na sua frase:
  - "esse é o teorema";
  - "toda função contínua num retângulo";
  - "numa região limitada com fronteira";
  - "o livro ainda observa".

### B7-4 · as três respostas (alvo 25) · 15:33–15:58
- **Os painéis se cruzavam enquanto cresciam.** A miniatura ficou no canto e o ✓ espremido.
- Os três painéis voltam **já no tamanho e na posição finais** do alvo (x = 80, 690, 1300; 540 × 740) e se acendem um por vez, na ordem da fala.
- Se houver crescimento, cada painel cresce **a partir do próprio centro** e nunca passa da sua caixa final. Teste em todos os quadros (G4).
- O ✓ fica no canto superior direito **dentro** do painel, a (X + 170, 240), com 6 px de traço.

### B8-1 · a função de Dirichlet (alvo 26)
- 7 s de tela vazia e sem a linha 2 do canto (G2). A chapa do painel x² + y² do B7-4 cresce para o palco e vira a célula da Dirichlet.
- `4 CONTRA ZERO` estava espremido. Siga o alvo 26: a frase fica numa linha só, a 26 px, alinhada à direita em (1680, 1030), sem tocar em nada.

### B8-2 · uma fronteira que não some (alvo 27)
- Parado de 4,7 s:
  - em "Qualquer disquinho", a sonda passa por 3 lugares do quadrado;
  - `CONDIÇÃO SUFICIENTE` entra em "condição suficiente".

### B9-1 · o teste em três perguntas (alvo 28, v2)
- Abria vazio (G2). Os três chips nascem **um por pergunta**, na fala, e agora são **numerados** (`1 · LIMITADA?`, `2 · DESCONTINUIDADES: NULO?`, `3 · FRONTEIRA: NULO?`).
- Os ✓ de cada cartão ficam sob os números 1 2 3 (alinhados com os chips).
- Os cartões entram um por exemplo, e cada ✓ entra quando a voz fecha aquela pergunta.

### B9-2 · por que isso importa (alvo 29)
- Abria vazio (G2). Os cartões do B9-1 encolhem e saem enquanto os três novos entram.
- Mantenha a divisa do seu render.

### S1 · síntese (alvo 30)
- O 3D ficava estático e sem evento.
  - Em "a diferença entre elas é o volume das tampas", o muro coral acende.
  - Em "as tampas podem ser altas", ele acende de novo.
  - Câmera parada (sem giro).
- As caixas da coluna entravam na ordem 1, 3, 2. A ordem certa é 1 (`TAMPAS`), 2 (`CONTEÚDO NULO`), 3 (`CONTINUIDADE UNIFORME`), na fala.

### S2 · próximo vídeo e CTA (alvo 31) · 19:34–19:40
- 6,3 s parado:
  - os dois pedaços se separam em "dividir a região em pedaços";
  - a solda acende em "mudar a função num conjunto de conteúdo nulo";
  - o CTA entra na tag `[happy]`.
- Tire o ponto solto (G8).

---

## 4. MF-Tools: os mapas obrigatórios

Todos com `TransformByGlyphMap`, `MathTex` de string única nos dois lados e o mapa escrito à mão.

| # | Bloco | De → para | Detalhe |
|---|---|---|---|
| 1 | B1-3 | `s(P) = ΣΣ m_ij Δx_iΔy_j` e `S(P) = ΣΣ M_ij Δx_iΔy_j` → `S(P) − s(P) = ΣΣ (M_ij − m_ij) Δx_iΔy_j` | Os Σ, os Δ e os dois lados casam. O `−` e os parênteses entram a caneta. O `M_ij − m_ij` final é o que voou da cota. |
| 2 | B7-2 | `< αε₂` e `< 4Mε₁` → `S(P) − s(P) < αε₂ + 4Mε₁` | `αε₂` e `4Mε₁` casam com as duas linhas. `S(P) − s(P) <` e `+` entram a caneta (**não** `FadeIn`). |
| 3 | B7-2 | `αε₂` → `α · ε/(2α)` → `ε/2` | Substituição: o ε₂ sai com `auto_fade` enquanto `ε/(2α)` é escrito. O par `α … α` fica coral, ganha um traço coral fino e some junto. Sobra `ε/2`. |
| 4 | B7-2 | `4Mε₁` → `4M · ε/(8M)` → `ε/2` | Mesmo esquema: `M` com `M` e `4` com `8` (vira 2) cancelam, coral. Depois `ε/2 + ε/2 = ε` → `S(P) − s(P) < ε`. |
| 5 | B4-1 | `área ≤ 4Δ` → `4 · 0,5 = 2` → `… 1` → `… 0,5` | O Δ troca de valor a cada refino. O resultado casa por mapa. |

Valores: ε₁ = ε/(8M) e ε₂ = ε/(2α), os mesmos do v1.

O relatório `glyphmaps_v2.txt` lista cada mapa com tempo, bloco, A → B, pares mapeados e glifos escritos a caneta depois. Esperado: os 5 mapas acima, `mapa_glifos` = 0 e `FadeIn` em glifo de fórmula = 0.

`origens_v2.txt` lista toda linha de fórmula com tempo e origem (caneta, voo ou glyph map) e a fonte. Linhas sem origem: zero.

---

## 5. O que NÃO fazer

- Não mexer no que o v1 acertou (sistema visual, 3D, pousos, números, duração).
- Nada de efeito novo: partícula, brilho, sombra, pulso, câmera girando. "Acender" = trocar a cor por 1–2 s e voltar.
- Nenhum `FadeIn` de fórmula ou de glifo de fórmula.
- Livro, autor ou "EP. N" na tela: não.
- Não mexer em `template/`, `assets/`, `docs/`, `AGENTS.md`, `pyproject.toml`, `uv.lock` nem em outras unidades.
- Sem voz, SRT, master, 1080p de vídeo, entrega, commit ou push.

---

## 6. QA do preview v2 (obrigatório)

1. **Render × alvo** (31, pasta v2), no estado final de cada trecho → `comparacao_v2.jpg` + `.txt` com toda diferença restante e o motivo.
2. **Parados (G3)** → `parados_v2.txt`: todos os trechos > 3 s, com tempo, duração e motivo. Esperado: zero > 5 s, e só "voz lendo a tela" entre 3 e 5 s.
3. **R5 ampliado (G4)** → `sobreposicoes_v2.txt`, a cada 0,5 s, inclusive nas animações. Esperado: zero.
4. **R6 + recorte (G5)**: nada sai de painel, cartão ou lupa (B6-3, B7-1, B7-4 em especial).
5. **Começo de bloco (G2)**: para cada bloco, o tempo do primeiro quadro com a linha 2 do canto e o primeiro quadro com figura. Esperado: 0 s e ≤ 0,5 s.
6. **MF-Tools** → `glyphmaps_v2.txt` e `origens_v2.txt` (§4).
7. **FLASH POR QUADRO = 0** e **alinhamento 3D ≤ 2 px**, como no v1.
8. **Gatilhos**: atraso ≤ 0,2 s para todos os eventos do §3 (`gatilhos_v2.txt`).
9. **Tamanhos (G6)**: nenhum texto < 24 px e nenhum índice < 22 px no 1080p equivalente.
10. **Números**: os do v1 + a tabela do B6-3 (§3) + a contagem de caixas do B4-1/B4-2.

---

## 7. Parada

Entregue o preview v2, a prancha, os relatórios do §6 e o relatório de entrega:
- arquivos alterados;
- verificações;
- caminho do preview;
- limitações;
- os trechos onde a sincronia com a fala apertou.

Pare. Não inicie voz, SRT, 1080p, master nem entrega.
