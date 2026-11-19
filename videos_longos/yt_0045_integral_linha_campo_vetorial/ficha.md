# Integral de linha de um campo vetorial

Série pública: **CÁLCULO III · EP. 20** (número yt_0045 e EP. 20 provisórios até o Kaio confirmar)

```
formato: longo_horizontal
tipo: teoria
serie_publica: CÁLCULO III · EP. 20
titulo: Integral de linha de um campo vetorial
disciplina: Cálculo III
modulo: 3.6 Integrais de linha
bloco: 3.6-T1
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §6.1 e §6.2 (definição, outra notação, Ex. 1 e 2); didática do Stewart. Livro só na descrição do YouTube
unidades: nenhuma na tela (exemplos adimensionais). t é o PARÂMETRO da curva; na fala ele é o tempo da conta (escolha de percurso: no círculo e na hélice o ângulo cresce junto com t), e γ′ é chamada de velocidade nesse sentido. Não escrever segundos, s nem unidade de t em lugar nenhum
notacao: γ curva (laranja), γ′ velocidade (violeta), F campo com componentes P, Q, R (verde-menta), Δγᵢ e dγ deslocamentos (violeta), t parâmetro, a ≤ t ≤ b, g(t) = F(γ(t))·γ′(t), W trabalho, α ângulo entre F e o deslocamento, R raio (só nos exemplos 2D) e 3ª componente (só no cartão geral do B6-1), c subida da hélice por unidade de t (z = c t), n número de pedaços. Sem θ, sem ds
solido_3d: nenhum do arsenal Blender
3d_threejs: nenhuma (lata e helice em projecao obliqua 2D, ver handoff v2)
duracao_alvo: ≈ 19:00 (narração v1: 3.390 palavras)
duracao_real: 17:50,23 (voz 17:48,96; narração v1.2: 3.424 palavras a 3,20 palavras/s)
```

## Estado (Preview v1 — handoff v1.1, 2026-11-18)

Unidade-base (somente leitura): `videos_longos/yt_0044_exercicios_integral_tripla/` — a `ficha.md` dela registra o preview v1 com os 9 lotes
aprovados no QA (26/26 alvos, GM1–GM21, R5 = 0, flash = 0). Reutilizados sem mudança: `kit.py`, `v41.py`; adaptados: `k44.py` → `k45.py`
(macros do keys45.js, palco 2D `Vista2D`/`eixos2`/`campo`/`papel_vista`, QA R21 e calibração), `c44.js` → `c45.js` (cenas helice, heliceCampo,
heliceLeitura), scripts `render/render3d/seco/still/stills_lote.sh`, `montar.py`, `quadros.py`, `gerar_ancoras.py`, `compara.py`, `qa44.py` → `qa45.py`.

| Ordem | Lote | Âncoras | Quadros (15 fps) | Duração (s) | Render 540p15 | 3D (s/quadro) | QA | Pendências |
|---:|---|---|---:|---:|---|---|---|---|
| 1 | PB4 | B4-1 a B4-3 | 2.826 | 188,40 | 57 s | 2D | aprovado (alvos 07–09; GM3–GM5; palco 2D 0,00 px) | B4-2 termina em n = 16 (a fala vai 4 → 8 → 16; o alvo mostra n = 8) |
| 2 | PB7 | B7-1 a B7-3 | 2.732 | 182,13 | 89 s | 37 s; 0,121 | aprovado (alvos 14–16; GM10–GM11; alinhamento 0,000 px) | — |
| 3 | PB1 | B1 | 1.022 | 68,13 | 19 s | 2D | aprovado (alvo 03) | — |
| 4 | PB2 | B2-1, B2-2, B3 | 3.258 | 217,20 | 67 s | 2D | aprovado (alvos 04–06; GM1–GM2) | — |
| 5 | PB5 | B5-1, B5-2 | 1.769 | 117,93 | 37 s | 2D | aprovado (alvos 10–11; GM6–GM7) | rótulo γ(−1) em x = 54 (no alvo encosta em x = 20, fora da margem) |
| 6 | PB6 | B6-1, B6-2 | 2.464 | 164,27 | 52 s | 2D | aprovado (alvos 12–13; GM8–GM9) | 6,6 s de tela vazia antes do 1º gatilho do B6-1 |
| 7 | PH | H1, H2 | 1.520 | 101,33 | 42 s | 0,103 | aprovado (alvos 01–02) | — |
| 8 | PA | A1 | 188 | 12,53 | 10 s | 2D | aprovado | — |
| 9 | PS | S1, S2 + CTA | 1.268 | 84,53 | 29 s | 2D | aprovado (alvos 17–18; cartão 8,2 s antes do CTA) | 7,8 s de tela vazia antes do 1º gatilho do S1 |
| — | Montagem | PH → PA → PB1 → PB2 → PB4 → PB5 → PB6 → PB7 → PS | 17.047 | 1.136,47 (18:56,47) | `renders/v1/yt_0045_preview_v1_540p15.mp4` | — | aprovado | voz, SRT e 1080p não iniciados (fora do escopo) |

