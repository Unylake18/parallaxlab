# yt_0030 · CÁLCULO III · EP. 04 · Exercícios do módulo 3.1 · HANDOFF FINAL
**7 correções de tela + voz + sincronização + legenda `.srt` + render 1080p + master + entrega** (arquivo único e autocontido; a narração **v3.3 fechada** está no Anexo A e em `narracao_v33.md` do zip)

2026-11-12. Base: preview v3 (`renders/v3/yt_0030_preview_v3_540p15.mp4`, 1803,87 s ≈ 30:04, 960×540, 15 fps, sem voz), que a Produção assistiu inteiro e aprovou como base. O fechamento visual é **só** a lista fechada do §2 (7 itens). A narração é a **v3.3 fechada** (refino do GPT filtrado pela Produção, Anexo C): 69 parágrafos = as mesmas 69 âncoras, **5.414 palavras ≈ 30:05**, e as **482 frases de sincronia** da cena (459 gatilhos + 23 fins de sublinhado) conferidas por script. Ela **substitui** a v3.2 do `narracao.md` antes de qualquer render (§3.1). Fora a frase de log da leitura 8 (§3.1), nenhuma linha da cena muda por causa dela. Este documento substitui os handoffs v1 a v3 do yt_0030 **no que diverge**. Matemática, números, paleta, caneta, canto, fundo violeta com a grade dos eixos, layouts A/B, os 50 alvos, os 160 glyph maps e o gancho/abertura/escada do v3 seguem como estão.

---

## 0. Autorização, fases e modo de execução

**Fases explicitamente abertas pelo Kaio nesta unidade:** correções (§2), **voz (ElevenLabs v4)**, **sincronização**, **legenda `.srt`**, **render final 1080p**, **master** e **entrega** em `entregas/`. O Kaio pediu para seguir direto: corrigir e já ir para o 1080p e a entrega, **sem** parar para um preview v4 de aprovação.

**Não abertas (não fazer):**
- publicação, capa, `commit`, `push`, `branch`, PR;
- qualquer mudança em `template/`, `assets/`, `pyproject.toml`, `uv.lock`, `AGENTS.md` ou `docs/`.

Só a unidade `videos_longos/yt_0030_exercicios_modulo_31/` pode ser alterada, além de `renders/` e `entregas/`, que são saída, e de **uma entrada nova** em `videos/entregas_registro.json` (§8). Pode **copiar** scripts do yt_0028 para dentro da unidade, sem alterar o yt_0028.

**Modo de execução (importante):** não encerre a vez entre etapas. Depois de lançar um render ou a geração de voz, espere na mesma vez (comando em primeiro plano com timeout de até 10 min por lote, ou laço `until` que consulta o arquivo de saída) e siga direto para a auditoria. Mensagem de progresso não é entrega.

**Só há duas paradas permitidas:**
1. A variável `ELEVENLABS_API_KEY` não existe na sessão. Peça ao Kaio; **nunca** grave a chave em arquivo, commit, log ou relatório.
2. O WAV gerado passa de **32:30**. Reporte a duração e pare: quem decide cortes é a Produção. (Previsto: 5.414 palavras a 3 p/s ≈ 30:05.)

Qualquer outra dúvida: escolha a leitura mais provável, diga qual e siga.

Ordem: **§3.1 instalar a narração v3.3 → §2 correções (com prova de cada uma em 540p sem voz) → §4 voz → §5 sincronização → §6 conferência 540p com voz → §7 render 1080p → §8 QA e entrega → §9 relatório.** Pare só depois do relatório.

Guarde este arquivo na unidade como `handoff_final.md`.

---

## 1. Estado de partida

- **Unidade:** `videos_longos/yt_0030_exercicios_modulo_31/`.
  - Lotes, na ordem do vídeo: **PH, PD1, PD2, PD3, PD3B, PD4, PD5, PA1, PA2, PA4, PA3, PS** (`cena.py`). Sem 3D.
  - Kit: `kit.py`, `v30.py`, `lib30.py`, `alg30.py`, `escada30.py`. Tempos: `tempos.py` lê `narracao.md` (cada parágrafo é uma âncora: **69 âncoras**, `H-1` … `S-3`).
  - Emenda: `montar.py` com a **costura de 0,4 s** entre lotes (os últimos 0,4 s de um lote, depois do fim da fala, são compostos com os primeiros 0,4 s do seguinte). A costura fica no final (§7).
  - QA: `qa_v3.py` e os relatórios de `renders/v3/qa/`.
- **Pipeline de voz:** o do yt_0028 (`videos_longos/yt_0028_limite_continuidade_derivadas_parciais/`). Copie para a unidade e adapte nomes, lotes e caminhos:
  - `alinhar_voz.py` (alinhamento forçado + STT de conferência);
  - a parte "final" de `gerar_ancoras.py` (tempo real da voz), que aqui entra **dentro do `tempos.py`** (§5);
  - `gerar_srt.py`, `render1080.sh`, `montar_preview.py`, `qa_canto.py`, `qa_fundo.py`, `qa_parado.py`, `qa_sync.py`, `qa_voz.py`, `tiras.py`.
