# Coordenadas esféricas na integral tripla

Série pública: **CÁLCULO III · EP. 16**

```
formato: longo_horizontal
tipo: teoria_visual
serie_publica: CÁLCULO III · EP. 16
titulo: Coordenadas esféricas na integral tripla
disciplina: Cálculo III
modulo: 3.5 Integral tripla (o docs/mapa_curricular.md do repositório ainda usa a numeração antiga)
bloco: 3.5-T2
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §5.5 (coordenadas esféricas; teorema de mudança de variáveis; Ex. 5, bola com densidade igual à distância; Exercício 5.5-4, cone + esfera); Stewart §15.8 (cunha esférica, casquinha). Só na descrição do YouTube: nada de livro na tela nem na fala
unidades: r, x, y, z, s e R em metros; φ e θ em radianos; volumes em m³
notacao: igual aos vídeos da lei de Gauss: ρ = densidade; r = distância ao centro (variável); R = raio fixo da bola (no lugar do a dos episódios anteriores); s = r sen φ, a sombra no chão (como o s do Griffiths); φ = ângulo a partir de +z, em [0, π]; θ = ângulo das polares; T = a transformação
solido_3d: nenhum do arsenal Blender (bola, cascas, cones, caixa e lata feitos direto em Three.js)
3d_threejs: bola (octante com degradê de densidade e contorno r = 0,84), grade, ponto, caixa, caixa2, bolagrade, caixinha, cebola (octante), receita (sólida), casquinha, lata; piso z = 0 e papel sob o 3D (geometria portada de yt_0041_quadros_alvo_v3/c3d41.html)
duracao_alvo: 20:53,77 (voz v1.5 ElevenLabs de 20:52,56, sem a frase extra do fim do S2, + 1,2 s de cauda do CTA; 4.027 palavras, 3,22 palavras/s)
```

## Estado

- **FINAL (handoff final, 2026-11-17):** voz ElevenLabs v4 (voz qw7jgPZWOKrl10GsjQ82), `audio/narracao_final.wav` (20:52,56), alinhamento forçado,
  âncoras em tempo real (`gerar_ancoras.py`), PRESSA (`k41.py`, piso 0,6), 19 âncoras, 299 gatilhos com atraso de −0,18 a +0,27 s.
  Master 1080p30 CRF 14 em `renders/yt_0041_master_final_1080p30.mp4`; legenda `legenda.srt`; capítulos `renders/capitulos_final.txt`; QA em `renders/final/`.
- **Frase extra no fim do S2:** a narração v1.5 trazia, depois de "Até a próxima!", a frase "E dá para ver de onde vêm os dois r: …" (acréscimo que era do B2-2).
  Ela foi cortada do WAV, do alinhamento, do texto e da legenda; originais em `audio/narracao_final_ORIGINAL_com_frase_extra.wav`,
  `alinhamento_palavras_ORIGINAL.json` e `referencia/yt_0041_narracao_v1_5_ORIGINAL.md`. Para ter a frase no B2-2 é preciso regerar a voz.
- Histórico: previews v1–v4 (silenciosos) em `renders/v1` … `renders/v4`; v5 = 540p com a voz.

## Pipeline (como rodar)

- Âncoras estimadas (3 palavras/s + 0,15 s antes + 0,35 s depois): `python gerar_ancoras.py` → `ancoras.json`, `duracoes_estimadas.json`.
- Lote 2D: `./render.sh PA`. Lote com 3D: `./render3d.sh PB1` (passada seca → `threejs/pedidos3d/PB1.json` → `node threejs/r3d.js` → PNGs com alfa em
  `threejs/q3d/PB1_960x540/<cena>/` + `pontos.json` → render do Manim). Passada seca rápida: `./seco.sh PB1`.
- Montagem: `python montar.py` (ordem PH, PA, PB1 … PB7, PS). QA: `python qa41.py`. Quadros soltos: `python quadros.py PB1 86.5 140.3`.
- Miniaturas 3D (B2-1, B7, S1): `python threejs/minis41.py`. Sonda das cenas contra os alvos: `python threejs/sonda41.py`.

## Arquivos

- `kit.py` (cópia do kit do yt_0037, título INTEGRAL TRIPLA), `v41.py` (cópia do v37.py; parte/junta do lib37), `k41.py` (desta unidade: macros do
  sb41, câmeras/pontos do c41.js, base `B41`, caneta, voos, glyph maps do MF-Tools, QA por quadro), `sec_h.py`, `sec_a.py`, `sec_b1.py` … `sec_b7.py`,
  `sec_s.py`, `cena.py`.
- `threejs/cena3d/c41.js` (porte do `c3d41.html` com os estados animáveis) + uma página por cena; `threejs/r3d.js` (do yt_0037).
- `referencia/` (handoff, narração, proposta, quadros-alvo e geradores), `verificacao/` (sympy 63/63).
