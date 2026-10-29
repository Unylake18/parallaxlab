# HANDOFF — yt_0015 "Momento linear e impulso" (preview silencioso v1, com trechos em Three.js)

Documento autocontido para o Claude Code. Matemática, números, textos de tela e storyboard são **especificação de implementação**
(AGENTS.md): não redesenhar. Se achar inconsistência objetiva, reporte antes de ampliar o escopo.

## 0. Identificação
- **Unidade:** `videos_longos/yt_0015_momento_impulso/` (ID provisório: confirme que `yt_0015_*` não existe; se existir, use o próximo
  livre e reporte). `formato: longo_horizontal` (`template/config_horizontal.py`; `template/layout_horizontal.py` se útil).
- **Endereço no mapa:** `disciplina: Física I` · `bloco: Momento e colisões` · `modulo: 4.9 Momento linear e impulso` ·
  `referencia: Sears 8.1–8.2 · Moysés 4.5 e 9.2 · Feynman I, 10-1 a 10-3`. `natureza: teoria_visual` (com exercícios resolvidos).
- Primeiro de uma série de 3 longos do 4.9 (depois: centro de massa, foguete). Vem depois de `yt_0013_colisoes_1d` e `yt_0014`.
- **Duração nominal:** ~18–20 min com a voz (narração congelada, ~3.020 palavras). Neste preview silencioso, use os tempos
  nominais da §6; a voz vem depois e a cena se estica para ela.
- **solido_3d:** `nenhum` (arsenal Blender), porque os sólidos de 4.9–4.10 (`colisao_1d`, `colisao_2d`, `explosao`) não mostram
  impulso. Registre no relatório "Teste do arsenal: não usado, porque ...".
- **3D em Three.js (pedido do Kaio, 2026-10-27):** em **dois trechos** (C01 trilho de ar e C13 luz na água) e, opcional, na granada
  do CTA. Pipeline experimental em `experimentos/threejs/` (ver §4c). O resto é Manim 2D.

## 1. Rodada
**Objetivo:** criar a unidade e renderizar o **preview silencioso 960×540 / 15 fps**, do hook ao CTA. Sem voz, SRT, master, entrega,
commit ou push. Não mexer em `template/`, `docs/`, `assets/`.
**Ler:** `videos_longos/yt_0013_colisoes_1d/ficha.md` (modelo de ficha) e, no `cena.py` do yt_0013, só os helpers reutilizáveis
(`Corpo`, `arrow`, `placa`/painel, header de duas linhas, abertura, CTA, constantes de cor e a função de notação). Copie os helpers
para o `cena.py` novo (não importe entre unidades). `docs/padrao_video_longo.md` (§1 estrutura, §2 tela, §3 tipografia, §4 cores) e
`docs/formatos.md` (campos da ficha) só para conferir.
Ler também: `experimentos/threejs/README.md` (pipeline 3D + Manim) e, como base, `experimentos/threejs/modelo/`; o
`exemplo_toroide/` só se precisar de uma receita.
**Narração congelada:** `videos_longos/yt_0015_momento_impulso/narracao_sugestao.md` (já copiada para a pasta; não editar).
Os IDs das âncoras (H1, C01-1...) são os nomes das seções do `cena.py`. Neste preview silencioso, use os tempos nominais da §6,
mas dê a cada âncora tempo para a fala dela (~2,7 palavras/s) para que a sincronia futura só estique.
**Criar:** `ficha.md` (campos de `formatos.md`, `solido_3d:` preenchido, campo extra `3d_threejs: C01, C13 (+CTA opcional)`,
status "v1 preview silencioso"), `cena.py`, a subpasta `threejs/` (§4c).
**Alterar:** nada fora da unidade.

## 2. Tese, hipóteses e física congelada
- **Pergunta narrativa:** "Por que dobrar os joelhos salva suas pernas?" **Payoff:** o impulso é a área sob F(t) e só depende de Δp;
  quem escolhe o tempo de contato escolhe a força. A conservação do momento vem de dP⃗/dt = F⃗_ext e vale componente por componente.
