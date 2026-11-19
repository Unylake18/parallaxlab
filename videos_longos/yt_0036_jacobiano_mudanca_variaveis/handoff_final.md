# yt_0036 · CÁLCULO III · EP. 11 · Jacobiano e mudança de variáveis · HANDOFF FINAL
**Correções de tela (K1–K16) + narração final v2 + voz + sincronização + legenda `.srt` + render 1080p + master + entrega**

Arquivo único e autocontido. Data: 2026-11-15.

**Base:** o preview v2 (21:42,53, 960×540, 15 fps, sem voz), do zip `yt0036_v2_para_gpt`. O v2 cumpriu o handoff v2:
- papel na tela inteira em 100 % das amostras 2D (1.246 de 1.246);
- R5 = 0, flash por quadro = 0, moldura vazia = 0 (limite de 0,5 s), tamanho ≥ 26 px em todas as âncoras;
- CONTA INTEIRA com 199 degraus e nenhum faltando, C18 (a dobra) incluído;
- 100+ passos de glyph map; alinhamento 3D × Manim de 0,04 px;
- a figura do B4-3 com as pernas, a tabela 2×2 do B6-2, as metades do B6-4, o plano u, v do B7 e o cartão do S2 com 8,67 s.

O Kaio perguntou se já dá para fechar com a narração. **Sim.** A matemática e a ordem estão prontas. O que falta é **definição das animações** e três momentos de abertura e fecho:
1. voos e glyph maps com glifo duplicado, negrito no pouso e glifo passando por cima de texto (K3, K4);
2. quatro buracos de ritmo: o zoom do B4-2 que entra no verde e corta (K6), a dobra do B5-3 que some 0,3 s depois do ✓ (K9), o `8/3` do B5-4 que desmancha antes de ficar (K10) e a troca de página do B6-3 (K12);
3. detalhes de quadro: moldura do chip vazia, glifo solto, placa em cima do trapézio, palco pequeno, A1 parado, margem;
4. **hook** reescrito (K1): o quadro 0 já tem a integral e o trapézio, e a fala abre pelo problema;
5. **gancho** reescrito (K15): duas células com o mesmo Δr e Δθ, a de fora maior, que é exatamente como o EP. 12 (coordenadas polares) abre.

No zip `yt0036_handoff_final_completo.zip` vão:
- este documento;
- `yt_0036_narracao_final_v2.md` (narração final; substitui a `yt_0036_narracao_v1_1.md` como fonte do `gerar_ancoras.py`);
- `yt_0036_final_quadros_erros/` (K01a…K15 no instante do problema, 960×540) e `00_folha_erros_final.jpg`;
- `verificacao/` (os dois scripts sympy e as saídas, 41/41 e 26/26);
- `anteriores/` (handoff v1, handoff v2, narração v1.1), só para consulta.

Onde este documento não diverge, continuam valendo o handoff v1 (`yt_0036_handoff_v1.md`) e o handoff v2 (`yt_0036_v1_avaliacao_e_handoff_v2.md`).

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
- só `videos_longos/yt_0036_jacobiano_mudanca_variaveis/`;
- `renders/` e `entregas/`, que são saída;
- pode **copiar** (sem alterar a origem) do `videos_longos/yt_0034_regioes_gerais_troca_ordem/` para a unidade:
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
2. O WAV passa de **24:30**. Reporte a duração e pare (estimativa: 4.071 palavras a 3 palavras/s ≈ 22:36).

Qualquer outra dúvida: escolha a leitura mais provável, diga qual e siga.

**Ordem:**
1. §3 correções no código, com stills de conferência (sem voz, tempos do v2 como rascunho);
2. §4 narração final v2 e busca dos gatilhos;
3. §5 voz;
4. §6 sincronização;
5. §7 conferência 540p com voz;
6. §8 1080p;
7. §9 QA e entrega;
8. §10 relatório.

Pare só depois do relatório. Guarde este arquivo na unidade como `handoff_final.md` e copie `yt_0036_final_quadros_erros/` para `referencia_final/`.

---

## 1. Estado de partida

- **Unidade:** `videos_longos/yt_0036_jacobiano_mudanca_variaveis/` (checkout principal).
- **Código:** as seções do v2, o `j36.py`, a cena Three.js do B4-2 e o `qa_v2` que gerou os relatórios do zip v2. Este handoff foi escrito sem acesso ao código: cada item diz **onde está na tela e qual texto procurar** (`grep` pelo trecho do LaTeX ou da placa). Cite arquivo:linha no relatório.
- **Lotes do v2 (quadro inicial a 15 fps):** PH 0 · PA 1360 · PB1 1667 · PB2 3177 · PB3 3925 · PB4 6074 · PB5 9194 · PB6 13413 · PB7 16548 · PB8 17751 · PS 18368. Tempo no lote = tempo do preview − início do lote ÷ 15.
- **Não reabrir:**
  - a matemática e os números (Anexo A);
  - as escadas C1–C18 degrau por degrau (só o K10 acrescenta o **pouso** do `8/3`, que já é degrau);
  - a ordem H1 → H2 → A1 → B1-1 … B8 → S1 → S2;
  - as cores:

    | Uso | Cor |
    |---|---|
    | x | âmbar #FFC24D |
    | y | magenta #EA63FF |
    | f (integrando) | ciano #35D9FF |
    | u | laranja #FF9440 |
    | v | verde-água #2EE6A6 |
    | \|J\| e fatores | lima #C6F26B |
    | chapa / malha da célula | #663A4C / #FFB3BC |
    | entrada / saída | #7FB2FF / #FF7A8A |
    | ALERTA | #FF5D5D |
    | geometria (GEO) | #B8C4DA |

  - o fundo: violeta `#18143A → #0F0C26` com `papel(ax)` de tela inteira (dois planos: cada um na sua metade, emenda sob a seta de φ); liso só no 3D do B4-2 e no CTA;
  - o 3D do B4-2 (câmera, landing, alinhamento) e o ciclo do chip `|J| = 1/2` (nasce no B3-3, sai no fim do B3-3, renasce no B6-1);
  - o tamanho mínimo das letras (≥ 26 px, ≥ 32 px nas linhas-chave) e a regra da caneta (traço fino, glifo a glifo, nada antes da vez).
