# Centro de massa e momento de inércia na integral tripla

Série pública: **CÁLCULO III · EP. 18**

```
formato: longo_horizontal
tipo: teoria_visual
serie_publica: CÁLCULO III · EP. 18
titulo: Centro de massa e momento de inércia na integral tripla
disciplina: Cálculo III
modulo: 3.5 Integral tripla
bloco: 3.5-T4
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §5.7, com apoio didático de Stewart §15.8. Livro só na descrição do YouTube
unidades: massa em kg; momento de inércia em kg·m²; distâncias x, y, z, s, r, R, h, s_G em m; θ, φ, t em radianos
notacao: ρ = densidade; k = densidade constante; s = distância ao eixo z; r = distância à origem; φ = ângulo esférico; R, h = raio e altura fixos; (x̄, ȳ, z̄) = centro de massa; (M_yz, M_xz, M_xy) = momentos em relação aos planos; I_z = momento de inércia em relação ao eixo z; s_G = raio de giração; u, w, t = variáveis auxiliares; I_n = integral de sec^n t de 0 a π/4
solido_3d: nenhum do arsenal Blender (todos os sólidos feitos direto em Three.js)
3d_threejs: lataGiro, lataPesada, lataDuas, cmPontos, lataCel, lataPlano, lataSim, lataSim2, taca, giroCel, distEixo, cilindroH, esferaOct, lataParede (geometria em referencia/yt_0043_quadros_alvo_v1/c3d43.html)
duracao_alvo: ≈ 21:48 (narração v1: 3.892 palavras)
duracao_real: 21:05,40 (master 1080p30; voz 21:04,40 + cauda de 1,0 s do CTA; narração v1.1: 4.122 palavras, 3,26 palavras/s; ElevenLabs eleven_v4, voz qw7jgPZWOKrl10GsjQ82)
```

## Estado (Preview v1 — handoff v1.1, 2026-11-17)

Unidade-base utilizada (somente leitura): `videos_longos/yt_0041_coordenadas_esfericas/` no estado validado de preview v4 (conforme §0.3, pois `yt_0042` não registrava aprovação do handoff v1.2 em `ficha.md`).

| Ordem | Lote | Âncoras | Quadros (15 fps) | Duração (s) | Render 540p15 | 3D (quadros / tempo) | QA | Pendências |
|---:|---|---|---:|---:|---|---|---|
| 1 | PB2 | B2-1, B2-2 | 2.099 | 139,93 s (2:19,93) | concluído (59 s) | 39 render + 2.067 cópias (5,0 s; 0,1294 s/q) | aprovado (alvos 08–09; alin. 0,000 px) | - |
| 2 | PB1 | B1-1 a B1-3 | 3.322 | 221,47 s (3:41,47) | concluído (110 s) | 80 render + 3.247 cópias (9,5 s; 0,1184 s/q) | aprovado (alvos 03–07; alin. máx 0,010 px) | - |
| 3 | PB3 | B3-1 a B3-5 | 4.928 | 328,53 s (5:28,53) | concluído (137 s) | 119 render + 3.966 cópias (13,4 s; 0,1129 s/q) | aprovado (alvos 10–14; alin. 0,000 px) | - |
| 4 | PB4 | B4-1 a B4-6 | 6.295 | 419,67 s (6:59,67) | concluído (165 s) | 48 render + 3.295 cópias (7,0 s; 0,1459 s/q) | aprovado (alvos 15–20; alin. 0,000 px) | - |
| 5 | PH | H1, H2 | 1.650 | 110,00 s (1:50,00) | concluído (55 s) | 62 render + 1.590 cópias (7,5 s; 0,1203 s/q) | aprovado (alvos 01–02; alin. máx 0,010 px) | - |
| 6 | PA | A1 | 278 | 18,53 s (0:18,53) | concluído (10 s) | 2D (sem cena 3D) | aprovado | - |
| 7 | PS | S1, S2 | 1.040 | 69,33 s (1:09,33) | concluído (26 s) | 16 render + 418 cópias (2,0 s; 0,1235 s/q) | aprovado (alvo 21; alin. 0,000 px) | - |
| 8 | Montagem | PH → PA → PB1 → PB2 → PB3 → PB4 → PS | 19.612 | 1.307,47 s (21:47,47) | `renders/v1/yt_0043_preview_v1_540p15.mp4` | 364 render + 14.583 cópias (44,4 s) | aprovado (23/23 alvos 1080p, GM1–GM18, R5=0, R6=0, flash=0) | Voz, SRT e master 1080p não iniciados (fora do escopo do preview) |

## Resumo do QA (`renders/v1/qa/`)

- **Alinhamento 3D × Manim (`alinhamento3d_v1.txt`):** pior erro `0,010 px` em 44.575 amostras nas 14 cenas 3D (limite ≤ 2,0 px).
- **Tamanhos tipográficos (`tamanhos_v1.txt`):** 338 elementos registrados; mínimo absoluto `26 px`, zero ocorrências abaixo de 26 px.
- **Sincronização de gatilhos (`gatilhos_v1.txt`):** 149 gatilhos acionados + 1 início de âncora (`A1`); maior desvio `+0,27 s` (limite ≤ 0,30 s); gatilhos sem frase = `0`.
- **Sobreposições e margens (`sobreposicoes_v1.txt`):** `R5 = 0`, `R5V = 0`, `R6 = 0`, `EIXO 3D × CANTO = 0`.
- **Escrita e animações (`flash_por_quadro_v1.txt`, `glyph_maps_v1.txt`, `origens_v1.txt`, `conta_inteira_v1.txt`):** `FLASH POR QUADRO = 0`, `GM1–GM18` presentes (`faltando = []`, avisos = `0`), 5 voos geométricos registrados, 84 escritas a caneta registradas.
- **Grade e palco (`grade_v1.txt`, `palco_parado_v1.txt`, `texto_em_mathtex_v1.txt`):** `SEM-GRADE fora do CTA = 0` (`3D-grade = 995 s`, `2D-grade = 306 s`, `CTA-liso = 9 s`), `palco vazio > 0,5 s = 0`, `canto sem linha 2 = 0`, `PALAVRA-EM-MATHTEX = 0`.
