# yt_0037 · CÁLCULO III · EP. 12 · Coordenadas polares na integral dupla · HANDOFF FINAL
**Correções de tela (K1–K16) + narração final v3 + voz + sincronização + legenda `.srt` + render 1080p + master + entrega**

Arquivo único e autocontido. Data: 2026-11-15.

**Base:** o preview v2 (16:04,13, 960×540, 15 fps, sem voz), do zip `yt0037_v2_para_gpt`. O v2 cumpriu o handoff v2:
- G1–G8 entraram: tipografia grande, coluna paginada, palco grande, cartão `√π ?` do H2 até o S1;
- a casca do B4-2 com o anel lima inteiro e `2πr · e^(−r²) · dr`;
- o B7 com sec/cossec deduzidos;
- a lupa do B2-2, a homotopia do B3 e o confronto de Gauss.

O Kaio perguntou se já dá para fechar com a narração. **Sim.** O que falta é tela, e nada muda a matemática:
1. um **pulso automático** (os traços acendem e o 3D escurece a cada 2 s de palco ocioso). É efeito não pedido e sai;
2. a **grade recortada em caixa**, que vira grade de tela inteira (regra nova do Kaio);
3. **glifos fantasmas** nos voos e glyph maps;
4. três degraus de conta pulados (`e⁰ = 1`, `sen π = 0`, `(2 cos θ)²/2`);
5. detalhes de canto, caixa vazia, rótulos e a abertura do B6-3;
6. o S1 e o S2 refeitos (alvos novos).

No zip `yt0037_handoff_final_completo.zip` vão:
- este documento;
- `yt_0037_narracao_final_v3.md` (narração final; substitui `yt_0037_narracao_v2_1.md` como fonte do `gerar_ancoras.py`);
- `quadros_do_erro/` (K01–K16 no instante do problema, 960×540, mais quatro tiras de voo) e `00_folha_erros_v2.jpg`;
- `alvos_final/` (`v3_01_H2_promessa_sino.jpg`, `v3_02_S1_paineis_juntos.jpg`, `v3_03_S2_gancho_massa.jpg` + `sb34t3.html`, `shot3.js`).

Onde este documento não diverge, continuam valendo o handoff v1, o handoff v2 (`yt_0037_v1_avaliacao_e_handoff_v2.md`) e os alvos v2.

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
- só `videos_longos/yt_0037_coordenadas_polares/`;
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
2. O WAV passa de **18:30**. Reporte a duração e pare (estimativa: 3.076 palavras a 3 palavras/s ≈ 17:15).

Qualquer outra dúvida: escolha a leitura mais provável, diga qual e siga.

**Ordem:**
1. §3 correções no código, com stills de conferência (sem voz, tempos do v2 como rascunho);
2. §4 narração v3 e busca dos gatilhos;
3. §5 voz;
4. §6 sincronização;
5. §7 conferência 540p com voz;
6. §8 1080p;
7. §9 QA e entrega;
8. §10 relatório.

Pare só depois do relatório. Guarde este arquivo na unidade como `handoff_final.md`, copie `quadros_do_erro/` para `referencia_final/` e `alvos_final/` para `referencia/handoff_final/`.

---

## 1. Estado de partida

- **Unidade:** `videos_longos/yt_0037_coordenadas_polares/` (checkout principal).
- **Código:**
  - `sec_h`, `sec_a`, `sec_b1` … `sec_b7`, `sec_s`;
  - `kit.py`, `v37.py`, `lib37.py`, `pecas37.py`, `p37.py`, `polar37.py`, `v2kit.py`;
  - `threejs/cena3d/c37.js` (`sino`, `casca`, `gauss`);
  - `gerar_ancoras.py` → `ancoras.json`;
  - `qa_v2.py`, `verificacao/verif_numerica.py`.
- **Não reabrir:**
  - a matemática e os números (Anexo A);
  - as contas do v2, degrau por degrau, exceto os três degraus que **entram** (K9, K12, K14);
  - a ordem H1 → H2 → A1 → B1-1 … B7 → S1 → S2;
  - as cores:

    | Uso | Cor |
    |---|---|
    | r | laranja #FF9440 |
    | θ | verde-água #2EE6A6 |
    | r do jacobiano | lima #C6F26B |
    | u | #E08A3C |
    | x | âmbar #FFC24D |
    | y | magenta #EA63FF |
    | f, sino, densidade ρ | ciano #35D9FF |
    | entrada | azul-claro #7FB2FF |
    | saída | coral #FF7A8A |
    | resultado | menta #8CFFD2 |
    | ALERTA | #FF5D5D |

  - os 3D do v2 (sino, casca, gauss, câmeras `CAM_CASCA` e `CAM_GAUSS2`) e a regra G3 (alfa em x ∈ [40, 1010]);
  - o giro de câmera de ~5° no B4-1, as legendas retiradas do B4-2 e o cartão `√π ?` até o S1 (escolhas do v2, aprovadas).
- **sympy:** não instale. `verif_numerica.py` basta.
- **A cena segue a voz.** Os tempos do v2 não valem mais. Todos os lotes, inclusive os quadros do Three.js, são re-renderizados com a linha do tempo da voz.

---

## 2. Avaliação do v2 (resumo)

**Bom e fica:**
- o hook com o sino 3D no quadro 0 e a grade que se curva;
- a lupa do B2-2 e o teste da unidade do B2-3;
- a homotopia do B3;
- a casca andando com o anel lima inteiro;
- o disco grande do B5;
- o confronto entre os dois discos;
- a coluna paginada, com no máximo 6 linhas.

**Hook (H1/H2):** a pergunta é boa, mas dependia de quem viu o EP. 11 ("Lembra da pergunta…"). Na v3 a fala abre pelo próprio sino que está na tela. O H2 passa a **mostrar** a promessa: o sino 2D com `ÁREA = ?` (K3). Quem chega pelo título entende o que vai ganhar.