- **sympy:** já está na `.venv` (o Kaio autorizou no v1). Rode `verificacao/verifica_yt0036_v2_degraus.py` (26/26) e `verifica_calc3_34t1_sympy.py` (41/41) uma vez no fim.
- **A cena segue a voz.** Os tempos do v2 não valem mais. Todos os lotes, inclusive os quadros do Three.js, são re-renderizados com a linha do tempo da voz.

---

## 2. Avaliação do v2 (resumo)

**Bom e fica:** a grade inclinada do H1 e o trapézio que voa endireitando; a régua do B1; o paralelogramo e o `ad − bc` deduzido pela caixa; o sinal pela orientação; a grade curva com GRANDE/PEQUENA; o 3D do produto vetorial com pouso de 0,04 px; a tabela que encolhe para 1,02; a soma de Riemann; o teorema com as hipóteses e as miniaturas; a dobra com a metade da direita; o trapézio com o chip, a tabela 2×2 e as duas conferências; o B7 com o plano u, v; a síntese.

**Hook (H1):** a ideia é forte (a integral trava, a grade nova destrava, mas aparece um meio que ninguém chamou), mas o v2 abre com 2 s de papel vazio, depois os eixos, e a integral só entra aos 14 s; a fala abre lendo os quatro cantos antes de dizer qual é o problema. Na final:
- **quadro 0** com eixos + trapézio nascendo e a integral escrita nos primeiros 2 s;
- a fala abre pela integral e pelo problema ("Olha esta integral dupla… ela trava nas duas ordens") e só depois lê os cantos;
- o canto vira `A INTEGRAL QUE TRAVA` (quem chega pelo título não precisa ter visto o vídeo passado);
- fecha com a promessa "no fim, essa integral sai inteira, com número e tudo".

**Evolução:** a ordem segue como está:

régua (1D) → transformação → linear (det) → curva (fator local) → jacobiano → teorema → hipóteses (dobra) → conferência → trapézio → exercício → mundo → síntese

O que atrapalhava o entendimento era a definição das animações (K3, K4) e os quatro buracos de ritmo (K6, K9, K10, K12), não a ordem.

**Gancho final (S2):** o Atlas confirma o próximo, 3.4-T2 **Coordenadas polares** (EP. 12). O EP. 12 abre com "Olha esse sino… quanto vale a integral dupla dela nesse disco?" e com duas células, uma perto da origem e outra longe, com o mesmo Δr e Δθ e a de fora bem maior. O S2 final:
- pergunta exatamente isso (o disco, o sino, as duas ordens que travam);
- mostra as **duas células** e diz que o fator muda de ponto para ponto;
- promete a área inteira debaixo do sino da estatística (o EP. 12 entrega);
- lê θ como **téta**.

---

## 3. Correções (lista fechada)

Cada item traz o tempo no preview v2, o que procurar no código, o que está errado, a troca, o aceite e o quadro (`referencia_final/`).

### K1 · H1: abertura com a integral no quadro 0
**Tempo:** 0:00–0:14. **Quadros:** `K01a` (0:00, só papel), `K01b` (0:02, eixos e trapézio a 10 %).

**Errado:**
- 0:00–0:02 papel vazio; 0:02–0:04 os eixos e o trapézio nascem; a integral `∬_B e^{(x+y)/(x−y)} dA` só aparece por volta de 0:14;
- canto `O DESAFIO DO VÍDEO PASSADO` (depende de ter visto o EP. 10);
- a fala v1.1 lê os cantos antes de dizer o problema.

**Troca:**
1. **Quadro 0:** papel e eixos já estão na tela (são cenário, não termo). O trapézio nasce com `Create` de 0,0 a 1,0 s; a caneta escreve a integral na faixa de baixo de 0,2 a 2,0 s (gatilho "Olha esta integral", a 1ª palavra da fala).
2. Canto `A INTEGRAL QUE TRAVA` desde o quadro 0 (título do vídeo em cima, apagado, como sempre).
3. Novo gatilho "Os cantos do trapézio": quatro pontos brancos pequenos (raio 0,05), um por canto, um por vez (0,25 s cada). Sem rótulo novo: os tiques 1, 2, −1, −2 dos eixos já dão os números.
4. O resto do H1 fica como no v2, com os gatilhos da narração final (tabela do §4).

**Aceite:**
- still em t = 0,000 s: eixos visíveis e trapézio já começando; em t = 1,0 s o trapézio completo; em t = 2,0 s a integral completa (`stills/K01_t0.png`, `K01_t1.png`, `K01_t2.png`);
- `qa_canto`: canto do H1 = `A INTEGRAL QUE TRAVA` em todos os quadros do H1;
- tela parada nos primeiros 3 s = 0.

### K2 · Moldura antes do conteúdo (chip do B3-3 e caixas do A1)
**Tempo:** 6:35,7–6:36,3 (chip `|J| =`); 1:44 (caixa `3 · O F…` do A1). **Quadros:** `K02`, `K14`.

**Errado:** a moldura do chip nasce sozinha e o `|J| =` é escrito depois (≈ 0,4 s de moldura vazia). O QA de moldura vazia não pegou porque o limite era 0,5 s. Nas caixas dos itens do A1, a caixa aparece inteira antes do texto.

**Troca:** moldura e conteúdo nascem **juntos**: o `Create` da moldura com o mesmo `run_time` do início da caneta do rótulo, os dois no mesmo `AnimationGroup(lag_ratio=0)` (são dois traçados, não há preview de destino). O `1/2` continua chegando por voo (K3).

