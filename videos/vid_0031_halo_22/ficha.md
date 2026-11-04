# Por que o anel do Sol tem 22°?

formato: curto_vertical
Série pública: **DA EQUAÇÃO AO FENÔMENO · EP. 09** (confirmado no handoff v2)
disciplina: Física IV
bloco: Óptica
modulo: 7.2 Óptica geométrica (dispersão e prismas)
referencia: Moysés vol. 4 e Sears Física IV, prisma e desvio mínimo (seções a conferir)
3d_threejs: C01 céu azul com o halo que acende de dentro para fora, Sol com núcleo pequeno e flare, push-in 1,00 → 1,10 e mergulho no cristal (sem poste, sem chão, sem lugares); C02 coluna hexagonal 3D na lupa (gelo azulado); C04 câmera sobe do chão quente de verão até o véu, cristais só no alto; C05–C08 e C11 só o volume do cristal (corpo, contorno, feixe e Sol em vetor no Manim); fim do C09 o cone vira o céu do C01 (fusão); C10 zoom na borda do halo; C11 céu no terço de cima (anel ≥ 3,6)
solido_3d: nenhum do arsenal Blender; prisma hexagonal feito direto em Three.js (prisma_triangular do arsenal só como referência de material e arestas)
Fase: preview silencioso v6 (handoff v6: hook com HALO SOLAR DE 22° / COMO ELE SE FORMA?, texto sem caixa, Sol redondo inteiro, cristal com corpo de gelo, C05 centrado com o feixe atravessando, caderno na álgebra do C06/C08, o cone saindo da pessoa no C09, índices do gelo de Warren & Brandt 2008, síntese na tela toda, ≤ 178 s) + stills 1080×1920

## Física (congelada no handoff v1)

- Prisma hexagonal regular, n = 1,31 (v6, cores: vermelho 1,3079 a 656 nm e violeta 1,3190 a 405 nm, Warren & Brandt 2008). Snell vetorial e reflexão total reais; sem Fresnel/difração.
- Caminho de 60° (face de entrada → face alternada): D = i₁ + i₂ − 60°; D_min = 21,84° em i₁ = i₂ = 40,92°, r₁ = r₂ = 30°.
- Fundo achatado: D < 22,84° ⇔ 30,7° < i₁ < 52,1°. Cores (v6): vermelho 21,68° (dentro), violeta 22,52° (fora).

## Pipeline

- `fisica.py`: funções puras (`desvio`, `saida`, `par_invertido`, `d_min`, traçado vetorial `tracar`/`caminho60`, histograma
  `amostra_desvios`, `perfil_anel`; v2: `theta_arco_iris`, `projecao_orientacoes`) e o QA da §10 + asserts do §B.3 (`uv run python videos/vid_0031_halo_22/fisica.py` → `qa/checagens.txt`).
- `arte_vid0025.py` (v4): pessoa, Sol e chão copiados do vid_0025 (main 84de462f) + espelhamento da pessoa.
- `roteiro.py` (v5): fonte única de tempos (orçamento ≤ 178,5 s), câmera do céu (hook: `LUGARES`, `ESC_HOOK`, `MERGULHO`),
  cena de lado com o Sol grande (`SOL_L`, `SOL_LR`, `ini_no_disco`, `d_perp`; todo raio nasce no disco) e estado do cristal e do
  feixe por quadro (`estado_cristal`; o feixe nasce no contorno do Sol `sol_cr`).
- `gerar_timeline.py` → `timeline.json`: tempos (estimados pela fala), chaves das camadas 3D, câmera do céu (pitch 25°,
  FOV horizontal 60°, retilínea), centro do Sol (v2: y = 1,667, y_px ≈ 380), ponto da borda interna, curvas de 22° e 24°
  projetadas e perfil do anel (v2: tom de apresentação `tom_v2`, borda interna quente e fina, corpo branco-azulado).