- p⃗ = m v⃗ · F⃗_res = dp⃗/dt (m constante) · **J⃗ = ∫F⃗ dt** · **J⃗_res = Δp⃗** · F⃗_méd = J⃗/Δt (altura do retângulo de mesma área e mesma base) ·
  dP⃗/dt = F⃗_ext (forças internas se cancelam aos pares).
- Eixo x positivo para a direita, y para cima. g = 9,8 m/s². 1 kgf = 9,8 N.
- Hipóteses: nas colisões, forças impulsivas ≫ peso e atrito (e se diz quando o peso entra); gelo e trilho de ar sem atrito; massa do
  foguete constante em C06.
- **Fora do escopo:** centro de massa (próximo vídeo), massa variável/foguete real, colisões (já feitas), coeficiente de restituição.

### Cuidados conceituais (vieram da revisão; não alterar)
1. **C03:** a colisão é horizontal. O gráfico se chama **F_x(t)** com rótulo `FORÇA DA PAREDE` (não F_res): na direção x, antes do
   contato a força é praticamente zero. Só depois aparece o teorema geral com F⃗_res.
2. **C07 (muro):** as duas curvas são **F_res(t)** com **a mesma área (560 N·s)**. A força do chão N = F_res + m g; o peso (784 N) entra
   só na conversão para "quantos pesos": ≈ 72 e ≈ 6. A área de N **não** é igual nos dois casos; não desenhar N com área igual.
3. **C13 (Newton/Snell):** v₁ sen θ₁ = v₂ sen θ₂ dá a **forma angular** de Snell (sen θ₁/sen θ₂ = constante). No modelo corpuscular,
   a constante é **v₂/v₁**. **Nunca escrever "= n₁₂"**. Na descrição ondulatória a relação aparece invertida: sen θ₁/sen θ₂ = v₁/v₂.
4. **C01:** o argumento do Feynman mostra **qual grandeza** (m·v); não escrever na tela que ele "prova" a conservação. Isso é C09.

## 3. Notação
p⃗ (momento), P⃗ (momento total), J⃗ (impulso), F⃗_res, F_x, F_méd, N (força do chão), vᵢ e v_f (velocidade inicial e final), V
(velocidade de quem recua: você no gelo, o caçador), Δt, h, d. Siga a função de notação do yt_0013 para os índices (ᵢ, f).

## 4. Gramática visual
- **Cores (padrão de Mecânica):** velocidade **violeta** `#9C8CFF`; momento p⃗, P⃗, Δp⃗ **magenta** `#EA63FF`; força (F, F_x, F_res, N,
  peso, F₁₂) azul-claro `#5AA2FF`; impulso J⃗ **e toda área sob F(t)** `#9CC7FF` (nunca verde); corpos em aço `#7A8696`/`#B8C4DA`;
  geometria e eixos `GEO`/`DIM`; ângulos em **arcos brancos finos**; números e massas brancos.
- C13: corpúsculos de luz como **pontos brancos**; o raio como trilha branca fina; a água como região `PANEL` translúcida (`#0E2A52`)
  com borda `GEO`; normal tracejada `DIM`; impulso `#9CC7FF`.
- **Corpos 2D limpos e chatos**, sem brilho nem sombra: bola = círculo de aço; pessoa = silhueta 2D simples em aço (hook/C07); pulga =
  ícone 2D simples em aço; foguete = silhueta 2D. Nada de caixas 3D.
- **Header de duas linhas** (como o yt_0013): linha 1 `MECÂNICA · MOMENTO LINEAR E IMPULSO` (~17, `DIM`, opacidade 0,5, fixa);
  linha 2 = título da cena em maiúsculas (~30, branco 0,95), com FadeOut do antigo antes do FadeIn do novo. No hook, só a linha 1.
- Equações na coluna direita (x ≈ 4,3), aparato à esquerda. Poucas equações por vez; ao trocar de etapa, a anterior sai.
- Vetores finos quando pequenos, ponta sempre visível. Variável definida na tela sempre com a cor da grandeza.
- **Gráficos F(t):** eixos `DIM`, curva azul-claro, área preenchida `#9CC7FF` com opacidade ~0,45; retângulo da força média com borda
  tracejada azul-claro e a mesma área (confira numericamente). Este par "diagrama antes/depois + gráfico F(t)" é o aparato do vídeo:
  aparece em C03 e volta em C04, C06, C07 e C08.