**Aceite:** `qa/moldura_vazia.txt` por quadro com limite **0,1 s** (3 quadros a 30 fps): 0, em chip, selos, placas, cartões e caixas do A1.

### K3 · Voos: cópia duplicada, negrito no pouso e travessia sobre texto (definição das animações)
**Tempo:** 6:36,5; 16:01,5; 17:29; 18:05,5; 19:34. **Quadros:** `K03a`…`K03e`.

**Errado:**
1. **Saída do voo:** o `TransformFromCopy` começa sobre a fonte com o contorno da caneta. Nos primeiros ~0,3 s, fonte e cópia aparecem deslocadas alguns pixels: `11/22` no `ÁREA = |−1/2| = 1/2` (6:36,5) e `‖J‖ = 11/22` no voo do `|J| = 1/2` para o chip (16:01,5).
2. **Pouso em negrito:** a cópia pousa com contorno e fica um quadro mais grossa que o resto da linha.
3. **Travessia:** o trajeto reto passa por cima de texto já escrito:
   - 17:29: o `∫` que desce para `½ ∫₁² v(e − 1/e) dv` cruza a linha `= ∫₁² ∫_{−v}^{v} e^{u/v} · ½ du dv`;
   - 18:05,5: o `3` sai de `3 CÉLULAS` e cruza o próprio rótulo;
   - 19:34: o `2·2` e o `2·1` do `½(2·2 − 2·1)` passam por cima do colchete `½[2v]₁²`.

**Troca (no helper de voo, um lugar só):**
1. a cópia voa só com preenchimento: `src_c = src.copy().set_stroke(width=0)`;
2. `rate_func=rush_from`: sai rápido da fonte e pousa devagar;
3. o destino pousa com `stroke_width = 0` (o contorno fino é só da caneta, durante o `Write`);
4. se o trajeto reto cruza a caixa de algum texto já escrito (amostre 20 pontos do caminho), use `path_arc` com módulo ≥ 0,6 rad para o lado livre; se ainda cruzar, faça o voo por cima da coluna (arco para fora) ou mude a fonte para a cópia mais próxima sem obstáculo;
5. glifo que aparece duas vezes no destino: um vem por voo e o outro pela caneta. Nunca o mesmo glifo de origem mapeado para dois destinos.

**Aceite:**
- `qa/duplicados_por_quadro.txt`: em **todos os quadros**, dois glifos com a mesma forma (mesmo nº de pontos, tamanho ± 10 %) e centros a menos de 1/3 do tamanho, por mais de 2 quadros seguidos, = 0 (exclua só os 2 primeiros quadros de cada voo);
- glifo com contorno > 0,5 px depois do pouso = 0;
- voo × texto escrito (caixas se cruzando) = 0 em todo quadro; voo × traço do desenho ≤ 0,2 s por voo (o v2 tinha 69 amostras R5V);
- prancha `voos_final.jpg`: os cinco momentos acima, um quadro a cada 0,1 s durante o voo.

### K4 · Glyph maps legíveis
**Tempo:** 5:27–5:39 (B3-2), 17:26–17:28 (B6-3), 18:03–18:05 (B6-4). **Quadros:** `K04a`…`K04d`.

**Errado:**
- **(a) nascimento em cima da linha de cima:** em 5:28 a cópia de `= (a + b)(c + d) − ac − bd − 2bc` nasce em cima da própria linha e os glifos descem atravessando-a (a linha parece duplicada, `≡ (a̶+̶b̶)…`);
- **(b) cancelamento com buracos:** em 5:34–5:37 os pares que se cancelam somem e ficam `= ␣ + ad + bc + bd ␣ − bd − 2bc` e depois `= ␣ + ad + bc ␣ − 2bc`, com buracos e um `+` logo depois do `=` por ~3 s; em 5:38, ao fechar os buracos, os sobreviventes passam uns por cima dos outros (`ad + ɑd + b2bc`);
- **(c) linha estendida remapeada:** em 17:27 o trecho `= v e − v e^{−1}` é remapeado para virar `= v e − v e^{−1} = v(e − 1/e)` e os glifos já escritos se embaralham;
- **(d)** em 18:03–18:05 o `2² − 1² = 4 − 1` nasce com glifos se sobrepondo (mesmo caso do (a), menor).

**Troca:**
1. **(a), (d):** a linha nova do mapa fica **abaixo**, com folga de ≥ 0,25 × a altura da linha; a cópia sai com `stroke_width = 0` e `rush_from` (como no K3). Nenhum glifo em movimento sobre a linha de cima por mais de 0,2 s.
2. **(b):** cancelamento em **dois tempos**, no gatilho falado:
   1. os pares que se cancelam (`ac` com `−ac`, `bd` com `−bd`) saem juntos, cada par ao mesmo tempo, com `auto_fade` (0,5 s);
   2. **só depois**, os sobreviventes fecham os buracos (0,8 s), e o `+` que sobraria logo depois do `=` sai junto. O degrau escrito é `= ad + bc − 2bc`, como no v2.
   Buraco aberto na linha por mais de 0,6 s = 0.
3. **(c):** a parte já escrita de uma linha **nunca** entra no mapa. Para estender a linha, só o trecho novo `= v(e − 1/e)` nasce à direita (o `v` voa do `v e`, o resto a caneta), e a linha antiga fica parada.
4. Vale para todos os mapas do vídeo, não só estes quatro.

**Aceite:**
- `qa/legibilidade_mapas.txt`: em todo quadro durante um glyph map, caixas de glifos diferentes (não o mesmo glifo em voo) sobrepostas em mais de 30 % da menor caixa por mais de 0,3 s = 0; buraco > 0,6 s = 0;
- prancha `mapas_final.jpg`: 5:27–5:40 (B3-2) e 17:26–17:29 (B6-3), um quadro a cada 0,5 s.

### K5 · Glifo solto embaixo do plano u, v (B4-1)
**Tempo:** 7:16–7:18 (lote PB4, t ≈ 31,1–33,5 s). **Quadro:** `K05`.

