# Coordenadas cilíndricas na integral tripla

Série pública: **CÁLCULO III · EP. 17**

```
formato: longo_horizontal
tipo: teoria_visual
serie_publica: CÁLCULO III · EP. 17
titulo: Coordenadas cilíndricas na integral tripla
disciplina: Cálculo III
modulo: 3.5 Integral tripla
bloco: 3.5-T3
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §5.6 (Ex. 1 lata com densidade √(x²+y²+z²); Ex. 2 cilindro fora do eixo). Livro só na descrição do YouTube
unidades: s, r, x, y, z, R, h em metros; θ e t em radianos; volumes em m³
notacao: s = distância ao eixo z; θ = ângulo das polares; z = altura; r = distância até a origem (r² = s² + z²); ρ = densidade; R, h = raio e altura fixos; T = a transformação; u, t = substituições
solido_3d: nenhum do arsenal Blender (lata, grade, ponto, caixa, latagrade, caixinha, cilindro, deslocado, giro feitos direto em Three.js)
3d_threejs: lata, grade, ponto, caixa, latagrade, caixinha, cilindroRot, deslocadoSonda, giro (geometria em referencia/yt_0042_quadros_alvo_v1/c3d42.html)
duracao_alvo: ≈ 20:11 (narração v1: 3.600 palavras)
```

## Estado

- **Preview v1 (handoff v1, 2026-11-16):** preview silencioso 960×540 / 15 fps do vídeo inteiro em `renders/v1/yt_0042_preview_v1_540p15.mp4`
  (20:11, 18.165 quadros). QA em `renders/v1/qa/` (`python qa42.py`): flash 0, R6 0, texto-em-MathTex 0, GM1–GM14 100%,
  gatilhos 0 ausentes, alinhamento 3D pior 0,014 px (limite 2 px). Voz, SRT, master, 1080p e entrega **não** iniciados.

## Pipeline (como rodar)

- Âncoras estimadas (3 palavras/s + 0,15 s antes + 0,35 s depois): `python gerar_ancoras.py` → `ancoras.json`, `duracoes_estimadas.json`.
- Lote 2D: `./render.sh PA`. Lote com 3D: `./render3d.sh PB1` (passada seca → `threejs/pedidos3d/PB1.json` → `node threejs/r3d.js` → PNGs com alfa em
  `threejs/q3d/PB1_960x540/<cena>/` + `pontos.json` → render do Manim). Passada seca rápida: `./seco.sh PB1`.
- Montagem: `python montar.py` (ordem PH, PA, PB1 … PB6, PS). QA: `python qa42.py`.

## Arquivos

- `kit.py` (cópia do kit do yt_0041, título INTEGRAL TRIPLA), `v42.py` (cópia do v41.py), `k42.py` (desta unidade: macros do sb42,
  câmeras/pontos do c42.js, base `B42`), `sec_h.py`, `sec_a.py`, `sec_b1.py` … `sec_b6.py`, `sec_s.py`, `cena.py`.
- `threejs/cena3d/c42.js` (porte do `c3d42.html` com os estados animáveis) + uma página por cena; `threejs/r3d.js`.
- `referencia/` (handoff, narração, proposta, quadros-alvo e geradores), `verificacao/` (sympy 56/56).
