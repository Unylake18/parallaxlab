# Three.js + Manim: guia do pipeline

Estado: **experimental** (2026-10-27). Nasceu do demo do solenoide e do curto de teste vid_0029 (campo do toroide, V2
aprovada no visual, V3 em produção). Ainda não é padrão do canal: `template/`, `docs/` e `AGENTS.md` não mudaram.

## A ideia em uma linha

**Three.js mostra o objeto e o fenômeno (3D dinâmico, fundo); o Manim faz vetores, rótulos e álgebra (2D, por cima,
com fundo transparente).** Os dois leem o mesmo `timeline.json` e são compostos quadro a quadro.

- Three.js = o sólido, a corrente passando, o campo "vivo", a câmera girando.
- Manim = tudo que precisa ser exato e explicado: setas de grandeza, rótulos, equações, gráficos, legendas de cena.
- Remotion: adiado. Só entra se timeline + composição em Python virar gargalo.
- Blender (arsenal): continua válido para quadros estáticos ou sequências pré-renderizadas; o Three.js ficou mais
  fluido e mais rápido de iterar. Portar um sólido do arsenal = reescrever o construtor em JS dentro do `cena3d.js`.

```
timeline.json ──┬──> cena3d/ (Three.js) ──render3d.js (Chromium headless)──> frames3d_WxH/f00000.png ...
                └──> cena.py (Manim, -t) ─────────────────────────────────> CenaX.mov (com alfa)
                                         compor.py (PyAV, H.264 CRF 14) ──> renders/preview_WxH.mp4
```

## O que tem nesta pasta

| Pasta | O que é |
|---|---|
| `modelo/` | **Ponto de partida.** Unidade mínima que funciona: anel de aço com rastro verde, anel de campo, câmera órbita → vista de cima, círculo do Manim alinhado por cima e uma equação acima da faixa de legenda. 8 s. |
| `novo_video.py` | Copia o `modelo/` para `videos/vid_NNNN_nome/` com o Three.js dentro. |
| `vendor/three-r128/` | `three.min.js` e `RoomEnvironment.js` (r128) locais. O render não depende de CDN. |
| `exemplo_toroide/` | Snapshot da **camada 3D** do vid_0029 V2 (cena3d, timeline, render, compor, QA) + briefing, handoffs v2/v3 e relatório. Referência das receitas completas (setas girando, contagem dentro/fora, círculo amperiano). A unidade final `videos/vid_0029_*` (com o `cena.py`) entra no repositório depois. |
| `solenoide/` | Primeiro demo (solenoide, tudo num `cena3d.html`). Histórico; o modelo já incorpora o que deu certo. |

## Preparar um PC novo (uma vez)

1. Repositório e `.venv` do canal como sempre (`uv run python -m manim ...` precisa funcionar). Nada novo no Python:
   o `compor.py` usa `av`, `numpy` e `Pillow`, que já vêm com o Manim.
2. **Node.js** LTS (18 ou mais novo): <https://nodejs.org>. Conferir com `node -v`.
3. Chromium do Playwright, na versão casada com o `playwright-core` do `package.json`:
   ```
   npx -y playwright@1.55.0 install chromium
   ```
   (Se preferir outro Chrome/Chromium, aponte com a variável `CHROMIUM_PATH`.)
4. GPU: no Windows o `render3d.js` usa ANGLE/Direct3D 11 (`--use-angle=d3d11`), rápido (~0,14 s/quadro em 1080×1920).
   Em Linux/macOS cai para SwiftShader (CPU): mesmo resultado, mais lento.

## Fazer um vídeo novo

Na raiz do repositório (PowerShell ou bash):

```
uv run python experimentos/threejs/novo_video.py vid_0031_nome_curto
cd videos/vid_0031_nome_curto
npm install                              # baixa só o playwright-core (node_modules fica fora do Git)
node render3d.js --quadros 0,45,100      # 3 quadros para olhar (frames3d_540x960/)
node render3d.js                         # todos os quadros do preview 540×960 a 15 fps
node qa/alinhamento.js                   # erro 3D × Manim na vista de cima (esperado ≤ 2 px; o modelo dá 0)
cd ../..
```

Camada Manim (fundo transparente) e composição — bash:

```
MEDIA_DIR=videos/vid_0031_nome_curto/media_preview uv run --no-sync python -m manim -t -r 540,960 --fps 15 videos/vid_0031_nome_curto/cena.py CenaModelo
uv run --no-sync python videos/vid_0031_nome_curto/compor.py --classe CenaModelo
```

PowerShell: `$env:MEDIA_DIR="videos/vid_0031_nome_curto/media_preview"` numa linha e o comando do Manim na seguinte.

Saída: `renders/preview_540x960.mp4` (composto) e `renders/parte3d_540x960.mp4` (só o 3D). Use `--sufixo v2` para não
sobrescrever versões. Final: `node render3d.js --w 1080 --h 1920 --fps 30`, Manim com `-r 1080,1920 --fps 30` e
`compor.py --res 1080x1920 --fps 30`.