- **Não reabrir:**
  - matemática e números (todos já conferidos; SymPy em `verificacao/`);
  - a narração v3.3 (Anexo A), depois de instalada no §3.1: nenhuma palavra muda;
  - a ordem H → A → D1 → D2 → D3 → D3b → D4 → D5 → P2 → A1 → A2 → A4 → A3 → S;
  - cores (CAMPO #2EE6A0/#8CFFD2, x âmbar #FFC24D, y magenta #EA63FF, POS #E08A3C, rot violeta #9C8CFF, div #7FB2FF, LIMA #C6F26B, CORAL #FF7A8A, GEO #B8C4DA), canto, fundo violeta #18143A → #0F0C26 com a grade que nasce dos eixos;
  - nenhum livro, autor ou Atlas na tela ou na fala.
- **A cena segue a voz:** os tempos do preview v3 **não valem mais**. Todos os lotes são re-renderizados com a linha do tempo da voz.

---

## 2. Correções de tela (lista fechada: 7 itens, nada além disso)

Como ler cada item: **onde** (tempo no v3 e arquivo:linha), **o que está errado**, **a correção exata** e **o aceite** (o número que prova). As linhas citadas são as do código que gerou o v3. Se uma linha andou, procure pelo texto citado.

O quadro do v3 que mostra cada erro está na pasta `yt_0030_final_evidencias_v3/` do zip (`c1_…png` a `c7_…png`); copie-a para a unidade como `referencia_final/`.

**Antes de tudo, instale a narração v3.3 (§3.1)**: as provas abaixo já usam os tempos dela.

Antes da voz, prove os 7 itens no 540p sem voz: re-renderize **só** os lotes PH, PD4, PA1, PA4 e PA3 com os tempos de hoje (3 p/s) e rode o QA desses lotes. Os outros lotes mudam só pelo item C4, que se prova no 540p com voz (§6).

### C1 · D4 · Uma nota de instrução apareceu no vídeo (BLOQUEANTE)
- **Onde:** v3 14:34–15:07 (lote PD4, âncora do "item e"). `sec_d4.py:410`.
- **Errado:** a legenda âmbar "NO PALCO: SÓ A COMPONENTE HORIZONTAL P" é a instrução do handoff v2 ("O palco mostra só a componente horizontal P") copiada como texto de tela. "NO PALCO" é palavra de bastidor e não pode aparecer.
- **Correção:** troque só o texto, mantendo posição, cor, tamanho e o resto da linha:

  ```python
  npl = legenda("SÓ A COMPONENTE HORIZONTAL P", 1124, 850, AMB, "left", 24)
  ```

  As linhas 415 (`FadeIn(npl)`), 456 (`FadeOut(npl)`) e 457 (`remove`) não mudam.
- **Varredura obrigatória:** depois da troca, liste todo texto de tela da unidade e procure palavra de bastidor:

  ```
  grep -n -o 'legenda("[^"]*"\|T("[^"]*"\|TC(r"[^"]*"\|leg_mix(\[[^]]*\]' sec_*.py escada30.py | grep -i "PALCO\|NA TELA\|ALVO\|NOTA\|HANDOFF\|TODO\|INSTRU"
  ```

  Esperado: 0 linhas. (O parâmetro `nota=` dos glyph maps não vai para a tela e fica fora dessa busca.) Cole a saída no relatório.
- **Aceite:** quadro em 14:40 (tempo do v3) mostra "SÓ A COMPONENTE HORIZONTAL P" e nada com "NO PALCO". Prova: `qa/c1_d4_legenda.png`.

### C2 · A4 · O painel da direita fica vazio por quase um minuto
- **Onde:** v3 24:20–25:18 (lote PA4, âncoras A4-1 e A4-2). `sec_a4.py:120–169`.
- **Errado:** o painel da direita tem só os eixos durante ~58 s, enquanto a voz fala do "terceiro campo do desafio" e das equações de Cauchy-Riemann. Meio quadro morto. (O handoff v3 pediu esse vazio; a Produção errou e corrige aqui.)
- **Correção:** o painel da direita mostra **o campo ③ do desafio, F = (x² − y², 2xy)**, desde a primeira frase do A4 até "Agora lê como transformação". Aí o campo sai e a morfose começa no mesmo painel, como hoje.
  1. Em `sec_a4.py`, logo depois da linha 124 (`n1 = legenda("UMA MALHA DE QUADRADINHOS", ...)`), crie:

     ```python
     cf = campo30(VR4, F3, -1, 3.5, 0, 4, .5, rmin=0, mmax=6, nome="A4 f₃ (direita, até a morfose)")
     nf = legenda("O TERCEIRO CAMPO DO DESAFIO", 1440, 868, GEO, "center", 28)
     ```

     `F3` e `campo30` já vêm de `lib30` (o D5 usa os mesmos). Limites: x de −1 a 3,5 e y de **0** a 4 (passo 0,5), para que a linha de setas mais baixa fique em y = 800 px, a ≥ 45 px da legenda em 868.
  2. Linha 125: troque o texto do registro para `"A2 → A4 (malha à esquerda; campo ③ do desafio à direita)"`.
  3. Linha 126: o play de entrada passa a ser

     ```python
     self.play(FadeIn(pe), FadeIn(pd), Create(ee), Create(ed), FadeIn(me), FadeIn(n1), cresce_campo(cf, 0.8), FadeIn(nf), run_time=0.8)
     ```

  4. Linhas 143–144 ("o nosso campo é exatamente o quadrado"): o que acende agora é **o campo**, porque "o nosso campo" é ele:

     ```python
     acende(self, [cf], CAMPO2, 1.0)
     ```

     A linha 160 ("e toda função complexa derivável", malha acende) fica como está.
  5. Linha 168 ("agora lê como transformação"): o campo sai **no mesmo play** em que a cópia da malha voa para a direita, terminando nos primeiros 40% do voo. Troque as linhas 169–170 por:

     ```python
     self.add(mv, mk2)
     self.play(FadeOut(cf, rate_func=lambda t: min(1.0, t / 0.4)), FadeOut(nf, rate_func=lambda t: min(1.0, t / 0.4)),
               UpdateFromAlphaFunc(mv, lambda m, a: m.em(1, smooth(a))), UpdateFromAlphaFunc(mk2, lambda m, a: m.em(1, smooth(a))), run_time=1.0)
     cf.clear_updaters()
     self.remove(cf, nf)
     ```

     O play seguinte (a dobra por z^s com `FadeIn(n2)`) não muda. `n2` entra no mesmo lugar de `nf`, que já saiu: sem texto sobre texto.
  6. Docstring do topo do arquivo: troque "painel da direita vazio" por "à direita, o campo ③ do desafio até a morfose".
- **Aceite:**
  - `painel_vazio` = 0 no PA4 (o painel da direita tem conteúdo do primeiro ao último quadro);
  - `sobreposicoes` = 0 no PA4, inclusive nos 25/50/75% do play do item 5 (setas que somem × malha que chega podem se cruzar só enquanto a opacidade das setas cai; texto × texto = 0);
  - `setas_na_chapa` sem seta fora do painel da direita;
  - prova: tira com 4 quadros (A4-1 no meio, "o nosso campo" com o campo aceso, 50% do voo da malha, fim da morfose) em `qa/c2_a4_tira.png`.

### C3 · D4 · O painel do zoom ×10 fica vazio por 8,5 s
- **Onde:** v3 13:43–13:52 (lote PD4, âncora D4-6, "Item d: confere com um zoom… iguais ao modelo linear."). `sec_d4.py:349–366`.
- **Errado:** o painel da direita (moldura `pd`) entra junto com o zoom ×1 e fica vazio até "Aqui, olha: o zoom de dez vezes". É o único `painel_vazio` do QA v3.
- **Correção:** a moldura da direita só entra quando o zoom ×10 entra, e a janela do zoom nasce antes, à esquerda, na frase do episódio passado.
  1. Mova as definições de `lado`, `quadro()`, `qz` e `qg` (linhas 352–361) para **antes** da linha 349.
  2. Linha 349: tire `FadeIn(pd)` do play de entrada:

     ```python
     self.play(FadeIn(pe), cresce_campo(z1, 0.6), FadeIn(oz1), FadeIn(nz1), run_time=0.8)
     ```

  3. Depois da linha 351 (`acende(self, [nz1], CAMPO2, 0.8)`), crie a janela do zoom:

     ```python
     self.play(Create(qz), run_time=0.3)
     ```

  4. Linhas 362–366 ("aqui olha o zoom de dez vezes"): tire o `Create(qz)` daí (já existe) e ponha `FadeIn(pd)` no play do voo:

     ```python
     self.gat("aqui olha o zoom de dez vezes")
     cq = qz.copy()
     self.add(cq)
     self.play(FadeIn(pd), Transform(cq, qg), cresce_campo(z10, 0.8), FadeIn(oz2), FadeIn(nz2), run_time=0.8)
     ```

     O resto (linha 367 em diante: `FadeOut(cq)`, `FadeOut(qz)`, o zoom ×100, o s² cancelado, os quadradinhos) não muda.
- **Aceite:** `painel_vazio` = 0 no PD4; entre "confere com um zoom" e "aqui olha" a metade direita do quadro não tem moldura vazia; a janela `qz` está na tela desde "deixava as setas arrumadinhas". Prova: `qa/c3_d4_zoom.png` (quadros em "confere com um zoom", "arrumadinhas" e no fim do voo).

### C4 · Canto · A linha 2 do canto some por até 2,8 s nas trocas de seção
- **Onde:** medido no v3 (linha 2 do canto sem texto por mais de 0,6 s): 1:18,3 (3,5 s), 13:20,5 (1,5 s), 14:34,5 (2,2 s), 16:26,5 (2,8 s) e 20:11,9 (12,3 s, a escada da P2, sem linha 2). Os intervalos 0:00–0:41,6 (gancho) e 29:26–30:04 (cartão e CTA) são sem canto **de propósito** e ficam.
- **Errado:** `secao()` (`kit.py:750` e `_secao_n` em `lib30.py:690`) tira a linha antiga e deixa o `FadeIn` da nova pendurado em `self._pend`, que só entra no próximo `play`. Quando o próximo passo é um `gat()` que espera a frase, o canto fica sem título durante toda a espera.
- **Correção:**
  1. Em `kit.py`, no `gat()` (linha 668), antes do `self.wait(...)`: se houver pendência e houver tempo, toque a pendência já:

     ```python
     if self._pend and alvo - self.nq >= round(0.3 * FPS) + 1:
         anims, self._pend = self._pend, []
         self.play(*anims, run_time=0.3)
     ```

     (Coloque isso depois do cálculo de `alvo` e antes do `if alvo - self.nq >= 1: self.wait(...)`.) Faça o mesmo no `ate()` (linha 680).
  2. P2 (início do lote PA1, antes da escada das aplicações): `self.secao("PARTE 2")`. No `S` (resumo) a linha 2 "RESUMO" já existe.
- **Aceite:** `qa_canto.py` (do yt_0028, adaptado) mede a linha 2 do canto a cada quadro: **nenhum trecho > 0,6 s sem linha 2**, fora o gancho (H) e o cartão + CTA (fim do S). Liste os trechos que sobrarem com o motivo. A sincronização (§5) continua ≤ 0,2 s: o play de 0,3 s só acontece quando sobra espera.

### C5 · A3 · O topo das curvas 1/r e 1/r² é um patamar reto
- **Onde:** v3 26:54–27:22 (gráfico de 1/r) e 28:26–28:58 (1/r² com 1/r tracejado). `sec_a3.py:23`.
- **Errado:** `min(f(r), 2.6)` corta a curva no teto e desenha um segmento horizontal grudado no alto do eixo. Parece um degrau que a função não tem.
- **Correção:** a curva **começa** no ponto em que f(r) = 2,6 (nunca é achatada). Troque o laço das linhas 20–23 por:

  ```python
  r0 = 1 / 2.6 if f(.5) == 2.0 else 1 / math.sqrt(2.6)        # 1/r: r0 = 0,3846 · 1/r²: r0 = 0,6202
  pts = []
  for i in range(201):
      r = r0 + i / 200 * (4.0 - r0)
      pts.append(PX(gx + (r / 4) * gw, gy - f(r) / 2.6 * gh))
  ```

  (Se preferir, identifique a curva por um terceiro campo da tupla `curvas` em vez do teste `f(.5) == 2.0`; o que importa é r0 exato para cada função.)
- **Aceite:** em 27:00 e 28:30 (tempos do v3) cada curva toca o teto do gráfico em um ponto só, sem trecho horizontal; a tracejada 1/r continua acima da 1/r² para r > 1. Prova: `qa/c5_a3_graficos.png` (os dois gráficos ampliados 2×).

### C6 · A3 · "COULOMB · GRAVITAÇÃO" com um buraco no meio
- **Onde:** v3 28:26 em diante. `sec_a3.py:244`.
- **Errado:** "· GRAVITAÇÃO" está fixo em x = 1290, ~45 px depois do fim de "COULOMB". Lê-se como duas legendas soltas.
- **Correção:**

  ```python
  c0 = legenda("COULOMB", 1124, 450, GEO, "left", 26)
  cl = [c0, legenda("· GRAVITAÇÃO", c0.get_right()[0] * 120 + 960 + 10, 450, GEO, "left", 26)]
  ```

  (A mesma conta de px já usada em `sec_h.py` para o título da abertura.) A entrada em dois tempos ("a de coulomb" → "e a da gravitação") continua.
- **Aceite:** espaço entre o B de COULOMB e o ponto · = 10 ± 2 px, mesma linha de base. Prova: recorte em `qa/c6_a3_coulomb.png`.

### C7 · Abertura · 12 s de tela vazia abaixo do título
- **Onde:** v3 0:42–0:54 (lote PH, âncora A-1, "Fala, pessoal! Bem-vindos ao Parallax Lab! … só com exercícios."). `sec_h.py:161–178` e 196.
- **Errado:** depois que o título é escrito, a tela fica só com logo e título até "vai ser uma escada". Com o palco vazio, a abertura perde o ritmo que o gancho criou.
- **Correção:** a silhueta da escada aparece em traço fraco logo depois do título, e cada degrau depois **acende por cima** da sua silhueta, como hoje.
  1. Mova as linhas 174–176 (`D = [...]`, `Ap = [...]`, `p1, p2 = titulos_escada()`) para logo depois da linha 162 (`self.remove(self.wm)`) e, em seguida, crie e toque as silhuetas, **sem gatilho novo** (entram assim que o título termina de ser escrito, ~1 s depois de "Fala, pessoal"):

     ```python
     fant = VGroup(*[d.caixa.copy() for d in D], *[a.caixa.copy() for a in Ap])
     for f, d in zip(fant, [*D, *Ap]):
         f.set_fill(opacity=0).set_stroke(d.cor, 3 / 1.2, 0.30)
         f._sem_contorno = True
     fant.set_z_index(-1)
     self.play(LaggedStart(*[Create(f) for f in fant], lag_ratio=0.08), run_time=1.2)
     ```

     Só a moldura, sem ícone e sem texto, na cor de cada degrau a 30% de opacidade, abaixo dos degraus reais. Os sublinhados de "quarto episódio" e "o integrador do módulo" (linhas 172–173) continuam depois disso, nas mesmas frases.
  2. Os degraus reais entram exatamente como hoje (linhas 177 em diante), por cima das silhuetas.
  3. Linha 196: inclua `fant` no `resto`, para sair no mesmo play em que o degrau DOIS FILMES vira o palco do D1.
  4. Marque `fant` como fantasma no QA de sobreposição (como os `fantasma(...)` do D4), para não contar moldura × degrau.
- **Aceite:** em 0:45 (tempo do v3) a silhueta inteira da escada (6 degraus + 4 aplicações) está na tela; `palco_parado` e `holds` do PH sem trecho novo; `sobreposicoes` = 0 (texto × texto). Prova: `qa/c7_abertura.png` (quadros em "bem-vindos", "vai ser uma escada" e "pausa o vídeo e tenta").

### O que NÃO mexer (aprovado como está)
Gancho (filmes, fórmulas fora de ordem, caixas alinhadas com os palcos de cima), escada da abertura/P2/resumo, D1 (o painel da direita só com os eixos durante o enunciado é proposital: é o "pausa e tenta"), D2, D3 (α, quadradinhos, origem, giro de 90°), D3b, D4 (limite ε-δ com o disco, os carimbos DOMÍNIO/LIMITE/IGUAL À SETA, parciais, o zoom ×100, a classe C¹), D5 (chaves P/Q, derivadas até a célula, as três lembranças do gancho, "A TABELA FALA DO PONTO"), P2, A1, A2 (a gota na hipérbole, Laplace), A4 depois da morfose (Mercator), A3 fora C5/C6, resumo com as trocas de rótulo, cartão 8 × 16 kg e CTA. Nenhuma outra mudança de layout, cor, texto ou tempo.

---

## 3. Narração final (texto para gravação)

### 3.1 Instalar a v3.3 (primeiro passo do handoff, antes da C1)
1. `narracao.md` atual → copie para `narracao_v32.md` (arquivo histórico; nada lê dele).
2. Copie `narracao_v33.md` do zip por cima de `narracao.md`. Mesmo formato de sempre: título `#`, 14 cabeçalhos `### <bloco> · <título>` e os parágrafos separados por linha em branco. O Anexo A deste arquivo é o mesmo texto, sem os cabeçalhos.
3. Copie `confere_frases_v33.py` e `frases_sincronia_v33.json` do zip para a unidade e rode `uv run --no-sync python confere_frases_v33.py`. Saída exigida: `âncoras 69 · frases 482/482 · faltando 0 · palavras 5414` (código de saída 0). Ele usa a mesma tokenização da cena (`\w+` em minúsculas, **com** acento). Se faltar alguma, a cópia saiu errada: não edite frase de gatilho na cena.
4. `python tempos.py`: total **5414 palavras = 1804,7 s = 30:04,7**.
5. Única linha de código ligada à narração: em `sec_d3b.py:65`, troque o texto de log da leitura 8 de `"P com xis pequeno embaixo é a derivada parcial de P em relação a xis"` para `"fi com xis pequeno embaixo é a derivada parcial de fi em relação a xis"`. A fala mudou porque o sublinhado cai no índice de `φ_x` (a tela mostra `ÍNDICE = DERIVADA: φ_x = ∂φ/∂x`); o sublinhado e o `ate="calcula o rotacional"` ficam como estão.
6. No log do primeiro render 540p (as provas do §2), `[gatilho-sem-frase]` = 0. As 23 frases `ate=` usam `falta()`, que também imprime `[gatilho-sem-frase]` se não achar a frase.

### 3.2 Texto para gravação
- Fonte única: `narracao.md` da unidade (v3.3). O Anexo A deste arquivo é o mesmo texto (69 parágrafos, 5.414 palavras, conferido parágrafo a parágrafo).
- Gere `narracao_tags.md` por script a partir do `narracao.md`: título `# yt_0030 · narração com tags ElevenLabs v4 (v3.3 fechada)`, depois `## Texto corrido (para gravação)` e os 69 parágrafos na ordem, **sem** os cabeçalhos `###`, com as tags `[ ]`. Gere também `narracao_limpa.md` (o mesmo sem as tags).
- As 22 leituras de símbolo (Anexo B do `handoff_v3.md`) já estão no texto, cada uma no mesmo parágrafo (a 8 agora diz "fi com xis pequeno embaixo…"). Não acrescente nem tire nenhuma.
- Tags usadas: `[thoughtful]` 33, `[curious]` 26, `[excited]` 9, `[thoughtful, emphatic]` 6, `[happy]` 3. Nenhuma tag nova.

---

## 4. Voz (ElevenLabs v4)
Referência: `docs/roteiro_voz_elevenlabs_v4.md`.
1. Confirme `ELEVENLABS_API_KEY` na sessão (primeira parada permitida, §0).
   - Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`.
   - Formato `mp3_44100_192`, decodificado para WAV mono 16 bits 44,1 kHz.
2. Rode primeiro com `--seco` (só mostra os blocos, sem gastar crédito):

   ```
   uv run --no-sync python videos/gerar_voz_elevenlabs.py videos_longos/yt_0030_exercicios_modulo_31/narracao_tags.md videos_longos/yt_0030_exercicios_modulo_31/audio/narracao_v1.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)" --seco
   ```

   Depois, a geração de verdade, sem `--seco`.
3. **Uma tomada completa.** Siga com ela. O Kaio ouve em paralelo; se reprovar, regera, e a §5 refaz tudo sozinha. Por isso a sincronização precisa ser **automática e reproduzível**. A tomada aprovada vira `audio/narracao_final.wav` (cópia).
4. **Checagens automáticas do WAV** (`qa_voz.py` → `qa/voz.txt`):
   - duração (parada 2 se > 32:30);
   - picos e clipping;
   - silêncio > 1,5 s dentro de um parágrafo;
   - **tag lida em voz alta**: na transcrição de conferência (`alinhar_voz.py --stt`), procure `curious`, `thoughtful`, `emphatic`, `excited`, `happy`;
   - pronúncia, pela transcrição: "Parallax Lab", "Cálculo três", "fi", "nabla", "alfa", "épsilon", "delta", "ípsilon", "cê um", "Schwarz", "Cauchy-Riemann", "Laplace", "Mercator", "Groenlândia", "Ampère", "Gauss", "Coulomb";
   - fronteiras entre blocos sem corte audível.
5. Registre no relatório: modelo, voz, versão do texto, número de blocos, duração e taxa real (palavras ÷ segundos de fala).

---

## 5. Sincronização (a cena segue a voz)
Regras permanentes dos longos:
- **WAV contínuo**;
- **nunca** cortar a voz por âncora nem inserir silêncio;
- **atraso imagem × fala ≤ 0,2 s** (o `LEAD` do `kit.py` é 0,09 s);
- cena parada esperando a voz, só com informação na tela.

1. **Tempo por palavra:** `alinhar_voz.py` → `alinhamento_palavras.json` (alinhamento forçado de `texto_narracao.txt`, que sai do `narracao_tags.md`, com o WAV).
2. **`tempos.py` no modo voz real** (sem mexer na cena: os lotes já pedem gatilho por frase). Quando `alinhamento_palavras.json` e `audio/narracao_final.wav` existirem, `ANC_DADOS` sai do alinhamento, **no mesmo formato de hoje** (`ini`, `fim`, `dur`, `fala`, `t`, `bloco`, `palavras`). Copie a lógica da parte "final" do `gerar_ancoras.py` do yt_0028:
   - âncora = parágrafo (as 69 de hoje, mesmos ids);
   - `ini` = início da primeira palavra do parágrafo − 0,15 s (a primeira âncora começa em 0);
   - `fim` = `ini` da âncora seguinte (contínuo); a última termina 1,0 s depois do fim do WAV;
   - `t` = início real de cada token, relativo ao `ini` (mesma tokenização `\w+` em minúsculas do `tempos.py`; `assert` de que a sequência de tokens do alinhamento é igual à do texto);
   - grave `ancoras.json` como cópia de conferência. Nada de tempo à mão.
3. **Costura de 0,4 s:** cada lote termina com 0,4 s de saída depois do `fim` da sua última âncora, e o `montar.py` sobrepõe esses 0,4 s aos primeiros 0,4 s do lote seguinte. Confira, no `lotes_*.json` que o `montar.py` grava, que o quadro absoluto de início de cada lote = `ini` da primeira âncora do lote × fps, **±1 quadro**. Se não bater, o erro acumula 0,4 s por emenda: corrija antes de seguir.
4. Rode os 12 lotes em 540p/15 e confira no log:
   - `[gatilho-sem-frase]` = 0;
   - os `[estouro]`, listados com o motivo (a animação é mais longa que a fala). Estouro > 1 s numa âncora: encurte a animação dentro da cadência da caneta (piso 0,20 s/glifo) ou deixe a âncora seguinte começar mais tarde. **Nunca** acelere a voz.
5. **Relatório de sincronização** (`qa_sync.py` → `qa/sync.txt`): para as **69 âncoras**, os **459 gatilhos** e os **23 fins de sublinhado**, o atraso entre a palavra e o evento visual (meta ≤ 0,2 s), com a lista do que passar disso. Inclua os 22 sublinhados de leitura e os 10 PAUSE E TENTE do v3.
6. **Legenda `.srt`** (`gerar_srt.py`):
   - até 2 linhas × 42 caracteres;
   - de 2 a 5 s por bloco;
   - na legenda: "Cálculo três" vira "Cálculo III" e "cê um" vira "C¹"; o resto fica como falado;
   - tempo do WAV = tempo do vídeo.

   Longos não têm legendado embutido: o master é o único vídeo final.

A tabela das 69 âncoras (primeiras palavras, palavras e início estimado a 3 p/s) está no Anexo B.

---

## 6. Conferência 540p com voz (antes do 1080p)
Render dos **12 lotes** em 540p/15 com os tempos da voz, emenda com o `montar.py` (costura de 0,4 s) e preview com voz (`montar_preview.py` com o WAV) em `renders/final/yt_0030_preview_final_540p15_voz.mp4`. Rode **todos** os portões e feche o que falhar antes do 1080p:

| Portão | Meta |
|---|---|
| Os 7 itens do §2 | cada aceite cumprido, com a prova no `qa/` |
| Prancha dos alvos (`comparar.py`, `RODADA=final`) | os 50 alvos dentro da tolerância de hoje (≤ 4 px a 1080p) |
| Glyph maps | ≥ 160; `TransformMatchingShapes` = 0 |
| Sem origem (R11) | 0 |
| R12 / R13 | 0 / ≤ 5 linhas + enunciado |
| Sobreposições | 0, inclusive em 25/50/75% de cada transição e durante os voos |
| Margens | 0 texto cortado |
| `FLASH` (caneta) | 0 |
| `holds` > 6 s | só com informação na tela e fala seguindo (liste) |
| `palco_parado` > 8 s | 0 |
| `painel_vazio` > 2 s | 0 (o v3 tinha 1; C2 e C3 zeram) |
| Canto (`qa_canto.py`, C4) | linha 2 nunca some > 0,6 s fora de H e do cartão/CTA |
| Fundo (`qa_fundo.py`) | violeta + grade em todos os lotes |
| Leituras | 22/22 com sublinhado no gatilho |
| PAUSE E TENTE | as 10 do v3, cada uma na sua frase |
| `[gatilho-sem-frase]` | 0 (e `confere_frases_v33.py` 482/482) |
| SYNC (`qa/sync.txt`) | atraso ≤ 0,2 s |
| VOZ (`qa/voz.txt`) | sem borda abrupta, sem silêncio inserido, sem tag lida |

Monte também uma **prancha com um quadro de cada âncora no instante da primeira palavra** (69 quadros, `qa/prancha_ancoras.jpg`), para ver se a imagem certa está na tela quando a fala começa.

---

## 7. Render final 1080p
1. **Manim em 1080p30, sem perdas:** `render1080.sh` (copiado do yt_0028) para os 12 lotes, com **`CRF=0`** no ambiente. Motivo: a costura de 0,4 s compõe quadros e obriga a codificar a emenda uma vez; com os lotes sem perdas, o vídeo final passa por **uma única** compressão em CRF 14 (o AGENTS permite `CRF=0` como fonte sem perdas). Sem modo leve: não há teto de tempo de render.
2. **Emenda com a costura em 1080p:** adapte o `montar.py` para `montar1080.py`:
   - entrada `media1080_<C>/videos/cena/1080p30/<C>.mp4`, na ordem PH, PD1, PD2, PD3, PD3B, PD4, PD5, PA1, PA2, PA4, PA3, PS;
   - `K = 12` quadros (0,4 s a 30 fps);
   - fundo da composição em 1920×1080 (se `assets/calculo/` não tiver o PNG liso nessa resolução, gere uma cópia **local na unidade**; não toque em `assets/`);
   - saída `renders/yt_0030_sem_audio_1080p30.mp4` em **libx264, yuv420p, CRF 14, preset `slow`**, gravando o `crf=14.0` no stream;
   - grave `renders/lotes_final_1080.json` (quadro de início de cada lote) e repita a conferência do §5.3 a 30 fps.
3. **Master:**

   ```
   uv run python videos/montar_master.py videos_longos/yt_0030_exercicios_modulo_31/renders/yt_0030_sem_audio_1080p30.mp4 videos_longos/yt_0030_exercicios_modulo_31/audio/narracao_final.wav videos_longos/yt_0030_exercicios_modulo_31/renders/yt_0030_master_final_1080p30.mp4
   ```

   A voz é colada **sem recompressão do vídeo**. Confira:
   - 1920×1080, 30 fps;
   - duração do master = WAV + 1,0 s (a cauda da última âncora);
   - `crf=14.0`, com o comando do AGENTS: `uv run python -c "import av,re;c=av.open('ARQ.mp4');d=b''.join(bytes(p) for _,p in zip(range(4),c.demux(c.streams.video[0])));print(re.search(rb'crf=([0-9.]+)',d).group(1))"`.
4. Depois que o master passar no §8, apague os lotes 1080p sem perdas (`media1080_*`) **desta** unidade. Se o disco apertar antes, apague só PNGs e renders 540p **desta** unidade já auditados. Nada de limpeza ampla.

---

## 8. QA final e entrega
- **QA completo no vídeo final** (obrigatório no fechamento):
  - os portões do §6 sobre o 1080p (amostragem por lote; a prancha dos 50 alvos roda inteira, porque os alvos são 1080p);
  - A/V: voz contínua, sem clipping, sem corte, imagem e voz começando juntas;
  - `.srt` aberto e conferido em 5 pontos: início, meio, fim, uma frase longa e uma leitura de símbolo (a do "nabla dois fi" no A2);
  - `crf=14.0`;
  - capítulos (`renders/capitulos_final.txt`) com os tempos da voz, um por bloco: `0:00 TRÊS FILMES, TRÊS FÓRMULAS` (H) · `BEM-VINDOS` (A) · `MESMA FÓRMULA, DOIS FILMES` (D1) · `DESENHAR SEM MIL SETAS` (D2) · `A FAMÍLIA DE REDEMOINHOS` (D3) · `DUAS REGRAS` (D3b) · `O CAMPO QUE NÃO MELHORA DE PERTO` (D4) · `O DESAFIO` (D5) · `APLICAÇÃO · O RIO` (P2) · `APLICAÇÃO · ÁGUA BATENDO NA PAREDE` (A2) · `APLICAÇÃO · MAPAS QUE NÃO ENTORTAM` (A4) · `APLICAÇÃO · POR QUE 1/r E 1/r²` (A3) · `RESUMO E PRÓXIMO VÍDEO` (S). Cada capítulo começa no `ini` da primeira âncora do bloco.
- **Registro da entrega:** acrescente em `videos/entregas_registro.json` (só esta entrada, como a do yt_0028):

  ```json
  "yt_0030_exercicios_modulo_31": {"serie": "CÁLCULO III", "ep": 4, "assunto": "Exercícios do módulo 3.1", "numero": "0030", "master": "videos_longos/yt_0030_exercicios_modulo_31/renders/yt_0030_master_final_1080p30.mp4"}
  ```

  Sem isso o `entregar.py` usaria o título longo da ficha.
- **Entrega:** `uv run python videos/entregar.py yt_0030 --dry-run` e depois `uv run python videos/entregar.py yt_0030` (cópia; não move nem apaga). Pasta esperada: `entregas/Cálculo III - EP 04 - Exercícios do módulo 3.1 - 0030/` com:
  - `master - 0030.mp4`;
  - `legenda - 0030.srt`;
  - `audio/` (WAV final);
  - `texto/` (ficha, `narracao_tags.md`, `narracao_limpa.md`, este handoff, capítulos);
  - `manifesto - 0030.json`.

  Sem capa.
- **Ficha:** acrescente em `## Estado` a linha do fechamento (data, WAV, duração, master, `.srt`, pasta de entrega) e troque `duracao_alvo` pela duração real.
- Não rode `entregar.py` com uma versão que reprove um portão do §6. Se algum portão ficar aberto, pare e reporte qual e por quê; a entrega assim mesmo só acontece se o Kaio autorizar.

