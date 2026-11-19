# Exercícios do módulo: integral tripla

Série pública: **CÁLCULO III · EP. 19** (número `yt_0044` e EP. 19 provisórios até o Kaio confirmar)

```
formato: longo_horizontal
tipo: exercicios
serie_publica: CÁLCULO III · EP. 19
titulo: Exercícios do módulo: integral tripla
disciplina: Cálculo III
modulo: 3.5 Integral tripla
bloco: 3.5-E1
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, cap. 5 (exercícios 5.4-3, 5.4-4, 5.7-4/6 como base); didática do Stewart. Livro só na descrição do YouTube
unidades: x, y, z, s, r, R, h, L, d em metros; θ, φ, α em radianos; massa em kg; I em kg·m²
notacao: ρ = densidade; k = densidade constante; s = distância ao eixo; r = distância até a origem; φ e α só nas esféricas; R, h, L fixos; d = distância entre eixos; (x̄, ȳ, z̄) centro de massa; M_yz, M_xy momentos em relação aos planos; I_z, I_cm momentos de inércia; u, w substituições; n = divisões por aresta; Δ = maior lado
solido_3d: nenhum do arsenal Blender (tudo feito direto em Three.js)
3d_threejs: lataParede, cubo, cuboCaixas, cuboSonda, cuboDiag, cuboFolha, tetraSonda, tetraCent, tetraPlano, cone, coneCm, coneCasca, semi, semiFatia, lataDobradica, lataDob3, helice (geometria em referencia/yt_0044_quadros_alvo_v1/c3d44.html, cenas em cenas44.js)
duracao_alvo: ≈ 28:56 (narração v1: 5.168 palavras)
```

## Estado (Preview v1 — handoff v1.1, 2026-11-17)

Unidade-base (somente leitura): `videos_longos/yt_0043_centro_massa_momento_inercia/` — a `ficha.md` dela registra o preview v1 com os 7 lotes aprovados no QA e a entrega final (a unidade tem também os alvos v2). Reutilizados: `kit.py`, `v41.py` (sem mudança), `k43.py` → `k44.py`, scripts `render/render3d/seco/still.sh`, `montar.py`, `quadros.py`, `gerar_ancoras.py` (modo estimado), `qa43.py` → `qa44.py`, `threejs/r3d.js` e os helpers do `c43.js` → `c44.js`.

| Ordem | Lote | Âncoras | Quadros (15 fps) | Duração (s) | Render 540p15 (Manim) | 3D (render + cópias; s/quadro) | QA | Pendências |
|---:|---|---|---:|---:|---|---|---|---|
| 1 | PE3 | E3-1 a E3-4 | 4.055 | 270,33 | 122 s | 42 + 2.603; 0,134 | aprovado (alvos 12–15; GM11–GM15) | gatilho "Vezes k" a +0,33 s |
| 2 | PE5 | E5-1 a E5-3 | 3.243 | 216,20 | 188 s | 46 + 1.417; 0,170 | aprovado (alvos 19–21; GM17–GM19) | — |
| 3 | PE1 | E1-1 a E1-5 | 4.972 | 331,47 | 137 s | 79 + 3.652; 0,124 | aprovado (alvos 03–07; GM1–GM6) | — |
| 4 | PE2 | E2-1 a E2-4 | 4.280 | 285,33 | 118 s | 66 + 3.369; 0,134 | aprovado (alvos 08–11; GM7–GM10) | — |
| 5 | PE4 | E4-1 a E4-3 | 3.067 | 204,47 | 86 s | 32 + 2.110; 0,154 | aprovado (alvos 16–18; GM16) | — |
| 6 | PE6 | E6-1 a E6-3 | 3.117 | 207,80 | 68 s | 2D | aprovado (alvos 22–24; GM20–GM21) | — |
| 7 | PH | H1, H2 | 1.625 | 108,33 | 45 s | 27 + 850; 0,126 | aprovado (alvos 01–02) | — |
| 8 | PA | A1 | 223 | 14,87 | 9 s | 2D | aprovado | — |
| 9 | PS | S1, S2 + CTA | 1.450 | 96,67 | 53 s | 47 + 569; 0,117 | aprovado (alvos 25–26; cartão 8,2 s antes do CTA) | — |
| — | Montagem | PH → PA → PE1 → … → PE6 → PS | 26.032 | 1.735,47 (28:55,47) | `renders/v1/yt_0044_preview_v1_540p15.mp4` | 339 + 14.570 | aprovado (0 quadros pretos; emendas em `renders/v1/qa/emendas_v1.jpg`) | voz, SRT e 1080p não iniciados (fora do escopo) |