QA (`renders/v1/qa/`): 18/18 alvos comparados em stills nativos 1920×1080; R5 = R5V = R6 = 0; flash = 0; R21 = 0; GM1–GM11 presentes;
68/68 degraus da proposta com tempo; gatilhos ≤ +0,27 s, nenhum sem frase; alinhamento 3D 0,000 px; palco 2D 0,00 px (81 medidas); nada < 26 px.

## Estado (Preview v2 — handoff v2, 2026-11-18)

Preview silencioso 960x540/15 fps: `renders/v2/yt_0045_preview_v2_540p15.mp4` (17.047 quadros, 18:56,47). QA em `renders/v2/qa/` (prancha `prancha_alvos_v2.jpg`, `lata_campo_v2.txt`).
Refeitos: PB7 (42 s), PH (23 s), PB4 (52 s), PB2 (53 s), PB5 (35 s), PB6 (41 s), PS (26 s); PA e PB1 reutilizam o v1.
Mudancas: lata e helice em projecao obliqua 2D (sem Three.js); setas do campo centradas nos nos da grade; narracao v1.1 (122 gatilhos, B6-1 e S1 sem tela vazia).
Pendencias: [vazio] H1 0,40–1,80 s (1o gatilho em 1,67 s); B4-2 termina em n = 16; gamma(−1) em x = 54 no B5; itens 24/25 por construcao. Voz, SRT e 1080p nao iniciados.

## Estado final (handoff final, 2026-11-18)

Master `renders/yt_0045_master_final_1080p30.mp4` (1920×1080, 30 fps, **CRF 14.0**, 17:50,23; voz 17:48,96 + 1,27 s de cauda do CTA). Legenda `legenda.srt` (287 blocos).
Voz: ElevenLabs `eleven_v4`, voz `qw7jgPZWOKrl10GsjQ82`, 4 blocos de API, uma tomada completa, 3,20 palavras/s (`audio/narracao_final.wav`; amostras em `audio/teste_pronuncia/`).
Narração: `referencia/yt_0045_narracao_v1_2_final.md` (3.424 palavras, 19 âncoras, 122 gatilhos).
Correções R1–R8 (prancha `renders/final/qa/correcoes_final.jpg`): R1 conta/seta F na 2ª volta; R2 eixo z cortado atrás da frente (corte de 10 px por lado, não 8: o aceite pede ≥ 6 px de folga do traço); R3 duas setas curtas no B7;
R4 2ª volta só no B7-3; R5 lata entra na 1ª palavra (H1) e junto do título (B7-1); R6 B4-3; R7 B6-1; R8 canto inteiro no quadro 0. Também: linha `= R²(…)` do B4-2 mais à esquerda (margem R6) e saída do S1 dentro da fala do S2.
Lata e hélice em projeção oblíqua 2D no papel (sem Three.js). `3d_threejs: nenhuma`, `solido_3d: nenhum do arsenal Blender`.
Sincronia (PRESSA, 2 passadas): 122 gatilhos de −0,21 a +0,13 s, 19 âncoras, 0 fora de ≤ +0,20 s; estouro único: S2 0,27 s (saída do S1). QA em `renders/final/qa/`.
Entrega: `entregas/Cálculo III - EP 20 - Integral de linha de um campo vetorial - 0045` (série/EP provisórios até o Kaio confirmar).
