# Por que o campo não escapa do toroide?

formato: curto_vertical

Série pública: **POR TRÁS DA FÓRMULA · EP. 09** (aprovado pelo Kaio em 2026-10-26; slot conferido: não há `vid_0025`–`vid_0028`, último EP. da série é o 08 em `vid_0022`)

Fase: **final entregue (2026-10-27)**. Master e legendado 1080×1920 / 30 fps, CRF 14, 144,9 s, em
`entregas/Por Trás da Fórmula - EP 09 - Por que o campo não escapa do toroide - 0029/`. Voz ElevenLabs v4 (Dioke), narração V2;
sincronia por palavra (Scribe) em `sincronizar.py` → `timeline.json` (59 eventos, pior atraso +0,02 s); legenda `--style compacto`
com cores das grandezas (`legenda_cores.py`). Sem publicação.

- Unidade: `vid_0029`. Classe Manim: `CampoToroide029`.
- Primeiro teste do pipeline **Three.js (3D dinâmico) + Manim (passo a passo 2D e álgebra)**.
- Duração: animação-base v1 172 s; v2 (handoff de correções) 185 s; v3 (elos e faixa de legenda) 195 s; final com voz entre 175 e 200 s.
- v3: elos símbolo ↔ desenho (`kit.elo`); faixa da legenda reservada (y de −4,67 a −6,0, nada abaixo de −4,5);
  vista de cima reescalada (fator 3,0/2,1, centro em y = 3,3).
- v2: corrente = 3 rastros de luz verdes (sem tracinhos); campo = pulsos magenta correndo nos anéis (velocidade ∝ 1/r);
  modo "contagem" (`realce_3d`) recua o 3D na vista de cima; vetores B e dℓ no Manim; gráfico B(r) com o eixo r alinhado à vista de cima.

solido_3d: toroide_corrente

Portado para Three.js (o Blender não é usado nesta unidade). Parâmetros da ficha do arsenal: `raio_maior = 1.6`, `raio_menor = 0.5`,
`raio_fio = 0.04`, `nucleo = 0`, `eixo = 0`; **exceção aprovada: `n_espiras = 24`** (legibilidade dos ⊙/⊗ no celular; o N da conta é simbólico).
Cores do padrão dos longos, não as da ficha: fio aço `#7A8696`, corrente verde `#3FE08B`, B magenta `#EA63FF`, geometria `#B8C4DA`.

## Física (especificação do briefing)

- Toroide ideal, seção circular, N espiras apertadas, corrente I, raio médio R, raio da seção a, núcleo de ar; eixo z.
- Simetria: no toroide ideal, o campo acompanha círculos em torno do eixo e tem o mesmo módulo em cada círculo.
- Ampère num círculo de raio r: B·2πr = μ₀ I_enc. Buraco: 0. Enrolamento: B = μ₀NI/(2πr). Fora: NI − NI = 0.
- Dentro não é uniforme: razão das bordas (R + a)/(R − a) = 2,1/1,1 ≈ 1,9. Caso-limite a ≪ R: B ≈ μ₀ n I, n = N/(2πR).
- Sentidos: corrente sobe (+z, ⊙) no lado de dentro e desce (−z, ⊗) no lado de fora; amperiano anti-horário visto de cima;
  B anti-horário visto de cima.
- Campo desenhado = modelo ideal (anéis concêntricos ao eixo, só dentro da seção, brilho e tamanho ∝ 1/r). Nada de Biot–Savart da hélice.

## Pipeline

- `timeline.json`: fonte única de tempos (beats, eventos, flashes, chaves de câmera e do raio do amperiano).
- `cena3d/` (`index.html`, `cena3d.js`, `three.min.js` r128, `RoomEnvironment.js`): `window.setFrame(f)` determinístico.
- `render3d.js` (Node + `playwright-core` 1.55.0, `package.json` da unidade; usa o Chromium já instalado): PNGs em `frames3d_540x960/`.
- `cena.py`: camada Manim transparente (`-t`, `.mov` com alfa), sem imagem do 3D.
- `compor.py` (PyAV, sem ffmpeg de linha de comando): `parte3d.mp4` e o preview composto.
- Vista de cima alinhada: fator 3D → Manim = 3,6/2,1; centro do toroide em (0; 2,2); R − a → 1,886; R → 2,743; R + a → 3,600.
  Espira k cruza o plano z = 0 em φ = 2πk/24 (lado de dentro, ⊙) e em φ = 2π(k + ½)/24 (lado de fora, ⊗), φ₀ = 0.