- Todo texto fora do MathTex em Space Grotesk maiúscula; símbolos em MathTex.

## 4b. Cabeçalho e capítulos (padrão dos dois vídeos de colisões)
Canto superior esquerdo, duas linhas, **igual ao yt_0013/yt_0014** (copie o helper do header do `cena.py` do yt_0013):
- **Linha 1 (título do vídeo, fixo, pequeno e apagado):** `MECÂNICA · MOMENTO LINEAR E IMPULSO` (~17, `DIM` `#8FA3C4`, opacidade 0,5).
- **Linha 2 (capítulo atual, logo abaixo):** Space Grotesk maiúscula ~30, branco 0,95. Troca: FadeOut do antigo (~0,25 s) e **só depois**
  FadeIn do novo. No hook e no CTA, só a linha 1. Nos trechos em Three.js, o header continua por cima (camada Manim).
- Os capítulos são **os mesmos** que vão para `capitulos_youtube.txt` depois (não gerar o arquivo agora):

| Bloco | Linha 2 do header (= capítulo) |
|---|---|
| Hook | — (só linha 1) |
| Abertura | — (título central; header volta depois) |
| C01 | `POR QUE MASSA VEZES VELOCIDADE?` |
| C02 | `MOMENTO LINEAR` |
| C03 | `IMPULSO` |
| C04 | `EXERCÍCIO 1 · BOLA NA PAREDE` |
| C05 | `EXERCÍCIO 2 · CHUTE EM 2D` |
| C06 | `EXERCÍCIO 3 · FORÇA QUE CRESCE COM O TEMPO` |
| C07 | `EXERCÍCIO 4 · DE VOLTA AO MURO` |
| C08 | `EXERCÍCIO 5 · A PULGA` |
| C09 | `POR QUE O MOMENTO SE CONSERVA` |
| C10 | `EXERCÍCIO 6 · AGARRAR OU REBATER` |
| C11 | `EXERCÍCIO 7 · O CAÇADOR NO LAGO` |
| C12 | `EXERCÍCIO 8 · OS GASES DO RIFLE` |
| C13 | `EXERCÍCIO 9 · NEWTON E A LUZ` |
| Síntese | `RESUMO` |

Nada de `²`, `×` ou símbolos dentro de `txt()` (a Space Grotesk não tem todos os glifos): por isso "VEZES" e "COM O TEMPO".
Abaixo do header, nos exercícios, um selo discreto com a fonte (`SEARS · EX. 8.2`, `MOYSÉS · PROB. 4.7`), ~20, `DIM`, opacidade 0,6.

## 4c. Trechos em Three.js
Regra do pipeline: **Three.js = objeto e fenômeno (fundo); Manim = vetores, rótulos, equações, header (por cima, `-t` com alfa).**
Os dois leem um `timeline.json` e o `compor.py` junta quadro a quadro (H.264 CRF 14 no final).

**Adaptação 16:9 (pendência conhecida do README):** o `modelo/` é 9×16. Na subpasta `videos_longos/yt_0015_momento_impulso/threejs/`
(copie o `modelo/` à mão; o `novo_video.py` aponta para `videos/` curtos), troque W/H para 960×540 (preview) e 1920×1080 (final),
as constantes 9 e 16 do quadro Manim para 16 e 9 no `cena.py` da camada, no `render3d.js` e no `qa/alinhamento.js`. Não alterar o
`experimentos/threejs/` original. Se a adaptação ficar grande demais, **pare nela** e reporte, deixando C01 e C13 em Manim 2D.

**T1 — C01 trilho de ar (C01-1 a C01-4).**
- Trilho de alumínio/aço longo em leve perspectiva (câmera 3/4 baixa, fov ~25°), furinhos do ar, dois carrinhos de aço iguais
  (`#7A8696` com faixa `#B8C4DA`), fundo `#050816`. Cápsula de explosão pequena entre eles (flash branco curto, sem fogo).