**Errado:** um glifo `0` com um pedaço de seta (`0⌐`) fica sozinho embaixo do plano u, v, em torno de (680, 1000) a 1080p, por ~2,5 s. Não pertence a nenhuma linha nem ao eixo.

**Troca:** liste os objetos visíveis nesse quadro (t do lote ≈ 31,5 s), ache a origem (resto de voo, tique ou rótulo de uma cena anterior) e tire-o da cena no fim do play que o criou.

**Aceite:** `qa/orfaos.txt`: objeto visível com caixa < 40 × 40 px que não é tique, rótulo de eixo, rótulo de vértice nem glifo de uma linha da coluna, por mais de 0,3 s, = 0 no vídeo inteiro.

### K6 · Zoom do B4-1 para o B4-2: sem tela verde e sem corte
**Tempo:** 7:18–7:22 (lote PB4, t ≈ 33–37 s). **Quadros:** `K06a` (antes), `K06b` (7:20, tela verde), `K06c` (7:22, o MNPQ limpo).

**Errado:** a câmera entra no mapa de calor da grade curva (as células GRANDE/PEQUENA em verde) e por ~1,5 s a tela fica toda verde, com o canto em cima do verde. Depois a cena **corta** para o paralelogramo MNPQ limpo, num enquadramento que não é o fim do zoom.

**Troca:**
1. antes do zoom (0,6 s), o preenchimento do mapa de calor vai a 0; só a célula escolhida, a de M = φ(0,75; 0,5), recebe chapa + malha;
2. o zoom mira o centro dessa célula e termina **exatamente** no enquadramento do MNPQ (a mesma célula, os mesmos cantos M, N, P, Q). Sem corte;
3. canto e logo por cima de tudo (z alto).

**Aceite:**
- nenhum quadro do zoom com mais de 40 % da tela coberta por preenchimento;
- distância entre os 4 cantos da célula no último quadro do zoom e os 4 cantos do MNPQ no primeiro quadro do B4-2 ≤ 2 px a 1080p;
- prancha `zoom_final.jpg`, 7:17–7:23 a cada 0,25 s.

### K7 · B4-2: a linha de M pequena e longe
**Tempo:** 7:22–7:46. **Quadro:** `K07`.

**Errado:** `M = φ(0,75; 0,5)` fica pequeno, apagado e no **pé** da coluna (y ≈ 830 a 540p), enquanto o topo está vazio; as linhas `ARCO MN ≅ ‖∂φ/∂u‖ Δu` e `ARCO MQ ≅ ‖∂φ/∂v‖ Δv` nascem acima dela.

**Troca:** `M = φ(0,75; 0,5)` vira a **1ª linha** da coluna (topo, na altura da 1ª linha das outras cenas), no tamanho normal de linha (dígito ≥ 26,7 px), branco. As linhas ARCO descem abaixo dela, na ordem da fala.

**Aceite:** relatório de tamanho com a linha de M ≥ 26 px; ordem de cima para baixo = ordem de nascimento.

### K8 · B5-3: palco pequeno enquanto a coluna está vazia
**Tempo:** 12:16 até o 1º degrau da coluna do B5-3. **Quadros:** `K08a` (12:28), `K08b` (13:47,6).

**Errado:** os dois planos (u, v com as metades laranja e verde-água; x, y com o quadrado) ocupam só o canto esquerdo (unidade ≈ 170 px a 1080p) e a metade direita da tela fica vazia até a coluna começar.

**Troca:** enquanto a coluna está vazia, os dois planos ficam **grandes e centrados** na tela inteira (unidade ≥ 270 px a 1080p, emenda do papel sob a seta de φ). No gatilho do 1º degrau da coluna (`φ(u, v) = (u², v)…`), um único movimento de 0,8 s leva os dois planos para o tamanho e o lugar do v2. A placa `SOBREPOSIÇÃO: CONTOU DUAS VEZES` e a nota `u = 0 É BORDA` nascem depois do movimento, no lugar do v2.

**Aceite:** still no meio da fala da dobra (antes da coluna) com unidade ≥ 270 px; palco vazio (metade da tela sem nada além do papel) ≤ 0,5 s.

### K9 · A dobra (C18) tem de terminar dentro do B5-3
**Tempo:** 13:41–13:48. **Quadros:** `K08b` (13:47,6, o ✓ recém-escrito), `K09` (13:48,2, já é a cena seguinte).

**Errado:** a escada C18 estoura a âncora: o canto já trocou para `CONFERINDO O TEOREMA` (B5-4) enquanto a dobra ainda está sendo escrita, e a última linha `∬_{[0,1]×[0,1]} 2u du dv = ∫₀¹ [u²]₀¹ dv = ∫₀¹ (1 − 0) dv = 1 ✓` fica ≈ 0,3 s na tela antes do corte.

**Troca:** com a voz:
- a escada C18 termina **dentro** do B5-3, e o ✓ fica pelo menos 2,0 s na tela antes da 1ª palavra do B5-4;
- se a fala do B5-3 for mais curta que a escada, aplique a regra de estouro do §6 (a âncora seguinte começa mais tarde); nunca acelere a voz nem corte a caneta abaixo do mínimo;
- o canto troca só no 1º play do B5-4.

**Aceite:** `qa/sync.txt` com o hold do C18.8 ≥ 2,0 s; `qa_canto`: quadros com canto de outra âncora = 0.

### K10 · B5-4: o `8/3` tem de ficar
**Tempo:** 14:22–14:25. **Quadros:** `K10a` (14:23, `= 8/3` sendo escrito), `K10b` (14:24, a escada desmancha).

**Errado:** a última linha `= (4/3 + 4/3) − (0 + 0)` recebe o `= 8/3` e, em menos de 0,5 s, a escada inteira encolhe e se embaralha até virar `COM J: ÁREA = 8/3`. O resultado não é lido escrito na escada.