---

## 9. Relatório de entrega (obrigatório, e depois pare)
1. Arquivos alterados e criados: código (com as linhas de cada item C1–C7 e a linha da leitura 8), `narracao.md` v3.3 e `narracao_v32.md`, `tempos.py`, `narracao_tags.md`, `narracao_limpa.md`, `ancoras.json`, `.srt`, ficha, registro de entregas.
2. Os itens C1 a C7, cada um com o caminho da prova e o número do aceite. O resultado da varredura de texto de bastidor (C1).
3. Verificações e resultados: todos os portões do §6 com números reais (antes no 540p com voz, depois no 1080p), a sincronização das 69 âncoras e dos gatilhos, o QA de voz.
4. Caminhos: WAV, preview 540p com voz, master 1080p, `.srt`, capítulos e a pasta em `entregas/`.
5. Custo de render por lote (540p e 1080p) e o tamanho dos lotes sem perdas.
6. Duração final e taxa real da voz (palavras ÷ segundos), comparadas com a estimativa de 3 palavras/s (30:05).
7. Pendências reais (estouros de âncora, exceções de portão).

Depois do relatório: **pare**. Sem publicação, capa, commit ou push.

---

## Anexo A · Narração v3.3 fechada com tags (texto para gravação; idêntico ao `narracao.md` v3.3, sem os cabeçalhos)