- Movimentos sincronizados com o `timeline.json`: C01-2 explosão, carrinhos saem iguais; C01-3 vêm um contra o outro, batem, grudam,
  param; C01-4 a câmera **passa a andar junto** com o carrinho da esquerda (é o "carro" do Feynman; dispensa desenhar um carro):
  o carrinho da esquerda fica parado no quadro e o mundo desliza.
- Manim por cima: setas violeta (v, 2v), rótulos `m`, `VISÃO DO CARRO`, e a equação `m·2v + m·0 = 2m·v` em magenta. Quando a
  equação entra, `realce_3d` recua o 3D (escurece e dessatura).
- C01-5 a C01-7 voltam ao Manim 2D puro (transição: o último quadro 3D recua e some).

**T2 — C13 luz na água (C13-2 a C13-5).**
- Tanque de vidro com água (`MeshPhysicalMaterial` de transmissão leve, tom `#0E2A52`), superfície plana visível, um espelho plano
  para C13-2. Câmera de lado, quase ortográfica na hora das contas (para os ângulos do Manim casarem: confira com `qa/alinhamento.js`,
  erro ≤ 2 px).
- Corpúsculos: **pontos brancos brilhantes** em fila, como um rastro de luz (mesma técnica do rastro do toroide, em branco, não verde).
  No espelho, refletem; na água, entram e se aproximam da normal.
- Manim por cima: normal tracejada `DIM`, ângulos em arcos brancos finos, componentes tangencial e normal da velocidade (violeta),
  impulso normal `#9CC7FF`, e as equações da §6 na coluna direita.
- C13-6 e C13-7 em Manim 2D (o tanque recua).

**T3 (opcional) — granada do CTA:** esfera de aço que se parte em fragmentos no meio de uma parábola, com um ponto luminoso seguindo
a parábola. Só se T1 e T2 estiverem prontos; senão, 2D.

Qualidade: aço com `envMapIntensity` baixo, sem brilho excessivo; cores da paleta sem `sRGBEncoding` (README, regra 6); nada de bolinhas
para corrente (não há corrente neste vídeo). "Bem lindo": iluminação suave, sombras de contato discretas, movimento suave (3u² − 2u³).

## 5. Abertura e CTA
Hook → `BEM-VINDOS AO PARALLAX LAB` → título `MOMENTO LINEAR E IMPULSO` + `NESTE VÍDEO: O QUE UMA FORÇA FAZ AO LONGO DO TEMPO` →
retomada (miniaturas de colisões 1D e 2D com P⃗ᵢ = P⃗_f). CTA no padrão: FadeOut geral + `self.clear()`, logo com anéis,
`INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS`, pergunta `SE A GRANADA EXPLODE NO AR, O QUE CONTINUA NA PARÁBOLA?` com uma granada 2D
que se parte e um ponto que segue a parábola, e `PRÓXIMO VÍDEO: CENTRO DE MASSA` (assunto em ciano).

## 6. Storyboard por âncora
Os IDs (H1, C01-1...) são os da narração congelada, que chega na rodada da voz. Use-os como nomes das âncoras/seções no `cena.py`.

**HOOK (~40 s)**
- H1: silhueta em cima de um muro de 2,5 m (cota `GEO`); cai e aterrissa de **pernas duras**; flash curto de impacto no pé.
- H2: reset; mesma queda, agora **os joelhos dobram** e o corpo desce até agachar.
- H3: as duas aterrissagens lado a lado; `MESMA QUEDA. MESMA VELOCIDADE.` e depois, no centro, `POR QUE DOBRAR OS JOELHOS SALVA SUAS PERNAS?`

**ABERTURA (~40 s)**: A1 bem-vindos · A2 título + `NESTE VÍDEO` · A3 miniaturas de colisões com P⃗ᵢ = P⃗_f.