**Evolução:** a ordem segue como está:

ponto → grade → fator (três caminhos) → teorema → receita → disco → casca → disco deslocado → Gauss → normal → quando não usar → síntese

O que atrapalhava o entendimento era visual (fantasmas, pulso) e os três degraus pulados, não a ordem.

**Gancho final (S2):** o Atlas confirma o próximo, 3.4-T3 **Massa e centro de massa** (EP. 13). Ele abre exatamente no meio disco de raio a com ρ = k r sobre o lápis. O S2 v3:
- usa o mesmo desenho do EP. 13 (mapa radial em **ciano**, a cor da densidade na série);
- diz "ela" (a chapa);
- monta a massa em polares sem calcular: `M = ∫₀^π ∫₀^a (k r) · r dr dθ`. Um r é da densidade e o outro é o jacobiano, o fator deste vídeo. É a ponte entre os dois vídeos.

---

## 3. Correções (lista fechada)

Cada item traz o tempo no preview v2, o arquivo:linha (código de 2026-11-15), o que está errado, a troca, o aceite e o quadro. As linhas podem ter andado alguns números; procure pelo trecho citado.

### K1 · Pulso automático e piscadas (GRAVE: efeito não pedido)
**Tempo:** a cada 2 s de palco ocioso, o vídeo todo. Exemplos: 0:52, 3:32, 11:56, 14:12.
**Quadros:** `K01a`…`K01d`.

**Errado:**
- `v2kit.py:45–95` (`_pulso_v2`, instalado em `v2kit.py:94–95`) e `v2kit.py:125–150` (`_wait_vivo_v2`) fazem todos os traços do palco acenderem num contorno largo e claro. O preenchimento clareia e o 3D perde 32 % de opacidade, a cada 1,6 s.
- O docstring do `v2kit.py:7` diz "o pulso automático sai", mas o código pôs um pulso mais forte.
- O Kaio proíbe efeitos não pedidos.

**Troca:**
1. No fim do `v2kit.py`, depois da linha `_p37.B37.wait = _wait_vivo_v2`, acrescente:
   ```python
   _p37.B37._sem_vivo = True        # FINAL: sem palco vivo automático (nem _pulso_v2, nem _pulso do kit)
   ```
   O `_play_vivo` (`p37.py:926`), o `_wait_vivo` (`p37.py:941`) e o `_wait_vivo_v2` já respeitam `_sem_vivo`.
2. Piscadas escritas à mão que saem:
   - `sec_b3.py:176–183`: as metades "piscam" (`pisca`, `there_and_back`). Troque por **um** `realca(self, mc, mc2, cor=AZC, rt=0.6)` no gatilho "a soma das duas" e um `realca(self, mb, mb2, cor=CORAL, rt=0.6)` logo depois (traço fino que nasce e sai, sem preenchimento).
   - `sec_s.py:146–151`: os anéis piscam em menta, o `?` cresce 1,3× e `acende(c3)`. Esses três somem; o S2 inteiro é refeito no K16.
3. `acende(...)` em texto vira **sublinhado** (`self.sublinha(glifos, rt_vis=1.0)`, traço branco de 2 px, regra do Kaio para a leitura dos símbolos). As chamadas são:
   - `sec_b2.py:309`, `sec_b4.py:148`, `sec_b4.py:271`, `sec_b4.py:400`, `sec_b5.py:92`;
   - `sec_b6.py:102`, `sec_b6.py:154`, `sec_b6.py:155`, `sec_b6.py:419`;
   - `sec_b7.py:168`, `sec_h.py:115`, `sec_s.py:82`.

   No `sec_b6.py:102` (o cartão do canto), simplesmente apague. Os `realca` sobre o **desenho** ficam (um traço na hora do gatilho, sem repetição).

**Palco parado depois do K1:** a regra G7 passa a medir a **tela** (palco + coluna, sem o canto). Parado é nenhum pixel mudando > 8 níveis em mais de 1 % da área.
- Enquanto a coluna está sendo escrita pela caneta, a tela não está parada.
- Trecho de tela parada > 5 s: dê movimento de conteúdo com sentido (a reta-sonda gira, a casca anda, o `a` cresce) ou divida a espera entre os gatilhos (§6).
- **Nunca** use brilho.

**Aceite:**
- `grep -c "_pulso_v2\|vivo-palco" log_*.txt` = 0 na passada final;
- `qa/pulso.txt`: em cada lote, a diferença de luminância média do palco entre quadros consecutivos não tem nenhum ciclo periódico de 1,2–2 s (FFT da série; pico < 3× o ruído);
- tela parada > 5 s = 0.

### K2 · Grade de tela inteira (regra nova do Kaio, 2026-11-15)
**Tempo:** todo o vídeo. Exemplos: 0:40 (hook liso), 5:36 (B3 liso), 14:04 (B7 grade em caixa), 14:53 (S1 liso).
**Quadros:** `K02a`…`K02d`.

**Regra (vale para todo Cálculo):**
- palco com eixos → `papel(v)` **sem** `area`, de borda a borda, nascendo dos eixos e passando por baixo da coluna;
- dois planos na tela (B1-2, B2-2 com a lupa, B3-1 rθ × xy) → cada plano com o seu papel, cada um na **sua metade** (corte vertical no meio da distância entre os dois palcos);
- tela sem gráfico (o 2D do H1/H2 depois do pouso, A1, S1, cartão do S2, CTA) → `papel(passo=0.5)` (quadradinho de 60 px);
- lupa ou painel → fundo opaco próprio (`rgba(30,26,70,.92)`);
- só o 3D Three.js fica liso, e a grade entra no pouso.