69 parágrafos · 5.414 palavras · ≈ 30:05 a 3 palavras/s. Cada parágrafo é uma âncora (Anexo B). O que mudou da v3.2 e por quê: Anexo C.

**Texto corrido** (o `narracao_tags.md` sai do `narracao.md`, não deste anexo)

[curious] Três quadradinhos de fluido, três resultados diferentes. Um só entorta. Outro gira, encolhe e entorta, tudo ao mesmo tempo. E, no terceiro campo, um gira sem crescer e o outro cresce sem girar. Embaixo, três fórmulas, fora de ordem. [thoughtful] A pergunta é: dá para saber qual fórmula faz qual filme só olhando para ela, antes de soltar o fluido? Dá. E hoje é você que vai fazer isso. [excited] Depois, a gente vai usar exatamente as mesmas contas para investigar uma pergunta de física: por que o campo magnético de um fio enfraquece com um sobre a distância, e o campo de uma carga, com um sobre a distância ao quadrado? Não é decoreba. É o rotacional e o divergente, junto com a simetria, que ajudam a escolher a lei.

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Esse é o quarto episódio da nossa série de Cálculo três, e hoje é dia de colocar a mão na massa: o integrador do módulo, só com exercícios. [thoughtful] Vai ser uma escada: cada degrau prepara o seguinte. Vamos ler uma fórmula de dois jeitos, desenhar um campo, explorar uma família de redemoinhos, descobrir duas regras, enfrentar um campo que não melhora de perto e, no topo, o desafio do episódio passado: prever o quadradinho. [curious] Depois, as aplicações: um rio, um jato numa parede, mapas que não entortam e as leis do um sobre a distância. [happy] Então pega papel e caneta. A cada enunciado, pausa o vídeo e tenta antes da resolução.

[thoughtful] Primeiro degrau. Uma função recebe dois números e devolve outros dois: na primeira coordenada, a soma dos dois; na segunda, a diferença. Na tela: fi de u, v igual a u mais v, u menos v. Fi é só o nome da função. Primeiro, como transformação. No plano da esquerda fica o ponto de partida; no da direita, onde ele vai parar. Três itens: a imagem de uma reta, de um quadrado e de um círculo. Pausa o vídeo e tenta.

[curious] Primeiro, o eixo horizontal da esquerda, onde o segundo número é zero. Aí a soma e a diferença ficam iguais ao primeiro número. As coordenadas de saída são iguais. O eixo vai parar na diagonal.

[thoughtful] Agora o quadrado de lado um. Como a transformação é linear, ela leva segmento em segmento: basta transformar os quatro cantos. A origem fica parada. O canto um, zero: a soma dá um mais zero, e a diferença, um menos zero. Ele vai para um, um. O canto um, um vai para dois, zero. E o canto zero, um vai para um, menos um. Liga os pontos: apareceu outro quadrado, inclinado quarenta e cinco graus, com lado raiz de dois. O lado mede a distância até o ponto um, um. A área era um; agora é raiz de dois ao quadrado: dois. E olha a ordem dos cantos: antes percorriam a figura no sentido anti-horário; depois, no horário. O quadrado foi espelhado. Não foi só rotação.

