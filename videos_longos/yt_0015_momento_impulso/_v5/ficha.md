# MOMENTO LINEAR E IMPULSO — O QUE UMA FORÇA FAZ AO LONGO DO TEMPO

- **ID:** yt_0015 (Parte 1 de 2: uma partícula; a Parte 2, sistemas, é o yt_0016)
- **formato:** longo_horizontal
- **natureza:** teoria_visual (teoria aprofundada + exercícios resolvidos)
- **disciplina:** Física I · **bloco:** Momento e colisões · **modulo:** 4.9
- **referencia:** Moysés 4.5 e 9.2 · Sears 8.1 · Feynman I, 10-1 a 10-5
- **duração esperada:** ~18–19 min com a voz (narração v4: 2.942 palavras; nominal 18,2 min a 2,7 palavras/s); preview v4 18:16
- **solido_3d:** nenhum, porque os sólidos de 4.9–4.10 do arsenal Blender (`colisao_1d`, `colisao_2d`, `explosao`) não mostram impulso
  nem a aterrissagem; a pessoa e o trilho são Three.js.
- **3d_threejs:** hook/E4-1 (manequim), F2 (cavalo CC0 da Quaternius, `assets_unidade/cavalo/`, ver LICENCA.txt). v4: o trilho (T3) saiu do 3D
  (pedido do Kaio: 2D/2,5D); o T1 é uma projeção 2,5D desenhada no Manim (`sec_momento.py`).
- **Status:** v4 preview silencioso 960×540 / 15 fps (teoria refeita: T1 de onde vem o momento, T5 impulso do caso constante às
  componentes; sem referências de livro na tela; sem voz, SRT, master nem entrega). Pergunta narrativa: "Por que dobrar os joelhos
  salva suas pernas?"
- **Fontes da especificação:** `handoff_v4.md` (com o adendo do trilho 2D) e `narracao_sugestao.md` (narração v4) sobre `handoff_v3.md` (tela, grade de layout, peças) sobre `handoff_v2.md` (física, tela, manequim, álgebra) e `narracao_sugestao.md` (narração v3 congelada; ids das
  âncoras). Histórico: `handoff_v1.md`, `narracao_sugestao_v2.md`, `ancoras_v1.json`, `_v1/` (lotes do v1).
- **Reservado para o yt_0016:** `_reservado_yt0016/` (C09–C13 do v1: conservação em sistemas, gelo, caçador, gases do rifle, Newton e a
  luz, inclusive o tanque de água em Three.js).

## Estrutura (v4)
hook H1–H3 (3D: manequim no muro) · abertura A1–A3 · T1 de onde vem o momento (2,5D: partícula numa curva no espaço, ΣF⃗ = m a⃗ →
d(m v⃗)/dt → p⃗ = m v⃗ → componentes → ΣF⃗ = dp⃗/dt) · T2 o fato experimental · T3 por que massa vezes velocidade (trilho 2D/2,5D) ·
T4 da conservação à terceira lei · T5 impulso (caso constante → integral → força média → componentes) · E1 bola na parede · E2 chute
em 2D · E3 força que cresce com o tempo · T6 momento ou energia? · E4 de volta ao muro (3D recuado no E4-1) · E5 a pulga · síntese
S1–S2 · encerramento F1–F2 (o cavalo e a corda → próximo vídeo: conservação do momento em sistemas).

## Cabeçalho e capítulos
Linha 1: `MECÂNICA · MOMENTO LINEAR E IMPULSO` (17, DIM, op. 0,5). Linha 2 = capítulo (30, branco). v4: sem selo de livro; os exercícios
têm um selo de ligação no lugar (20, DIM, op. 0,85): E1 TEOREMA DO IMPULSO · COM SINAL · E2 IMPULSO POR COMPONENTES · E3 IMPULSO COMO
INTEGRAL · T6 IMPULSO × TRABALHO · E4 DOIS CAMINHOS: TEMPO E DISTÂNCIA · E5 FORÇA DE CONTATO × RESULTANTE. Capítulos: DE ONDE VEM O
MOMENTO · O FATO EXPERIMENTAL · POR QUE MASSA VEZES VELOCIDADE? · DA CONSERVAÇÃO À TERCEIRA LEI · IMPULSO · EXERCÍCIO 1..3 · MOMENTO OU
ENERGIA? · EXERCÍCIO 4..5 · RESUMO. Selo DICA (cartão `#0E2A52`, borda `#7FB2FF`) em T5-9, E1-5, E2-4, T6-5 e E5-4. As fontes (livros)
vão só na descrição do YouTube (fim do `narracao_sugestao.md`).

## Semântica de cor
velocidade violeta `#9C8CFF` · momento p, P, Δp magenta `#EA63FF` · força (F, F_res, N, peso, F₁₍₂₎) `#5AA2FF` · impulso J e toda área sob
F(t) `#9CC7FF` · corpos e manequim em aço `#7A8696`/`#B8C4DA` · muro em concreto · geometria/eixos `#B8C4DA`/`#8FA3C4` · assunto do próximo
vídeo em ciano.

