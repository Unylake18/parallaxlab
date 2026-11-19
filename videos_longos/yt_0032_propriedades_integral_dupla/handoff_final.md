# yt_0032 · CÁLCULO III · EP. 07 · Propriedades da integral dupla · HANDOFF FINAL
**Correções de tela + voz + sincronização + legenda `.srt` + render 1080p + master + entrega**

Arquivo único e autocontido. A narração é a **v3.1 fechada** (v3 + 8 trocas de frase, §4), que vai no zip como `narracao_v31.md` e substitui o `narracao.md` da unidade.

Data: 2026-11-13. A base é o **preview v2**: 17:52, 960×540, 15 fps, sem voz. O Kaio aprovou como base e pediu para deixar "tudo bem redondinho" antes da narração.

O que este documento traz:
- a lista fechada de correções (§3), com tempo no v2, arquivo e linha, troca e aceite. Os quadros do erro estão em `yt_0032_final_quadros_do_erro/` no zip;
- o fechamento: voz, sincronização, 1080p, QA e entrega.

O que continua valendo:
- tudo o que o v2 acertou;
- os handoffs v1 e v2 e os alvos `referencia/` e `referencia_v2/`, onde este documento não diverge;
- a arte do meio da rodada (cordão, metal, balança).

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
- qualquer mudança em `template/`, `assets/`, `pyproject.toml`, `uv.lock`, `AGENTS.md` ou `docs/`.

**O que pode ser alterado:**
- só a unidade `videos_longos/yt_0032_propriedades_integral_dupla/`;
- `renders/` e `entregas/`, que são saída;
- pode **copiar** scripts do pipeline de voz do yt_0028 (ou do yt_0029, se ele já estiver fechado) para dentro da unidade, sem alterar esses vídeos.

**Modo de execução:**
- Não encerre a vez entre etapas.
- Depois de lançar um render (Manim ou Three.js) ou a geração de voz, espere na mesma vez e siga direto para a auditoria. Use um comando em primeiro plano com timeout de até 10 min por lote, ou um laço `until` que consulta o arquivo de saída.
- Mensagem de progresso não é entrega.

**Só há duas paradas permitidas:**
1. A variável `ELEVENLABS_API_KEY` não existe na sessão. Peça ao Kaio. **Nunca** grave a chave em arquivo, log ou relatório.
2. O WAV passa de **19:30**. Reporte a duração e pare: quem decide cortes é a Produção.

Qualquer outra dúvida: escolha a leitura mais provável, diga qual e siga.

**Ordem:** §3 correções no código, com stills de conferência → §5 voz → §6 sincronização → §7 conferência 540p com voz (prova das correções) → §8 1080p → §9 QA e entrega → §10 relatório. Pare só depois do relatório.

Guarde este arquivo na unidade como `handoff_final.md`. Copie `yt_0032_final_quadros_do_erro/` do zip para `referencia_final/`.

---

## 1. Estado de partida
- **Unidade:** `videos_longos/yt_0032_propriedades_integral_dupla/`.
- **Lotes:** PH, PA, PB1, PB2, PB3, PB4, PB5, PB6, PB7, PS (`cena.py`).
- **Lotes com 3D:** PB1, PB2, PB3, PB6 (`render3d.sh`).
- **Kit:** `kit.py`, `lib32.py`, `v32.py`. QA: `qa32.py`, `comparar.py`. Âncoras: `narracao.md` → `gerar_ancoras.py` → `ancoras.json`. Hoje o `gerar_ancoras.py` está no modo de estimativa; o modo "tempo real da voz" vem do yt_0028.
- **Pipeline de voz:** copie do yt_0028 e adapte nomes, lotes e caminhos:
  - `alinhar_voz.py` (alinhamento forçado + STT de conferência);
  - o modo "tempo real da voz" do `gerar_ancoras.py`;
  - `gerar_srt.py`, `render1080.sh`, `montar_final.py`, `qa_parado.py`, `qa_canto.py`, `qa_fundo.py`.