[curious] E um círculo em volta da origem? Soma ao quadrado mais diferença ao quadrado. Abre os dois quadrados: num aparece mais duas vezes o produto; no outro, menos. Esses termos cruzados se cancelam, e sobra duas vezes a soma dos quadrados das coordenadas. Então a distância até a origem fica multiplicada por raiz de dois, e o círculo vira um círculo com o raio multiplicado por raiz de dois. E, como a área vai com o quadrado do raio, ela também dobra.

[thoughtful] Agora a mesma fórmula, lida como campo. A setinha em cima do F diz que o resultado é um vetor. Em cada ponto do plano, você pendura a seta com a soma e a diferença das coordenadas. No eixo horizontal, a coordenada vertical é zero, então as duas componentes ficam iguais: à direita da origem, as setas saem na diagonal, para cima. No eixo vertical, a seta é a coordenada vertical e menos ela: em cima da origem, as setas apontam para a direita e para baixo; embaixo, para a esquerda e para cima.

[curious] E aqui fica uma pergunta para o topo da escada. Como transformação, a área dobrou. Como campo, se a gente soltar um pedacinho de fluido nessas velocidades, a área dele também dobra? Guarda o seu palpite.

[thoughtful] Segundo degrau: desenhar um campo sem calcular mil setas. O campo é este: a horizontal vale um; a vertical, a coordenada horizontal menos a vertical. Pausa o vídeo e tenta desenhar o padrão.

[curious] O truque é procurar onde o campo não muda. A componente horizontal já é constante. A vertical só depende da diferença entre as coordenadas. Então, sobre uma reta em que essa diferença não varia, a seta é a mesma em todo ponto. A seta dupla da tela lê-se implica. E essas retas são as paralelas à diagonal.

[thoughtful] Na própria diagonal, a diferença vale zero: a seta é um, zero, horizontal, apontando para a direita. Uma reta abaixo, a diferença passa a valer um: a seta é um, um, a quarenta e cinco graus. Mais uma abaixo, vale dois: a seta é um, dois, ainda mais inclinada. E, acima da diagonal, a diferença é negativa, então as setas apontam para baixo.

[curious] Agora é só copiar: em cada reta, repetimos a seta que encontramos. E o campo inteiro está desenhado: setas que vão empinando quando descemos de uma reta para outra e que se inclinam cada vez mais para baixo quando subimos.

[thoughtful] Guarda esse desenho, porque ele vai voltar. Essa mudança de direção entre retas vizinhas é uma derivada, e no topo da escada a gente vai ler isso numa tabela.

[thoughtful] Terceiro degrau: uma família inteira de redemoinhos. Começa com menos a coordenada vertical na primeira componente e a horizontal na segunda. Divide tudo por uma potência da distância ao quadrado. Xis ao quadrado mais ípsilon ao quadrado é a distância ao quadrado. O expoente é alfa. Cada valor do expoente alfa cria um campo diferente. Pausa o vídeo e tenta: o que acontece com alfa zero, meio e um?

[curious] As setas continuam tangentes às circunferências em volta da origem, sempre no sentido anti-horário. Muda o comprimento. O vetor de cima tem tamanho igual à distância; o denominador vale a distância elevada a dois alfa. Então a rapidez é a distância elevada a um menos dois alfa. Com alfa zero, a rapidez cresce com a distância: é a rotação rígida. Com alfa meio, a rapidez vale um, independentemente da posição. Com alfa um, ela cai com um sobre a distância: é o vórtice que já conhecemos.

[thoughtful] Agora a conta do rotacional. Na tela, P e Q são as duas componentes, e o d arredondado é a derivada parcial. O rotacional é a derivada da componente vertical na direção horizontal, menos a derivada da componente horizontal na direção vertical. A componente vertical é a coordenada horizontal multiplicada pela distância ao quadrado elevada a menos alfa. Regra do produto: a primeira parte dá a própria potência; a segunda, pela regra da cadeia, dá menos alfa vezes a potência com um a menos no expoente, vezes duas vezes a coordenada horizontal, vezes a coordenada horizontal de novo. Põe a potência com um a menos em evidência: no parêntese, sobra a distância ao quadrado menos dois alfa vezes o quadrado da coordenada horizontal. A outra derivada é igualzinha, agora com a coordenada vertical e o sinal trocado. Ao subtrair, a distância ao quadrado aparece duas vezes, e os dois termos com alfa se juntam em dois alfa vezes a soma dos quadrados, que é a distância ao quadrado de novo. Sobra uma fórmula curtinha: dois menos dois alfa, sobre a distância ao quadrado elevada a alfa. E o divergente? Agora é a soma: a derivada da componente horizontal na direção horizontal, mais a da vertical na direção vertical. Nas duas, só a regra da cadeia trabalha, e sai o mesmo termo, dois alfa vezes o produto das coordenadas vezes a potência com um a menos: uma vez com sinal de mais, outra com sinal de menos. Eles se cancelam: zero, para qualquer alfa. Nenhum desses redemoinhos muda a área local do fluido. Ainda pode haver giro e deformação.

[curious] Agora lê a fórmula caso a caso. Alfa zero: dois menos zero, sobre a potência zero, que vale um. Rotacional dois, exatamente o disco rígido. Alfa meio: dois menos um, sobre a distância. Todas as setas têm o mesmo tamanho e, mesmo assim, o rotacional vale um sobre a distância. A rodinha gira mais perto do centro. Alfa um: dois menos dois dá zero. As partículas continuam dando a volta, mas o quadradinho não apresenta rotação local: é o vórtice do segundo episódio.

[excited] E alfa dois? Dois menos quatro dá menos dois: o rotacional fica negativo. As setas continuam dando a volta no sentido anti-horário, e o quadradinho gira no sentido horário! Olha por quê: a seta do lado de dentro é bem mais forte que a do lado de fora. Então a borda de dentro do quadradinho avança mais rápido, e ele vira para trás. O sentido da volta não é o sentido do giro. Não confunda os dois.

[thoughtful] E na origem? Primeiro precisamos perguntar se existe limite. Lê-se: limite de F quando X tende à origem. Com alfa zero, não tem divisão nenhuma: é a rotação rígida, definida e contínua no centro. Com alfa entre zero e meio, a fórmula original não vale na origem, mas a rapidez vai a zero quando nos aproximamos. Então o limite é o vetor nulo e, definindo a seta da origem como zero, o campo fica contínuo. Com alfa meio, a rapidez fica um, só que a direção depende do caminho: não tem limite. E, com alfa maior que meio, a seta explode perto da origem. Sem limite finito.

[curious] Último item: gira cada seta noventa graus, no sentido horário. O redemoinho vira uma explosão radial, com setas para fora. A componente horizontal nova é a vertical antiga, e a vertical nova é menos a horizontal antiga. Então o divergente novo é exatamente a conta do rotacional antigo. Os papéis se trocam: o rotacional vira zero, e o divergente passa a ser dois menos dois alfa, dividido pela distância ao quadrado elevada a alfa. Com alfa um, é a falsa fonte do segundo episódio: setas para fora, mas divergente zero fora do centro. [thoughtful, emphatic] Guarda essa fórmula: dois menos dois alfa. Ela volta na física.

[thoughtful] Antes de subir, duas regras que economizam contas. A primeira começa assim: pega um campo que é o gradiente de uma função. As componentes são as derivadas parciais da função. Na tela, nabla fi: lê-se gradiente de fi. E, daqui em diante, fi com xis pequeno embaixo é a derivada parcial de fi em relação a xis. Calcula o rotacional. A primeira componente é a derivada em relação à vertical da derivada em relação à profundidade, menos a derivada em relação à profundidade da derivada em relação à vertical. E as outras duas componentes seguem o mesmo padrão: uma derivada mista menos a mesma derivada mista com a ordem trocada. Se a função é classe cê dois, as derivadas mistas são iguais, por Schwarz. Tudo cancela. No plano, só sobra a terceira componente do rotacional, e ela também vale zero. Um gradiente nunca gira localmente, nessas condições.

[curious] Lembra do campo que esticava o quadradinho no episódio passado? Ele é o gradiente da metade da diferença entre os quadrados das coordenadas. Por isso o quadradinho deformava, mas não girava.

[thoughtful] Segunda regra, agora no espaço. Calcula o rotacional de um campo e depois o divergente desse rotacional. A primeira componente é derivada na horizontal, a segunda na vertical e a terceira na profundidade. Aparecem seis derivadas mistas, e elas se cancelam aos pares, por Schwarz. Um rotacional nunca diverge, com regularidade suficiente.

[curious] E isso vira teste. Alguém mostra este campo e pergunta: existe outro campo cujo rotacional seja ele? Não precisa procurar. Calcula o divergente: a primeira parcela dá seno, a segunda dá menos seno, e a terceira dá um. Total: um. Se ele fosse o rotacional de um campo regular, seu divergente seria zero. Então não existe esse campo.

[thoughtful] Isso também aparece na física. O campo magnético tem divergente zero, pela lei de Gauss para o magnetismo, que diz que não existe polo magnético isolado. No espaço todo, sob hipóteses adequadas, ele pode ser o rotacional de outro campo, chamado potencial vetor. A seta dupla nos dois sentidos lê-se se e somente se. As duas ideias andam juntas, mas cada direção tem as suas hipóteses. A regra de hoje prova uma das metades: todo rotacional suficientemente regular tem divergente zero.

[thoughtful, emphatic] E repara na hipótese: classe cê dois. Sem derivadas regulares, não aplique o cancelamento automaticamente. No próximo degrau, vamos ver por que essas condições fazem tanta diferença.

[thoughtful] Quarto degrau, o mais delicado da escada. Este campo pega o vetor posição e multiplica por uma fração: o produto das coordenadas dividido pela distância ao quadrado. Como a expressão não está definida na origem, a gente define a seta como zero naquele ponto.

[curious] Olha o desenho. Nas diagonais de subida, as setas apontam para fora da origem. Nas outras diagonais, apontam para dentro. Nos eixos, as setas somem, porque o produto das coordenadas é zero. Pausa o vídeo e tenta resolver os cinco itens antes de acompanhar.

[thoughtful] Item a: existe limite na origem? Calcula o tamanho da seta. As barras duplas da tela são esse tamanho, a norma; a barra simples é o módulo, o valor sem sinal. O vetor posição tem tamanho igual à distância da origem. Então a seta tem tamanho igual ao módulo do produto das coordenadas, dividido pela distância. Em polares, o produto das coordenadas é a distância ao quadrado vezes o cosseno do ângulo e o seno do ângulo. E cosseno vezes seno é metade do seno do dobro do ângulo. Então o tamanho da seta é a distância multiplicada por metade do módulo desse seno. E isso nunca passa da metade da distância, pois o seno não passa de um em módulo.