## Arquivos
`cena.py` (lotes: PH/PT2/PG4 camadas transparentes dos trechos 3D; PA abertura; PB T1; PC T2-5..T4; PD T5; PE E1–E3; PF T6; PG E4-2..E5;
PS síntese e fim) · `kit.py` (helpers, relógio por quadro, cabeçalho, DICA, silhueta e pulga 2D preenchidas) · `sec_*.py` (seções) ·
`ancoras.json` (de `gerar_ancoras.py`) · `threejs/` (`cena3d/muro.js` manequim e muro; `cena3d/c01.js` trilho; `timeline_{hook,e4,trilho}.json`
de `gerar_timelines.py`; `qa/muro_proj.js` projeções e alinhamento da cota) · `compor.py` (3D + Manim → H.264 CRF 14) ·
`render.sh`, `render3d_todos.sh`, `montar_preview.py`, `stills.sh`, `auditar.sh`, `prancha_v2.py`.

## QA (v2)
Áreas medidas no código: T5-5 meia-senoide 20,0000 e triângulo 20,0000 N·s; E4-2 560,000 e 560,000 N·s. Riemann T5-3: 20,523 → 20,129 →
20,008 N·s (4, 8, 32). Alinhamento da cota 3D × Manim: 0 px (câmera parada nas janelas). Camadas 3D: mesmo número de quadros (578, 1067, 228).

## QA (v3)
Áreas: T5-5 20,0000 e 20,0000 N·s; E4-2 em escala real 560 N·s nas duas (retângulo 56.000 N × 0,01 s; parábola de pico 5.880 N em 1/7 s;
medidas 560,03 e 560,000, a primeira pela amostragem do degrau). Auditorias (`AUDITORIA=1`): sobreposição, vazio (> 6 s), centralização
(|x| < 0,1) e pausas (> 8 s) zeradas em todos os lotes. Alinhamento 3D × Manim: hook e E4-1 0 px; trilho 1,9 px; F2 por projeção quadro a
quadro (`qa/proj_quadros.js`). Grade de layout em `kit.py` (PALCO, CONTA, CENTRO, DOIS PAINÉIS, LEGENDA, DICA).

## QA (v4)
Preview `renders/preview_yt0015_v4_960x540.mp4` (18:16, 16.439 quadros). Auditorias (`AUDITORIA=1`, todos os lotes 2D): vazio, centro e
"só álgebra" (novo: intervalo > 2 s sem objeto não textual) zerados; sobreposição: só v⃗ × Δv⃗ (0,06 × 0,08) no T1-2 e a cópia do T5-2 que
nasce em cima da original e desliza. Trechos parados (`medir_parado.py`, quadro a quadro no vídeo): 1 acima de 6 s (hook, 5,2–13,2 s,
3D do H1). Áreas: T5-7 meia-senoide, triângulo e retângulo da média 20,0000 N·s; E4-2 560,03 (amostragem do degrau; exato 560) e
560,000 N·s; Riemann T5-5 20,523 → 20,129 → 20,008. Alinhamento: hook e E4-1 0 px (projeções fixas), F2 por quadro, T1 desenhado no
Manim (0 px por construção), T3 sem 3D. `grep MOYSÉS|SEARS|FEYNMAN *.py` → nada.
Novos: `sec_momento.py` (T1), `sec_trilho.py` (T3 2D), `medir_parado.py`, `stills_v4.sh`; lotes do v4: PH · PA · PT1 · PB · PT3 · PC ·
PD · PE · PF · PG4 · PG · PS · PF2 (o PT2/trilho 3D saiu da montagem). Código do v3 guardado em `_v3/`.

## QA (v5 — polimento de tela, handoff_v5.md)
Preview `renders/preview_yt0015_v5_960x540.mp4` (18:16). Lotes refeitos: PT1, PT3, PC, PD, PE, PF, PG + 3D do hook (dolly-in −8% e
balanço de peso) e do cavalo (corda num gancho na traseira) com as camadas PH/PF2. T1: poses s = 3,674 (96,9°; |v⃗| 1,76; |ΣF⃗| 1,77),
3,940 (90,3°; 1,71; 1,95) e 3,500 (93,4°; 1,79; 1,52); pior folga de rótulo 0,14; pior vetor 0,91 com ponta/comprimento 0,20.
Órfãos (`Base.orfaos`, a cada âncora): zero em todos os lotes — causa achada: animar um VGroup de glifos de uma equação já em cena
(Indicate/Write/FadeIn de um pedaço) quebra a equação; `Base._reparar` remonta depois de cada play. Parados > 6 s: zero. Só álgebra: zero.
Sobreposição: só a cópia do T5-2 no primeiro quadro (idêntica à original).