**Troca:**
1. `pecas37.py:63–64`:
   ```python
   def papel_v(v, area):
       return papel(v).set_z_index(-10)          # FINAL: tela inteira (o area fica só na assinatura)
   ```
   Isso conserta B1-1, B2-1, B3-2, B5, B6-1, B6-3, B7 e S2 de uma vez.
2. `sec_h.py` (depois do pouso do sino no 2D), `sec_a.py:11`, `sec_s.py` (S1) e o CTA: `self.grade = papel(passo=0.5).set_z_index(-10)` entrando no primeiro play do bloco.
3. `sec_b3.py:82–95` (B3-1, homotopia): papel de `VR` na metade esquerda e de `VD` na direita. Nenhum dos dois existe hoje. Mesma coisa no B1-2 (`sec_b1.py:166–171`) e no B2-2.
4. Os painéis do S1 ganham fundo opaco (alvo `v3_02`).

**Aceite:**
- `qa/grade.txt`: em cada quadro 2D, existe linha de grade a < 40 px das bordas esquerda e direita e a < 40 px do topo e da base, fora do 3D;
- quadros 2D sem grade = 0;
- nenhuma linha de grade por cima de glifo (a grade em z −10).

### K3 · H2: a promessa sem imagem
**Tempo:** 0:44–0:56. **Quadro:** `K03`. **Alvo:** `v3_01_H2_promessa_sino.jpg`.

**Errado:** a fala promete "a área inteira debaixo da curva do sino", mas a tela continua nos dois discos. O `√π ?` entra sem contexto.

**Troca (`sec_h.py:113–130`):**
1. No gatilho "a curva do sino":
   - os dois discos, a seta e as legendas de baixo saem (0,3 s);
   - no mesmo play, o sino 2D é desenhado: `Create`, 1,0 s; eixo x de −3,4 a 3,5 com 250 px/u centrado em x = 960 e base em y = 880; pico em y = 455; `CI`, 5 px; área em `CI` a 25 %;
   - `ÁREA = ?` (Space Grotesk 44 px, branco) dentro da área em (960, 800), pela caneta;
   - `A CURVA DO SINO: DE −∞ A +∞` (30 px, GEO) em (960, 960).
2. A integral dupla fica no alto, em (960, 240).
3. No gatilho "estatística", o cartão `√π ?` entra no canto, como hoje. O `?` do cartão **voa** do `?` de `ÁREA = ?` (`TransformFromCopy`).
4. O sino 2D sai no corte para o A1.

**Aceite:** still no fim do H2 ≈ alvo `v3_01`; o sino com a área visível ≥ 3 s antes do A1.

### K4 · B1-1: palco pequeno e rótulo r longe do segmento
**Tempo:** 1:12–2:07. **Quadro:** `K04`.

**Errado:**
- `sec_b1.py:9` `V1 = Vw(330, 900, 290)`: o triângulo ocupa ~560 px e os 2/3 da direita ficam vazios por ~30 s;
- `sec_b1.py:99`: o rótulo `r = 2` fica a 122 px à esquerda do meio do segmento e encosta no eixo y. O "r" sozinho parece rótulo do eixo.

**Troca:**
1. `V1 = Vw(250, 985, 365)`. O x vai até 816 px. O topo do eixo y fica em 237 px, e o rótulo `y` fica abaixo da linha 3 do canto com ≥ 40 px de folga.
2. `lr`: canto esquerdo em `mh[0] + 22` e centro vertical em `mh[1] + 14`, dentro do triângulo, colado à hipotenusa, com a `placa_min`. O "r" nasce ao lado do segmento e o "= 2" cresce para a direita.

**Aceite:**
- palco ≥ 560 × 740 px;
- R5 (folga 10 px) = 0;
- "r" a ≤ 30 px do segmento laranja.

### K5 · Caixa vazia nos selos PASSO
**Tempo:** 6:52 e 7:24. **Quadros:** `K05a`, `K05b`.

**Errado:** `p37.py:202–205` `poe_selo` desenha a moldura (`Create`, 0,35 s) e **depois** escreve o texto. A caixa fica vazia na tela.

**Troca:**
```python
def poe_selo(sc, sl, extra=()):
    sc.pena(sl[1], extra=list(extra))                 # o texto primeiro, pela caneta
    sc.play(Create(sl[0]), run_time=0.30)             # a moldura fecha em volta do texto pronto
```
No `sec_b3.py:249–251`, o selo `PASSO 4 · CALCULAR` não é escrito e apagado em seguida (o `sai_fim` vem 0,2 s depois). Ele sai daqui: o PASSO 4 vira só a linha 3 do canto do B4-1 (como já é).

**Aceite:** QA `CAIXA VAZIA` **por quadro** (não só ao fim do play) = 0.

### K6 · Canto atrasado na troca de bloco
**Tempo:** 5:36 (B3-1 com o canto do B2) e 7:28 (B4-1 com o subtítulo do B3). **Quadros:** `K06a`, `K06b`.

**Errado:** `secao()`/`subt()` só agendam o `FadeIn` para o próximo play (`kit.py:772–779`).
- No B3-1, são chamados **depois** do primeiro play (`sec_b3.py:92–95`).
- No B4-1 (`sec_b4.py:84–92`), o 3D entra por corte e o primeiro play só vem no gatilho "de volta ao disco".

**Troca:**
- `sec_b3.py`: mova `self.secao("O TEOREMA EM POLARES")` e `self.subt("CADA METADE CUMPRE O TEOREMA")` para **antes** do `self.play(GrowFromPoint(aR…` da linha 92.
- `sec_b4.py`: logo depois do `self.subt("PASSO 4 · CALCULAR")`, faça `self.pena(lx, lz, lag=0.05)` (os rótulos do 3D; o `ly` sai, ver K10). O canto troca no 1º quadro do bloco.
- Regra geral: em todo `an()` que abre bloco novo, a linha 2 e a linha 3 do canto trocam no **primeiro play** do bloco.