## Resumo do QA (`renders/v1/qa/`)

- 26/26 alvos comparados em stills nativos 1920×1080 no quadro exato de `self.marca` (`comparacao/`, `prancha_alvos.jpg`).
- Alinhamento 3D × Manim: pior 0,010 px (`alinhamento3d_v1.txt`).
- R5 = 0, R5V = 0, R6 = 0, eixo 3D × canto = 0, flash por quadro = 0, papel fora do CTA = 100 %.
- GM1–GM21 presentes; degraus da proposta 63/63 com tempo (C6.13 fora, por ser reserva).
- Gatilhos: 183 executados, nenhum sem frase, 1 acima de 0,30 s ("Vezes k", +0,33 s).
- Tamanhos: nada pedido abaixo de 26 px; alturas medidas nas caixas dos stills em `tamanhos_v1.txt`.

## Estado (Preview v2 — handoff v2, 2026-11-18)

Alvos v2 em `referencia/yt_0044_quadros_alvo_v2/` (o v1 foi mantido). Preview v2: `renders/v2/yt_0044_preview_v2_540p15.mp4` (26.032 quadros, 28:55,47; 0 quadros pretos). QA em `renders/v2/qa/` (Q1–Q29 + `comparacao_v2/`, `emendas_v2.jpg`, `q29_prancha_3d_v2.jpg`).

| Lote | Render Manim | 3D (render + cópias; s/quadro) | Observação |
|---|---|---|---|
| PE3 | 139 s | 58 + 2.597; 0,129 | cotas R/h, h/2 no quarto aberto, SNAP |
| PE2 | 198 s | 66 + 3.368; 0,147 | câmera nova do tetraedro (SC 2,4; DF 1,85) |
| PE1 | 172 s | 79 + 3.681; 0,124 | caixas sem arame, tique 1/2, cota Δz |
| PE4 | 121 s | 32 + 2.119; 0,154 | cartões do E4-3 com o degradê como imagem única |
| PE5 | 138 s | 46 + 1.417; 0,145 | piso finito, fio R/s, células ± |
| PH | 67 s | 27 + 850; 0,158 | cota 2R no lugar da placa EIXO |
| PS | 70 s | 47 + 589; 0,127 | hélice sem verticais |
| PE6 | 86 s | 2D | refeito: tinha 4 s de papel vazio no E6-1 e 1,4 s nos E6-2/E6-3 |
| PA | 16 s | 2D | refeito: último quadro limpo (emenda) |

- G8 (origem na grade): `cam44(snap=True)` desloca a câmera inteira; O cai em múltiplo de 60 px (erro 0,000 px). Alinhamento 3D × Manim: pior 0,010 px.
- Pendências do v1: gatilho "Vezes k" resolvido (maior atraso do vídeo agora +0,13 s); 0 pausas de papel vazio > 0,5 s; emendas com o fundo idêntico (o último quadro de cada lote agora é o papel limpo: o v1 terminava no meio do fade, a ~20 %).
- Não atendido: Q21 (piso inteiro). Com o `DF`, o `PISOK` e os deslocamentos OL/OC/OM do handoff, o piso passa do clip da coluna (e da margem esquerda) em 9 das 17 cenas, igual ao alvo v2; os sólidos, cotas e eixos ficam inteiros (Q26).

## Estado (Final · 2026-11-18)

- **Master:** `renders/yt_0044_master_final_1080p30.mp4` — 1920×1080, 30 fps, CRF 14.0, **duração real 27:04,57** (voz 27:03,44 + cauda de 1,13 s do CTA).
- **Voz:** ElevenLabs v4, voz `qw7jgPZWOKrl10GsjQ82`, 6 blocos de API, WAV 27:03,44 (`audio/narracao_final.wav`), 3,20 palavras/s (5.191 palavras).
- **Correções de tela:** F1 piso octogonal (apótema 1,25 lataParede/hélice; 1,1 lataDobradica/lataDob3/cone*/semi*), F2 células e placas da `lataDob3`, F3 placas 1/2 e 5/9, F4 canto inteiro no quadro 0, F5 seta/placa/legenda do F em #2EE6A0.
- **Sync:** 27 âncoras, 184 gatilhos, atraso de −0,25 a +0,16 s no 1080p30. **Legenda:** `legenda.srt` (439 blocos). **Capítulos:** `renders/capitulos_final.txt`.
- Número `yt_0044` e EP. 19 provisórios até o Kaio confirmar.