**Troca:**
1. o `= 8/3` é escrito no fim da última linha (caneta) e a escada inteira fica parada **≥ 2,5 s**;
2. a escada sai com `FadeOut` (0,6 s), **exceto** o `8/3` final, que **voa** (K3) para `COM J: ÁREA = 8/3`; o rótulo `COM J: ÁREA =` é escrito a caneta;
3. nada de encolher a escada inteira.

**Aceite:** `conta_inteira` com o degrau `= 8/3` e hold ≥ 2,5 s; `legibilidade_mapas` = 0 nesse trecho.

### K11 · B6-3: placa `v CONGELADO` em cima do trapézio
**Tempo:** da entrada da placa (≈ 17:00) até a troca de cena (≈ 17:40). **Quadro:** `K11`. Procure `CONGELADO`.

**Errado:** a placa está sobre a borda de cima do trapézio de u, v e cobre parte da faixa verde-água (a fatia com v congelado) e da borda `v = 2`.

**Troca:** a placa sai do trapézio. Fica à direita do rótulo `u = v`, na mesma altura da faixa, com folga ≥ 24 px da borda do trapézio e do rótulo.

**Aceite:** caixa da placa × polígono do trapézio = 0 (interseção de áreas, não só de traços); R5 = 0.

### K12 · B6-3: troca de página sobreposta
**Tempo:** 17:26–17:29. **Quadros:** `K12`, `K04d`.

**Errado:** as linhas `PRIMITIVA EM u: v e^{u/v}` e `CONFERE: d/du (v e^{u/v}) = … ✓` somem ao mesmo tempo em que as linhas de baixo sobem para o lugar delas; por ~1 s há duas camadas de texto meio transparentes uma sobre a outra.

**Troca:** em sequência: `FadeOut` das duas linhas (0,4 s) → só então o `shift` para cima das linhas que ficam (0,6 s). O mesmo padrão em toda troca de página da coluna.

**Aceite:** `legibilidade_mapas` = 0 em todas as trocas de página; prancha `mapas_final.jpg` com 17:26–17:29.

### K13 · Margem
**Tempo:** 18:07 (lote PB6, t ≈ 192,8 s). **Quadro:** `K13`.

**Errado:** um traço de fração e um glifo em voo passam a x = 1857–1874 px (menos de 48 px da borda direita) no B6-4. Os outros 38 casos do relatório de margem são o chão do 3D do B4-2, que é grade.

**Troca:** o voo do B6-4 fica dentro de x ≤ 1872 (arco para dentro ou fonte mais à esquerda). No QA, o chão do 3D sai da conta de margem (é grade, como o papel).

**Aceite:** `qa/margem.txt` = 0, com o chão do 3D excluído e dito no cabeçalho.

### K14 · A1: tela parada e título tardio
**Tempo:** 1:31,5–1:39 (só `CÁLCULO III · MUDANÇA DE VARIÁVEIS` no centro, 7 s), 1:40–1:48. **Quadro:** `K14`.

**Errado:** o título `JACOBIANO E MUDANÇA DE VARIÁVEIS` só começa aos 1:39; por 7 s a tela tem uma linha pequena (o QA de palco parado acusou 7,0 s).

**Troca:**
- o título a caneta começa na 1ª palavra do A1 ("Fala, pessoal") e termina em ≤ 3 s;
- `NESTE VÍDEO` no gatilho "Hoje a gente troca";
- os cinco itens (`1 · A RÉGUA`, `2 · O PARALELOGRAMO`, `3 · O FATOR LOCAL`, `4 · O TEOREMA`, `5 · O TRAPÉZIO`) nos gatilhos da fala ("a régua esticada", "o paralelogramo", "o fator local de área", "o teorema", "o trapézio inteiro"), cada caixa nascendo junto com o seu texto (K2).

**Aceite:** tela parada > 5 s = 0 no A1; moldura vazia = 0.

### K15 · S2: o gancho para coordenadas polares (EP. 12)
**Tempo:** 20:45 até o CTA. **Quadro:** `K15` (o S2 do v2, com uma célula só).

**Fica do v2:** o disco x² + y² ≤ 1 no papel, `∬_{x²+y²≤1} e^{−(x²+y²)} dA`, as tiras com `TRAVA` / `TRAVA` / `EM PÉ E DEITADO`, a grade quadrada que some, a grade de círculos (laranja) e raios (verde-água) com `r` e `θ`, a célula de fora (chapa + malha), o rótulo `ÁREA ≅ ? · Δr Δθ` e o cartão à direita.

**Entra:**
1. uma **segunda célula**, do mesmo Δr e do mesmo Δθ que a do v2, no **mesmo setor**, no 2º anel a partir da origem (a primeira célula que não encosta na origem). Chapa + malha iguais às da célula de fora, no gatilho "Olha estas duas células";
2. uma chave fina pegando as duas células pelo lado de fora do setor, com `MESMO Δr, MESMO Δθ` a caneta (gatilho "o mesmo delta erre");
3. `MENOR` ao lado da célula de dentro e `MAIOR` ao lado da de fora, fora das células, ≥ 26 px (gatilho "bem maior");
4. o `ÁREA ≅ ? · Δr Δθ` nasce depois disso (gatilho "Qual é ele");
5. o cartão ganha uma 3ª linha, `E A ÁREA DEBAIXO DO SINO` (gatilho "debaixo do sino"), na mesma fonte da 2ª linha.

Nenhum outro elemento novo. Sem brilho, sem pulso.

**Aceite:**
- as duas células com Δr e Δθ iguais (log dos parâmetros) e área da de fora > 3 × a de dentro;
- R5 = 0 (rótulos fora das células e da grade de raios);
- cartão ≥ 8 s antes do CTA, sem sobrepor;
- still `S2_final.png` com as duas células, a chave, MENOR/MAIOR e o cartão de 3 linhas.

