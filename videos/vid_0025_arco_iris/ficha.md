# Por que o arco-íris tem 42°?

- ID: `vid_0025`
- Pasta: `videos/vid_0025_arco_iris/`
- Série pública: **DA EQUAÇÃO AO FENÔMENO · EP. 07**
- formato: `curto_vertical`
- Área: Física IV / Óptica geométrica
- Mapa curricular: §7.2 — reflexão, refração e lei de Snell
- Headline: `POR QUE O ARCO-ÍRIS TEM 42°?`
- Pergunta central: Por que o arco-íris aparece sempre a 42° da sombra da sua cabeça?
- Payoff: dentro da gota, o ângulo de saída da luz tem um máximo; perto dele os raios se amontoam, e esse máximo vale 42°.
- Duração narrativa alvo: ~180–190 s (preview silencioso segue a grade C01–C11 de ~168 s; a cena se estica na fase de voz).
- solido_3d: nenhum — o raio vive num plano que passa pelo centro da gota (o corte 2D é exato) e o arsenal não tem gota nem cone de visão; o cone de 42° do C10 sai do próprio Manim (2.5D).
- Fase aberta (24/10/2026): implementação Manim + preview silencioso completo 540×960 / 15 fps. Voz, SRT, master, capa e publicação ainda não abertos.
- Classe: `ArcoIris025` em `cena.py`.

## Modelo físico

Gota esférica de raio R, luz solar paralela (propagação esquerda → direita), raio incidente
caracterizado pela altura b ao eixo, índice de refração da água n, uma única reflexão interna
(arco primário). Com x = b/R:

```
sin i = b/R                 i = asin(b/R)
sin i = n sin r             r = asin((b/R)/n)
D = 180° + 2i − 4r          (entrada + reflexão + saída)
θ = 180° − D = 4r − 2i      (ângulo a partir da direção antissolar)
```

Uma única implementação dessa física (helpers puros em `cena.py`) alimenta raios desenhados,
gráfico θ × b/R, destaques e verificações. A trajetória de cada raio é calculada por interseção
reta–circunferência, refração vetorial (Snell) e reflexão vetorial; nada é posicionado a olho.

## Solução verificada

- Máximo: dθ/di = 0 → dr/di = 1/2 → cos i = (n/2) cos r → cos² i = (n² − 1)/3.
- n = 1,333: i_max ≈ 59,41°, r ≈ 40,2°, θ_max ≈ 42,08°, b/R = sin i_max ≈ 0,861. Tela: 59,4° · 40,2° · 42,1°.
- Dispersão: vermelho n ≈ 1,331 → θ_max ≈ 42,4°; violeta n ≈ 1,343 → θ_max ≈ 40,6°. Vermelho por fora, violeta por dentro.
- Amontoamento: 0,793 ≲ b/R ≲ 0,913 → raios a menos de ~1° do máximo; em área do disco incidente, 0,913² − 0,793² ≈ 0,205 (≈ um em cada cinco). Fração geométrica de raios, não potência/intensidade (Fresnel fora).
- Leque de C06/C07: N = 25 amostras equiponderadas em área, b_k/R = sqrt((k − 0,5)/25); exatamente 5 de 25 caem na faixa do amontoamento (b/R = 0,812 · 0,837 · 0,860 · 0,883 · 0,906).
- Raio central demonstrativo separado: b/R = 0 → θ = 0 (não entra na contagem 5 de 25).
- Casos de checagem: b = 0 → θ = 0; b/R = 1 → θ ≈ 14,4°.

## Hipóteses

Gota esférica, luz paralela, uma reflexão interna (arco primário).
Fora do vídeo: arco secundário (~51°), faixa escura de Alexandre, refletância/transmitância de Fresnel.

## Orientação espacial (não espelhar)

Eixo x da cena esquerda → direita; luz solar propaga esquerda → direita. SOL (esquerda) → OBSERVADOR → GOTAS (direita).
Raio protagonista entra na metade superior (b > 0) e sai para a esquerda e para baixo, a ~42,08° da direção
de retroespalhamento, em direção ao observador. O zoom C01 → C02 e a volta C09 → C10 preservam essa orientação.

## Checagens (QA desta rodada)

QA-01 Snell no raio protagonista · QA-02 máximo (i ≈ 59,41°, θ ≈ 42,08°, b/R ≈ 0,861) · QA-03 r ≈ 40,2° ·
QA-04 curva cresce/achata/máximo/cai · QA-05 nenhum raio com θ > 42,1° · QA-06 raio central θ = 0 ·
QA-07 leque ponderado em (b/R)² · QA-08 exatamente 5 de 25 na faixa · QA-09 20,5% só como fração geométrica ·
QA-10 dispersão e ordem das cores · QA-11 orientação · QA-12 cone de 42° → círculo · QA-13 Sol > 42° → arco abaixo do horizonte.
Resultados no relatório de entrega da rodada.

## Preview silencioso — rodada 1 (24/10/2026)