[curious] Agora o desafio do épsilon. Épsilon é a tolerância na seta; delta, o raio onde você anda perto da origem. Alguém escolhe um épsilon. Você responde com delta igual a dois épsilon. Se o ponto está a menos de delta da origem, o tamanho da seta é no máximo metade dessa distância, ou seja, menos que épsilon. Venceu, para qualquer épsilon. O limite é o vetor nulo.

[thoughtful] Item b: continuidade. O ponto está no domínio, porque definimos a seta ali. O limite existe e é o vetor zero. E é igual à seta do ponto. Os três pedaços passam: o campo é contínuo. Item c: as derivadas parciais na origem. Andando pelo eixo horizontal, o produto das coordenadas é zero, seta zero: derivada zero. Na tela, ela é o limite, quando h tende a zero, da diferença das setas dividida pelo passo h. Pelo vertical, a mesma coisa. A tabela é toda zero: rotacional zero, divergente zero, deformação zero. A previsão seria: perto da origem, nada muda na primeira ordem.

[curious] Item d: confere com um zoom. No episódio passado, o campo suave deixava as setas arrumadinhas quando a gente ampliava uma região pequena. Aqui, olha: o zoom de dez vezes mostra exatamente o mesmo padrão. E o de cem vezes, também. Isso se chama homogeneidade: multiplicar a posição por um número faz o vetor do campo ser multiplicado pelo mesmo número. Na conta, o número aparece ao quadrado em cima e embaixo da fração, cancela, e sobra o fator que multiplica o vetor posição. Então o desenho não se aproxima da tabela zero. Na diagonal, a seta tem sempre metade do tamanho do deslocamento. O erro, dividido pelo passo, fica em meio. Para haver diferenciabilidade, essa razão teria que ir a zero. Não vai. Em qualquer vizinhança, por menor que seja, tem quadradinho crescendo nas diagonais de subida, encolhendo nas outras, e girando para os dois lados.

[thoughtful, emphatic] A tabela errou. Por quê? Item e: calcula a derivada da componente horizontal em relação à coordenada horizontal, fora da origem. A componente horizontal é o quadrado da coordenada horizontal vezes a vertical, dividido pela distância ao quadrado. Regra do quociente: derivada de cima vezes a de baixo, menos a de cima vezes a derivada de baixo, sobre o quadrado do denominador. A derivada de cima é duas vezes o produto das coordenadas. A de baixo é duas vezes a coordenada horizontal. Os termos com a quarta potência se cancelam, e sobra duas vezes a coordenada horizontal vezes o cubo da vertical, sobre a distância à quarta potência. Agora olha essa derivada se aproximando da origem. Nos eixos, ela vale zero, fora do centro. Na diagonal, as duas coordenadas são iguais: aparece duas vezes a quarta potência em cima e quatro vezes a quarta potência embaixo. Resultado: meio. E vale meio na diagonal inteira, por menor que seja a distância da origem. A derivada não é contínua na origem. O campo não é de classe cê um, e a tabela perde a garantia de ser uma boa aproximação. Repara: o cê um é uma garantia, não uma exigência. Tem campo que não é cê um e mesmo assim é diferenciável. Aqui demonstramos que a aproximação falha.

[curious] Olha a escada. No episódio passado, o campo encrenqueiro nem era contínuo. Este é contínuo, tem as duas derivadas parciais e mesmo assim engana. Ter derivadas parciais não basta para garantir que a tabela descreva o campo de perto.

[excited] Topo da escada! Chegou a hora do desafio prometido. Três campos. Para cada um, monta a tabela, lê os quatro números e prevê se o quadradinho gira, muda de área ou deforma. Só depois a gente solta o fluido. A tabela se chama jacobiana, a letra J: as derivadas de P em cima e as de Q embaixo. Lembra das quatro medidas? Rotacional: o de baixo à esquerda menos o de cima à direita. Divergente: a diagonal somada. Primeira deformação, dê um: a diagonal subtraída. Segunda, dê dois: os dois termos fora da diagonal, somados. Vamos testar.

[thoughtful] Primeiro campo: a fórmula do primeiro degrau, a soma e a diferença das coordenadas. Pausa o vídeo e tenta.

[thoughtful] A tabela. A componente horizontal é a soma, então as derivadas são um e um. A vertical é a diferença: derivadas um e menos um. Em cima, um e um; embaixo, um e menos um. Agora as medidas. Rotacional: o de baixo à esquerda menos o de cima à direita, um menos um, zero. Divergente: a diagonal, um mais menos um, zero. Primeira deformação: um menos menos um, dois. Segunda: um mais um, dois. Previsão: não gira, não muda de área, só deforma.

[curious] Solta. O quadradinho estica numa direção um pouco acima do eixo horizontal, achata na perpendicular, e a área fica igual o tempo todo.

[excited] E aí está a resposta do palpite! Como transformação, essa fórmula dobrava a área. Como campo, ela não muda a área nenhuma. Por quê? Porque são dois filmes diferentes. A transformação leva cada ponto diretamente à sua imagem. O campo é uma velocidade: o fluido se move seguindo as setas ao longo do tempo, e quem mede a taxa de área desse fluido é o divergente, que aqui vale zero. O fator de área da transformação é outra grandeza, que vai aparecer quando estudarmos mudança de variáveis. Mesma fórmula, perguntas diferentes.

[thoughtful] Segundo campo: o do segundo degrau, um na horizontal e a diferença na vertical. Pausa e tenta.

[thoughtful] A componente horizontal é constante: derivadas zero e zero. A vertical: um na direção horizontal e menos um na vertical. Tabela: zero e zero em cima; um e menos um embaixo. Rotacional: um menos zero, um. Divergente: zero mais menos um, menos um. Deformações: zero menos menos um, um; e um mais zero, um. Previsão: tudo junto. Gira no sentido anti-horário, encolhe e entorta.

[curious] E isso já aparecia no desenho do segundo degrau: indo para a direita, a seta fica mais inclinada para cima. Esse é o um embaixo à esquerda. Andando para cima, a seta abaixa, e aí aparece o menos um. Solta: o quadradinho viaja pelo campo, gira, encolhe e entorta. A viagem depende da velocidade no centro; ela não aparece na jacobiana porque a gente tirou a seta do centro. A tabela explica forma e área, não o transporte.

[thoughtful] Terceiro campo: a primeira componente é a diferença dos quadrados das coordenadas; a segunda, duas vezes o produto delas. Agora a tabela não é constante: muda com a posição. Derivando a diferença dos quadrados, encontramos duas vezes a horizontal e menos duas vezes a vertical na primeira linha. Derivando duas vezes o produto, aparecem duas vezes a vertical e duas vezes a horizontal na segunda. Então o ponto importa. Pausa o vídeo e prevê nos três pontos mostrados: um, zero; zero, um; e um, um.

[curious] Rotacional: duas vezes a vertical, menos menos duas vezes a vertical. Resultado: quatro vezes a vertical. Divergente: duas vezes a horizontal mais duas vezes a horizontal: quatro vezes a horizontal. E as duas deformações, cada uma é um termo menos ele mesmo. Zero, em qualquer ponto. No ponto um, zero: quatro vezes zero, rotacional zero; quatro vezes um, divergente quatro. Só cresce. No zero, um: rotacional quatro, divergente zero. Só gira. No um, um: gira e cresce.

[excited] Solta os três! Um cresce sem girar, um gira sem crescer, e o terceiro faz as duas coisas. E nenhum entorta: as quinas continuam em ângulo reto. E repara: a tabela fala do que acontece no ponto, naquele instante. Um quadradinho de tamanho finito sente a tabela mudando de um canto para o outro, e os lados até se curvam, mas tão pouco que nem dá para ver. Bem pequeno, esse campo nunca deforma um quadradinho. Guarda isso, porque ele tem nome, e vai aparecer na segunda parte.

[thoughtful, emphatic] Desafio cumprido. A fórmula do campo vira uma tabela, a tabela vira quatro números, e os quatro números contam o que acontece com um quadradinho bem pequeno, logo que você solta. E o cê um garante que essa leitura vale.

[excited] Pronto: você prevê o quadradinho só pela fórmula. Agora vem a melhor parte. Essas contas não ficam no papel. Elas descrevem água de verdade e ajudam nas leis da física. [thoughtful] Vamos começar por um rio.

[thoughtful] Um canal reto, com seis metros de largura. A água corre a um metro por segundo bem no meio e a velocidade cai até zero nas margens, numa parábola. A componente na direção do canal é um menos o quadrado da coordenada horizontal sobre nove. No meio dá um; nas margens, a três metros do centro, dá um menos nove nonos: zero. Três perguntas: o escoamento é incompressível? O escoamento gira? E onde o atrito é maior? Pausa o vídeo e tenta.

[curious] Primeira: a velocidade só tem componente na direção do canal, e ela não muda ao longo do canal. Divergente zero: incompressível.

[thoughtful] Segunda: as linhas de corrente são retas. Dá vontade de dizer que não gira. Mas o rotacional é a derivada da velocidade ao longo do canal entre as margens. Dá menos dois nonos da coordenada horizontal. Na margem esquerda, menos dois nonos vezes menos três dá dois terços por segundo. Um galho ali gira no sentido anti-horário, no modelo de uma rodinha ideal pequena, perto da margem. Lembra que o rotacional é o dobro da velocidade angular dessa rodinha. O galho gira com ômega, a velocidade angular, igual a um terço de radiano por segundo. E o período, o T da tela, o tempo de uma volta, é dois pi dividido por um terço: seis pi, uns dezenove segundos. Na margem direita, menos dois terços: o giro é horário. Bem no centro, a rotação local é zero: o galho desce o rio sem girar.

[curious] Olha os três quadradinhos. O do meio só viaja. Os das margens viajam, entortam e giram, cada um para um lado. Por quê? A água do lado de dentro corre mais rápido que a do lado de fora, perto de cada margem. Uma borda avança mais que a outra.

[thoughtful] Terceira: o atrito. O atrito viscoso vem da deformação: da diferença de velocidade entre camadas vizinhas. Aqui, a primeira deformação é zero e a segunda vale menos dois nonos da coordenada horizontal. Em módulo, é máxima nas margens e zero no centro. É perto das margens que as camadas de água mais deslizam umas sobre as outras: ali o atrito é maior.

[thoughtful] Segundo problema: um jato de água descendo e batendo numa parede, como numa pia. Num modelo ideal, perto do ponto de estagnação, a velocidade tem a coordenada horizontal na primeira componente e menos a vertical na segunda. É o campo do episódio passado, só na metade de cima do plano, com a parede embaixo.