### K16 · "téta" e gatilhos novos
**Errado:** a v1.1 lia θ como "teta". O Kaio pediu "téta" (a voz não pode ler a palavra comum).

**Troca:**
- na narração final todo θ está escrito **téta**; troque também qualquer `self.gat("…teta…")` e o `narracao_tags.md`;
- `grep -c '\bteta\b'` = 0 na fala, nos gatilhos e no `narracao_tags.md`;
- aplique os gatilhos que mudaram (§4).

**Aceite:** `[gatilho-sem-frase]` = 0 antes da voz.

### O que NÃO mexer
- O conteúdo do B1, B2, B3-1, B3-3 (fora o K2/K3), B4-3 (figura com pernas, 3D, tabela), B5-1, B5-2 (miniaturas), B6-1 (fora o voo), B6-2 (tabela 2×2), B6-4 (metades), B7 (plano u, v e selo), B8 e S1.
- As contas C1–C18, degrau por degrau.
- O papel de tela inteira, as cores e o ciclo do chip.
- A cena Three.js e a câmera do B4-2 (só re-render com a linha do tempo da voz).
- O H1 depois de "Os cantos do trapézio" (só os gatilhos da fala nova).

---

## 4. Narração final v2

Arquivo: `yt_0036_narracao_final_v2.md` (no zip). Ele substitui a v1.1 como fonte do `gerar_ancoras.py`. Tem **4.071 palavras ≈ 22:36** a 3 palavras/s (revisão v2.1: refino do GPT filtrado; o nome do arquivo não muda; a lista do que entrou está no cabeçalho do arquivo).

**O que mudou em relação à v1.1 (só isto):**
- **H1:** abre pela integral e pelo problema ("Olha esta integral dupla… em cima deste trapézio. Ela ficou de desafio no fim do vídeo passado, e tem um problema: ela trava nas duas ordens."); os cantos passam a ser lidos depois das duas travas ("Os cantos do trapézio são…"); fecha com "E, no fim, essa integral sai inteira, com número e tudo.";
- **S2:** "É o famoso sino" (sem citar outro vídeo), as duas células ("Olha estas duas células… As duas têm o mesmo delta erre e o mesmo delta téta, mas a de fora é bem maior. Então o fator de área muda de ponto para ponto. Qual é ele?") e "E, com esse fator, sai até a área inteira debaixo do sino, a curva que está em toda a estatística.";
- **B5-4:** "como no vídeo das regiões gerais" → "do jeito que a gente já sabe" (regra do canal: não citar vídeo pelo nome);
- **téta** no S2 e no Anexo B;
- **revisão v2.1** (só fala): H2 "em vez de decorar a fórmula"; B1-1 lê G(b) − G(a) nas duas primitivas; B3-2 "Na posição do desenho"; B4-2 "positivos"; B4-3 "Perto de M… três vírgula vinte e cinco" e "fator local"; B5-1 "sob as hipóteses certas" + ponte para o teorema; B5-4 lê `(1 − y²/4) − (y²/4 − 1)`; B6-1 "em cinco passos" e "o meio que faltava na abertura"; B6-3 "à fração u sobre vê" e os dois limites do colchete; B7 "a primitiva do cosseno de u"; B8 o divergente; S2 "talvez o problema seja a grade" e "muda com a distância até a origem".

**Gatilhos que mudam:**

| Âncora | Antes | Agora |
|---|---|---|
| H1 | "ficou um desafio"→trapézio | "Olha esta integral"→trapézio + integral (quadro 0, K1) |
| H1 | (não havia) | "Os cantos do trapézio"→os quatro pontos (K1) |
| B1-1 | "e fica quatro sobre"→`2²/2 − 0²/2` e `= 2` | "em dois, quatro sobre dois"→`2²/2 − 0²/2` · "Dá dois"→`= 2` |
| B5-4 | "a saída menos a entrada"→as duas linhas | "a saída menos a entrada"→`(1 − y²/4) − (y²/4 − 1)` · "Distribuindo o sinal"→`= 2 − y²/2` |
| B5-4 | qualquer gatilho com "regiões gerais" | troque para "do jeito que a gente já sabe" |
| S2 | "pedaço de anel"→célula | "Olha estas duas células"→as duas células (K15) |
| S2 | "Qual é o fator"→`?` | "o mesmo delta erre"→chave · "bem maior"→MENOR/MAIOR · "Qual é ele"→`ÁREA ≅ ? · Δr Δθ` |
| S2 | (não havia) | "debaixo do sino"→3ª linha do cartão |

Os demais gatilhos do S2 ("um desafio", "Em pé, trava", "deitado, trava", "círculos e raios", "no próximo vídeo", "deixa o like") continuam no texto. Os gatilhos das contas do B1-1, B6-3 e B7 ("que é um meio", "quatro vezes um meio", "é vê vezes é elevado", "deriva e confere", "colchete de menos vê", "fica vê vezes", "dá seno de vê menos") continuam no texto; rode a busca e corrija qualquer outro que a v2.1 tenha deslocado.

Rode a busca de gatilhos: `[gatilho-sem-frase]` = 0 antes da voz.

---

## 5. Voz (ElevenLabs v4)

Referência: `docs/roteiro_voz_elevenlabs_v4.md`.