**C01 — POR QUE MASSA × VELOCIDADE? (~2 min)**
- C01-1: trilho de ar (linha `GEO` com furinhos), dois carrinhos iguais parados, cápsula de explosão entre eles.
- C01-2: explosão; setas violeta iguais e opostas.
- C01-3: dois carrinhos iguais vindo um contra o outro com setas iguais; batem, grudam, **param**.
- C01-4: a mesma colisão vista de um carro que anda junto com o carrinho da esquerda (rótulo `VISÃO DO CARRO`; um carrinho estilizado
  de observador acima do trilho): um parado, o outro com seta 2v; depois o conjunto com seta v.
- C01-5: `m·2v + m·0 = 2m·v` em magenta.
- C01-6: dois casos rápidos (m contra 2m; 2m contra 3m) com Σ m·v batendo antes e depois.
- C01-7: `m·v` destacado; `v` e `m·v²` riscados.

**C02 — MOMENTO LINEAR (~1 min)**
- C02-1: bloco com seta violeta (velocidade) e, logo abaixo, seta magenta (momento); `p⃗ = m v⃗`.
- C02-2: `kg·m/s = N·s`.
- C02-3: `F⃗_res = dp⃗/dt` e, ao lado, `= m a⃗` (m constante). Sem selo histórico ("Newton escreveu...").

**C03 — IMPULSO (~1,5 min)**
- C03-1: bola chegando numa parede (colisão horizontal); gráfico **F_x(t)** `FORÇA DA PAREDE` nasce sincronizado: zero, sobe rápido,
  pico, desce, zero.
- C03-2: área preenchida; depois o teorema geral `J⃗ = ∫F⃗_res dt = Δp⃗`.
- C03-3: retângulo de mesma base e mesma área; `F_méd = J/Δt`.
- C03-4: a curva estreita e sobe com a área constante (contador de área parado na tela).

**C04 — EXERCÍCIO 1 · BOLA NA PAREDE (Sears, Ex. 8.2) (~1,2 min)**
- 0,40 kg; vᵢ = −30 m/s (para a esquerda); v_f = +20 m/s; Δt = 0,010 s; eixo +x à direita.
- C04-3: `J = 0,40·(20 − (−30)) = 20 N·s`; p⃗ᵢ, p⃗_f e Δp⃗ (para a direita).
- C04-4: a conta errada `0,40·(20 − 30) = −4 N·s` riscada (cinza apagado) + `A PAREDE PUXOU A BOLA?`
- C04-5: `F_méd = 20/0,010 = 2.000 N`; peso 3,9 N como seta minúscula ao lado.
- C04-6: `PARAR` (Δp até zero) × `REBATER` (Δp até zero e volta).

**C05 — EXERCÍCIO 2 · CHUTE EM 2D (Sears, Ex. 8.3) (~1,3 min)**
- 0,40 kg; vᵢ = 20 m/s para a esquerda; v_f = 30 m/s a 45° para cima e para a direita; Δt = 0,010 s.
- Componentes: v_f,x = v_f,y = 21,2 m/s; vᵢ,x = −20 m/s. `Jx = 16,5 N·s`, `Jy = 8,5 N·s`.
- C05-4: triângulo de momentos (p⃗ᵢ, p⃗_f, Δp⃗ = p⃗_f − p⃗ᵢ fechando); F⃗_méd sobre Δp⃗: `1,9×10³ N a 27°`.
- C05-5: arcos de 27° (Δp⃗) e 45° (v⃗_f) lado a lado.

**C06 — EXERCÍCIO 3 · FORÇA QUE CRESCE COM t² (Sears, Exerc. 8.11) (~1,3 min)**
- Foguete 2D, 2.150 kg; gráfico `F = A t²` com o ponto (1,25 s; 781,25 N).
- `A = 781,25/1,25² = 500 N/s²`.
- Área entre t = 2,0 e 3,5 s preenchendo; `J = ∫ 500 t² dt = (500/3)(3,5³ − 2,0³)`.
- `J ≈ 5,81×10³ N·s`, `Δv = J/m = 2,70 m/s`; retângulo de F_méd = 3.875 N sobreposto.

