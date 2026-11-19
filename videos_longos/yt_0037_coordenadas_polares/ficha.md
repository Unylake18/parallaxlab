# Coordenadas polares na integral dupla

Série pública: **CÁLCULO III · EP. 12**

```
formato: longo_horizontal
tipo: teoria_visual
serie_publica: CÁLCULO III · EP. 12
titulo: Coordenadas polares na integral dupla
disciplina: Cálculo III
modulo: 3.4 Mudança de variáveis na integral dupla (o docs/mapa_curricular.md do repositório ainda usa a numeração antiga)
bloco: 3.4-T2
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §4.1 (polares) e §4.2 (teorema de mudança de variáveis; Ex. 5, integral de Gauss pelo confronto); Stewart §15.3 (setores, disco x² + y² ≤ 2x). Só na descrição do YouTube: nada de livro na tela nem na fala
unidades: x, y, r e a em metros; θ em radianos; áreas em m²
solido_3d: nenhum do arsenal Blender (o sino z = e^(−(x²+y²)) sobre o disco e sobre o quadrado, feito direto em Three.js como nos EP. 05 a 10)
3d_threejs: sino = z = e^(−(x²+y²)) sobre o disco unitário (H1); casca = o mesmo sino virando traço com a casca fina r₀ ≤ r ≤ r₀ + 0,10 e o anel lima inteiro no chão (B4-1 com traco = 0, B4-2; porte da chave casca do c3d34t2.html v2); gauss = o sino sobre o quadrado [−a, a]² com o disco inscrito e o circunscrito no chão (B6), com a câmera subindo até a vista de cima e a troca para o 2D do alvo v2_03
duracao_alvo: 15:59,20 (voz v3.1 de 15:55,44 + 3,76 s de CTA; 3.081 palavras)
```

## Estado

- 2026-11-14 · handoff v1 (`yt_0037_handoff_v1.md`, narração `yt_0037_narracao_v2.md`): preview visual silencioso do vídeo inteiro,
  960×540 / 15 fps, em `renders/v1/`. Sem voz, SRT, master, 1080p nem entrega. Sem commit.
- 2026-11-14 · handoff v2 (`yt_0037_v1_avaliacao_e_handoff_v2.md`, narração `yt_0037_narracao_v2_1.md`, alvos em `referencia/handoff_v2/`):
  regras G1–G8 e correção de E01–E42; todas as seções refeitas; preview v2 em `renders/v2/` com o QA do §7 em `renders/v2/qa/`. O v1 ficou
  copiado em `renders/v1/` (código em `renders/v1/codigo_v1/`, logs em `renders/v1/logs_v1/`). Sem voz, SRT, master, 1080p nem entrega. Sem commit.

## Estrutura

- `cena.py`: um lote por bloco (`PH`, `PA`, `PB1`…`PB7`, `PS`; `PT` é só teste do kit). Lotes com 3D: `PH` (sino), `PB4` (casca), `PB6` (gauss).
- Kit copiado do yt_0035 (sem importar): `kit.py`, `v37.py`, `lib37.py`, `pecas37.py`, `p37.py`; peças deste vídeo em `polar37.py`;
  regras do v2 em `v2kit.py` (tamanhos G1, `escreve_seq` na ordem de leitura com voos e arco por voo, molduras ligadas ao texto, auditorias
  de esqueleto/caixa vazia/duplicado/coluna ao fim de cada play e o R5 v2 com folga 10 px, borda 40 px e texto × alfa do 3D).
- `threejs/`: `cena3d/c37.js` (`sino`, `casca`, `gauss`; a câmera vem do Manim), `sino.html`, `casca.html`, `gauss.html`, `r3d.js`,
  `pedidos3d/`, `q3d/`. Câmeras v2 em `p37.py`: `CAM_CASCA` e `CAM_GAUSS2` (alfa dentro de x ∈ [40, 1010], y ∈ [170, 1050]).
- `gerar_ancoras.py` → `ancoras.json` e `duracoes_estimadas.json` (0,15 + palavras/3 + 0,35 s por âncora; 16:01,15).
- Render: `./render.sh LOTE` (2D), `./render3d.sh LOTE` (3D), `./render_todos.sh` (fila), `./seco.sh LOTE` (passada seca), `python montar.py v2`.
- QA: `python qa_v2.py` → `renders/v2/qa/` (o `qa37.py` do v1 continua para `renders/v1/`). Conferência numérica: `verificacao/verif_numerica.py`
  (o sympy não está na `.venv`).