- `cena3d/` (`index.html`, `cena3d.js`, `three.min.js` r128, `RoomEnvironment.js`): `window.setFrame(f)` determinístico.
  Céu = quad de tela cheia; halo = função do ângulo à direção do Sol (cone exato). Close: coluna com eixo em z, câmera
  termina olhando ao longo do eixo no `close_fim`.
- `render3d.js` (Node + `playwright-core` 1.55.0): PNGs em `frames3d_540x960/`.
- `cena.py` (`HaloSol031`): camada Manim transparente (`-t`).
  `uv run python -m manim -t --disable_caching -r 540,960 --fps 15 videos/vid_0031_halo_22/cena.py HaloSol031`
  (`--disable_caching` é obrigatório: com o cache, o Manim reaproveitou partes antigas e o .mov saiu com 38 quadros a mais.)
  Modo seco (tempos + geometria do QA em segundos, sem desenhar): `SECO=1 uv run python -m manim --dry_run --progress_bar none -r 540,960 --fps 15 …`
- `compor.py`: `renders/parte3d_540x960.mp4` e `renders/preview_540x960.mp4`.
- `qa/sobreposicao.py` → `qa/sobreposicao.txt` (caixas de texto × traços, nos estados marcados com qa na cena);
  `qa/quadros.py` → `qa/quadros/*.png` + `qa/prancha_preview_v5.png`; `qa/stills.py` (stills 1080×1920); `qa/antes_depois.py`
  (prancha antes × depois v4 → v5). `qa/sobreposicao.py` v5 inclui (i) origem dos raios, (j) tempo parado das equações,
  (k) área vazia e (l) cinza no cristal.
- `qa/alinhamento.js` (`NODE_PATH=node_modules node qa/alinhamento.js`): alinhamento 3D × Manim → `qa/alinhamento.json`.

## Fase v7 (handoff de 2026-11-02) — preview silencioso 540×960 / 15 fps

- Orçamento por cena = fala final (509 palavras ≈ 178,6 s; `narracao_sugestao.md`): C01 10,5 · C02 21,1 · C03 10,2 · C04 9,8 · C05 11,2 · C06 29,5 · C07 11,9 · C08 28,1 (≈ 29) · C09 16,8 · C10 14,4 · C11 15,1.
- C05: hexágono em (1,55; 0,9), circunraio 2,6; o feixe entra pelo meio de uma face nos três casos; o Sol (R 0,46) fica a ≥ 2,4 do contorno; lista fixa embaixo (oposta / vizinha / alternada).
- C09: a pessoa cresce (H 2,55 ≈ 17 % da tela), 48 linhas de visão, cone preenchido, eixo olho → Sol, giro 2.5D até o anel do C01.
- 3D: lupa do C02 gira 360° em 4 s com corpo; C04 com céu mais escuro e 38 cristais maiores de aresta clara (cilindros).
- Física congelada (`fisica.py` sem alteração; n = 1,3079 / 1,3190).

## Fase v8 — voz + sincronia (2026-11-02)

- Texto v2 (564 palavras, `narracao_tags.md`); voz `eleven_v4`, `qw7jgPZWOKrl10GsjQ82` → `audio/narracao_v4.wav` (175,1 s; a primeira voz, do texto v1, está em `audio/narracao_v4_texto_v1_158s.wav`).
- `alinhar_voz.py` → `alinhamento_palavras.json`; `gerar_ancoras.py` → `ancoras.json` (71 âncoras); `plan_sync.py` → `sync.json` (eventos remapeados, escala por trecho, pausas) e `audio/narracao_sync.wav` (178,06 s; 2,5 s de pausas).
- Preview com voz: `renders/preview_v8_voz_540x960.mp4` (178,07 s). Atraso da imagem em relação à palavra: máx. −0,02 s, média −0,10 s (59 âncoras medidas).

- Legendado (2026-11-04): estilo `semcaixa` de `videos/montar_legendado.py` (negrito, contorno 3 px, sem a caixa semitransparente do estilo padrão), cores por `legenda_cores.py`.