**Aceite:** `qa_canto.py`: em cada âncora que troca de bloco, o canto novo está na tela até 0,5 s depois da primeira palavra; quadros com o canto do bloco anterior = 0.

### K7 · Rótulo y encostado no canto (B3-2)
**Tempo:** 6:52. **Quadro:** `K07`.

**Errado:** no B3-2 (`sec_b3.py:198–208`, `VS`, eixo y até 2,15), o `y` fica em y ≈ 164 px, em cima de "A RETA-SONDA SAI DA ORIGEM".

**Troca:** eixo y até 2,0 (`eixos_xy(v, -.1, 2.35, -.1, 2.0, size=40)`). O papel continua de tela inteira.

**Regra para todos os blocos:** rótulo do eixo y com base ≥ 205 px (linha 3 do canto termina em ~165 px).

**Aceite:** R5 texto × canto = 0 no vídeo todo.

### K8 · Fantasmas nos voos e glyph maps (definição das animações)
**Tempo:** 3:28, 4:44, 8:20–8:24, 8:31–8:32, 9:28, 13:36. **Quadros:** `K08a`…`K08f` e as tiras `K08_tira_*.png` (quadro a quadro, 0,5 s).

**Errado:**
1. **Saída do voo:** o `TransformFromCopy` começa exatamente sobre a fonte. Nos primeiros ~0,3 s, fonte e cópia aparecem deslocadas uns pixels e o glifo parece duplicado ("1−1//e" em 8:31, "e^{−1}1" em 8:23,5).
2. **Pouso em negrito:** a cópia herda o contorno da fonte (caneta). No pouso, fica um quadro em negrito (`2π · (1−1/e)/2` em 9:28).
3. **Glyph map com glifo usado duas vezes:** em `sec_b4.py:224–225`, `fo2` e `ba2 + de2` aparecem duas vezes no mapa (o mesmo glifo vira dois). Pior: `loB` (o limite **0**) vira o **1** do `−1/2`. Esse mapeamento é matematicamente falso e some com o K9. O mesmo padrão está em `sec_b6.py:300–301` (`ba5 + de5` duas vezes).

**Troca:**
1. `pecas37.py:338–362` (`voos`):
   - a cópia voa só com preenchimento: `src_c = src.copy().set_stroke(width=0)`;
   - `rate_func=rush_from`: sai rápido da fonte e pousa devagar;
   - `path_arc` com módulo ≥ 0,6 quando o trajeto passa por cima de outra linha.
2. Glifo que aparece duas vezes no destino (o "2" de dois denominadores, o "−" de duas frações): um vem por **voo/mapa** e o outro pela **caneta**. Nunca o mesmo glifo de origem mapeado duas vezes (`copy=True` só para cópia deliberada, um destino por chamada).
3. Durante um glyph map, a linha de origem fica parada e a nova nasce **abaixo** (ou ao lado) sem sobrepor; nenhum glifo em voo cruza a linha de cima por mais de 0,2 s.

**Aceite:**
- `qa/duplicados_por_quadro.txt`: em **todos os quadros** (não só ao fim do play), dois glifos com a mesma forma (mesmo nº de pontos, tamanho ±10 %) e centros a menos de 1/3 do tamanho, por mais de 2 quadros seguidos, = 0. Exclua os 2 primeiros quadros de cada voo;
- glifo com contorno > 0,5 px no pouso = 0;
- prancha `voos_final.jpg` com as mesmas quatro tiras do zip refeitas (cada 0,5 s), sem duplicado visível.

### K9 · B4-1: o degrau e⁰ = 1 (CONTA INTEIRA)
**Tempo:** 8:20–8:27. **Quadro:** `K09`.

**Errado:** `sec_b4.py:217–226` vai de `[−e^{−u}/2]₀¹` direto para `−e^{−1}/2 − (−1/2)`. Pula o G(0) com o valor substituído (`−e⁰/2`) e o `e⁰ = 1`.

**Troca (três linhas no lugar de P3):**

| Linha | Tex | Gatilho (v3) | Como nasce |
|---|---|---|---|
| P3 | `= -\dfrac{\Ci{e^{-1}}}{2} - \Big(-\dfrac{\Ci{e^{0}}}{2}\Big)` | "Em um: menos é elevado" | glyph map do P2: o `1` de cima do colchete vira o expoente `−1`, o `0` de baixo vira o expoente `0`; o resto da primitiva é copiado (`copy=True`) uma vez para cada parcela |
| P4 | `= -\dfrac{1}{2e} + \dfrac{1}{2}` | "menos com menos dá mais" | glyph map do P3: `e^{−1}` → `1/e` (o `e` vai para o denominador), `e⁰` → `1`, `−(−` → `+` |
| P5 | `= \dfrac{1-1/e}{2}\ \approx 0{,}316` | "a metade de um menos" | glyph map do P4 (o `1/2` é posto em evidência); o chip `∫₀¹ e^{−r²} r dr = (1−1/e)/2 ≈ 0,316` nasce dele, como hoje |

`degrau()` em cada linha. Se a coluna passar de 6 linhas, a página 2 começa no P3 (o P1 e o P2 viram o chip da primitiva, como no padrão de paginação do v2).

**Aceite:** CONTAS B4-1 com os 3 degraus e o tempo de cada um; nenhum glifo de origem mapeado duas vezes.

### K10 · B4: "y" solto entre o sino e a coluna
**Tempo:** 7:36–8:48. **Quadro:** `K10`.

**Errado:** `sec_b4.py:91` prende o `y` na ponta do eixo y (`"ey"`, deslocamento 66, −6). A ponta fica **atrás** do sino opaco, e o "y" flutua sozinho a ~90 px de qualquer traço.

**Troca:**
- no B4-1 (sino opaco), o `ly` não entra;
- no B4-2, ele nasce no play em que o sino vira traço, preso a `"ey"` com deslocamento (22, −14) e a ≤ 30 px da ponta visível.