1. Confirme `ELEVENLABS_API_KEY` (primeira parada, §0).
   - Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`.
   - Formato `mp3_44100_192`, decodificado para WAV mono 16 bits 44,1 kHz.
2. Gere `narracao_tags.md` e `narracao_limpa.md` a partir da narração final v2 (como no yt_0034). Rode primeiro com `--seco`, depois sem ele:
   ```
   uv run --no-sync python videos/gerar_voz_elevenlabs.py videos_longos/yt_0036_jacobiano_mudanca_variaveis/narracao_tags.md videos_longos/yt_0036_jacobiano_mudanca_variaveis/audio/narracao_v1.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)" --seco
   ```
3. **Uma tomada completa.** Siga com ela. O Kaio ouve em paralelo; se reprovar, ele regera e a §6 refaz tudo sozinha. A tomada aprovada vira `audio/narracao_final.wav`.
4. `qa/voz.txt` (`qa_voz.py`):
   - duração;
   - picos e clipping;
   - silêncio > 1,5 s dentro de um parágrafo;
   - tag lida em voz alta;
   - fronteiras sem corte audível;
   - pronúncia de:
     - letras: "xis", "ípsilon", "u", "vê", "á", "bê", "cê", "dê", "erre", "téta" (nunca "teta"), "i, jota, cá";
     - símbolos: "fi", "gama", "delta", "ômega", "classe cê um", "dê xis dê ípsilon", "dê u dê vê", "á dê menos bê cê", "gê linha de tê";
     - funções: "é elevado à fração xis mais ípsilon sobre xis menos ípsilon", "três quartos de é menos um sobre é", "secante da latitude ao quadrado", "o cosseno de xis menos ípsilon sobre o seno de xis mais ípsilon";
     - nomes: "jacobiano", "Mercator", "Groenlândia", "Parallax Lab".
5. No relatório: modelo, voz, número de blocos, duração e taxa real (palavras ÷ segundos de fala).

---

## 6. Sincronização (a cena segue a voz)

Regras permanentes dos longos:
- WAV contínuo;
- **nunca** cortar a voz por âncora nem inserir silêncio;
- atraso imagem × fala **≤ 0,2 s** (LEAD 0,15 s);
- quando a fala é mais longa que a construção, a espera se divide entre os gatilhos, nunca tudo no fim da âncora.

1. `alinhar_voz.py` → `alinhamento_palavras.json`.
2. `ancoras.json` **gerado por script**: `gerar_ancoras.py` no modo tempo real. Cada âncora começa na primeira palavra do seu trecho. Os `self.gat("…")` são buscados no alinhamento.
3. **3D:** a linha do tempo do Three.js do B4-2 sai do mesmo `ancoras.json`. Re-renderize e rode o QA de alinhamento (≤ 2 px) e o QA dos pousos.
4. Rode os lotes 540p e confira:
   - `[gatilho-sem-frase]` = 0;
   - os `[estouro]`, cada um com o motivo. Estouro > 1 s numa âncora: encurte a animação dentro da regra da caneta ou deixe a âncora seguinte começar mais tarde. **Nunca** acelere a voz. O C18 (K9) é o caso mais provável.
5. `qa/sync.txt` (`qa_sync.py`): o atraso de cada âncora, de cada degrau das contas e de cada gatilho do §3 (meta ≤ 0,2 s).
6. **Legenda `.srt`** (`gerar_srt.py`):
   - até 2 linhas × 42 caracteres, de 2 a 5 s por bloco;
   - tempo do WAV = tempo do vídeo;
   - trocas:
     - "xis" → x, "ípsilon" → y;
     - "u" → u, "vê" → v (só como variável), "erre" → r, "téta" → θ;
     - "fi" → φ, "delta" → Δ (com a letra: "delta u" → Δu);
     - "á dê menos bê cê" → ad − bc;
     - "é elevado a" → e^ (só no número de Euler);
     - "Cálculo um" → "Cálculo I".

---

## 7. Conferência 540p com voz (antes do 1080p)

Render de **todos os lotes** em 540p/15 fps com os tempos da voz, e preview com voz. Feche o que falhar antes do 1080p.

**Portões:**
- `FLASH POR QUADRO` = 0;
- **GRADE** de tela inteira em ≥ 95 % dos blocos de cada amostra 2D (exceções: o 3D do B4-2, o S2 depois que a grade quadrada some, o CTA);
- **MOLDURA VAZIA por quadro**, limite 0,1 s = 0 (K2);
- **DUPLICADOS por quadro** = 0, inclusive durante voos e glyph maps (K3);
- **LEGIBILIDADE DOS MAPAS** = 0 (K4, K10, K12);
- **ÓRFÃOS** = 0 (K5);
- R5 = 0 a cada quadro (texto × texto, texto × traço, placa × região), também durante os voos; voo × texto = 0 e voo × traço ≤ 0,2 s por voo (K3);
- canto: troca no 1º play de cada bloco; quadros com canto de outra âncora = 0 (K9);
- margem segura: ≥ 48 px da borda (chão do 3D excluído, K13); dígito ≥ 26 px (≥ 32 px nas linhas-chave);
- alinhamento 3D ≤ 2 px; pousos sem pisca; zoom do K6 sem corte (≤ 2 px);
- tela parada > 5 s = 0; a lista de 3 a 5 s vai com a fala ao lado;
- palco vazio ≤ 0,5 s (K8);
- `[gatilho-sem-frase]` = 0;
- tabela CONTAS com cada degrau C1–C18, o tempo e a frase que o dispara, mais os holds do C18.8 (≥ 2,0 s) e do `8/3` (≥ 2,5 s);
- `qa_canto.py` e `qa_fundo.py`;
- cartão do S2 ≥ 8 s; B7 `PAUSE E TENTE` com o tempo da fala;
- SYNC e VOZ.

**Pranchas:**
- `correcoes_final.jpg`: para cada K1–K15, o quadro do erro (`referencia_final/`) ao lado do quadro corrigido no gatilho do item;
- `voos_final.jpg` (K3), `mapas_final.jpg` (K4, K12), `zoom_final.jpg` (K6);
- uma prancha com **um quadro de cada âncora no instante da primeira palavra** (24 quadros).

---

## 8. Render final 1080p

1. **Three.js em 1080p** (o B4-2), com a mesma câmera e a linha do tempo da voz, e QA 3D de novo sobre o 1080p.
2. **Manim em 1080p30** pelo fluxo normal, com `template/config_horizontal.py`.
   - Não configure CRF: o `template/qualidade.py` já usa **14** em renders ≥ 1080p.
   - Não recodifique. Sem teto de tempo de render.
3. **Emenda** com `montar_final.py` (remux, sem reencodar), na ordem dos lotes.
4. **Master:**
   ```
   uv run python videos/montar_master.py <sem_audio_1080p30.mp4> audio/narracao_final.wav renders/yt_0036_master_final_1080p30.mp4
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
  - início (a integral do H1);
  - `det = 5` do B3-2;
  - `2 ≠ 1` da dobra (C18, B5-3);
  - `8/3` do B5-4;
  - `(3/4)(e − 1/e)` do B6-3;
  - fim.