- Render: `media/videos/cena/960p15/ArcoIris025.mp4` (cópia em `renders/preview_r3_ArcoIris025.mp4`), 540×960, 15 fps, 147,8 s, 2.217 quadros, sem áudio.
- Marcas de estado (s): C01 0 · C02 12,9 · C03 17,8 · C04 25,2 · C05 36,0 · C06 53,9 · C07 71,0 · C08 83,6 · C09 103,8 · C10 116,3 · C11 138,4 · fim 146,9.
- Pranchas e zip para avaliação: `renders/preview_r3_prancha_0N.png`, `renders/preview_r3_para_gpt.zip` (temporários, não versionar).
- Teste do arsenal: não se aplica (solido_3d: nenhum).

## Preview silencioso — rodada r4 (24/10/2026)

- Render: `media/videos/cena/960p15/ArcoIris025.mp4` (cópia em `renders/preview_r4_ArcoIris025.mp4`), 540×960, 15 fps, 211,3 s, 3.169 quadros, sem áudio.
- Marcas (s): C01 0 · C02 12,5 · C03 20,9 · C04 32,2 · C05 49,1 · C06 77,7 · C07 98,2 · C08 116,4 · C09 158,2 · C10 174,3 · C11 199,1 · fim 208,6.
- Gancho com geometria lateral coerente (abertura medida = 42,078°); C05 com viradas e álgebra em estados; C07 com detalhe angular ×10 e contagem por 1°; C08 com derivação completa até cos²i = (n²−1)/3; C10 com indicador solar separado. Detalhes e pendências em `relatorio_r4.md`.
- Pranchas e zip: `renders/preview_r4_prancha_0N.png`, `renders/preview_r4_para_gpt.zip` (temporários).

## Preview silencioso — rodada r4b (25/10/2026)

- Teto pedido pelo usuário: abaixo de 3 min (máx. 2:59). Fator de andamento global PACE = 0,82; sem remover estados.
- Render: `media/videos/cena/960p15/ArcoIris025.mp4` (cópia em `renders/preview_r4b_ArcoIris025.mp4`), 540×960, 15 fps, **172,99 s**, 2.595 quadros, sem áudio.
- Marcas (s): C01 0 · C02 10,0 · C03 16,7 · C04 25,7 · C05 39,4 · C06 62,2 · C07 78,8 · C08 93,4 · C09 126,0 · C10 138,6 · C11 158,5 · fim 166,0.
- Atenção para a fase de voz: a narração congelada tem ~180–190 s e o preview tem 173 s; resolver na voz sem passar de 2:59.

## Preview silencioso — rodada r5 (25/10/2026)

- Pedido do usuário: referencial dos 42° mais didático (em relação a quê, por que semicírculo), pessoa/Sol/gota mais bonitos, tudo em maiúsculas Space Grotesk como nos longos (yt_0009+), nada sobreposto, vídeo abaixo de 2:59.
- Render limpo: `media/videos/cena/960p15/ArcoIris025.mp4` (cópia em `renders/preview_r5_ArcoIris025.mp4`), 540×960, 15 fps, **173,93 s**, 2.609 quadros, sem áudio.
- Marcas (s): C01 0 · C02 14,4 · C03 20,5 · C04 29,5 · C05 42,7 · C06 66,6 · C07 80,9 · C08 94,8 · C09 129,1 · C10 140,5 · C11 167,3 · fim 173,9.
- Auditor de sobreposição no próprio `cena.py` (texto×texto, texto×traço, quadro, faixa inferior): zero avisos no render final. Detalhes em `relatorio_r5.md`.

## Preview com voz — rodada r6 (25/10/2026)

- Voz ElevenLabs v4 (narracao_tags_v5.md → audio/narracao_v5.wav, 146,2 s) + nova abertura animada + sincronização por 70 âncoras (alinhamento forçado palavra a palavra).
- Vídeo: `renders/vid_0025_preview_com_voz.mp4`, 540×960, 15 fps, **150,996 s (2:31)**, 2.265 quadros. Atraso máximo medido entre imagem e palavra: +0,016 s (meta ≤ 0,2 s); a imagem começa 0,07–0,13 s antes da palavra.
- Pipeline: `alinhar_voz.py` → `gerar_ancoras.py` → `MEDIR=1` (nat.json) → `plan_sync.py` (sync.json + audio/narracao_sync.wav) → render → `conferir_ancoras.py`. Detalhes em `relatorio_r6.md`.

## SRT — fase aberta em 25/10/2026

- `legenda.srt` (69 blocos, até 2 linhas de 30 caracteres) gerado por `gerar_legenda.py` a partir do alinhamento forçado, já no tempo do vídeo (voz + 9 pausas de `sync.json`); nenhum bloco atravessa uma pausa.
- Validação: texto do SRT idêntico ao texto narrado (sem tags), sem sobreposição, cada bloco começa na palavra falada (±0,08 s), maior linha 30 caracteres, velocidade de leitura média 16,3 e máxima 20,4 caracteres/s, último bloco termina em 149,8 s (vídeo 150,98 s).
- Legendado embutido, master final e capa continuam fechados.

## Entrega final — 25/10/2026

- Master e legendado colorido 1080×1920/30 fps, CRF 14,0, 150,84 s; sincronia medida a 30 fps (atraso máx. −0,007 s). Entregue em `entregas/Da Equação ao Fenômeno - EP 07 - Por que o arco-íris tem 42° - 0025/`. Detalhes em `relatorio_final.md`.
- Capa e publicação continuam fechadas.