**Aceite:** rótulo de eixo a ≤ 30 px da ponta do eixo **visível**; rótulo de eixo sem eixo visível = 0.

### K11 · B4-2: ALTURA atravessada pela seta do eixo y
**Tempo:** 9:04–9:36. **Quadro:** `K11`.

**Errado:** `sec_b4.py:334–338` (`poe_alt`) põe `ALTURA e^{−r²}` a 40 px da parede. A seta magenta do eixo y passa por cima do texto.

**Troca:** em `poe_alt`, `x_alvo = max(x + 40, x_ey + 30)`, com `x_ey` a coordenada em px da ponta `"ey"` (a mesma do `pal.prende`). Se ainda tocar a seta, a placa vai para baixo da chave, alinhada à esquerda com ela. O R5 v2 conta seta 3D × texto.

**Aceite:** R5 texto × traço do 3D (seta incluída) = 0 em todo o B4-2.

### K12 · B5: dois degraus pulados (CONTA INTEIRA)
**Tempo:** 10:36–11:10.

**Errado:**
- `sec_b5.py:185–198` vai de `∫[r²/2]₀^{2cos θ} dθ` direto para `∫ 2cos²θ dθ`, sem o G(b) − G(a) substituído;
- `sec_b5.py:214` tem `(π/2 + 0) − (−π/2 + 0)`, mas a fala não dizia de onde vem o 0 (`sen π`, `sen(−π)`).

**Troca:**
1. Entre Q1 e Q2, uma linha Q1b:
   ```
   = \displaystyle\int_{-\pi/2}^{\pi/2}\Big(\dfrac{(\Co{2\cos\T})^2}{2}-\dfrac{0^2}{2}\Big)\dt \;=\; \int_{-\pi/2}^{\pi/2}\dfrac{4\cos^2\T}{2}\,\dt
   ```
   - gatilho "Em dois cosseno de teta";
   - o `2cos θ` voa do limite de cima do colchete e o `0` do de baixo;
   - a segunda metade da linha entra em "quatro cosseno ao quadrado".

   O Q2 (`= ∫ 2cos²θ dθ`) entra em "Fica dois cosseno ao quadrado".
2. Q4 continua. No gatilho "que é zero", o `sen π` aparece pequeno (30 px, GEO) sobre o `0` da primeira parcela e sai em 1 s. Faz o mesmo com `sen(−π)` em "mais zero".

**Aceite:** CONTAS B5 com Q1b e os dois "= 0" lidos; coluna ≤ 6 linhas (pagine se preciso).

### K13 · B6-1: "SEM PRIMITIVA ELEMENTAR" encostado na coluna
**Tempo:** 11:40. **Quadro:** `K13`.

**Errado:** `sec_b6.py:108` `leg("SEM PRIMITIVA ELEMENTAR", 600, 318, AL, "left", 30)` termina em x ≈ 975, a 25 px da coluna (X6 = 1000).

**Troca:** `leg("SEM PRIMITIVA ELEMENTAR", 265, 300, AL, "center", 30)`. Fica à esquerda do eixo y, acima da cauda esquerda da curva, que ali está em y ≈ 770.

**Aceite:** texto do palco a ≥ 40 px da coluna.

### K14 · B6-2: o degrau e⁰ = 1 e a tabela
**Tempo:** 12:30–13:10. **Quadro:** `K14`.

**Errado:**
- `sec_b6.py:293–301` vai de `2π[−e^{−r²}/2]₀^b` direto para `2π(−e^{−b²}/2 + 1/2)`, sem `G(0) = −e⁰/2`, e mapeia `ba5 + de5` duas vezes (ver K8);
- `sec_b6.py:336`: `a = 2, CIMA = 3{,}140`, mas π(1 − e^{−8}) = 3,14054…, que arredonda para **3,141**.

**Troca:**
1. Linha C6a nova antes do C6:
   ```
   = 2\pi\Big(-\dfrac{\Ci{e^{-b^2}}}{2}-\Big(-\dfrac{\Ci{e^{0}}}{2}\Big)\Big)
   ```
   - gatilho "Em bê: menos é elevado";
   - o `b` e o `0` voam dos limites do colchete;
   - o C6 entra em "O dois pi multiplica a diferença" e o C7 em "pi vezes um menos é elevado a menos bê".

   Para caber, assim que o C7 estiver escrito, C4–C7 viram o chip `∬_{D_b} = π(1 − e^{−b²})` no alto da página 2 (o resultado voa para o chip). A desigualdade e a tabela vêm abaixo dele.
2. `sec_b6.py:336`: `"3{,}140"` → `"3{,}141"`.

**Aceite:** CONTAS B6-2 com C6a; tabela igual ao Anexo A; coluna ≤ 6 linhas + tabela.

### K15 · B6-3: palco vazio na abertura da curva normal
**Tempo:** 13:30–13:34. **Quadros:** `K15`, `K08e`.

**Errado:**
- `sec_b6.py:379–386`: o papel entra num retângulo vazio (sem eixos visíveis, `K15`) e a curva só vem no gatilho seguinte;
- o rótulo `e^{−x²/2}` nasce como cópia sobre outra cópia (`K08e`).

**Troca:**
- no play da linha 383 entram juntos o papel (tela inteira), os eixos e a curva `Create(d2["c"])` com `FadeIn(sh2)`;
- no gatilho "a curva normal padrão" só o rótulo `lc2` é escrito pela caneta (uma vez).

**Aceite:** palco só com papel ≤ 0,5 s; rótulo sem duplicado (K8).

### K16 · S1 e S2 refeitos (síntese e gancho do EP. 13)
**Tempo:** S1 14:52–15:30, S2 15:32–15:55. **Quadros:** `K16a`, `K16b`. **Alvos:** `v3_02_S1_paineis_juntos.jpg`, `v3_03_S2_gancho_massa.jpg`.