- `renders/capitulos_final.txt` com os tempos da voz:

| Âncora | Título |
|---|---|
| H1 | `A INTEGRAL QUE TRAVA` |
| A1 | `BEM-VINDOS` |
| B1-1 | `A RÉGUA ESTICADA` |
| B2-1 | `A TRANSFORMAÇÃO` |
| B3-1 | `O PARALELOGRAMO E O DETERMINANTE` |
| B4-1 | `A GRADE CURVA` |
| B4-3 | `O JACOBIANO` |
| B5-2 | `O TEOREMA DE MUDANÇA DE VARIÁVEIS` |
| B5-3 | `POR QUE INVERSÍVEL` |
| B6-1 | `O TRAPÉZIO DO COMEÇO` |
| B7 | `PAUSE E TENTE` |
| B8 | `O JACOBIANO NO MUNDO` |
| S1 | `JUNTANDO TUDO` |

**Entrega:** `uv run python videos/entregar.py yt_0036` (cópia).
- O destino tem de ser o `entregas/` do checkout principal.
- A pasta leva:
  - `master`;
  - `legenda` (`.srt`);
  - `audio/`;
  - `texto/`: ficha, `narracao_tags.md`, `narracao_limpa.md`, este handoff e os capítulos;
  - `manifesto`.
- O número `0036` vai no fim de cada nome. Não há capa.
- Série, EP e assunto vêm da `ficha.md`: `CÁLCULO III · EP. 11`, `# Jacobiano e mudança de variáveis`.
- **Na ficha:** a duração real e `duracao_alvo` da narração final v2.

Não rode `entregar.py` se um portão do §7 estiver aberto. Pare e reporte.

---

## 10. Relatório de entrega (obrigatório, e depois pare)

1. Arquivos alterados e criados (com arquivo:linha de cada K).
2. K1–K16, cada um com o caminho do still que prova, e as pranchas `correcoes_final.jpg`, `voos_final.jpg`, `mapas_final.jpg` e `zoom_final.jpg`.
3. Todos os portões do §7 com números reais, a tabela CONTAS, a sincronização das 24 âncoras e o QA de voz.
4. Caminhos: WAV, preview 540p com voz, master 1080p, `.srt`, capítulos e a pasta em `entregas/`.
5. Three.js: cena, resolução, custo por quadro no 1080p, alinhamento medido (px).
6. Duração final e taxa real da voz, comparadas com 3 palavras/s.
7. sympy: 41/41 e 26/26.
8. Pendências reais.

Depois do relatório: **pare**. Não faça publicação, capa, commit, merge nem push.

---

## Anexo A · Números congelados

| Onde | Valor |
|---|---|
| H1 | trapézio (1, 0), (2, 0), (0, −2), (0, −1); u = x + y, v = x − y; 1 ≤ v ≤ 2, −v ≤ u ≤ v; 3 células da grade nova (1 + 1 + ½ + ½); área no papel 3/2 → cada célula vale 1/2 |
| B1-1 | ∫₀² x dx = 2; x = 2t ⇒ dx = 2 dt; ∫₀¹ (2t)·2 dt = 4 · 1/2 = 2 ✓ |
| B3 | φ(u, v) = (2u + v, u + 3v); caixa (2 + 1)(1 + 3) = 3 · 4 = 12; menos 2 · (2·1/2) = 2, 2 · (1·3/2) = 3 e 2 · (1·1) = 2 → 12 − 2 − 3 − 2 = 5; det = 2·3 − 1·1 = 5; ad − bc pela caixa |
| B3-3 | x = (u + v)/2, y = (u − v)/2; det = −1/4 − 1/4 = −1/2; ÁREA = \|−1/2\| = 1/2 (orientação invertida) |
| B4 | φ(u, v) = (u² − v², 2uv); J = 4u² + 4v²; em M = (0,75; 0,5): J = 2,25 + 1 = 3,25; em (0, 0): J = 0; razão área real / \|J\|ΔuΔv: 1,44 → 1,16 → 1,08 → 1,02 |
| B5-3 (C18) | φ(u, v) = (u², v) em [−1, 1] × [0, 1]: J = 2u; ∫₋₁¹ \|2u\| du = 1 + 1 = 2; ∬ = 2 ≠ 1 (área da imagem); metade da direita [0, 1] × [0, 1]: ∬ 2u du dv = 1 ✓ (u = 0 é borda) |
| B5-4 | parábolas: ∬_{[0,1]²} (4u² + 4v²) du dv = 4/3 + 4/3 = 8/3; deitado também 8/3 |
| B6 | \|J\| = 1/2; ∂(u, v)/∂(x, y) = −2 e (−2)(−1/2) = 1 ✓; ∫_{−v}^{v} e^{u/v} du = v(e − 1/e); ½ ∫₁² v(e − 1/e) dv = (3/4)(e − 1/e) ≈ 1,763; f = 1 → 3 · 1/2 = 3/2 = área no papel 2·2/2 − 1·1/2 ✓ |
| B7 | J = +1/2; ∫_{−v}^{v} cos u / sen v du = 2 sen v / sen v = 2; ½ ∫₁² 2 dv = ½ (2·2 − 2·1) = 1 |
| B8 | Mercator: fator sec²(latitude); 72° → ≈ 10,5; Groenlândia × África ≈ 14 |

Se algum valor da tela divergir dos scripts de `verificacao/`, vale o script; reporte.