**C07 — DE VOLTA AO MURO (Moysés, Prob. 9.1) (~2 min)**
- C07-1: 80 kg, h = 2,5 m; `v = √(2·9,8·2,5) = 7,0 m/s`.
- C07-2: `Δp = 560 kg·m/s` em magenta, igual nos dois casos.
- C07-3: dois gráficos **F_res(t)** lado a lado, **mesma área 560 N·s** (conferir): `PERNAS DURAS` (Δt = 0,01 s, alto e estreito) ×
  `JOELHOS` (Δt = 0,14 s, baixo e largo). Escala vertical comum (o pico das pernas duras pode sair do quadro com uma seta "↑" e o valor).
- C07-4: `F_res,méd = 56.000 N` × `3.920 N`.
- C07-5: `N = F_res + m g`; faixa fina do peso (784 N) somada; `≈ 72 PESOS` × `≈ 6 PESOS`.
- C07-6: centro: `MESMO IMPULSO. MAIS TEMPO. MENOS FORÇA.`
- C07-7: tabela curta: `SAQUE DE TÊNIS ≈ 49 kgf` · `PÊNALTI ≈ 92 kgf` · `CARRO A 60 km/h NO MURO ≈ 25 tf`.

**C08 — CABELUDO · A PULGA (Moysés, Prob. 4.7) (~1,8 min)**
- Pulga de 2 mg; pulo de 50 cm; zoom: patas esticam 1 mm antes de sair do chão.
- `v = √(2gh) = 3,13 m/s`.
- `CAMINHO 1`: `a = v²/(2d) = g·h/d = 500 g`.
- `CAMINHO 2`: `Δt = 2d/v = 0,64 ms`; `F_res = m v/Δt`; as duas expressões se igualam na tela.
- `N = m(a + g) = m g (h/d + 1) = 501 PESOS`; o "+1" pisca.
- `N ≈ 9,8×10⁻³ N ≈ 1,0×10⁻³ kgf`; silhueta humana de 70 kg ao lado de um bloco `35 t`.

**C09 — POR QUE O MOMENTO SE CONSERVA (~1,5 min)**
- Dois corpos interagindo; F⃗₁₂ e F⃗₂₁ iguais e opostas.
- `dp⃗₁/dt = F⃗₁₂`, `dp⃗₂/dt = F⃗₂₁` → somadas: `d(p⃗₁ + p⃗₂)/dt = 0`.
- Muitos corpos: `dP⃗/dt = F⃗_ext`; `F⃗_ext = 0 ⇒ P⃗ CONSTANTE`.
- Separado por componentes: `dPx/dt = F_ext,x` e `dPy/dt = F_ext,y`.

**C10 — EXERCÍCIO 6 · AGARRAR OU REBATER (Sears, Exerc. 8.20) (~1 min)**
- Você 70,0 kg no gelo; bola 0,600 kg a 10,0 m/s.
- `AGARRA`: `V = 0,600·10,0/70,6 = 0,085 m/s`.
- `REBATE` (bola volta a 8,0 m/s): `70,0·V = 0,600·(10,0 + 8,0)` → `V = 0,154 m/s`; miniatura do C04-6 ao lado.

**C11 — EXERCÍCIO 7 · O CAÇADOR NO LAGO (Sears, Exerc. 8.25) (~1,3 min)**
- Caçador + arma 72,5 kg; bala 4,20 g a 965 m/s.
- Horizontal: `V = 0,00420·965/72,5 = 0,0559 m/s`.
- Tiro a 56°: aparece a **normal do gelo** (azul-claro) crescendo durante o disparo.
- `Py NÃO SE CONSERVA` · `Px SE CONSERVA`; `V = 0,0559·cos 56° = 0,031 m/s`.

**C12 — EXERCÍCIO 8 · OS GASES DO RIFLE (Sears, Exerc. 8.17) (~1,1 min)**
- Rifle 2,80 kg apoiado frouxamente; bala 7,20 g a 601 m/s **em relação ao cano**; rifle recua a 1,85 m/s **em relação ao chão**.
- Bala em relação ao chão: `601 − 1,85 = 599,15 m/s`; `p_bala = 4,31 kg·m/s`; `p_rifle = −5,18 kg·m/s`.
- As setas não fecham; surge uma nuvem de gases com `p_gases = +0,866 kg·m/s`, e a soma fecha em zero.
- `SISTEMA = BALA + RIFLE + GASES`.