**S1 errado:** `sec_s.py:44–100`: o painel "O FATOR" fica sozinho por ~30 s e os 2/3 da direita ficam vazios. Os painéis 2 e 3 entram nos últimos 5 s.

**S1 troca:**
- no primeiro play do S1, os **três** painéis entram juntos com título e desenho:
  - grade polar com a célula lima;
  - disco em degradê;
  - sino;
- fundo opaco nos painéis, papel(passo=0.5) atrás;
- os resultados entram nos gatilhos de sempre:
  - `dA = r dr dθ` em "o pedacinho de área é", com o ✓ do painel 1;
  - `π(1 − 1/e)` e o ✓ do painel 2 em "o disco deu pi";
  - `∫ e^{−x²} dx = √π`, voando do cartão do canto, e o ✓ do painel 3 em "o sino inteiro deu";
- painéis sem resultado mostram só o título, sem ✓, nunca uma caixa vazia;
- a reta-sonda do painel 1 continua em "os limites saem da";
- `sec_s.py:82` (`acende`) sai.

**S2 troca (`sec_s.py:110–152`, fala v3):**

| Gatilho | Tela |
|---|---|
| "para o próximo vídeo" | painel `NO PRÓXIMO VÍDEO: MASSA E CENTRO DE MASSA` sobe para (1140, 250, 680×250) |
| "mais pesado na borda" | legenda em **ciano** (CI), 32 px |
| "a densidade, rô" | os 40 setores do `sec_s.py:134–136` pintam do centro para a borda em `mixh("#132A44", CI, .10 + .70·r)`, no lugar do lavanda; `ρ = k r` (46 px; ρ e k em CI, r laranja) entra em (1140, 590) |
| "Coloca um lápis" | lápis no centro da base, como hoje |
| "Onde ela equilibra" | reta de simetria x = 0 tracejada branca (2,5 px) da base ao arco; `?` 72 px à direita da reta, em y = 0,45a; `ONDE ELA EQUILIBRA?` (**ela**, a chapa) |
| "a massa já se monta" | `M = ∫₀^π ∫₀^a (k r) · r dr dθ` em (1140, 720), 46 px; o `(k r)` voa do `ρ = k r`; o r lima e o resto pela caneta |
| "Um erre é da densidade" | chave ciano sob `(k r)` + `DENSIDADE` (28 px, CI) |
| "o erre do jacobiano" | chave/guia lima sob o r lima + `JACOBIANO` (28 px, LI), uma linha abaixo |
| "deixa o like" | CTA |

Sem pulso, sem escala no `?`, sem `acende`. O cartão fica ≥ 8 s antes do CTA.

**Aceite:**
- stills do S1 (no "o pedacinho de área é") e do S2 (no "deixa o like") ≈ alvos `v3_02` e `v3_03`;
- `[cartao]` ≥ 8 s;
- nada calcula a massa nem o centro (isso é do EP. 13).

### O que NÃO mexer
- O conteúdo do B2 (setores, arco × lado, jacobiano, teste da unidade), do B3 (metades, receita) e do B7.
- As cenas Three.js e as câmeras (só re-render com a linha do tempo da voz).
- O H1 até "bem maior" (só os gatilhos da fala nova).
- O A1 (só o papel do K2).

---

## 4. Narração final v3

Arquivo: `yt_0037_narracao_final_v3.md` (no zip). Ele substitui a v2.1 como fonte do `gerar_ancoras.py`. Tem **3.076 palavras ≈ 17:15** (revisão v3.1: refino do GPT filtrado, o nome do arquivo não muda).

**O que a v3.1 mudou (só fala; nenhuma tela nem gatilho muda):**
- B5: "somando um **aos** dois lados" (era "dos", erro de digitação); "a origem, erre igual a zero, já está na região"; "Como a função é um, o integrando em polares é só erre", antes da conta da área;
- B4-1: "A de fora só multiplica por dois pi, porque o resultado de dentro não depende de téta";
- B4-2: "e no limite, com cascas cada vez mais finas, a soma vira a integral";
- B6-2: "E o quadrado de á raiz de dois é dois á ao quadrado" (justifica o expoente −2a² da ponta de cima) e "as duas exponenciais vão para zero" antes de "as duas pontas vão para pi";
- S2: "Mas a massa total ainda não diz onde apoiar o lápis: para isso, precisa de uma ideia nova, o centro de massa".
Todos os gatilhos da v3 continuam no texto; o B6-2 "á igual a um / dois / três" são três gatilhos separados ("Com á igual a um", "Com á igual a dois", "Com á igual a três").

**Mudanças:**
- H1 abre pelo sino ("Olha esse sino…");
- H2 cita a estatística;
- B4-1, B5 e B6-2 leem os degraus do K9, K12 e K14;
- S2 do K16.

**Gatilhos que mudam de frase:**

| Arquivo:linha | Antes | Agora |
|---|---|---|
| `sec_b4.py:217` | "em um menos um" | "Em um: menos é elevado" (P3) |
| `sec_b4.py:226` | "a diferença dá a" | "menos com menos dá mais" (P4) e "a metade de um menos" (P5) |
| `sec_b5.py:191` | "dois cosseno ao quadrado de" | "Em dois cosseno de téta" (Q1b), "quatro cosseno ao quadrado" (2ª metade do Q1b), "Fica dois cosseno ao quadrado" (Q2) |
| `sec_b5.py:212` | "em pi sobre dois pi" | "Em pi sobre dois: pi sobre dois" (Q4), "que é zero", "mais zero" |
| `sec_b6.py:293` | "que dá pi vezes a" | "Em bê: menos é elevado" (C6a), "O dois pi multiplica" (C6), "pi vezes um menos é elevado a menos bê" (C7) |
| `sec_h.py:128` | "a área inteira debaixo" | "a curva do sino" (K3), "estatística" (cartão) |
| `sec_s.py:132–151` | (S2 antigo) | os gatilhos da tabela do K16 |