Ordem de trabalho que funcionou no vid_0029: briefing → `timeline.json` com beats e eventos → 3D só com quadros
soltos (`--quadros`) até a câmera e o objeto ficarem certos → Manim → composição → voz → ajustar só o timeline →
re-renderizar os dois.

## Regras do pipeline (por que cada coisa é assim)

1. **Tudo é função do quadro.** `window.setFrame(f)` desenha o quadro `f` a partir de `t = f/FPS`. Nada de
   `requestAnimationFrame`, `Date.now()` ou estado acumulado entre quadros: é isso que deixa o render determinístico e
   permite renderizar quadros soltos.
2. **Uma fonte de tempo.** Todo instante mora no `timeline.json` (beats, eventos, chaves da câmera). O `cena.py` usa
   `ate(E["evento"])` em vez de números soltos, e as funções de suavização são as mesmas nos dois lados
   (`suave = 3u² − 2u³`). Depois da voz, só o timeline muda.
3. **Mesmo número de quadros.** O `compor.py` avisa se o `.mov` do Manim e os PNGs do 3D não batem.
4. **Alinhamento 3D ↔ Manim por dolly-zoom.** O quadro do Manim tem 16 unidades de altura. Na vista `topo`:
   `altura_visivel = 16 / K` e a câmera fica a `D = (altura_visivel/2) / tan(fov/2)` do plano z = 0. Com isso um
   ponto 3D `(x, y, 0)` cai no Manim em `(cx + K·x, cy + K·y)`, onde `K = fator_3d_manim` e `(cx, cy) =
   centro_topo_manim`. O deslocamento vertical do alvo é feito com `camera.setViewOffset(W, H, 0, cy/16·H, W, H)`, sem
   inclinar a câmera. Fov pequeno (8°) na vista de cima = quase ortográfico, o círculo do Manim casa com o anel.
   Confira sempre com `qa/alinhamento.js` (usa `window.projeta`).
5. **Estrelas numa cena separada**, desenhada antes, para não "zoomarem" durante o dolly.
6. **Cores do Three r128:** ele trata hex como linear e a saída como sRGB; sem conversão as cores saem lavadas. O
   modelo converte com `new THREE.Color(hex).convertSRGBToLinear()` e mantém `envMapIntensity` baixo.
7. **Determinismo do render:** `preserveDrawingBuffer: true`, `setPixelRatio(1)`, `deviceScaleFactor: 1`.

## Receitas visuais (decididas nas avaliações)

- **Corrente = rastro de luz verde** (#3FE08B) correndo pelo tubo, não partículas. Shader ao longo de `uv.x` do tubo:
  brilho `exp(−Δ/τ)` atrás da cabeça, cabeça ~30% mais clara. 1 a 3 rastros por espira. No V1 do toroide, ~150
  tracinhos deixaram a tela poluída; o rastro resolveu (V2 aprovada). Nos longos 2D, a corrente é tracinho/flash
  verde, nunca bolinha.
- **Campo B = magenta** (#EA63FF): anéis finos com pulsos que andam; velocidade ∝ intensidade (no toroide, ∝ 1/r).
- **Modo contagem / "o 3D recua":** quando o Manim precisa da atenção (contar espiras, escrever a equação), o
  `realce_3d` (0 → 1) escurece e dessatura o 3D sem tirá-lo da tela.
- **Paleta:** aço #7A8696, geometria/linhas de construção #B8C4DA, texto apagado #8FA3C4, fundo #050816, painel
  #0E2A52 com borda #7FB2FF. Sem azul/ciano decorativo; violeta só para velocidade.
- **Equação ligada ao desenho (lição da V2 → V3):** cada símbolo que entra na tela pisca junto com o seu gêmeo no
  desenho (B ↔ setas magenta, r ↔ seta do raio, 2πr ↔ contorno, I_enc ↔ fios que atravessam o disco, N ↔ anel de
  ⊙). Detalhes no `exemplo_toroide/pautas/vid_0029_v2_avaliacao_e_handoff_v3.md`.

## Faixa de legenda (curto vertical)

Reserve `y_px` 760–840 em 540×960 (Manim y −4,67 a −6,0) para a legenda queimada; o conteúdo da cena fica acima de
y = −4,5. O `timeline.json` do modelo guarda isso em `legenda`, e o `cena.py` do modelo dá erro se uma equação invadir
a faixa. Conferir num quadro de teste no Reels antes de fechar.

## O que não vai para o Git

`node_modules/`, `frames3d_*/`, `media/`, `media_preview/`, `renders/` (ver `.gitignore`). Tudo é regenerável a partir
do código + timeline. Vídeos finais seguem para `entregas/` pelo fluxo normal (`videos/entregar.py`).

## Pendências conhecidas

- O modelo é vertical 9×16. Para um longo 16×9 é preciso trocar o quadro no `cena.py`, no `render3d.js` (w/h) e no
  QA (as constantes 9 e 16).
- Portar os sólidos do arsenal Blender: um por vez, depois de fechar cores e aparência no vid_0029.