- **Não reabrir:**
  - a matemática e os números (Anexo A);
  - a ordem H → A → B1 … B7 → S;
  - as cores (f ciano #35D9FF, g lilás #C9A7FF, x² âmbar #FFC24D, y² magenta #EA63FF, menta #8CFFD2, coral #FF7A8A, ponto #E08A3C);
  - o fundo violeta com a grade dos eixos;
  - o 3D em Three.js;
  - a arte do cordão, do metal e da balança;
  - nada de livros nem do Atlas na tela ou na fala.
- **A cena segue a voz.** Os tempos do v2 não valem mais. Todos os lotes, inclusive os quadros do Three.js, são re-renderizados com a linha do tempo da voz.

---

## 2. Avaliação do v2 (resumo)

O v2 cumpriu o handoff v2:
- termos com origem nos itens D1–D12;
- k negativo em 3D;
- a vista de cima do muro;
- Space Grotesk e `\dfrac`;
- 24 passos de glyph map;
- palco parado = 0;
- cartão do Fubini com 10,3 s.

Assisti o vídeo inteiro (um quadro a cada 4 s e os trechos críticos em resolução cheia). Sobraram **18 correções** (mais o C19, que veio da narração v3.1):
- a maioria é **número ou símbolo que ainda aparece sem origem**, nos pontos que o v2 não cobria;
- três são **notação ou representação**;
- duas são **glitches de animação**.

Nenhuma muda os números ou a ordem. A narração recebeu 8 trocas pontuais de frase (§4); uma delas pede o C19.

---

## 3. Correções (lista fechada)

Formato de cada item:
- **Onde:** bloco · tempo no v2 · arquivo:linha · quadro do erro no zip;
- **Errado:** o que está errado;
- **Troca:** o que fazer;
- **Gatilho:** a frase da narração v3 em que o evento acontece;
- **Aceite:** como provar.

Prove cada item com um **still no gatilho** (`still.sh`, 960×540) antes da voz e, de novo, na prancha do §7.

### Didática: número ou símbolo sem origem

**C1 · B1-1 · a grade não refina.**
- **Onde:** 2:00–2:20 · `sec_b1.py:15-20` · `C01_b11_grade_parada.jpg`
- **Errado:** a fala explica integrabilidade ("suas somas de Riemann convergem… à medida que a partição fica fina, independentemente dos pontos escolhidos"), mas a chapa fica com a grade 4×4 parada.
- **Troca:**
  - Em "à medida que a", a grade refina 4 → 8 → 16. Cada nível novo **nasce no lugar** (`Create` das linhas novas), sem `Transform` de uma grade na outra: ver C17.
  - Em "independentemente dos pontos", entra um ponto laranja (#E08A3C, raio 5) por célula da grade 8×8, e os pontos pulam duas vezes para outras posições dentro da própria célula (0,5 s cada).
  - Os pontos saem em "esse valor é escrito".
- **Aceite:** stills nos dois gatilhos; o palco muda dentro do B1-1.

**C2 · B1-4 · o 1,53 (e o 4) sem origem.**
- **Onde:** 4:12–4:24 · `sec_b1.py:236-251` · `C02_b14_153_sem_origem.jpg`
- **Errado:** `2 · 1,53` aparece sem dizer que 1,53 m² é a área do metal de cima, e `1 · 4` sem dizer que 4 m² é a área da chapa.
- **Troca:**
  - Em "uma camada de um", prenda o rótulo `ÁREA 4 m²` (GEO, 26 px) na camada, abaixo de `1 kg/m²`.
  - Em "mais um reforço de", prenda `ÁREA ≈ 1,53 m²` no reforço. Logo abaixo, a legenda GEO `4 − 2,472 DO METAL LEVE`. O 2,472 é a área leve: no metal leve, ρ = 1, então a massa 2,472 kg da balança vale 2,472 m².
  - Em `a1` (`1 · 4`), o 4 **voa** de `ÁREA 4 m²`. Em `a2` (`2 · 1,53`), o 1,53 **voa** de `ÁREA ≈ 1,53 m²`. Use `TransformFromCopy` com `path_arc`, como no M9.
- **Aceite:** `origens_final.txt` lista os dois voos; still em "o reforço aproximadamente três".

**C3 · B2-2 · m e M soltos.**
- **Onde:** 5:36–5:52 · `sec_b2.py:108-114` · `C03_b22_m_M_soltos.jpg`
- **Errado:** `m · α ≤ ∬_B f ≤ M · α` não se liga às duas lajes que já estão na tela (`1 · 4 = 4 kg` e `3 · 4 = 12 kg`).
- **Troca:** pares que acendem juntos, na mesma cor, sem objeto novo:
  - Em "um valor eme minúsculo": acendem o `m` da fórmula e o `1` de `1 · 4 = 4 kg` em azul AZC #7FB2FF. Acrescente `m = 1` (AZC, 30 px) à esquerda da laje de baixo.
  - Em "e um eme maiúsculo": acendem o `M` e o `3` de `3 · 4 = 12 kg` em coral. Acrescente `M = 3` (coral, 30 px) à esquerda da laje de cima.
  - Em "que chamamos de alfa": acendem os dois `α` e os dois `4` em GEO.
  - Cada par volta à cor normal depois de 1,2 s. `m = 1` e `M = 3` ficam até o fim do bloco.
- **Aceite:** stills nos três gatilhos.

**C4 · B3-2 · a cota da tabela sem conta.**
- **Onde:** 6:48–7:00 · `sec_b3.py:67-68` · `C04_b32_cota_sem_conta.jpg`
- **Errado:** os números da coluna `COTA (kg)` aparecem prontos.
- **Troca:**
  - Abaixo de `COTA SUPERIOR`, a linha `\text{cota} = 100 \cdot \text{área}` (36 px), escrita em "a cota superior desse muro chega", **antes** da primeira linha da tabela.
  - Na linha n = 64, o `9,3` nasce de um glyph map curto, ao lado da tabela: `100 \cdot 0{,}093 → 9{,}3`. O 100 voa do rótulo `ρ = 100` no topo do muro e o 0,093 voa da célula ÁREA da mesma linha. Depois, o 9,3 desce para a célula COTA.
  - As linhas seguintes (128 … 1024) entram como hoje.
- **Aceite:** +1 glyph map em `glyphmaps_final.txt` (mapa 14); still em "nove vírgula três".

**C5 · B3-3 · o L ≈ 2,25 m só existe no zoom.**
- **Onde:** 7:28–7:36 · `sec_b3.py:152` · `C05_b33_L_no_zoom.jpg`
- **Errado:** L é o comprimento da solda inteira, mas o rótulo está no painel de zoom, que mostra só um pedaço.
- **Troca:**
  - Em "a linha da solda tem", a solda inteira da chapa (à esquerda) acende em laranja POS e é percorrida da esquerda para a direita em 1,2 s.
  - Prenda `L ≈ 2,25 m` (POS, 30 px) acima da curva, perto do ponto mais alto.
  - O `2{,}25` de `src` e de `V1` passa a voar **desse** rótulo.
  - O `6 kg/m²` continua no zoom, porque é a densidade do cordão.
- **Aceite:** still em "dois vírgula vinte e cinco".

**C6 · B6-1 · o raio 1,63 sem conta.**
- **Onde:** 11:52–11:56 · `sec_b6.py:68-71` · `C06_b61_raio_163.jpg`
- **Errado:** `ARCO DE RAIO 1,63` aparece sem a conta.
- **Troca:**
  - Depois de `x² + y² = 8/3`, um glyph map (mapa 15): `\X^2+\Y^2=\dfrac{8}{3}` → `r^2=\dfrac{8}{3}` → `r=\sqrt{\dfrac{8}{3}}\approx 1{,}63`.
  - O `x² + y²` vira `r²`, com a legenda GEO `r: DISTÂNCIA ATÉ A ORIGEM`.
  - Na chapa 3D, um segmento fino POS liga a origem a um ponto do arco, com `r` (28 px) preso no meio.
  - Gatilho: "a um vírgula sessenta e três da origem".
  - A legenda `lr` fica só `ONDE f = MÉDIA`.
- **Aceite:** mapa 15 no log; still no gatilho; alinhamento ≤ 2 px do segmento.

**C7 · B6-3 · o mínimo e o máximo sem conta, e desligados de m e M.**
- **Onde:** 12:48–13:08 · `sec_b6.py:152-155` · `C07_b63_min_max.jpg`
- **Errado:** `min = 0` e `max = 8` aparecem prontos, e a fórmula da linha seguinte usa `m` e `M`, que não se ligam a eles.
- **Troca:**
  - `lmin` = `m=\f(0,0)=0` (28 px); `lmax` = `M=\f(2,2)=2^2+2^2=8` (28 px).
  - Na fórmula `C1`, o `m` e o `M` **voam** desses rótulos (`TransformFromCopy`), em vez de nascer da caneta.
  - Mova o `÷ α` (`sec_b6.py:167`) para encostar na linha `C1b`: 24 px à direita do último glifo, na altura do meio da fração, com 30 px.
- **Aceite:** stills em "e o máximo é oito" e "dividindo pela área"; os dois voos em `origens_final.txt`.

**C8 · H1 e B6-4 · a média 1,76 sem conta.**
- **Onde:** H1, 0:48 · `sec_h.py:71` · `C08a_h1_media.jpg`. B6-4, 13:48 · `sec_b6.py:221-231` · `C08b_b64_media.jpg`
- **Errado:** "média ≈ 1,76" e "média 2" aparecem sem conta, e a regra da série é a fórmula-mãe antes do número.
- **Troca:**
  - **H1:** `q3` vira `MÉDIA = \dfrac{\Ci{7{,}06}}{4}\approx\Ci{1{,}76}\ \text{kg/m}^2`. O 7,06 voa da soma `S` (que está na tela) e o 4 é escrito pela caneta.
  - **B6-4, cartão 1:** abaixo do subtítulo, `\dfrac{7{,}06}{4}\approx 1{,}76` (30 px).
  - **B6-4, cartão 2:** abaixo do subtítulo, `\dfrac{1+3}{2}=2` (30 px), com a legenda `ÁREAS IGUAIS` (GEO, 24 px).
  - **O ponto laranja do cartão 1** (`dp_`, `sec_b6.py:238`) termina no canto do degrau 3 e fica lá sem sentido. Depois do salto, ele sai (`FadeOut` 0,3 s).
- **Aceite:** stills em "um vírgula setenta e seis quilo por metro quadrado" (H1) e "a média é dois" (B6-4).

**C9 · B7-1 · o 1 e o 0 dos eixos sem conta.**
- **Onde:** 15:16–15:20 · `sec_b7.py:37` · `C09_b71_eixos.jpg`
- **Errado:** `SEM LIMITE: 1 NO EIXO x, 0 NO EIXO y` é afirmado, não calculado.
- **Troca:**
  - Em "pelo eixo horizontal", a linha `\text{eixo } x:\ \dfrac{x^2}{x^2+0}=1` (34 px).
  - Em "pelo vertical, zero", a linha `\text{eixo } y:\ \dfrac{0}{0+y^2}=0`.
  - Cada resultado **voa** para o rótulo `1` ou `0` dentro do disco.
  - A legenda vira só `SEM LIMITE NA ORIGEM` (GEO, 26 px), em "e o limite na origem nem existe".
  - Use `\X` e `\Y` com as cores âmbar/magenta, como no resto do bloco.
- **Aceite:** os dois voos em `origens_final.txt`; still em "pelo vertical, zero".

**C10 · B7-2 · a soma = 1 e o π sem conta.**
- **Onde:** 15:48–16:04 · `sec_b7.py:98-106` · `C10_b72_soma_1.jpg`
- **Errado:** a fala diz "o numerador fica igual ao denominador. Resultado: um!", mas a tela só mostra o disco azul com "1". O `= π` também aparece pronto.
- **Troca:**
  - **Mapa 16**, à direita dos discos, em "Somando as duas, fora da origem":
    - `\Am{\dfrac{x^2}{x^2+y^2}}+\Mg{\dfrac{y^2}{x^2+y^2}}`
    - → `\dfrac{\Am{x^2}+\Mg{y^2}}{x^2+y^2}`: os dois numeradores se juntam sobre **uma** barra; os dois denominadores viram um;
    - → `=1`: em "Resultado: um!", numerador e denominador acendem em CI e somem juntos, como no cancelamento padrão.
  - O `1` final **voa** para o disco azul.
  - **O π (mapa 17)** em "que é a área: pi": `\iint_{\text{disco}}1=\text{área}=\pi\cdot 1^2=\pi`. O 1 voa do disco azul, o 1² do "raio 1" e o π segue para a linha `A1`.
- **Aceite:** mapas 16 e 17 no log; stills em "Resultado: um!" e "que é a área".

**C11 · S2 · a "área leve" sem lugar no desenho.**
- **Onde:** 17:16–17:24 · `sec_s.py:69-75` · `C11_s2_area_leve.jpg`
- **Errado:** `2 · área leve` não aponta para a região.
- **Troca:**
  - Quando `área leve` é escrita, o pedaço leve da chapa (abaixo da solda) ganha contorno CI de 3 px e preenchimento CI a 25%, por 1,5 s.
  - Depois fica só o contorno, até as fatias entrarem.
  - Ao lado da chapa, a legenda `ÁREA LEVE: ABAIXO DA SOLDA` (GEO, 24 px).
- **Aceite:** still em "numa conta no papel".

### Notação e representação

**C12 · B3-1 e B3-2 · B virou duas coisas.**
- **Onde:** 6:28–6:40 · `sec_b3.py:44` e `:50` · `C12_b31_B_e_solda.jpg`
- **Errado:** `B TEM CONTEÚDO NULO ⇒ ∬_B f = 0` e `|∬_B f| ≤ …` chamam a solda de B. No resto do vídeo, B é a chapa (B1-1 e B4-1) ou o metal leve (B5).
- **Troca:**
  - Chame a solda de **S**: `S TEM CONTEÚDO NULO ⇒ ∬_S f = 0` e `\left|\iint_S\f\right|\le M\cdot\text{área da cobertura}`.
  - Em "Começa pela solda matemática", prenda um rótulo `S` (MEN, 34 px) junto à solda na cena 3D (ponto 3D novo no `timeline.json`, ≤ 2 px).
  - A fala não diz a letra, então nada muda nela.
- **Aceite:** `grep -n "iint_B" sec_b3.py` sem ocorrência no B3-1 e no B3-2; still em "essa é a quarta".

**C13 · B4-2 · o disco reusa o nome f.**
- **Onde:** 9:04–9:16 · `sec_b4.py:125-139` · `C13_b42_disco_f.jpg`
- **Errado:** no B4-1, f é a densidade com ρ = 1 na solda. No B4-2, o disco também se chama f (`∬_disco f`, `f COM FURO NA ORIGEM`, `f(0,0) = 5`). Foi pedido meu no v2 ("sem letras novas"), mas ficou ambíguo.
- **Troca:**
  - `it` vira `\iint_{\text{disco}}\Am{\dfrac{x^2}{x^2+y^2}}` (34 px). É a função do B7, que reaparece lá.
  - `lfu` vira `UMA FUNÇÃO COM FURO NA ORIGEM`.
  - `nl` vira `\text{no furo}=` + valor (0, 1, 5), dentro do quadro e à direita do disco, não fora dele.
- **Aceite:** still em "como um furo na origem".

**C14 · B5-2 · a faixa de 0,2 parece medida ao longo da curva.**
- **Onde:** 10:28–10:36 · `sec_b5.py:143-153` · `C14_b52_faixa.jpg`
- **Errado:** a faixa acompanha a solda, e a área sai `0,2 · 2`. Sem uma cota vertical, o aluno pode achar que deveria ser `0,2 · 2,25`.
- **Troca:**
  - Em "numa faixa de vinte centímetros de altura", desenhe uma **cota vertical** (seta dupla GEO de 2 px, com traços nas pontas) cruzando a faixa em x = 0,5, rotulada `0,2 m`.
  - `lf` vira `FAIXA DE 0,2 m DE ALTURA`.
  - Abaixo de `FAIXA: 0,2 · 2 = 0,4 m²`, a legenda `ALTURA × LARGURA` (GEO, 24 px).
- **Aceite:** still em "a soma das áreas".

**C15 · B6-2 · a hipótese do caminho só em palavras.**
- **Onde:** 12:16–12:24 · `sec_b6.py` (B6-2) · `C15_b62_caminho.jpg`
- **Errado:** a fala explica "dois pontos quaisquer da região podem ser ligados por um caminho contínuo que não sai dela", e o palco não mostra.
- **Troca:**
  - Em "dois pontos quaisquer", entram na chapa dois pontos brancos (raio 6) em (0,4; 1,5) e (1,7; 0,4).
  - Em "por um caminho contínuo", nasce entre eles uma curva POS de 3 px (Bézier por (0,7; 0,6) e (1,3; 1,6)), traçada em 1,2 s.
  - O caminho fica até "e a função é contínua" e sai antes do `(r, s)`.
- **Aceite:** still em "que não sai dela".

### Ritmo e glitches

**C16 · S1 · a lista das sete propriedades está apertada.**
- **Onde:** 16:24–16:56 · `sec_s.py:17` · `C16_s1_lista.jpg`
- **Errado:** são 7 itens em 3 linhas de 26 px, ilegíveis em tela de celular.
- **Troca:**
  - Uma propriedade por linha, 7 linhas, 30 px.
  - O numeral romano vai em CI e o resto em BR, com espaçamento de 44 px.
  - Use a coluna direita, abaixo dos três cartões ✓. Se não couber, use duas colunas (I–IV e V–VII).
  - Cada linha entra no mesmo gatilho do agrupamento de hoje.
- **Aceite:** R-texto = 0; nenhuma sobreposição com os cartões.

**C17 · S2 · a grade refina com riscos diagonais.**
- **Onde:** 17:07–17:09 · `sec_s.py:59-62` · `C17_s2_riscos.jpg`
- **Errado:** quando a grade passa de 4 → 8 → 16, as linhas novas aparecem tortas, como riscos diagonais. É o `Transform` de uma grade na outra.
- **Troca:**
  - As linhas novas nascem **no lugar** (`Create`, de baixo para cima nas verticais e da esquerda para a direita nas horizontais).
  - As velhas ficam, porque são subconjunto da nova.
  - Nenhuma linha gira.
- **Aceite:** tira de 6 quadros em 17:06–17:10 sem linha inclinada.

**C18 · H1 e S2 · o início do H1 e o canto vazio do S2.**
- **Onde:**
  - H1, 0:12–0:14 · `sec_h.py:31-45` · `C18a_h1_quebra.jpg`;
  - S2, 17:00–17:36 · `sec_s.py` · `C18b_s2_canto.jpg`.
- **Errado:**
  - No H1, a chapa se parte e três pontinhos brancos soltos aparecem fora dela. Os pedaços cruzam o travessão da balança no caminho para os pratos.
  - No S2, o canto fica sem título.
- **Troca:**
  - **H1:** a balança entra **antes** (`FadeIn` 0,5 s, sem os pontos de pivô soltos). Os pedaços sobem e descem cada um no seu prato por um arco **acima** do travessão.
  - **S2:** `poe_canto(self, "O PRÓXIMO PASSO")` no início do S2. O canto some com o resto na entrada do CTA.
- **Aceite:** tira de 0:11–0:15 sem objeto solto; `qa_canto.py` sem trecho vazio fora do CTA.

**C19 · B3-3 · o cordão de 1 mm vira 13,5 g.**
- **Onde:** 7:44 · `sec_b3.py:171-177` · `C05_b33_L_no_zoom.jpg` (mesmo bloco).
- **Errado:** 6 · 2,25 · 0,001 = 0,0135 kg = 13,5 g, e a tela diz `13 g`.
- **Troca:** na linha `0,01 → 0,001`, o resultado vira `13{,}5\ \text{g}` (`135 g → 13,5 g → 0`). A fala v3.1 diz "uns treze gramas e meio".
- **Aceite:** still em "com um milímetro".

**Total esperado de glyph maps:** 24 passos do v2 + mapas 14, 15, 16 e 17, com 1 passo no 14, 2 no 15, 2 no 16 e 1 no 17. **Total: ≥ 30 passos.**

---

## 4. Narração v3.1 (8 trocas de frase sobre a v3)

Copie `narracao_v31.md` do zip por cima do `narracao.md` da unidade. São 3.177 palavras, cerca de 17:40 de fala a 3 palavras/s, com as mesmas 26 âncoras e as mesmas primeiras palavras de cada âncora.

As trocas, e o `self.gat` que muda em cada uma:

| Bloco | v3 → v3.1 | Gatilho no código |
|---|---|---|
| B3-1 | "mas a área vai ficando cada vez menor" → "mas o que vai ficando pequeno é a área da base" | `a altura pode ser` fica |
| B3-2 | "o que desaparece é a área da cobertura. Repetindo, a contribuição fica menor…" → "o que encolhe é a área da cobertura. Refinando sempre, a cota fica menor…" | `sec_b3.py:105` `repetindo a contribuição fica` → `refinando sempre a cota` |
| B3-3 | "uns treze gramas." → "uns treze gramas e meio." | `com um milímetro uns` fica; tela no C19 |
| B3-3 | "A integral dupla com densidade superficial limitada não representa…" → "É uma descrição diferente da densidade superficial limitada que usamos na integral dupla." | nenhum |
| B4-1 | "A média, dois?" → "O meio-termo, dois?" (2 é a média de 1 e 3, não a média da chapa, 1,76) | nenhum; o chip continua `ρ = 2` |
| B6-1 | "E existe algum ponto da chapa que já tem exatamente a altura média?" → "Mas será que algum ponto da chapa já tem essa altura antes de nivelarmos o morro?" | `sec_b6.py:66` `e existe algum ponto` → `mas será que algum` |
| B6-3 | "Esse é o ponto érre, ésse." → "Em algum lugar desse caminho está o ponto érre, ésse que procuramos." | `sec_b6.py:200` `esse é o ponto` → `em algum lugar desse` |
| B7-2 | "Dois números iguais que somam pi: cada um vale pi sobre dois." → "Se as duas integrais são iguais e somam pi, cada uma vale pi sobre dois." | `sec_b7.py:121` `dois números iguais que` → `se as duas integrais`; `sec_b7.py:124` `cada um vale pi` → `cada uma vale pi` |

Depois de trocar, rode a busca dos gatilhos contra o texto novo: `[gatilho-sem-frase]` = 0 antes de gerar a voz.

**Texto para gravação:** crie `narracao_tags.md` com a seção `## Texto corrido (para gravação)`. Ela contém só os parágrafos `> [...]` da §3 do `narracao.md`, na ordem, sem títulos e sem as linhas **Tela:**.
- Tags permitidas: [curious], [thoughtful], [surprised], [happy], [excited], [serious]. Uma por parágrafo; o S2 tem duas.
- Não use [slowly] nem [pause].
- As letras ficam escritas como a voz deve ler: éfe, gê, cá, xis, ípsilon, érre, ésse, eme, alfa.

Crie também `narracao_limpa.md`, sem tags, para o alinhamento e o `.srt`.

---

## 5. Voz (ElevenLabs v4)

Referência: `docs/roteiro_voz_elevenlabs_v4.md`.

1. Confirme `ELEVENLABS_API_KEY` (primeira parada, §0).
   - Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`.
   - Formato `mp3_44100_192`, decodificado para WAV mono 16 bits 44,1 kHz.
2. Rode primeiro com `--seco`, depois sem ele:

   ```
   uv run --no-sync python videos/gerar_voz_elevenlabs.py videos_longos/yt_0032_propriedades_integral_dupla/narracao_tags.md videos_longos/yt_0032_propriedades_integral_dupla/audio/narracao_v1.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)" --seco
   ```

3. **Uma tomada completa.** Siga com ela. O Kaio ouve em paralelo; se reprovar, regera, e a §6 refaz tudo sozinha. Por isso a sincronização precisa ser automática e reproduzível. A tomada aprovada vira `audio/narracao_final.wav`.
4. `qa/voz.txt`:
   - duração;
   - picos e clipping;
   - silêncio > 1,5 s dentro de um parágrafo;
   - tag lida em voz alta, procurada na transcrição de conferência (`curious`, `thoughtful`, `surprised`, `serious`, `excited`, `happy`);
   - pronúncia certa de "éfe", "gê", "cá", "érre, ésse", "eme", "alfa", "pi", "Riemann", "Fubini" e "Parallax Lab";
   - fronteiras entre blocos sem corte audível.
5. No relatório: modelo, voz, número de blocos, duração e taxa real (palavras ÷ segundos de fala).

---

## 6. Sincronização (a cena segue a voz)

Regras permanentes dos longos:
- WAV contínuo;
- **nunca** cortar a voz por âncora nem inserir silêncio;
- atraso imagem × fala **≤ 0,2 s** (LEAD 0,15 s);
- quando a fala é mais longa que a construção, a espera se divide entre os gatilhos (R10), nunca tudo no fim da âncora.

1. `alinhar_voz.py` → `alinhamento_palavras.json`.
2. `ancoras.json` **gerado por script**: `gerar_ancoras.py` no modo tempo real. Cada âncora começa na primeira palavra do seu trecho (tabela abaixo). Os `self.gat("…")` de cada seção são buscados no alinhamento.
3. **3D:** a linha do tempo do Three.js sai do mesmo `ancoras.json`. Re-renderize os quadros 3D de PB1, PB2, PB3 e PB6, inclusive o rótulo `S` do C12 e o segmento `r` do C6, e rode o QA de alinhamento (≤ 2 px).
4. Rode os lotes 540p e confira:
   - `[gatilho-sem-frase]` = 0;
   - os `[estouro]`, listados com o motivo.

   Estouro > 1 s numa âncora: encurte a animação dentro da regra da caneta (piso de 0,20 s por glifo) ou deixe a âncora seguinte começar mais tarde. **Nunca** acelere a voz.
5. `qa/sync.txt`: o atraso de cada âncora e de cada gatilho do §3 (meta ≤ 0,2 s).
6. **Legenda `.srt`** (`gerar_srt.py`):
   - até 2 linhas × 42 caracteres, de 2 a 5 s por bloco;
   - "Cálculo um" vira "Cálculo I", "cá" vira "k", "éfe" e "gê" viram "f" e "g", "érre, ésse" vira "(r, s)", "eme" vira "m" ou "M" conforme o caso, e "alfa" vira "α";
   - tempo do WAV = tempo do vídeo.

| Âncora | Começa em |
|---|---|
| H1 | "Lembra da chapa de dois metais?" |
| H2 | "Parecem três perguntas diferentes, mas as" |
| A1 | "Fala, pessoal! Bem-vindos ao Parallax Lab!" |
| B1-1 | "Primeiro, as regras do jogo." |
| B1-2 | "Pega a nossa chapa quadrada de" |
| B1-3 | "E olha o que isso dá" |
| B1-4 | "A segunda parte da primeira propriedade" |
| B2-1 | "Agora uma propriedade que parece óbvia" |
| B2-2 | "E a comparação permite descobrir se" |
| B3-1 | "Agora, a primeira pergunta da abertura" |
| B3-2 | "Vamos exagerar: densidade de cem quilos" |
| B3-3 | "Só que aqui precisamos separar o" |
| B4-1 | "Agora, uma consequência surpreendente." |
| B4-2 | "E essa propriedade nasce das anteriores." |
| B5-1 | "Agora voltamos à balança, com a" |
| B5-2 | "E se a parte comum tiver" |
| B5-3 | "E dividir é uma das estratégias" |
| B6-1 | "Agora, a terceira pergunta: a média." |
| B6-2 | "Mas isso acontece com qualquer função?" |
| B6-3 | "E a demonstração é muito bonita," |
| B6-4 | "Agora a parte interessante: o que" |
| B6-5 | "E essa média aparece em muito" |
| B7-1 | "Para fechar, um exemplo que junta" |
| B7-2 | "E agora o valor, sem calcular" |
| S1 | "Então olha o que aprendemos." |
| S2 | "Mas repara numa coisa. Até aqui," |

---

## 7. Conferência 540p com voz (antes do 1080p)

Render de **todos os lotes** em 540p/15 fps com os tempos da voz, e preview com voz. Feche o que falhar antes do 1080p.

**Portões:**
- `FLASH` = 0;
- sobreposição = 0 a cada 0,2 s, também durante os voos;
- margem segura;
- R10 transições = 0;
- R-texto = 0;
- frações `\dfrac` com 26 px ou mais, sem `\tfrac` e sem rótulo girado;
- `\text{}` só para nome de grandeza (`eixo x`/`eixo y` e `no furo` entram nessa lista);
- alinhamento 3D ≤ 2 px;
- palco parado > 6 s = 0 (máscara só do palco);
- `[gatilho-sem-frase]` = 0;
- `qa_canto.py` e `qa_fundo.py` (C18);
- logo em todos os quadros do A1;
- cartão do Fubini ≥ 8 s, com o CTA só em "E conta nos comentários";
- SYNC;
- VOZ.

**Pranchas:**
- `correcoes_final.jpg`: para cada C1–C19, o quadro do erro do v2 (`referencia_final/`) ao lado do quadro corrigido no gatilho.
- Uma prancha com **um quadro de cada âncora no instante da primeira palavra** (26 quadros).
- Lado a lado com os alvos v2 (05, 07a, 09, 10, 11, 12, 13, 14, 16, 18, 20, 22, 23, 24, 26), para confirmar que nada regrediu.

---

## 8. Render final 1080p

1. **Three.js em 1080p** (PB1, PB2, PB3, PB6) com a mesma câmera e a linha do tempo da voz, e QA 3D de novo sobre o 1080p.
2. **Manim em 1080p30** pelo fluxo normal, com `template/config_horizontal.py`.
   - Não configure CRF: o `template/qualidade.py` já usa **14** em renders ≥ 1080p.
   - Não recodifique.
   - Sem teto de tempo de render.
3. **Emenda** com `montar_final.py` (remux, sem reencodar), na ordem PH, PA, PB1, PB2, PB3, PB4, PB5, PB6, PB7, PS.
4. **Master:**

   ```
   uv run python videos/montar_master.py <sem_audio_1080p30.mp4> audio/narracao_final.wav renders/yt_0032_master_final_1080p30.mp4
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
- `.srt` conferido em 5 pontos: início, meio, fim, uma frase longa e o B6-2 (érre, ésse);
- `crf=14.0`;
- `renders/capitulos_final.txt` com os tempos da voz e estes títulos:
  - `A BALANÇA`
  - `BEM-VINDOS`
  - `SOMAR E MULTIPLICAR`
  - `SINAL E COMPARAÇÃO`
  - `A SOLDA NÃO PESA`
  - `MUDAR f SEM MUDAR A INTEGRAL`
  - `DIVIDIR A REGIÃO`
  - `VALOR MÉDIO`
  - `INTEGRAL SEM INTEGRAR`
  - `SÍNTESE E PRÓXIMO`

**Entrega:** `uv run python videos/entregar.py yt_0032` (cópia). A pasta em `entregas/` leva:
- `master`;
- `legenda` (`.srt`);
- `audio/`;
- `texto/`: ficha, `narracao_tags.md`, `narracao_limpa.md`, este handoff e os capítulos;
- `manifesto`.

O número `0032` vai no fim de cada nome. Não há capa. Série, EP e assunto vêm da `ficha.md`: `CÁLCULO III · EP. 07`, `# Propriedades da integral dupla`.

**Na ficha:**
- `3d_threejs:` ganha `b14k`;
- a duração vira a real.

Não rode `entregar.py` se um portão do §7 estiver aberto. Pare e reporte.

---

## 10. Relatório de entrega (obrigatório, e depois pare)

1. Arquivos alterados e criados.
2. C1 a C19, cada um com o caminho do still que prova, e a prancha `correcoes_final.jpg`.
3. Todos os portões do §7 com números reais, a sincronização das 26 âncoras e o QA de voz.
4. Caminhos: WAV, preview 540p com voz, master 1080p, `.srt`, capítulos e a pasta em `entregas/`.
5. Three.js: resolução, custo por quadro no 1080p e alinhamento medido (px).
6. Duração final e taxa real da voz, comparadas com 3 palavras/s.
7. Pendências reais.

Depois do relatório: **pare**. Não faça publicação, capa, commit nem push.

---

## Anexo A · Números congelados

| Grandeza | Valor |
|---|---|
| Balança | 2,472 + 4,584 ≈ 7,06 kg |
| Média da chapa | 7,06/4 ≈ 1,76 kg/m² |
| Camadas | 1 · 4 = 4; 2 · 1,53 ≈ 3,06 (1,53 = 4 − 2,472); total ≈ 7,06 |
| Faixa de estimativa | 4 a 12 kg; 13 kg fora |
| Simetria | ∬x² = ∬y² = 16/3; ∬(x² + y²) = 32/3 |
| Muro de 100 | cota = 100 · área: n = 64 → 0,093 m² → 9,3 kg; 128 → 4,6; 256 → 2,3; 512 → 1,2; 1024 → 0,6 |
| Cordão | m ≈ 6 · 2,25 · 0,01 ≈ 0,135 kg = 135 g; com 1 mm, 0,0135 kg = 13,5 g |
| Sobreposição | faixa 0,2 · 2 = 0,4 m²; 4 + 0,4 = 4,4 m² |
| Média de x² + y² | (32/3)/4 = 8/3 ≈ 2,67; acima = abaixo = 8π/9 ≈ 2,79; r = √(8/3) ≈ 1,63 |
| Extremos | m = f(0,0) = 0; M = f(2,2) = 8 |
| Dois quadrados | (1 + 3)/2 = 2 |
| B7 | eixo x: 1; eixo y: 0; soma = 1; ∬1 = π · 1² = π; cada uma π/2 |
| S2 | massa = 3 · 4 − 2 · área leve; 7,06 = 12 − 2 · 2,472 (= 7,056) |