**"téta" (pedido do Kaio, 2026-11-15):** na v3, toda leitura de θ está escrita **téta** (85 ocorrências), para a voz não ler a palavra comum "teta". Troque também os 8 `self.gat("…teta…")` (em `sec_b1.py`, `sec_b2.py`, `sec_b3.py`, `sec_b5.py`) para "téta", e qualquer gatilho novo deste handoff que tenha a palavra. Nenhum `teta` sem acento na fala, nos gatilhos nem no `narracao_tags.md` (`grep -c '\bteta\b'` = 0).

Rode a busca de gatilhos: `[gatilho-sem-frase]` = 0 antes da voz.

---

## 5. Voz (ElevenLabs v4)

Referência: `docs/roteiro_voz_elevenlabs_v4.md`.

1. Confirme `ELEVENLABS_API_KEY` (primeira parada, §0).
   - Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`.
   - Formato `mp3_44100_192`, decodificado para WAV mono 16 bits 44,1 kHz.
2. Gere `narracao_tags.md` e `narracao_limpa.md` a partir da v3 (como no yt_0034). Rode primeiro com `--seco`, depois sem ele:
   ```
   uv run --no-sync python videos/gerar_voz_elevenlabs.py videos_longos/yt_0037_coordenadas_polares/narracao_tags.md videos_longos/yt_0037_coordenadas_polares/audio/narracao_v1.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)" --seco
   ```
3. **Uma tomada completa.** Siga com ela. O Kaio ouve em paralelo; se reprovar, ele regera e a §6 refaz tudo sozinha. A tomada aprovada vira `audio/narracao_final.wav`.
4. `qa/voz.txt` (`qa_voz.py`):
   - duração;
   - picos e clipping;
   - silêncio > 1,5 s dentro de um parágrafo;
   - tag lida em voz alta;
   - fronteiras sem corte audível;
   - pronúncia de:
     - letras: "erre", "téta" (nunca "teta"), "xis", "ípsilon", "á", "bê", "u", "dê u", "dê erre", "dê téta", "rô", "cá";
     - funções: "é elevado a menos, xis ao quadrado mais ípsilon ao quadrado", "é elevado a zero", "secante", "cossecante", "cosseno de dois teta";
     - números: "zero vírgula três um seis", "um vírgula noventa e nove", "três vírgula zero oito", "raiz de dois pi";
     - nomes: "Pitágoras", "Parallax Lab".
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
3. **3D:** a linha do tempo do Three.js sai do mesmo `ancoras.json`.
   - Re-renderize `sino` (PH), `casca` (PB4) e `gauss` (PB6).
   - Rode o QA de alinhamento (≤ 2 px) e o QA dos pousos.
4. Rode os lotes 540p e confira:
   - `[gatilho-sem-frase]` = 0;
   - os `[estouro]`, cada um com o motivo. Estouro > 1 s numa âncora: encurte a animação dentro da regra da caneta ou deixe a âncora seguinte começar mais tarde. **Nunca** acelere a voz.
   - Os atrasos do v2 (+1,5 s em "a de dentro dá", B5; +1,0 s em "a de fora dá", B6-1) entram na meta ≤ 0,2 s.
5. `qa/sync.txt` (`qa_sync.py`): o atraso de cada âncora, de cada degrau das contas e de cada gatilho do §3 (meta ≤ 0,2 s).
6. **Legenda `.srt`** (`gerar_srt.py`):
   - até 2 linhas × 42 caracteres, de 2 a 5 s por bloco;
   - tempo do WAV = tempo do vídeo;
   - trocas:
     - "xis" → x, "ípsilon" → y;
     - "erre" → r, "téta" → θ, "rô" → ρ, "cá" → k;
     - "á" → a, "bê" → b;
     - "pi" → π;
     - "é elevado a" → e^ (só no número de Euler);
     - "Cálculo um" → "Cálculo I".

---

## 7. Conferência 540p com voz (antes do 1080p)

Render de **todos os lotes** em 540p/15 fps com os tempos da voz, e preview com voz. Feche o que falhar antes do 1080p.

**Portões:**
- `FLASH POR QUADRO` = 0;
- **PULSO** = 0 (K1);
- **GRADE** de tela inteira em todo quadro 2D (K2);
- **CAIXA VAZIA por quadro** = 0 (K5);
- **DUPLICADOS por quadro** = 0, inclusive durante voos e glyph maps (K8);
- R5 = 0 a cada 0,2 s:
  - texto × texto;
  - texto × linhas/polígonos;
  - texto × canto (K7);
  - texto × seta/aresta 3D (K11);
  - também durante os voos;
- rótulo de eixo a ≤ 30 px de ponta visível (K10);
- canto: troca no primeiro play de cada bloco; quadros com canto velho = 0 (K6);
- margem segura (≤ 1880 px, ≥ 40 px), rótulos ≥ 26 px, algarismo ≥ 30 px (G1);
- alinhamento 3D ≤ 2 px; pousos sem pisca;
- tela parada > 5 s = 0; a lista de 3 a 5 s vai com a fala ao lado;
- palco vazio ≤ 0,5 s (a vinheta do logo no A1 não conta);
- `[gatilho-sem-frase]` = 0;
- tabela CONTAS com cada degrau, o tempo e a frase que o dispara, incluindo os novos do K9, K12 e K14;
- `qa_canto.py` e `qa_fundo.py`;
- logo em todos os quadros do A1;
- cartão do S2 ≥ 8 s;
- SYNC e VOZ.

**Pranchas:**
- `correcoes_final.jpg`: para cada K1–K16, o quadro do erro (`referencia_final/`) ao lado do quadro corrigido no gatilho do item;
- `voos_final.jpg` (K8);
- uma prancha com **um quadro de cada âncora no instante da primeira palavra** (19 quadros);
- lado a lado com os alvos v2 (`v2_01` … `v2_06`) e os finais (`v3_01` … `v3_03`).

---

## 8. Render final 1080p

1. **Three.js em 1080p** (`sino`, `casca`, `gauss`), com a mesma câmera e a linha do tempo da voz, e QA 3D de novo sobre o 1080p.
2. **Manim em 1080p30** pelo fluxo normal, com `template/config_horizontal.py`.
   - Não configure CRF: o `template/qualidade.py` já usa **14** em renders ≥ 1080p.
   - Não recodifique. Sem teto de tempo de render.
3. **Emenda** com `montar_final.py` (remux, sem reencodar), na ordem dos lotes.
4. **Master:**
   ```
   uv run python videos/montar_master.py <sem_audio_1080p30.mp4> audio/narracao_final.wav renders/yt_0037_master_final_1080p30.mp4
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
  - o degrau `e⁰ = 1` do B4-1;
  - `sen π = 0` do B5;
  - a tabela do B6-2;
  - `√(2π)` do B6-3;
  - fim.