[curious] Primeiro: na parede, a componente vertical é zero, então a água não a atravessa: ela desliza. Numa parede de verdade, a viscosidade faz uma camada fina de água grudar nela, e este modelo ideal ignora essa camada. Segundo: a tabela tem um e zero em cima, zero e menos um embaixo. Rotacional zero, divergente um menos um, zero, e primeira deformação um menos menos um, dois. A água não gira e não comprime: só deforma. Uma gota de tinta que desce pelo eixo se achata e se espalha pela parede, sempre com a mesma área. E as linhas de corrente são hipérboles, fora dos eixos: as curvas onde o produto das coordenadas é constante. Confere. Lê-se dê xis ípsilon, dê tê: a taxa de variação do produto no tempo. Andando com a água, o produto muda pela velocidade horizontal vezes a coordenada vertical, mais a horizontal vezes a velocidade vertical. Dá o produto menos o produto: zero. O produto não muda: a água anda em cima da hipérbole, ou do eixo.

[thoughtful] Terceiro: esse campo é o gradiente da metade da diferença entre os quadrados das coordenadas. Essa função se chama potencial de velocidade. E o laplaciano dela, escrito nabla dois fi, a soma das duas derivadas segundas, aquela curiosidade do segundo episódio, dá um menos um: zero.

[thoughtful, emphatic] E isso não é coincidência. Se a velocidade é um gradiente, o campo é irrotacional, se suficientemente suave. Se também tem divergente zero, então o divergente do gradiente é zero. E o divergente do gradiente é o laplaciano. Escoamento irrotacional e incompressível quer dizer laplaciano do potencial igual a zero: é a equação de Laplace. A mesma equação aparece no potencial elétrico em regiões sem cargas e na temperatura de uma chapa em equilíbrio, sob as hipóteses adequadas.

[curious] Lembra do terceiro campo do desafio, sem deformação? Olha por quê. Deformação zero em todo lugar dá duas equações. Iguala cada deformação a zero e passa um termo para o outro lado: a derivada horizontal da primeira componente é igual à derivada vertical da segunda, e a derivada vertical da primeira é igual a menos a derivada horizontal da segunda. Essas são as equações de Cauchy-Riemann.

[thoughtful] Elas aparecem quando juntamos as duas componentes num número complexo. O nosso campo é exatamente o quadrado do número complexo com parte real horizontal e imaginária vertical. Abre o quadrado: o i da tela é a unidade imaginária. Sai o quadrado da horizontal, mais duas vezes i vezes o produto, mais i ao quadrado vezes o quadrado da vertical. E o quadrado da unidade imaginária é menos um. Sobra a diferença dos quadrados na parte real e duas vezes o produto na parte imaginária. E toda função complexa derivável satisfaz essas equações, como o cubo e a exponencial.

[curious] Agora lê como transformação. Onde a derivada complexa não é zero, uma tabela assim só gira e muda a escala: quadradinhos pequenos viram quadradinhos, maiores ou menores, mas sempre com ângulos retos. Isso se chama mapa conforme. E você conhece um: o mapa-múndi de Mercator preserva os ângulos, mas distorce as áreas, ainda mais perto dos polos. Por isso a Groenlândia aparece quase do tamanho da África, mas com o formato certo em cada pedacinho.

[thoughtful] E o irmão desse campo, com o sinal da segunda componente trocado, tem rotacional zero, divergente zero e só deformação local.

[excited] E agora chegamos ao último problema, aquele da abertura. Um fio comprido com corrente atravessa a tela. As linhas do campo magnético são circunferências ao redor dele. A pergunta é: como a intensidade diminui com a distância? Pausa e pensa.

[thoughtful] A física traz duas informações. Primeiro, o campo dá a volta no fio, e o tamanho só depende da distância até ele. Supondo uma lei de potência, podemos usar a família do terceiro degrau: menos a coordenada vertical e a horizontal, divididas pela distância ao quadrado elevada a um expoente alfa desconhecido. Agora entra a segunda informação: fora do fio não há corrente. Na magnetostática, a lei de Ampère diz que, nessa região, o rotacional do campo magnético é zero.

[curious] Agora usa a fórmula que a gente guardou. O rotacional é dois menos dois alfa, sobre a distância ao quadrado elevada a alfa. Para ser zero fora do fio, o numerador zera: dois igual a dois alfa, e alfa igual a um. Então o tamanho do campo vai com a distância dividida pela distância ao quadrado: um sobre a distância. O campo do fio cai com um sobre a distância. A intensidade ainda depende da corrente; o que a conta escolhe é como ela cai.

[thoughtful] Faz o mesmo com um fio carregado. O campo elétrico aponta para fora para carga positiva, então ele tem a forma da explosão radial do terceiro degrau. Fora do fio não tem carga, e a lei de Gauss dá divergente zero. Divergente: dois menos dois alfa, dividido pela potência da distância. Alfa um, e o campo também cai com um sobre a distância.

[excited] E uma carga pontual no espaço? Escreve o campo como o vetor posição dividido pela distância elevada a um expoente. O X maiúsculo é o vetor posição; as barras duplas, a distância; p, o expoente. No plano, o divergente teria dois menos esse expoente. Agora, no espaço. Faz a conta de uma parcela: a derivada da coordenada horizontal dividida pela distância elevada ao expoente, em relação à horizontal. A derivada da distância, nessa direção, é a coordenada horizontal dividida pela distância. Então dá um sobre a distância elevada ao expoente, menos o expoente vezes o quadrado da coordenada horizontal, sobre a distância elevada ao expoente mais dois. As outras parcelas são iguais, cada uma com sua coordenada. Agora soma. Os primeiros termos dão três vezes a mesma potência inversa; os quadrados das coordenadas somam a distância ao quadrado, que cancela o mais dois do expoente. Sobra o número de parcelas menos o expoente, sobre a distância elevada ao expoente. No plano são duas parcelas; no espaço, três. O divergente no espaço é três menos o expoente, sobre a distância elevada a esse expoente. Para zerar, o expoente é três. A intensidade fica um sobre a distância ao quadrado. Essa é a dependência de duas leis: a de Coulomb e a da gravitação.

[thoughtful, emphatic] No plano, o número que aparece é dois; no espaço, é três. O expoente da lei vem da dimensão do espaço: em três dimensões, o campo tem mais lugar para se espalhar. Mas cuidado: o rotacional e o divergente sozinhos não decidem a lei. É a lei física, impondo rotacional ou divergente zero fora da fonte, junto com a simetria: as linhas em círculo em volta do fio e as linhas radiais em volta da carga. Com as duas juntas, a dependência fica determinada.

[thoughtful] Olha a escada inteira. A mesma fórmula conta dois filmes. Um campo se desenha pelas curvas onde ele não muda. Vimos que o sentido da volta não é o sentido do giro. Um gradiente nunca gira, e um rotacional nunca diverge, sob hipóteses certas. Ter derivadas parciais não basta. E, com a tabela, você prevê o quadradinho antes de soltar. [curious] E, nas aplicações, um rio que gira nas margens, uma parede onde a água deforma, mapas conformes e leis de distância.

[excited] No próximo vídeo, a gente troca de pergunta. Até aqui, medimos o que acontece perto de cada ponto. Agora é hora de somar pedacinhos. Uma chapa quadrada de dois metros de lado, leve num canto e cada vez mais densa até o outro. Pelo valor do centro, a massa dá oito quilos. Pela média dos quatro cantos, dezesseis. O dobro! Qual das duas está certa? A resposta exata vem de somar pedacinhos cada vez menores e chegar ao limite: a integral dupla.

[happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual degrau da escada foi o mais difícil para você? Até a próxima!

---

## Anexo B · As 69 âncoras da v3.3 (cada parágrafo é uma âncora; o `ini` real sai do alinhamento da voz)

| Âncora | Começa em (primeiras palavras) | Palavras | Início estimado (3 p/s) |
|---|---|---|---|
| H-1 | "Três quadradinhos de fluido, três resultados diferentes." | 129 | 0:00.0 |
| A-1 | "Fala, pessoal! Bem-vindos ao Parallax Lab! Esse" | 117 | 0:43.0 |
| D1-1 | "Primeiro degrau. Uma função recebe dois números" | 81 | 1:22.0 |
| D1-2 | "Primeiro, o eixo horizontal da esquerda, onde" | 35 | 1:49.0 |
| D1-3 | "Agora o quadrado de lado um. Como" | 126 | 2:00.7 |
| D1-4 | "E um círculo em volta da origem?" | 82 | 2:42.7 |
| D1-5 | "Agora a mesma fórmula, lida como campo." | 94 | 3:10.0 |
| D1-6 | "E aqui fica uma pergunta para o" | 36 | 3:41.3 |
| D2-1 | "Segundo degrau: desenhar um campo sem calcular" | 33 | 3:53.3 |
| D2-2 | "O truque é procurar onde o campo" | 57 | 4:04.3 |
| D2-3 | "Na própria diagonal, a diferença vale zero:" | 63 | 4:23.3 |
| D2-4 | "Agora é só copiar: em cada reta," | 40 | 4:44.3 |
| D2-5 | "Guarda esse desenho, porque ele vai voltar." | 29 | 4:57.7 |
| D3-1 | "Terceiro degrau: uma família inteira de redemoinhos." | 69 | 5:07.3 |
| D3-2 | "As setas continuam tangentes às circunferências em" | 86 | 5:30.3 |
| D3-3 | "Agora a conta do rotacional. Na tela," | 268 | 5:59.0 |
| D3-4 | "Agora lê a fórmula caso a caso." | 83 | 7:28.3 |
| D3-5 | "E alfa dois? Dois menos quatro dá" | 77 | 7:56.0 |
| D3-6 | "E na origem? Primeiro precisamos perguntar se" | 107 | 8:21.7 |
| D3-7 | "Último item: gira cada seta noventa graus," | 104 | 8:57.3 |
| D3b-1 | "Antes de subir, duas regras que economizam" | 147 | 9:32.0 |
| D3b-2 | "Lembra do campo que esticava o quadradinho" | 31 | 10:21.0 |
| D3b-3 | "Segunda regra, agora no espaço. Calcula o" | 52 | 10:31.3 |
| D3b-4 | "E isso vira teste. Alguém mostra este" | 58 | 10:48.7 |
| D3b-5 | "Isso também aparece na física. O campo" | 81 | 11:08.0 |
| D3b-6 | "E repara na hipótese: classe cê dois." | 27 | 11:35.0 |
| D4-1 | "Quarto degrau, o mais delicado da escada." | 44 | 11:44.0 |
| D4-2 | "Olha o desenho. Nas diagonais de subida," | 44 | 11:58.7 |
| D4-3 | "Item a: existe limite na origem? Calcula" | 121 | 12:13.3 |
| D4-4 | "Agora o desafio do épsilon. Épsilon é" | 67 | 12:53.7 |
| D4-5 | "Item b: continuidade. O ponto está no" | 103 | 13:16.0 |
| D4-6 | "Item d: confere com um zoom. No" | 147 | 13:50.3 |
| D4-7 | "A tabela errou. Por quê? Item e:" | 216 | 14:39.3 |
| D4-8 | "Olha a escada. No episódio passado, o" | 39 | 15:51.3 |
| D5-1 | "Topo da escada! Chegou a hora do" | 97 | 16:04.3 |
| D5-2 | "Primeiro campo: a fórmula do primeiro degrau," | 19 | 16:36.7 |
| D5-3 | "A tabela. A componente horizontal é a" | 83 | 16:43.0 |
| D5-4 | "Solta. O quadradinho estica numa direção um" | 23 | 17:10.7 |
| D5-5 | "E aí está a resposta do palpite!" | 91 | 17:18.3 |
| D5-6 | "Segundo campo: o do segundo degrau, um" | 17 | 17:48.7 |
| D5-7 | "A componente horizontal é constante: derivadas zero" | 64 | 17:54.3 |
| D5-8 | "E isso já aparecia no desenho do" | 78 | 18:15.7 |
| D5-9 | "Terceiro campo: a primeira componente é a" | 85 | 18:41.7 |
| D5-10 | "Rotacional: duas vezes a vertical, menos menos" | 77 | 19:10.0 |
| D5-11 | "Solta os três! Um cresce sem girar," | 88 | 19:35.7 |
| D5-12 | "Desafio cumprido. A fórmula do campo vira" | 40 | 20:05.0 |
| P2-1 | "Pronto: você prevê o quadradinho só pela" | 35 | 20:18.3 |
| A1-1 | "Um canal reto, com seis metros de" | 82 | 20:30.0 |
| A1-2 | "Primeira: a velocidade só tem componente na" | 21 | 20:57.3 |
| A1-3 | "Segunda: as linhas de corrente são retas." | 144 | 21:04.3 |
| A1-4 | "Olha os três quadradinhos. O do meio" | 49 | 21:52.3 |
| A1-5 | "Terceira: o atrito. O atrito viscoso vem" | 62 | 22:08.7 |
| A2-1 | "Segundo problema: um jato de água descendo" | 54 | 22:29.3 |
| A2-2 | "Primeiro: na parede, a componente vertical é" | 171 | 22:47.3 |
| A2-3 | "Terceiro: esse campo é o gradiente da" | 46 | 23:44.3 |
| A2-4 | "E isso não é coincidência. Se a" | 78 | 23:59.7 |
| A4-1 | "Lembra do terceiro campo do desafio, sem" | 66 | 24:25.7 |
| A4-2 | "Elas aparecem quando juntamos as duas componentes" | 98 | 24:47.7 |
| A4-3 | "Agora lê como transformação. Onde a derivada" | 75 | 25:20.3 |
| A4-4 | "E o irmão desse campo, com o" | 21 | 25:45.3 |
| A3-1 | "E agora chegamos ao último problema, aquele" | 40 | 25:52.3 |
| A3-2 | "A física traz duas informações. Primeiro, o" | 80 | 26:05.7 |
| A3-3 | "Agora usa a fórmula que a gente" | 85 | 26:32.3 |
| A3-4 | "Faz o mesmo com um fio carregado." | 63 | 27:00.7 |
| A3-5 | "E uma carga pontual no espaço? Escreve" | 212 | 27:21.7 |
| A3-6 | "No plano, o número que aparece é" | 84 | 28:32.3 |
| S-1 | "Olha a escada inteira. A mesma fórmula" | 81 | 29:00.3 |
| S-2 | "No próximo vídeo, a gente troca de" | 82 | 29:27.3 |
| S-3 | "Se essa aula te ajudou, deixa o" | 30 | 29:54.7 |

---

## Anexo C · Filtro da narração v3.3 (refino do GPT): o que entrou e o que não entrou

**Resultado conferido por script, com a tokenização da cena (com acento):** 69/69 âncoras, mesmos ids e mesma ordem · **482/482 frases de sincronia** (459 gatilhos `self.gat` + 23 fins de sublinhado `le(..., ate=...)`) · nenhuma inversão de ordem entre frases dentro de um parágrafo · todos os parágrafos a ±13% da v3.2 · 22/22 leituras · 10 "pausa (o vídeo) e tenta/pensa/prevê" · tags idênticas às da v3.2 (33/26/9/6/3) · **5.414 palavras ≈ 30:05 a 3 p/s**. 63 dos 69 parágrafos mudaram.

### O que entrou do GPT (rigor e fala mais oral)
| Âncora | Mudança aceita |
|---|---|
| H-1 | "três resultados diferentes"; "uma pergunta de física" (no lugar de "parece de outro mundo"); "o rotacional e o divergente, **junto com a simetria**, que ajudam a escolher a lei" |
| A-1 | verbos da escada ("vamos ler… explorar… descobrir… enfrentar") e "cada degrau prepara o seguinte" |
| D1-3 | "apareceu outro quadrado, inclinado… **Não foi só rotação**" (espelhamento explícito) |
| D3-3 | "área **local**" e "Ainda pode haver giro e deformação" |
| D3-6 | conserta um erro da v3.2: "todos esses campos dividem por zero lá" era falso para α = 0; "sem limite finito" para α > ½ |
| D3-7 | falsa fonte: "setas para fora, mas divergente zero fora do centro" |
| D3b-1/3 | "nessas condições", "com regularidade suficiente" |
| D3b-5 | lei de Gauss do magnetismo; potencial vetor "sob hipóteses adequadas"; "todo rotacional suficientemente regular" |
| D4-3 a D4-7 | regra do quociente completa ("sobre o quadrado do denominador"); "tem campo que não é cê um e mesmo assim é **diferenciável**"; some o "e vale meio e vale meio" repetido da v3.2 |
| D5-5 | imagem imediata × fluido andando no tempo; "Mesma fórmula, perguntas diferentes" |
| A1-3 | a rodinha ideal pequena perto da margem (o galho não é uma sonda infinitesimal) |
| A1-5 | "em módulo, é máxima nas margens" (d₂ troca de sinal entre as margens) |
| A2-2 | velocidade tangencial na parede real; "hipérboles, **fora dos eixos**"; "ou do eixo" |
| A3-2 a A3-5 | "fora do fio", "supondo uma lei de potência", leitura mais limpa da conta no espaço |
| A4-3 | Mercator "distorce as áreas, ainda mais perto dos polos" (agora o "por isso a Groenlândia…" tem causa) |
| S-2 | "somar pedacinhos cada vez menores e chegar ao limite" (prepara a soma de Riemann do EP. 05) |

### O que voltou para a v3.2 ou foi ajustado (e por quê)
| Âncora | O que o GPT fez | Decisão |
|---|---|---|
| A3-3 | "proporcional **à** distância dividida…": a crase quebra o gatilho `a distância dividida pela distância ao quadrado` (o GPT conferiu sem acento; a cena compara com acento) | "o tamanho do campo **vai com** a distância dividida pela distância ao quadrado"; e volta a leitura do símbolo "sobre a distância ao quadrado elevada a alfa" (o GPT tinha "sobre a potência da distância") |
| D2-2, D3b-5, A2-3 | tirou 3 frases que fecham sublinhados de leitura (`e essas retas são as paralelas`, `as duas ideias andam juntas`, `aquela curiosidade do segundo episódio`). O pacote só listava os 459 gatilhos; essas 23 frases de `ate=` não estavam nele | as 3 frases voltam, com o resto do refino mantido (em D3b-5: "As duas ideias andam juntas, mas cada direção tem as suas hipóteses") |
| A2-2 | falou rotacional, divergente e deformação **antes** de "a tabela tem um e zero" | volta a ordem da v3.2: a cena escreve a tabela e os valores voam das células; na ordem do GPT as três medidas sairiam atrasadas em relação à fala |
| D5-11, D5-12 | "nenhum entorta **na aproximação local**… ângulo reto **no desenho**… não apresenta deformação angular de primeira ordem"; "quadradinho infinitesimal" | v3.2 inteira. A nota 1 do GPT não procede: o campo z² é holomorfo, então o fluxo dele é conforme em cada instante e as quinas ficam em 90° **exatos** mesmo no quadradinho finito (os lados é que se curvam). A ressalva enfraqueceria uma afirmação verdadeira e traz jargão |
| D3b-1 | leitura 8 "P com xis pequeno embaixo…" | **aceita a nota 6 do GPT**: a tela mostra `ÍNDICE = DERIVADA: φ_x = ∂φ/∂x` e o sublinhado cai no índice de φ_x, então a fala vira "**fi** com xis pequeno embaixo é a derivada parcial de **fi** em relação a xis". Também volta "derivada em relação à vertical da derivada em relação à profundidade" (o GPT tinha deixado meia frase curta e meia longa) |
| D3-3 | "traz menos alfa, uma potência…"; "a soma das derivadas de cada componente na sua própria direção" | volta a leitura dos símbolos da v3.2 nas duas passagens (regra da série: ler o que está na tela) |
| A1-5 | "o cisalhamento viscoso é maior junto às margens" | sem "cisalhamento" (decisão da v3): "é perto das margens que as camadas de água mais deslizam umas sobre as outras: ali o atrito é maior" |
| A3-6 | "É uma diferença essencial"; "**ele** tem mais lugar" | corta o enchimento; "o campo tem mais lugar"; volta "o rotacional e o divergente sozinhos não decidem a lei" |
| H-1 | "dá para ligar as fórmulas aos movimentos" | volta "qual fórmula faz qual filme só olhando para ela" (amarra com "dois filmes" do D1 e do D5) |
| D1-1, D1-3, D3-6, D4-6, A4-3 | pequenos cortes de lógica | voltam: "a imagem de uma reta, de um quadrado e de um círculo"; "ela leva segmento em segmento"; "não tem divisão nenhuma" e "então o limite é o vetor nulo"; "em qualquer vizinhança, por menor que seja"; "uma tabela assim **só** gira e muda a escala", "E você conhece um" |
| D1-2, D2-2, D5-7 | "A conta mostra tudo.", "Economiza muita conta.", "Confere na animação." | cortados (enchimento) |