**C13 — CABELUDO FINAL · NEWTON E A LUZ (Moysés, Prob. 9.2) (~2,3 min)**
- C13-1: `SÉCULO XVII`; raio desenhado como fluxo de pontos brancos.
- C13-2: espelho; impulso perpendicular à superfície; componente tangencial igual, normal invertida; `θ₁′ = θ₁`.
- C13-3: ar → água; impulso normal; tangencial preservada; `v₁ sen θ₁ = v₂ sen θ₂` (ângulos a partir da normal).
- C13-4: `sen θ₁ / sen θ₂ = CONSTANTE` e, embaixo, `MODELO DE NEWTON: = v₂/v₁`.
- C13-5: raio se aproxima da normal (θ₂ < θ₁) → `v₂/v₁ > 1` → `NEWTON: LUZ MAIS RÁPIDA NA ÁGUA`.
- C13-6: `1850 · FOUCAULT: A LUZ É MAIS LENTA NA ÁGUA`; o `v₂ > v₁` riscado; ao lado `DESCRIÇÃO ONDULATÓRIA: sen θ₁ / sen θ₂ = v₁/v₂`.
- C13-7: `IMPULSO CERTO + MODELO ERRADO = PREVISÃO TESTÁVEL`.

**SÍNTESE (~45 s)**: S1 as duas curvas F_res(t) do muro, mesma área · S2 `J⃗ = ∫F⃗_res dt = Δp⃗` e `dP⃗/dt = F⃗_ext`.
**ENCERRAMENTO (~30 s)**: ver §5.

## 7. Payoffs protegidos (não cortar)
1) m·v é a grandeza certa (simetria + referencial). 2) J⃗ = área sob F(t) = Δp⃗. 3) Força média = retângulo de mesma área. 4) O sinal
é física (C04). 5) F_méd aponta para Δp⃗, não para v⃗_f (C05). 6) Mesma área de F_res, tempos diferentes: 72 × 6 pesos (C07). 7) O "+1"
do peso (C08). 8) dP⃗/dt = F⃗_ext e conservação por componente (C09, C11). 9) Sistema completo (C12). 10) Snell angular no modelo
corpuscular → previsão testável derrubada por Foucault (C13).

## 8. Render mínimo
Preview 960×540 / 15 fps em lotes por seção (`SECOES=...`, como no yt_0013); um preview completo só no fim. Trechos T1/T2: primeiro
quadros soltos (`node render3d.js --quadros ...`) até câmera e objeto ficarem certos; depois o trecho inteiro, composto, e emendado no
preview. Stills 1920×1080 de C01-4 (3D + setas), C05-4 (triângulo), C07-3 (as duas áreas) e C13-3 (refração 3D + ângulos).
Não gerar voz, SRT, master nem entrega.

## 9. QA do preview
- Áreas iguais em C03-4 e C07-3 **numericamente** (reporte os valores medidos no código).
- C03 rotulado F_x / FORÇA DA PAREDE; C07 rotulado F_res; nenhum "= n₁₂" em C13.
- Todos os números da §6 conferem com o código (sem arredondar diferente do que está aqui).
- Δp⃗ sempre desenhado como p⃗_f − p⃗ᵢ.
- Nada de texto sobreposto; equações legíveis a 960×540; header trocando sem sobreposição.
- Sem índices de debug do MF-Tools no render final.
- Header: capítulos exatamente como na §4b; troca sem sobreposição; header legível sobre o 3D.
- Three.js: alinhamento 3D × Manim ≤ 2 px (reportar o valor); mesmo número de quadros nas duas camadas.

## 10. Parada e relatório
Pare com o preview completo. Relatório (AGENTS.md): arquivos criados, renders e caminhos, verificações feitas, valores das áreas
medidas, alinhamento do Three.js, tempo de render do 3D, "Teste do arsenal: não usado, porque ...", pendências e o que ficou
diferente desta especificação. Não commitar nem dar push.