- `renders/capitulos_final.txt` com os tempos da voz:

| Âncora | Título |
|---|---|
| H1 | `A INTEGRAL QUE NÃO COLABORA` |
| A1 | `BEM-VINDOS` |
| B1-1 | `O ENDEREÇO DE UM PONTO` |
| B1-2 | `A GRADE DE CÍRCULOS E RAIOS` |
| B2-1 | `O RETÂNGULO POLAR` |
| B2-2 | `O FATOR É O JACOBIANO` |
| B2-3 | `O TESTE DA UNIDADE` |
| B3-1 | `O TEOREMA EM POLARES` |
| B3-2 | `A RECEITA E A RETA-SONDA` |
| B4-1 | `O DISCO DO COMEÇO` |
| B4-2 | `ANÉIS E CASCAS` |
| B5 | `UM DISCO FORA DO CENTRO` |
| B6-1 | `O SINO INTEIRO (GAUSS)` |
| B6-3 | `A CURVA NORMAL` |
| B7 | `QUANDO USAR POLARES` |
| S1 | `JUNTANDO TUDO` |

**Entrega:** `uv run python videos/entregar.py yt_0037` (cópia).
- O destino tem de ser o `entregas/` do checkout principal.
- A pasta leva:
  - `master`;
  - `legenda` (`.srt`);
  - `audio/`;
  - `texto/`: ficha, `narracao_tags.md`, `narracao_limpa.md`, este handoff e os capítulos;
  - `manifesto`.
- O número `0037` vai no fim de cada nome. Não há capa.
- Série, EP e assunto vêm da `ficha.md`: `CÁLCULO III · EP. 12`, `# Coordenadas polares na integral dupla`.
- **Na ficha:** a duração real e `duracao_alvo` da v3.

Não rode `entregar.py` se um portão do §7 estiver aberto. Pare e reporte.

---

## 10. Relatório de entrega (obrigatório, e depois pare)

1. Arquivos alterados e criados.
2. K1–K16, cada um com o caminho do still que prova, e as pranchas `correcoes_final.jpg` e `voos_final.jpg`.
3. Todos os portões do §7 com números reais, a tabela CONTAS, a sincronização das 19 âncoras e o QA de voz.
4. Caminhos: WAV, preview 540p com voz, master 1080p, `.srt`, capítulos e a pasta em `entregas/`.
5. Three.js: cenas, resolução, custo por quadro no 1080p, alinhamento medido (px).
6. Duração final e taxa real da voz, comparadas com 3 palavras/s.
7. Pendências reais.

Depois do relatório: **pare**. Não faça publicação, capa, commit, merge nem push.

---

## Anexo A · Números congelados

| Onde | Valor |
|---|---|
| B1-1 | r = 2, θ = π/3 → x = 1, y = √3 |
| B2-1/B2-2 | setor ½ r² Δθ; célula ½(r₂² − r₁²)Δθ = r̄ Δr Δθ; células do exemplo 3/4·½·π/6 e 7/4·½·π/6; det = r |
| B2-3 | disco de raio a: ∫₀^{2π}∫₀^a r dr dθ = πa² (sem o r daria 2πa) |
| B4-1 | ∫₀¹ e^{−r²} r dr = −e^{−1}/2 − (−e⁰/2) = (1 − 1/e)/2 ≈ 0,316; disco = π(1 − 1/e) ≈ 1,99 |
| B4-2 | casca 2πr · e^{−r²} · dr; ∫₀¹ 2πr e^{−r²} dr = 2π · (1 − 1/e)/2 = π(1 − 1/e) |
| B5 | x² + y² ≤ 2x ⇔ (x − 1)² + y² ≤ 1; r ≤ 2 cos θ, −π/2 ≤ θ ≤ π/2; θ = π/3 → r = 1; área: ∫(4cos²θ/2)dθ = [θ + sen 2θ/2] = π |
| B6-2 | ∬_{D_b} = π(1 − e^{−b²}); a = 1: 1,986 · 2,231 · 2,716; a = 2: 3,084 · 3,112 · **3,141**; a = 3: 3,1412 · 3,1415 · 3,1416; ∫e^{−x²} = √π |
| B6-3 | ∫e^{−x²/2} dx = √2 · √π = √(2π) |
| B7 | x = 1 ⇒ r = sec θ; y = 1 ⇒ r = cossec θ; corte em θ = π/4; área 1 |
| S2 | ρ = k r; M = ∫₀^π∫₀^a (k r) r dr dθ (não calcular na tela) |

Se algum valor da tela divergir de `verif_numerica.py`, vale o script; reporte.
